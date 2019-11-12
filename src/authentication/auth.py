from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time


def obtain_required_cookies():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get('https://hackforums.net/member.php?action=login')

    time.sleep(7)    # wait for the possible identity check to finish

    usernameElem = browser.find_element_by_name('username')
    usernameElem.send_keys('Napoleon')

    passwordElem = browser.find_element_by_name('password')
    passwordElem.send_keys('LillyTheDog1!')
    passwordElem.send_keys(Keys.RETURN)

    time.sleep(3)    # have to wait for the login cookies to be transferred

    cookies = __extract_login_cookies(browser.get_cookies())
    browser.close()

    return cookies


def __extract_login_cookies(cookies_list):
    cookie_string = ''

    for cookie in cookies_list:
        cookie_string += cookie['name']
        cookie_string += '='
        cookie_string += cookie['value']
        cookie_string += '; '

    return cookie_string[:-2]    # remove the final '; '


if __name__ == '__main__':
    print('testing')
    cookies = obtain_required_cookies()
    print(cookies)