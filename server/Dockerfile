FROM python:3.8

RUN apt update
RUN apt install -y libpython3-dev \
    zlib1g-dev \
    musl-dev \
    libgdk-pixbuf2.0-dev \
    libgdk-pixbuf2.0 \
    libjpeg-dev \
    libwebp-dev \
    gettext \
    libpq-dev \
    libffi-dev \
    libgdal-dev

RUN pip3 install --upgrade pip && pip3 install poetry

RUN mkdir -p /home/python/app
WORKDIR /home/python/app

COPY pyproject.toml ./
#COPY poetry.lock ./
RUN poetry install

COPY . /home/python/app/
