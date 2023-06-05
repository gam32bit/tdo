#pdfplumber
import pdfplumber

pdf = pdfplumber.open("tdostats.pdf")

def get_tables(doc):
    tables = []
    for page in doc.pages:
        if len(page.find_tables()) > 0:
            tables.append(page.extract_tables)
    print(tables)

get_tables(pdf)

