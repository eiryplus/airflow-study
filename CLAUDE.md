# CLAUDE.md

このリポジトリで作業する際のルール。

## 開発・実行ルール

- **Python環境**: 必ず `venv` の仮想環境(`.venv`)をアクティベートしてからコードを実行してください。
- **パッケージ管理**: グローバル環境へのインストールは禁止です。パッケージの追加や管理は仮想環境内で行ってください。

## テスト

- `dags/` 配下にコードを追加・変更した場合は、必ず対応する unittest を `tests/` 配下に作成・更新すること。
- テストは `make test`(内部で `poetry run pytest`、pytest-cov によるカバレッジ計測込み)で実行する。
- pytest / coverage の設定は `pyproject.toml` の `[tool.pytest.ini_options]` / `[tool.coverage.*]` を参照。
