import discord
import asyncio
from discord.ext import commands
import time
import xlsxwriter
# pip install xlsxwriter
from datetime import date

correct = '\U0001F44D'
client = commands.Bot(command_prefix='.')
today = date.today()
client.passed = 0
client.row = 0
client.workbook = xlsxwriter.Workbook('TestSuiteReport.xlsx')
client.worksheet = client.workbook.add_worksheet()


class Tests(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Calls on start up
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot logging in')

    #Test Suite - !test in text channel to execute
    @commands.command()
    async def test(self, ctx):

        #worksheetDataEntry(worksheet, row, id, description, passFail, date)
        await worksheetDataEntryManual(0, "ID", "Description", "Pass/Fail", "Date")
        await reservedEntry(self)
        await test_ping(self, ctx, "Hear ya!", "Using !ping command in text channel and bot respond 'Hey There'")
        time.sleep(1)
        #Test - !play - Is the tester in a voice channel while calling?
        await test_play(self, ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'You need to be in a voice channel.', "Calling !play while not in a voice channel.")
        time.sleep(1)
        #Test - !play - Tester input an empty link
        await test_play(self, ctx, '', 'Invalid Youtube Link', '!play command - with no link input')
        time.sleep(1)
        #Test - !play - Tester input an invalid link
        await test_play(self, ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXc', 'Invalid Youtube Link', '!play command - with incorrect link')
        time.sleep(1)
        #Test - !play - Can bot join and play music?
        await connectVoiceChannel(ctx)
        await test_play(self, ctx, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', '**Now playing:** Rick Astley - Never Gonna Give You Up (Official Music Video)',
                        "Using !play command in text channel to queue the URL youtube link to music bot and play in the requestor's voice channel")
        time.sleep(8)
        #Test - !play - Queue another song
        await test_play(self, ctx, 'https://www.youtube.com/watch?v=jDwVkXVHIqg', '**Added to Queue:** toad sings chandelier', "Queue another song while bot is playing music")
        time.sleep(5)
        #Test - !skip - Skip a song
        await test_skip(self, ctx, '**Now playing:** toad sings chandelier', "Using !skip command in text channel to skip music bot's current song")
        time.sleep(5)
        #Test - !stop - Can bot stop playing with '!stop'?
        await test_stop(self, ctx, 'Stoppingu', "Using !stop command in text channel to stop the music bot")
        #Finish - Disconnect from voice channel, produce worksheet file, close QA bot
        await ctx.guild.voice_client.disconnect()
        await worksheetDataEntryManual(client.row+2, "", "Passed / Total", str(client.passed)+"/"+str(client.row), "")
        client.workbook.close()
        await client.close()

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before, after):
        #Test - Did music bot successfully join a voice channel when called?
        if member.id == 839410270287429663 and not before.channel and after.channel:
            await worksheetDataEntryManual(1, "A1", "Music bot joins a voice channel", "Pass", today.strftime("%b-%d-%Y"))
            client.passed += 1

# Unit Test - !ping command
async def test_ping(self, ctx, messageCheck, testDescription):
    await ctx.send('!ping')
    await testConfirmation(self, ctx, messageCheck, testDescription)

# Unit Test - !play command
async def test_play(self, ctx, link, messageCheck, testDescription):
    await ctx.send(f'!play {link}')
    await testConfirmation(self, ctx, messageCheck, testDescription)

#Helper function - Connects to the tester's voice channel
async def connectVoiceChannel(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send('Joining voice chat')
    else:
        await ctx.send('Join a voice channel to further test - play, skip, disconnect')

# Unit Test - !skip command
async def test_skip(self, ctx,  messageCheck, testDescription):
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.send(f'!skip')
        await testConfirmation(self, ctx, messageCheck, testDescription)
    else:
        await ctx.send("Error: Tester is not a channel")

# Unit Test - !stop command
async def test_stop(self, ctx, messageCheck, testDescription):
    await ctx.send(f'!stop')
    await testConfirmation(self, ctx, messageCheck, testDescription)

#Helper function - Checks bot replies for correctness
async def testConfirmation(self, ctx, messageCheck, testDescription):

    def check(message):
        return message.content == messageCheck and message.author.bot
    try:
        msg = await self.client.wait_for('message', check=check, timeout=5.0)
        if msg:
            await msg.add_reaction(correct)
            await worksheetDataEntry(testDescription, "Pass", today.strftime("%b-%d-%Y"))
            client.passed += 1

    except asyncio.TimeoutError:
        await ctx.send("Error - Expected: " + messageCheck)
        await worksheetDataEntry(testDescription, "Fail", today.strftime("%b-%d-%Y"))

#Reserved workbook data entry for special async cases.


async def reservedEntry(self):
    client.row += 1
    await worksheetDataEntryManual(1, "A1", "Music bot joins a voice channel", "Fail", today.strftime("%b-%d-%Y"))

#Automatic data entry that increments ID and row


async def worksheetDataEntry(description, passFail, date):
    client.row += 1
    id = "U" + str(client.row)

    client.worksheet.write(client.row, 0, id)
    client.worksheet.write(client.row, 1, description)
    client.worksheet.write(client.row, 2, passFail)
    client.worksheet.write(client.row, 3, date)

# Allows manual custom data entry where you can input the row and id


async def worksheetDataEntryManual(row, id, description, passFail, date):
    client.worksheet.write(row, 0, id)
    client.worksheet.write(row, 1, description)
    client.worksheet.write(row, 2, passFail)
    client.worksheet.write(row, 3, date)


def setup(client):
    client.add_cog(Tests(client))
