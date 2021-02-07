import requests

# webhook of a discord channel

mUrl = "https://discord.com/api/webhooks/807828812833751091/eW0c3JeMnruuNL9gvioFmHTUk65oO2IQVGWUvWGLqqgopVJI7pvYKnC3q6EOO7l4DcpF"

# message. here "!pop" will call the stockbot in the #stockbot_automation channel and show which stocks

# are being discussed in Discord

data = {"content": '!pop'}

response = requests.post(mUrl, json=data)
