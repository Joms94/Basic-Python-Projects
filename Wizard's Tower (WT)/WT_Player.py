import pandas as pd
import os


class Player(object):
    def __init__(self, name="Merlin", damage=7, health=50, gold=0, wave_no=1):
        self.name = name
        self.damage = round(damage)
        self.health = round(health)
        self.gold = round(gold)
        self.wave_no = round(wave_no)

    def take_damage(self, damage_taken=0):
        self.health = self.health - damage_taken
        self.save()
        print(f"{self.name}'s health: {str(self.health)}\n")
        return self.health

    def gain_stats(self, damage_gained=0, health_gained=0):
        self.damage = self.damage + damage_gained
        self.health = self.health + health_gained
        return self.health, self.damage

    def gain_health(self, health_gained=0):
        self.health = self.health + health_gained
        return self.health

    def gain_damage(self, damage_gained=0):
        self.damage = self.damage + damage_gained
        return self.damage

    def earn_gold(self, gold_earned=0):
        self.gold = self.gold + gold_earned
        self.save()

    def lose_gold(self, gold_lost=0):
        self.gold = self.gold - gold_lost

    def get_stats(self):
        stats = pd.DataFrame(data={"Max Hit": self.damage,
                                   "Health": self.health,
                                   "Gold": self.gold,
                                   "Wave": self.wave_no},
                             index=[0]).to_string(index=False)
        print(stats)
        return stats

    def get_name(self):
        return self.name

    def get_damage(self):
        return self.damage

    def get_health(self):
        return int(self.health)

    def get_gold(self):
        print(f"{self.name} now has {self.gold} gold.")

    def return_gold(self):
        return int(self.gold)

    def inherit(self):
        return round(int(self.gold/2))

    def get_wave(self):
        return self.wave_no

    def increase_wave(self, increment=1):
        self.wave_no = self.wave_no + increment
        return self.wave_no

    def save(self, path=os.path.join('wt_savegames.csv')):
        with open(path, "w") as file:
            file.seek(0)
            file.write(str(self.name) + "," + str(self.damage)+"," + str(self.health) + ","
                       + str(self.gold)+"," + str(self.wave_no) + "\n")
            file.truncate()
