from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from pubg_python import PUBG, Shard
from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG
from aiogram import Bot, Dispatcher
import asyncio
from models import Player
from settings import api_key, tg_token, db_main

api = PUBG(api_key, "pc-eu")

bot = Bot(token=tg_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hi')

@dp.message(Command('winrate_teammates'))
async def cmd_start(message: Message):
    await message.answer(text="В разработке")

@dp.message(Command('leaderboard'))
async def cmd_start(message: Message):

    s = 0

    game = {}
    kd = {}
    kda = {}
    damage = {}
    top_1 = {}
    top_10 = {}
    headshot = {}

    for i in range(10):

        if i == 0:
            player_names = ['oran_gg_e', 'ol1vOCHKA', 'TexasDolly', 'magichka_nuar', 'Shafi_____',
                            'B1mBOSS', 'karma-__-', 'kuatkamiev', 'TechnicolorBlack', 'ClickMer']
            players = api.players_from_names(player_names)

        if i == 1:
            player_names = ['CougarHex', 'EV0Like', 'freaky_slider', 'General-L1', 'Glenn_ufa',
                            'Kingjulyen', 'levirran', 'lillypillyhell', 'Luka_Shymkent', 'maksason14']
            players = api.players_from_names(player_names)

        if i == 2:
            player_names = ['MIKHAILB9', 'Nikita_Kotov17', 'Rengoku1237', 'Romzes19', 'Ryukbtww',
                            'Shelby_Young', 'TaLiCmAn4IK', 'telnoter', 'tOKAE-v', 'TSARrrr']
            players = api.players_from_names(player_names)

        if i == 3:
            player_names = ['vazgenxer', 'wii663', 'Zef1r_off', 'ZLOY_PISUN', 'ZRideR59',
                            'zZzAlexXxzZz', 'Meehoa', 'S0XFATEEV']
            players = api.players_from_names(player_names)

        if i == 4:
            break

        for player in players:
            s = s + 1
            player_season = player.get_current_season()
            squad_fpp_stats = player_season.game_mode_stats("squad", "fpp")
            await message.answer(text=f"{player.name} {s}/38")

            if squad_fpp_stats:

                game.update({player.name: squad_fpp_stats["rounds_played"]})

                if squad_fpp_stats["losses"] != 0:
                    kd.update({player.name: squad_fpp_stats["kills"] / squad_fpp_stats["losses"]})
                    kda.update({player.name: (squad_fpp_stats["kills"] + squad_fpp_stats["assists"]) / squad_fpp_stats[
                        "losses"]})
                else:
                    kd.update({player.name: squad_fpp_stats["kills"]})
                    kda.update({player.name: squad_fpp_stats["kills"] + squad_fpp_stats["assists"]})

                if squad_fpp_stats["rounds_played"] != 0:
                    damage.update({player.name: squad_fpp_stats["damage_dealt"] / squad_fpp_stats["rounds_played"]})
                    top_1.update({player.name: squad_fpp_stats["wins"] / squad_fpp_stats["rounds_played"] * 100})
                    top_10.update({player.name: squad_fpp_stats["top_10s"] / squad_fpp_stats["rounds_played"] * 100})
                else:
                    damage.update({player.name: squad_fpp_stats["damage_dealt"]})
                    top_1.update({player.name: squad_fpp_stats["wins"] * 100})
                    top_10.update({player.name: squad_fpp_stats["top_10s"] * 100})

                if squad_fpp_stats["kills"] != 0:
                    headshot.update({player.name: squad_fpp_stats["headshot_kills"] / squad_fpp_stats["kills"] * 100})
                else:
                    headshot.update({player.name: squad_fpp_stats["headshot_kills"] * 100})

    sorted_game = dict(sorted(game.items(), key=lambda item: item[1], reverse=True))
    sorted_kd = dict(sorted(kd.items(), key=lambda item: item[1], reverse=True))
    sorted_kda = dict(sorted(kda.items(), key=lambda item: item[1], reverse=True))
    sorted_damage = dict(sorted(damage.items(), key=lambda item: item[1], reverse=True))
    sorted_top_1 = dict(sorted(top_1.items(), key=lambda item: item[1], reverse=True))
    sorted_top_10 = dict(sorted(top_10.items(), key=lambda item: item[1], reverse=True))
    sorted_headshot = dict(sorted(headshot.items(), key=lambda item: item[1], reverse=True))

    s = 0
    output = "games\n"
    for game in sorted_game:
        s += 1
        output += f"{s}, {game}, {sorted_game[game]}\n"
    await message.answer(text=output)

    s = 0
    output = "kd\n"
    for kds in sorted_kd:
        s += 1
        output += f"{s}, {kds}, {sorted_kd[kds]}\n"
    await message.answer(text=output)

    s = 0
    output = "kda\n"
    for kdas in sorted_kda:
        s += 1
        output += f"{s}, {kdas}, {sorted_kda[kdas]}\n"
    await message.answer(text=output)

    s = 0
    output = "damage\n"  # Заголовок сообщения
    for damages in sorted_damage:
        s += 1
        output += f"{s}, {damages}, {sorted_damage[damages]}\n"
    await message.answer(text=output)

    s = 0
    output = "top_1\n"  # Заголовок сообщения
    for top_1s in sorted_top_1:
        s += 1
        output += f"{s}, {top_1s}, {sorted_top_1[top_1s]}\n"
    await message.answer(text=output)

    s = 0
    output = "top_10\n"  # Заголовок сообщения
    for top_10s in sorted_top_10:
        s += 1
        output += f"{s}, {top_10s}, {sorted_top_10[top_10s]}\n"
    await message.answer(text=output)

    s = 0
    output = "headshot\n"  # Заголовок сообщения
    for headshots in sorted_headshot:
        s += 1
        output += f"{s}, {headshots}, {sorted_headshot[headshots]}\n"
    await message.answer(text=output)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        asyncio.run(db_main())
    except KeyboardInterrupt:
        print("Бот выключен")

