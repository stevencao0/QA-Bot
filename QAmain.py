import discord
import os
from discord.ext import commands
# Discord.py is an Asynchornous library - functions are called when responding to an event
#.\QAmain.py
client = commands.Bot(command_prefix='.')
token = ''


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# loads all .py files in local cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
