# Quick little demo

```sh
docker build -t test-py .
clear
docker run -t test-py # this yields no token
docker run -e SECRET_TOKEN="hello world" -t test-py # this prints hello world
```

Dont do env files in docker containers. Pass in the value via environment variables 
