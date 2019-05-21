from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import os.path as op

basedir = op.abspath(op.dirname(__file__))
PROJECT_ROOT = op.abspath(op.join(basedir, os.pardir))

BROWSER_FIREFOX_EXE =  op.join(basedir, 'bin/firefox/firefox-66.0.2/firefox')
BROWSER_FIREFOX_DRIVER = op.join(basedir, 'bin/driver/geckodriver-v0.23.0/geckodriver')
BROWSER_HEADLESS = False


firefox_binary = FirefoxBinary(BROWSER_FIREFOX_EXE)

profile = webdriver.FirefoxProfile()
# profile.DEFAULT_PREFERENCES['frozen']['javascript.enabled'] = False
profile.set_preference("app.update.auto", False)
profile.set_preference("app.update.enabled", False)
#profile.set_preference("permissions.default.image", 2)
profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

profile.update_preferences()

options = FirefoxOptions()
options.set_preference("dom.webnotifications.enabled", False)

if BROWSER_HEADLESS:
    options.add_argument('-headless')

#cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False

browser = webdriver.Firefox(
    executable_path=BROWSER_FIREFOX_DRIVER,
    firefox_binary=firefox_binary,
    firefox_options=options,
    # firefox_profile=profile,
    # capabilities=cap,
    log_path=op.join(basedir, 'geckodriver.log')
)

browser.get('http://localhost:8000')

assert 'Django' in browser.title

browser.close()
