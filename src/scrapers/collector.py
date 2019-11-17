from bs4 import BeautifulSoup
import re
import requests
import time

BASE_URL = 'https://hackforums.net/showthread.php?tid='
PAGE_PARAM = '&page='


def request_thread_comments(cookie, thread_id):

    with requests.Session() as session:
        # DO NOT MODIFY HEADERS
        headers = {
            "Cookie" : cookie, 
            "User-Agent" : "PostmanRuntime/7.19.0",
            "Accept" : "*/*",
            "Cache-Control" : "no-cache",
            "Postman-Token" : "76a8bb46-a397-44ef-8033-3a62127ab6f1",
            "Host" : "hackforums.net",
            "Accept-Encoding" : "gzip, deflate",
            "Connection" : "keep-alive"
        }
        session.headers = headers
        thread_url = BASE_URL + thread_id

        response = session.get(thread_url)

        if response.status_code != 200:
            raise Exception('Invalid response status')
        else:
            comments_pages = []
            page_soup = BeautifulSoup(response.text, 'html.parser')
            comments_pages.append(page_soup)

            next_page_count = 2
            while page_soup.find('a', {"class" : "pagination_next"}) is not None:
                next_page = thread_url + PAGE_PARAM + str(next_page_count)
                
                response = session.get(next_page)
                if response.status_code == 200:
                    page_soup = BeautifulSoup(response.text, 'html.parser')
                    comments_pages.append(page_soup)
                next_page_count += 1
                time.sleep(0.25)    # Need to avoid detection

            return comments_pages


def generate_comments_from_html_text(soup):
    names = []
    author_field = soup.find_all('div',{"class" : "author_information"})
    for author in author_field:
        names.append(author.strong.span.get_text())
    comments_text = []
    comments = soup.find_all('div', {"class" : "post_body scaleimages"})
    for comment in comments:
        if comment.blockquote is None:
            comments_text.append(comment.get_text().replace('\n', '').replace('\t', '').replace('\r', ''))
        else:
            text_parts = comment.find_all(text=True, recursive=False)
            comments_text.append(str(text_parts[-1]).replace('\n', '').replace('\t', '').replace('\r', ''))

    post_numbers = []
    floor_numbers = soup.find_all('a', {"id" : re.compile(r"post_url_*")})
    for number in floor_numbers:
        post_numbers.append(number.get_text())

    return (names, comments_text, post_numbers)