from .base_test import *


@on_platforms(browsers)
class GuineaPigTest(BaseTest):

    @classmethod
    def setup_class(cls):
        BaseTest.setup_class()

    # verify page title
    def test_title(self):
        self.driver.get('https://saucelabs.com/test/guinea-pig')
        title = "I am a page title - Sauce Labs"
        self.assertEqual(title, self.driver.title, "Title does not match!")

    # verify no focus text
    def test_nofocus_text(self):
        self.driver.get('https://saucelabs.com/test/guinea-pig')
        text = "i has no focus"
        self.assertEqual(text, self.driver.find_element_by_id("i_am_a_textbox").get_attribute("value"),
                           "No focus text does not match!")

    # verify email text entry
    def test_email_entry(self):
        self.driver.get('https://saucelabs.com/test/guinea-pig')
        email = "hede@hodo.com"
        email_text_field = self.driver.find_element_by_id("fbemail")
        email_text_field.click()
        email_text_field.send_keys(email)
        self.assertEqual(email, email_text_field.get_attribute("value"), "Email text does not match!")


if __name__ == '__main__':
    unittest.main()
