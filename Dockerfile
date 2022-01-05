FROM ubuntu:20.04

WORKDIR /app

COPY requirements.txt .

RUN
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .

CMD pytest --executor --docker_start && allure serve allure-report