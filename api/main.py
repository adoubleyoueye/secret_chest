from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.message.routers import router as message_router

"""
We initialise the server in main.py; this is where we create our app.
"""
app = FastAPI()

"""
Open and close our connection to our MongoDB server.
When the app startup event is triggered, We open a connection to MongoDB and ensure that it is available via the app object so we can access it in our different routers.
"""
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

"""
Attach API endpoints
"""
app.include_router(message_router, tags=["message"], prefix="/message")

"""
Start the async event loop and ASGI server.
"""

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
