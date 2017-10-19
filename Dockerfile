FROM python:3.6
RUN apt-get update && apt-get install -y redis-server
COPY . /web
WORKDIR /web
RUN pip install pipenv
RUN pipenv install --ignore-pipfile
EXPOSE 8000
CMD redis-server /etc/redis/redis.conf && pipenv run python app.py
