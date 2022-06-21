from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests
import subprocess
import asyncio

from providers.aws import aws
from providers.gmail import gmail


app = FastAPI()

class Token(BaseModel):
    token: str
    provider: str

@app.post("/email")
def simple_send(access: Token):

    bashCmd = ['ping', '-c', '1', 'api_container']
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    ip_api = str(output.split()[2].decode('UTF-8')[1:-1])

    url = f'http://{ip_api}:8000/api/token/verify/'
    url_data = f'http://{ip_api}:8000/api/check?token={access.token}'
    my_token = {'token': access.token}

    response = requests.post(url, json = my_token)

    match int(str(response.status_code)[0]):
        case 2:
            data = requests.get(url_data)
            text = f"Użytkownik {data.json()['username']}  wyraża chęć opóźnienia swojego transportu o  dni W celu ustalenia szczegółów odpisz na: {data.json()['email']}"
            recipent = 'miseczkag@gmail.com'
            match access.provider:
                case 'aws':
                    return aws(recipent=recipent, text=text)
                case 'gmail':
                    return asyncio.run(gmail(recipent=recipent, text=text))
                case _:
                    return JSONResponse(status_code=422, content={"message": "unprocessable or non-existing provider"})
        case _:
            return JSONResponse(status_code=response.status_code, content=response.json())