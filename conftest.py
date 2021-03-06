import pytest
import logging
import allure
from selenium import webdriver
from helper import create_dir_logs
import requests
from helper import wait_start_server
from config import settings
from component_api.my_requests import MyRequests
create_dir_logs()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='w',
                    level=logging.INFO, filename='_logs/selenium.log')

with open("tests/test_api/end_points", 'r') as params:
    list_params = params.readlines()
    list_endpoints = [i.strip('\n') for i in list_params]


def pytest_addoption(parser):
    parser.addoption("--browser", action="store_true", default="chrome")
    parser.addoption('--headless', action="store_true", help="Run headless")
    parser.addoption('--executor', action="store_true")
    parser.addoption('--bversion', action="store", default="96.0", help="version browser")
    parser.addoption('--system', action='store', default='ubuntu', help='if start on windows set win')
    parser.addoption('--docker_start', action="store_true")


@pytest.fixture(scope='session')
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    headless = request.config.getoption("--headless")
    bversion = request.config.getoption("--bversion")
    system = request.config.getoption("--system")
    wait_server_start = request.config.getoption('--docker_start')

    if wait_server_start:
        # waiting server
        wait_start_server(settings.url.ip_docker)
    if executor:
        caps = {
            "browserName": browser,
            "browserVersion": bversion,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False,
                "screenResolution": '1920x1080x24'
            },
            'goog:chromeOptions': {}
        }
        browser = webdriver.Remote(
            command_executor=f'http://{settings.url.ip_docker}:4444//wd/hub',
            desired_capabilities=caps
        )
        browser.get(f'http://{settings.url.ip_docker}:7070')
    elif headless:
        options = webdriver.ChromeOptions()
        options.headless = request.config.getoption("--headless")
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        browser.get(f'http://{settings.url.ip_docker}:7070')
    elif system == 'win':
        browser = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
    else:
        browser = webdriver.Chrome()
    browser.maximize_window()

    def fin():
        browser.quit()

    request.addfinalizer(fin)
    return browser


@pytest.fixture(scope='function')
def log_fixture(request, browser):
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
    return MyRequests.request_get(end_point)
