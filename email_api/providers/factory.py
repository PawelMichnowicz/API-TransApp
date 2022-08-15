import asyncio
import environ
import boto3
from abc import ABC, abstractmethod
from celery import Celery
from starlette.responses import JSONResponse
from botocore.exceptions import ClientError
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig


env = environ.Env()
environ.Env.read_env()

celery = Celery(__name__)
celery.conf.broker_url = "redis://redis:6379/0"

class Provider(ABC):

    @abstractmethod
    def send(self) -> JSONResponse:
        pass



def get_providers():
    dict_providers = {}
    for class_provider in Provider.__subclasses__():
        dict_providers[class_provider.__name__] = class_provider
    return dict_providers


def create_provider(name, sender, recipent):
    try:
        return get_providers()[name](sender, recipent)
    except:
        return UnknownProvider()



class MailGunProvider(Provider):
    ...


class AwsProvider(Provider):

    def __init__(self, sender, recipent):
        self.SENDER = sender
        self.RECIPIENT = recipent
        self.AWS_REGION = env('AWS_REGION')
        self.client = boto3.client('ses',region_name=self.AWS_REGION)


    def send(self, text) -> JSONResponse:

        SUBJECT = "mail"
        BODY_TEXT = 'mail'
        BODY_HTML = text
        CHARSET = "UTF-8"

        try:
            #Provide the contents of the email.
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        self.RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=self.SENDER,
            )

        except ClientError as e:
            return(e.response['Error']['Message'])
        else:
            return JSONResponse(status_code=200, content={"message": "email has been sent by aws to " + self.RECIPIENT})


class GmailProvider(Provider):

    def __init__(self, sender, recipent):
        self.sender = sender
        self.recipent = recipent
        self.conf = ConnectionConfig(
            MAIL_USERNAME = env('GMAIL_EMAIL'),
            MAIL_PASSWORD = env('GMAIL_PASSWORD'),
            MAIL_FROM = env('GMAIL_EMAIL'),
            MAIL_PORT = 587,
            MAIL_SERVER = env('GMAIL_SMTP'),
            MAIL_TLS = True,
            MAIL_SSL = False,
            USE_CREDENTIALS = True,
            )


    async def async_send(self, text) -> JSONResponse:

        message = MessageSchema(
                    subject="Fastapi-Mail mail",
                    recipients=[self.recipent,],
                    body=text
                    )
        fm = FastMail(self.conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": f"email has been sent by gmail to {self.recipent}"})

    def send(self, text):
        return asyncio.run(self.async_send(text))


class UnknownProvider(Provider):
    def send(self, *args) -> JSONResponse:
        return JSONResponse(status_code=422, content={"message": "unprocessable or non-existing provider"})






