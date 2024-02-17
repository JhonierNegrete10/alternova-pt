#Dockerfile
FROM python:3.9

RUN apt-get update -y \
    && apt-get install -y iputils-ping \
    && apt-get install -y net-tools

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


CMD [ "python", "main.py"]