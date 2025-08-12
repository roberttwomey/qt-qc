# pygmc examples https://pypi.org/project/pygmc/
# pygmc is a Python client for the GMC API

import pygmc
import pandas as pd

# Connect to the GMC API
gc = pygmc.connect()

ver = gc.get_version()
print(ver)

cpm = gc.get_cpm()
print(cpm)

history = gc.get_history_data()
df = pd.DataFrame(history[1:], columns=history[0])

print(df)