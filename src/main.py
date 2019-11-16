from authentication.auth import obtain_cookies_and_thread_meta
from scrapers.collector import request_thread_comments, generate_comments_from_html_text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from sentiment.fitting import vote, predictedSVC, predictNaiveBayes, predictSGD, get_sentiment

search_term = 'fortnite'
forum_url = 'https://hackforums.net/showthread.php?tid='
# sentiment = get_sentiment()
# clf1 = predictedSVC()
# clf2 = predictNaiveBayes()
# clf3 = predictSGD()


def __aggregate_thread_ids(meta_info_list):
    new_list = []
    for thread in meta_info_list:
        new_list.append(thread[0])    # 0th elem is the tid
    
    # print(new_list)
    return new_list

# def analyzeComment(comment: list):
#     pred1 = clf1.predict_proba(comment)
#     pred2 = clf2.predict_proba(comment)
#     pred3 = clf3.predict_proba(comment)

#     result, totalP = vote(pred1, pred2, pred3)

#     return result, totalP


if __name__ == '__main__':

    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # this might take some time
    scrape_results = obtain_cookies_and_thread_meta(browser, search_term)
    cookie = scrape_results[0]
    thread_meta = scrape_results[1]

    thread_ids = __aggregate_thread_ids(thread_meta)
    
    # TODO Begin scraping each thread for the information
    for i, thread in enumerate(thread_ids):
        # print(thread)
        thread_url = forum_url + thread
        # meta_thread_tuple = (i, thread_url, 'Hack Forums', $VENDOR_NAME, $PRODUCT_NAME, $REPLIES, $VIEWS, 'MANUAL-ID-REQ', 'MANUAL-ID-REQ', 'MANUAL-ID-REQ') 
        
        for comment_page in request_thread_comments(cookie, thread):
            print(generate_comments_from_html_text(comment_page))
            # break
        break


    browser.close()
    # TODO Analyze the comments for sentiment

    # comment = ["Best ever"] #need to pass the comments in a list for it to classify them so far can do one comment at a time. Trying to correct for more

    # pred1 = clf1.predict_proba(comment)
    # pred2 = clf2.predict_proba(comment)
    # pred3 = clf3.predict_proba(comment)

    # result, totalP = vote(pred1, pred2, pred3)

    # print("I think you are talking about {0} with a score of {1}".format(sentiment[result], totalP))

    # TODO Write the data to an Excel file
