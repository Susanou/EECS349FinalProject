from authentication.auth import obtain_cookies_and_thread_meta

search_term = 'fortnite'
forum_url = 'https://hackforums.net/showthread.php?tid='

def __aggregate_thread_ids(meta_info_list):
    new_list = []
    for thread in meta_info_list:
        new_list.append(thread[0])    # 0th elem is the tid
    
    return new_list


if __name__ == '__main__':

    # this might take some time
    scrape_results = obtain_cookies_and_thread_meta(search_term)
    cookie = scrape_results[0]
    thread_meta = scrape_results[1]

    thread_ids = __aggregate_thread_ids(thread_meta)
    
    # TODO Begin scraping each thread for the information
    for i, thread in enumerate(thread_ids):
        thread_url = forum_url + thread
        # meta_thread_tuple = (i, thread_url, 'Hack Forums', $VENDOR_NAME, $PRODUCT_NAME, $REPLIES, $VIEWS, 'MANUAL-ID-REQ', 'MANUAL-ID-REQ', 'MANUAL-ID-REQ') 
        
        print('scraping')


    # TODO Analyze the comments for sentiment

    # TODO Write the data to an Excel file
