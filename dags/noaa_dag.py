from airflow import DAG
from airflow.models.connection import Connection
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeValueCheckOperator
from airflow.operators.dummy import DummyOperator 
from airflow.operators.python import PythonOperator
#from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator
from time import time_ns
from datetime import datetime
import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config

AWS_CONN_ID = "s3_conn"
SNOWFLAKE_CONN_ID = "snowflake_conn"

def list_files():
    s3client = boto3.client('s3', region_name='us-west-2', config=Config(signature_version=UNSIGNED))
    objects = s3client.list_objects(Bucket='santiago-astro', Prefix='NOAA')
    for my_bucket_object in objects:
        print(my_bucket_object)

with DAG(
    dag_id="noaa_s3_to_snowflake_dag", 
    schedule="@daily", 
    start_date=datetime(2023, 1, 1), 
    is_paused_upon_creation=False, 
    catchup=False
) as dag:
    
    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end")

    value_check = SnowflakeValueCheckOperator(
        task_id="check_row_count",
        snowflake_conn_id='snowflake_conn',
        sql=f"SELECT COUNT(*) FROM TPCDS_SF100TCL.STORE;",
        pass_value=1902,
    )

    S3_list_files = PythonOperator(
        task_id="S3_list_files",
        python_callable=list_files,
        # op_kwargs: Optional[Dict] = None,
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )

    begin >> value_check >> end
    # begin >> truncate_snowflake_stage_table >> copy_from_s3_to_snowflake >> end