[private]
default:
    just --fmt --unstable 2> /dev/null
    just --list --unsorted

tree *args:
    tree {{ args }} -L 4 --gitignore --dirsfirst

DCO := "docker-compose"

# 產生 .env 檔案給 docker-compose 使用
[group('Docker Compose')]
env env_name="dev":
    ./gen_env.sh .env.{{ env_name }}*

[group('alembic')]
alembic *args:
    {{ DCO }} run --rm backend uv run alembic {{ args }}

delete-and-restart-db: && alembic-migrate
    {{ DCO }} down -v db
    {{ DCO }} up -d db --wait

[group('alembic')]
alembic-commit *args: (alembic "revision --autogenerate" args)

[group('alembic')]
alembic-commit-migrate *args: (alembic "revision --autogenerate" args) alembic-migrate

[group('alembic')]
alembic-migrate *args: (alembic "upgrade head")

# 重置資料庫
[group('alembic')]
alembic-reset-db: (alembic "downgrade base") (alembic "upgrade head")
