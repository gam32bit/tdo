#pdfplumber
import pdfplumber
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


pdf = pdfplumber.open("tdostats.pdf")

totals_columns = ["Year", "ECOs", "Crisis_evals", "TDOs", "Per_Total_Evals", "Total_Events",
                  "Per_Total_TDOs", "Total_LOC_Events", "LOC_w_ECO", "LOC_n_ECO",
                  "TDO_Executed", "Engaged_OP", "Never_engaged", "Med_Treat_Events",
                  "Other_events"]

def get_totals(doc):
    totals_rows = []
    year_counter = 2015
    select_pages = [1, 2, 3, 4, 5, 7, 10, 13]
    doc_pages = list(doc.pages[i] for i in select_pages)
    for page in doc_pages:
        last_row = page.extract_table()[-1]
        last_row[0] = year_counter
        if year_counter < 2017:
            last_row.insert(1, float("NaN"))
        year_counter += 1
        totals_rows.append(last_row)
    return totals_rows

def create_totals_table(rows, cols):
    df = pd.DataFrame(get_totals(pdf), columns=totals_columns)
    for column in ["ECOs", "Crisis_evals", "TDOs"]:
        df[column] = df[column].str.replace(",", "")
    for column in ["Per_Total_Evals", "Per_Total_TDOs"]:
        df[column] = df[column].str.replace("%", "")
    df = df.apply(pd.to_numeric)
    return df
        
tdos_df = create_totals_table(get_totals(pdf), totals_columns)

x = list(tdos_df["Year"])
y = list(tdos_df["ECOs"])
z = list(tdos_df["Total_LOC_Events"])

plt.plot(x, y)
plt.show()



