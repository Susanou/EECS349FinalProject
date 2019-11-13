import openpyxl

def __write_comments_data_header(sheet):
    sheet['A1'] = 'Thread_id'
    sheet['A2'] = 'Specific page of the comment'
    sheet['B1'] = 'Comment_link'
    sheet['C1'] = 'Floor_number'
    sheet['D1'] = 'User name'
    sheet['E1'] = 'Trade'
    sheet['E2'] = '[1] if the comment indicates the trade'
    sheet['F1'] = 'Review'
    sheet['F2'] = 'Sentiment of review (if the comment includes review)'
    sheet['G1'] = 'Q&A'
    sheet['G2'] = '[1] if the comment includes a Q&A'
    sheet['H1'] = 'Content'


def __write_threads_data_header(sheet):
    sheet['A1'] = 'Thread_id'
    sheet['B1'] = 'Thread_link'
    sheet['C1'] = 'Market'
    sheet['D1'] = 'Vendor name'
    sheet['E1'] = 'Product/service name'
    sheet['F1'] = 'Replies'
    sheet['G1'] = 'Views'
    sheet['H1'] = 'Category'
    sheet['H2'] = 'Crimeware or CaaS'
    sheet['I1'] = 'Price'
    sheet['K1'] = 'Payment method'
    sheet['K2'] = '1:PayPal 2:CreditCard 3:Cryptocurrency 4: Others'

def write_comments_data_points(sheet, data_tuple, row_num):
    for i, char in enumerate(__char_range('A', chr(ord('A') + len(data_tuple) - 1))):
        sheet[char + row_num] = data_tuple[i]


def __char_range(c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

if __name__ == '__main__':
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Data Analysis'
    wb.save('t1_g14_data.xlsx')