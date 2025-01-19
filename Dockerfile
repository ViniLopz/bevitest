FROM python:3.10-slim

# Configuração do diretório de trabalho
WORKDIR /app

# Copiar dependências e arquivos necessários para o contêiner
COPY requirements.txt ./

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
