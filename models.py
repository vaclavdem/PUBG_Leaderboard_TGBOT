class Teammate():
    def __init__(self, nickname):
        self.nickname = nickname

class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.games_id = []
        self.teammates = []

    def add_teammate(self, teammate):
        if isinstance(teammate, Teammate):
            self.teammates.append(teammate)
        else:
            print("Ошибка: добавляемый объект не является тиммейтом!")