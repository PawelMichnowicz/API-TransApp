import jwt, datetime
from dotenv import dotenv_values

env_var = dotenv_values()
ACCESS_SECRET = 'django-insecure-6014=#wx7fw#=*x3e-0l+(3jhj5p@bi2d=^q-qy3$k0i7!%qs)'
REFRESH_SECRET = env_var['REFRESH_SECRET'] 
ALG = env_var['ALG'] 


def create_access_token(user):
    return jwt.encode({
        'user_id': user['id'],
        'email' : user['email'],
        'username' : user['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
        'iat': datetime.datetime.utcnow()
        },
        ACCESS_SECRET, 
        algorithm=ALG)

def decode_access_token(access_token):
    return jwt.decode(
    access_token,
    ACCESS_SECRET,
    algorithms=[ALG])

def create_refresh_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
        },
        REFRESH_SECRET,
        algorithm=ALG)

def decode_refresh_token(refresh_token):
    return jwt.decode(
    refresh_token,
    REFRESH_SECRET,
    algorithms=[ALG]
)
