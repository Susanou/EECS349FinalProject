from authentication.auth import obtain_cookies_and_threads

search_term = 'fortnite'

if __name__ == '__main__':

    # this might take some time
    scrape_results = obtain_cookies_and_threads(search_term)
    cookie = scrape_results[0]
    thread_ids = scrape_results[1]

    # TODO Begin scraping each thread for the information
    for thread in thread_ids:
        print('scraping')


    # TODO Analyze the comments for sentiment

    # TODO Write the data to an Excel file
