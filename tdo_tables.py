#pdfplumber
import pdfplumber
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt



pdf = pdfplumber.open("tdostats.pdf")

loc_columns = ["Month_Year", "Total_Events"]

def get_total(doc):
    total_rows = []
    year_counter = 2014
    select_pages = [1, 2, 3, 4, 5, 7, 10, 13]
    doc_pages = list(doc.pages[i] for i in select_pages)
    for page in doc_pages:
        table_first_half = page.extract_table()[-13:-7]
        table_second_half = page.extract_table()[-7:-1]
        if year_counter < 2016:
            for row in table_first_half:
                total_rows.append([row[0] + " " + str(year_counter), row[6]])
            for row in table_second_half:
                total_rows.append([row[0] + " " + str(year_counter + 1), row[6]])
        else:
            for row in table_first_half:
                total_rows.append([row[0] + " " + str(year_counter), row[7]])
            for row in table_second_half:
                total_rows.append([row[0] + " " + str(year_counter + 1), row[7]])
        year_counter += 1
    return total_rows

def create_table(rows, cols):
    df = pd.DataFrame(rows, columns=cols)
    df["Total_Events"] = df["Total_Events"].apply(pd.to_numeric)
    df["Month_Year"] = pd.to_datetime(df["Month_Year"], format="%B %Y")
    df = df.set_index(df["Month_Year"])
    df = df.sort_index()
    return df

loc_df = create_table(get_total(pdf), loc_columns)

print(loc_df)

plt.style.use('seaborn-dark')
plt.plot(loc_df['Total_Events'])
plt.ylabel('Events Per Month', fontsize=12.0)
plt.title('Loss of Custody Events', fontsize=16.0, pad=10.0)
plt.gcf().autofmt_xdate()
plt.tight_layout(pad=2.0)
plt.show()



