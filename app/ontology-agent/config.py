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
    #: 모델과 **짝**이다 — 허용 effort 는 CLI 가 아니라 모델별로 갈린다. 모델을 바꾸면
    #: 그 모델이 받는 값인지 다시 재야 한다. `gpt-5.6-terra` + `low` 가 레퍼런스 통과
    #: 조합이다(조사 리포트 §5.6-3). `none` 은 금지 — 툴 연결 판단이 죽는다.
    ai_reasoning_effort: str = "low"
    #: 스키마 위반 시 재시도 횟수 (SPEC-005 OQ-5 — 1회 재시도 후 실패)
    ai_schema_retry: int = 1

    #: 워커 컨테이너에서 본 MCP 도구 서버 주소. `-c mcp_servers.<key>.url` 에 그대로 박힌다.
    mcp_url: str = "http://ontology-mcp:28081/mcp"

    #: 채팅 저장소 — **온톨로지 DB 와 다른 파일**이다(WORK-003 Domain 주석).
    #: 대화 기록이 브론즈~골드와 같은 파일에 앉으면 데이터 계층이 오염된다.
    chat_db_path: Path | None = None  # 미지정 시 온톨로지 DB 옆 ontology_chat.db

    # 접속 게이트 — 내부 공유용 비밀번호 하나(DEC-005 D2 · SPEC-003 §4).
    # **기본값을 두지 않는다.** 값은 배포 시 env 로만 주입하고 코드·문서·응답 어디에도 적지 않는다.
    # 미주입이면 인증 엔드포인트가 기동 시점에 명시적으로 거부한다(빈 비밀번호로 열리지 않게).
    demo_password: str = ""
    session_cookie_name: str = "ontology_demo_sid"
    session_max_age_sec: int = 60 * 60 * 24 * 30  # 30일 (SPEC-003 OQ-3)
    session_cookie_secure: bool = True

    #: 브라우저가 API 를 부를 수 있는 오리진. **프론트는 Vercel, API 는 홈서버라 배포에서
    #: 둘은 항상 다른 오리진이다**(DEC-005) — 이 목록이 비면 화면이 API 에 닿지 못한다.
    #: `credentials: include` 를 쓰므로 `*` 는 쓸 수 없다(브라우저 규칙) — 명시 목록이다.
    #: 로컬 기본값은 `next dev` 두 주소다. 배포 값은 env 로 주입한다.
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @property
    def session_cookie_samesite(self) -> str:
        """`secure` 에서 **파생**한다 — 손잡이를 늘리지 않는다.

        배포는 교차 사이트(Vercel → 홈서버)라 `Lax` 면 쿠키가 아예 안 실려 세션이
        성립하지 않는다. `None` 은 `Secure` 를 요구하므로 둘은 원래 한 몸이다.
        로컬 http(`secure=0`)에서는 `None` 을 브라우저가 거부하므로 `Lax` 로 내린다.
        """
        return "none" if self.session_cookie_secure else "lax"

    # MCP 도구 서버 (research §5.2)
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 28081
    mcp_server_key: str = "ontology"
    mcp_allowed_hosts: list[str] = ["*"]
    mcp_allowed_origins: list[str] = ["*"]

    @property
    def resolved_db_path(self) -> Path:
        return self.db_path or (self.data_dir / "db" / "ontology_demo.db")

    @property
    def resolved_chat_db_path(self) -> Path:
        """채팅 저장소 경로. 온톨로지 DB 와 **다른 파일**이다 — 같은 파일에 두면
        빌드가 DB 를 다시 만들 때 대화 기록이 함께 날아간다."""
        return self.chat_db_path or (self.resolved_db_path.parent / "ontology_chat.db")

    @property
    def sources(self) -> SourcePaths:
        """원천 경로 묶음 — 규약은 `SourcePaths` 하나가 갖는다.

        진입점은 `sources_for()` 하나다. 이 프로퍼티는 그쪽에 위임한다 —
        같은 규약을 두 번 조립하지 않는다(WORK-001 W9).
        """
        return sources_for(self.data_dir)


settings = Settings()
