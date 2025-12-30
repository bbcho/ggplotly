# %%
from ggplotly import *
import pandas as pd

# %%
data()

# %%
df = data('commodity_prices')

# %%
df

# %%
df.date = pd.to_datetime(df.date)

# %%
df

# %%
df = df[df.series == 'CL01'].set_index('date').value

# %%
df

# %%
ggplot(df) + geom_line()
