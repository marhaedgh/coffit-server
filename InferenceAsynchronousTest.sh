#!/bin/bash

# 요청을 보낼 URL
URL="http://localhost:8000/v1/chat/completions"

# Bearer 토큰 설정
TOKEN="1234"

# JSON 데이터를 생성하는 함수
generate_json_payload() {
  cat <<EOF
{
  "model": "rbln_vllm_llama-3-Korean-Bllossom-8B_npu4_batch4_max4096",
  "messages": [
    {"role": "system", "content": "."},
    {"role": "user", "content": "주휴수당에 대해서 자세하게 설명해주고, 연말에 내가 뭐해야하는지 설명해줘. 추가적으로 서울의 수도에 대해서도 설명해줘."}
  ],
  "max_tokens": 4000,
  "temperature": 0.0,
  "stream": false
}
EOF
}

# 동시에 보낼 요청 개수 설정
REQUEST_COUNT=11

# 반복문을 통해 여러 개의 비동기 요청 전송
for i in $(seq 1 $REQUEST_COUNT)
do
  echo "Sending request #$i"
  curl --location "$URL" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $TOKEN" \
  --data "$(generate_json_payload)" \
  --silent --output "response_$i.json" &

  # 10ms (0.01초) 대기
  sleep 3
done

# 모든 백그라운드 작업이 완료될 때까지 대기
wait

echo "All requests completed!"
