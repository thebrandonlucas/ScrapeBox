import PySimpleGUI as sg
import requests
import os
import subprocess
import tldextract
from bs4 import BeautifulSoup

# from packages.pythonSitemap import config
# from packages.pythonSitemap import crawler
# from packages.pythonSitemap import *
# import packages.pythonSitemap.config
# import packages.pythonSitemap.crawler
# import packages.pythonSitemap.main
import main
# TODO: fix package problems

mainDir = os.getcwd()

sg.ChangeLookAndFeel('Black')
main_form = sg.FlexForm('Scraping the Web', default_element_size=(40, 1))

layout = [
    # [sg.Text("Web Scraper", size=(30, 1), font=("Times", 20))],
    [sg.Text("Enter URL", size=(12, 1), font=("Times", 20)),
     sg.InputText(size=(30, 1), font=("Times", 20))
    ],
    # [sg.Text("Enter URL to generate sitemap", size=(20, 1), font=("Times", 20)),
    #  sg.InputText()
    # ],
    [sg.Submit("Generate Sitemap", size=(20, 2), font=("Times", 20)),
     sg.Submit("Scrape", size=(20, 2), font=("Times", 20))
    ]
]

main_form = main_form.Layout(layout)
while True:
    button, values = main_form.Read()
    # user clicks 'X'
    if button is None:
        break
    # download chosen page
    if button == 'Scrape':
        # check if save destination is empty
        file_destination = sg.PopupGetFolder("Enter Destination")
        try:
            webpage = requests.get(values[0])
            soup = BeautifulSoup(webpage.content, 'html.parser')
        except:
            sg.Popup(button, "Error, could not download page")
            continue

        text = soup.get_text()
        os.chdir(file_destination)
        # remove https:// and replace / with _ so it can write file
        outputName = values[0].split("https://", 1)[1].replace('/', '_') + '.txt'
        # domain_name = tldextract.extract(values[0])
        sg.Popup(outputName)
        try:
            file = open(outputName, "w")
        except:
            sg.Popup("Couldn't create file. Please ensure duplicate filename does not exist")
            continue
        file.write(text)
        file.close()
        os.chdir(mainDir)

        # write to file
    elif button == 'Generate Sitemap':
        outputName = values[0].split("https://", 1)[1].replace('/', '_') + '.txt'
        outputName = 'test.txt'
        sitemap = main.main(values[0], outputName)
        sitemap.main()
        break
