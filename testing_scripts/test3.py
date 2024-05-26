import praw
import sys 
from praw import Reddit
import base64
import pandas as pd
import requests
import requests.auth
from utils.constants import REDDIT_PW,REDDIT_USERNAME
username = REDDIT_USERNAME
password= REDDIT_PW
HEADERS ={"User-Agent": "test-app by u/mjcolon218"}
def get_access_token(client_id, client_secret, username, password):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = HEADERS
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    response = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)
    response.raise_for_status()
    reddit_token = response.json().get('access_token')
    print("Authenticated Token Verified")
    #print(reddit.user.me(),"-Connection Successful-")

    #print(token)
    return reddit_token

def connect_reddit(client_id, client_secret, user_agent):
    """
    Connects to Reddit using provided credentials and returns a Reddit client instance.
    :param client_id: The client ID of the Reddit application.
    :param client_secret: The client secret of the Reddit application.
    :param user_agent: The user agent string for the Reddit application.
    :return: An instance of the Reddit client.
    """
    
    try:
        access_token = get_access_token(client_id=client_id, client_secret=client_secret,username=username,password=password)
        #

        
        
        return access_token
    except Exception as e:
        print(e)
        sys.exit(1)
        
        
def extract_posts(access_token,subreddit:str,time_filter:str, limit=None):
#search_query = 'dataengineering'
    headers = {**HEADERS,**{"Authorization": f"bearer {access_token}"}}
    search = requests.get(f'https://oauth.reddit.com/r/all/search.json?q={subreddit}&limit={limit}', headers=headers)
    r_json = search.json()
    
    
    
    subscsriber_count_list = []
    created_utc_list = []
    is_video_list = []
    post_score_list = []
    over_18_list = []
    author_list = []
    num_of_comments_list=[]

    for i in r_json['data']['children']:
        subscsriber_count_list.append(i['data']['subreddit_subscribers'])
        created_utc_list.append(i['data']['created'])
        is_video_list.append(i['data']['is_video'])
        post_score_list.append(i['data']['score'])
        over_18_list.append(i['data']['over_18'])
        author_list.append(i['data']['author'])
        num_of_comments_list.append(i['data']['num_comments'])  
    df = pd.DataFrame({
    'subscriber_count':subscsriber_count_list,
    'created_utc':created_utc_list,
    'is_video': is_video_list,
    'post_score':post_score_list,
    'over_18':over_18_list,
    'author':author_list,
    'comment_count':num_of_comments_list
        })
    print(df)
    
    
    
    
    import pandas as pd 
from etls.reddit_etl import connect_reddit, extract_posts,get_access_token,transform_data
from utils.constants import CLIENT_ID,SECRET,REDDIT_USERNAME,REDDIT_PW
import requests
import requests.auth
# Creating a function called reddit pipeline.
client_id_variable = CLIENT_ID
secret_variable = SECRET
username = REDDIT_USERNAME
password= REDDIT_PW

def reddit_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
    # Get access token
    
    access_token = connect_reddit(client_id_variable, secret_variable, user_agent='test-app')    
    #transformation
    #loading to csv
    #extraction
    reddit_posts = extract_posts(access_token,subreddit,time_filter,limit)
    transform = transform_data(reddit_posts)