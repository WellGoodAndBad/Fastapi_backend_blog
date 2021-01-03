from fastapi_users.authentication import JWTAuthentication
import os


SECRET = os.environ.get('SECRET_KEY',  'SOME_RANDOM_SECRET_KEY')

jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)
