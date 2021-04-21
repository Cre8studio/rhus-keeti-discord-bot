import discord
intents = discord.Intents.default()
intents.members = True

import re
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

from openpyxl import Workbook
from openpyxl import load_workbook

import os

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    global thisGuild
    global systemChannel
    logger.info(f'We have logged in as {client.user}')
    thisGuild = client.guilds[0]
    logger.info(f'connected to: {thisGuild}')
    systemChannel = discord.utils.get(thisGuild.channels, name="system")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if type(message.channel) == discord.channel.DMChannel:
        if validate_is_contact_number(message.content) and validate_is_date(message.content):
            match = re.findall('\d{10}', message.content)
            validnumber = match[0]
            match2 = re.findall('(\d{2}\/\d{2}\/\d{4})', message.content)
            validdate = match2[0]
            workbook = load_workbook("Rhus_Keeti_Data.xlsx")
            worksheet = workbook.active
            found = False
            for row in range(3, len(worksheet['F'])+1):
                worksheetvalue = worksheet[f'E{row}'].value
                if (isinstance(worksheetvalue, str) == False):
                    worksheetvalue = worksheetvalue.strftime("%d/%m/%Y") #needed to do this because the excel spreadsheet number format picks up the value as date
                    
                if worksheet[f'F{row}'].value == validnumber and worksheetvalue == validdate:
                    worksheet[f'G{row}'] = f'{message.author.name}#{message.author.discriminator}'
                    workbook.save("Rhus_Keeti_Data.xlsx")
                    
                    member = thisGuild.get_member(message.author.id)
                    role = discord.utils.get(thisGuild.roles, name=worksheet[f'A{row}'].value)
                    await member.add_roles(role)
                    logger.info(f'Added {role.name} to @{member}')
                    role2 = discord.utils.get(thisGuild.roles, name=worksheet[f'B{row}'].value)
                    await member.add_roles(role2)
                    logger.info(f'Added {role2.name} to @{member}')
                    await systemChannel.send(f'{message.author.name} has been authenticated')
                    await message.channel.send("Baie welkom by die Rhus Keeti Discord Server. Jy het toegang tot die Algemene groep en jou kursusgroep. Respekteer mekaar. Lekker kuier en deel met ons jou ervarings!")
                    found = True
                    break
            
            if found == False:
                await systemChannel.send(f'@{message.author.name}: {message.content} - failed')
                await message.channel.send("Probeer weer. Wat is jou kontak nommer en geboorte datum? bv. 0765940666 30/01/2000")
        else:
            await systemChannel.send(f'@{message.author.name}: {message.content} - failed')
            await message.channel.send("Probeer weer. Wat is jou kontak nommer en geboorte datum? bv. 0765940666 30/01/2000")
    else:
        if message.content.startswith('$whois'):
            for member in thisGuild.members:
                if len(member.roles) <= 1:
                    await systemChannel.send(f"{member.mention} has no roles")

@client.event
async def on_member_join(member):
    message = f'member joined: {member}'
    await write(message)
    DMchannel = await member.create_dm()
    await DMchannel.send("Goeie Dag Verkenner/Offisier, my naam is Jan Tarentaal die rekenaar program. \n Ek is aangestel om seker te maak jy is een van ons Rhus Keeti kampers die jaar. \n Antwoord asseblief op hierdie boodskap met jou nommer (die een waarmee jy ingeskryf is) asook jou geboorte datum. \n In die volgende formaat: 0765940666 30/01/2000. \n \n Hiermee sal ek die nodige rolle aan jou kan gee waarmee jy alles sal kan sien wat jy gaan nodig he om die kamp teen volle te kan geniet. \n Vriendelike groete \n Jan Tarentaal die rekenaar program.")
    
    
@client.event
async def on_member_remove(member):
    message = f'member left: {member}'
    await write(message)
    
@client.event
async def on_guild_join(guild):
    message = f'joined a guild: {guild.name}'
    await write(message)

@client.event    
async def on_guild_remove(guild):
    message = f'left guild: {guild.name}'
    await write(message)

def validate_is_contact_number(number):
    match = re.findall('\d{10}', number)
    return len(match) > 0

def validate_is_date(message):
    match = re.findall('(\d{2}\/\d{2}\/\d{4})', message)
    return (len(match) > 0)

async def write(message):
    logging.info(message)
    await systemChannel.send(message)

client.run(os.getenv('TOKEN'))
