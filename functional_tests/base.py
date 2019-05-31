import os
import os.path as op
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions

basedir = op.abspath(op.join(op.dirname(__file__), op.pardir, op.pardir))
PROJECT_ROOT = op.abspath(op.join(basedir, os.pardir))

BROWSER_FIREFOX_EXE = op.join(basedir, 'bin/firefox/firefox-66.0.2/firefox')
BROWSER_FIREFOX_DRIVER = op.join(basedir, 'bin/driver/geckodriver-v0.23.0/geckodriver')
BROWSER_HEADLESS = False

firefox_binary = FirefoxBinary(BROWSER_FIREFOX_EXE)

profile = webdriver.FirefoxProfile()
# profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
profile.set_preference("app.update.auto", False)
profile.set_preference("app.update.enabled", False)
# profile.set_preference("permissions.default.image", 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

profile.update_preferences()

options = FirefoxOptions()
options.set_preference("dom.webnotifications.enabled", False)

if BROWSER_HEADLESS:
    options.add_argument('-headless')

# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(
            executable_path=BROWSER_FIREFOX_DRIVER,
            firefox_binary=firefox_binary,
            firefox_options=options,
            # firefox_profile=profile,
            # capabilities=cap,
            log_path=op.join(basedir, 'geckodriver.log'))
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)