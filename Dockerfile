FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install build-essential libssl-dev libffi-dev python3-dev default-libmysqlclient-dev gcc -y
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000