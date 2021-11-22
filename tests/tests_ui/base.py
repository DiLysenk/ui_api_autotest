from pageobject.register_page import RegisterPage
from pageobject.admin_page import AdminPage, CssAdminPage
from pageobject.login_page import LoginAdminPage
from pageobject.main_page import MainPage
from _pytest.fixtures import FixtureRequest
import pytest

class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, request: FixtureRequest):
        self.driver = driver

        self.login_admin: LoginAdminPage = request.getfixturevalue('login_admin')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.admin_page: AdminPage = request.getfixturevalue('admin_page')
        self.register_page: RegisterPage = request.getfixturevalue('register_page')
