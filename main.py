import discord
import asyncio
import random
import yt_dlp as youtube_dl
import os

from discord.utils import get
from pytube import YouTube
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())
#TheTestIsOn = True



#---------------------------------------
#        ЗВУКОВОЙ ФУНКЦИОНАЛ
#---------------------------------------



@bot.command()
async def play(ctx, url):
    save_path = settings['wd'] + ctx.guild.name + '/'
    os.makedirs(save_path, exist_ok=True)
    if ctx.author.voice is None:
        await ctx.send("Вы не подключены к голосовому каналу")
        return
    author = ctx.message.author
    voice_channel = author.voice.channel
    await ctx.send(f'Погодите секунду, сейчас загружу')
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video.download(output_path=save_path, filename='tryme.mp4')

    voice_client = get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        vc = await voice_channel.connect()
    else:
        vc = voice_client
        vc.stop()    
    vc.play(discord.FFmpegPCMAudio(save_path + 'tryme.mp4'))
    await ctx.send(f'Готово!')
    while vc.is_playing():
        await asyncio.sleep(1)
    if vc.is_paused()==False:
        await vc.disconnect()

@bot.command()
async def restart(ctx):
    save_path = settings['wd'] + ctx.guild.name + '/'
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
    vc.play(discord.FFmpegPCMAudio(save_path + 'tryme.mp4'))
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