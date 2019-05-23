import os
import os.path as op
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a coll new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title  and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # The page updates again, and now shows both items on her list
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        self.fail('Finish the test')

        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep


if __name__ == '__main__':
    unittest.main(warnings='ignore')
