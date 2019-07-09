import os
import os.path as op
import time
from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from .server_tools import reset_database

# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# basedir = op.abspath(op.join(op.dirname(__file__), op.pardir, op.pardir))
# PROJECT_ROOT = op.abspath(op.join(basedir, os.pardir))
# BROWSER_FIREFOX_EXE = op.join(basedir, 'bin/firefox/firefox-66.0.2/firefox')
# BROWSER_FIREFOX_DRIVER = op.join(basedir, 'bin/driver/geckodriver-v0.23.0/geckodriver')
# BROWSER_HEADLESS = False
#
# firefox_binary = FirefoxBinary(BROWSER_FIREFOX_EXE)
#
# profile = webdriver.FirefoxProfile()
# # profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
# profile.set_preference("app.update.auto", False)
# profile.set_preference("app.update.enabled", False)
# # profile.set_preference("permissions.default.image", 2)
# profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#
# profile.update_preferences()
#
# options = FirefoxOptions()
# options.set_preference("dom.webnotifications.enabled", False)
#
# if BROWSER_HEADLESS:
#     options.add_argument('-headless')
# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

options = Options()
options.headless = True

MAX_WAIT = 10
SCREEN_DUMP_LOCATION = op.join(op.dirname(op.abspath(__file__)), 'screendumps')


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(options=options)
        self.staging_server = os.environ.get('STAGING_SERVER')
        if self.staging_server:
            self.live_server_url = 'http://' + self.staging_server
            reset_database(self.staging_server)

    def tearDown(self):
        if self._test_has_failed():
            if not op.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to.window(handle)
                self.take_screenshot()
                self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # slightly obscure but could not find a better way
        return any(error for (method, error) in self._outcome.errors)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return f'{SCREEN_DUMP_LOCATION}/{self.__class__.__name__}.{self._testMethodName}-window{self._windowid}-{timestamp}'

    @wait
    def wait_for(self, fn):
        return fn()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def add_list_item(self, item_text):
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')
