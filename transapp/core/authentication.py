import jwt
from dotenv import dotenv_values

env_var = dotenv_values()
ACCESS_SECRET = 'django-insecure-6014=#wx7fw#=*x3e-0l+(3jhj5p@bi2d=^q-qy3$k0i7!%qs)'
REFRESH_SECRET = env_var['REFRESH_SECRET'] 
ALG = env_var['ALG'] 


def decode_access_token(access_token):
    return jwt.decode(
    access_token,
    ACCESS_SECRET,
    algorithms=[ALG])

