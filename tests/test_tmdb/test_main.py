from pageobject.tmdb_page import TMDB
import allure
import pytest


@allure.parent_suite("UI")
@allure.suite("themoviedb.org")
@allure.label("owner", "QA")
@pytest.mark.usefixtures('log_fixture')
class TestTMDBPage:

    @allure.description("""login in site""")
    @allure.title("login")
    @pytest.mark.smoke
    def test_main(self, browser):
        p = TMDB(browser)
        p.navigate()
        p.login()
        assert p.find_by_link_text('xBender')

    @allure.description("""search movie""")
    @allure.title("login")
    @pytest.mark.smoke
    def test_search_movie(self, browser):
        p = TMDB(browser)
        p.navigate()
        p.fill_search_field('spider-man')
        assert p.find_by_link_text('Spider-Man')
