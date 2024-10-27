import asyncio
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter

from dto.DemonInferResponse import DemonInferResponse

class AgentService:

    def __init__(self, modelLoader):
        self.modelLoader = modelLoader
    
    #크롤링 에이전트
    # 크롤링 후 PDF -> 마크다운PDF 로 변경하여 RAG에 적재.
    # 이 과정에서 PDF 텍스트데이터로 추출
    #(시연용) 크롤링 되었다는 가정 하 실데이터 넣는 코드

    async def demonAlertResponse(self, url):
        #URL 타고 들어가서 본문내용(PDF) 추출 후 텍스트로 변환 //일단 html스크랩

        text_splitter = CharacterTextSplitter(        
            separator="\n\n",
            chunk_size=3000,     # 쪼개는 글자수
            chunk_overlap=300,   # 오버랩 글자수
            length_function=len,
            is_separator_regex=False,
        )
        # Chunk 단위로 분할 -> vllm에도 map_reduce가 있나...?
        docs = WebBaseLoader(url).load_and_split(text_splitter)

        content = docs[0] #텍스트

        title = await self.create_title(content)
        keyword = await self.create_keywords(content)
        short_summarization = await self.create_short_summarization(content)
        summarization = await self.create_summarization(content)
        classification = await self.create_classification(content)
        whattodo = await self.create_whattodo(content)

        demonInferResponse = DemonInferResponse(
            title = title, 
            keywords = keyword,
            one_line_summarization = short_summarization,
            summarization = summarization,
            classification = classification,
            what_to_do = whattodo
        )

        return demonInferResponse

        

    #제목생성
    async def create_title(self, content):

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a creative assistant helping entrepreneurs find value in policies by creating compelling titles. The title should be short, engaging, and accurately reflect the benefits of the policy. Use persuasive and inviting language to make entrepreneurs interested in reading the policy. Avoid jargon and focus on making it sound like a must-read for small business success.

        Title tips:
        1. Highlight any benefits or support provided by the policy.
        2. Use positive language to make the title more attractive.
        3. Keep it concise and impactful, ideally under 10 words.

        <|start_header_id|>user<|end_header_id|>
        content: {content}

        Create an appealing and informative title for this policy that will catch the attention of entrepreneurs and make them eager to learn more. Respond in Korean
        <|eot_id|>
        """

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '0'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        title = result.outputs[0].text

        return title

    
    #키워드 생성
    async def create_keywords(self, content):

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an assistant skilled at identifying key topics in policies for entrepreneurs. Your task is to extract 3-5 impactful keywords that encapsulate the core topics of the policy. These keywords should help entrepreneurs understand the main ideas at a glance and locate relevant information quickly.

        Keyword selection tips:
        1. Focus on terms that represent the policy’s purpose and scope.
        2. Include any terms related to eligibility, support type, or conditions.
        3. Avoid overly broad terms and ensure each keyword is unique and specific.

        <|start_header_id|>user<|end_header_id|>
        content: {content}
        List 3-5 critical keywords by JSON type from this policy that capture the main topics and concepts relevant to entrepreneurs. Respond in Korean, Only respond JSON type answer
        <|eot_id|>
        """

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '1'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        keyword = result.outputs[0].text

        return keyword

    
    #한줄 요약 생성
    async def create_short_summarization(self, content):

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a knowledgeable assistant dedicated to helping entrepreneurs quickly understand policy essentials. Summarize the policy content in a way that is clear, concise, and directly relevant to small business needs. Highlight any benefits, eligibility criteria, or key deadlines that the entrepreneur should know. Aim for an approachable, informative tone.

        Guidelines for a useful summary:
        1. Begin with a brief overview of what the policy covers.
        2. Identify who is eligible and how they benefit.
        3. Mention any important dates, deadlines, or requirements.
        4. Use plain language, avoiding unnecessary technical terms.

        <|start_header_id|>user<|end_header_id|>
        content: {content}

        Provide a clear and concise summary of the policy, covering its purpose, benefits, and any key details entrepreneurs need to know. Respond in Korean, make it in 20 charactors.
        <|eot_id|>
        """

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '2'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        short_summarization = result.outputs[0].text

        return short_summarization


    #분류 생성
    async def create_classification(self, content):

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an assistant focused on classifying policies to help individual entrepreneurs find relevant information quickly. Your task is to categorize each policy based on its target audience and the type of support it offers. The categories should be specific enough to match policies with entrepreneurs' business types, size, industry, and operational needs.

        Guidelines for classification:
        1. Determine which types of business (e.g., retail, services, manufacturing) the policy is most relevant to.
        2. Identify if the policy applies to specific business sizes or stages (e.g., startups, small businesses, growth phase). 
        3. Consider any industry-specific requirements or restrictions.
        4. Ensure categories are detailed but concise, such as "Retail - Startup Support" or "Manufacturing - Tax Relief for Equipment." 
        5. ~~~ #여기 디테일한 사업자 정보들 넣으면 될 듯 합니다. 

        <|start_header_id|>user<|end_header_id|>
        content: {content}
        Based on the above criteria, provide a classification for this policy that highlights the target business type, industry, and any specific conditions or eligibility factors. Respond in Korean
        <|eot_id|>
        """
        # 뱉는 형태 정의 필요

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '3'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        classification = result.outputs[0].text

        return classification


    #요약 생성
    async def create_summarization(self, content):
        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a knowledgeable assistant dedicated to helping entrepreneurs quickly understand policy essentials. Summarize the policy content in a way that is clear, concise, and directly relevant to small business needs. Highlight any benefits, eligibility criteria, or key deadlines that the entrepreneur should know. Aim for an approachable, informative tone.

        Guidelines for a useful summary:
        1. Begin with a brief overview of what the policy covers.
        2. Identify who is eligible and how they benefit.
        3. Mention any important dates, deadlines, or requirements.
        4. Use plain language, avoiding unnecessary technical terms.

        <|start_header_id|>user<|end_header_id|>
        content: {content}

        Provide a clear and concise summary of the policy, covering its purpose, benefits, and any key details entrepreneurs need to know. Respond in Korean
        <|eot_id|>
        """
        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '4'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params)

        summarization = result.outputs[0].text

        return summarization


    #할일 생성
    async def create_whattodo(self, content):

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a strategic advisor for entrepreneurs, guiding them in effectively applying policies. Your goal is to provide clear, actionable steps that help entrepreneurs understand what they need to do to benefit from the policy. Ensure each step is practical, realistic, and specific to small business operations.

        Guidelines for actionable steps:
        1. Begin with any immediate actions required (e.g., registrations, applications).
        2. Break down each step in simple language, focusing on what to do, how to do it, and why it’s beneficial.
        3. Include any important deadlines or documentation required.

        <|start_header_id|>user<|end_header_id>
        content: {content}
        Provide step-by-step actions entrepreneurs should take to benefit from this policy. Include any deadlines or requirements they should be aware of. Respond in Korean
        <|eot_id|>
        """

        sampling_params = SamplingParams(
            temperature=0.0,
            skip_special_tokens=True,
            stop_token_ids=self.modelLoader.stop_tokens(),
        )

        request_id = '1'

        result = await self.modelLoader.run_single(prompt, request_id, sampling_params) #userid로 requestid 식별해도 괜찮겠다

        whattodo = result.outputs[0].text

        return whattodo

    #세부내용 리포트(마크다운)생성 에이전트