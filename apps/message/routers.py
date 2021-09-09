from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from cryptography.fernet import Fernet
from pydantic import BaseModel
from .models import MessageModel

router = APIRouter()

"""
encrypt_message

Generates an encryption key, that can be used for encryption and decryption.
It convert the message to byte string, so that it can be encrypted.
Instance the Fernet class with the encryption key
Then encrypt the string with Fernet instance.
"""


async def encrypt_message(message):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = fernet.encrypt(message.encode())
    decMessage = fernet.decrypt(message).decode()
    return [message, key]


"""
decrypt_message

Generates an encryption key, that can be used for encryption and decryption.
It convert the message to byte string, so that it can be encrypted.
Instance the Fernet class with the encryption key
Then encrypt the string with Fernet instance.
"""


async def decrypt_message(key, encrypted_message):
    key = bytes(key, 'utf-8')
    encrypted_message = bytes(encrypted_message, 'utf-8')
    decrypted_message = Fernet(key).decrypt(encrypted_message).decode()
    return decrypted_message


"""
create_message route

receives the new message data as a JSON string in a POST request.
We have to decode this JSON request body into a Python dictionary and encrypt the message before passing it to our MongoDB client.

The insert_one method response includes the _id of the newly created message.
After we insert the encrypted message into our collection, we use the inserted_id to find the correct document and return this in our JSONResponse
"""


@router.post("/", response_description="Drop message")
async def create_message(request: Request, message: MessageModel = Body(...)):
    message_and_key = await encrypt_message(message.text)
    location = message.id
    message.text = message_and_key[0]
    message = jsonable_encoder(message)
    new_message = await request.app.mongodb["secrets"].insert_one(message)
    data = {"Location": location, "Password": message_and_key[1]}
    data = jsonable_encoder(data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=data)

"""
The message detail route has a path parameter of id, which FastAPI passes as an argument to the show_message function.
We use the id to attempt to find the corresponding message in the database.

If a document with the specified id does not exist, we raise an HTTPException with a status of 404.
"""


class Data(BaseModel):
    password: str


@router.post("/{id}")
async def show_message(data: Data, request: Request):
    id = request.url.path.split("/")[-1]
    if (message := await request.app.mongodb["secrets"].find_one({"_id": id})) is not None:
        decrypted_message = await decrypt_message(data.password, message['text'])
        await request.app.mongodb["secrets"].delete_one({"_id": id})
        return(decrypted_message)
    raise HTTPException(status_code=404, detail=f"Message {id} not found")
