"""온톨로지 데모 설정.

데이터·DB 경로와 LLM 경로(open-kknaks — ADR-04) 설정. 값 하드코딩 금지 — 전부 여기 경유.
원천 데이터는 PII 포함이라 레포 밖(gitignore) — 기본값은 코디 워크트리 기준이며,
워커·다른 환경은 ONTOLOGY_DATA_DIR 로 지정한다.
"""

import unicodedata
from dataclasses import dataclass
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SourcePaths:
    """원천 배치 규약 — `data_dir` 하위 고정(기록 04·05 의 산출 위치 그대로).

    **원천 경로의 단일 원천이다.** 적재기·빌드·게이트가 경로를 다시 조립하지 않고
    전부 여기를 지난다 — 규약이 두 곳에 있으면 한쪽만 고쳐지는 날 조용히 어긋난다.
    """

    data_dir: Path

    @property
    def vegas_dir(self) -> Path:
        return self.data_dir / "bronze" / "vegas"

    @property
    def nexus_dir(self) -> Path:
        return self.data_dir / "bronze" / "nexus"

    @property
    def reviews_csv(self) -> Path:
        """리뷰 원천 CSV 1건. 파일명에 지점·수집일이 박혀 있어 이름으로 찾는다.

        macOS 는 파일명을 NFD 로 저장해 한글이 자모로 분해된다 — 정규화하고 비교한다.
        """
        matches = sorted(
            p for p in self.data_dir.glob("*.csv")
            if "리뷰" in unicodedata.normalize("NFC", p.name)
        )
        if not matches:
            raise FileNotFoundError(f"리뷰 CSV 를 찾지 못했다: {self.data_dir}/*리뷰*.csv")
        return matches[0]

    @property
    def scoring_dir(self) -> Path:
        """LLM 채점 산출물(기록 04 7장 항목 4). 재채점하지 않고 이 산출물을 쓴다."""
        return self.data_dir / "silver" / "_scoring"

    @property
    def ontology_dir(self) -> Path:
        return self.data_dir / "ontology"


def sources_for(data_dir: Path | None = None) -> SourcePaths:
    """원천 경로 묶음. `data_dir` 를 주면 그 경로 기준, 없으면 설정값 기준."""
    return SourcePaths(data_dir if data_dir is not None else settings.data_dir)


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

    @property
    def sources(self) -> SourcePaths:
        """원천 경로 묶음 — 규약은 `SourcePaths` 하나가 갖는다."""
        return SourcePaths(self.data_dir)


settings = Settings()
