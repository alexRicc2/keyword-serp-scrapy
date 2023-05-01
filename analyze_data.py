import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

pageSpeed_df = pd.read_csv('PS_scores.csv')

# display(pageSpeed_df.head())
print(pageSpeed_df) #display the entire dataframe