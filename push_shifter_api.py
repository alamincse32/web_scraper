import pandas as pd
from pmaw import PushshiftAPI as push
import datetime as dt

api = push()

subreddit = "eating_disorders"
limit = 100000
before = int(dt.datetime(2021,2,1,0,0).timestamp())
after = int(dt.datetime(2020,12,1,0,0).timestamp())
comment = api.search_comments(subreddit = subreddit,limit=limit,before=before,after=after)

print(f'Retrive {len(comment)} comments from psuhshift')

data = pd.DataFrame(comment)

data.head(5)
data.to_csv('comment.csv',header=True,index=False,columns=list(data.axes[1]))

