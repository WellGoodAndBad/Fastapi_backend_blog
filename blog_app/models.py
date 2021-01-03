from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, sql
from sqlalchemy.orm import relationship
from fastapi_users.db.sqlalchemy import GUID
from main_package import db


class PostBlog(db.Base):
    __tablename__ = "posts_blog"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    text_blog = Column(String)
    date = Column(DateTime(timezone=True), server_default=sql.func.now())

    owner_id = Column(GUID, ForeignKey("user.id"))
    owner = relationship("UserTable", back_populates="post")


post = PostBlog.__table__

# db.Base.metadata.create_all(db.engine)