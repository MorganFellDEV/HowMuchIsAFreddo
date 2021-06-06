# Needs a specific user-agent whilst using AWS to avoid queue-it.

import requests
from bs4 import BeautifulSoup as bs
import scraperSettings

def ScrapeMorrisonsFreddo(passthrough_link):
    try:
        site_link = passthrough_link
        page = requests.get(site_link, headers=scraperSettings.gb_headers)
        html_soup = bs(page.content, 'html.parser')
        price = html_soup.find("meta", itemprop="price")
        price = price.get("content")
        price = format(float(price), '.2f')
        return price
    except:
        print("Exception, possible timeout.")