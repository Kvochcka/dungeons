import random


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
