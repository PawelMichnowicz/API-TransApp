import jwt
import environ

env = environ.Env()
environ.Env.read_env()
ACCESS_SECRET = env('ACCESS_SECRET') 
ALG = env('ALG') 

def decode_access_token(access_token):
    return jwt.decode(
    access_token,
    ACCESS_SECRET,
    algorithms=[ALG])
