import pandas as pd 
from etls.reddit_etl import connect_reddit, extract_posts, transform_data,load_to_csv
from utils.constants import CLIENT_ID, SECRET, REDDIT_USERNAME, REDDIT_PW,OUTPUT_PATH
import requests
import requests.auth

# Define variables for client ID, secret, username, and password
client_id_variable = CLIENT_ID
secret_variable = SECRET
username = REDDIT_USERNAME
password = REDDIT_PW

def reddit_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
    """
    The main pipeline function to extract, transform, and load Reddit posts data.
    :param file_name: The name of the output file.
    :param subreddit: The subreddit to extract posts from.
    :param time_filter: The time filter for fetching top posts (e.g., 'day', 'week', 'month'). Default is 'day'.
    :param limit: The maximum number of posts to fetch. Defaults to None (no limit).
    """
    
    # Step 1: Get access token
    # Obtain an access token using the provided client credentials and user credentials
    access_token = connect_reddit(client_id_variable, secret_variable, user_agent='test-app')    

    # Step 2: Extract posts
    # Extract posts from the specified subreddit using the given time filter and limit
    reddit_posts = extract_posts(access_token, subreddit, time_filter, limit)

    # Step 3: Transform data
    # Apply transformations to the extracted Reddit posts data
    transformed_data = transform_data(reddit_posts)
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_to_csv(transformed_data,file_path)

    # Step 4: Load to CSV
    # Save the transformed data to a CSV file with the given file name
    #transformed_data.to_csv(file_name, index=False)
    print(f"Data successfully saved to {file_name}:Processed-Locally")
    return file_path