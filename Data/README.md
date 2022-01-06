# brad rapid annotation tool
Forked from https://github.com/knaw-huc/brat-docker
## Build

    docker build -t brat .

## Local setup

Create a dir for authenticated users:

    mkdir secrets

Create a file 'secrets/users.json' containing username/password pairs
as follows:

```
{
    "User1": "secret1",
    "User2": "secret2"
}
```

## Run

    docker run -p 8001:8080 -v "$(pwd)/secrets:/secrets" brat

Point browser to http://localhost:8001 and login using credentials from
users.json.

## Run using docker-compose

```docker-compose.yml
version: "3.6"
services:
  brat:
    build: .
    volumes:
      - ./data:/data
      - ./work:/work
      - ./secrets:/secrets
    ports:
      - 8001:8080
```

Run:

    $ docker-compose up
