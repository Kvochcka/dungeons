import random


class Room:
    """
    ###### #####
    #          #
    ### ########
    """

    def __init__(self, enter_num: int = None):
        self.length = 12
        self.enter_num = enter_num or random.randint(1, self.length - 2)
        self.exit_num = random.randint(1, self.length - 2)

    def build_next(self) -> 'Room':
        return Room(self.exit_num)

    def show(self):
        for i in range(self.length):
            if i == self.enter_num:
                print(' ', end='')
            else:
                print('#', end='')

        print('\n#', end='')
        for i in range(self.length - 2):
            print(' ', end='')
        print('#\n', end='')

        for i in range(self.length):
            if i == self.exit_num:
                print(' ', end='')
            else:
                print('#', end='')
        print()

    def __str__(self):
        return f'length: {self.length}, enter_num: {self.enter_num}, exit_num: {self.exit_num}'


class Dungeon:
    """
    ###### #####
    #          #
    ### ########
    ### ########
    #          #
    ######## ###
    ######## ###
    #          #
    ### ########
    ### ########
    #          #
    ##### ## ###
    """

    # NEW CODE
    def __init__(self):
        self.level = 0
        self.map = [Room()]

    # NEW CODE
    def change_level(self, up: bool):
        if up:
            if self.level == 0:
                raise
            self.level -= 1
        else:
            if self.level == len(self.map) - 1:
                current_room = self.map[self.level]
                self.map.append(current_room.build_next())

            self.level += 1

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