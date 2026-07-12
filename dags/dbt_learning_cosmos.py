"""dbt-study の dbt プロジェクトを Cosmos で DAG 化する。

dbt の各モデル / seed / テストが Airflow の個別タスクとして展開される。
接続情報は Airflow Connection `dbt_postgres` から ProfileMapping で生成する
(profiles.yml の複製は不要)。
"""

from datetime import datetime

from cosmos import DbtDag, ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping

DBT_PROJECT_DIR = "/opt/airflow/dbt_project"
DBT_EXECUTABLE = "/opt/dbt-venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="dbt_learning",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="dbt_postgres",
        profile_args={"schema": "analytics"},
    ),
)

dbt_learning_cosmos = DbtDag(
    dag_id="dbt_learning_cosmos",
    project_config=ProjectConfig(DBT_PROJECT_DIR),
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=DBT_EXECUTABLE),
    # dbt_privacy パッケージを使っているため実行前に dbt deps を走らせる
    operator_args={"install_deps": True},
    schedule="@daily",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    # 同一 DB に対する dbt の並行実行は backup リレーション名が衝突するため禁止
    max_active_runs=1,
    tags=["study", "dbt"],
)
