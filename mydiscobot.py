import discord
from discord.ext.commands import Bot
import youtube_dl
import random
import requests
from discord import Game
from discord import Status


BOT_PREFIX = "!"
command_prefix = BOT_PREFIX
client = Bot(BOT_PREFIX)


@client.event
async def on_ready():
    print('bot is ready')
    await client.change_presence(game=Game(name='with ur mum | !help'))
    await client.change_presence(status=discord.Status('dnd'))

@client.event
async def on_member_join(member):
    channel = client.get_channel(468156564897923085)
    await client.send_message(channel, 'Please welcome ' + member)


@client.event
async def on_message(message):
    if message.content.startswith('!you'):
        await client.send_message(message.channel, 'gayyy')
    await client.process_commands(message)


@client.command(description='gives weather at zipcode location',
                brief='!weather [zipcode]')
async def weather(zipcode):
    z = zipcode
    url = 'https://api.openweathermap.org/data/2.5/weather?zip='+z+',us&appid=bc57d25a9a5966e6c00441b9fd6bd6c2'
    r = requests.get(url)
    value = r.json()['main']['temp']
    value_faren = int((value - 273.15) * 1.8 + 32)
    await client.say('The current temp (F) at ' + z + ' is: '+ str(value_faren) + ' degrees')



@client.command(name='8ball',
                description='Answers a yes/no question.',
                brief='!8ball [question]',
                aliases=['eight_ball', 'eightball','8-ball'],
                pass_context=True)
async def eight_ball(context):
    outcomes = [
        'My sources say no',
        'Thats is a resounding no',
        'It is not looking likely',
        'Outlook not so good.',
        'Too hard to tell',
        'It is quite possible',
        'Most likely.',
        'Definitely',
        'Signs point to yes.'
    ]
    await client.say(random.choice(outcomes))

@client.command(description='Gives a squared value of your number',
                brief='!squared [number]')
async def squared(number):
    squarenum = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squarenum))

@client.command(brief='Gives current prices of Bitcoin')
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say('Bitcoin price is $: ' + value)

@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True,
                brief='use !play [song name] use !leave after done')
async def play(ctx, *description):
    des = str(description)
    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q='+des+'&order=relevance&type=video&maxResults=1&key=AIzaSyAke4iBdpIGMw-ujUKawc_Avtvh0G-q0lA'
    req = requests.get(url)
    value = req.json()['items'][0]['id']['videoId']
    new_url = 'https://www.youtube.com/watch?v='+value+''
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(new_url)
    player.start()



client.run(os.getenv('TOKEN'))

