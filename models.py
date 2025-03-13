from chicken_dinner.pubgapi import PUBGCore
from chicken_dinner.pubgapi import PUBG
from pubg_python import PUBG, Shard
import pubg_python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum
from settings import api_key
from chicken_dinner.pubgapi import PUBG
from settings import api_1, api_2


# Подключение к MySQL
DATABASE_URL = "mysql+mysqlconnector://Vatslav:Va_12345678@localhost/PUBG_db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Таблица "многие ко многим"
game_players = Table(
    'game_players', Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id'), primary_key=True),
    Column('player_id', Integer, ForeignKey('players.id'), primary_key=True)
)


# Перечисление результатов игры
class GameResult(enum.Enum):
    win = "win"
    lose = "lose"
    draw = "draw"


# Модель игрока
class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)

    games = relationship("Game", secondary=game_players, back_populates="players")

    def __repr__(self):
        return f"Player(id={self.id}, nickname='{self.nickname}')"


# Модель игры
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    game_id = Column(String(100), nullable=False)  # Исправлено на String
    result = Column(String(100), nullable=False)
    game_mode = Column(String(100), nullable=False)
    teammate1 = Column(String(50))
    teammate2 = Column(String(50))
    teammate3 = Column(String(50))

    players = relationship("Player", secondary=game_players, back_populates="games")

    def __repr__(self):
        return f"Game(id={self.id}, game_id='{self.game_id}', result='{self.result.name}')"


# Создание таблиц
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()


# Функция для добавления игрока
def get_or_create_player(session, nickname):
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
    game = Game(game_id=game_id, result=result, game_mode=game_mode, teammate1=teammate1, teammate2=teammate2, teammate3=teammate3)
    session.add(game)
    session.commit()

    return game


# Функция добавления игр игроку (исправлено добавление в player.games)
def add_games_to_player(session, player_nickname, game_id, result, game_mode, teammate1, teammate2, teammate3):
    # Получаем или создаём игрока
    player = get_or_create_player(session, player_nickname)

    # Проверяем, есть ли уже такая игра в базе
    game = session.query(Game).filter_by(game_id=game_id).first()

    # Если игра существует, проверяем, привязан ли игрок к ней
    if game:
        if player in game.players:
            print(f"Игра уже есть у этого игрока {player.nickname}.")
            return game  # Возвращаем существующую игру
    else:
        # Если игры нет в базе, создаём новую
        game = create_game(session, game_id, result, game_mode, teammate1, teammate2, teammate3)
        player.games.append(game)

    return game  # Возвращаем объект игры

def get_games_by_player_id(session, player_id):
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print(f"Игрок с ID {player_id} не найден.")
        return []

    return player.games


def get_player_id(session, player_nickname):
    player = session.query(Player).filter_by(nickname=player_nickname).first()

    if player:
        return player.id  # Возвращаем ID игрока
    else:
        print(f"Игрок {player_nickname} не найден в базе.")
        return None

nicknames = [
    "oran_gg_e", "ol1vOCHKA", "TexasDolly", "magichka_nuar", "Shafi_____", "B1mBOSS",
    "karma-__-", "kuatkamiev", "TechnicolorBlack", "ClickMer", "CougarHex", "EV0Like",
    "freaky_slider", "General-L1", "Glenn_ufa", "Kingjulyen", "levirran", "lillypillyhell",
    "Luka_Shymkent", "maksason14", "MIKHAILB9", "Nikita_Kotov17", "Rengoku1237", "Romzes19",
    "Ryukbtww", "Shelby_Young", "TaLiCmAn4IK", "telnoter", "tOKAE-v", "TSARrrr",
    "vazgenxer", "wii663", "Zef1r_off", "ZLOY_PISUN", "ZRideR59", "zZzAlexXxzZz",
    "Meehoa", "S0XFATEEV"
]

for nickname in nicknames:
    get_or_create_player(session, nickname)



session.commit()  # Финальный коммит
