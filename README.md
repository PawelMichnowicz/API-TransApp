API to manage delivery to warehouse 
======
A REST API written in Django-Rest-Framework with additional microservice written in FastAPI.

## Usage and installation

```sh
git clone https://github.com/PawelMichnowicz/API-TransApp.git
docker-compose up --build
```


## Features 

- User Authentication system by JWT
- Users have various possibility based on their work position
- Microservice used to send emails
- Unitests 

Rest of features describe in table below:

Endpoint |HTTP Method | Result
-- | -- |--
`document/check-company` | GET | Get contractor data from the GUS
`document/documents/` | GET | Get list of documents available in database
`storage/action-approve-delivery/{id}/`| POST | Confirm delivery to warehouse and assign its duartion and workers
...




