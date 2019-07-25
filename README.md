# Assignment (incomplete)

A simple event collection API allowing both the submission and fetching of events. Events are located using the source IP address of the event submission by calling an external Geolocation API (*pulled from docker hub workivate/geoip-api*).

The application itself has the following requirement(s):

- API must be able to deal with Geolocation API limitations 
- Average response time from API should be around ~200ms or less

 The external API has the following limitations:

- API can handle only 5 requests per second
- Geolocation API likes to have a "hiccup" and returning a response may take even up to 5 seconds

Tasks currently outstanding:

- Docker container setup
- Validation, insert actual parameters into db, code commenting
- API endpoint for fetching
- Tests

### Requirements

flask, redis, sqlalchemy, redis queue, docker

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
    "name": "[1 to 120 chars]",
    "status_code": "[integer]"
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

For production, **uWSGI** and **NGINX** should be used to serve the flask application. The application should be setup using a **docker** container for portability. If the expected load on the application requires a cluster setup to meet load demand, the application should also be configured to use an external database and redis server. 

**It is highly recommended that this application should be secured with authentication and throttled to avoid abuse of the API. Logging must also be used to monitor application health.**

Following the suggested changes for production, the **docker** container can be deployed onto AWS as an ECS service with a load balancer attached. An RDS database (e.g. using MySQL) can be used.

