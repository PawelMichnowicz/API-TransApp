
FROM python:3.10.2-slim

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN cp -r providers/credentials/.aws ~/


EXPOSE 8001


