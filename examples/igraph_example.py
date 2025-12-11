# %%

from ggplotly import ggplot, aes, geom_edgebundle, data

# Load igraph object
g = data('us_flights')

# Create bundle geom from graph
p = ggplot() + geom_edgebundle(graph=g, verbose=False, C=6, I=50)

p.draw()
# %%
