from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from blog_app import schemas as blg_schm
from blog_app import service
from users_app import schemas as usr_schm
from users_app.models import users
from main_package.fast_users import fastapi_users
from blog_app.models import post
from main_package import db


router = APIRouter()


@router.get("/all-posts", response_model=List[blg_schm.PostList])
async def post_list():
    q = post.join(users).select(use_labels=True)
    post_list = await db.database.fetch_all(query=q)
    return [dict(result) for result in post_list]


@router.post("/create-post", status_code=201, response_model=blg_schm.PostCreate)
async def post_create(item: blg_schm.PostCreate, user: usr_schm.User = Depends(fastapi_users.get_current_active_user)):
    crt_post = post.insert().values(**{'title': item.posts_blog_title,
                                       'text_blog': item.posts_blog_text_blog}, owner_id=user.id)
    pk = await db.database.execute(crt_post)
    return {**item.dict(), "id": pk, "owner_id": {"id": user.id}}


@router.get("/my-posts", response_model=List[blg_schm.PostList])
async def posts_user(user: usr_schm.User = Depends(fastapi_users.get_current_active_user)):
    user = post.join(users).select().where(post.c.owner_id == user.id)
    post_list = await db.database.fetch_all(query=user)
    return [dict(result) for result in post_list]


@router.get("/{pk}", response_model=blg_schm.PostSingle)
async def post_single(pk: int):
    q = post.join(users).select(use_labels=True).where(post.c.id == pk)
    post_pk = await db.database.fetch_one(q)
    if post_pk is not None:
        return dict(post_pk)
    if post_pk is None:
        raise HTTPException(status_code=404, detail="Post not found")


@router.get("/update/{pk}", status_code=201, response_model=blg_schm.PostSingle)
async def post_create(
        pk: int, item: blg_schm.PostCreate, user: usr_schm.User = Depends(fastapi_users.get_current_active_user)
    ):
    check = await service.check_owner(user, pk)
    if check:
        q_updt = post.update().where((post.c.id == pk) & (post.c.owner_id == user.id)).values(**{'title': item.posts_blog_title,
                                                                                                 'text_blog': item.posts_blog_text_blog})
        post_updt = await db.database.execute(q_updt)
        return dict(post_updt)


@router.get("/delete/{pk}", response_class=ORJSONResponse)
async def post_create(pk: int, user: usr_schm.User = Depends(fastapi_users.get_current_active_user)):
    check = await service.check_owner(user, pk)
    if check:
        q_del = post.delete().where((post.c.id == pk) & (post.c.owner_id == user.id))
        await db.database.execute(q_del)
        return {"status_code": 200, "details": f"post with id {pk} was deleted"}