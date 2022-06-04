import discord
import os
from discord.ext import commands
# Discord.py is an Asynchornous library - functions are called when responding to an event
#.\QAmain.py
#client = discord.Client()
client = commands.Bot(command_prefix='!')
token = 'OTgxNzU4MjQ0MDU1ODM0NjY1.GtEdMo.0SBcCYv1f2ZtzG9OT42-XKO35_CAAj-SgHkS5E'


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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
