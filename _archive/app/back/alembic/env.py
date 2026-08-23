"""Alembic 환경 (KDEV-WORK-011).

DB URL 은 alembic.ini 가 아니라 config.database_url() 이 SoT — 코드/컨테이너와 단일 출처.
target_metadata = core.db.Base.metadata (models import 로 테이블 등록).
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import config as app_config
from core.db import Base
import core.models  # noqa: F401 — User 등 모델을 metadata 에 등록

config = context.config
config.set_main_option("sqlalchemy.url", app_config.database_url())

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=app_config.database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
