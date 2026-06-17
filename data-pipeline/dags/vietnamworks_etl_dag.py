from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
def _bronze_run(date_str):
    from pipeline.bronze import run
    return run(date_str=date_str)

def _silver_run(date_str):
    from pipeline.silver import run
    return run(date_str=date_str)

def _silver_to_postgres_run(date_str):
    from pipeline.silver_to_postgres import run
    return run(date_str=date_str)

def _embedding_run():
    from ai.embedding import run
    return run()

def _salary_train_run():
    from ai.salary_predictor import run
    return run()

default_args = {
    "owner" : "techjobai",
    "retries" : 2,
    "retry_delay" : timedelta(minutes=5)
}

with DAG(
    dag_id= "vietnamworks_etl",
    default_args= default_args,
    start_date= datetime(2026, 5, 26),
    schedule_interval= "@daily",
    catchup= False,
    tags= ["vietnamworks", "etl"],
) as dag:
    
    ingest_to_bronze = PythonOperator(
        task_id="ingest_to_bronze",
        python_callable=_bronze_run,
        op_kwargs={"date_str": "{{ ds }}"},
    )

    extract_to_silver = PythonOperator(
        task_id= "extract_to_silver",
        python_callable= _silver_run,
        op_kwargs={"date_str": "{{ ds }}"},
    )

    silver_to_postgres = PythonOperator(
        task_id= "silver_to_postgres",
        python_callable= _silver_to_postgres_run,
        op_kwargs={"date_str": "{{ ds }}"},
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/airflow/dbt_vietnamworks && /home/airflow/.local/bin/dbt build --profiles-dir .",
    )

    generate_embeddings = PythonOperator(
        task_id="generate_embeddings",
        python_callable=_embedding_run,
    )

    train_salary_model = PythonOperator(
        task_id="train_salary_model",
        python_callable=_salary_train_run,
    )

    ingest_to_bronze >> extract_to_silver >> silver_to_postgres >> dbt_build >> generate_embeddings >> train_salary_model
