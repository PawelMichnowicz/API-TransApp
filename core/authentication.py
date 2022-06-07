import jwt, datetime, json
from rest_framework import exceptions
from base64 import b64decode, b64encode

def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
        'iat': datetime.datetime.utcnow()
        },
        'access_secret', 
        algorithm='HS256')

def decode_access_token(access_token):
    return jwt.decode(
    access_token,
    'access_secret',
    algorithms=['HS256'])

def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
        },
        'refresh_secret',
        algorithm='HS256')

def decode_refresh_token(refresh_token):
    return jwt.decode(
    refresh_token,
    b64decode('refresh_secret'),
    algorithms=['HS256']
)
