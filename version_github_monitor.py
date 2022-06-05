import requests
import os
import json
from discord import Webhook, RequestsWebhookAdapter, Embed
import time
import discord
import os
starttime = time.time()

bearer_token = os.environ['BEARER_TOKEN']
user_to_track = os.environ['user_to_track']
discord_webhook = os.environ['discord_webhook']

def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames={}".format(user_to_track)
    user_fields = "user.fields=description,created_at,name,profile_image_url,protected,url,public_metrics"
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


def create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id):

    #### Create the initial embed object ####
    embed = discord.Embed(title="{} is live".format(username), url="https://twitter.com/{}".format(username), color=0x109319)

    # Add author, thumbnail, fields, and footer to the embed
    embed.set_author(name="{}".format(name), url="https://twitter.com/{}".format(username), icon_url="{}".format(img_url))

    embed.set_thumbnail(url="{}".format(img_url))

    embed.add_field(name="Followers", value="{}".format(followers_count), inline=False)
    embed.add_field(name="Followings", value="{}".format(following_count), inline=False)
    embed.add_field(name="Tweets", value="{}".format(tweet_count), inline=False)
    embed.add_field(name="Protected ?", value="{}".format(is_protected), inline=False)
    embed.add_field(name="Creation_date", value="{}".format(creation_date), inline=False)
    if description:
        embed.add_field(name="Description", value="{}".format(description), inline=False)
    embed.add_field(name="ID", value="{}".format(id), inline=False)
    webhook = Webhook.from_url(discord_webhook, adapter=RequestsWebhookAdapter())
    webhook.send(embed = embed)

def main():
    url = create_url()
    response = connect_to_endpoint(url)
    json_response = connect_to_endpoint(url).json()
    if response.text[2:6] == "data":
        name = json_response["data"][0]["name"]
        username = json_response["data"][0]["username"]
        img_url = json_response["data"][0]["profile_image_url"]
        description = json_response["data"][0]["description"]
        followers_count = json_response["data"][0]["public_metrics"]['followers_count']
        following_count = json_response["data"][0]["public_metrics"]['following_count']
        tweet_count = json_response["data"][0]["public_metrics"]['tweet_count']
        is_protected = json_response["data"][0]["protected"]
        creation_date = json_response["data"][0]["created_at"]
        id = json_response["data"][0]["id"]

        create_embed(name,username,img_url,description,followers_count,following_count,tweet_count,is_protected,creation_date,id)



while True:
    main()
    time.sleep(15.0 - ((time.time() - starttime) % 15.0))
