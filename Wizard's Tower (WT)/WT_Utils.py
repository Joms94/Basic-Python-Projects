import os
import time
import pandas as pd
from WT_Player import Player


# Loads existing character. Returns a Player object.
def load_character():
    path = os.path.join('wt_savegames.csv')
    try:
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
    except FileNotFoundError:
        with open(os.path.join('wt_savegames.csv'), "w") as file:
            file.seek(0)
            character = ["Merlin", 7, 50, 0, 1]
            file.write(f"{character[0]},{character[1]},{character[2]},{character[3]},{character[4]}")
            file.truncate()


def final_wave_check(wizard):
    if wizard.get_wave() == 31:
        clear_console()
        print("Victory!\n")
        time.sleep(2)
        print(f"\n{wizard.get_name()} has repelled the invasion... but at a terrible cost.")
        time.sleep(4)
        print(f"For too long, generations of wizards and witches have died guarding its secrets.\n")
        time.sleep(4)
        print(f"But now, under the great sorcerer {wizard.get_name()}, peace has come.")
        time.sleep(4)
        print("Unless of course... they wish to provoke ever-greater assaults?\n")
        time.sleep(4)


def view_monsters(path=os.path.join('wt_monster_list.csv')):
    pc = load_character()
    if pc.get_wave() >= 28:
        path = os.path.join('wt_monster_list_4.csv')
    elif pc.get_wave() >= 22:
        path = os.path.join('wt_monster_list_3.csv')
    elif pc.get_wave() >= 10:
        path = os.path.join('wt_monster_list_2.csv')
    monster_table = pd.read_csv(path)
    return monster_table


def encounter_delay(delay=2):
    pc = load_character()
    return time.sleep(round(max(2, (delay+pc.get_wave()))/6))


def game_speed(delay=0.3):
    pc = load_character()
    return time.sleep((0.3 + delay)/pc.get_wave())


def clear_console():
    print('\n' * 150)
