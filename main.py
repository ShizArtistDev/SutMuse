import discord
import random

from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())
# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix

@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях
async def ping(ctx): # Создаём функцию и передаём аргумент ctx.
    await ctx.send(f'Я здесь!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author

@bot.command() 
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

@bot.command()
async def roll(ctx, min_num=None, max_num=None): 
    author = ctx.message.author 
    if min_num is None or max_num is None:
        await ctx.send(f'{author.mention}, прошу, ввместе с командой вводи минимальное и максимальное число (например: !roll 4 17)')
        return
    try:
        min_num = int(min_num)
        max_num = int(max_num)
        if min_num>max_num:
            temp = min_num
            min_num = max_num
            max_num = temp
    except ValueError:
        await ctx.send(f'{author.mention}, введи нормальные числа')
        return
    
    random_number = random.randint(min_num, max_num)
    await ctx.send(f'{author.mention}, Твоё число в диапазоне от {min_num} до {max_num} = {random_number}')

bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена