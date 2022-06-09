
FROM python:3.9

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "send_email:app", "--reload", "--port", "8001", "--host", "0.0.0.0"]

