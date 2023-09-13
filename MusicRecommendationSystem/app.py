import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Load data
data = pd.read_csv('music_data.csv')
# Create user-item matrix
user_item_matrix = data.pivot_table(index='user_id', columns='song_id', values='rating')
# Compute user similarity
user_similarity = cosine_similarity(user_item_matrix.fillna(0))
# Create a function to make recommendations
def make_recommendations(user_id, num_recommendations):
    similar_users = user_similarity[user_id-1].argsort()[::-1]
    similar_users = similar_users[1:num_recommendations+1]
    similar_user_ids = [x+1 for x in similar_users]
    recommendations = pd.DataFrame()
    for user in similar_user_ids:
        top_songs = user_item_matrix.loc[user].sort_values(ascending=False).head(num_recommendations).index
        recommendations = pd.concat([recommendations, pd.DataFrame(top_songs)], axis=1)
    recommendations = recommendations.melt()['song_id'].dropna().drop_duplicates().head(num_recommendations)
    return recommendations.tolist()
# Evaluate the system
y_true = data['song_id']
y_pred = data['user_id'].apply(lambda x: make_recommendations(x, 10)[0])
accuracy = accuracy_score(y_true, y_pred)
print('Accuracy:', accuracy)
# Add a comment
# This code is for a music recommender system on Spotify. 
# It takes in a user ID and returns a list of recommended songs. 
# The recommendations are based on the user's listening history and the listening history of other users who are similar to the user.
 