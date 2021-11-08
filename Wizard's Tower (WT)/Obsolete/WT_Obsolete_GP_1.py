from random import randint
import pandas as pd
from WT_Monsters import view_monsters
from WT_Player import Player
from WT_Items import Item, HealthItem, ManaItem
import time
import sys


# Loads existing character. Returns a Player object.
def load_character():
    path = "D:\Personal\Education\Programming\Projects\Wizard's Tower (WT)\wt_savegames.csv"
    with open(path, "r") as file:
        file.seek(0)
        stats = file.readline().split(",")
        loaded_character = Player(
                    name=stats[0],
                    damage=int(stats[1]),
                    health=int(stats[2]),
                    gold=int(stats[3]),
                    wave_no=int(stats[4].strip()))
        return loaded_character


# Creates a wizard. Returns a Player object.
def create_wizard(inheritance=0):
    choice = ""
    while choice != "1" or "2":
        print("1 = Create wizard\n2 = Load wizard\n3 = Quit\n")
        choice = input()
        if choice == "1":
            print("Hail, wizard! Choose a name.\n")
            pc = Player(name=input())
            if inheritance >= 1:
                print(f"Your predecessor left you {inheritance} gold.\n")
                pc.earn_gold(gold_earned=inheritance)
                pc.save()
                return pc
            else:
                pc.save()
                return pc
        if choice == "2":
            pc = load_character()
            return pc
        if choice == "3":
            pc = load_character()
            pc.save()
            print(f"Fair winds, {pc.get_name()}!")
            sys.exit()
        else:
            print("Unrecognised input. Try again.\n")


# Offers the choice of fighting or going to the shop.
# 1 initiates a battle. 2 opens the shop.
def menu(pc=Player()):
    death_check()
    print(f"What say you, {pc.get_name()}? Wave {pc.get_wave()} awaits!\n1 = Fight!\n2 = Shop!\n3 = Save and quit!\n")
    choice = input()
    return choice


def clear_console():
    print('\n' * 150)


# Gives players the chance to buy items.
def display_items(pc=load_character()):
    print(f"{pc.get_name()} has {pc.return_gold()} gold.")
    purchase = ""
    while purchase != "exit":
        health_potion = HealthItem()
        mana_potion = ManaItem()
        sun_elixir = HealthItem(name="Sun King Elixir",
                                description=f"+{round(pc.return_gold()/2)} Health",
                                price=pc.return_gold(),
                                effect=(round(pc.return_gold()/2)))
        naramsin_elixir = ManaItem(name="Naram-Sin Elixir",
                                   description=f"+{round(pc.return_gold()/20)} Damage",
                                   price=pc.return_gold(),
                                   effect=(round(pc.return_gold()/20)))
        item_frame = pd.DataFrame(zip(health_potion.attrs(),
                                      mana_potion.attrs(),
                                      sun_elixir.attrs(),
                                      naramsin_elixir.attrs())).swapaxes("index", "columns")
        item_frame.columns = ["Item", "Description", "Cost"]
        item_frame.index += 1
        shop_dialogue = f"\nPurchase an item by typing the number to its left.\nExit the shop with 'enter'.\n\n{item_frame}\n"
        print(shop_dialogue)
        purchase = input()
        if purchase == "1":
            clear_console()
            health_potion.buy(pc, pc.return_gold())
            pc.save()
        elif purchase == "2":
            clear_console()
            mana_potion.buy(pc, pc.return_gold())
            pc.save()
        elif purchase == "3":
            clear_console()
            sun_elixir.buy(pc, pc.return_gold())
            pc.save()
        elif purchase == "4":
            clear_console()
            naramsin_elixir.buy(pc, pc.return_gold())
            pc.save()
        elif purchase == "":
            pc.save()
            break
        else:
            clear_console()
            print("Invalid input")
            print(shop_dialogue)


def purchase_item(item, pc=load_character()):
    clear_console()
    item.buy(pc, pc.return_gold())
    pc.save()


def game_speed(delay=0.02):
    return time.sleep(delay)


# Generates a dataframe of monsters and their attributes.
# Gets attributes from a csv file (accessed with view_monsters()).
def generate_encounter(monster_quantity=1):
    clear_console()
    encounter = pd.DataFrame(columns=["Name", "Damage", "Health", "Gold"])
    while len(encounter) < monster_quantity:
        encounter = encounter.append(view_monsters().iloc[randint(0, len(view_monsters())-1)], ignore_index=True)
    print(f"You encounter:\n {str(encounter)}\n")
    encounter = encounter.sort_values(by=["Gold"], ascending=False)
    encounter.reset_index(inplace=True)
    del encounter["index"]
    return encounter


def death_check(pc=load_character()):
    if pc.get_health() <= 0:
        clear_console()
        print(f"{pc.get_name()} has departed this world. Will their apprentice replace them?")
        inheritance = pc.inherit()
        return inheritance


# Handles player death, monster death, or ends the battle if no monsters remain in the encounter table.
def cleanup(current_encounter):
    pc = load_character()
    try:
        if pc.get_health() <= 0:
            print(f"{pc.get_name()} has been slain! The bards will sing of their deeds.\n")
            pc.save()
            create_wizard(pc.inherit())
        if current_encounter is None:
            pc.save()
            menu(pc)
        # Distributes gold to the player after killing a monster, then drops the monster from the encounter table.
        if current_encounter is not None:
            if current_encounter.iloc[0][2] <= 0:
                game_speed()
                print(str(current_encounter.iloc[0][0]) + " slain!\n")
                pc.earn_gold(current_encounter.iloc[0][3])
                current_encounter.drop(index=0, axis=0, inplace=True)
                current_encounter.reset_index(inplace=True)
                del current_encounter["index"]
                pc.save()
            if len(current_encounter) <= 0:
                pc.get_gold()
                pc.increase_wave(1)
                pc.save()
                menu(pc)
    except RecursionError:
        print("A recursion error occurred during the cleanup sequence.")
        pc.save()
        sys.exit()
    except IndexError:
        pc.save()
        pass


def begin_battle(current_encounter):
    pc = load_character()
    game_speed(2)
    try:
        monster = 0
        while monster < len(current_encounter):
            game_speed(0.1)
            print(f"{current_encounter.iloc[monster][0]} attacks {pc.get_name()}!")
            pc.take_damage(randint(0, current_encounter.iloc[monster][1]))
            cleanup(current_encounter)
            pc.save()
            monster = monster + 1
    except RecursionError:
        print("A recursion error occurred during the begin battle sequence.")
        pc.save()
        sys.exit()
    finally:
        return current_encounter


def player_attack(current_encounter):
    pc = load_character()
    death_check()
    game_speed()
    try:
        cleanup(current_encounter)
        print(f"{pc.get_name()} attacks {current_encounter.iloc[0][0]}!")
        new_monster_health = current_encounter.iloc[0][2] - randint(0, pc.get_damage())
        print(f"{current_encounter.iloc[0][0]}'s health: {str(new_monster_health)}\n")
        current_encounter.iloc[0][2] = int(new_monster_health)
        cleanup(current_encounter)
        return current_encounter
    except RecursionError:
        print("A recursion error occurred during the player attack sequence.")
        pc.save()
        sys.exit()
    except IndexError:
        pass


def monster_attack(current_encounter):
    pc = load_character()
    death_check()
    game_speed()
    try:
        cleanup(current_encounter)
        print(f"{current_encounter.iloc[0][0]} attacks {pc.get_name()}!")
        pc.take_damage(randint(0, int(current_encounter.iloc[0][1])))
        pc.save()
        cleanup(current_encounter)
    except RecursionError:
        print("A recursion error occurred during the monster attack sequence.")
        pc.save()
        sys.exit()
    except IndexError:
        pass


while True:
    wizard = create_wizard()
    menu(wizard)
    battle = begin_battle(generate_encounter(wizard.get_wave()))
    while battle is not None:
        monster_attack(player_attack(battle))
