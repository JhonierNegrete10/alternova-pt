from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .models import UserModel, UserRegister


class UserCRUD:
    def create(self, user: UserRegister, session: Session):
        db_user = UserModel(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def get_all(self, skip, limit, session: Session):
        statement = select(UserModel).offset(skip).limit(limit)
        result = session.execute(statement)
        result = result.scalars().all()
        return [obj_db for obj_db in result]

    def get_by_email(self, email: str, session: Session):
        statement = select(UserModel).where(UserModel.email == email)
        result = session.execute(statement)
        user = result.scalars().first()
        return user


user_crud = UserCRUD()
