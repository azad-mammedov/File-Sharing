# FROM python:3.7-alpine
 
# ENV PYTHONUNBUFFERED 1
# COPY ./requirements.txt /requirements.txt

# RUN apk add --update --no-cache postgresql-client jpeg-dev
# RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# RUN pip install -r /requirements.txt
# RUN apk del .tmp-build-deps

# RUN mkdir /File-Sharing
# COPY . /File-Sharing
# WORKDIR /File-Sharing
FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
# COPY wait_for_db.sh wait_for_db.sh
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]