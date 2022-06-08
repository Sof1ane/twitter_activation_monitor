# Twitter Reactivation Monitor, Bearer Auth Mode

Simple script to send Discord notifications as soon as someone reactivates his account. You can changes fields that appears in the Discord Embed if you want to make it lighter or not.

# What to update in code ? 

Username : Change it to the one you wanna monitor. Separated by commas

Bearer token : Change it to your twitter bearer token. Get it [here](https://developer.twitter.com/en/portal/dashboard) . Paste it raw in the .env or make it a string in the script.

Discord webhook : Change it to you discord webhook of the channel you want updates to appear. See tutorial [here](https://help.dashe.io/en/articles/2521940-how-to-create-a-discord-webhook-url) . Past

I suggest you to create a .env file to keep theses variables.

Exemple of the .env file format

![Screenshot_7](https://user-images.githubusercontent.com/43276871/172608773-7e8f04f8-a584-4524-ba45-f19a5d4bc74f.png)


# How to Run

Once you made these changes just run the file with Python, dont forget to install the needed packages in requirements.txt with the command : 

```bash
$ pip install -r requirements.txt
```


# Whats next ?

Stop spamming on the same delay as the api call rate. Or maybe change the way it pings, I thought about updating the embed and not sending an other one.




