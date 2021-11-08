# world_pop_scraper.py
This grabs the top 10 countries by population from Wikipedia and puts them in a column chart. A simple exercise for becoming more familiar with http requests and pandas plots.

pop_scraper navigates to the relevant wikipedia page, looks for the right table, then for every row, puts each cell into a dataframe.
Extraneous characters are then stripped from the population column so they can be more easily read as integers rather than strings in pop_graph.

pop_graph creates the graph with the parameters I've arbitrarily decided look OK. 

That's it!
