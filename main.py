import uvicorn
from fastapi import FastAPI
from main_package.fast_users import fastapi_users
from main_package import security, db
from blog_app import view
from users_app import view as usr_view
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    fastapi_users.get_auth_router(security.jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(None), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        security.SECRET, after_forgot_password=None
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
app.include_router(view.router, prefix="/blog")
app.include_router(usr_view.router, tags=["auth"]
)


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)