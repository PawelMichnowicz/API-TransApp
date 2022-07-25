
def create_client(**params):
    defaults = {
            'username':'user_',
            'password':'123',
            'position':"DIR",
            'warehouse':None,
        }

    defaults.update(**params)

    print(defaults)




create_client(**{'position':'USR'})