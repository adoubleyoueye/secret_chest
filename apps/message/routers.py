from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import MessageModel

router = APIRouter()


@router.post("/", response_description="Drop message")
async def create_message(request: Request, task: MessageModel = Body(...)):
    task = jsonable_encoder(task)
    new_message = await request.app.mongodb["secrets"].insert_one(task)
    created_message = await request.app.mongodb["secrets"].find_one(
        {"_id": new_message.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_message)

@router.get("/{id}", response_description="Pickup message")
async def show_message(id: str, request: Request):
    if (task := await request.app.mongodb["secrets"].find_one({"_id": id})) is not None:
        await request.app.mongodb["secrets"].delete_one({"_id": id})
        return task

    raise HTTPException(status_code=404, detail=f"Message {id} not found")