import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.attack_power = 10
        self.inventory = []
        self.coins = 0

    def attack(self, target):
        damage = random.randint(5, max(self.attack_power, 5))
        print(f"Вы наносите {damage} урона {target.name}.")
        target.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        print(f"{self.name} получает {damage} урона. Осталось здоровья: {self.health}.")

    def is_alive(self):
        return self.health > 0

    def restore_health(self):
        self.health = self.max_health
        print("Здоровье восстановлено до максимального значения.")

    def upgrade_max_health(self, amount):
        self.max_health += amount
        self.health = self.max_health  # восстанавливаем здоровье НО до нового максимума
        print(f"Максимальное здоровье увеличено до {self.max_health}.")


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
            damage = random.randint(5, max(self.attack_power, 5))
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
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.map = [["[]" for _ in range(self.width)] for _ in range(self.height)]
        self.generate_map()

    def generate_map(self):
        # карта
        def place_random(symbol, avoid=(0, 0)):
            while True:
                x, y = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
                if self.map[x][y] == "[]" and (x, y) != avoid:
                    self.map[x][y] = symbol
                    break

        # видимые объекты
        place_random("d", avoid=(0, 0))  # Спуск
        place_random("e")  # = выход из подземелья
        place_random("s")  # = торговец

    def display_map(self, player_position):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if (i, j) == player_position:
                    print("P", end=" ")  # = игрок
                else:
                    print(cell, end=" ")
            print()


class Game:
    def __init__(self):
        self.player = None
        self.dungeon = None

    def run(self):
        name = input("Введите имя вашего персонажа: ")
        self.player = Player(name)
        self.main_menu()

    def main_menu(self):
        while self.player.is_alive():
            print("\n1. Войти в подземелье")
            print("2. Магазин")
            print("3. Выход")
            choice = input("Ваш выбор: ")
            if choice == "1":
                self.enter_dungeon()
            elif choice == "2":
                self.shop()
            elif choice == "3":
                print("До встречи!")
                break
            else:
                print("Неверный ввод.")

    def enter_dungeon(self):
        self.dungeon = Dungeon()  # создаем новое подземелье
        player_position = (0, 0)  # начальная позиция игрока
        while True:
            self.dungeon.display_map(player_position)  # отображаем карту
            print("\nВыберите направление:")
            print("1. Вверх")
            print("2. Вниз")
            print("3. Влево")
            print("4. Вправо")
            print("5. Вернуться в главное меню")
            choice = input("Ваш выбор: ")

            if choice == "1":  # вверх
                new_position = (max(player_position[0] - 1, 0), player_position[1])
            elif choice == "2":  # вниз
                new_position = (min(player_position[0] + 1, self.dungeon.height - 1), player_position[1])
            elif choice == "3":  # влево
                new_position = (player_position[0], max(player_position[1] - 1, 0))
            elif choice == "4":  # вправо
                new_position = (player_position[0], min(player_position[1] + 1, self.dungeon.width - 1))
            elif choice == "5":  # главное меню
                print("Возвращаемся в главное меню...")
                break
            else:
                print("Неверный ввод.")
                continue

            # проверка вероятности появления монстра
            if random.random() < 0.45:  # 45% шанс появления монстра
                monster = random.choice([Goblin(), Dragon(), Skeleton()])
                print(f"Вы встретили {monster.name}!")
                if not self.battle(monster):
                    print("Вы сбежали из боя.")
                    self.player.restore_health()  # восстанавливаем здоровье
                    break  # возвращаемся в главное меню

            # проверка активации ловушки
            if random.random() < 0.3:  # 30% шанс попасть в ловушку
                print("Вы попали в ловушку!")
                damage = random.randint(5, 15)
                self.player.take_damage(damage)

            # Обработка событий на видимых объектах
            event = self.dungeon.map[new_position[0]][new_position[1]]
            if event == "d":
                print("Вы нашли спуск на следующий уровень!")
                self.dungeon = Dungeon()  # генерируем новый уровень
                player_position = (0, 0)  #и сбрасываем позицию игрока
                continue
            elif event == "e":
                print("Вы нашли выход из подземелья!")
                print(f"Вы собрали {self.player.coins} монет. Хотите выйти?")
                if input("1 - Выйти, 2 - Остаться: ") == "1":
                    print("Вы покидаете подземелье с добычей!")
                    break
            elif event == "s":
                print("Вы нашли торговца!")
                self.shop()

            player_position = new_position  # обновляем позицию

            if not self.player.is_alive():
                print("Вы погибли. Игра окончена.")
                break

    def battle(self, monster):
        while self.player.is_alive() and monster.is_alive():
            print("\nВыберите действие:")
            print("1. Атака")
            print("2. Блок")
            print("3. Лечение (зелье)")
            print("4. Сбежать")
            choice = input("Ваш выбор: ")

            if choice == "1":
                self.player.attack(monster)
                if monster.is_alive():
                    monster.attack(self.player)
            elif choice == "2":
                print("Вы блокируете атаку!")
                if random.random() < 0.7:
                    print("Вы успешно заблокировали удар!")
                else:
                    print("Блок провален!")
                    monster.attack(self.player)
            elif choice == "3":
                if "зелье" in self.player.inventory:
                    print("Вы использовали зелье и восстановили 20 здоровья!")
                    self.player.health = min(self.player.health + 20, self.player.max_health)
                    self.player.inventory.remove("зелье")
                else:
                    print("У вас нет зелий!")
            elif choice == "4":
                print("Вы сбежали из боя!")
                return False  # сбегаем, но монстр остается живым
            else:
                print("Неверный выбор!")

            if not monster.is_alive():
                print(f"Вы победили {monster.name} и получили {monster.reward} монет.")
                self.player.coins += monster.reward
                return True  # монстр побежден
            elif not self.player.is_alive():
                print("Вы погибли. Игра окончена.")
                return False

    def shop(self):
        print("Добро пожаловать в магазин!")
        print("1. Зелье (20 монет)")
        print("2. Броня (+40 к здоровью, 50 монет)")
        print("3. Бомба (30 монет)")
        print("4. Выход")
        shop_choice = input("Ваш выбор: ")
        if shop_choice == "1":
            if self.player.coins >= 20:
                self.player.inventory.append("зелье")
                self.player.coins -= 20
                print("Вы купили зелье.")
            else:
                print("Не хватает монет.")
        elif shop_choice == "2":
            if self.player.coins >= 50:
                self.player.upgrade_max_health(40)  #увеличиваем максимальное здоровье
                self.player.coins -= 50
                print("Вы купили броню.")
            else:
                print("Не хватает монет.")
        elif shop_choice == "3":
            if self.player.coins >= 30:
                self.player.inventory.append("бомба")
                self.player.coins -= 30
                print("Вы купили бомбу.")
            else:
                print("Не хватает монет.")
        elif shop_choice == "4":
            pass
        else:
            print("Неверный ввод.")


if __name__ == "__main__":
    game = Game()
    game.run()