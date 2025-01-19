from sqlalchemy import Column, Integer, String, Float, Enum
from enum import Enum as PyEnum
from app.database.connection import Base

# Define os status possíveis para o produto usando um enumerado do Python
class ProductStatus(PyEnum):
    em_estoque = "em estoque"
    em_reposicao = "em reposição"
    em_falta = "em falta"

# Define o modelo de Produto
class Product(Base):
    __tablename__ = "products"

    # Define as colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    status = Column(Enum(ProductStatus), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
