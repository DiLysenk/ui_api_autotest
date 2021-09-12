import pytest
import logging
import allure
import time
from selenium import webdriver
from config_parser import ConfigParser
import requests
import os
from requests.exceptions import ConnectionError



config = ConfigParser()
try:
    os.mkdir('logs')
    os.mkdir('allure')
except FileExistsError:
    print('папка создана всё ок')


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w',
                    level=logging.INFO, filename='logs/selenium.log')


with open("test/test_api/end_points", 'r') as params:
    list_params = params.readlines()
    list_endpoints = [i.strip('\n') for i in list_params]

for i in range(10):
    i += 1
    time.sleep(15)
    try:
        var = requests.get('http://172.17.0.1:7070').status_code
        break
    except ConnectionError:
        print("сервер c opencart еще не поднялся")
        pass
        if i == 10:
            raise AssertionError("сервер c opencart не поднялся, попробуйте запустить еще раз")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption('--headless', action="store_true", help="Run headless")
    parser.addoption('--executor', action="store")
    parser.addoption('--bversion', action="store", default="91.0", help="version browser")


@pytest.fixture(scope='session')
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    headless = request.config.getoption("--headless")
    bversion = request.config.getoption("--bversion")
    if executor != None:
        caps = {
            "browserName": browser,
            "browserVersion": bversion,
            'goog:chromeOptions': {}
        }
        browser = webdriver.Remote(
            command_executor=f'http://172.17.0.1:4444//wd/hub',
            desired_capabilities=caps
        )
        browser.maximize_window()
        browser.get(config.USER_FRONT)
    elif headless == True:
        options = webdriver.ChromeOptions()
        options.headless = request.config.getoption("--headless")
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        browser.get(config.USER_FRONT)
    else:
        browser = webdriver.Chrome()
        browser.maximize_window()

    def fin():
        browser.quit()

    request.addfinalizer(fin)
    return browser


@pytest.fixture(scope='function')
def loging(request, browser):
    logger = logging.getLogger('BrowserLogger')
    test_name = request.node.name

    logger.info(f"===> Test started name, test is {test_name}")

    def fin():
        allure.attach(
            browser.get_screenshot_as_png(),
            name='finalizer attach',
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"===> Test finished name, test is {test_name}")

    request.addfinalizer(fin)

@pytest.fixture(name="end_point", params=list_endpoints)
def get_end_point(request):
    yield request.param


@pytest.fixture
def response_get(end_point):
    return requests.get(end_point)