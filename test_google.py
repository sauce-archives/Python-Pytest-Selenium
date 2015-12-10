import os
import unittest
import sys
import new
from selenium import webdriver
from sauceclient import SauceClient

browsers = [{
    "platform": "Windows 10",
    "browserName": "internet explorer",
    "version": "11"
}, {
    "platform": "OS X 10.10",
    "browserName": "safari",
    "version": "8"
}]

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']
log_output = os.environ['LOG_OUTPUT']

# This decorator is required to iterate over browsers
def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator

def log_to_file(data):
    if log_output:
        with open("result_log.txt", "a") as f:
            f.write(data + "\n")

@on_platforms(browsers)
class FirstSampleTest(unittest.TestCase):

    # setUp runs before each test case
    def setUp(self):
        self.desired_capabilities['name'] = self.id()
        self.driver = webdriver.Remote(
           command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
           desired_capabilities=self.desired_capabilities)

    # verify google title
    def test_google(self):
        self.driver.get("http://www.google.com")
        assert ("Google" in self.driver.title), "Unable to load google page"

    # type 'Sauce Labs' into google search box and submit
    def test_google_search(self):
        self.driver.get("http://www.google.com")
        elem = self.driver.find_element_by_name("q")
        elem.send_keys("Sauce Labs")
        elem.submit()

    # tearDown runs after each test case
    def tearDown(self):
        self.driver.quit()
        session_id = self.driver.session_id
        job_name = self.id()
        sauce_client = SauceClient(username, access_key)
        status = (sys.exc_info() == (None, None, None))
        sauce_client.jobs.update_job(session_id, passed=status)
        output = "SauceOnDemandSessionID=%s job-name=%s" % (session_id, job_name)
        log_to_file(output)
