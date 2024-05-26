import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
# Get job arguments
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read the data from S3
AmazonS3_node1716686219090 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": "\"", "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://aws-reddit-engineering/raw/reddit_20240526.csv"], "recurse": True},
    transformation_ctx="AmazonS3_node1716686219090"
)

# Convert DynamicFrame to DataFrame
df = AmazonS3_node1716686219090.toDF()

# Rename the column 'post_score' to 'score'
df = df.withColumnRenamed('post_score', 'score')

# Convert DataFrame back to DynamicFrame
transformed_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "transformed_dynamic_frame")

# Write the transformed data back to S3
AmazonS3_node1716686223034 = glueContext.write_dynamic_frame.from_options(
    frame=transformed_dynamic_frame,
    connection_type="s3",
    format="glueparquet",
    connection_options={"path": "s3://aws-reddit-engineering/transformed/", "partitionKeys": []},
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1716686223034"
)

# Commit the job
job.commit()
