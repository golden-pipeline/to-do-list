# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos da aplicação
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

# Define a porta exposta
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "__init__.py"]
