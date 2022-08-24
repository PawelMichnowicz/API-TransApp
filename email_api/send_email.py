import requests
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from providers.factory import get_providers
from celery_worker import provider_send

app = FastAPI()

enum_providers = {key: val.__name__ for key, val in get_providers().items()}
ProviderEnum = Enum('PoviderEnum', enum_providers)

class Data(BaseModel):
    token: str
    email: str
    email_text: str

@app.post("/email-complain")
def simple_send(data: Data, provider: ProviderEnum):

    url = 'http://api:8000/api/users/token/verify/'
    my_token = {'token': data.token}
    response = requests.post(url, json = my_token)

    match response.status_code:
        case 200:
            text = data.email_text
            recipent = data.email
            sender = 'miseczkag@gmail.com'
            return provider_send(provider.name, sender, recipent, text)
        case _:
            return JSONResponse(status_code=response.status_code, content=response.json())
