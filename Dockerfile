# Use uma imagem base oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos da aplicação
COPY app/ /app

# Instala dependências
RUN pip install --no-cache-dir -r /app/requirements.txt

# Define a porta exposta
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "/app/main.py"]
