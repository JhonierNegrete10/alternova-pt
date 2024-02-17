import re
from typing import List

from db.configDatabase import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .crud import user_crud
from .models import UserLogin, UserModel, UserOutput, UserRegister
from .security.hashing import Hash
from .security.token import create_access_token

user_routes = APIRouter(prefix="/user", tags=["user"])


# Rutas de FastAPI
@user_routes.post("/")
def create_user(user: UserRegister, session: Session = Depends(get_db)):
    # Crear el usuario en la base de datos
    # Validar la contraseña con una expresión regular
    if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", user.password):
        raise HTTPException(
            status_code=400,
            detail="La contraseña debe tener al menos 8 caracteres, una letra y un número.",
        )

    # Verificar si el correo electrónico no existe en la base de datos
    existing_user = user_crud.get_user_by_email(user.email, session)

    if existing_user:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado."
        )
    # Hash the password
    hashed_password = Hash.hash_password(user.password)
    # print(hashed_password)
    # Finalmente, agregar la información del usuario a la base de datos
    user_model = UserModel(hashed_password=hashed_password, **user.dict())
    print(user_model)
    db_user = user_crud.add_user(user_model, session)

    # Create the token
    access_token = create_access_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@user_routes.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_db)):
    # Check if the user exists in the database
    user_db = user_crud.get_user_by_email(user_login.email.lower(), session)
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Check if the password matches
    if not Hash.verify_password(user_login.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="""password incorrect ! """
        )
    access_token = create_access_token(data={"sub": user_login.email})

    return {"access_token": access_token, "token_type": "bearer"}


@user_routes.get("/", response_model=List[UserOutput])
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    db_users = user_crud.get_users(skip, limit, session)
    return db_users
