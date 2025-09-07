from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.monitor import detect_drift
from main import main as train_pipeline

default_args = {
    'owner': 'model-forge',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'model_retrain_pipeline',
    default_args=default_args,
    description='Retrain if drift detected or on schedule',
    schedule_interval='@weekly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:

    drift_check = PythonOperator(
        task_id='detect_drift',
        python_callable=detect_drift,
        op_kwargs={'config_path': 'configs/config.yaml'}
    )

    retrain = PythonOperator(
        task_id='retrain_model',
        python_callable=train_pipeline,
        trigger_rule='all_success'
    )

    drift_check >> retrain
