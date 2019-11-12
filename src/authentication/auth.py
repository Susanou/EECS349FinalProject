from selenium import webdriver
import time


def obtain_required_cookies(login_url):
    browser = webdriver.Firefox()
    browser.get(login_url)

    time.sleep(6)    # wait for the possible identity check to finish

    usernameElem = browser.find_element_by_name('username')
    usernameElem.send_keys('Napoleon')

    passwordElem = browser.find_element_by_name('password')
    passwordElem.send_keys('LillyTheDog1!')

    buttonElemn = browser.find_element_by_name('submit')
    buttonElemn.submit()
    

    return browser.manage().getCookies()


if __name__ == '__main__':
    cookies = obtain_required_cookies('https://hackforums.net/member.php?action=login')
    print(cookies)