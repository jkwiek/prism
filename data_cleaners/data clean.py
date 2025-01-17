import os
import pandas as pd
import numpy as np

#open data file
file_paths = [
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos.csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(1).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(2).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(3).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(4).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(5).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(6).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(7).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(8).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(9).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(10).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(11).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(12).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(13).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(14).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(15).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(16).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(17).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(18).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(19).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(20).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(21).csv',
    '~/PycharmProjects/prism-tiktok-post/data/videos/videos(22).csv'
]

# Read all CSV files into a list of DataFrames
dfs = [pd.read_csv(file) for file in file_paths]

# Concatenate all DataFrames into one
df_orig = pd.concat(dfs, ignore_index=True)

df_orig.drop_duplicates(keep='first', inplace=True)



#drop unnecessary data columns
columns_to_drop = [ 'content', 'hashtag', 'covers_url', 'video_download', 'video_id', 'music_name','music_author', 'music_URL', 'comment_likes', 'reply_num']
df=df_orig.drop(columns=columns_to_drop)

#create 2nd:3rd person comment ratio

second_person_pronouns = [" you ", " your ", "yours", "yourself", "you'", "you're", "youre", " u ", " ur "]
third_person_pronouns = [" she ", " he ", " her ", " him ", "hers ", " his", "she'll", "he'll", " shes ", " she's ", " hes ", " he's ", " herself ", " himself "]

not_pronouns = ['"', "you would think", "you'd think", "u would think", "you know", "y'know"]


def contains_any(pronoun_list, comment):
    if any(not_pronoun in comment for not_pronoun in not_pronouns):
        return False
    return any(pronoun in comment for pronoun in pronoun_list)


second_result = df['comment_text'].apply(lambda comment: contains_any(second_person_pronouns, comment))
third_result = df['comment_text'].apply(lambda comment: contains_any(third_person_pronouns, comment))

df['2nd_person_pronoun'] = np.where(second_result, 1, 0)
df['3rd_person_pronoun'] = np.where((third_result & ~second_result), 1, 0)

#export commenter names and dates (being used)

##take care of duplicates (comments by the same user)
df_forcomments = df.groupby('comment_person', as_index=False).agg({
    '2nd_person_pronoun': 'sum',
    '3rd_person_pronoun': 'sum'})

zero_count = (df == 0).sum(axis=1)

#keep only rows where the count of zeroes is less than two
df_forcomments = df[zero_count < 2]

#take random rows for dates
df_fordates = df[zero_count < 2]
df_fordates[['comment_date', 'post_date', '2nd_person_pronoun', '3rd_person_pronoun']].sample(n=1000, random_state=42).to_csv('commenter_dates.csv', index=False)

#take random rows for names

df_forcomments[['comment_person', '2nd_person_pronoun', '3rd_person_pronoun']].sample(n=1000, random_state=42).to_csv('commenters.csv', index=False)

#consolidate columns

columns_to_consolidate = ['url', 'poster', 'like_num', 'comment_num', 'views_num', 'forward_num',
       'bookmark_num', 'video_duration']

#consolidate everything except last two columns, which are summed
df = df.groupby('url', as_index=False).agg({
    **{col: 'first' for col in columns_to_consolidate},
    '2nd_person_pronoun':'sum',
    '3rd_person_pronoun': 'sum'
})

df['3rd_to_2nd_ratio'] = df['3rd_person_pronoun'] / df['2nd_person_pronoun']
df['pronoun_to_total_ratio'] = (df['3rd_person_pronoun'] + df['2nd_person_pronoun']) / df['comment_num']

#if there are no pronouns at all, delete the row
df=df.dropna(subset=['3rd_to_2nd_ratio'])


#export poster names
df['url'] = df['url'].str.split('/video/').str[0]

df['url'].to_csv('posters.csv', index=False)


####importing profile info######

pro_file = os.path.expanduser('~/Downloads/poster_profiles.csv')
dfp = pd.read_csv(pro_file)

columns_to_consolidate_2 = ['following', 'followers', 'is_verified']

 #find character count of descriptions on average
dfp['description'] = dfp['description'].apply(lambda description: len(str(description)))

number_of_posts = dfp.groupby('url').size()

dfp = dfp.groupby('url', as_index=False).agg({
    **{col: 'first' for col in columns_to_consolidate_2},
    'post_date': 'last',
    'avg_like_num':'mean',
    'avg_comment_num': 'mean',
    'avg_views_num': 'mean',
    'description': 'mean',
})
number_of_posts = number_of_posts.reset_index(drop=True)

dfp['number_of_posts'] = number_of_posts

dfp['follower_to_following_ratio'] = dfp['followers'] / dfp['following']


merged_df = pd.merge(df, dfp, how='inner', left_index=True, right_index=True)


#export is_verified column (qualitative)

merged_df[['is_verified','3rd_to_2nd_ratio']].to_csv('verified_posters.csv',index=False)

data_df = merged_df.drop(columns='is_verified')
data_df.to_csv('quant_poster_data', index=False)


