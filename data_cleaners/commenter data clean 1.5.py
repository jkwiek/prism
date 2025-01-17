import os
import pandas as pd

#import user names
user_names = '~/PycharmProjects/prism-tiktok-post/data/user_names.csv'
dfu = pd.read_csv(user_names)

#creating url based on username
dfu['url'] = "https://www.tiktok.com/@" + dfu['Text'].astype(str)

#exporting url to be processed by octoparse
dfu['url'].to_csv('commenter_urls.csv', index=False)