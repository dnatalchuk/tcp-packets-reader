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
❯ DOCKER_BUILDKIT=0 docker build . -t challenge
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
docker run --name=challenge-app -d -v /proc/net/tcp:/code/tcp_file challenge:latest
```
* Command above in order to access `/proc/net/tcp` of the host - volume will be mounted inside docker container under path `/code/tcp_file`. The path to poll connections is managed via `POLLING_PATH` variable in code level (default value: `/code/tcp_connections`);

* Once container will be started and respective id associated - run command below to check container execution logs:

```
❯ docker logs `docker ps -aqf "name=challenge-app"`
```
* Output from the above command should be similar to below:

```
❯ docker logs `docker ps -aqf "name=challenge-app"`
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

## Questions and Answers:
* `L1`:
```
1. How would you prove the code is correct?

Answer: By running the test script and passing the sample content of `/proc/net/tcp` that is defined in `sample_tcp_file.txt` which is consumed during GitHub Actions execution pipeline. Program output will present results in a format according to the declared scope of the task.

2. How would you make this solution better?

Answer: Add unit tests for all the functions used in the Python script and integration tests as well; improve and add more support for security and authorization while app usage; improve app output/execution logging to either to 3rd party solution or open-sourced solutions; add Prometheus exporter to calculate and present key app metrics; on top of Prometheus metrics add Grafana dashboards to visualize better app metrics for analytics and monitoring purposes; add alerting capabilities using Prometheus alertManager to inform in case app stopped running or critical app errors appeared; extend GitHub actions capabilities not only to build the docker image but also add release tagging flow to map specific git tags to docker image version (currently latest tag is used), also add logic to pipeline to manage docker image push to the registry and deployment to target environment via CD tool of choice; another possible improvement might be to rewrite this app from Python3 to Go instead, to achieve better performance and resource utilization.

3. Is it possible for this program to miss a connection?

Answer: It shouldn't, but some corner cases might appear.

4. If you weren't following these requirements, how would you solve the problem of logging every new connection?

Answer: There is a possibility to use some message queues implementations, so we will ensure that each message will not be missed and consumed by the consumer once they're ready. Also, we can couple consumers running, so even in case of issues with the one consumer - another one will continue to consume and handle messages accordingly. 

```
* `L2`:
```
1. Why did you choose x to write the build automation?

Answer: GitHub Actions have been chosen because of its native integration with GitHub; ease to configure and manage; no operational overhead to manage this CI tool; fast pipelines execution and nice visualization.

2. Is there anything else you would test if you had more time?

Answer: Add unit tests for all the functions used in the Python script and integration tests as well; conduct performance testing to identify existing app performance limitations and quotas; perform penetration testing to identify possible security threats and mitigate them;

3. What is the most important tool, script, or technique you have for solving problems in production? Explain why this tool/script/technique is the most important.

Answer: For solving and preventing possible issues on production, only automation should be used for making any changes via respective changes on git level as well, but no manual operations. It helps to mitigate a lot of possible issues and unknowns, make processes more reliable and confident, have the possibility to trace end-2-end changes made and it's consequences. There are also a lot of tools and best practices to follow.


```
* `L3`:
```
1. If you had to deploy this program to hundreds of servers, what would be your preferred method? Why?

Answer: Since this app is Dockerised, the best way would be to use Kubernetes (preferably k8s available on the public cloud) to orchestrate and manage app lifecycle, resiliency, seal-healing, optimal resources allocation, and management. Additional reasons are Multi-cloud capability, increased developer productivity, Open source, proven and battle-tested, the market leader, developed eco-system.

2. What is the hardest technical problem or outage you've had to solve in your career? Explain what made it so difficult?

Answer: It was the situation at the beginning of my carrier and I was managing and cooperating with local data center decommissioning and migrating to the remote one in another country. It was quite a big project to complete, with a lot of unknowns, a lot of parties involved, and integration challenges. But it was successfully completed and implemented with no impact on customers, but performance and costs reductions were achieved for the company.

```
