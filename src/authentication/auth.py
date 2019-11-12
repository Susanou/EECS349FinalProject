from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.firefox.options import Options
import time


def obtain_required_cookies(login_url):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(login_url)

    time.sleep(7)    # wait for the possible identity check to finish

    usernameElem = browser.find_element_by_name('username')
    usernameElem.send_keys('Napoleon')

    passwordElem = browser.find_element_by_name('password')
    passwordElem.send_keys('LillyTheDog1!')

    try:
        passwordElem.submit()
    except JavascriptException:
        # Ideally, we would find the login button. However, Selenium finds a different button with the same name and tries to invoke it. Which fails.
        # We just opt to use submit, which is not a registered method for the button. But who cares it works.
        print('Submitted')

    cookies = __extract_login_cookies(browser.get_cookies())
    browser.close()

    return cookies


def __extract_login_cookies(cookies_list):
    cookie_string = ''

    for cookie in cookies_list:
        cookie_string += cookie['name']
        cookie_string += cookie['value']
        cookie_string += '; '

    return cookie_string[:-2]    # remove the final '; '


if __name__ == '__main__':
    print('testing')
    cookies = obtain_required_cookies('https://hackforums.net/member.php?action=login')
    print(cookies)