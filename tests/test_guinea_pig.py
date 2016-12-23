import pytest


@pytest.mark.usefixtures('driver')
class TestGuineaPig(object):

    def test_title(self, driver):
        """
        Verify page title
        :return: None
        """
        driver.get('https://saucelabs-sample-test-frameworks.github.io/training-test-page')
        title = "I am a page title - Sauce Labs"
        assert title == driver.title

    def test_nofocus_text(self, driver):
        """
        Verify no focus text
        :return: None
        """
        driver.get('https://saucelabs-sample-test-frameworks.github.io/training-test-page')
        text = "i has no focus"
        assert text == driver.find_element_by_id("i_am_a_textbox").get_attribute("value")

    def test_email_entry(self, driver):
        """
        Verify email text entry
        :return: None
        """
        driver.get('https://saucelabs-sample-test-frameworks.github.io/training-test-page')
        email = "hede@hodo.com"
        email_text_field = driver.find_element_by_id("fbemail")
        email_text_field.click()
        email_text_field.send_keys(email)
        assert email == email_text_field.get_attribute("value")
