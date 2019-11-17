from authentication.auth import obtain_cookies_and_thread_meta
# import data_formatter.formatter
from data_formatter.formatter import create_workbook, write_data_points
from scrapers.collector import request_thread_comments, generate_comments_from_html_text
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from sentiment.fitting import vote, predictedSVC, predictNaiveBayes, predictSGD, get_sentiment

search_term = 'fortnite'
forum_url = 'https://hackforums.net/showthread.php?tid='
sentiment = get_sentiment()
clf1 = predictedSVC()
clf2 = predictNaiveBayes()
clf3 = predictSGD()


def __aggregate_thread_ids(meta_info_list):
    new_list = []
    for thread in meta_info_list:
        new_list.append(thread[0])    # 0th elem is the tid
    
    return new_list

def analyzeComment(comment: list):
    pred1 = clf1.predict_proba(comment)
    pred2 = clf2.predict_proba(comment)
    pred3 = clf3.predict_proba(comment)

    result, totalP = vote(pred1, pred2, pred3)

    return result, totalP


if __name__ == '__main__':

    all_threads = []
    all_comments = []
    try:
        print('Commencing the scraping', end='\n\n')
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)

        # this might take some time
        scrape_results = obtain_cookies_and_thread_meta(browser, search_term)
        cookie = scrape_results[0]
        thread_meta = scrape_results[1]

        thread_ids = __aggregate_thread_ids(thread_meta)
        
        all_threads = []
        all_comments = []

        for i, thread in enumerate(thread_ids):
            thread_url = forum_url + thread
            cur_thread = thread_meta[i]
            meta_thread_tuple = (i, thread_url, 'Hack Forums', cur_thread[1], cur_thread[2], cur_thread[3], cur_thread[4], 'MANUAL-ID-REQ', 'MANUAL-ID-REQ', 'MANUAL-ID-REQ') 
            all_threads.append(meta_thread_tuple)

            for comment_page in request_thread_comments(cookie, thread):
                comments_for_page = generate_comments_from_html_text(comment_page)

                authors = comments_for_page[0]
                bodies = comments_for_page[1]
                nums = comments_for_page[2]

                for j in range(len(nums)):
                    all_comments.append((i, nums[j], authors[j], bodies[j]))
            break
    finally:
        browser.close()

    # TODO Analyze the comments for sentiment

    # comment = ["Best ever"] #need to pass the comments in a list for it to classify them so far can do one comment at a time. Trying to correct for more

    analyzed_comments = []
    for comment in all_comments:
        pred1 = clf1.predict_proba(comment)
        pred2 = clf2.predict_proba(comment)
        pred3 = clf3.predict_proba(comment)
        result, totalP = vote(pred1, pred2, pred3)

        analyzed_comments.append((comment[0]), comment[1], comment[2], pred1, pred2, pred3, comment[3])

    print(analyzed_comments)

    # print("I think you are talking about {0} with a score of {1}".format(sentiment[result], totalP))

    # TODO Write the data to an Excel file

    print('Writing to Excel document')
    title = 'Project T1_Template.xlsx'
    wb = create_workbook(title)
    sheet = wb.get_sheet_by_name('Threads')
    for q, thread in enumerate(all_threads):
        write_data_points(sheet, thread, q)
        wb.save(title)

    sheet = wb.get_sheet_by_name('Comments')
    for q, comment in enumerate(analyzed_comments):
        write_data_points(sheet, comment, q)
        wb.save(title)

    wb.close()



    # wb = openpyxl.Workbook()
    # sheet = wb.active
    # sheet.title = 'Threads'
    # __write_threads_data_header(sheet)
    


    # __write_comments_data_header(sheet)

    # write_data_points(sheet, data, 1)
    # wb.save('t1_g14_data.xlsx')
