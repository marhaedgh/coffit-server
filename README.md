# Coffit 서버
## How to run
- 할당받은 rebellions 자원 ssh로 접속  
- malhaedgh_backend 폴더로 이동
- `$ cd malhaedgh/malhaedgh_backend`
- 리벨리온 임베딩 모델 컴파일
- `python3 RBLNCompileEmbeddingModel.py` 
- 리벨리온 sLLM 모델 컴파일(컴파일시 batch size, length 변경 가능. ATOM 메모리 생각해서 수정할 것)
- `python3 RBLNCompileLLModel.py`
- ~~리벨리온 Reranking 모델 컴파일~~
- ~~`python3 RBLNCompileEmbeddingModel.py` ~~
  
- Vector store에 새로운 파일(정책데이터, 지원사업 데이터) 추가될 때마다 아래 명령어 수행
- ```bash 
    $ python3 create_vector_store.py \
    --vector_store_dir ./rag_data \
    --compiled_embedding_model bge-m3 \      
    --load_from_storage False \    
    --chunk_size 1024 \   
    --chunk_overlap_size 100
     ``` 

- docker -> mysql Wikis 참고하여 데이터베이스 컨테이너 띄우기
-  추론서버 실행
- ```bash 
    $ python3 -m vllm.entrypoints.openai.api_server \
        --model rbln_vllm_llama-3-Korean-Bllossom-8B_npu8_batch4_max8192 \
        --compiled-model-dir rbln_vllm_llama-3-Korean-Bllossom-8B_npu8_batch4_max8192 \
        --dtype auto \
        --device rbln \
        --max-num-seqs 4 \
        --max-num-batched-tokens 8192 \
        --max-model-len 8192 \
        --block-size 8192 \
        --api-key 1234 \
        --port 8000
    ``` 
- ATOM개수 4개 일 경우 : rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096
- ATOM개수 8개 일 경우 : rbln_vllm_llama-3-Korean-Bllossom-8B_npu8_batch4_max8192
- 
- `$ streamlit run ChatServer.py` streamlit 채팅 서버 실행 (접근 포트 8501)
- `$ uvicorn main:app --host 0.0.0.0 --port 9000 --reload` fastapi 서비스 서버 실행
- 리벨리온 자원에서 할당받은 인스턴스 공인IP에 포트 9000 = 22306, 8501 = 22305로 접근할 것
- 
-  Prometheus2 평가 추론 서버 실행
-  ```bash 
    $ python3 -m vllm.entrypoints.openai.api_server \
        --model rbln_vllm_prometheus-7b-v2.0_npu2_batch2_max4096 \
        --compiled-model-dir rbln_vllm_prometheus-7b-v2.0_npu2_batch2_max4096 \
        --dtype auto \
        --device rbln \
        --max-num-seqs 2 \
        --max-num-batched-tokens 4096 \
        --max-model-len 4096 \
        --block-size 4096 \
        --api-key 5678 \
        --port 8001
    ``` 

- `$ python3 EvalPrometheus.py` 프로메테우스 평가 실행
  
- 현재 서버 작업물은 API 요청으로 혹은 앱에서 결과 확인 가능


## Wikis
- [파일 설명](https://github.com/marhaedgh/rbln-infer-server/wiki/%ED%8C%8C%EC%9D%BC-%EC%84%A4%EB%AA%85)
- [docker -> mysql](https://github.com/marhaedgh/rbln-infer-server/wiki/docker-%E2%80%90--mysql-%EC%8B%A4%ED%96%89)
- ~~[Triton Inference Server 실행하는 법](https://github.com/marhaedgh/rbln-infer-server/wiki/Triton-Inference-Server-%EC%8B%A4%ED%96%89%ED%95%98%EB%8A%94-%EB%B2%95)~~
- ~~[Basic vLLM backend Test](https://github.com/marhaedgh/rbln-infer-server/wiki/Basic-vLLM-backend-Test)~~

<br/>
<br/>

## 설계 문서
### Current Server Architecture
<img width="670" alt="image" src="https://github.com/user-attachments/assets/4a4eb525-e87c-476c-b04e-ccaa1be58b63">


### ERD
<image width=500 src="https://github.com/user-attachments/assets/ac46ee20-d122-4942-b3c8-5cc3d70717c5">

<br/>
<br/>
<br/>

### 모델 성능 개발 전략
- 자체적으로 개발한 evaluate_code/rbln_summary.py 또는 Prometheus2 평가모델을 활용하여 현재 프롬프트의 성능을 평가 및 기록하고, 피드백을 통해 프롬프트를 개선합니다.
- 서비스시 사용자에게 output을 제공하기 전에 자체적으로 개발한 평가체계를 통해 평가점수에 미달할 경우 재 생성해서 신뢰도를 유지합니다.
