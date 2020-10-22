FROM python:3.9

RUN apt update

RUN pip3 install --upgrade pip && pip3 install poetry

RUN mkdir -p /home/python/app
WORKDIR /home/python/app

COPY pyproject.toml ./
#COPY poetry.lock ./
RUN poetry install

COPY . /home/python/app/
