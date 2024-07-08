import discord

from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())
# Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix

@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях
async def ping(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'I`m here, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена