import os
import pandas as pd

file = os.path.expanduser('/data/commenter_dates.csv')
dfcd = pd.read_csv(file)

dfcdr = pd.DataFrame()

dfcdr['time_difference_hrs'] = (pd.to_datetime(dfcd['comment_date']) - pd.to_datetime(dfcd['post_date'])).dt.total_seconds() // 3600
dfcdr['3rd_to_2nd_ratio'] = dfcd['3rd_person_pronoun'] / dfcd['2nd_person_pronoun']

print(dfcdr.head())