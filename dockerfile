FROM python:3.10.2-slim


RUN apt update && apt install -y build-essential default-libmysqlclient-dev 
RUN python -m pip install --upgrade pip
WORKDIR /code
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000


# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
