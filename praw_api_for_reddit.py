import praw as pr
import pandas as pd
reddit = pr.Reddit(client_id='6peMbHx5tjvuHtu3dxm47w',client_secret='sACOL-6WhqFQ4CVsCt3cMQTyQJlzfA',
                   user_agent='python:DataCollectionTesting:0.0.1(by/alamincse32')

hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)

posts = []

for post in hot_posts:
    #print(post.created)
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])


submission = reddit.submission(url="https://www.reddit.com/r/MapPorn/comments/a3p0uq/an_image_of_gps_tracking_of_multiple_wolves_in/")
submission.comments.replace_more(limit=0)
for top_level_comment in submission.comments.list():
    print(top_level_comment.body)