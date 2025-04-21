from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def base():
    return {'message': 'hello world'}