import pytest


@pytest.mark.usefixtures("driver")
def test_valid_crentials_login(driver):
    driver.get('http://www.saucedemo.com')

    driver.execute_script("window.open('https://www.saucelabs.com')")

    assert driver.window_handles

