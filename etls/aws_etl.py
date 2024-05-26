import s3fs
from s3fs import S3FileSystem
from utils.constants import AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY


def connect_to_s3():
    try:
        s3 = s3fs.S3FileSystem(
            anon=False,
            key=AWS_ACCESS_KEY_ID,
            secret=AWS_ACCESS_KEY
        )
        return s3
    except Exception as e:
        print(e)
def create_bucket_if_not_exist(s3: s3fs.S3FileSystem, bucket:str):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print("Bucket created")
        else :
            print("Bucket already exists")
    except Exception as e:
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket:str, s3_file_name: str):
    """
    Uploads a file to S3 using s3fs.
    
    :param s3: An initialized s3fs.S3FileSystem object.
    :param file_path: The path to the local file to be uploaded.
    :param bucket: The name of the S3 bucket.
    :param s3_file_name: The desired name of the file in S3.
    """
    try:
        # Ensure the S3 path is correctly formatted
        s3_path = f"{bucket}/raw/{s3_file_name}"
        
        # Upload the local file to the specified S3 path
        s3.put(file_path, s3_path)
        
        print('File uploaded to S3')
    except FileNotFoundError:
        print('The file was not found')
    except Exception as e:
        print(f"An error occurred: {e}")
