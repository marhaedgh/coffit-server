import json
import asyncio
from sqlalchemy.orm import Session

from dto.CreateBusinessResponse import CreateBusinessResponse
from dto.JsonInferResponse import JsonInferResponse
from dto.DemonInferResponse import DemonInferResponse
from db.database import get_db
from repository.BusinessDataRepository import BusinessDataRepository
from repository.AlertRepository import AlertRepository
from repository.UserAlertMappingRepository import UserAlertMappingRepository
from repository.UserRepository import UserRepository

from util.CrawllerForPresentation import url_to_filename
from util.CrawllerForPresentation import extract_text_from_url


class AgentService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader


    async def prepare_json_infer_request(self, context, json_path):

        with open(json_path, 'r', encoding='utf-8') as file:
            json_str = file.read()

        if "{context}" in json_str:
            context_str = json.dumps(context, ensure_ascii=False).replace('"', '\\"')
            json_str = json_str.replace("{context}", context_str)
            
        json_data = json.loads(json_str)

        return self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)


    async def prepare_request(self, content, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        return self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)
    

    async def prepare_classification_request(self, user_business_data, alerts, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_str = file.read()
        
        if "{business_data}" in json_str:
            json_str = json_str.replace("{business_data}", str(user_business_data))
        
        results = []
        for alert in alerts:
            temp_json_str = json_str.replace("{context}", str(alert))
            
            json_data = json.loads(temp_json_str)
            
            result = self.modelLoader.tokenizer.apply_chat_template(
                json_data,
                add_generation_prompt=True,
                tokenize=False
            )
            results.append(result)
        
        return results


    async def initial_mapping_notifications(self, create_business_response:CreateBusinessResponse):
        user_id = create_business_response.user_id
        business_data_id = create_business_response.business_data_id

        db: Session = next(get_db())

        alert_repository = AlertRepository(db)
        alerts = alert_repository.get_all()

        business_repository = BusinessDataRepository(db)
        user_business_data = business_repository.get_by_id(business_data_id)

        layer0_classification_requests = await self.prepare_classification_request(user_business_data, alerts, "./prompt/classification.json")

        semaphore = asyncio.Semaphore(4)
        tasks = []
        layer0_classifications = []

        async def limited_acomplete(request):
            async with semaphore:
                return await self.modelLoader.llm_llama.acomplete(request)

        for request in layer0_classification_requests:
            task = asyncio.create_task(limited_acomplete(request))
            tasks.append(task)

        if tasks:
            results = await asyncio.gather(*tasks)
            layer0_classifications += results

        print(layer0_classifications)
        user_alert_mapping_repository = UserAlertMappingRepository(db)
        for i in range(len(layer0_classifications)):
            response_text = layer0_classifications[i].text
            print(response_text)
            
            if response_text > "0":
                user_alert_mapping_repository.create({
                    "user_id": user_id,
                    "alert_id": alerts[i].id  
                })
                
        return 0


    async def json_alert_infer_request(self, context):
        # 1. 준비 요청을 비동기로 병렬 수행하고 결과를 가져옴
        layer0_title_request, layer0_keywords_request, layer0_summarization_request, layer0_whattodo_request = await asyncio.gather(
            self.prepare_json_infer_request(context, "./prompt/title.json"),
            self.prepare_json_infer_request(context, "./prompt/keywords.json"),
            self.prepare_json_infer_request(context, "./prompt/summarization_korean.json"),
            self.prepare_json_infer_request(context, "./prompt/whattodo.json")
        )

        # 2. acompletion 요청을 병렬로 수행하고 결과를 가져옴
        layer0_title, layer0_keywords, layer0_summarization, layer0_whattodo = await asyncio.gather(
            self.modelLoader.llm_llama.acomplete(layer0_title_request),
            self.modelLoader.llm_llama.acomplete(layer0_keywords_request),
            self.modelLoader.llm_llama.acomplete(layer0_summarization_request),
            self.modelLoader.llm_llama.acomplete(layer0_whattodo_request)
        )

        #layer1_line_summarization_request = await self.prepare_json_infer_request(context, "./prompt/line_summarization.json")
        #layer1_line_summarization = await self.modelLoader.llm_llama.acomplete(layer1_line_summarization_request)

        layer1_line_summarization_request, layer1_convert_to_chatting_request = await asyncio.gather(
            self.prepare_json_infer_request(context, "./prompt/line_summarization.json"),
            self.prepare_json_infer_request(context, "./prompt/convert_to_chatting.json")
        )
        layer1_line_summarization, layer1_convert_to_chatting = await asyncio.gather(
            self.modelLoader.llm_llama.acomplete(layer1_line_summarization_request),
            self.modelLoader.llm_llama.acomplete(layer1_convert_to_chatting_request)
        )

        """
        #layer 추가시 아래와 같은 형식으로 추가하기. 하나일 경우 그냥 await
        layer2_line_summarization_request = await asyncio.gather(
            self.prepare_json_infer_request(context, "./prompt/line_summarization.json"),
        )

        layer2_line_summarization = await asyncio.gather( 
            self.modelLoader.llm_llama.acomplete(layer2_line_summarization_request),
        )
        """

        title = str(layer0_title)
        keyword = str(layer0_keywords)
        line_summarization = str(layer1_line_summarization)
        #summarization = str(layer0_summarization)
        summarization = str(layer1_convert_to_chatting) #채팅 형식으로 된거 요약에 저장, 사용자에게 제공
        whattodo = str(layer0_whattodo)


        db: Session = next(get_db())

        alert_repository = AlertRepository(db)
        gen_alert = alert_repository.create({
            "title": title,
            "keywords": keyword,
            "line_summarization": line_summarization,
            "text_summarization": summarization,
            "task_summarization": whattodo
        })

        """
        user_alert_mapping_repository = UserAlertMappingRepository(db)
        user_alert_mapping_repository.create({
            "user_id": 0,
            "alert_id": gen_alert.id
        })
        """

        json_infer_response = JsonInferResponse(
            title=title, 
            keywords=keyword,
            line_summarization=line_summarization,
            summarization=summarization,
            what_to_do=whattodo
        )

        return json_infer_response


    async def demon_alert_response_efficient(self, url):
        #URL 타고 들어가서 본문내용(PDF) 추출 후 텍스트로 변환 //일단 html스크랩

        output_dir = "./rag_data/data"

        content = extract_text_from_url(url, output_dir)

        # 1. 준비 요청을 비동기로 병렬 수행하고 결과를 가져옴
        layer0_title_request, layer0_keywords_request, layer0_summarization_request, \
        layer0_classification_request, layer0_whattodo_request = await asyncio.gather(
            self.prepare_request(content, "./prompt/title.json"),
            self.prepare_request(content, "./prompt/keywords.json"),
            self.prepare_request(content, "./prompt/summarization_korean.json"),
            self.prepare_request(content, "./prompt/classification.json"),
            self.prepare_request(content, "./prompt/whattodo.json")
        )

        # 2. acompletion 요청을 병렬로 수행하고 결과를 가져옴
        layer0_title, layer0_keywords, layer0_summarization, \
        layer0_classification, layer0_whattodo = await asyncio.gather(
            self.modelLoader.llm_llama.acomplete(layer0_title_request),
            self.modelLoader.llm_llama.acomplete(layer0_keywords_request),
            self.modelLoader.llm_llama.acomplete(layer0_summarization_request),
            self.modelLoader.llm_llama.acomplete(layer0_classification_request),
            self.modelLoader.llm_llama.acomplete(layer0_whattodo_request)
        )

        layer1_line_summarization_request = await self.prepare_request(content, "./prompt/line_summarization.json")
        layer1_line_summarization = await self.modelLoader.llm_llama.acomplete(layer1_line_summarization_request)

        """
        #layer 추가시 아래와 같은 형식으로 추가하기. 하나일 경우 그냥 await
        layer1_line_summarization_request = await asyncio.gather(
            self.prepare_request(content, "./prompt/line_summarization.json"),
        )

        layer1_line_summarization = await asyncio.gather( 
            self.modelLoader.llm_llama.acomplete(layer1_line_summarization_request),
        )
        """


        title = str(layer0_title)
        keyword = str(layer0_keywords)
        line_summarization = str(layer1_line_summarization)
        summarization = str(layer0_summarization)
        classification = str(layer0_classification)
        whattodo = str(layer0_whattodo)


        db: Session = next(get_db())
        business_data_repository = BusinessDataRepository(db)
        business_data_id = 0  # 예시값

        alert_repository = AlertRepository(db)
        gen_alert = alert_repository.create({
            "business_data_id": business_data_id,
            "title": title,
            "keywords": json.dumps({"keywords": keyword}),
            "line_summarization": line_summarization,
            "text_summarization": summarization,
            "task_summarization": whattodo
            #"due_date":
        })

        user_alert_mapping_repository = UserAlertMappingRepository(db)
        user_alert_mapping_repository.create({
            "user_id": 0,
            "alert_id": gen_alert.id
        })


        demon_infer_response = DemonInferResponse(
            title=title, 
            keywords=keyword,
            line_summarization=line_summarization,
            summarization=summarization,
            classification=classification,
            what_to_do=whattodo
        )


        return demon_infer_response
        

    #세부내용 리포트(마크다운)생성 에이전트