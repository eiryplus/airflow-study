# Airflow learning environment (Docker Compose + LocalExecutor)
COMPOSE := docker compose

.PHONY: install build network up down restart logs ps dags-list clean

## dbt-study と共有する external ネットワークを作成(存在しなければ)
network:
	docker network inspect data-platform >/dev/null 2>&1 || docker network create data-platform

## ローカル開発用の venv を作成(IDE 補完・DAG の静的チェック用)
install:
	poetry install

## Airflow イメージのビルド
build:
	$(COMPOSE) build

## 全サービスを起動(UI: http://localhost:8081)
up: network
	$(COMPOSE) up -d

## 全サービスを停止
down:
	$(COMPOSE) down

restart: down up

## ログを追跡表示
logs:
	$(COMPOSE) logs -f

## サービスの状態を表示
ps:
	$(COMPOSE) ps

## 認識されている DAG の一覧を表示
dags-list:
	$(COMPOSE) exec airflow-scheduler airflow dags list

## コンテナ・ボリューム・ログを削除して初期状態に戻す
clean:
	$(COMPOSE) down -v --remove-orphans
	rm -rf logs
