import pytest
from os import environ

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection

import urllib3
urllib3.disable_warnings()

browsers = [
    {
        "platformName": "Windows 10",
        "browserName": "MicrosoftEdge",
        "platformVersion": "latest",
        "sauce:options": {"seleniumVersion": '3.141.0',}
    }, {
        "platformName": "Windows 10",
        "browserName": "firefox",
        "platformVersion": "latest",
        "sauce:options": {"seleniumVersion": '3.141.0'}
    }, {
        "platformName": "Windows 10",
        "browserName": "internet explorer",
        "plaformVersion": "latest",
        "sauce:options": {"seleniumVersion": '3.141.0'}
    }, {
        "platformName": "OS X 10.13",
        "browserName": "safari",
        "platformVersion": "latest",
        "sauce:options": {"seleniumVersion": '3.141.0'}
    }, {
        "platformName": "OS X 10.12",
        "browserName": "chrome",
        "platformVersion": "latest",
        "sauce:options": {"seleniumVersion": '3.141.0', "extendedDebugging": True}
    }]

def pytest_generate_tests(metafunc):
    if 'driver' in metafunc.fixturenames:
        metafunc.parametrize('browser_config',
                             browsers,
                             ids=_generate_param_ids('broswerConfig', browsers),
                             scope='function')


def _generate_param_ids(name, values):
    return [("<%s:%s>" % (name, value)).replace('.', '_') for value in values]


@pytest.yield_fixture(scope='function')
def driver(request, browser_config):
    # if the assignment below does not make sense to you please read up on object assignments.
    # The point is to make a copy and not mess with the original test spec.
    desired_caps = dict()
    desired_caps.update(browser_config)
    test_name = request.node.name
    build_tag = environ.get('BUILD_TAG', None)
    tunnel_id = environ.get('TUNNEL_IDENTIFIER', None)
    username = environ.get('SAUCE_USERNAME', None)
    access_key = environ.get('SAUCE_ACCESS_KEY', None)

    selenium_endpoint = "https://%s:%s@ondemand.saucelabs.com:443/wd/hub" % (username, access_key)
    desired_caps['build'] = build_tag
    # we can move this to the config load or not, also messing with this on a test to test basis is possible :)
    desired_caps['tunnelIdentifier'] = tunnel_id
    desired_caps['name'] = test_name

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps, 
        keep_alive=True
    )

    # This is specifically for SauceLabs plugin.
    # In case test fails after selenium session creation having this here will help track it down.
    # creates one file per test non ideal but xdist is awful
    if browser is not None:
        print("SauceOnDemandSessionID={} job-name={}".format(browser.session_id, test_name))
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

