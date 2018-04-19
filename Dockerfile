
FROM python:3.6.4-alpine3.7
LABEL Name=LSAPI Version=0.0.1
WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]
COPY ["app.py", "./"]
RUN apk update \
  && apk add --update alpine-sdk
RUN ["pip", "install", "pipenv"]
RUN ["pipenv", "install", "--system"]

ENV DEBUG="false" UDP_IP="172.17.10.20" UDP_PORT=10001 SHELL=/bin/sh
EXPOSE 5000
CMD pipenv run gunicorn app:app --workers=4 --bind=0.0.0.0:5000 --pid=pid --worker-class=meinheld.gmeinheld.MeinheldWorker
