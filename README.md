<H2>Howdy all!</H2>

I recently published a [story](https://www.virginiamercury.com/2023/06/26/more-patients-in-crisis-falling-through-cracks-of-state-psychiatric-commitment-system/) that was based on some data analysis I did of a [report](https://www.documentcloud.org/documents/23861481-draft-dbhds-es-activity-and-tdo-exception-report-summary-mar-2023-cz) I obtained from the Department of Behavioral Health and Developmental Services in VA. I wanted to share a quick walkthrough of how I extracted the data from tables in a PDF using a Python module called [PDFplumber](https://github.com/jsvine/pdfplumber). I also uploaded a video to Youtube if you prefer that.

By using PDFplumber, I was able to create a graph which shows the trend at the center of my article. I hope some of you can take something away from this walkthrough that will help you supplement your own reporting, especially if you're interested in data journalism.

![graph](https://www.virginiamercury.com/wp-content/uploads/2023/06/lossofcustodyfinalfinal.jpg)

In order to use PDFplumber, you need a Python IDE installed. A lot of data analysts will use [Jupyter Notebooks](https://jupyter.org/install), but I use [VS code](https://code.visualstudio.com/download). If you don't know any Python, it's not too hard, and I'd recommend the [Socratica](https://www.youtube.com/@Socratica) videos on youtube.

You can use [pip](https://pip.pypa.io/en/stable/cli/pip_install/) to install and import PDFplumber into your script, and from there the first thing you want to do is create a variable to open the pdf:

    pdf = pdfplumber.open("tdostats.pdf")

Note that the PDF will need to be [OCR'd](https://ocrmypdf.readthedocs.io/en/latest/installation.html) for this to work. From there, you will need to use the "pages" class to make it possible to extract data in Python. For example, I created a list of pages that I wanted to extract from and then used list comprehension to create a list of PDFplumber "pages" objects:

    select_pages = [1, 2, 3, 4, 5, 7, 10, 13]
    doc_pages = list(pdf.pages[i] for i in select_pages)

From there, you can use the [extract_table](https://github.com/jsvine/pdfplumber#extracting-tables) method to take data from the table. Depending on how many tables on the page you want to extract, you may want to use the extract_tables method instead. Refer to the PDFplumber documentation for more info.

In my case, I wanted to extract the month (and year) as well as a "total events" value from the table on each page, and because the top of the tables were messy, I decided to count backwards. Because each table was one fiscal year (Jul-Dec one year and then Jan-June the following year), I split the table in two to make things easier.

    for page in doc_pages:
            table_first_half = page.extract_table()[-13:-7]
            table_second_half = page.extract_table()[-7:-1]

That's it! I wrote some additional [code](https://github.com/gam32bit/tdo/blob/master/tdo_tables.py) to pull the values from the table and clean the data before creating the final visualization. 

I'm by no means an expert coder, very much a beginner, so if there are things I could have done better let me know. That being said, I hope this walkthrough proves that any journalist can use programming to enhance their work, so you should try it if you haven't already!
