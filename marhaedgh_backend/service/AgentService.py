import json
import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from langchain.text_splitter import CharacterTextSplitter
from sqlalchemy.orm import Session

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


    async def prepare_request(self, content, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        return self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)


    async def demon_alert_response_efficient(self, url):
        #URL 타고 들어가서 본문내용(PDF) 추출 후 텍스트로 변환 //일단 html스크랩

        output_dir = "./rag_data"  # 저장할 디렉토리 경로
        # URL에서 텍스트 추출 및 저장
        content = extract_text_from_url(url, output_dir)

        # 배치로 요청을 처리합니다.
        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        # 각 추론 요청에 필요한 JSON 파일을 로드하고 메시지를 생성합니다.
        layer0_tasks = [
            await self.prepare_request(content, "./prompt/title.json"),                   #제목
            await self.prepare_request(content, "./prompt/keywords.json"),                #키워드
            await self.prepare_request(content, "./prompt/summarization_korean.json"),    #요약
            await self.prepare_request(content, "./prompt/classification.json"),          #분류
            await self.prepare_request(content, "./prompt/whattodo.json"),                #할일
        ]

        layer0_results = await self.modelLoader.run_multi(layer0_tasks, sampling_params)

        layer1_tasks = [
            await self.prepare_request(
                layer0_results[2].outputs[0].text,
                "./prompt/line_summarization.json"                               #요약 -> 한줄요약
            )
        ]

        layer1_results = await self.modelLoader.run_multi(layer1_tasks, sampling_params)

        # 여기서 레이어링 / 멀티 단위로 해서 더 빠르게 처리

        title = layer0_results[0].outputs[0].text
        keyword = layer0_results[1].outputs[0].text
        summarizations = [layer0_results[2].outputs[0].text, layer1_results[0].outputs[0].text]
        classification = layer0_results[3].outputs[0].text
        whattodo = layer0_results[4].outputs[0].text

        # 데이터베이스에 저장
        db: Session = next(get_db())
        business_data_repository = BusinessDataRepository(db)
        business_data_id = 0  # 예시값

        alert_repository = AlertRepository(db)
        gen_alert = alert_repository.create({
            "business_data_id": business_data_id,
            "title": title,
            "keywords": json.dumps({"keywords": keyword}),
            "line_summarization": summarizations[1],
            "text_summarization": summarizations[0],
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
            line_summarization=summarizations[1],
            summarization=summarizations[0],
            classification=classification,
            what_to_do=whattodo
        )

        return demon_infer_response
        

    #세부내용 리포트(마크다운)생성 에이전트