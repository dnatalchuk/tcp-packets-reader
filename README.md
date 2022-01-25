# Python application to report new TCP connections on a Linux host.

> Program toto read /proc/net/tcp every 10 seconds and outputs any new connections. 

## Prerequisites:
* `Python 3.8`


## Table of contents and structure

```
.
|-- Dockerfile
|-- README.md
|-- src
|   `-- app.py
`-- tests
    |-- sample_tcp_file.txt
    `-- test_app.py
```

## Building docker image and testing locally:
* `DOCKER_BUILDKIT=0 docker build . -t challenge_app`
* Sample output:
```
❯ DOCKER_BUILDKIT=0 docker build . -t tcp-packets-reader
Sending build context to Docker daemon  15.87kB
Step 1/8 : FROM python:3.8 as base
 ---> 1d136c1ca7e1
Step 2/8 : FROM base as testing
 ---> 1d136c1ca7e1
Step 3/8 : COPY tests/ ./tests
 ---> 735f9c8cd1cf
Step 4/8 : RUN python3 ./tests/test_app.py 
 ---> Running in d5e61d38beb7
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:39199 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:63967 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:56253 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:264 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 127.0.0.1:34690 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:52120 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:28416 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:5555 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 127.0.0.53:13568 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 0.0.0.0:5632 -> 0.0.0.0:0
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:63628 -> 91.189.91.15:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:41164 -> 172.217.13.110:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:6876 -> 169.254.169.254:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:7900 -> 169.254.169.254:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:46296 -> 91.189.88.152:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:27821 -> 91.189.92.20:47873
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:7388 -> 169.254.169.254:20480
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:62692 -> 91.189.91.42:47873
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:5632 -> 204.225.215.59:19417
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:42726 -> 91.189.88.179:47873
2021-08-09 11:43:46+00:00: New connection: 10.162.15.225:45784 -> 91.189.88.152:20480
Removing intermediate container d5e61d38beb7
 ---> 9472b33849d8
Step 5/8 : FROM base as main-app
 ---> 1d136c1ca7e1
Step 6/8 : WORKDIR /code
 ---> Using cache
 ---> 443fceabe0b4
Step 7/8 : COPY src/ .
 ---> Using cache
 ---> faec9b3674d5
Step 8/8 : CMD [ "python3", "./app.py" ]
 ---> Running in 8855050bee7e
Removing intermediate container 8855050bee7e
 ---> c0e29e48a467
Successfully built c0e29e48a467
Successfully tagged challenge:latest
```

* During docker build runtime - the test stage will be executed to show that the application working as expected.
* For testing purpose - the same content of `app.py` is used except variable `POLLING_PATH` (the path to poll connections defined on code level and default value is `/code/tcp_connections`). For `POLLING_PATH` the sample content of `/proc/net/tcp` is defined in `sample_tcp_file.txt` which is consumed during the testing phase;

## Running the application and check execution results:
* Start the application and run the respective docker image with the next command:

```
docker run --name=challenge-app -d -v /proc/net/tcp:/code/tcp_file tcp-packets-reader:latest
```
* Command above in order to access `/proc/net/tcp` of the host - volume will be mounted inside docker container under path `/code/tcp_file`. The path to poll connections is managed via `POLLING_PATH` variable in code level (default value: `/code/tcp_connections`);

* Once container will be started and respective id associated - run command below to check container execution logs:

```
❯ docker logs `docker ps -aqf "name=tcp-packets-reader"`
```
* Output from the above command should be similar to below:

```
❯ docker logs `docker ps -aqf "name=tcp-packets-reader"`
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:39199 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:63967 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:56253 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:264 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 127.0.0.1:34690 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:52120 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:28416 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:5555 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 127.0.0.53:13568 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 0.0.0.0:5632 -> 0.0.0.0:0
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:63628 -> 91.189.91.15:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:41164 -> 172.217.13.110:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:6876 -> 169.254.169.254:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:7900 -> 169.254.169.254:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:46296 -> 91.189.88.152:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:27821 -> 91.189.92.20:47873
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:7388 -> 169.254.169.254:20480
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:62692 -> 91.189.91.42:47873
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:5632 -> 204.225.215.59:19417
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:42726 -> 91.189.88.179:47873
2021-08-09 15:33:45+00:00: New connection: 10.162.15.225:45784 -> 91.189.88.152:20480
```

Test weebhook
