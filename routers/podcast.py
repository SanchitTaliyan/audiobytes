from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/")
def read_root():
    pass