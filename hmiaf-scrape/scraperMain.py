import mysql.connector
import datetime
from bs4 import BeautifulSoup as bs
import requests

import time
import csv
import json
import scraperTesco
import scraperWaitrose
import scraperMorrisons
import scraperSettings

import boto3


lambdaclient = boto3.client('lambda',region_name='eu-west-2')

mydb = mysql.connector.connect(
    host="REDACTED",
    user="REDACTED",
    password="REDACTED",
    database="hmiaf"
)

mycursor = mydb.cursor()


def UpdateSQL(passthrough_item_id, passthrough_grab_time, passthrough_price):
    mycursor.execute("INSERT into prices(item_id,grabbed_time,price) values (%s,%s,%s)",
                     (passthrough_item_id, passthrough_grab_time, str(passthrough_price)))
    mydb.commit()


latest_price_query = "SELECT * FROM prices WHERE item_id=%s ORDER BY grabbed_time DESC LIMIT 1"

mycursor.execute("SELECT * FROM items")
for item in mycursor.fetchall():
    print("Item: " + str(item))
    mycursor.execute(latest_price_query, (item[0],))
    price_sql = (mycursor.fetchall()[0])[3]
    print("Price DB: %s" % (price_sql))
    if (item[1] == "Tesco"):
        price_scrape = scraperTesco.ScrapeTescoFreddo(item[2])
        print("Price online: %s" % (price_scrape))

    elif (item[1] == "Waitrose"):
        price_scrape = scraperWaitrose.ScrapeWaitroseFreddo(item[2])
        print("Price online: %s" % (price_scrape))

    elif (item[1] == "Morrisons"):
        price_scrape = scraperMorrisons.ScrapeMorrisonsFreddo(item[2])
        print("Price online: %s" % (price_scrape))

    if (price_sql != float(price_scrape)):
        UpdateSQL(item[0], time.strftime('%Y-%m-%d %H:%M:%S'), price_scrape)
        if (float(price_scrape) > price_sql):  # Price gone up
            print("Price has gone up!")
            # tweet price up
            tweetbot_inputParams = {
                "ItemStore": str(item[1]),
                "ItemOldPrice": str(price_sql),
                "ItemNewPrice": str(price_scrape),
                "ItemChange": "up",
                "IsMultipack": str(item[3]),
                "MultipackQuantity": str(item[4])
            }
            response = lambdaclient.invoke(
                FunctionName='REDACTED',
                InvocationType='RequestResponse',
                Payload=json.dumps(tweetbot_inputParams)
            )
            print("BEFORE SENDING" + json.dumps(tweetbot_inputParams))
            response_from_twitter_bot = json.load(response['Payload'])
            print(response_from_twitter_bot)

        elif (float(price_scrape) < price_sql):  # Price gone down
            print("Price has gone down.")
            # tweet price down
            tweetbot_inputParams = {
                "ItemStore": str(item[1]),
                "ItemOldPrice": str(price_sql),
                "ItemNewPrice": str(price_scrape),
                "ItemChange": "down",
                "IsMultipack": str(item[3]),
                "MultipackQuantity": str(item[4])
            }
            print("BEFORESENDING" + json.dumps(tweetbot_inputParams))
            response = lambdaclient.invoke(
                FunctionName='REDACTED',
                InvocationType='RequestResponse',
                Payload=json.dumps(tweetbot_inputParams)
            )
            print(response)
            response_from_twitter_bot = json.load(response['Payload'])
            print((response_from_twitter_bot))
        else:
            print("No change.")


mydb.close()
