import configparser


class ConfigParser:

    def __init__(self):
        self.parsed = self.config_parser()
        self.LOGIN = self.parsed[0]
        self.PASSWORD = self.parsed[1]
        self.ADMIN_FRONT = self.parsed[2]
        self.USER_FRONT = self.parsed[3]

    def config_parser(self):
        path = ['test.config']
        config = configparser.ConfigParser()
        for i in range(len(path)):
            try:
                config.read(path[i])
            except configparser.NoSectionError:
                raise AssertionError("конфигурационный файл не найден")
        login = config.get('user', 'username')
        password = config.get('user', 'password')
        admin_front = config.get('url', 'admin_front')
        user_front = config.get('url', 'user_front')
        return login, password, admin_front, user_front
