from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta 
import os
from airflow.operators.python import PythonOperator
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
from pipelines.aws_s3_pipeline import upload_s3_pipeline
from pipelines.reddit_pipeline import reddit_pipeline
dag_owner = 'Maurice J Colon'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 0,
        'retry_delay': timedelta(minutes=1),
        'start_date': datetime(year=2024,month=5,day=23)
        }
file_postfix = datetime.now().strftime("%Y%m%d")

with DAG(dag_id='etl_reddit_pipeline',
        default_args=default_args,
        description='a DAG for extracting and processing Reddit data',
        schedule_interval='@daily',
        catchup=False,
        tags=['reddit','etl','pipeline']
) as dag:
    start = EmptyOperator(task_id='start')

    extraction = PythonOperator(
        task_id = 'reddit_extraction',
        python_callable = reddit_pipeline,
        op_kwargs = {
            'file_name':f'reddit_{file_postfix}',
            'subreddit': 'dataengineering',
            'time_filter':'day',
            'limit':  50
        }

    )
    upload_s3 = PythonOperator(
        task_id = 's3_upload',
        python_callable = upload_s3_pipeline,
    )
    
    start >> extraction >> upload_s3