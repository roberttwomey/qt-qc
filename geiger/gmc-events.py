# pygmc examples https://pypi.org/project/pygmc/
# pygmc is a Python client for the GMC API

# import pygmc
# import pandas as pd

# # Connect to the GMC API
# gc = pygmc.connect()

# ver = gc.get_version()
# print(ver)

# cpm = gc.get_cpm()
# print(cpm)

# history = gc.get_history_data()
# df = pd.DataFrame(history[1:], columns=history[0])

# print(df)


import pygmc
import time, sys

gc = pygmc.connect()  # Connect to the Geiger counter
last_cps = None

time.sleep(1)  # Allow time for the connection to stabilize

while True:
    current_cps = gc.get_cps()
    # if current_cps != last_cps and current_cps > 0:
    if current_cps > 0:
        # print(f"New count registered: {current_cps} CPS")
        for i in range(current_cps):
            print("+", end=" ")
        sys.stdout.flush()
        last_cps = current_cps
    time.sleep(1)  # Poll every 0.1 seconds for sub-second precision
    # time.sleep(0.1)  # Poll every 0.1 seconds for sub-second precision