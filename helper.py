import time
import requests
import os
from requests.exceptions import ConnectionError

RETRY = 20


def wait_server():
    for i in range(RETRY):
        try:
            requests.get('http://172.17.0.1:7070').status_code == 200
        except ConnectionError:
            time.sleep(i)
            if i == RETRY - 1:
                raise AssertionError("сервер c opencart не поднялся, попробуйте запустить еще раз")


def create_dir_logs():
    try:
        os.mkdir('logs')
    except FileExistsError:
        print('папка создана всё ок')


def create_dir_allure():
    try:
        os.mkdir('allure')
    except FileExistsError:
        print('папка создана всё ок')


wait_server()