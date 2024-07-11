import discord
import asyncio
import random
import yt_dlp as youtube_dl

from discord.utils import get
from pytube import YouTube
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())
#TheTestIsOn = True



#---------------------------------------
#          ТЕКСТОВЫЙ ФУНКЦИОНАЛ
#---------------------------------------



# @bot.command()
# async def ping(ctx):
#     await ctx.send(f'Я здесь!')

# @bot.command() 
# async def hello(ctx):
#     author = ctx.message.author
#     await ctx.send(f'Привет, {author.mention}!')

# @bot.command()
# async def roll(ctx, min_num=None, max_num=None, another=None): 
#     author = ctx.message.author 
#     if another is None:
#         if min_num is None or max_num is None:
#             await ctx.send(f'{author.mention}, пожалуйста, вместе с командой вводи минимальное и максимальное число (например: !roll {random.randint(0, 17)} {random.randint(18, 49)})')
#             return
#         try:
#             min_num = int(min_num)
#             max_num = int(max_num)
#             if min_num>max_num:
#                 temp = min_num
#                 min_num = max_num
#                 max_num = temp
#         except ValueError:
#             await ctx.send(f'{author.mention}, пожалуйста, введи нормальные числа')
#             return
        
#         random_number = random.randint(min_num, max_num)
#         await ctx.send(f'{author.mention}, Твоё число в диапазоне от {min_num} до {max_num} = {random_number}') 
#     else:
#         await ctx.send(f'{author.mention}, Пожалуйста, введи только 2 числа')



#---------------------------------------
#        ЗВУКОВОЙ ФУНКЦИОНАЛ
#---------------------------------------



@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
        return
        
    author = ctx.message.author
    voice_channel = author.voice.channel
    await ctx.send(f'Погодите секунду, сейчас загружу')
    save_path = 'C:/pyvids'
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(output_path=save_path, filename='tryme.mp4')

    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = voice_client
        vc.stop()    
    vc.play(discord.FFmpegPCMAudio(settings['wd']))
    await ctx.send(f'Готово!')
    while vc.is_playing():
        await asyncio.sleep(1)
    if vc.is_paused()==False:
        await vc.disconnect()

@bot.command()
async def restart(ctx):
    if ctx.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
        return
    author = ctx.message.author
    voice_channel = author.voice.channel
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = voice_client
        vc.stop()    
    vc.play(discord.FFmpegPCMAudio(settings['wd']))
    await ctx.send(f'Без проблем, запускаю ещё раз!')
    while vc.is_playing():
        await asyncio.sleep(1)
    if vc.is_paused()==False:
        await vc.disconnect()
    
@bot.command()
async def pause(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send('Сейчас ничего не играет')

@bot.command()
async def resume(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send('Сейчас ничего не стоит на паузе')

@bot.command()
async def stop(ctx):
    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        voice_client.disconnect()
    else:
        await ctx.send('Сейчас ничего не играет')


#---------------------------------------
#        ТЕСТОВЫЙ ФУНКЦИОНАЛ
#
#        Работает, только когда
#     переменная TheTestIsOn = True
#---------------------------------------

#if TheTestIsOn:
         
    
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена