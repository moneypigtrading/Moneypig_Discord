import discord

class discord_utility():

    def send_file_to_discord(self, message, file_path, webhook_id, webhook_token):

    #https://www.reddit.com/r/Discord_Bots/comments/9ip99a/can_you_upload_images_directly_with_a_webhook/

        webhook = discord.Webhook.partial(webhook_id, webhook_token, adapter=discord.RequestsWebhookAdapter())  # Your webhook

        with open(file=file_path, mode='rb') as f:

            my_file = discord.File(f)

        webhook.send(message, username='webhook', file=my_file)