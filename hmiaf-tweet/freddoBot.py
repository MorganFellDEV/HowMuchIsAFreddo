import tweepy
import os
import sys
import random

consumer_key = os.environ["AWS_HMIAF_CONSUMER_KEY"]
consumer_secret = os.environ["AWS_HMIAF_CONSUMER_SECRET"]

oauth_token = os.environ["AWS_HMIAF_OAUTH_TOKEN"]
oauth_secret = os.environ["AWS_HMIAF_OAUTH_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_secret)
api = tweepy.API(auth)

reactions_positive = [
    ", hooray!",
    ", fantastic!",
    ", brilliant!",
    ", wonderful!"
]

reactions_negative = [
    ", are you joking?",
    ", horrific.",
    ", disgusting.",
    ", really?!?"
]

def lambda_handler(event,context):
    pt_Store = event['ItemStore']
    pt_oldPrice = event['ItemOldPrice']
    pt_NewPrice = event['ItemNewPrice']
    pt_Change = event['ItemChange']
    is_multipack = event['IsMultipack']
    multipack_quantity = event['MultipackQuantity']
    
    if (is_multipack == "True"):
        individualPrice = format((float(pt_NewPrice) / float(multipack_quantity)), '.2f')
        
        if (pt_Change == "up"): # Negative reaction
            try:
                api.update_status(status="The price for a %sx Freddo multipack at %s has gone %s from £%s to £%s, that's £%s per Freddo%s" % (multipack_quantity, pt_Store, pt_Change, pt_oldPrice, pt_NewPrice,individualPrice, random.choice(reactions_negative)))
                return{
                    'status':'tweeted'
                }
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        elif (pt_Change == "down"): # Positive reaction
            try:
                api.update_status(status="The price for a %sx Freddo multipack at %s has gone %s from £%s to £%s, that's £%s per Freddo%s" % (multipack_quantity, pt_Store, pt_Change, pt_oldPrice, pt_NewPrice,individualPrice, random.choice(reactions_positive)))
                return{
                    'status':'tweeted'
                }
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
        
    elif (is_multipack == "False"):
        if (pt_Change == "up"): # Negative reaction
            try:
                api.update_status(status="The price for a Freddo at %s has gone %s from £%s to £%s%s" % (pt_Store, pt_Change, pt_oldPrice, pt_NewPrice, random.choice(reactions_negative)))
                return{
                    'status':'tweeted'
                }
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
            
        elif (pt_Change == "down"): # Positive reaction
            try:
                api.update_status(status="The price for a Freddo at %s has gone %s from £%s to £%s%s" % (pt_Store, pt_Change, pt_oldPrice, pt_NewPrice, random.choice(reactions_positive)))
                return{
                    'status':'tweeted'
                }
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise