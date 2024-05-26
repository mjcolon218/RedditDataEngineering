# Data Pipeline with Reddit, Airflow, Celery, Postgres, S3, AWS Glue, Athena, and Redshift

This project provides a comprehensive data pipeline solution to extract, transform, and load (ETL) Reddit data into a Redshift data warehouse. The pipeline leverages a combination of tools and services including Apache Airflow, Celery, PostgreSQL, Amazon S3, AWS Glue, Amazon Athena, and Amazon Redshift.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [System Setup](#system-setup)
- [Video](#video)

## Overview

- **Docker for Environment Consistency**: Containerized Airflow, Celery, Redis, and PostgreSQL for consistent and reproducible environments.
- **Task Scheduling with Airflow**: Managed and scheduled ETL workflows.
- **Data Extraction with Python**: Extracted data from an API.
- **Data Upload to S3**: Uploaded extracted data to an S3 bucket.
- **Data Cataloging with AWS Glue**: Automatically detected and cataloged data.
- **Querying with Amazon Athena**: Performed SQL queries on data stored in S3.
## Architecture
![RedditDataEngineering.png](assets%2FRedditDataEngineering.png)
1. **Reddit API**: Source of the data.
2. **Apache Airflow & Celery**: Orchestrates the ETL process and manages task distribution.
3. **PostgreSQL**: Temporary storage and metadata management.
4. **Amazon S3**: Raw data storage.
5. **AWS Glue**: Data cataloging and ETL jobs.
6. **Amazon Athena**: SQL-based data transformation.
7. **Amazon Redshift**: Data warehousing and analytics.

## Prerequisites
- AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- Reddit API credentials.
- Docker Installation
- Python 3.9 or higher

## System Setup
1. Clone the repository.
   ```bash
    git clone https://github.com/airscholar/RedditDataEngineering.git
   ```
2. Create a virtual environment.
   ```bash
    python3 -m venv venv
   ```
3. Activate the virtual environment.
   ```bash
    source venv/bin/activate
   ```
4. Install the dependencies.
   ```bash
    pip install -r requirements.txt
   ```
5. Rename the configuration file and the credentials to the file.
   ```bash
    mv config/config.conf.example config/config.conf
   ```
6. Starting the containers
   ```bash
    docker-compose up -d
   ```
7. Launch the Airflow web UI.
   ```bash
    open http://localhost:8080
   ```
## Documentation
1. **Check out the** : [Airflow Documentation](https://airflow.apache.org/docs/stable/)
2. **Check out the** : [Celery Documentation](https://docs.celeryproject.org/en/stable/)
3. **Check out the** : [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)
4. **Check out the** : [Access Keys Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
5. **Check out the** : [Docker Documentation](https://docs.docker.com/reference/)
6. **Check out the** : [Policy Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-and-attach-iam-policy.html)
7. **Check out the** : [Requests Documentation](https://requests.readthedocs.io/en/latest/)
8. **Check out the** : [S3fs Documentation](https://requests.readthedocs.io/en/latest/)

# Key Takeaways #
 
 1. **Airflow**: A workflow management system that allows you to create, schedule, and monitor data pipelines.
 2. **Celery**: A task queue system that allows you to distribute tasks across multiple workers.
 3. **Boto3**: A Python library that allows you to interact with AWS services.
 4. **Access Keys**: A set of credentials that allow you to access AWS services.
 5. **Docker**: A containerization system that allows you to package and run applications in isolated environments.
 6. **Policy**: A set of permissions that allow you to access AWS services.
 7. **Requests**: A Python library that allows you to make HTTP requests.
 8. **S3fs**: A Python library that allows you to interact with Amazon S3.
 9. **Documentation** Documented the setup and configuration steps for reproducibility.

 These key takeaways highlight the technical skills and knowledge applied in the project, showcasing my expertise in modern data engineering practices and the use of cloud services for scalable data solutions.
 I also added some images of me working in the AWS enviornment using some of the micro-servies.

 # AWS Services #
 1. **GlueJob and Crawler**
 
 ![gjob.PNG](assets%2Fgjob.png)
 2. **Redshift Datawarehouse**

 ![redshift.PNG](assets%2Fredshift.png)

 3. **Airflow Docker Container**
 ![projectsnippets.PNG](assets%2Fprojectsnippets.png)

 ## AWS Glue Policy

To ensure that AWS Glue has the necessary permissions to interact with your S3 buckets and other services, attach the following policy to your Glue IAM role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::aws-reddit-engineering",
                "arn:aws:s3:::aws-reddit-engineering/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "glue:*"
            ],
            "Resource": [
                "arn:aws:glue:*:<your-account-id>:catalog",
                "arn:aws:glue:*:<your-account-id>:database/*",
                "arn:aws:glue:*:<your-account-id>:table/*",
                "arn:aws:glue:*:<your-account-id>:crawler/*",
                "arn:aws:glue:*:<your-account-id>:job/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
} 
```

## Common Troubleshooting Issues

### 1. Access Denied Errors

**Symptom**: You receive a "403 Access Denied" error when AWS Glue or any other service tries to access your S3 buckets.

**Solution**:
- **Check IAM Role Permissions**: Ensure that the IAM role used by your Glue job has the necessary permissions. Refer to the [AWS Glue Policy](#aws-glue-policy) section in this document to set up the correct policy.
- **Bucket Policy**: Ensure that the S3 bucket policies allow the necessary actions from the IAM role. You may need to adjust the bucket policy to grant the required permissions.

### 2. Airflow Task Failures

**Symptom**: Airflow tasks fail to execute, or DAGs are not running as expected.

**Solution**:
- **Check Logs**: Inspect the logs for the failing tasks in the Airflow web UI. Logs often contain detailed error messages that can help identify the problem.
- **Environment Variables**: Ensure all required environment variables are correctly set in the `docker-compose.yml` file.
- **Dependencies**: Verify that all dependencies are correctly installed and accessible within the Docker containers.

### 3. Docker Container Issues

**Symptom**: Docker containers fail to start, or services are not running correctly.

**Solution**:
- **Inspect Container Logs**: Use `docker logs <container_id>` to view the logs of a specific container and identify issues.
- **Rebuild Containers**: Sometimes, rebuilding the containers can resolve issues. Use the following commands:
  ```bash
  docker-compose down
  docker-compose up --build ```

4. **Glue Job Failures**
- Symptom: Glue jobs fail to start or do not complete successfully.

**Solution:**

- Check CloudWatch Logs: Glue job logs are stored in CloudWatch. Inspect these logs to identify any errors or issues.
Validate Scripts: Ensure that the ETL scripts are correctly written and do not contain syntax errors or logical issues.
Network Configuration: Ensure that your Glue job can access the required S3 buckets and any other network resources.
5. **Athena Query Issues**
- Symptom: Athena queries return errors or unexpected results.

**Solution:**

- Check Table Definitions: Ensure that the table definitions in Athena match the schema of the data in your S3 buckets.
Query Syntax: Verify that your SQL query syntax is correct.
Data Format: Ensure that the data format in S3 is consistent with the format expected by Athena.
6. **Redshift Loading Issues**
- Symptom: Data fails to load into Amazon Redshift from S3.

**Solution:**

- Check IAM Role Permissions: Ensure the IAM role used for the COPY command has the necessary permissions to access the S3 bucket.
Validate COPY Command: Ensure the syntax and parameters of the COPY command are correct.
Data Format: Ensure the data in S3 is in the correct format and structure for Redshift to load.

*Bonus*
- I also added a folder called testing_scripts with some jupyter notebook and some toy code to show how I executed the functionalty of my code then just modularized for my airflow scheduler.
- Stay Tuned Tableau Dashboard Coming Soon. 