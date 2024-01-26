from airflow.decorators import task, dag
from airflow.models     import Variable 
from datetime           import datetime

@dag(dag_id            = 'example_simple_variable_call',
     schedule_interval = '@once',
     description       = 'writes_variable_to_XCOM',
     catchup           = False,
     default_args      = {'owner'      : 'ss',
                          'start_date' : datetime(2023, 9, 1)})

def dig_labs():
    from logging  import error
    from textwrap import dedent

    def fetch_data_from_api():
        return Variable.get("DIG_LABS_HOSTNAME")

    def fetch_data_from_api_encrypted():
        return Variable.get("DIG_LABS_ADMIN_TOKEN_ID")
    
    @task()
    def extract_data():
        response_data = fetch_data_from_api()
        return response_data
    
    @task()
    def extract_data_encrypted():
        response_data = fetch_data_from_api_encrypted()
        return response_data

    extract_data() >> extract_data_encrypted()

dig_labs()