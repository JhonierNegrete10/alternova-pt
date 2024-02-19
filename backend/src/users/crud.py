from sqlmodel import Session, select

from .models import UserModel, UserRegister


class UserCRUD:
    def create(self, user: UserRegister, session: Session):
        db_user = UserModel(**user.model_dump())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def get_all(self, skip, limit, session: Session):
        statement = select(UserModel).offset(skip).limit(limit)
        result = session.exec(statement)
        result = result.all()
        return [obj_db for obj_db in result]

    def get_by_email(self, email: str, session: Session):
        statement = select(UserModel).where(UserModel.email == email)
        result = session.exec(statement)
        user = result.first()
        return user


user_crud = UserCRUD()
