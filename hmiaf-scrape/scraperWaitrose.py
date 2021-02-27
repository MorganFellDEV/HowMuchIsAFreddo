import requests
from bs4 import BeautifulSoup as bs
import scraperSettings

def ScrapeWaitroseFreddo(passthrough_link):
    site_Waitrose = passthrough_link
    page = requests.get(site_Waitrose,headers=scraperSettings.headers)
    html_soup = bs(page.content, 'html.parser')
    price_div = html_soup.find('div', class_='priceAndActions___16N4-')
    span_tag = price_div.span.find('span', recursive=False)
    span_tag = span_tag.text
    span_tag = span_tag.replace("£","")
    price = float(span_tag)
    return format(price, '.2f')
    