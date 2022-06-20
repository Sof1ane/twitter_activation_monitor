import requests
import os
import json
import discord
from discord import Webhook, RequestsWebhookAdapter, Embed
import time

bearer_token = str(os.environ['BEARER_TOKEN'])
user_to_track = str(os.environ['USER_TO_TRACK'])
discord_webhook = str(os.environ['DISCORD_WEBHOOK'])

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
    embed.set_author(name="{}".format(name), url="https://twitter.com/{}".format(username), icon_url="{}".format(img_url))

    embed.set_thumbnail(url="{}".format(img_url))

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
    webhook = Webhook.from_url(discord_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(embed = embed)

def main():
    url = create_url()
    response = connect_to_endpoint(url)
    json_response = connect_to_endpoint(url).json()
    num_accounts = response.text.count("profile_image_url")
    for i in range(num_accounts):
        if response.text[2:6] == "data":
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

            create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id,location)
            
while True:
    main()
    time.sleep(25.0 - ((time.time() - starttime) % 25.0))
