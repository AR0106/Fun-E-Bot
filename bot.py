import discord
import requests
import json
import openai
import os
import datetime

dcClient = discord.Client()


@dcClient.event
async def on_ready():
    print('logged in as {0.user}'.format(dcClient))


@dcClient.event
async def on_message(message):
    if message.content.startswith('$fune'):
        openai.api_key = 'openai-key'

        context = 'Q: How do you buy a person?\n' + 'A: Import it from Africa or East Asia\n' + \
            '\n' + 'Q: ' + message.content.replace('$fune ', '')

        if message.content == '$fune continue':
            async for previous_message in message.channel.history(limit=20):
                if previous_message.author == dcClient.user and len(previous_message.content) / 4 >= 192 and message.content != 'The Message is Too Long, Please Try a New Question':
                    context = previous_message.content
                    break
            if len(previous_message.content) / 4 >= 192:
                print(len(previous_message.content) / 4)
                await message.reply('The Message is Too Long, Please Try a New Question')
                return

        response = openai.Completion.create(
            engine="curie",
            prompt=context,
            temperature=0.7,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response = json.loads(json.dumps(response))

        previous_message = response['choices'][0]['text']

        await message.reply(response['choices'][0]['text'], mention_author=True)
        print('sent response to {0.author}: {1} - {2} Tokens'.format(
            message, datetime.datetime.now(), len(context) / 4))

dcClient.run('discord-key')
