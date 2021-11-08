import sys
import pandas as pd
from random import randint
from WT_Player import Player
from WT_Utils import game_speed, clear_console, load_character, final_wave_check, view_monsters, encounter_delay
from WT_Shop import shop_loop


# Creates a wizard. Returns a Player object.
def create_wizard():
    choice = ""
    pc = load_character()
    inheritance = pc.inherit()
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
            quit_game()
        else:
            print("Unrecognised input. Try again.\n")


def menu():
    pc = load_character()
    print(f"What say you, {pc.get_name()}? Wave {pc.get_wave()} awaits!\n1 = Fight!\n2 = Shop!\n3 = Save and quit!\n")
    choice = input()
    return choice


def quit_game():
    pc = load_character()
    if pc.get_health() <= 0:
        print(f"Rest in peace, {pc.get_name()}.")
    if pc.get_health() > 0:
        print(f"Fair winds, {pc.get_name()}!")
    pc.save()
    sys.exit()


# Generates and returns a dataframe of monsters and their attributes.
def generate_encounter():
    clear_console()
    pc = load_character()
    monster_quantity = pc.get_wave()
    if pc.get_wave() == 30:
        monster_quantity = pc.get_wave() * 2
    new_encounter = pd.DataFrame(columns=["Name", "Damage", "Health", "Gold"])
    while len(new_encounter) < monster_quantity:
        new_encounter = new_encounter.append(view_monsters().iloc[randint(0, len(view_monsters())-1)],
                                             ignore_index=True)
    print(f"You encounter:\n {str(new_encounter)}\n")
    new_encounter = new_encounter.sort_values(by=["Gold"], ascending=False)
    new_encounter.reset_index(inplace=True)
    del new_encounter["index"]
    encounter_delay()
    return new_encounter


# Causes all monsters in the encounter table to attack the player.
def opening_attack(pc, current_encounter):
    monster = 0
    while monster < len(current_encounter):
        game_speed()
        print(f"{current_encounter.iloc[monster][0]} attacks {pc.get_name()}!")
        pc.take_damage(randint(0, current_encounter.iloc[monster][1]))
        pc.save()
        monster = monster + 1


# Causes the player to attack the first monster in the encounter table, then returns the updated encounter table.
def player_attack(pc, current_encounter):
    if len(current_encounter) > 0:
        game_speed()
        print(f"{pc.get_name()} attacks {current_encounter.iloc[0][0]}!")
        new_monster_health = current_encounter.iloc[0][2] - randint(0, pc.get_damage())
        print(f"{current_encounter.iloc[0][0]}'s health: {str(new_monster_health)}\n")
        current_encounter.iloc[0][2] = int(new_monster_health)
        current_encounter = monster_death_check(pc, current_encounter)
        return current_encounter
    else:
        pc.save()
        monster_death_check(pc, current_encounter)
        return current_encounter


def player_death_check(pc):
    if pc.get_health() <= 0:
        print(f"{pc.get_name()} has been slain! The bards will sing of their deeds.\n")
        pc.save()


# Causes the first monster in the encounter table to attack the player, then returns the updated encounter table.
def monster_attack(pc, current_encounter):
    if len(current_encounter) > 0:
        game_speed()
        print(f"{current_encounter.iloc[0][0]} attacks {pc.get_name()}!")
        pc.take_damage(randint(0, int(current_encounter.iloc[0][1])))
        return current_encounter
    else:
        pc.save()
        player_death_check(pc)
        game_speed()
        return current_encounter


def monster_death_check(pc, current_encounter):
    if current_encounter.iloc[0][2] <= 0:
        game_speed()
        print(str(current_encounter.iloc[0][0]) + " slain!\n")
        pc.earn_gold(current_encounter.iloc[0][3])
        current_encounter.drop(index=0, axis=0, inplace=True)
        current_encounter.reset_index(inplace=True)
        del current_encounter["index"]
        return current_encounter
    else:
        return current_encounter


def victory_check(pc, current_encounter):
    if len(current_encounter) <= 0 and (pc.get_health() > 0):
        game_speed()
        print("Victory!")
        pc.get_gold()
        pc.increase_wave(1)
        pc.save()


# Main game loop.
menu_choice = " "
print(f"\nFoes besiege your tower. Survive to the end of wave 30 to exhaust their might!")
while True:
    wizard = create_wizard()
    if wizard.get_health() <= 0:
        print(f"Alas! {wizard.get_name()} did not survive the last skirmish. Who will avenge them?")
    while wizard.get_health() > 0:
        final_wave_check(wizard)
        menu_choice = menu()
        if wizard.get_health() > 0:
            if menu_choice == "1":
                encounter = generate_encounter()
                opening_attack(wizard, encounter)
                while len(encounter) > 0:
                    if wizard.get_health() <= 0:
                        player_death_check(wizard)
                        break
                    encounter = player_attack(wizard, encounter)
                    encounter = monster_attack(wizard, encounter)
                    victory_check(wizard, encounter)
            if menu_choice == "2":
                player_death_check(wizard)
                while True:
                    try:
                        shop_loop(wizard)
                        wizard.get_stats()
                        wizard.save()
                    except AttributeError:
                        wizard.save()
                        break
            if menu_choice == "3":
                quit_game()
