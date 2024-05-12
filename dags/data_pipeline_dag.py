from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_scripts import extract as extract_module
from etl_scripts import transform as transform_module
from etl_scripts import store as store_module

# Default parameters for the DAG
default_params = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG structure
with DAG(
    dag_id='news_etl_pipeline',
    default_args=default_params,
    description='Automated ETL pipeline for news articles with extract, transform, store phases.',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    # Define tasks
    extract_task = PythonOperator(
        task_id='extract_news',
        python_callable=extract_module.get_news,
        dag=dag
    )

    transform_task = PythonOperator(
        task_id='transform_news',
        python_callable=transform_module.clean_news_data,
        provide_context=True,
        op_kwargs={'articles': '{{ ti.xcom_pull(task_ids="extract_news") }}'},
        dag=dag
    )

    store_task = PythonOperator(
        task_id='store_news',
        python_callable=store_module.save_news,
        provide_context=True,
        op_kwargs={'news_data': '{{ ti.xcom_pull(task_ids="transform_news") }}'},
        dag=dag
    )

    # Set task dependencies
    extract_task >> transform_task >> store_task
