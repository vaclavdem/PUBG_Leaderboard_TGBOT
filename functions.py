from settings import GUILD_ID
from aiogram import Bot
from aiogram.types import BotCommand
from settings import client, telegram_bot, dp

async def get_voice_channel_info():
    """ Функция получает список пользователей в голосовых каналах. """
    guild = client.get_guild(GUILD_ID)
    if not guild:
        return "❌ Ошибка: Сервер не найден. Проверьте GUILD_ID."

    report = []
    for channel in guild.voice_channels:
        members = [member.display_name for member in channel.members]
        if members:
            report.append(f"🔊 <b>{channel.name}</b> ({len(members)} чел.): " + ", ".join(members))

    return "\n".join(report) if report else "🔇 В голосовых каналах никого нет."

async def set_commands(bot: Bot):
    """Автоматически устанавливает список команд в меню Telegram"""
    commands = [
        BotCommand(command="status", description="Показать, кто в голосовых каналах"),
        BotCommand(command="leaderboard",
                   description="Посчитать статистику по клану для выбранного режима игры(анранкед)"),
        BotCommand(command="winrate_teammates",
                   description="Посчитать средний рейтинг со всеми сокланами для выбранного игрока. отключено, на доработке"),
        BotCommand(command="help", description="Показать список команд"),
    ]
    await bot.set_my_commands(commands)

async def start_telegram_bot():
    """Запуск Telegram-бота"""
    print("✅ Запуск Telegram-бота...")
    await set_commands(telegram_bot)  # Устанавливаем команды
    await dp.start_polling(telegram_bot)

# Функция для добавления игрока
def get_or_create_player(session, nickname):
    from models import Player
    player = session.query(Player).filter_by(nickname=nickname).first()

    if player:  # Если игрок уже существует, возвращаем его
        print(f"Игрок {nickname} уже есть в базе.")
        return player

    new_player = Player(nickname=nickname)
    session.add(new_player)
    session.commit()

    print(f"Игрок {nickname} добавлен в базу.")

    return player


# Функция для создания игры (добавлен game_id)
def create_game(session, game_id, result, game_mode, teammate1, teammate2, teammate3):
    from models import Game
    game = Game(game_id=game_id, result=result, game_mode=game_mode, teammate1=teammate1, teammate2=teammate2, teammate3=teammate3)
    session.add(game)
    session.commit()

    return game


# Функция добавления игр игроку (исправлено добавление в player.games)
def add_games_to_player(session, player_nickname, game_id, result, game_mode, teammate1, teammate2, teammate3):
    from models import Game
    flag = 0

    # Получаем или создаём игрока
    player = get_or_create_player(session, player_nickname)

    # Проверяем, есть ли уже такая игра в базе
    game = session.query(Game).filter_by(game_id=game_id).first()

    # Если игра существует, проверяем, привязан ли игрок к ней
    if game:
        for game_api in player.games:
            if game.game_id == game_api.game_id:
                print(f"Игра уже есть у этого игрока {player.nickname}.")
                flag = 1
                return game  # Возвращаем существующую игру
                # Если игры нет в базе, создаём новую

    if flag == 0:
        game = create_game(session, game_id, result, game_mode, teammate1, teammate2, teammate3)
        player.games.append(game)
        print("Игры игрока:", [game.game_id for game in player.games])


    return game  # Возвращаем объект игры

def get_games_by_player_id(session, player_id):
    from models import Player
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print(f"Игрок с ID {player_id} не найден.")
        return []

    return player.games


def get_player_id(session, player_nickname):
    from models import Player
    player = session.query(Player).filter_by(nickname=player_nickname).first()

    if player:
        return player.id  # Возвращаем ID игрока
    else:
        print(f"Игрок {player_nickname} не найден в базе.")
        return None
