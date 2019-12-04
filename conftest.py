import pytest

from simplesauce.options import SauceOptions
from simplesauce.session import SauceSession

import urllib3
urllib3.disable_warnings()

browsers = [
    'internet explorer',
    'chrome',
    'firefox',
    'safari',
    'edge'
]


@pytest.fixture(params=browsers)
def driver(request):
    opts = SauceOptions(browserName=request.param)
    sauce = SauceSession(options=opts)
    sauce.start()

    yield sauce.driver

    # report results
    # use the test result to send the pass/fail status to Sauce Labs
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    sauce.driver.execute_script("sauce:job-result={}".format(sauce_result))
    sauce.stop()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

