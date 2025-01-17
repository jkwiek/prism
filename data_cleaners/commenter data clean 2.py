import os
import pandas as pd

#import user names
user_names = os.path.expanduser('~/PycharmProjects/prism-tiktok-post/user_names.csv')
dfu = pd.read_csv(user_names)

#creating url based on username
dfc['url'] = "www.tiktok.com/@" + dfu['field'].astype(str) + "?lang=en"

#exporting url to be processed by octoparse
dfc['url'].to_csv('commenter_urls.csv', index=False)


#importing username data from octoparse

commenter_pro_file = os.path.expanduser('~/PycharmProjects/prism-tiktok-post/commenters_profiles.csv')
dfcp = pd.read_csv(commenter_pro_file)

number_of_posts = dfcp.groupby('url').size()

dfcp = dfcp.groupby('url', as_index=False).agg({
    'following':'first',
    'followers': 'first',
    'is_verified': 'first',
    'post_date': 'last',
    'avg_like_num':'mean',
    'avg_comment_num': 'mean',
    'avg_views_num': 'mean',

})

number_of_posts = number_of_posts.reset_index(drop=True)

dfcp['number_of_posts'] = number_of_posts

dfcp['follower_to_following_ratio'] = dfcp['followers'] / dfcp['following']

merged_dfc = pd.merge(dfc, dfcp, how='inner', left_index=True, right_index=True)

#export is_verified column (qualitative)

merged_dfc[['is_verified','2nd_person_pronoun','3rd_person_pronoun']].to_csv('verified_commenters.csv', index=False)





