from fastapi import FastAPI


from app.kittens.breeds.router import router as breeds_router
from app.kittens.router import router as kittens_router


app = FastAPI(
    title="Oнлайн выставки котят",
    description="API для администратора онлайн выставки котят",
)


app.include_router(breeds_router)
app.include_router(kittens_router)
