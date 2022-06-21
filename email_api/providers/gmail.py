import environ
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from starlette.responses import JSONResponse

async def gmail(recipent, text):
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

    message = MessageSchema(
                subject="Fastapi-Mail module",
                recipients=[recipent,],  
                body=text
                )
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent by gmail"})