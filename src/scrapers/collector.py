from bs4 import BeautifulSoup
import re
import requests

BASE_URL = 'www.hackforums.net/showthread.php?tid='
PAGE_PARAM = '&page='


def request_thread_comments(cookie, thread_id):
    headers = {"Cookie" : cookie}
    thread_url = BASE_URL + thread_id
    response = requests.get(thread_url, headers=headers)

    if response.status_code != 200:
        raise Exception('Invalid response status')
    else:
        comments_pages = []
        page_soup = BeautifulSoup(response.text, 'html.parser')
        comments_pages.append(page_soup)

        next_page_count = 2
        while page_soup.find('a', {"class" : "pagination_next"}) is not None:
            next_page = thread_url + PAGE_PARAM + str(next_page_count)
            
            response = requests.get(next_page, headers=headers)
            if response.status_code == 200:
                page_soup = BeautifulSoup(response.text, 'html.parser')
                comments_pages.append(page_soup)
            next_page_count += 1

        return comments_pages


def generate_comments_from_html_text(soup):
    names = []
    author_field = soup.find_all('div',{"class" : "author_information"})
    for author in author_field:
        names.append(author.strong.span.get_text())
    comments_text = []
    comments = soup.find_all('div', {"class" : "post_body scaleimages"})
    for comment in comments:
        comments_text.append(comment.get_text())
    post_numbers = []
    floor_numbers = soup.find_all('a', {"class" : re.compile('post_url_*')})
    for number in floor_numbers:
        post_numbers.append(number.get_text())

    return(names, comments, post_numbers)
