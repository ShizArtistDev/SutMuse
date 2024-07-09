import discord
import random
import youtube_dl

from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())


#---------------------------------------
#          БАЗОВЫЙ ФУНКЦИОНАЛ
#---------------------------------------


@bot.command()
async def ping(ctx):
    await ctx.send(f'Я здесь!')

@bot.command() 
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

@bot.command()
async def roll(ctx, min_num=None, max_num=None, another=None): 
    author = ctx.message.author 
    if another is None:
        if min_num is None or max_num is None:
            await ctx.send(f'{author.mention}, пожалуйста, вместе с командой вводи минимальное и максимальное число (например: !roll {random.randint(0, 17)} {random.randint(18, 49)})')
            return
        try:
            min_num = int(min_num)
            max_num = int(max_num)
            if min_num>max_num:
                temp = min_num
                min_num = max_num
                max_num = temp
        except ValueError:
            await ctx.send(f'{author.mention}, пожалуйста, введи нормальные числа')
            return
        
        random_number = random.randint(min_num, max_num)
        await ctx.send(f'{author.mention}, Твоё число в диапазоне от {min_num} до {max_num} = {random_number}') 
    else:
        await ctx.send(f'{author.mention}, Пожалуйста, введи только 2 числа')


#---------------------------------------
#        ОСНОВНОЙ ФУНКЦИОНАЛ
#---------------------------------------


@bot.command()
async def play(ctx, url):
    author = ctx.message.author
    voice_channel = author.voice.channel
    if voice_channel:
        vc = await voice_channel.connect()
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(url2))
    else:
        await ctx.send(f'{author.mention}, Тебе нужно быть в голосовом канале, чтобы использоваь эту команду!')

@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send('Сейчас ничего не играет')

@bot.command()
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send('Бот не подключён к голосовому каналу')


bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена