import random


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 10
        self.inventory = []
        self.coins = 0

    def attack(self, target):
        damage = random.randint(5, self.attack_power)
        print(f"Вы наносите {damage} урона {target.name}.")
        target.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} получает {damage} урона. Осталось здоровья: {self.health}.")

    def is_alive(self):
        return self.health > 0


class Monster:
    def __init__(self, name, health, attack_power, miss_chance, reward):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.miss_chance = miss_chance
        self.reward = reward

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} получает {damage} урона. Осталось здоровья: {self.health}.")

    def attack(self, target):
        if random.random() > self.miss_chance:
            damage = random.randint(5, self.attack_power)
            print(f"{self.name} наносит {damage} урона {target.name}.")
            target.take_damage(damage)
        else:
            print(f"{self.name} промахивается!")

    def is_alive(self):
        return self.health > 0


class Goblin(Monster):
    def __init__(self):
        super().__init__("Гоблин", health=15, attack_power=3, miss_chance=0.3, reward=10)


class Dragon(Monster):
    def __init__(self):
        super().__init__("Дракон", health=75, attack_power=10, miss_chance=0.1, reward=100)


class Skeleton(Monster):
    def __init__(self):
        super().__init__("Скелет", health=25, attack_power=5, miss_chance=0.2, reward=20)


class Dungeon:
    def __init__(self):
        self.level = 1
        self.map = self.generate_map()

    def generate_map(self):
        return [random.choice(["[]", "m", "t"]) for _ in range(5)]

    def handle_room(self, player, room):
        if room == "d":
            print("Вы нашли спуск на новый уровень!")
            self.level += 1
            self.map = self.generate_map()
        elif room == "e":
            print("Выход из подземелья. Возвращаемся в главное меню.")
            main_menu(player)
        elif room == "[]":
            if random.random() < 0.5:
                monster = random.choice([Goblin(), Dragon(), Skeleton()])
                print(f"Вы встретили {monster.name}!")
                self.battle(player, monster)
            else:
                print("Комната пуста.")
        elif room == "m":
            print("Вы вступаете в бой с монстром!")
            monster = random.choice([Goblin(), Skeleton()])
            self.battle(player, monster)
        elif room == "t":
            print("Вы попали в ловушку!")
            damage = random.randint(5, 15)
            player.take_damage(damage)

    def battle(self, player, monster):
        while player.health > 0 and monster.is_alive():
            print("\nВыберите действие:")
            print("1. Атака")
            print("2. Блок")
            print("3. Лечение")
            print("4. Сбежать")
            choice = input("Ваш выбор: ")

            if choice == "1":
                player.attack(monster)
                if monster.is_alive():
                    monster.attack(player)
            elif choice == "2":
                print("Вы блокируете атаку!")
                if random.random() < 0.7:
                    print("Вы успешно заблокировали удар!")
                else:
                    print("Блок провален!")
                    monster.attack(player)
            elif choice == "3":
                if "зелье" in player.inventory:
                    print("Вы использовали зелье и восстановили 20 здоровья!")
                    player.health = min(player.health + 20, 100)
                    player.inventory.remove("зелье")
                else:
                    print("У вас нет предметов для лечения!")
            elif choice == "4":
                print("Вы сбежали из боя.")
                return
            else:
                print("Неверный выбор!")
        if not monster.is_alive():
            print(f"Вы победили {monster.name} и получили {monster.reward} монет.")
            player.coins += monster.reward
        elif player.health <= 0:
            print("Вы погибли. Игра окончена.")


def main_menu(player):
    while player.is_alive():
        print("\n1. Войти в подземелье")
        print("2. Магазин")
        print("3. Выход")
        choice = input("Ваш выбор: ")
        if choice == "1":
            dungeon = Dungeon()
            for room in dungeon.map:
                dungeon.handle_room(player, room)
                if not player.is_alive():
                    break
        elif choice == "2":
            print("Добро пожаловать в магазин!")
            print("1. Зелье (20 монет)")
            print("2. Свиток исцеления (50 монет)")
            print("3. Выход")
            shop_choice = input("Ваш выбор: ")
            if shop_choice == "1":
                if player.coins >= 20:
                    player.inventory.append("зелье")
                    player.coins -= 20
                    print("Вы купили зелье.")
                else:
                    print("Не хватает монет.")
            elif shop_choice == "2":
                if player.coins >= 50:
                    player.inventory.append("свиток")
                    player.coins -= 50
                    print("Вы купили свиток.")
                else:
                    print("Не хватает монет.")
            elif shop_choice == "3":
                pass
            else:
                print("Неверный ввод.")
        elif choice == "3":
            print("До встречи!")
            break
        else:
            print("Неверный ввод.")


name = input("Введите имя вашего персонажа: ")
player = Player(name)
main_menu(player)