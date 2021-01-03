from blog_app.models import post
from users_app.models import users
from main_package import db
from fastapi import HTTPException


async def check_owner(cur_user, pk):
    qru = users.select().where(users.c.id == cur_user.id)
    user = await db.database.fetch_one(qru)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    qrp = post.select().where(post.c.id == pk)
    post_del = await db.database.fetch_one(qrp)
    if post_del is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post_del._row['owner_id'] != user._row['id']:
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        return True
