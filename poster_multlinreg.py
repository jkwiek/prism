import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# For splitting the dataset
from sklearn.model_selection import train_test_split

# For building the model
from sklearn.linear_model import LinearRegression

# For model evaluation
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#import dataset (post end)
data = pd.read_csv('merged_df.csv')
independent_vars = data[
    ['like_num',
     'comment_num',
     'views_num',
     'video_duration',
     'following',
     'followers',
     'post_date',
     'avg_like_num',
     'avg_comment_num',
     'avg_views_num',
     'description',
     'number_of_posts',
     'follower_to_following_ratio']]

dependent_var = data['2nd_to_3rd_ratio']