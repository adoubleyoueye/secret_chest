from apps.message.routers import encrypt_message
from fastapi.testclient import TestClient
from cryptography.fernet import Fernet
from ..main import app

client = TestClient(app)


def test_encrypt_message(message="Pants smell like shirts"):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    message = fernet.encrypt(message.encode())
    assert message != "Pants smell like shirts"

# def test_startup_db_client():
#     app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
#     app.mongodb = app.mongodb_client[settings.DB_NAME]


# def test_shutdown_db_client():
#     app.mongodb_client.close()