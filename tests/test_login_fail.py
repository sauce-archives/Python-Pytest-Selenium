import pytest


@pytest.mark.usefixtures("driver")
def test_valid_crentials_login(driver):
    driver.get('https://www.saucedemo.com')

    driver.find_element_by_id('user-name').send_keys('locked_out_user')
    driver.find_element_by_id('password').send_keys('secret_sauce')
    driver.find_element_by_css_selector('.login-button').click()

    assert driver.find_element_by_css_selector('.error-button').is_displayed()
