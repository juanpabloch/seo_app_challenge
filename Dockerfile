FROM python:3.8.1-slim-buster

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    libmagickwand-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn==20.0.4"

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN mkdir /app/staticfiles

RUN mkdir /app/sites

COPY . .

CMD set -xe; python manage.py migrate --noinput; gunicorn mysite.wsgi:application;
