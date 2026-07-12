# airflow-study

Apache Airflow の学習環境。Airflow は Docker コンテナ上で実行します。

## 構成

| 項目 | 内容 |
| --- | --- |
| Python | 3.13 |
| パッケージ管理 | Poetry(全モジュールを PyPI から取得) |
| Airflow | 3.3.0 |
| Executor | LocalExecutor |
| メタデータ DB | PostgreSQL 16(コンテナ) |
| UI ポート | **http://localhost:8081**(8080 は他インスタンス用のため回避) |

コンテナイメージは `python:3.13-slim` をベースに、ローカルと同じ
`pyproject.toml` / `poetry.lock` から Poetry でインストールして構築します。

### サービス構成(docker-compose.yml)

- `postgres` — メタデータ DB
- `airflow-init` — DB マイグレーション(初回のみ実行して終了)
- `airflow-apiserver` — UI / REST API(ホスト 8081 → コンテナ 8080)
- `airflow-scheduler` — スケジューラ(LocalExecutor でタスクもここで実行)
- `airflow-dag-processor` — DAG ファイルのパース
- `airflow-triggerer` — Deferrable Operator 用

認証は SimpleAuthManager の `ALL_ADMINS=True`(学習用のためログイン不要)。

## セットアップと起動

```sh
make build   # イメージのビルド
make up      # 起動 → http://localhost:8081
```

ローカルで IDE 補完や DAG の静的チェックをしたい場合は venv も作れます:

```sh
make install  # poetry が .venv を in-project で作成
```

## dbt-study との連携(Cosmos)

隣の `dbt-study` リポジトリの dbt プロジェクトを
[astronomer-cosmos](https://astronomer.github.io/astronomer-cosmos/) で DAG 化しています。

- 共有 external ネットワーク `data-platform` 経由で dbt 用 Postgres
  (`dbt-postgres`)に接続(`make up` がネットワークを自動作成)
- `../dbt-study/dbt_project` をコンテナの `/opt/airflow/dbt_project` にマウント
- dbt CLI は Airflow との依存衝突を避けるためイメージ内の専用 venv
  (`/opt/dbt-venv`)にインストール(バージョンは dbt-study に合わせる)
- DB 接続は Airflow Connection `dbt_postgres`(環境変数で定義)から
  ProfileMapping で生成。profiles.yml の複製は不要
- DAG 定義: [dags/dbt_learning_cosmos.py](dags/dbt_learning_cosmos.py)
  — dbt の各 seed / モデル / テストが個別タスクとして展開される

事前に dbt-study 側の Postgres を起動しておくこと:

```sh
cd ../dbt-study && docker compose up -d postgres
```

## DAG の追加

`dags/` 配下に Python ファイルを置くと、コンテナにマウントされ
dag-processor が自動で読み込みます。
サンプルとして [dags/hello_airflow.py](dags/hello_airflow.py) を用意しています。

```sh
make dags-list  # 認識されている DAG の確認
make logs       # 全サービスのログ追跡
```

## 停止・クリーンアップ

```sh
make down   # コンテナ停止(DB データは保持)
make clean  # コンテナ・ボリューム・ログを削除して初期状態へ
```
