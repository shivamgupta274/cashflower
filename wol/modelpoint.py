import pandas as pd

from cashflower import ModelPoint

policy = ModelPoint(name="policy", data=pd.read_csv("./input/policy_1000.csv"))
