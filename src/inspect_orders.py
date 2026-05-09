import pandas as pd

order = pd.read_csv("data/raw/olist/olist_orders_dataset.csv")

print(order.head())
print(order.info())
print(order.shape)
print(order.columns)
print(order.dtypes)