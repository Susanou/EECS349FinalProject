from selenium import webdriver
from selenium.common.exceptions import JavascriptException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import bs4


def obtain_cookies_and_thread_meta(keyword):
    options = Options()
    options.headless = True
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

    threads = []
    threads.append(__extract_threads_on_page(browser))
    while __next_page(browser):
        threads.append(__extract_threads_on_page(browser))

    return (cookies, threads)


def __extract_threads_on_page(browser):
    time.sleep(3)    # wait for page to load

    # 1st page
    page_soup = bs4.BeautifulSoup(browser.page_source, 'html.parser')
    current_rows = page_soup.find_all("tr", {"class" : "inline_row"})

    threads_meta = []
    for row in current_rows:
        threads_meta.append(__get_thread_meta(row))
    
    return threads_meta


def __next_page(browser):
    try:
        next_button = browser.find_element_by_class_name('pagination_next')
        next_button.click()
        return True
    except:
        return False    # next button cannot be found or clicked, means on the last page


def __get_thread_meta(row_soup):
    info = row_soup.find_next('a', href=True)
    tid = info['href'].split('&')[0].split('=')[1]
    title = info.get_text()

    author = row_soup.find_next('div', {"class" : "author smalltext"}).get_text()

    reply_count = row_soup.find_next('td', {"class" : "trow1 mobile-remove"}).get_text()
    views = row_soup.find_next('td', {"class" : "trow1 mobile-remove"}).get_text()

    return (tid, author, title, reply_count, views)

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
    cookies = obtain_cookies_and_thread_meta('fortnite')
    print(cookies)