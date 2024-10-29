from sqlalchemy.orm import Session
from db.models.BusinessData import BusinessData

class BusinessDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, business_data: dict) -> BusinessData:
        business_data = BusinessData(**business_data)
        self.db.add(business_data)
        self.db.commit()
        self.db.refresh(business_data)
        return business_data

    def get_by_id(self, business_data_id: int) -> BusinessData:
        return self.db.query(BusinessData).filter(BusinessData.id == business_data_id).first()

    def update(self, business_data_id: int, update_data: dict) -> BusinessData:
        business_data = self.get_by_id(business_data_id)
        if business_data:
            for key, value in update_data.items():
                setattr(business_data, key, value)
            self.db.commit()
            self.db.refresh(business_data)
        return business_data

    def delete(self, business_data_id: int) -> None:
        business_data = self.get_by_id(business_data_id)
        if business_data:
            self.db.delete(business_data)
            self.db.commit()
