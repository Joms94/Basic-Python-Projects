import pandas as pd
from WT_Player import Player
from WT_Items import Item, health_potion, mana_potion, sun_elixir, sin_elixir
from WT_Utils import clear_console, load_character


items = [health_potion.attrs(),
         mana_potion.attrs(),
         sun_elixir.attrs(),
         sin_elixir.attrs()]
items_all_attrs = [health_potion.get_all(),
                   mana_potion.get_all(),
                   sun_elixir.get_all(),
                   sin_elixir.get_all()]


def display_items():
    print(f"\nPurchase an item by typing the number to its left.\nExit the shop with any other key.\n")
    shop = pd.DataFrame(data=items, columns=["Item", "Description  ", "Price"])
    full_attrs_shop = pd.DataFrame(data=items_all_attrs, columns=["Item", "Description  ", "Price", "Effect"])
    shop.index += 1
    print(shop)
    return full_attrs_shop


def item_choice(full_attrs_shop):
    choice_no = input("\n")
    try:
        chosen_item = Item(name=full_attrs_shop.iloc[int(choice_no)-1][0],
                           description=full_attrs_shop.iloc[int(choice_no)-1][1],
                           price=full_attrs_shop.iloc[int(choice_no)-1][2],
                           effect=full_attrs_shop.iloc[int(choice_no)-1][3])
        return chosen_item
    except ValueError:
        pass
    except IndexError:
        pass


def purchase_item(pc, item):
    clear_console()
    item.buy(pc, pc.return_gold())
    pc.save()


def shop_loop(wizard):
    purchase_item(wizard, item_choice(display_items()))
