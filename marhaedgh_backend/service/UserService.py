from sqlalchemy.orm import Session
from dto.CreateBusinessRequest import CreateBusinessRequest
from dto.CreateBusinessResponse import CreateBusinessResponse

from db.database import get_db
from repository.UserRepository import UserRepository
from repository.BusinessDataRepository import BusinessDataRepository

class UserService:

    def create_business(self, req: CreateBusinessRequest):


        # TODO: 사용자 입력(CreateBusinessRequest)에 들어있는 정보 DB에 넣어 사용자 넣기.
        # 넣기전에 존재하는 사용자인지 검사 필요(시연엔 x)
        db: Session = next(get_db())
        
        business_data_repository = BusinessDataRepository(db)

        business_data = {
            "business_type": req.business_type,
            "corporation_type": req.corporation_type,
            "industry": req.industry,
            "region_city": req.region_city,
            "region_district": req.region_district,
            "representative_birthday": req.representative_birthday,
            "representative_gender": req.representative_gender,
            "revenue": req.revenue,
            "employees": req.employees
        }

        gen_business_data = business_data_repository.create(business_data)

        user_repository = UserRepository(db)

        user_data = {
            "business_data_id": gen_business_data.id
        }

        gen_user_data = user_repository.create(user_data)
        # 최초로 들어온 사용자는 정책이 생길 때까지 아무것도 없음 -> 넣은 시점에서 기간이 살아있는 알림들은 받아볼 수 있게 넣어주는 것도 방법일 듯
        
        create_business_response = CreateBusinessResponse(
            user_id = gen_user_data.id,
            business_data_id = gen_user_data.business_data_id,
        )
        return create_business_response
