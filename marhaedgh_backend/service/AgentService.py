import json
import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from langchain.text_splitter import CharacterTextSplitter

from dto.DemonInferResponse import DemonInferResponse

from util.CrawllerForPresentation import url_to_filename
from util.CrawllerForPresentation import extract_text_from_url


class AgentService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader
        

    async def demon_alert_response(self, url):
        #URL 타고 들어가서 본문내용(PDF) 추출 후 텍스트로 변환 //일단 html스크랩

        output_dir = "/home/guest/marhaedgh/marhaedgh_backend/rag_data"  # 저장할 디렉토리 경로
        # URL에서 텍스트 추출 및 저장
        content = extract_text_from_url(url, output_dir)

        title = await self.create_title(content)
        keyword = await self.create_keywords(content)
        summarization = await self.create_summarization(content)
        classification = await self.create_classification(content)
        whattodo = await self.create_whattodo(content)

        demon_infer_response = DemonInferResponse(
            title = title, 
            keywords = keyword,
            summarization = summarization,
            classification = classification,
            what_to_do = whattodo
        )

        return demon_infer_response


    #제목생성
    async def create_title(self, content):
        # JSON 파일 로드
        with open("/home/guest/marhaedgh/marhaedgh_backend/prompt/title.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)  # JSON 파일을 파이썬 객체로 로드

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        # 여러 역할별로 `apply_chat_template`을 사용하여 메시지를 인코딩합니다.
        encoded_message = self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)

        #여기서 프롬프트 레이어도 쌓을 수 있음

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '0'

        #chat = self.modelLoader.tokenizer.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(encoded_message, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        title = result.outputs[0].text

        return title

    
    #키워드 생성
    async def create_keywords(self, content):
        # JSON 파일 로드
        with open("/home/guest/marhaedgh/marhaedgh_backend/prompt/keywords.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)  # JSON 파일을 파이썬 객체로 로드

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        # 여러 역할별로 `apply_chat_template`을 사용하여 메시지를 인코딩합니다.
        encoded_message = self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)

        #여기서 프롬프트 레이어도 쌓을 수 있음

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '1'

        #chat = self.modelLoader.tokenizer.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(encoded_message, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        keywords = result.outputs[0].text

        return keywords


    #분류 생성
    async def create_classification(self, content):
        # JSON 파일 로드
        with open("/home/guest/marhaedgh/marhaedgh_backend/prompt/classification.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)  # JSON 파일을 파이썬 객체로 로드

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        # 여러 역할별로 `apply_chat_template`을 사용하여 메시지를 인코딩합니다.
        encoded_message = self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)

        #여기서 프롬프트 레이어도 쌓을 수 있음

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '2'

        #chat = self.modelLoader.tokenizer.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(encoded_message, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        classification = result.outputs[0].text

        return classification


    #요약 생성
    async def create_summarization(self, content):
        # JSON 파일 로드
        with open("/home/guest/marhaedgh/marhaedgh_backend/prompt/summarization.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)  # JSON 파일을 파이썬 객체로 로드

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        # 여러 역할별로 `apply_chat_template`을 사용하여 메시지를 인코딩합니다.
        encoded_message = self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)

        #여기서 프롬프트 레이어도 쌓을 수 있음

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '3'

        #chat = self.modelLoader.tokenizer.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(encoded_message, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        summarization = result.outputs[0].text

        return summarization


    #할일 생성
    async def create_whattodo(self, content):
        # JSON 파일 로드
        with open("/home/guest/marhaedgh/marhaedgh_backend/prompt/whattodo.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)  # JSON 파일을 파이썬 객체로 로드

        if len(json_data) >= 2 and 'content' in json_data[1]:
            json_data[1]['content'] = content + json_data[1]['content']

        # 여러 역할별로 `apply_chat_template`을 사용하여 메시지를 인코딩합니다.
        encoded_message = self.modelLoader.tokenizer.apply_chat_template(json_data, add_generation_prompt=True, tokenize=False)

        #여기서 프롬프트 레이어도 쌓을 수 있음

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '4'

        #chat = self.modelLoader.tokenizer.apply_chat_template(chat, add_generation_prompt=True, tokenize=False)
        result = await self.modelLoader.run_single(encoded_message, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        whattodo = result.outputs[0].text

        return whattodo

    #세부내용 리포트(마크다운)생성 에이전트