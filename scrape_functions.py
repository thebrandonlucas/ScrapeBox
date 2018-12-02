import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import time
def single_scrape(page):
    # sleep to stop get request refusal
    time.sleep(2)
    webpage = requests.get(page)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    text = soup.get_text()

    # remove https:// and replace / with _ so it can write file
    if "https" not in page:
        outputName = page.split("http://", 1)[1].replace('/', '_').strip() + '.scrape'
    else:
        outputName = page.split("https://", 1)[1].replace('/', '_').strip() + '.scrape'

    file = open(outputName, "w")
    file.write(text)
    file.close()
    # sleep to stop get request refusal
    return text
