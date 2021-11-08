# Goal: extract information on top 10 most populous countries, then put them into a bar or column chart.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


def pop_scraper():
    link = "https://en.wikipedia.org/wiki/World_population"
    population_html = requests.get(link).text
    pop_soup = BeautifulSoup(population_html, "html.parser")
    country_frame = pd.DataFrame(columns=["Country", "Population", "% of World", "Last Update"])
    for row in pop_soup.find_all("tbody")[4].find_all("tr")[1:]:
        col = row.find_all("td")
        country = col[0]
        population = col[1]
        pct_world = col[2]
        date = col[3]
        country_frame = country_frame.append(
            {"Country": country.text, "Population": population.text,
             "% of World": pct_world.text, "Last Update": date.text},
            ignore_index=True)
    country_frame["Population"] = country_frame["Population"].str.replace(',|\$',"").str.strip().astype("int64")
    return country_frame


def pop_graph(pop_dataframe):
    data = pop_dataframe
    graph = data.plot.bar(x="Country", y="Population", figsize=(18, 10), rot=0, color="red")
    graph.set_title("Top 10 Countries by Population", fontdict={'fontsize': 23})
    graph.set_xlabel("Country", fontdict={'fontsize': 15})
    graph.set_ylabel("Population (Billions)", fontdict={'fontsize': 15})
    plt.show()


if __name__ == '__main__':
    pop_graph(pop_scraper())
