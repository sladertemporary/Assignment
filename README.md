# Assignment

To do list:
- API fetch endpoint
- Adjust DB commit method to use real parameters
- Validation, model parameters
- Docker container config (redis, flask, rq, sqlalchemy, sqlite)
- Tests
- Documentation & Comments

## Documentation

### Event Store

Store an event with geolocation acquired from Geolocation API

**URL** : `/event/submit/`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints**

```json
{
    "name": "[1 to 30 chars]",
    "status_code": "[1 to 30 chars]"
}
```

**Data examples**

Partial data is allowed.

```json
{
    "name": "EC2 Instance Offline",
    "status_code": "2"
}
```

#### Success Responses

**Condition** : Data provided is valid and task succesfully assigned to Redis worker.

**Code** : `202 Accepted`

**Content example** : Response will include details of the task ID for submitting event to database. 

```json
{
    "data": {
        "task_id": "faadc2ae-7c74-4a0f-8d65-ae92dfddf882"
    },
    "status": "success"
}
```

#### Error Response

**Condition** : If provided data is invalid, e.g. a name field is too long.

**Code** : `400 BAD REQUEST`




## Deployment proposition

