#MIT License
#Copyright (c) 2020 Semih Aydın
#UTF-8

import discord
from discord.ext import commands
import sqlite3
import json
import os
from logging_files.evos_log import logger

intents = discord.Intents.default()
intents.members = True
modules = 0
loaded = 0
defaultPrefix = '.'

def get_prefix(client,message):
    db = sqlite3.connect("data/server/Data.db")
    cursor = db.cursor()
    try :
        cursor.execute("SELECT CUSTOM_PREFIX FROM ServerData WHERE SERVER_ID=?",(str(message.guild.id),))
        customPrefix = cursor.fetchone()
        return customPrefix[0]
    except Exception as e:
        logger.error(f"Evos | GetPrefix | Error: {e}")
        return defaultPrefix

def get_token():
    with open("data/Token.json", "r") as tokenjsonFile:
        data = json.load(tokenjsonFile)
        token = data["token"]
    return token

client = commands.Bot(command_prefix=get_prefix,intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} hazır.")
    print(f"{len(client.guilds)} sunucuda aktif.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(".yardım | 🎵 HIGH QUALITY MUSIC"))
    logger.info("Evos is ready.")

print("Modül yükleme işlemi başladı.")
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        modules += 1
        try :
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f"\t{filename[:-3]} yüklendi.")
            loaded += 1
        except Exception as e:
            logger.error(f"Evos | LoadModule | File: {filename[:-3]} | Error: {e}")
            print(f"\t{filename[:-3]} yüklenemedi.")
print(f"\t-------------------\n\tToplam Eklenti : \t{modules}\n\tYüklenen Eklenti : \t{loaded}\n\tYüklenemeyen Eklenti : \t{modules-loaded}\n\t-------------------")
print("Modül yükleme işlemi tamamlandı.")

client.run(get_token())