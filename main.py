from pubg_python import PUBG, Shard
from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG
import asyncio,aiohttp,json
from bs4 import BeautifulSoup as soup
import discord
from discord.ext import commands

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiYjBmMjI5MC1kYThhLTAxM2QtYmUyOC00NjQ0ZDA0YjAzMzEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNzQxMDI2Mjk1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImNsYW5fYm90In0.VP7mJuRRQEJd27HJrEdzEIq1VpCZ3DIOr7GrE0oyxy8"

api = PUBG(api_key, "pc-eu")

player_names = input().split()

players = api.players_from_names(player_names)

for player in players:
    player_season = player.get_current_season()
    squad_fpp_stats = player_season.game_mode_stats("squad", "fpp")
    print(player.name, " ", squad_fpp_stats)

#oran_gg_e ol1vOCHKA TexasDolly