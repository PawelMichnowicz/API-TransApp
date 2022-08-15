import requests

def send_email(url, email, email_text, token):
    send_email_json = {'token': token,
                    'email': email,
                    'email_text': email_text,
                    }
    response = requests.post(url, json=send_email_json)
    return response
