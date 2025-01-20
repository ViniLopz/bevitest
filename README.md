# API CRUD de Produtos com FastAPI

## Descrição do Projeto
Esta é uma API desenvolvida com FastAPI para gerenciar produtos, permitindo operações de criação, leitura, atualização e exclusão (CRUD). Logs de visualizações de produtos são armazenados no MongoDB um banco de dados nao relacional, e a aplicação utiliza SQLite como banco de dados relacional.

## Funcionalidades
- Criar produtos com validações específicas.
- Listar produtos com suas informações básicas.
- Atualizar produtos existentes.
- Excluir produtos.
- Registrar logs de visualizações no MongoDB.
- Consultar histórico de visualizações por produto.

## Tecnologias Utilizadas
- **Python**: Linguagem principal.
- **FastAPI**: Framework para APIs.
- **SQLAlchemy** e **Alembic**: ORM e migração de banco de dados.
- **MongoDB**: Banco NoSQL para logs.
- **Docker** e **docker-compose**: Para ambiente containerizado.
- **pytest**: Para testes unitários.
- **Postman**: Para testes manuais e documentação.
- **VSCode**: Editor de código-fonte usado no desenvolvimento.
- **MongoDBCompass: Para visualizar os logs gerados.

## Instalação

**Pré-requisitos**
- Docker instalado.
- Python 3.9+ 

## Passos para Configurar
## 1. Clone este repositório:
   
   git clone https://github.com/SEU_USUARIO/bevitest.git
   
## 1.1 Navegue ate o diretorio do projeto 
   cd bevitest

## 2. Configure o ambiente com Docker:
Suba os serviços:
make up

Realize as migrações no banco:
make upgrade

Execute os testes: 
make test

## 3.1 Configure localmente (opção local)
Certifique o diretorio e instale as dependências:
pip install -r requirements.txt

Inicie o servidor:
uvicorn app.main:app --reload


##  4.Como Utilizar:
Utilize um cliente HTTP como Postman para interagir com as rotas (CRUD).
