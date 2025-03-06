# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /backend

# Copia os arquivos da aplicação
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia toda a aplicação mantendo a estrutura correta
COPY . .

# Expõe a porta 5000
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "backend/main.py"]
