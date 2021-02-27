import requests
from bs4 import BeautifulSoup as bs
import scraperSettings

def ScrapeTescoFreddo(passthrough_link):
    site_link = passthrough_link
    page = requests.get(site_link, headers=scraperSettings.tesco_headers)
    html_soup = bs(page.content, 'html.parser')
    price_div = html_soup.find('div', class_='price-per-sellable-unit price-per-sellable-unit--price price-per-sellable-unit--price-per-item')
    span_tag = price_div.span.find('span', attrs={'data-auto':'price-value','class':'value'}, recursive=False)
    price = format(float(span_tag.text), '.2f')
    return price

