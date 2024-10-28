# 서버!
compile_tutorial.py : 기본 rbln zoo llama3 8B 컴파일 코드
inference_tutorial.py : 기본 rbln zoo llama3 8B 컴파일모델 추론 코드
vllm_api_example.py : Continuous Batching vllm-rbln 예제코드 llama3 8B 수정 .ver
vllm_example_compile.py : vllm_api_example.py 코드 실행을 위한 batch size 4 모델 컴파일 코드

vllm_example_compile.py에서 batchsize 등 모델 관련 수정해서 vllm_backend에 넣어줘야함.

## Triton Inference Server 실행하는 법
도커 설치후 다음 스텝 밟기
> 서버실행 명령어
sudo docker run --privileged --shm-size=1g --ulimit memlock=-1 \
   -v /home/guest/marhaedgh/vllm_backend:/opt/tritonserver/vllm_backend \
   -p 8000:8000 -p 8001:8001 -p 8002:8002 --ulimit stack=67108864 -ti nvcr.io/nvidia/tritonserver:24.01-vllm-python-py3

컨테이너 실행시 사용할 것
> $ pip3 install -i https://pypi.rbln.ai/simple/ "rebel-compiler>=0.5.2" "optimum-rbln>=0.1.4" vllm-rbln
> $ tritonserver --model-repository /opt/tritonserver/vllm_backend/samples/model_repository

주의
컨테이너에서 작업시 pip update 꼭 해줄것.
huggingface login 해주기
컨테이너에서 model.json 참고시 해당 컨테이너 기준 절대경로로 붙여넣을 것. 

> 간소화(도커 이미지로 만들어서 다음 명령어만 치면 됨)
sudo docker run --privileged --shm-size=1g --ulimit memlock=-1 \
   -v /home/guest/marhaedgh/vllm_backend:/opt/tritonserver/vllm_backend \
   -p 8000:8000 -p 8001:8001 -p 8002:8002 --ulimit stack=67108864 -ti test-image1:v1.0.0

> $ tritonserver --model-repository /opt/tritonserver/vllm_backend/samples/model_repository

## Basic vLLM backend Test

1. vllm_example_compile 파일 참고해서 RBLN SDK로 컴파일하기
2. vllm_api_example.py 파일 참고해서 실행시키기.
> compile_tutorial.py 는 기본 llama3 8B 모델
> 그외에 bllossom, luxia 모델 추가


## docker -> mysql
>
도커 이미지 빌드
sudo docker image build -t malhaedgh_db_image .

도커 실행
sudo docker container run --name malhaedgh_db -d -p 3305:3306 --rm -v /home/guest/marhaedgh/docker/mysql_db:/var/lib/mysql malhaedgh_db_image

도커 컨테이너 접속
> docker exec -it malhaedgh_db_image bash

도커 컨테이너 강종
> sudo docker stop malhaedgh_db

도커 컨테이너 삭제
> sudo docker rm malhaedgh_db
