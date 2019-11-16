def generate_comments_from_html_text(text):
    bs = BeautifulSoup(text, 'html.parser')

    names = []
    author_field = bs.find_all('div',{"class" : "author_information"})
    for author in author_field:
        names.append(author.strong.span.get_text())
    comments_text = []
    comments = bs.find_all('div', {"class" : "post_body scaleimages"})
    for comment in comments:
        comments_text.append(comment.get_text())
    return(names, comments)
