FROM python:3.8 as base

FROM base as testing
COPY tests/ ./tests
RUN python3 ./tests/test_app.py 

# command to run on container start
FROM base as main-app
WORKDIR /code
COPY src/ .
CMD [ "python3", "./app.py" ]