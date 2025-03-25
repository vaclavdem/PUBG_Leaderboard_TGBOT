import chicken_dinner.pubgapi
from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG
from pubg_python import PUBG, Shard
import pubg_python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import discord
import os
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

GUILD_ID = 627073760016465930

# Подключение к MySQL
DATABASE_URL = "mysql+mysqlconnector://Vatslav:Va_12345678@localhost/PUBG_db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

telegram_bot = Bot(
    token=tg_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# API PUBG
api_1 = chicken_dinner.pubgapi.PUBG(api_key, "pc-eu")

api_2 = pubg_python.PUBG(api_key, Shard.STEAM)



