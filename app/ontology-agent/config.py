"""온톨로지 데모 설정.

데이터·DB 경로와 LLM 경로(open-kknaks — ADR-04) 설정. 값 하드코딩 금지 — 전부 여기 경유.
원천 데이터는 PII 포함이라 레포 밖(gitignore) — 기본값은 코디 워크트리 기준이며,
워커·다른 환경은 ONTOLOGY_DATA_DIR 로 지정한다.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ONTOLOGY_", env_file=".env", extra="ignore")

    # 데이터 — 원천(bronze/silver/gold/ontology/scripts)과 산출 DB
    data_dir: Path = _REPO_ROOT / "reference" / "ontology_demo"
    db_path: Path | None = None  # 미지정 시 data_dir/db/ontology_demo.db

    # LLM 경로 — open-kknaks (ADR-04: SDK 직접 import 금지)
    redis_url: str = "redis://localhost:46379/0"
    ai_namespace: str = "ontology_demo"
    ai_queue: str = "ontology"
    ai_provider: str = "codex"
    ai_model: str = "gpt-5.6-terra"
    ai_timeout_sec: int = 180

    @property
    def resolved_db_path(self) -> Path:
        return self.db_path or (self.data_dir / "db" / "ontology_demo.db")


settings = Settings()
