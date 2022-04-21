# Test task for the interview

## How to run
To run the application on a local machine, docker and docker-compose are required.
```bash
docker build . -t finstc
docker compose up
```
You can also run the application without using a docker container.
To do this, you need to install the dependencies from requirements.txt and start the uvicorn server:
```bash
python -m pip install -r requirements.txt
python run.py
```
In this case, the necessary settings can be set in environment variables or in the config.py file:
```bash
export DB_ADDRESS=db
export DB_USER=finstc-user
export DB_PASSWORD=secret-for-finstc-user
export DB_NAME=finstc
export LOG_LEVEL=debug
export SERVICE_HOST='10.50.2.10'
export SERVICE_PORT=3520
```

## Documentation OpenAPI
After running the application, you can read the API specification at http://127.0.0.1:3520/docs (in case of standard setting).

The documentation is presented in the form of a Swagger UI panel with an OpenAPI-generated specification for the service.

The documentation specifies the request and response bodies in the form of JSONSchema.

## Request examples

### List of vehicles
```bash
curl --location --request GET 'http://127.0.0.1:3520/vehicle'
```

### Create vehicle
```bash
curl --location --request POST 'http://127.0.0.1:3520/vehicle' \
--header 'Content-Type: application/json' \
--data-raw '{
    "colour": "white",
    "vin": "some vin",
    "year": 2022,
    "brand": "Ford",
    "model": "Mustang",
    "diller_id": "b64ee5e4a2124f3eac82254238c56848"
}'
```

### Update vehicle
```bash
curl --location --request PUT 'http://127.0.0.1:3520/vehicle/a8cd66ccd5e64b6eb6a679c6ef826c48' \
--header 'Content-Type: application/json' \
--data-raw '{
    "brand": "Opel",
    "year": 2021
}'
```

### Delete vehicle
```bash
curl --location --request DELETE 'http://127.0.0.1:3520/vehicle/a8cd66ccd5e64b6eb6a679c6ef826c48'
```

### List of dillers
```bash
curl --location --request GET 'http://127.0.0.1:3520/diller'
```

### Create diller
```bash
curl --location --request POST 'http://127.0.0.1:3520/diller' \
--header 'Content-Type: application/json' \
--data-raw '{
"company_name": "Yellow Submarine",
"address": "Russia, Murmansk"
}'
```

### Diller update
```bash
curl --location --request PUT 'http://127.0.0.1:3520/diller/63c9ba193d0948f88507072d50345abd' \
--header 'Content-Type: application/json' \
--data-raw '{
    "address": "Russia, Moscow",
    "company_name": "BMW Motorrad"
}'
```

### Diller delete
```bash
curl --location --request DELETE 'http://127.0.0.1:3520/diller/b64ee5e4a2124f3eac82254238c56848'
```