from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.bigquery_check_operator import BigQueryCheckOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG with the default arguments
dag = DAG(
    'check_data_change_in_table',
    default_args=default_args,
    description='A DAG to check for data changes in a BigQuery table',
    schedule_interval=timedelta(minutes=15),  # Adjust this according to your needs
)

# Define tasks/operators in the DAG
start_task = DummyOperator(task_id='start', dag=dag)

# Check if there are any rows in the table
check_data_change_task = BigQueryCheckOperator(
    task_id='check_data_change_task',
    sql='SELECT COUNT(*) FROM mwaa_pricing.usage WHERE updated_date = CURRENT_DATE() AND CURRENT_TIME() <= TIME_ADD(updated_time, interval 5 minute)',
    gcp_conn_id='fe_bigquery_connection_id',
    use_legacy_sql=False,
    dag=dag,
)

# Dummy task to execute when the table data changes
execute_task = DummyOperator(task_id='execute_task', dag=dag)

# Define the task dependencies
start_task >> check_data_change_task >> execute_task
