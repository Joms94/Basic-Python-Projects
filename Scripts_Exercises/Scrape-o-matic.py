from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

path = os.path.join("Civilisation Winrates (Arabia, 1250 - 1650 ELO).txt")
page = requests.get("https://aoestats.io/map/arabia/RM_1v1/1250-1650").text
soup = BeautifulSoup(page, "html.parser")
civs = soup.find_all("tr")
rate_list = []
for i, civ in enumerate(civs):
    cells = civ.find_all("td")
    for j, cell in enumerate(cells):
        rate_list.append(cell.text)

civs_only = (rate_list[::3])
rates_only = (rate_list[1::3])
play_only = (rate_list[2::3])
civ_dictionary = dict(zip(civs_only, zip(rates_only, play_only)))

winrate_table = pd.DataFrame(civ_dictionary).swapaxes("index", "columns").sort_values(by=0, ascending=False)
winrate_table.columns = ["Win-rate", "Play-rate"]
print(winrate_table)

with open(path, "w") as file:
    file.seek(0)
    file.write(str(winrate_table))
    file.truncate()
    print("\nWin-rates updated successfully!")
