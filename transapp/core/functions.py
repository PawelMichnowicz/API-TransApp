import requests

def send_email(url, email, email_text, token):
    '''Send email using external url from email_api microservice'''
    send_email_json = {'token': token,
                    'email': email,
                    'email_text': email_text,
                    }
    response = requests.post(url, json=send_email_json)
    return response