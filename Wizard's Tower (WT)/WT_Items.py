from random import randint
import pandas as pd
from WT_Player import Player
from WT_Utils import load_character


class Item(object):
    def __init__(self, name="Unknown Concoction", description="?", price=10, effect=None):
        self.name = name
        self.description = description
        self.price = price
        self.effect = effect

    def get_name(self):
        return self.name

    def get_price(self):
        return int(self.price)

    def get_effect(self):
        return self.effect

    def get_all(self):
        att_list = [self.name,
                    self.description,
                    self.price,
                    self.effect]
        return att_list

    def attrs(self):
        att_list = [self.name,
                    self.description,
                    self.price]
        return att_list

    def buy(self, pc, gold):
        if self.price > gold:
            print(f"Not enough gold. You only have {pc.return_gold()}.")
        else:
            pc.lose_gold(self.price)
            pc.gain_stats(*self.get_effect())
            print(f"{self.get_name()} purchased. {pc.get_name()} has {pc.return_gold()} gold remaining.")


pc = load_character()
health_potion = Item(name="Health Potion",
                     description="+30 Health",
                     price=20,
                     effect=[0, 30])
mana_potion = Item(name="Mana Potion",
                   description="+2 Damage",
                   price=15,
                   effect=[2, 0])
sun_elixir = Item(name="Sun King Elixir",
                  description="+400 Health",
                  price=200,
                  effect=[0, 400])
sin_elixir = Item(name="Naram-Sin Elixir",
                  description="+15 Damage",
                  price=200,
                  effect=[15, 0])
