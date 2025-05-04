# Use uma imagem base do Python para garantir que você tenha as dependências do Python disponíveis
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requirements para o contêiner primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/requirements.txt

# Instale as dependências da sua aplicação usando o pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copie o código da sua aplicação para o contêiner
COPY . /app

# Exponha a porta que sua aplicação Flask irá ouvir (normalmente 5000)
EXPOSE 5000

# Defina a variável de ambiente FLASK_APP para o nome do seu arquivo principal da aplicação
ENV FLASK_APP=app.py

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:5001", "app:app"]
