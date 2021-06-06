import requests
from bs4 import BeautifulSoup as bs
import scraperSettings
import os

def ScrapeTescoFreddo(passthrough_link):
    try:
        site_link = passthrough_link
        #page = requests.get(site_link, headers=scraperSettings.tesco_headers, timeout=5)
        command = "curl " + site_link + """ -H 'authority: www.tesco.com' -H 'cache-control: max-age=0' -H 'sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"' -H 'sec-ch-ua-mobile: ?0' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' -H 'sec-fetch-site: none' -H 'sec-fetch-mode: navigate' -H 'sec-fetch-user: ?1' -H 'sec-fetch-dest: document' -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8'  --compressed """
        page = os.popen(command).read()
        html_soup = bs(page, 'html.parser')
        price_div = html_soup.find('div', class_='price-per-sellable-unit price-per-sellable-unit--price price-per-sellable-unit--price-per-item')
        span_tag = price_div.span.find('span', attrs={'data-auto':'price-value','class':'value'}, recursive=False)
        price = format(float(span_tag.text), '.2f')
        return price
    except:
        print ("Generic exception, probably timed out.")
