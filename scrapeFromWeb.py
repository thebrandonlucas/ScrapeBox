import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup

sg.ChangeLookAndFeel('Black')
main_form = sg.FlexForm('Scraping the Web', default_element_size=(40, 1))

layout = [
    [sg.Text("Web Scraper", size=(30, 1), font=("Times", 20))],
    [sg.Text("Enter URL", size=(20, 1), font=("Times", 20)),
     sg.InputText()
    ],
    # [sg.Text("Enter URL to generate sitemap", size=(20, 1), font=("Times", 20)),
    #  sg.InputText()
    # ],
    [sg.Submit("Generate Sitemap", size=(20, 1), font=("Times", 30)),
     sg.Submit("")
    ]
]

button, values = main_form.LayoutAndRead(layout)

while True:
    if button is None:
        break
    # download chosen page
    if button == 'Generate Sitemap':
        try:
            webpage = requests.get(values[0])
        except:
            sg.Popup(button, "Error, could not download page")

        soup = BeautifulSoup(webpage.content, 'html.parser')
        text = soup.get_text()
        sg.Popup(button, values[0])

    # open generate sitemap window
    # elif button == 'SiteMap':
    #     while True:
    #         main_form.Hide()
    #         sitemap_form = sg.FlexForm('SiteMap Generation', default_element_size=(40, 1))
    #
    #         sitemap_layout = [
    #             [sg.Text("Enter URL to generate sitemap", size=(30, 1), font=("Times", 20)),
    #              sg.InputText()
    #             ],
    #             [sg.Submit("Generate Sitemap", size=(20, 1), font=("Times", 30))]
    #         ]
    #
    #         buttonSiteMap, valuesSiteMap = sitemap_form.LayoutAndRead(sitemap_layout)
    #         if buttonSiteMap is None:
    #             sitemap_form.Close()
    #             main_form.UnHide()
    #             break
