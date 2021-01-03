from fastapi_users import FastAPIUsers
from users_app import models, schemas
from main_package import security


fastapi_users = FastAPIUsers(
    models.user_db,
    [security.jwt_authentication],
    schemas.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserDB,
)