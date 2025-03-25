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
from settings import api_1, api_2, Base, engine, session
from sqlalchemy import text
from functions import get_or_create_player

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
    result = Column(Integer, default=0)
    game_mode = Column(String(100), nullable=False)
    teammate1 = Column(String(50))
    teammate2 = Column(String(50))
    teammate3 = Column(String(50))

    players = relationship("Player", secondary=game_players, back_populates="games")

    def __repr__(self):
        return f"Game(id={self.id}, game_id='{self.game_id}', result='{self.result}')"


# Создание таблиц
Base.metadata.create_all(engine)

nicknames = [
    'oran_gg_e', 'ol1vOCHKA', 'TexasDolly', 'magichka_nuar', 'Shafi_____',
    'B1mBOSS', 'karma-__-', 'kuatkamiev', 'TechnicolorBlack', 'ClickMer',
    'CougarHex', 'EV0Like', 'freaky_slider', 'General-L1', 'Glenn_ufa',
    'Kingjulyen', 'levirran', 'lillypillyhell', 'Luka_Shymkent', 'maksason14',
    'MIKHAILB9', 'Nikita_Kotov17', 'Rengoku1237', 'Romzes19', 'Ryukbtww',
    'Shelby_Young', 'TaLiCmAn4IK', 'telnoter', 'tOKAE-v', 'TSARrrr',
    'vazgenxer', 'wii663', 'Zef1r_off', 'ZLOY_PISUN', 'ZRideR59',
    'zZzAlexXxzZz', 'Meehoa', 'S0XFATEEV', "roychigevarro", "stabyly2",
    "Esay_Sqezy", "Niigagay", "LeshkaALT", "STITCH_KZ"
]

for nickname in nicknames:
    get_or_create_player(session, nickname)



session.commit()  # Финальный коммит
