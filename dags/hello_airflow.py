"""学習用のサンプル DAG(TaskFlow API)。"""

from datetime import datetime

from airflow.sdk import dag, task


@dag(
    schedule="@daily",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=["study"],
)
def hello_airflow():
    @task
    def extract() -> dict:
        return {"message": "Hello, Airflow 3!"}

    @task
    def transform(payload: dict) -> str:
        return payload["message"].upper()

    @task
    def load(message: str) -> None:
        print(f"loaded: {message}")

    load(transform(extract()))


hello_airflow()
