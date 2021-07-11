from fastapi import FastAPI

from .app.routers import comments, follow, group, post, users


PREFIX = '/api/v1'


app = FastAPI(
    title='Blog API',
    description=(
        'Created by using FastAPI, Pydantic, SQLAlchemy, Alembic,'
        ' python-jose and bcrypt'
    )
)


app.include_router(users.router, prefix=PREFIX)
app.include_router(post.router, prefix=PREFIX)
app.include_router(comments.router, prefix=PREFIX)
app.include_router(group.router, prefix=PREFIX)
app.include_router(follow.router, prefix=PREFIX)
