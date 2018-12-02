import PySimpleGUI as sg
import requests
import os
import re
import subprocess
import tldextract
from time import sleep
from bs4 import BeautifulSoup

# from packages.pythonSitemap import config
# from packages.pythonSitemap import crawler
# from packages.pythonSitemap import *
# import packages.pythonSitemap.config
# import packages.pythonSitemap.crawler
# import packages.pythonSitemap.main
from scrape_functions import *
import main
# TODO: fix package problems

mainDir = os.getcwd()

sg.ChangeLookAndFeel('Black')
main_form = sg.FlexForm('ScrapeBox', default_element_size=(40, 1))

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
    ],
    [sg.Submit("Scrape a Sitemap", size=(41, 1), font=("Times", 20))],
    [sg.Text('_' * 89)],
    [sg.Text('Choose HTML Tag', size=(20, 1), font=("Times", 20)),
     # sg.Text('Choose Content Type', size=(20, 1), font=("Times", 20))
     ],
    [sg.InputCombo(('All', '<a>', '<b>', '<button>', '<div>', '<form>', '<h1>', '<img>',
                   '<input>', '<li>', '<meta>', '<p>', '<script>', '<select>', '<style>', '<table>',
                   '<tbody>', '<td>', '<textarea>', '<th>', '<thead>', '<ul>'),
                   size=(40, 1), font=("Times", 20)),
     # sg.InputCombo(('Text', 'Image'), size=(20, 1), font=("Times", 20))
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
        page = values[0]
        tag = values[1]
        # type = values[-1]
        # try:
        text = single_scrape(page, tag)
        # except:
        #     sg.Popup(button, "Error, could not download page")
        #     continue
        os.chdir(file_destination)
        sg.Popup("File Added")
        os.chdir(mainDir)

    # write to file
    elif button == 'Generate Sitemap':
        sg.Popup("This may take a minute...")
        outputName = values[0].split("https://", 1)[1].replace('/', '_') + '.smap'
        sitemap = main.main(values[0], outputName)
        sitemap.main()
        oldFile = open(outputName, 'r')
        cleanText = oldFile.read()
        cleanText = re.sub('<lastmod>.*?</lastmod>','', cleanText, flags=re.DOTALL)
        cleanText = BeautifulSoup(cleanText, 'lxml').text
        lines = cleanText.split()
        lines = [line for line in lines if line.strip()]
        cleanText = '\n'.join(lines)
        oldFile.close()
        os.remove(outputName)
        cleanFile = open(outputName, 'w')
        cleanFile.write(cleanText)
        cleanFile.close()
        sg.Popup("Sitemap Generated!")

    elif button == 'Scrape a Sitemap':
        sitemapName = sg.PopupGetFile('Choose Sitemap')
        sitemap = open(sitemapName, 'r').readlines()
        page = values[0]
        tag = values[1]
        dest_folder = sg.PopupGetFolder('Choose Destination Folder')
        os.chdir(dest_folder)
        domain_name = tldextract.extract(sitemap[0])
        domain_name = domain_name.subdomain + domain_name.domain + domain_name.suffix
        if not os.path.isdir(domain_name + "_scrapes"):
            os.makedirs(domain_name + "_scrapes")
        os.chdir(domain_name + "_scrapes")
        count = 0
        for page in sitemap:
            count = count + 1
            sg.OneLineProgressMeter('Progress...', count, 10000, 'key')
            try:
                text = single_scrape(page, tag)
            except:
                sg.Popup(button, "Error, could not download page \"" + page + "\"")
                continue
