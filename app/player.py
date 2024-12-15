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
