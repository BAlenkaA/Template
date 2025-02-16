from fastapi import APIRouter


main_router = APIRouter()

@main_router.get("/")
async def hello():
    return "Hello, World"