class Character:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.health = 100
        self.strength = 10
        self.coins = 50
        self.inventory = []
    def buy_item(self, item):
        # покупка предмета, если хватает монет
        pass

    def take_damage(self, damage):
        # уменьшение здоровья при атаке
        pass

    def attack(self, target):
        # Атака монстра
        pass

class Monster:
    def __init__(self, name, health, attack_power, miss_chance, reward):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.miss_chance = miss_chance
        self.reward = reward

    def take_damage(self, damage):
        # уменьшение здоровья монстра при атаке
        pass

    def attack(self, target):
        # атака на игрока
        pass

    def is_alive(self):
        # проверка, жив ли монстр
        pass

class Dungeon:
    def __init__(self):
        self.rooms = self.create_dungeon()

    def create_dungeon(self):
        # создание подземелья с помощью генераторов и рекурсии
        pass

    def enter_room(self, player, room):
        # логика входа в комнату, сражения с монстрами и нахождения сокровищ
        pass

class Item:
    def __init__(self, name, type, effect, cost):
        self.name = name
        self.type = type
        self.effect = effect
        self.cost = cost

    def use(self, target):
        # применение эффекта предмета
        pass