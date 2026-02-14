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
    men_div = soup.find_all("tr")
    header = men_div.pop(0) #header of the first table
    
    table_men = []
    table_women = []

    for container in men_div:
        cols = container.find_all("td")  #returns list of all columns
        if not cols:
            break
        
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


if __name__ == "__main__":
    soup = extract(url)
    tranform(soup)
