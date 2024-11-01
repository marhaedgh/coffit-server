from sqlalchemy.orm import Session
from db.models.User import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def update(self, user_id: int, update_data: dict) -> User:
        user = self.get_by_id(user_id)
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
