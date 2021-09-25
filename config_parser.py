import configparser
import os


class ConfigParser:

    def __init__(self):
        self.config = self.config_parser()
        self.LOGIN = self.config['login']
        self.PASSWORD = self.config['password']
        self.ADMIN_FRONT = self.config['admin_front']
        self.USER_FRONT = self.config['user_front']

    def config_parser(self):

        config = configparser.ConfigParser()
        path = os.getcwd().split('/')

        for j in range(len(path)):
            full_path = ''
            for i in path:
                part = str(i + '/')
                full_path = full_path + part
            if os.path.isfile(full_path + 'test.config') == True:
                try:
                    config.read(full_path + 'test.config')
                except configparser.NoSectionError:
                    print("конфигурационный файл не найден")
            else:
                path = path[:-1]

        login = config.get('user', 'username')
        password = config.get('user', 'password')
        admin_front = config.get('url', 'admin_front')
        user_front = config.get('url', 'user_front')

        return {'login': login, 'password': password, 'admin_front': admin_front, 'user_front': user_front}
