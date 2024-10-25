from typing import Literal, List

from pydantic import BaseModel

from model.Representative import Representative


class BusinessData(BaseModel):
    business_type: Literal['개인사업자', '법인사업자']
    corporation_type: List[Literal['창업', '재창업', '기존 사업자']] = None
    industry: Literal[
        '자동차 및 부품 판매업', '도매 및 상품 중개업', '소매업(자동차 제외)',
        '숙박업', '음식점업', '제조업', '교육 서비스업', '협회 및 단체, 수리 및 기타 개인 서비스업',
        '부동산업', '전문, 과학 및 기술 서비스업', '예술, 스포츠 및 여가관련 서비스업',
        '정보통신업', '농업, 임업 및 어업', '건설업', '운수 및 창고업',
        '보건업 및 사회복지 서비스업', '사업시설 관리, 사업 지원 및 임대 서비스업',
        '금융 및 보험업', '전기, 가스, 증기 및 공기 조절 공급업', '광업',
        '수도, 하수 및 폐기물 처리, 원료 재생업',
        '가구 내 고용활동 및 달리 분류되지 않은 자가 소비 생산활동',
        '공공 행정, 국방 및 사회보장 행정', '국제 및 외국기관'
    ]
    region: str
    representative: Representative
    revenue: float
    employees: int
