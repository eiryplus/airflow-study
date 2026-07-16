"""hello_airflow DAG の単体テスト。"""

from hello_airflow import hello_airflow


def test_dag_structure():
    dag = hello_airflow()

    assert dag.dag_id == "hello_airflow"
    assert set(dag.task_dict) == {"extract", "transform", "load"}
    assert dag.task_dict["extract"].downstream_task_ids == {"transform"}
    assert dag.task_dict["transform"].downstream_task_ids == {"load"}


def test_extract():
    dag = hello_airflow()
    extract = dag.task_dict["extract"].python_callable

    assert extract() == {"message": "Hello, Airflow 3!"}


def test_transform():
    dag = hello_airflow()
    transform = dag.task_dict["transform"].python_callable

    assert transform({"message": "hello"}) == "HELLO"
