import logging
import time
import requests
import os
from requests.exceptions import ConnectionError
from config_parser import ConfigParser
import logging
import enum

config = ConfigParser()
RETRY = 5


def wait_server():
    for i in range(RETRY):
        try:
            if requests.get(f'http://{config.IP_DOCKER}:7070').status_code == 200:
                return
        except ConnectionError:
            time.sleep(i)
            logging.error(f'сервис не длступен {i} сек ')
            if i == RETRY - 1:
                raise AssertionError(
                    f'http://{config.IP_DOCKER}:7070 сервер c opencart не поднялся, попробуйте запустить еще раз')


def create_dir_logs():
    try:
        os.mkdir('_logs')
    except FileExistsError:
        print('папка создана всё ок')


def create_dir_allure():
    try:
        os.mkdir('_allure')
    except FileExistsError:
        print('папка создана всё ок')


def selector(locator):
    if locator is enum.EnumMeta:
        return locator.val
    return locator

