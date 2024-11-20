import os
import requests
import json
from datetime import datetime


api_url = "https://www.bizinfo.go.kr/uss/rss/bizinfoApi.do"
service_key = "YOUR_SERVICE_KEY"
data_type = "json"
search_cnt = 100 

params = {
    "crtfcKey": service_key,
    "dataType": data_type,
    "searchCnt": search_cnt
}

response = requests.get(api_url, params=params)

if response.status_code == 200:

    data = response.json()
    
    save_dir = "/home/guest/marhaedgh/marhaedgh_backend/rag_data/data"
    os.makedirs(save_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"bizinfo_data_{timestamp}.json"
    file_path = os.path.join(save_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"데이터가 성공적으로 저장되었습니다: {file_path}")
else:
    print(f"API 요청 실패: 상태 코드 {response.status_code}")
