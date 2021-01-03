
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from users_app import schemas
from main_package import db


class UserTable(db.Base, SQLAlchemyBaseUserTable):
    account = relationship("Account", back_populates="owner")


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(schemas.UserDB, db.database, users)

# db.Base.metadata.create_all(db.engine)