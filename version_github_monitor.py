import requests
import os
import json
import discord
from discord import Webhook, RequestsWebhookAdapter, Embed
import time

bearer_token = str(os.environ['BEARER_TOKEN'])
user_to_track = str(os.environ['USER_TO_TRACK'])
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
    user_fields = "user.fields=description,created_at,name,profile_image_url,protected,url,public_metrics,location"
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


def create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id, location):

    #### Create the initial embed object ####
    embed = discord.Embed(title="{} is live".format(username), url="https://twitter.com/{}".format(username), color=0x109319)

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="{}".format(name), url="https://twitter.com/{}".format(username), icon_url="{}".format(img_url.replace("normal", "400x400")))

    embed.set_thumbnail(url="{}".format(img_url.replace("normal", "400x400")))

    embed.add_field(name="Followers", value="{}".format(followers_count))
    embed.add_field(name="Followings", value="{}".format(following_count))
    embed.add_field(name="Tweets", value="{}".format(tweet_count))
    embed.add_field(name="Protected ?", value="{}".format(is_protected))
    embed.add_field(name="Creation_date", value="{}".format(creation_date))
    if description:
        embed.add_field(name="Description", value="{}".format(description))
    if location: 
        embed.add_field(name="Localisation", value="{}".format(location))
    embed.add_field(name="ID", value="{}".format(id))
    return embed



def send_embed(response):

    json_response= embed.json()

    name = json_response["data"][i]["name"]
    username = json_response["data"][i]["username"]
    img_url = json_response["data"][i]["profile_image_url"]
    description = json_response["data"][i]["description"]
    followers_count = json_response["data"][i]["public_metrics"]['followers_count']
    following_count = json_response["data"][i]["public_metrics"]['following_count']
    tweet_count = json_response["data"][i]["public_metrics"]['tweet_count']
    is_protected = json_response["data"][i]["protected"]
    creation_date = json_response["data"][i]["created_at"]
    location = json_response["data"][i]["location"]
    id = json_response["data"][i]["id"]


    webhook = Webhook.from_url(discord_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(embed = embed)

def harvest_data():
    url = create_url()
    response = connect_to_endpoint(url)
    
    # embed_1 = create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id,location)
    return response


# def main():
    
#     send_embed(embed_to_send)

while True:
    first_harvest = harvest_data()
    time.sleep(25.0 - ((time.time() - starttime) % 25.0))
    second_harvest = harvest_data()
    if second_harvest.text[2:6] == "data":
        if first_harvest.text[2:6] == "data":
            if second_harvest != first_harvest:
                temp = create_embed(second_harvest)
                send_embed(temp)
