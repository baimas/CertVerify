# Dockerfile

# Use uma imagem base do Python com suporte ao Flask
FROM python:3.9-slim

RUN apt-get update && apt-get install -y libssl-dev


# Sete o diretório de trabalho para /app
WORKDIR /app

# Copie os arquivos necessários (app.py e outros)
COPY app.py .
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Defina a porta que o container deve expor
EXPOSE 5000

# Defina a variável de ambiente para o Flask (opcional, se necessário)
ENV FLASK_APP=app.py

# Comando para executar a aplicação quando o container for iniciado
CMD ["flask", "run", "--host=0.0.0.0"]
