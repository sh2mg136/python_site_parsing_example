import xlsxwriter


def write_xslx(parameter, filename):
    book = xlsxwriter.Workbook(filename)
    page = book.add_worksheet("shop items")

    row = 0
    col = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 10)
    page.set_column("C:C", 50)
    page.set_column("D:D", 50)

    for item in parameter:
        page.write(row, col, item[0])
        page.write(row, col+1, item[1])
        page.write(row, col+2, item[2])
        page.write(row, col+3, item[3])
        row += 1

    book.close()


def write_quotes_to_excel(parameter, filename):
    book = xlsxwriter.Workbook(filename)
    page = book.add_worksheet("quotes")

    row = 0
    col = 0

    page.set_column("A:A", 25)
    page.set_column("B:B", 200)

    page.write(row, col, "Author")
    page.write(row, col + 1, "Quote")

    row += 1

    for item in parameter:
        page.write(row, col, item[0])
        page.write(row, col+1, item[1])
        row += 1

    book.close()

