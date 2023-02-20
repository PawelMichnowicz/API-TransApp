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
- Microservice written in FastAPI used to send emails
- Unitests 


Rest of the features are included below in the table of endpoints:

Endpoint |HTTP Method | Result
-- | -- |--
`document/check-company` | GET | Get contractor data from the GUS (Główny Urząd Statystyczny)
`document/documents/` | GET | Get list of documents available in database
`storage/warehouses/` | GET | Get list of warehouse instances
`storage/warehouses/` | POST | Create warehouse instance
`storage/warehouses/{id}/` | GET | Retrive warehouse instance
`storage/warehouses/{id}/` | PUT | Update warehouse instance data
`storage/warehouses/{id}/` | DELETE | Delete warehouse instance
`storage/warehouse-stats/{id}/` | GET | Get statistics of the warehouse
`storage/workers-stats/`| GET | Get statistics of warehouse workers
`storage/actions-for-coordinator/`| GET | Get actions data available for coordinator
`storage/actions-for-coordinator/{id}`| GET | Get data of the action available for coordinator
`storage/actions-for-director/`| GET | Get actions data available for director of warehouse
`storage/actions-for-director/{id}/`| GET | Get data of the action available for director of warehouse
`storage/warehouse-add-action-window/`| POST | Add extra action time slot to warehouse instance
`storage/warehouse-overwrite-action-window/{id}/` | POST | Overwrite time slot of the action in the warehouse instance
`storage/action-approve-delivery/{id}/`| POST | Confirm the action as delivered to warehouse and assign its duartion and workers
`storage/action-approve-inprogress/{id}/`| POST | Confirm the action as prepared for delivery and assign its action time slot and warehouse instance
`storage/action-complain-email/{id}/`| POST | Send an email using microservice regarding damaged orders
`transport/vehicles` | GET | Get list or retrive vehicle instance
`transport/vehicles/{id}` | GET | Retrive vehicle instance
`transport/routes` | GET | Get list or retrive route instance
`transport/routes/{id}` | GET | Retrive route instance
`transport/transports` | GET | Get list or retrive transport instance
`transport/transports/{id}` | GET | Retrive transport instance






