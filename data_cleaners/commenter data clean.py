import os
import pandas as pd
import numpy as np

#open data file
file = os.path.expanduser('/data/commenters.csv')
dfc = pd.read_csv(file)

dfc['3rd_to_2nd_ratio'] = dfc['3rd_person_pronoun'] / dfc['2nd_person_pronoun']

dfc['search_url'] = "www.tiktok.com/search/user?lang=en&q=" + dfc['comment_person'].astype(str)
dfc['search_url'].to_csv('almost_url.csv', index=False)




