import requests
import json
import scraperSettings

# ASDA HAS AN API HOORAY THANK YOU 

api_link = "https://groceries.asda.com/api/items/view?&itemid="
def ScrapeAsdaFreddo(passthrough_link):
    try:
        site_link = passthrough_link
        asda_url_reversed = str(site_link).split('/')
        asda_url_reversed.reverse()
        actual_url = asda_url_reversed[0]
        asda_output = requests.get(str(api_link+actual_url), headers=scraperSettings.headers)
        json_version = json.loads(asda_output.content)
        price_output=(json_version["items"][0]['price'])
        price_output = price_output.replace("£","")
        price = float(price_output)
        return format(price, '.2f')
    except Exception as e:
        print(e)
        