import requests
import os
import json
import discord
from discord import Webhook, RequestsWebhookAdapter, Embed
import time
from dotenv import load_dotenv

load_dotenv()

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
    user_fields = "user.fields=description,created_at,name,profile_image_url,protected,public_metrics,url"
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


def send_embed(temp):
    
    name = temp["data"][0]["name"]
    username = temp["data"][0]["username"]
    img_url = temp["data"][0]["profile_image_url"]
    description = temp["data"][0]["description"]
    followers_count = temp["data"][0]["public_metrics"]['followers_count']
    following_count = temp["data"][0]["public_metrics"]['following_count']
    tweet_count = temp["data"][0]["public_metrics"]['tweet_count']
    is_protected = temp["data"][0]["protected"]
    creation_date = temp["data"][0]["created_at"]
    id = temp["data"][0]["id"]
    url = temp["data"][0]["url"]

    #### Create the initial embed object ####
    embed = discord.Embed(title="{} is live".format(temp[1]), url="https://twitter.com/{}".format(temp[1]), color=0x109319)

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="{}".format(temp[0]), url="https://twitter.com/{}".format(temp[1]), icon_url="{}".format(temp[2].replace("normal", "400x400")))

    embed.set_thumbnail(url="{}".format(temp[2].replace("normal", "400x400")))

    embed.add_field(name="Followers", value="{}".format(temp[4]))
    embed.add_field(name="Followings", value="{}".format(temp[5]))
    embed.add_field(name="Tweets", value="{}".format(temp[6]))
    embed.add_field(name="Protected ?", value="{}".format(temp[7]))
    embed.add_field(name="Creation_date", value="{}".format(temp[8]))
    if temp[3]:
        embed.add_field(name="Description", value="{}".format(temp[3]))
    if temp[10]:
        embed.add_field(name="URL", value="{}".format(temp[10]))
    embed.add_field(name="ID", value="{}".format(temp[9]))
    
    webhook = Webhook.from_url(discord_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(embed = embed)




def create_json(response):

    json_response= response.json()

    
    return (json_response)

    
def harvest_data():
    url = create_url()
    response = connect_to_endpoint(url)
    
    # embed_1 = create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id)
    return response.json()


# def main():
    
#     send_embed(embed_to_send)

while True:
    first_harvest = harvest_data()
    time.sleep(25.0 - ((time.time() - starttime) % 25.0))
    second_harvest = harvest_data()
    if second_harvest.text[2:6] == "data":
        if first_harvest.text[2:6] == "data":
            if second_harvest.text != first_harvest.text:
                temp = create_json(second_harvest)
                send_embed(temp)
                