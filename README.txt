Krankenpflege article metadata and processor


Project Description
The GOAL project (link: https://www.zhaw.ch/de/forschung/forschungsdatenbank/projektdetail/projektid/5535/) aims to develop case scenarios for adding full texts to repositories. The goal is to minimize manual workload for libraries and publishers while ensuring efficient workflows. 
In the context of the GOAL project, we focus on semi-automated workflows for bibliographic metadata related to the journal “Krankenpflege”, published by the Schweizer Berufsverband der Pflegefachfrauen und Pflegefachmänner SBK – ASI.
This Python script enhances exported and preprocessed bibliographic metadata of "Krankenpflege" articles in the CINAHL database by filling in missing data elements. Additionally, it aligns the table and columns with the standards defined by the GOAL project for data provision in CSV and Excel files. The resulting dataset contains bibliographic information for articles published by members of Swiss higher education institutions (HEIs) in the journal “Krankenpflege”.

The Excel contains the following columns:
Affiliation normalized
rec - header - controlInfo - aug - affil
rec - header - controlInfo - aug - au
rec - header - controlInfo - artinfo - tig - atl
rec - header - controlInfo - pubinfo – iid
rec - header - controlInfo - pubinfo - dt
rec - header - controlInfo - pubinfo – dt
rec - header - controlInfo - jinfo – jtl
rec - header - controlInfo - artinfo – ppf
pages.end
rec - header - controlInfo - jinfo – issn
rec - header - controlInfo – language
rec - header - controlInfo - language
rec - header - controlInfo - artinfo - sug - subj - subj
rec - header - controlInfo - artinfo – ab
rec - header - displayInfo - pLink - url

The following columns, along with their respective values, were added with the help of the Python script:
* dc.date.issued
* dc.publisher
* dc.identifier.uri
* publication.status
* dc.rights
* dcterms.type
* file.name

To populate the necessary values for dc.identifier.uri (link to the full text on the publisher’s website), web scraping was employed. The script searches the PDF archive of the journal using the article title as a search phrase. It then extracts the link from the first search result provided by the PDF archive and adds it to the CSV/Excel file.

These enriched bibliographic metadata facilitate the inclusion of all possible full texts into the repositories of project partners and beyond.


How to Install and Run the Project

Prerequisites
* Python 3.x
additional packages
* requests (version 2.31.0)
* beautifulsoup4 (version 4.12.3)
* pandas (version 2.1.3)


This Python script is designed to extract PDF links from the SBK-ASI website. Before running the script, follow these steps:
* Check your file: Ensure that the file you want to process contains all the column names mentioned earlier, or adjust the script accordingly (lines 23 to 35 and 58 to 63).
* Adjust file paths: Modify all file paths in lines 20 and 125 to 129 according to your requirements.
* Insert Cookies and Headers: Fill in the cookies and headers with your personal browser data after logging in with your username and password (see below).

How to Use the Project

```python
# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set your cookies and headers
cookies = "your cookies here"
headers = "your headers here"

# Read the preprocessed CSV file with bibliographic metadata
df = pd.read_csv("./data_in/2024-01-10_Krankenpflege_zhaw_1.csv", sep=";", encoding="utf-8", header=0)

# Rename columns
df = df.rename(columns={
    "Affiliation normalized": "affiliation normalized",
    # ... Rename other columns ...
})

# Add additional columns with predefined values
df.insert(6, "dc.date.issued", df["volume"])
df.insert(11, "dc.publisher", "Schweizer Berufsverband der Pflegefachfrauen und Pflegefachmänner")

When building a web scraping script, implementing authentication can sometimes introduce unnecessary overhead, especially if the content needs to be scraped only once. Instead of incorporating authentication directly into the script, consider the following approach:
1. Manual Authentication:
o Manually log in to the website using your web browser. This ensures that you have an authenticated session.
o While logged in, navigate to the page you want to scrape.
2. Capture Authenticated Request:
o Open the browser’s developer tools (usually by pressing F12 or right-clicking and selecting “Inspect”).
o Go to the “Network” tab.
o Perform an action (such as loading the page) that triggers the request you want to capture.
o Look for the relevant request in the network activity list. It will likely be an HTTP request (GET or POST) with the necessary data.
o Right-click on the request and choose “Copy as cURL” (or similar, depending on your browser).
3. Convert cURL Command:
o Paste the copied cURL command into a tool like curlconverter.com.
o The tool will convert the cURL command into Python code, including the necessary headers and cookies.
4. Use Headers and Cookies:
o Extract the headers and cookies from the converted Python code.
o Use these headers and cookies in the script for subsequent requests.


Contributing
Feel free to contribute by opening pull requests or reporting issues.
