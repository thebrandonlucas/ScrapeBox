import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import time
import re
def single_scrape(page, tag):
    # sleep to stop get request refusal
    time.sleep(2)
    webpage = requests.get(page)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    totalData = ""
    if 'All' not in tag:
        data = soup.find_all(re.search("<(.*)>", tag).group(1));
        for line in data:
            totalData += line.get_text();
        data = totalData
    else:
        data = soup.get_text()

    print(data)
    # remove https:// and replace / with _ so it can write file
    if "https" not in page:
        outputName = page.split("http://", 1)[1].replace('/', '_').strip() + '.scrape'
    else:
        outputName = page.split("https://", 1)[1].replace('/', '_').strip() + '.scrape'

    file = open(outputName, "w")
    file.write(data)
    file.close()
    # sleep to stop get request refusal
    return data
