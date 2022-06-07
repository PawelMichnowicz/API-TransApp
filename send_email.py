from fastapi import ( FastAPI, BackgroundTasks, UploadFile, File, Form, Query, Body, Depends )
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig



conf = ConnectionConfig(
    MAIL_USERNAME = "pmichnowicz13@email.com",
    MAIL_PASSWORD = "Kupadupa1313",
    MAIL_FROM = "pmichnowicz13@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smpt.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
)


app = FastAPI()

@app.get('/')
def home():
    return({"data":'elo'})
