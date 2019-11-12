from authentication.auth import obtain_cookies_and_threads

search_term = 'fortnite'

if __name__ == '__main__':
    cookie_string = obtain_cookies_and_threads(search_term)

    # TODO Search the forums for the crimeware

    # TODO Collect the threads meeting our criteria

    # TODO Begin scraping each thread for the information

    # TODO Analyze the comments for sentiment

    # TODO Write the data to an Excel file
