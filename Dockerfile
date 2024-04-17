# python 3.10 base image
FROM python:3.10.0

# Information
LABEL author="Oidaho" email="oidahomain@gmail.com"

ARG TOKEN
ARG GROUPID

ENV TOKEN $TOKEN
ENV GROUPID $GROUPID

ARG SQL_HOST
ARG SQL_PORT
ARG SQL_USER
ARG SQL_PSWD

ENV SQL_HOST $SQL_HOST
ENV SQL_PORT $SQL_PORT
ENV SQL_USER $SQL_USER
ENV SQL_PSWD $SQL_PSWD

WORKDIR /service

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "start.py"]