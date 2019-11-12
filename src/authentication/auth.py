from selenium import webdriver
from selenium.common.exceptions import JavascriptException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import bs4


def obtain_cookies_and_threads(keyword):
    options = Options()
    # options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get('https://hackforums.net/member.php?action=login')

    time.sleep(7)    # wait for the possible identity check to finish

    username_elem = browser.find_element_by_name('username')
    username_elem.send_keys('Napoleon')

    password_elem = browser.find_element_by_name('password')
    password_elem.send_keys('LillyTheDog1!')
    password_elem.send_keys(Keys.RETURN)

    time.sleep(5)    # have to wait for the login cookies to be transferred

    cookies = __extract_login_cookies(browser.get_cookies())

    browser.get('https://hackforums.net/search.php')
    # searchElem = browser.find_elements_by_name('keywords')

    num_replies_elem = browser.find_element_by_name("numreplies")
    num_replies_elem.send_keys('30')

    search_elems = browser.find_elements_by_name('keywords')
    for search_elem in search_elems:
        try:
            search_elem.send_keys(keyword)
            search_elem.send_keys(Keys.RETURN)
            break    # do not attempt to find the others
        except ElementNotInteractableException:
            continue
    
    time.sleep(2)
    # search_url = browser.current_url    # this will be used for getting more pages

    page_soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
    current_rows = page_soup.find_all("tr", {"class" : "inline_row"})

    threads = []
    for row in current_rows:
        threads.append(__get_thread_id(row))

    return (cookies, threads)


def __get_thread_id(row_soup):
    href = row_soup.find_next('a', href=True)
    thread_href = href['href'].split('&')[0]       # showthread.php?tid=5988772 , &highlight=....
    return thread_href.split('=')[1]               # showthread.php?tid= , 5988772


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
    cookies = obtain_cookies_and_threads('fortnite')
    print(cookies)