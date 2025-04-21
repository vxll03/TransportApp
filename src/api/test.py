from fastapi import APIRouter


test = APIRouter()


@test.get("/test")
def base():
    return {"message": "hello world"}
