# Import standard python library package
import subprocess
from urllib import request

# Import additional packages
import pandas as pd
from pypdf import PdfReader, PdfWriter

# Open and read Excel file with bibliographic metadata of articles in magazines
df = pd.read_excel("./data_in/articles_Gerontologie_zhaw_2023.xlsx")

# Add two new columns for notes about translation of articles
df["notiz_fr"] = (
    "Artikel erschien auf Französisch unter \"" 
    + df["fr. Titel"] 
    + "\""
    )
df["notiz_de"] = (
    "Artikel erschien auf Deutsch unter \"" 
    + df["dt. Titel"] 
    + "\""
    )

# Rename columns
df = df.rename(columns={
    "Hochschule (dt. Version)": "affiliation published", 
    "Autoren sortiert 2": "dc.contributor.author", 
    "Band": "volume",
    "Heft": "issue",
    "Seitenzahl (Beginn)": "pages.start",
    "Seitenzahl (Ende)": "pages.end",
    "dt. URL des Hefts": "dc.identifier.uri",
    })

# delete columns not needed anymore
df = df.drop(columns=[
    "QID", 
    "QID value"
    ])

# Add additional columns with predefined values
df.insert(8, "dc.date.issued", df["volume"])
df.insert(11, "dc.publisher", "Gerontologie CH")
df.insert(11, "dc.identifier.issn", "2673-4958")
df.insert(14, "publication.status", "publishedVersion")
df.insert(16, "dc.subject", None)
df.insert(18, "dc.rights", "licence according to publisher")
df.insert(19, "dcterms.type", "text")

df_german = df.copy()
df_french = df.copy()

# Delete columns with information regarding French articles
df_german = df_german.drop(columns=[
    "fr. Titel", 
    "notiz_de", 
    "fr. Zusammenfassung"
    ])

# Rename columns
df_german = df_german.rename(columns={
    "dt. Titel": "dc.title",
    "dt. Zusammenfassung": "dc.description.abstract",
    "notiz_fr": "note"
    })

# Add columns with predefinded German values
df_german.insert(
    9, "dc.relation.ispartof", "GERONTOLOGIE CH. Praxis + Forschung"
    )
df_german.insert(14, "dc.language.iso", "de")

# Delete columns with information regarding German articles 
df_french = df_french.drop(columns=[
    "dt. Titel", 
    "notiz_fr", 
    "dt. Zusammenfassung"
    ])

# Rename columns
df_french = df_french.rename(columns={ 
    "fr. Titel": "dc.title",
    "fr. Zusammenfassung": "dc.description.abstract",
    "notiz_de": "note"
    })

# Add columns with predefined values in French
df_french.insert(
    9, "dc.relation.ispartof", "GERONTOLOGIE CH. Pratique + Recherche"
    )
df_french.insert(14, "dc.language.iso", "fr")

# Change URL values from URL of German issue to French issue
df_french["dc.identifier.uri"].replace(regex="_dt", value="_fr", inplace=True)

# Combine German and French dataframe
df_combined = pd.concat([df_german, df_french])
df_combined.reset_index(drop=True, inplace=True)

# Add column for file name of PDF for each article
df_combined["file.name"] = (
    df_combined["dc.contributor.author"].str.split(",").str[0] 
    + "_" 
    + df_combined["dc.title"].str[:20]
        # Special characters in title will be deleted to avoid illegal characters in file names
        .str.replace("[\\/:\"*?<>|]", '', regex=True).str.rstrip() 
    + "_" 
    + df_combined["dc.date.issued"].astype(str) 
    + ".pdf"
    )

num_files_saved = 0 # counter for number of saved articles (PDF)

# Download all PDF files of issues mentioned in CSV once
unique_url = df_combined["dc.identifier.uri"].unique()
for i in range(len(unique_url)):
    file_issue = f"./data_in/issue_{i}.pdf"
    request.urlretrieve(unique_url[i], file_issue)

    # Filter dataframe per each unique url/issue
    df_pdf = (
        df_combined
        .loc[df_combined["dc.identifier.uri"] == unique_url[i]]
        .copy()
        )
    df_pdf.reset_index(drop=True, inplace=True)
    
    # Calculate page range of articles in downloaded PDF
    df_pdf["pages.start"] = df_pdf["pages.start"].apply(
        lambda x: (x/2) if x%2==0 else ((x-1)/2)
        )
    df_pdf["pages.end"] = df_pdf["pages.end"].apply(
        lambda x: (x/2) if x%2==0 else ((x-1)/2)
        )
    
    # Split PDF of issue into single files for each article (one PDF per row)
    with open(file_issue, "rb") as file:
        reader = PdfReader(file)
        for row in range(len(df_pdf.index)):
            output_file = ("./data_out/full-text/" + df_pdf.at[row, "file.name"])
            start_page = df_pdf.at[row, "pages.start"].astype(int) 
            end_page = df_pdf.at[row, "pages.end"].astype(int) 
            author = df_pdf.at[row, "Autoren"]
            writer = PdfWriter()
            
            try:
                for page in range(start_page, end_page + 1):
                    writer.add_page(reader.pages[page])
                    #Save file of article with correct page range
                    with open(output_file, "wb") as out:
                        #Add the metadata
                        writer.add_metadata({
                            "/Author": author,
                            "/Title": df_pdf.at[row, "dc.title"],
                            "/Subject": df_pdf.at[row, "dc.description.abstract"],
                            }) 
                        writer.write(out)
            
                num_files_saved += 1

            except Exception as error:
                print("An error occurred while writing", df_pdf.at[row, "file.name"], 
                  "\nreason: ", error)
            
# Compare length of dataframe to numbers of saved articles
if num_files_saved == len(df_combined):
    print("!!!Success!!!:"  
          "\nNumber of rows in csv is number of saved articles.")
else: 
    print("!!!Error!!!:" 
          "\nNumber of rows in csv is NOT number of saved articles.") 

print("Total number of rows:", len(df_combined),
      "\nTotal number of articles:", num_files_saved)

# delete column not needed for export
df_combined = df_combined.drop(columns="Autoren")

# Reorder columns
df_combined = df_combined[[
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
df_combined.to_csv(
    "./data_out/metadata/list_Gerontologie.csv", 
    sep=",", encoding="utf-8", index=False
    )

# Save changes to Excel file for combined article list
df_combined.to_excel(
    "./data_out/metadata/list_Gerontologie.xlsx", 
    index=False
    )

# Open Adobe Acrobat Pro to make adjustments to PDFs of articles via batch
subprocess.Popen("C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe")
