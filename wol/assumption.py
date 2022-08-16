import pandas as pd


assumption = dict()
assumption["mortality"] = pd.read_csv("./input/mortality.csv")
assumption["interest_rates"] = pd.read_csv("./input/interest_rates.csv")
