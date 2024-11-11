# Coffit 서버
## How to run
- 할당받은 rebellions 자원 ssh로 접속
-  `$ cd malhaedgh/malhaedgh_backend`
-  
- ```bash 
    $ python3 -m vllm.entrypoints.openai.api_server \
        --model rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096 \
        --compiled-model-dir rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096 \
        --dtype auto \
        --device rbln \
        --max-num-seqs 4 \
        --max-num-batched-tokens 4096 \
        --max-model-len 4096 \
        --block-size 4096 \
        --api-key 1234 
    ``` 
    추론서버(vLLM) 실행
 
- `$ streamlit run ChatServer.py` streamlit 채팅 서버 실행
- `$ uvicorn main:app --host 0.0.0.0 --port 9000 --reload` fastapi 서비스 서버 실행

- POSTMAN으로 결과 확인 가능


## Wikis
- [파일 설명](https://github.com/marhaedgh/rbln-infer-server/wiki/%ED%8C%8C%EC%9D%BC-%EC%84%A4%EB%AA%85)
- ~~[Triton Inference Server 실행하는 법](https://github.com/marhaedgh/rbln-infer-server/wiki/Triton-Inference-Server-%EC%8B%A4%ED%96%89%ED%95%98%EB%8A%94-%EB%B2%95)~~
- [Basic vLLM backend Test](https://github.com/marhaedgh/rbln-infer-server/wiki/Basic-vLLM-backend-Test)
- [docker -> mysql](https://github.com/marhaedgh/rbln-infer-server/wiki/docker-%E2%80%90--mysql-%EC%8B%A4%ED%96%89)

<br/>
<br/>

## 설계 문서
### Current Server Architecture
<img width="670" alt="image" src="https://github.com/user-attachments/assets/89cb3ddb-0064-4255-b040-f326847a1d26">

### ERD
<image width=500 src="https://github.com/user-attachments/assets/ac46ee20-d122-4942-b3c8-5cc3d70717c5">

<br/>
<br/>
<br/>
### 

### 모델 성능 개발 전략
- 
