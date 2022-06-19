from fastapi import FastAPI, Request, HTTPException 
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from jwt.exceptions import ExpiredSignatureError
from starlette.responses import JSONResponse
import environ


from jwt_handler import decode_access_token



env = environ.Env()
environ.Env.read_env()

ACCESS_SECRET = env('ACCESS_SECRET') 
REFRESH_SECRET = env('REFRESH_SECRET') 
ALG = env('ALG') 
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


@app.post("/email")
async def simple_send(request: Request, days: int):
    
    token = request.headers["Authorization"].split(" ")[1]
    try: 
        access_token = decode_access_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh your token")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = f"Użytkownik {access_token['username']} wyraża chęć opóźnienia swojego transportu o {days} dni W celu ustalenia szczegółów odpisz na: {access_token['email']}"


    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=['miseczkag@gmail.com',],  
        body=text
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})