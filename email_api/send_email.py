import requests
from enum import Enum,  auto
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from providers.factory import get_providers
from celery_worker import provider_send

app = FastAPI()

enum_providers = {key: val.__name__ for key, val in get_providers().items()}
ProviderEnum = Enum('PoviderEnum', enum_providers)

class Token(BaseModel):
    token: str


@app.post("/email")
def simple_send(access: Token, provider: ProviderEnum):

    url = f'http://api:8000/api/token/verify/'
    url_data = f'http://api:8000/api/check?token={access.token}'
    my_token = {'token': access.token}

    response = requests.post(url, json = my_token)

    match response.status_code:
        case 200:
            data = requests.get(url_data)
            text = f"Użytkownik {data.json()['username']}  wyraża chęć opóźnienia swojego transportu o  dni W celu ustalenia szczegółów odpisz na: {data.json()['email']}"
            recipent = 'miseczkag@gmail.com'
            sender = 'pmichnowicz13@gmail.com'
            return provider_send(provider.name, sender, recipent, text)
        case _:
            return JSONResponse(status_code=response.status_code, content=response.json())
