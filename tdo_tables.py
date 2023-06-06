#pdfplumber
import pdfplumber
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


pdf = pdfplumber.open("tdostats.pdf")

totals_columns = ["TDOs", "Total_Events"]

def get_totals(doc):
    totals_rows = []
    p_counter = 0
    select_pages = [1, 2, 3, 4, 5, 7, 10, 13]
    doc_pages = list(doc.pages[i] for i in select_pages)
    for page in doc_pages:
        table = page.extract_table()[-13:-2]
        if p_counter < 2:
            for row in table:
                totals_rows.append([row[2], row[4]])
        else:
            for row in table:
                totals_rows.append([row[3], row[5]])
        p_counter +=1
    return totals_rows

def create_totals_table(rows, cols):
    df = pd.DataFrame(get_totals(pdf), columns=totals_columns)
    for column in ["TDOs"]:
        df[column] = df[column].str.replace(",", "")
    df = df.apply(pd.to_numeric)
    return df
        
tdos_df = create_totals_table(get_totals(pdf), totals_columns)

x = list(tdos_df["Total_Events"])

plt.plot(x)
plt.show()



