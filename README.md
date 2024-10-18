# 서버!
compile_tutorial.py : 기본 rbln zoo llama3 8B 컴파일 코드
inference_tutorial.py : 기본 rbln zoo llama3 8B 컴파일모델 추론 코드
vllm_api_example.py : Continuous Batching vllm-rbln 예제코드 llama3 8B 수정 .ver
vllm_example_compile.py : vllm_api_example.py 코드 실행을 위한 batch size 4 모델 컴파일 코드

vllm_example_compile.py에서 batchsize 등 모델 관련 수정해서 vllm_backend에 넣어줘야함.

도커 설치후 다음 스텝 밟기
> 서버실행 명령어
sudo docker run --privileged --shm-size=1g --ulimit memlock=-1 \
   -v /home/guest/marhaedgh/vllm_backend:/opt/tritonserver/vllm_backend \
   -p 8000:8000 -p 8001:8001 -p 8002:8002 --ulimit stack=67108864 -ti nvcr.io/nvidia/tritonserver:24.01-vllm-python-py3

컨테이너 실행시 사용할 것
> $ pip3 install -i https://pypi.rbln.ai/simple/ "rebel-compiler>=0.5.2" "optimum-rbln>=0.1.4" vllm-rbln
> $ tritonserver --model-repository /opt/tritonserver/vllm_backend/samples/model_repository