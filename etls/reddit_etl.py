import praw
import sys 
from praw import Reddit
import base64
import requests
import requests.auth
from utils.constants import REDDIT_PW, REDDIT_USERNAME
import pandas as pd

# Define constants for Reddit username and password
username = REDDIT_USERNAME
password = REDDIT_PW

# Define headers for the requests
HEADERS = {"User-Agent": "test-app by u/mjcolon218"}

def get_access_token(client_id, client_secret, username, password):
    """
    Obtain an OAuth2 access token using the client credentials and user credentials.
    :param client_id: The client ID of the Reddit application.
    :param client_secret: The client secret of the Reddit application.
    :param username: The Reddit username.
    :param password: The Reddit password.
    :return: An access token.
    """
    # Set up basic authentication with the client credentials
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    headers = HEADERS
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    # Make a POST request to Reddit's access token endpoint
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    
    # Raise an error if the request was unsuccessful
    response.raise_for_status()
    
    # Extract the access token from the response
    reddit_token = response.json().get('access_token')
    print("Authenticated Token Verified")
    
    return reddit_token

def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    """
    Connects to Reddit using provided credentials and returns an access token.
    :param client_id: The client ID of the Reddit application.
    :param client_secret: The client secret of the Reddit application.
    :param user_agent: The user agent string for the Reddit application.
    :return: An access token.
    """
    try:
        # Obtain the access token using the provided credentials
        access_token = get_access_token(client_id=client_id, client_secret=client_secret, username=username, password=password)
        return access_token
    except Exception as e:
        print(e)
        sys.exit(1)

def extract_posts(access_token, subreddit: str, time_filter: str, limit=None):
    """
    Extract posts from the specified subreddit using the given time filter and limit.
    :param access_token: The access token for authenticating with Reddit.
    :param subreddit: The subreddit to extract posts from.
    :param time_filter: The time filter for fetching top posts (e.g., 'day', 'week', 'month').
    :param limit: The maximum number of posts to fetch. Defaults to None.
    :return: A pandas DataFrame containing the extracted post data.
    """
    # Set up the headers with the access token
    headers = {**HEADERS, **{"Authorization": f"bearer {access_token}"}}
    
    # Make a GET request to Reddit's search endpoint
    search = requests.get(f'https://oauth.reddit.com/r/all/search.json?q={subreddit}&limit={limit}', headers=headers)
    
    # Parse the JSON response
    r_json = search.json()
    
    # Initialize lists to store the extracted data
    subscsriber_count_list = []
    post_title_list = []
    created_utc_list = []
    is_video_list = []
    post_score_list = []
    over_18_list = []
    author_list = []
    num_of_comments_list = []
    post_id_list = []
    # Extract relevant data from each post
    for i in r_json['data']['children']:
        post_id_list.append(i['data']['id'])
        post_title_list.append(i['data']['title'])
        subscsriber_count_list.append(i['data']['subreddit_subscribers'])
        created_utc_list.append(i['data']['created'])
        is_video_list.append(i['data']['is_video'])
        post_score_list.append(i['data']['score'])
        over_18_list.append(i['data']['over_18'])
        author_list.append(i['data']['author'])
        num_of_comments_list.append(i['data']['num_comments'])  
        
    # Create a pandas DataFrame from the extracted data
    post_df = pd.DataFrame({
        'post_id': post_id_list,
        'post_title':post_title_list,
        'subscriber_count': subscsriber_count_list,
        'created_utc': created_utc_list,
        'is_video': is_video_list,
        'post_score': post_score_list,
        'over_18': over_18_list,
        'author': author_list,
        'comment_count': num_of_comments_list
    })
    
    return post_df  # Return the DataFrame
def transform_data(df):
    df['post_id'] = df['post_id'].astype(str)
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    df['over_18'] = df['over_18'].astype(bool)
    df['author'] = df['author'].astype(str)
    df['subscriber_count'] = df['subscriber_count'].astype(int) 
    df['post_score'] = df['post_score'].astype(int)
    df['comment_count'] = df['comment_count'].astype(str)

    print(df)
    print(df.info())
    return df
def load_to_csv(data:pd.DataFrame,path:str):
    data.to_csv(path, index=False)