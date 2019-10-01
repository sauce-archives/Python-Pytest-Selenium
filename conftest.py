import pytest
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

import urllib3
urllib3.disable_warnings()


@pytest.yield_fixture(scope='function')
def driver(request):
    caps = {
        'browserName':      'chrome',
        'platformName':     'Android',
        'platformVersion':  '9',
        'deviceOrientation':'portrait',
        'phoneOnly': False,
        'tabletOnly': False,
        'privateDevicesOnly': False 
    }

    rdc_key = os.environ['TESTOBJECT_KEY']
    rdc_user = os.environ['TESTOBJECT_USERNAME']
    caps['testobject_api_key'] = rdc_key
    test_name = request.node.name
    caps['name'] = test_name

    sauce_url = "https://appium.testobject.com/wd/hub"

    executor = RemoteConnection(sauce_url, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=caps, 
    )

    yield browser
    
    # Teardown starts here
    browser.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

