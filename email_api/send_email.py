from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests
from starlette.responses import JSONResponse



from providers import factory

app = FastAPI()

class Token(BaseModel):
    token: str
    provider: str


@app.post("/email")
def simple_send(access: Token):

    url = f'http://api:8000/api/token/verify/'
    url_data = f'http://api:8000/api/check?token={access.token}'
    my_token = {'token': access.token}

    response = requests.post(url, json = my_token)

    match int(str(response.status_code)[0]):
        case 2:
            data = requests.get(url_data)
            text = f"Użytkownik {data.json()['username']}  wyraża chęć opóźnienia swojego transportu o  dni W celu ustalenia szczegółów odpisz na: {data.json()['email']}"
            recipent = 'miseczkag@gmail.com'
            sender = 'pmichnowicz13@gmail.com'
            return factory.Creator().create_provider(access.provider).send(sender, recipent, text)
        case _:
            return JSONResponse(status_code=response.status_code, content=response.json())