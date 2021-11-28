from pageobject.tmdb_page import TMDB

def test_main(browser):
    p = TMDB(browser)
    p.navitage()
    p.login()
    assert p.is_visible_by_link_text('xBender')

def test_changed_sorting(browser):
    p = TMDB(browser)
    p.navitage()
    p.naviate_to_pop()
    p.choose_sorting('По рейтингу')

    assert p.is_visible_by_link_text('Di Mapigil ang Init')
