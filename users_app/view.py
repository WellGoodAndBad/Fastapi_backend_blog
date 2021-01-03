from main_package.security import jwt_authentication
from fastapi import Depends, Response, APIRouter
from main_package.fast_users import fastapi_users
from users_app import schemas as usr_schm


router = APIRouter()


@router.post("/auth/jwt/refresh")
async def refresh_jwt(response: Response, user: usr_schm.User = Depends(fastapi_users.get_current_active_user)):
    return await jwt_authentication.get_login_response(user, response)