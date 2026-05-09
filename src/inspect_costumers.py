import pandas as pd

customers = pd.read_csv("data/raw/olist/olist_customers_dataset.csv")

print(customers.head())
print(customers.shape)
print(customers.columns)
print(customers.dtypes)