from pageobject.register_page import RegisterPage
from pageobject.admin_page import AdminPage, CssAdminPage
from pageobject.login_page import LoginAdminPage
from pageobject.main_page import MainPage
import pytest
import allure
from faker import Faker

myFactory = Faker()


@pytest.mark.usefixtures('log_fixture')
class TestOpenCart:


    @allure.description("""Проверка согдания пользователя""")
    @allure.title('тест создание пользоватиеля')
    def test_registration(self, browser):
        p = RegisterPage(browser)
        p. \
            navigate_to(p.URL_REGISTER). \
            fill_form(myFactory.name(), myFactory.email()). \
            agree_policy(). \
            click_continue()
        assert browser.current_url[len(browser.current_url) - 7:] == "success", 'неудача'

    @allure.description("""Добавление нового контента в список товаров""")
    @allure.title('тест новго товара')
    def test_add_new_item(self, browser):
        name = myFactory.color()
        p = LoginAdminPage(browser)
        p. \
            navigate_to(p.ADMIN_PAGE). \
            login_admin()
        AdminPage(browser) \
            .go_to_Products() \
            .add_product(name)
        assert p.find_by_text(name), f"не найден товар{name}"

    @allure.description("""Проверка удаление товара с первой строчки""")
    @allure.title('тест удаление товара')
    def test_delete_item(self, browser):
        LoginAdminPage(browser). \
            navigate_to(LoginAdminPage.ADMIN_PAGE). \
            login_admin()
        AdminPage(browser).go_to_Products() \
            .select_product() \
            .delete_product()
        assert AdminPage(browser).find_presence(CssAdminPage.SUCCESS_DELETE), "товар не удалён"

    @allure.description("""Проверка изменение валюты на главной странице""")
    @allure.title('тест изменение валюты')
    def test_switch_currency(self, browser):
        MainPage(browser). \
            navigate_to(MainPage.OpenCArt). \
            change_currency()
        assert MainPage(browser).find_by_text('£'), "валюта не переведена"

    @allure.description("""Проверка изменение валюты на главной странице""")
    @allure.title('тест изменение валюты ')
    @pytest.mark.xfail
    def test_switch_currency_fail(self, browser):
        p = MainPage(browser)
        p. \
            navigate_to(p.OpenCArt). \
            change_currency()
        assert p.find_by_text('₽'), "не должно быть такой валюты"
