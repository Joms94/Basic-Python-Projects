from random import randint
import pandas as pd


class Monster(object):
    def __init__(self, name="Shapeless Beast", damage=2, health=5, gold=2):
        self.name = name
        self.damage = damage
        self.health = health
        self.gold = gold

    def power_up(self, multiplier=1):
        self.name = "Savage " + self.name
        self.damage = self.damage * multiplier
        self.health = self.health * multiplier
        self.gold = self.gold * multiplier

    def display_attributes(self):
        attribute_dictionary = {self.name: [self.damage, self.health, self.gold]}
        return attribute_dictionary

    def save(self, path="D:\Personal\Education\Programming\Projects\Wizard's Tower (WT)\wt_monster_list.csv"):
        with open(path, "a") as file:
            file.write(str(self.name)+","+str(self.damage)+","+str(self.health)+","+str(self.gold)+"\n")


def view_monsters(path="D:\Personal\Education\Programming\Projects\Wizard's Tower (WT)\wt_monster_list.csv"):
    monster_table = pd.read_csv(path)
    return monster_table


def create_monster(name="Shapeless Beast", damage=2, health=5, gold=2):
    created_monster = Monster(name, damage, health, gold)
    created_monster.save()
