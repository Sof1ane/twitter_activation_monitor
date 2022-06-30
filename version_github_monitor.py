import requests
import os
import json
import discord
from discord import Webhook, RequestsWebhookAdapter, Embed
import time

bearer_token = str(os.environ['BEARER_TOKEN'])
user_to_track = (os.environ['USER_TO_TRACK'])
discord_webhook = str(os.environ['DISCORD_WEBHOOK'])

first_harvest = []
second_harvest = []
# start time used for the loop

starttime = time.time()

# Create the url with the users you chosed and the fields you want the api to return

def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames={}".format(user_to_track)
    user_fields = "user.fields=description,created_at,name,profile_image_url,protected,url,public_metrics,location,url"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url



def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response


def send_embed(harvest):
    
    

    #### Create the initial embed object ####
    embed = discord.Embed(title="{} is live".format(harvest['username']), url="https://twitter.com/{}".format(harvest['username']), color=0x109319)

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="{}".format(harvest['username']), url="https://twitter.com/{}".format(harvest['username']), icon_url="{}".format(harvest['img_url'].replace("normal", "400x400")))

    embed.set_thumbnail(url="{}".format(harvest['img_url'].replace("normal", "400x400")))

    embed.add_field(name="Followers", value="{}".format(harvest['followers_count']))
    embed.add_field(name="Followings", value="{}".format(harvest['following_count']))
    embed.add_field(name="Tweets", value="{}".format(harvest['tweet_count']))
    embed.add_field(name="Protected ?", value="{}".format(harvest['is_protected']))
    embed.add_field(name="Creation_date", value="{}".format(harvest['creation_date']))
    embed.add_field(name="Description", value="{}".format(harvest['description']))
    embed.add_field(name="URL", value="{}".format(harvest['url']))
    embed.add_field(name="ID", value="{}".format(harvest['id']))
    
    webhook = Webhook.from_url(discord_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(embed = embed)

    
def harvest_data():

    url = create_url()

    response = connect_to_endpoint(url)

    temp= response.json()

    if response.text[2:6] == "data":

        dict = {
        'is_activated':False,
        "name" : temp["data"][0]["name"],
        "username" : temp["data"][0]["username"],
        "img_url" : temp["data"][0]["profile_image_url"],
        "description" : temp["data"][0]["description"],
        "followers_count" : temp["data"][0]["public_metrics"]['followers_count'],
        "following_count" : temp["data"][0]["public_metrics"]['following_count'],
        "tweet_count" : temp["data"][0]["public_metrics"]['tweet_count'],
        "is_protected" : temp["data"][0]["protected"],
        "creation_date" : temp["data"][0]["created_at"],
        "id" : temp["data"][0]["id"],
        "url" : temp["data"][0]["url"],
        }
        return (dict)

    else:
        
        dict = {
        'is_activated':False,
        "name" : '',
        "username" : '',
        "img_url" : '',
        "description" : '',
        "followers_count" : '',
        "following_count" : '',
        "tweet_count" : '',
        "is_protected" : '',
        "creation_date" : '',
        "id" : '',
        "url" : '',
        }
        return (dict)


    

# def main():
    
#     send_embed(embed_to_send)

                

while True:
    
    first_harvest = harvest_data()
    
    
    time.sleep(25.0 - ((time.time() - starttime) % 25.0))
    
    
    
    second_harvest = harvest_data()
    
    if second_harvest != first_harvest:
        send_embed(second_harvest)
        
