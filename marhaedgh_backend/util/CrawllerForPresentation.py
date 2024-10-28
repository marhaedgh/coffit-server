import os
import re
import requests
from bs4 import BeautifulSoup

def url_to_filename(url: str) -> str:
    # URL을 파일 이름으로 변환 (특수 문자는 _로 대체)
    filename = re.sub(r'[^a-zA-Z0-9]', '_', url) + ".md"
    return filename

def clean_text(text: str) -> str:
    # 3줄 이상의 연속된 개행을 2줄 개행으로 줄임
    text = re.sub(r'\n{3,}', '\n\n', text)  # 연속된 개행이 3줄 이상일 경우 2줄로 축소
    # 연속된 공백을 하나의 공백으로 줄임
    text = re.sub(r'[ \t]+', ' ', text)  # 연속된 공백을 하나의 공백으로
    return text.strip()  # 양 끝의 불필요한 공백 제거

def extract_text_from_url(url: str, output_dir: str) -> str:
    # 웹 페이지 HTML 가져오기
    response = requests.get(url)
    response.raise_for_status()  # 요청이 성공적으로 완료되었는지 확인
    html_content = response.text

    # HTML에서 텍스트만 추출
    soup = BeautifulSoup(html_content, "html.parser")
    text_content = soup.get_text(separator="\n")  # 줄바꿈으로 구분하여 텍스트 추출

    # 텍스트 정리
    clean_content = clean_text(text_content)

    # 지정한 폴더에 Markdown 파일로 저장
    os.makedirs(output_dir, exist_ok=True)  # 폴더가 없으면 생성
    filename = url_to_filename(url[7:35])
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(clean_content)
    
    print(f"{file_path}에 텍스트가 저장되었습니다.")
    return clean_content
