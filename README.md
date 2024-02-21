**Article metadata processing for professional journals**

**Project Description**
The [GOAL project](link:%20https://www.zhaw.ch/de/forschung/forschungsdatenbank/projektdetail/projektid/5535/) aims to develop case scenarios for adding full texts to repositories. The goal is to minimize manual workload for libraries and publishers while ensuring efficient workflows.
In the context of the GOAL project, we focus on semi-automated workflows for bibliographic metadata related to the [journal "Krankenpflege"](https://sbk-asi.ch/de/mitglieder/gemeinsam-stark/fachzeitschrift/), published by the Schweizer Berufsverband der Pflegefachfrauen und Pflegefachmänner SBK – ASI. We focus also on semi-automated workflows for bibliographic metadata and PDF files of articles related to the [journal "GERONTOLOGIE CH. Praxis + Forschung"](https://www.gerontologie.ch/wissen/magazin).
These enriched bibliographic metadata facilitate the inclusion of all possible full texts into the repositories of project partners and beyond.


**Enriching article metadata for the journal "Krankenpflege"**

Python script enhances exported and preprocessed bibliographic metadata of "Krankenpflege" articles in the CINAHL ultimate database by filling in missing data elements. This data was preprocessed with OpenRefine by the GOAL project (e.g. normalized affiliation data) before.
Additionally, the script aligns the table and columns with the standards defined by the GOAL project for data provision in CSV and Excel files. The resulting dataset contains bibliographic information for articles published by members of Swiss higher education institutions (HEIs) in the journal "Krankenpflege".

The input CSV contains the following columns:
- Affiliation normalized
- rec - header - controlInfo - aug - affil
- rec - header - controlInfo - aug - au
- rec - header - controlInfo - artinfo - tig - atl
- rec - header - controlInfo - pubinfo – iid
- rec - header - controlInfo - pubinfo - dt
- rec - header - controlInfo - pubinfo – dt
- rec - header - controlInfo - jinfo – jtl
- rec - header - controlInfo - artinfo – ppf
- pages.end
- rec - header - controlInfo - jinfo – issn
- rec - header - controlInfo – language
- rec - header - controlInfo - language
- rec - header - controlInfo - artinfo - sug - subj - subj
- rec - header - controlInfo - artinfo – ab
- rec - header - displayInfo - pLink - url

The following columns, along with their respective values, were added with the help of the Python script:
- dc.date.issued
- dc.publisher
- dc.identifier.uri
- publication.status
- dc.rights
- dcterms.type
- file.name

To populate the necessary values for dc.identifier.uri (link to the full text on the publisher's website), web scraping was employed. The script searches the PDF archive of the journal using the article title as a search phrase. It then extracts the link from the first search result provided by the PDF archive and adds it to the CSV/Excel file.


**Enriching article metadata and creating articles (PDF) for the journal "GERONTOLOGIE CH. Praxis + Forschung"**

The Python script enhances bibliographic metadata received from the publisher. The publisher has provided an Excel file with all articles published by Swiss university members from 2020 till 2023 (issue 1 and 2). This Excel was further preprocessed and saved as CSV with OpenRefine by the GOAL project (e.g. normalized affiliation data). Based on this file the Python script adds missing bibliographic data and uses this data to split full texts of issues (PDF) into single articles. Additionally, it aligns the table and columns received with the standards defined by the GOAL project for data provision in CSV and Excel files. The resulting dataset contains bibliographic information and full texts in PDF format for articles published by members of Swiss higher education institutions (HEIs) in the journal, that could be self-archived in repositories of the respective university.

The preprocessed CSV contains the following columns:
- affiliation normalized
- Hochschule (dt. Version)
- QID
- QID value
- Autoren
- Autoren sortiert 2
- Titel
- Titel
- Heft
- Band
- Seitenzahl (Beginn)
- Seitenzahl (Ende)
- URL des Hefts
- Zusammenfassung
- fr. Zusammenfassung

The following columns, along with their respective values, were added with the help of the Python script:
- dc.date.issued
- dc.publisher"
- dc.identifier.issn
- publication.status
- dc.subject
- dc.rights
- dcterms.type
- note
- dc.relation.ispartof
- dc.identifier.uri
- language.iso
- name


**How to Install and Run the Projects**

_Before running the scripts, follow these steps:_

- Check your file: Ensure that the file you want to process contains all the column names mentioned earlier, or adjust the script accordingly.
- Adjust file paths: Modify all file pathsif necessary. Both script contains relative file paths to the subfolders data\_in and data\_out (or data\_out/metadata and data\_out/full-text) for storing input files or output files.
- Insert your cookies and headers, before you run the Python Script for Krankenpflege: Fill in the cookies and headers with your personal browser data after logging in with your username and password (see below).

Because the webscraping for Krankenpflege was only done once instead of incorporating authentication directly into the script, we used the following approach:

1. Manual Authentication:

  - Manually log in to the website using your web browser. This ensures that you have an authenticated session.
  - While logged in, navigate to the page you want to scrape.

2. Capture Authenticated Request:

  - Open the browser's developer tools (usually by pressing F12 or right-clicking and selecting "Inspect").
  - Go to the "Network" tab.
  - Perform an action (such as loading the page) that triggers the request you want to capture.
  - Look for the relevant request in the network activity list. It will likely be an HTTP request (GET or POST) with the necessary data.
  - Right-click on the request and choose "Copy as cURL" (or similar, depending on your browser).

3. Convert cURL Command:

  -  Paste the copied cURL command into a tool like curlconverter.com.
  -  The tool will convert the cURL command into Python code, including the necessary headers and cookies.

4. Use Headers and Cookies:

- Extract the headers and cookies from the converted Python code.
- Use these headers and cookies in the script for subsequent requests.
- File names can be renamed in config.ini, parameter for webscraping can also be adjusted in config.ini

_Prerequisites_

- Python 3.11.7

additional packages

- requests (version 2.31.0)
- beautifulsoup4 (version 4.12.3)
- pandas (version 2.1.3)
- pypdf (version 3.17.1)

**Contributing**
Feel free to contribute by opening pull requests or reporting issues.
