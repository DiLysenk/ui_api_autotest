import time
import requests
import os
from requests.exceptions import ConnectionError

import logging


RETRY = 5


def wait_start_server(ip):
    for i in range(RETRY):
        try:
            if requests.get(f'http://{ip}:7070').status_code == 200:
                return
        except ConnectionError:
            time.sleep(i)
            logging.error(f'сервис не доступен {i} сек ')
            if i == RETRY - 1:
                raise AssertionError(
                    f'http://{ip}:7070 сервер c opencart не поднялся, попробуйте запустить еще раз')


def create_dir_logs():
    try:
        os.mkdir('_logs')
    except FileExistsError:
        print('папка создана всё ок')


class Helper:

    @staticmethod
    def get_unique_entity(list_of_entity):
        unique = []
        for entity in list_of_entity:
            if entity not in unique:
                unique.append(entity)
        return unique

    @staticmethod
    def get_unique_in_column(list_of_entity):
        entity = Helper.get_unique_entity(list_of_entity)
        while " " in entity:
            entity.remove(" ")
        return entity

    @staticmethod
    def filter_in_column(value):
        if " " != value:
            return value

    @staticmethod
    def filter_for_pagination(value):
        if "..." != value.text:
            try:
                return value
            except ValueError:
                raise AssertionError("Проверить пагинацию, ожидалось число")

    @staticmethod
    def find_in_elements_by_text(list_of_elements, text):
        for element in list_of_elements:
            if element.text == str(text):
                return element
