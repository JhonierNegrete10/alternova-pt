from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from .token import verify_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="users/v2/login",
    # scheme_name="email",
    # scopes={
    #     "me": "Read information about the current user.",
    #     # "items": "Read items."
    # },
)


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    """
    get current user
    """
    if not token:
        return None
    else:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return verify_token(token, credentials_exception)
