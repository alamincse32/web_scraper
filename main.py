
# Import the required python library

import requests
import pandas as pd
import datetime
from IPython.display import display
#parameter for authentication
CLIENT_ID = '6peMbHx5tjvuHtu3dxm47w'
SECRET_KEY = 'sACOL-6WhqFQ4CVsCt3cMQTyQJlzfA'

# we use this function to convert responses to dataframes
def df_from_response(res):
    # initialize temp dataframe for batch of data in response
    df = pd.DataFrame()

    # loop through each post pulled from res and append to df
    for post in res.json()['data']['children']:
        df = df.append({
            'subreddit': post['data']['subreddit'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'upvote_ratio': post['data']['upvote_ratio'],
            'ups': post['data']['ups'],
            'downs': post['data']['downs'],
            'score': post['data']['score'],
            'link_flair_css_class': post['data']['link_flair_css_class'],
            'created_utc': datetime.datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'id': post['data']['id'],
            'kind': post['kind']
        }, ignore_index=True)

    return df

#Authenticate API
auth = requests.auth.HTTPBasicAuth(CLIENT_ID,SECRET_KEY)

#login data
data = {
    'grant_type': 'password',
    'username': 'alamincse32',
    'password': 'Alamin2010'

}
params = {'limit': 100}
#defining header of the request
headers = {
    'User-Agent': 'DataCollectionTesting/0.0.1'
}

res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,data=data,headers=headers)

TOKEN = res.json()['access_token']

headers['Authorization'] = f'bearer {TOKEN}'

# loop through 10 times (returning 1K posts)
data1 = pd.DataFrame()
for i in range(3):
    # make request
    res = requests.get("https://oauth.reddit.com/r/EatingDisorders/new",
                       headers=headers,
                       params=params)

    # get dataframe from response
    new_df = df_from_response(res)

    # take the final row (oldest entry)
    row = new_df.iloc[len(new_df) - 1]
    # create fullname
    fullname = row['kind'] + '_' + row['id']
    # add/update fullname in params
    params['after'] = fullname

    # append new_df to data
    data1 = data1.append(new_df, ignore_index=True)
data1.to_csv('test_1.csv')


