FROM alpine:3.8

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev freetds-dev linux-headers python3-dev
COPY requirements .

RUN pip3 install -r production.txt

COPY ./main /code

WORKDIR /code

RUN ls -la

CMD [ "uwsgi", "--ini", "main/app.ini" ]