import re
from typing import List

from db.configDatabase import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .crud import user_crud
from .models import Token, TokenData, UserLogin, UserModel, UserOutput, UserRegister
from .security.hashing import Hash
from .security.outh import get_current_user
from .security.token import create_access_token

user_routes = APIRouter(prefix="/users", tags=["users"])


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
    existing_user = user_crud.get_by_email(user.email, session)

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
    db_user = user_crud.create(user_model, session)

    # Create the token
    access_token = create_access_token(data={"sub": db_user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@user_routes.post("/login")
def login(user_login: UserLogin, session: Session = Depends(get_db)):
    # Check if the user exists in the database
    user_db: UserModel = user_crud.get_by_email(user_login.email.lower(), session)
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
    db_users = user_crud.get_all(skip, limit, session)
    return db_users


@user_routes.get("/me", response_model=UserOutput)
def user_info(
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # print(current_user.email)
    data = user_crud.get_by_email(current_user.email, session)
    # print(data)
    return data


@user_routes.post("/v2/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)
):
    user_db: UserModel = user_crud.get_by_email(form_data.username.lower(), session)
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Check if the password matches
    if not Hash.verify_password(form_data.password, user_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="""password incorrect ! """
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")
