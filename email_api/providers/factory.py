from abc import ABC, abstractmethod
from starlette.responses import JSONResponse
import boto3
from botocore.exceptions import ClientError
import environ
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import asyncio


class Provider(ABC):

    @abstractmethod
    def send(self) -> JSONResponse:
        pass

class Creator(ABC):

    def create_provider(self, name):
        match name:
            case 'aws':
                return AwsProvider()
            case 'gmail':
                return GmailProvider()
            case _:
                return UnknownProvider()


class AwsProvider(Provider):

    def send(self, sender, recipent, text) -> JSONResponse:

        SENDER = sender
        RECIPIENT = recipent
        AWS_REGION = "us-east-1"
        SUBJECT = "mail"
        BODY_TEXT = 'mail'     
        BODY_HTML = text        
        CHARSET = "UTF-8"

        client = boto3.client('ses',region_name=AWS_REGION)

        try:
            #Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
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
                Source=SENDER,
            )

        except ClientError as e:
            return(e.response['Error']['Message'])
        else:
            return JSONResponse(status_code=200, content={"message": "email has been sent by aws" + response['MessageId']})


class GmailProvider(Provider):
    
    async def async_send(self, sender, recipent, text) -> JSONResponse:
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

    def send(self, sender, recipent, text):
        return asyncio.run(self.async_send(sender, recipent, text))


class UnknownProvider(Provider):
    def send(self) -> JSONResponse:
        return JSONResponse(status_code=422, content={"message": "unprocessable or non-existing provider"})


