from fastapi import FastAPI, Request, HTTPException 
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

from pydantic import BaseModel
from starlette.responses import JSONResponse
import environ
import requests


env = environ.Env()
environ.Env.read_env()


EMAIL = env('EMAIL') 
PASSWORD = env('PASSWORD')

conf = ConnectionConfig(
    MAIL_USERNAME = EMAIL,
    MAIL_PASSWORD = PASSWORD,
    MAIL_FROM = EMAIL,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
)

app = FastAPI()

class Token(BaseModel):
    token: str

@app.post("/email")
async def simple_send(access: Token):
    
    url = 'http://172.26.0.4:8000/api/token/verify/'
    url_data = f'http://172.26.0.4:8000/api/check?token={access.token}'
    my_token = {'token': access.token}

    response = requests.post(url, json = my_token)
    data = requests.get(url_data)


    match int(str(response.status_code)[0]) :

        case 2:
            text = f"Użytkownik {data.json()['username']}  wyraża chęć opóźnienia swojego transportu o  dni W celu ustalenia szczegółów odpisz na: {data.json()['email']}"

            message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=['miseczkag@gmail.com',],  
                body=text
                )
            fm = FastMail(conf)
            await fm.send_message(message)
            return JSONResponse(status_code=response.status_code, content={"message": "email has been sent"})

        case _:
            return JSONResponse(status_code=response.status_code, content=response.json())