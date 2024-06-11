# flask-learning

Repository used to learn about Flask, a Python microframework

This tests uses a postgreSQL database, that could be used via docker.

To start database open docker folder and use de follow command at terminal:

`docker-compose up -d`

## Dados de conexão

Database config:

- **host**: localhost (ou 127.0.0.1)
- **port**: 5435
- **database**: flask-db
- **user**: flask-user
- **pass**: flask

#### Connection string:

jdbc:postgresql://localhost:5435/flask-db

## Docker

Docker is required to run the db dockerfile.

See more at https://docs.docker.com/get-docker/

#### Update passwords

At first execution, use the path http://127.0.0.1:5000/update_default_users_passwords to update the passwords with encryption.