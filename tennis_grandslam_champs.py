import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
import requests
import re



url = "https://en.wikipedia.org/wiki/List_of_Grand_Slam_singles_champions_in_Open_Era_with_age_of_first_title"


def extract(url: str) -> BeautifulSoup:
    """
    Fetch the content in the webpage
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    print("Status-code:", r.status_code)
    return soup


def tranform(soup):
    """
    Extract the information contained in the page
    """
    
    all_rows = soup.find_all("tr")
    header = all_rows.pop(0) #header of the first table
    
    table_men = []
    table_women = []

    for container in all_rows:
        cols = container.find_all("td")  #returns list of all columns
        if cols:
            print(cols)
            total_titles = cols[5].get_text(strip=True)
            if total_titles:
                titles = int(re.search(r"of\s+(\d+)", total_titles).group(1))
            else:
                titles = 1

            entry = {
                "Age": cols[0].get_text(strip=True),
                "Name": cols[1].get_text(strip=True),
                "First_tournament": cols[2].get_text(strip=True),
                "First_title_date": cols[4].get_text(strip=True),
                "Total_titles": titles,
            }
            table_men.append(entry)
        
    df = pd.DataFrame(table_men)
    df.sort_values(by="Total_titles", ascending=False, inplace=True)

    return

def scrape_table(soup, gender:str):
    tables = soup.find_all("table", {"class": "wikitable"})
    header_list = []
    table_data = []


    for heading in soup.find_all(["h2", "h3"]):
        heading_text = heading.get_text(strip=True).lower()
        
        if gender in heading_text:
            table = heading.find_next("table", {"class": "wikitable"})
            header_row = table.find("tr")
            for th in header_row.find_all(["th", "td"]):
                header_text = th.get_text(strip=True)
                header_list.append(header_text)
            
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 0:
                    row_data = []
                    for col in cols:
                        text = col.get_text(strip=True)
                        row_data.append(text)
                    table_data.append(row_data)
                    
            print(table_data)
            break

if __name__ == "__main__":
    soup = extract(url)
    scrape_table(soup, "women")
