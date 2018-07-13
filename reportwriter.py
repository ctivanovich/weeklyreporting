def write_results(results):
    '''Takes dictionary and writes output to xlsx, with keys as s'''
    from openpyxl import Workbook
    book = Workbook(write_only=True)
    sheet = book.create_sheet(title='Weekly Report')
    for k, v in results.items():
        # v.insert(0, k)
        sheet.append(v)
    book.save('results.xlsx')
