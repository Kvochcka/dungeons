from app.dungeon import Dungeon
from app.player import Player


class Game:
    def __init__(self):
        self.player = None

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
                dungeon = Dungeon()
                for room in dungeon.map:
                    dungeon.handle_room(self.player, room)
                    if not self.player.is_alive():
                        break
            elif choice == "2":
                print("Добро пожаловать в магазин!")
                print("1. Зелье (20 монет)")
                print("2. Свиток исцеления (50 монет)")
                print("3. Выход")
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
                        self.player.inventory.append("свиток")
                        self.player.coins -= 50
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
