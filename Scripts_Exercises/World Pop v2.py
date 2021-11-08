# Goal: extract information on top 10 most populous countries, then put them into a bar or column chart.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


def population_scraper():
    link = "https://en.wikipedia.org/wiki/World_population"
    population_html = requests.get(link).text
    pop_soup = BeautifulSoup(population_html, "html.parser")
    info_list = []
    for i, row in enumerate(pop_soup.find_all("tbody")[4].find_all("tr")):
        col = row.find_all("td")
        for x, cell in enumerate(col):
            info_list.append(cell.text)
    keys = info_list[::5]


if __name__ == '__main__':
    population_scraper()
