import discord
import requests
import json

dcClient = discord.Client()


@dcClient.event
async def on_ready():
    print('logged in as {0.user}'.format(dcClient))


@dcClient.event
async def on_message(message):
    if message.content.startswith('$fune'):
        context = 'Q: How do you buy a person?\n' + 'A: Import it from Africa or East Asia\n' + \
            '\n' + 'Q: ' + message.content.replace('$fune ', '')

        payload = {
            "context": context,
            "token_max_length": 64,
            "temperature": 0.7,
            "top_p": 1.0,
        }

        response = requests.post(
            "http://api.vicgalle.net:5000/generate", params=payload).json()

        response = json.loads(json.dumps(response))

        await message.reply(response['text'], mention_author=True)
        print('sent response to {0.author}'.format(message))

dcClient.run('token')
