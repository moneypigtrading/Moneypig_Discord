import discord

from discord.ext import commands

import csv

import pandas as pd

from instabot import Bot

bot = Bot() #initiate the instabot class

import os

dirname = os.path.dirname(__file__)

filename = os.path.join(dirname, '../config.ini')


class discord_utility():

    def send_file_to_discord(self, message, file_path, webhook_id, webhook_token):

    #https://www.reddit.com/r/Discord_Bots/comments/9ip99a/can_you_upload_images_directly_with_a_webhook/

        webhook = discord.Webhook.partial(webhook_id, webhook_token, adapter=discord.RequestsWebhookAdapter())  # Your webhook

        with open(file=file_path, mode='rb') as f:

            my_file = discord.File(f)

        webhook.send(message, username='webhook', file=my_file)

    def send_format_csv_to_discord(self, message, file_path, out_file, webhook_id, webhook_token):

        webhook = discord.Webhook.partial(webhook_id, webhook_token, adapter=discord.RequestsWebhookAdapter())  # Your webhook

        f = open(file_path)
        csv_f = csv.reader(f)

        with open(out_file, 'w') as csvfile:

            writer = csv.writer(csvfile)

            for row in csv_f:
                print('{:<15}  {:<15}  {:<20} {:<25} '.format(*row), file=open(out_file, "a"))

        with open(file=out_file, mode='rb') as f:

            my_file = discord.File(f)

        webhook.send(message, username='webhook', file=my_file)


    def discord_bot_return_format_csv(self, message, file_path, webhook_id, webhook_token):

        #this is an interacitve Bot function

        #https://stackoverflow.com/questions/64321503/im-trying-to-output-the-already-formatted-contents-of-a-csv-file-into-a-text-ch

        # token here has to be a Discord developer token https://stackoverflow.com/questions/51602617/improper-token-passed

        print(webhook_id)

        print(webhook_token)

        f = open(file_path)
        csv_f = csv.reader(f)

        token = webhook_token
        client = discord.Client()

        @client.event
        async def on_ready():
            print('Bot ready')

        @client.event
        async def on_message(message):
            if message.author == client.user:  # preventing the bot from replying to itself
                return

            if message.channel.id == webhook_id:
                if message.content.startswith('%MarketMovers'):
                    channel = client.get_channel(webhook_id)
                    msg = message
                    await channel.send(msg)
                    for row in csv_f:
                        await channel.send(('`{:<40}  {:<10}  {:<10}`').format(*row).replace('Â', ''))
                else:
                    await message.delete()

        client.run(webhook_token)

    def post_to_instagram(self, file_name, IG_caption_message):

        # https://www.geeksforgeeks.org/post-a-picture-automatically-on-instagram-using-python/

        # how to publish with instagram locations

        #https://developers.facebook.com/docs/instagram-api/guides/content-publishing/#publish-with-locations

        # get the IG private key so that we can get historical data

        df = pd.read_csv(filename, skipinitialspace=True)

        secret = df['secret'].loc[df['name'] == 'instagram']

        secret = secret.to_string(index=False)

        secret = secret.lstrip()  # there is a leading space in the private key so need to remove it

        username = df['user_name'].loc[df['name'] == 'instagram']

        username = username.to_string(index=False).lstrip()

        print(username)
        print(secret)

        bot.login(username=username,
                  password=secret)

        bot.upload_photo(file_name, IG_caption_message)

    def post_to_facebook_group(self, facebook_group_id, message, access_token):

        import facebook
        import time

        groups = [facebook_group_id]

        time.sleep(5)
        graph = facebook.GraphAPI(access_token)
        groups = graph.get_object("me/groups")
        group_id = facebook_group_id #groups['data'][0]['id']  # we take the ID of the first group
        graph.put_object(group_id, "feed", message=message)
