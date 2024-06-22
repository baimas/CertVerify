# Use a imagem base do Python
FROM python:3.9-slim

# Atualize o sistema e instale as dependências necessárias
RUN apt-get update && apt-get install -y libssl-dev

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Verifique se o arquivo requirements.txt está sendo copiado corretamente
COPY requirements.txt /app/requirements.txt

# Instale as dependências especificadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copie todo o conteúdo do diretório local para o diretório de trabalho do container
COPY . /app

# Comando padrão para executar quando o container for iniciado
CMD ["flask", "run", "--host=0.0.0.0"]
