from pageobject.tmdb_page import TMDB


def test_main(browser):
    p = TMDB(browser)
    p.navitage()
    p.login()
    assert p.find_by_link_text('xBender')


def test_changed_sorting(browser):
    p = TMDB(browser)
    p.navitage()
    p.navigate_to_popular()
    p.select_element(p.loc.SORT_BTN, 'Popularity Ascending')
    assert p.find_by_link_text('Di Mapigil ang Init')
