from pageobject.grfc import GRFC


def test_action(browser):
    page = GRFC(browser)

    page.open_page()
    page.click_find()
    page.input_in_find('radio')
    page.push_enter()
    page.wait_time(5)
