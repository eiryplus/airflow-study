FROM python:3.13-slim

ENV AIRFLOW_HOME=/opt/airflow \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir poetry==2.4.1

# dbt は Airflow と依存関係が衝突しやすいため専用 venv に分離する。
# バージョンは dbt-study(poetry.lock)に合わせる
RUN python -m venv /opt/dbt-venv \
    && /opt/dbt-venv/bin/pip install --no-cache-dir \
        dbt-core==1.11.12 \
        dbt-postgres==1.10.2

WORKDIR /opt/airflow

# 依存定義だけを先にコピーしてレイヤーキャッシュを効かせる
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

EXPOSE 8080
