"""
    This file is part of the  GOAL data preprocessing package.
    (c) ZHAW HSB <apps.hsb@zhaw.ch>

    For the full copyright and license information, please view the LICENSE
    file that was distributed with this source code.
"""


# Import standard python library package
import configparser
import requests
import re

# Import additional packages
from bs4 import BeautifulSoup
import pandas as pd


"""Prepare the script before running:
    1. Check your file you like to process if it contains all column names mentioned 
    3. The script is webscraping PDF links from the website https://sbk-asi.ch/de/pdf-archiv/ you need to be logged in.
    fill in cookies and headers with your browser data after you have logged in with your user name and password (see config.ini)
"""

# Read config.ini and get values
config = configparser.ConfigParser
config.read("../config.ini")
input_csv = config.get("Krankenpflege", "input_csv")
search_url = config.get("Krankenpflege", "search_url")
cookies_login = config.get("Krankenpflege", "cookies_login")
headers_login = config.get("Krankenpflege", "headers_login")
phrase_link = config.get("Krankenpflege", "phrase_link")
url_homepage = config.get("Krankenpflege", "url_homepage")
output_csv = config.get("Krankenpflege", "output_csv")
output_excel = config.get("Krankenpflege", "output_excel")

# Open and read preprocessed CSV file with bibliographic metadata of articles in magazines
df = pd.read_csv(f"./data_in/{input_csv}", sep=";", encoding="utf-8", header=0)

# Rename columns
df = df.rename(columns={
    "Affiliation normalized": "affiliation normalized", 
    "Affiliation published": "affiliation published", 
    "rec - header - controlInfo - artinfo - aug - au": "dc.contributor.author", 
    "rec - header - controlInfo - artinfo - tig - atl": "dc.title",
    "rec - header - controlInfo - pubinfo - iid": "issue",
    "rec - header - controlInfo - pubinfo - dt": "volume",
    "rec - header - controlInfo - jinfo - jtl": "dc.relation.ispartof",
    "rec - header - controlInfo - artinfo - ppf": "pages.start",
    "rec - header - controlInfo - jinfo - issn": "dc.identifier.issn",
    "rec - header - controlInfo - language": "dc.language.iso",
    "rec - header - controlInfo - artinfo - sug - subj": "dc.subject",
    "rec - header - controlInfo - artinfo - ab": "dc.description.abstract"
  })


# Add additional columns with predefined values 
df.insert(6, "dc.date.issued", df["volume"])
df.insert(11, "dc.publisher", 
          "Schweizer Berufsverband der Pflegefachfrauen und Pflegefachmänner SBK - ASI||"
          + "Association suisse des infirmières et infirmiers SBK-ASI||"
          + "Associazione svizzera infermiere e infermieri SBK – ASI"
          )
df.insert(12, "dc.identifier.uri", None)
df.insert(14, "publication.status", "publishedVersion")
df.insert(16, "dc.rights", "licence according to publisher")
df.insert(18, "dcterms.type", "text")
df.insert(19, "note", 
          "link to record in CINAHL complete: " 
          + df["rec - header - displayInfo - pLink - url"]
          )
df.insert(20, "file.name", "no file provided by GOAL, full-text only accessible with subscription (dc.identifier.uri)")


# delete columns not needed anymore
df = df.drop(columns=[
    "rec - header - uiTerm", 
    "rec - header - controlInfo - artinfo - aug - affil",
    "rec - header - controlInfo - artinfo - ppct",
    "rec - header - displayInfo - pLink - url",
    "rec - header - controlInfo - artinfo - doctype"
    ])

# Add new column for search and build search query for PDF archive
df["search_query"] = (f"{search_url}{df["dc.title"]}")

# iterate over every search query for matching article in PDF-archive, open url and parse html code of website for link to PDF to article of first matching result
for row in range(len(df.index)):
    URL = df.at[row, "search_query"]
    page = requests.get(URL, cookies=cookies_login, headers=headers_login)
    soup_search = BeautifulSoup(page.content, "html.parser")
    
    try: 
        link = soup_search.find('a', attrs={'href': re.compile(phrase_link)}).get('href')
        print(link)
    except Exception as error:
        print(f"An error occurred while writing link for: {df.at[row, "dc.title"]}", 
            "\nreason: ", error)
        link = None
    

    # build complete direct link to PDF and record in dataframe    
    if link == None:
       df.at[row, "dc.identifier.uri"] = link
    else: 
        link_pdf = f"{url_homepage}{link}"
        df.at[row, "dc.identifier.uri"] = link_pdf


# delete columns not needed anymore
df = df.drop(columns="search_query")

# Reorder columns
df = df[[
    "affiliation normalized",
    "affiliation published",
    "dc.contributor.author",
    "dc.title",
    "issue",
    "volume",
    "dc.date.issued",
    "dc.relation.ispartof",
    "pages.start",
    "pages.end",
    "dc.identifier.issn",
    "dc.publisher",
    "dc.identifier.uri",
    "dc.language.iso",
    "publication.status",
    "dc.subject",
    "dc.description.abstract",
    "dc.rights",
    "dcterms.type",
    "note",
    "file.name",
]]


# Save changes to CSV file for combined article list
df.to_csv(f".\data_out\{output_csv}", sep=",", encoding="utf-8", index=False)

# Save changes to Excel file for combined article list
df.to_excel(f".\data_out\{output_excel}", index=False)
