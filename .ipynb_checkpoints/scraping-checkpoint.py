#import dependencies 
import pandas as pd 
import requests 
from bs4 import BeautifulSoup

df = pd.DataFrame(columns=['title', 'date', 'person', 'link'])

year = 2019
base_url = "https://www.presidency.ucsb.edu/documents/app-categories/elections-and-transitions/campaign-documents?field_docs_start_date_time_value%5Bvalue%5D%5Bdate%5D=2019"
for i in range(0, 121):
    print(f"Processing: year {year} page {i}")
    if i == 0:
        url = base_url
    else:
        url = base_url + "&page=" + str(i)
    data = requests.get(url)
    h = BeautifulSoup(data.text,"html.parser")
    dates = [d.find("span",attrs={'class':'date-display-single'})['content'] for d in h.find_all("div",attrs={'class':'views-row'})]
    doc_links = [d.find("div",attrs={'class':'field-title'}).find("a") for d in h.find_all("div",attrs={'class':'views-row'})]
    titles = [d.string for d in doc_links]
    links = [d['href'] for d in doc_links]
    persons = [d.find("div",attrs={'class':'col-sm-4'}).find("a").string for d in h.find_all("div",attrs={'class':'views-row'})]
    temp = pd.DataFrame({"title": titles, "date": dates, "person": persons, "link": links},columns=['title', 'date', 'person', 'link'])
    df = pd.concat([df, temp])

year = 2020
base_url = "https://www.presidency.ucsb.edu/documents/app-categories/elections-and-transitions/campaign-documents?field_docs_start_date_time_value%5Bvalue%5D%5Bdate%5D=2020"
for i in range(0, 222):
    print(f"Processing: year {year} page {i}")
    if i == 0:
        url = base_url
    else:
        url = base_url + "&page=" + str(i)
    data = requests.get(url)
    h = BeautifulSoup(data.text,"html.parser")
    dates = [d.find("span",attrs={'class':'date-display-single'})['content'] for d in h.find_all("div",attrs={'class':'views-row'})]
    doc_links = [d.find("div",attrs={'class':'field-title'}).find("a") for d in h.find_all("div",attrs={'class':'views-row'})]
    titles = [d.string for d in doc_links]
    links = [d['href'] for d in doc_links]
    persons = [d.find("div",attrs={'class':'col-sm-4'}).find("a").string for d in h.find_all("div",attrs={'class':'views-row'})]
    temp = pd.DataFrame({"title": titles, "date": dates, "person": persons, "link": links},columns=['title', 'date', 'person', 'link'])
    df = pd.concat([df, temp])

df = df.reset_index(drop=True)

print('Total Number of Documents:', len(df))

home_url = 'https://www.presidency.ucsb.edu'
df['transcript'] = ''

for i in range(len(df)):
    print("Fetching Transcript:",i)
    url = home_url + df.loc[i, 'link']
    data = requests.get(url)
    h = BeautifulSoup(data.text, "html.parser")
    transcript = h.find('div', attrs={'class':'field-docs-content'}).text
    df.loc[i, 'transcript'] = transcript

print('Scraping Complete, exporting to data.csv')

df.to_csv("data.csv",index=False)

print('Finished')