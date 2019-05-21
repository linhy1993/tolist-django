from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import os.path as op

basedir = op.abspath(op.join(op.dirname(__file__), op.pardir))
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

import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(
            executable_path=BROWSER_FIREFOX_DRIVER,
            firefox_binary=firefox_binary,
            firefox_options=options,
            # firefox_profile=profile,
            # capabilities=cap,
            log_path=op.join(basedir, 'geckodriver.log'))

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a coll new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title  and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        # She is invited to enter a to-do item straight away
        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        # The page updates again, and now shows both items on her list# Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
