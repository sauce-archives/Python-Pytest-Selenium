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
        'appiumVersion':    '1.9.1',
        'browserName':      '',
        'platformName':     'Android',
        'platformVersion':  '8.1',
        'deviceOrientation':'portrait',
        'phoneOnly': False,
        'tabletOnly': False,
        'privateDevicesOnly': False 
    }

    rdc_key = os.environ['TESTOBJECT_SAMPLE_ANDROID']
    rdc_user = os.environ['TESTOBJECT_USERNAME']
    caps['testobject_api_key'] = rdc_key
    test_name = request.node.name
    caps['name'] = test_name

    sauce_url = "http://us1.appium.testobject.com/wd/hub"

    executor = RemoteConnection(sauce_url, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=caps, 
        keep_alive=True
    )

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if browser is not None:
        with open("%s.testlog" % browser.session_id, 'w') as f:
            f.write("SauceOnDemandSessionID=%s job-name=%s\n" % (browser.session_id, test_name))
    else:
        raise WebDriverException("Never created!")

    yield browser
    # Teardown starts here
    # report results
    # use the test result to send the pass/fail status to Sauce Labs
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    browser.execute_script("sauce:job-result={}".format(sauce_result))
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

