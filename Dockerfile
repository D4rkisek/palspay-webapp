FROM python:3.9-alpine3.13
LABEL maintainer="webapps2024"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirement.txt
COPY .app .app