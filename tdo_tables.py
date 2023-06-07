#pdfplumber
import pdfplumber
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


pdf = pdfplumber.open("tdostats.pdf")

totals_columns = ["Month_Year", "TDOs", "Total_Events"]

def get_totals(doc):
    totals_rows = []
    year_counter = 2015
    select_pages = [1, 2, 3, 4, 5, 7, 10, 13]
    doc_pages = list(doc.pages[i] for i in select_pages)
    for page in doc_pages:
        table = page.extract_table()[-13:-2]
        if year_counter < 2017:
            for row in table:
                totals_rows.append([str(row[0]) + " " + str(year_counter), row[2], row[4]])
        else:
            for row in table:
                totals_rows.append([str(row[0]) + " " + str(year_counter), row[3], row[5]])
        year_counter +=1
    return totals_rows

def create_totals_table(rows, cols):
    df = pd.DataFrame(rows, columns=cols)
    for column in ["TDOs"]:
        df[column] = df[column].str.replace(",", "")
    df[["TDOs", "Total_Events"]] = df[["TDOs", "Total_Events"]].apply(pd.to_numeric)
    df["Month_Year"] = pd.to_datetime(df["Month_Year"], format="%B %Y")
    df = df.set_index(df["Month_Year"])
    df = df.sort_index()
    return df
        
tdos_df = create_totals_table(get_totals(pdf), totals_columns)

plt.style.use('seaborn-dark')
plt.plot(tdos_df["TDOs"])
plt.ylabel('TDOS', fontsize=12.0)
plt.title('Temporary Detention Orders in Virginia', fontsize=16.0, pad=10.0)
plt.gcf().autofmt_xdate()
plt.tight_layout(pad=2.0)
plt.show()





