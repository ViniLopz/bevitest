import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base, get_db
from httpx._transports.asgi import ASGITransport  # Import correto para ASGITransport
from app.main import app
from mongomock import MongoClient

# Configuração do banco de dados SQLite para testes
TEST_SQLITE_URL = "sqlite:///./test_products.db"
engine = create_engine(TEST_SQLITE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Substituindo o banco de dados MongoDB por um mock
mock_mongo_client = MongoClient()
mock_logs_collection = mock_mongo_client["product_logs"]["product_views"]

# Fixture para o banco de dados SQLite
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Substituir a dependência do banco de dados no FastAPI
@pytest.fixture(scope="function")
def override_db_dependency(db_session):
    app.dependency_overrides[get_db] = lambda: db_session

# Substituir logs MongoDB no controlador
@pytest.fixture(scope="function")
def override_logs_dependency():
    app.dependency_overrides["logs_collection"] = lambda: mock_logs_collection

# Cliente de teste do FastAPI
@pytest_asyncio.fixture(scope="function")
async def client():
    # Configurando o transporte ASGI com o app FastAPI
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac