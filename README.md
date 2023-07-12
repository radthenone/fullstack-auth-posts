<!-- markdownlint-disable MD033 MD022 MD001 MD041 -->
# Fullstack auth posts

| Apps       | Results                                                                                                                                                                                        |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pre-commit | [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/radthenone/fullstack-auth-posts/main.svg)](https://results.pre-commit.ci/latest/github/radthenone/fullstack-auth-posts/main) |
| coverage   | [![Coverage Status](https://coveralls.io/repos/github/radthenone/fullstack-auth-posts/badge.svg?branch=main)](https://coveralls.io/github/radthenone/fullstack-auth-posts?branch=main)           |


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
