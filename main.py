from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG
from pubg_python import PUBG, Shard
import pubg_python
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Bot, Dispatcher, types
import asyncio
from settings import tg_token, api_1, api_2
from models import add_games_to_player, session, Game, get_games_by_player_id, get_player_id


bot = Bot(token=tg_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Hi')


@dp.message(Command("winrate_teammates"))
async def winrate_teammates_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    player_names = ['oran_gg_e', 'ol1vOCHKA', 'TexasDolly', 'magichka_nuar', 'Shafi_____',
                    'B1mBOSS', 'karma-__-', 'kuatkamiev', 'TechnicolorBlack', 'ClickMer',
                    'CougarHex', 'EV0Like', 'freaky_slider', 'General-L1', 'Glenn_ufa',
                    'Kingjulyen', 'levirran', 'lillypillyhell', 'Luka_Shymkent', 'maksason14',
                    'MIKHAILB9', 'Nikita_Kotov17', 'Rengoku1237', 'Romzes19', 'Ryukbtww',
                    'Shelby_Young', 'TaLiCmAn4IK', 'telnoter', 'tOKAE-v', 'TSARrrr',
                    'vazgenxer', 'wii663', 'Zef1r_off', 'ZLOY_PISUN', 'ZRideR59',
                    'zZzAlexXxzZz', 'Meehoa', 'S0XFATEEV']
    if len(parts) > 1:
        args = parts[1]
        if args in player_names:
            await message.answer(text="Игрок найден")
            players = api_1.players_from_names([args])
            if players:
                player = players[0]
            else:
                await message.answer(text="Игрок не найден в PUBG API")
            player_season = player.get_current_season()
            games_list = player_season.match_ids("squad", "fpp")
            for game in games_list:
                games_teammates = {'oran_gg_e' : 0, 'ol1vOCHKA' : 0, 'TexasDolly' : 0, 'magichka_nuar' : 0,
                    'Shafi_____' : 0, 'B1mBOSS' : 0, 'karma-__-' : 0, 'kuatkamiev' : 0, 'TechnicolorBlack' : 0,
                    'ClickMer' : 0, 'CougarHex' : 0, 'EV0Like' : 0, 'freaky_slider' : 0, 'General-L1' : 0,
                    'Glenn_ufa' : 0, 'Kingjulyen' : 0, 'levirran' : 0, 'lillypillyhell' : 0, 'Luka_Shymkent' : 0,
                    'maksason14' : 0, 'MIKHAILB9' : 0, 'Nikita_Kotov17' : 0, 'Rengoku1237' : 0, 'Romzes19' : 0,
                    'Ryukbtww' : 0, 'Shelby_Young' : 0, 'TaLiCmAn4IK' : 0, 'telnoter' : 0, 'tOKAE-v' : 0,
                    'TSARrrr' : 0, 'vazgenxer' : 0, 'wii663' : 0, 'Zef1r_off' : 0, 'ZLOY_PISUN' : 0, 'ZRideR59' : 0,
                    'zZzAlexXxzZz' : 0, 'Meehoa' : 0, 'S0XFATEEV' : 0}
                wins_teammates = {'oran_gg_e' : 0, 'ol1vOCHKA' : 0, 'TexasDolly' : 0, 'magichka_nuar' : 0,
                    'Shafi_____' : 0, 'B1mBOSS' : 0, 'karma-__-' : 0, 'kuatkamiev' : 0, 'TechnicolorBlack' : 0,
                    'ClickMer' : 0, 'CougarHex' : 0, 'EV0Like' : 0, 'freaky_slider' : 0, 'General-L1' : 0,
                    'Glenn_ufa' : 0, 'Kingjulyen' : 0, 'levirran' : 0, 'lillypillyhell' : 0, 'Luka_Shymkent' : 0,
                    'maksason14' : 0, 'MIKHAILB9' : 0, 'Nikita_Kotov17' : 0, 'Rengoku1237' : 0, 'Romzes19' : 0,
                    'Ryukbtww' : 0, 'Shelby_Young' : 0, 'TaLiCmAn4IK' : 0, 'telnoter' : 0, 'tOKAE-v' : 0,
                    'TSARrrr' : 0, 'vazgenxer' : 0, 'wii663' : 0, 'Zef1r_off' : 0, 'ZLOY_PISUN' : 0, 'ZRideR59' : 0,
                    'zZzAlexXxzZz' : 0, 'Meehoa' : 0, 'S0XFATEEV' : 0}
                del games_teammates[player.name]
                del wins_teammates[player.name]
                teammate_list = []
                team1 = ''
                team2 = ''
                team3 = ''
                game_mode = 'squad'
                result = ''
                game_api = api_1.match(game)
                for roster in game_api.rosters:
                    for teammate in roster.player_names:
                        if teammate == player.name:
                            teammate_list = roster.player_names
                            teammate_list.remove(player.name)
                            result = roster.won
                            break
                if teammate_list.__len__() == 3:
                    team1 = teammate_list[0]
                    team2 = teammate_list[1]
                    team3 = teammate_list[2]
                if teammate_list.__len__() == 2:
                    team1 = teammate_list[0]
                    team2 = teammate_list[1]
                if teammate_list.__len__() == 1:
                    team1 = teammate_list[0]
                if result == False:
                    result = 'lose'
                else:
                    result = 'win'
                add_games_to_player(session=session, player_nickname=player.name, game_id=game, result=result, game_mode=game_mode,
                                    teammate1=team1, teammate2=team2, teammate3=team3)
            for game in get_games_by_player_id(session, get_player_id(session, player.name)):
                if game.result == 'win':
                    if game.teammate1 in player_names:
                        wins_teammates[game.teammate1] = wins_teammates[game.teammate1] + 1
                    if game.teammate2 in player_names:
                        wins_teammates[game.teammate2] = wins_teammates[game.teammate2] + 1
                    if game.teammate3 in player_names:
                        wins_teammates[game.teammate3] = wins_teammates[game.teammate3] + 1
                if game.teammate1 in player_names:
                    games_teammates[game.teammate1] = games_teammates[game.teammate1] + 1
                if game.teammate2 in player_names:
                    games_teammates[game.teammate2] = games_teammates[game.teammate2] + 1
                if game.teammate3 in player_names:
                    games_teammates[game.teammate3] = games_teammates[game.teammate3] + 1
            s = 0
            output = ''
            player_names.remove(player.name)
            for teammate in player_names:
                s += 1
                if games_teammates[teammate] != 0:
                    output += (f"{s}, {teammate}, побед: {wins_teammates[teammate]}, игр сыграно: {games_teammates[teammate]}, "
                            f"процент побед: {round(wins_teammates[teammate] / games_teammates[teammate] * 100, 2)}\n")
                else:
                    output += (
                        f"{s}, {teammate}, побед: {wins_teammates[teammate]}, игр сыграно: {games_teammates[teammate]}, "
                        f"процент побед: {wins_teammates[teammate] * 100}\n")
            await message.answer(text=output)

            await message.answer(text="В разработке")
        else:
            await message.answer(text="Игрок не найден")

    if len(parts) == 1:
        await message.answer(text="Введите ник игрока после комманды")

@dp.message(Command("leaderboard"))
async def winrate_teammates_handler(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        args = parts[1]

        s = 0

        game = {}
        kd = {}
        kda = {}
        damage = {}
        top_1 = {}
        top_10 = {}
        headshot = {}

        for i in range(10):

            if args != 'solo' and args != 'duo' and args != 'squad':
                await message.answer(text="Неправильно введён режим, возможные варианты - solo, duo, squad")
                break

            if i == 0:
                player_names = ['oran_gg_e', 'ol1vOCHKA', 'TexasDolly', 'magichka_nuar', 'Shafi_____',
                                'B1mBOSS', 'karma-__-', 'kuatkamiev', 'TechnicolorBlack', 'ClickMer']
                players = api_1.players_from_names(player_names)

            if i == 1:
                player_names = ['CougarHex', 'EV0Like', 'freaky_slider', 'General-L1', 'Glenn_ufa',
                                'Kingjulyen', 'levirran', 'lillypillyhell', 'Luka_Shymkent', 'maksason14']
                players = api_1.players_from_names(player_names)

            if i == 2:
                player_names = ['MIKHAILB9', 'Nikita_Kotov17', 'Rengoku1237', 'Romzes19', 'Ryukbtww',
                                'Shelby_Young', 'TaLiCmAn4IK', 'telnoter', 'tOKAE-v', 'TSARrrr']
                players = api_1.players_from_names(player_names)

            if i == 3:
                player_names = ['vazgenxer', 'wii663', 'Zef1r_off', 'ZLOY_PISUN', 'ZRideR59',
                                'zZzAlexXxzZz', 'Meehoa', 'S0XFATEEV']
                players = api_1.players_from_names(player_names)

            if i == 4:
                break

            for player in players:
                s = s + 1
                player_season = player.get_current_season()

                if args == 'squad':
                    squad_fpp_stats = player_season.game_mode_stats("squad", "fpp")

                if args == 'duo':
                    squad_fpp_stats = player_season.game_mode_stats("duo", "fpp")

                if args == 'solo':
                    squad_fpp_stats = player_season.game_mode_stats("solo", "fpp")

                await message.answer(text=f"{player.name} {s}/38")

                if squad_fpp_stats:

                    game.update({player.name: squad_fpp_stats["rounds_played"]})

                    if squad_fpp_stats["losses"] != 0:
                        kd.update({player.name: round(squad_fpp_stats["kills"] / squad_fpp_stats["losses"], 2)})
                        kda.update({player.name: round((squad_fpp_stats["kills"] + squad_fpp_stats["assists"]) / squad_fpp_stats[
                            "losses"], 2)})
                    else:
                        kd.update({player.name: squad_fpp_stats["kills"]})
                        kda.update({player.name: squad_fpp_stats["kills"] + squad_fpp_stats["assists"]})

                    if squad_fpp_stats["rounds_played"] != 0:
                        damage.update({player.name: round(squad_fpp_stats["damage_dealt"] / squad_fpp_stats["rounds_played"], 2)})
                        top_1.update({player.name: round(squad_fpp_stats["wins"] / squad_fpp_stats["rounds_played"] * 100, 2)})
                        top_10.update({player.name: round(squad_fpp_stats["top_10s"] / squad_fpp_stats["rounds_played"] * 100)})
                    else:
                        damage.update({player.name: squad_fpp_stats["damage_dealt"]})
                        top_1.update({player.name: squad_fpp_stats["wins"] * 100})
                        top_10.update({player.name: squad_fpp_stats["top_10s"] * 100})

                    if squad_fpp_stats["kills"] != 0:
                        headshot.update({player.name: round(squad_fpp_stats["headshot_kills"] / squad_fpp_stats["kills"] * 100, 2)})
                    else:
                        headshot.update({player.name: squad_fpp_stats["headshot_kills"] * 100})

        sorted_game = dict(sorted(game.items(), key=lambda item: item[1], reverse=True))
        sorted_kd = dict(sorted(kd.items(), key=lambda item: item[1], reverse=True))
        sorted_kda = dict(sorted(kda.items(), key=lambda item: item[1], reverse=True))
        sorted_damage = dict(sorted(damage.items(), key=lambda item: item[1], reverse=True))
        sorted_top_1 = dict(sorted(top_1.items(), key=lambda item: item[1], reverse=True))
        sorted_top_10 = dict(sorted(top_10.items(), key=lambda item: item[1], reverse=True))
        sorted_headshot = dict(sorted(headshot.items(), key=lambda item: item[1], reverse=True))

        if args == 'solo' or args == 'duo' or args == 'squad':

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
            output = "damage\n"
            for damages in sorted_damage:
                s += 1
                output += f"{s}, {damages}, {sorted_damage[damages]}\n"
            await message.answer(text=output)

            s = 0
            output = "top_1\n"
            for top_1s in sorted_top_1:
                s += 1
                output += f"{s}, {top_1s}, {sorted_top_1[top_1s]}\n"
            await message.answer(text=output)

            s = 0
            output = "top_10\n"
            for top_10s in sorted_top_10:
                s += 1
                output += f"{s}, {top_10s}, {sorted_top_10[top_10s]}\n"
            await message.answer(text=output)

            s = 0
            output = "headshot\n"
            for headshots in sorted_headshot:
                s += 1
                output += f"{s}, {headshots}, {sorted_headshot[headshots]}\n"
            await message.answer(text=output)

    if len(parts) == 1:
        await message.answer(text="Нужно написать режим игры(solo, duo, squad)")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")

