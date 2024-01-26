from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow import DAG
from airflow.models.connection import Connection
from time import time_ns
from datetime import datetime
import os

with DAG(
    dag_id="example_kubernetes_pod",
    schedule="@hourly",
    start_date=datetime(2023, 3, 30),
    catchup=False,
) as dag:
    
    example_kpo = KubernetesPodOperator(
        kubernetes_conn_id="example_kpo",
        image="hello-world",
        name="example_kpo",
        task_id="example_kpo",
        env_vars={
            "ENV_VAR_NAME_1": "{{ conn.CONN_ID.FIELD }}",
            "ENV_VAR_NAME_2": "{{ conn.CONN_ID.FIELD }}",
        },
        is_delete_operator_pod=True,
        get_logs=True,
        deferrable=True,
    )

# Set airflow environment variable: AIRFLOW__CORE__SENSITIVE_VAR_CONN_NAMES = true
# Set env variable that pulls from the secrets backend
# Where CONN_ID is the connection id, and FIELD is the field in the connection e.g. login, password, extra etc.
