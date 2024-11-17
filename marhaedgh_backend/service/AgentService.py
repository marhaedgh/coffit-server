import json
import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from langchain.text_splitter import CharacterTextSplitter
from sqlalchemy.orm import Session

from llama_index.core import Settings

from dto.JsonInferResponse import JsonInferResponse
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
            Settings.llm.acomplete(layer0_title_request),
            Settings.llm.acomplete(layer0_keywords_request),
            Settings.llm.acomplete(layer0_summarization_request),
            Settings.llm.acomplete(layer0_whattodo_request)
        )

        layer1_line_summarization_request = await self.prepare_json_infer_request(context, "./prompt/line_summarization.json")
        layer1_line_summarization = await Settings.llm.acomplete(layer1_line_summarization_request)

        """
        #layer 추가시 아래와 같은 형식으로 추가하기. 하나일 경우 그냥 await
        layer1_line_summarization_request = await asyncio.gather(
            self.prepare_json_infer_request(context, "./prompt/line_summarization.json"),
        )

        layer1_line_summarization = await asyncio.gather( 
            Settings.llm.acomplete(layer1_line_summarization_request),
        )
        """

        title = str(layer0_title)
        keyword = str(layer0_keywords)
        line_summarization = str(layer1_line_summarization)
        summarization = str(layer0_summarization)
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
            Settings.llm.acomplete(layer0_title_request),
            Settings.llm.acomplete(layer0_keywords_request),
            Settings.llm.acomplete(layer0_summarization_request),
            Settings.llm.acomplete(layer0_classification_request),
            Settings.llm.acomplete(layer0_whattodo_request)
        )

        layer1_line_summarization_request = await self.prepare_request(content, "./prompt/line_summarization.json")
        layer1_line_summarization = await Settings.llm.acomplete(layer1_line_summarization_request)

        """
        #layer 추가시 아래와 같은 형식으로 추가하기. 하나일 경우 그냥 await
        layer1_line_summarization_request = await asyncio.gather(
            self.prepare_request(content, "./prompt/line_summarization.json"),
        )

        layer1_line_summarization = await asyncio.gather( 
            Settings.llm.acomplete(layer1_line_summarization_request),
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