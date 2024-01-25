from airflow import DAG
from airflow.providers.microsoft.azure.operators.asb import AzureServiceBusReceiveMessageOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from datetime import datetime
import logging

def receive_and_log_messages():
    try:
        receive_message = AzureServiceBusReceiveMessageOperator(
            task_id='receive_message',
            azure_service_bus_conn_id='azure-service-bus',
            queue_name='demo-fe',
            max_message_count=1,
        )
        return logging.error(type(receive_message)) #receive_message.execute(context={})
    except AirflowException as e:
        logging.error(f"Failed to receive messages: {e}")
        return None

with DAG(
    'azure_service_bus_example',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
) as dag:

    receive_and_log_messages_task = PythonOperator(
    task_id='receive_and_log_messages',
    python_callable=receive_and_log_messages,
    dag=dag,
    )

receive_and_log_messages_task