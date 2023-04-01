from apps.message.routers import encrypt_message
from fastapi.testclient import TestClient
from cryptography.fernet import Fernet
from ..main import app

client = TestClient(app)
text = "Pants smell like shirts"


def test_encryption(message=text):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    assert encrypted_message != text
    assert decrypted_message == text

# def test_startup_db_client():
#     app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
#     app.mongodb = app.mongodb_client[settings.DB_NAME]


# def test_shutdown_db_client():
#     app.mongodb_client.close()