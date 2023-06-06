## Create project

```shell
  docker-compose up frontend --build
  docker-compose up postgres --build
  docker-compose up django --build
```

### Run project
```shell
#   FULL
  docker-compose up
#   ONLY ONE PART
  docker-compose start django
  docker-compose start frontend
#   TO STOP
  docker-compose stop django
  docker-compose stop frontend
```