"""파이프라인 정의 — 어떤 입력이 어떤 스테이지를 거치는가 (KDEV-WORK-014 P3 / KDEV-SPEC-008).

**정의는 데이터다**(KDEV-DEC-011 D2). 입력 종류가 늘어도 게이트 종류를 스키마 enum 에
추가하지 않고 여기에 정의를 등록한다 — `gates.stage_name` 에 CHECK 를 안 건 이유다.

저장 위치는 **코드 상수**로 정했다(SPEC-008 §7 OQ 해소). DB 테이블로 두면 얻는 것은
"마이그레이션 없이 스테이지 순서 변경"인데, 정의를 고치는 사람이 한 명뿐이라 그 이점이
아직 값을 못 한다. 테이블만 둘 늘어난다.

옮길 시점을 미리 정해 둔다 — **소스 종류가 3개를 넘거나**, **화면에서 정의를 편집**하고
싶어질 때. 그때도 데이터 마이그레이션은 없다(정의가 코드에만 있으므로 옮기기 쉽다).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Stage:
    name: str
    #: `auto` 는 승인 대상이 아니다 — 실패하면 재시도한다.
    kind: str
    #: route 판단에 따라 생성되지 않을 수 있다.
    optional: bool = False

    @property
    def is_gate(self) -> bool:
        return self.kind == "gate"


@dataclass(frozen=True)
class Pipeline:
    source_kind: str
    stages: tuple[Stage, ...]

    def gate_stages(self) -> tuple[Stage, ...]:
        return tuple(s for s in self.stages if s.is_gate)

    def auto_stages(self) -> tuple[Stage, ...]:
        """게이트 앞의 자동 준비 스테이지들 — 정의 순서대로.

        **이 값을 실제로 읽기 시작한 것은 WORK-017 P2 다.** 그전까지 준비부는
        "수집 1회 + 요약 1회" 로 굳어 있어서, 여기 `auto` 가 둘 적혀 있어도
        아무도 보지 않았다. 잔디는 셋(`collect`·`investigate`·`compose`)이라
        정의를 읽지 않고는 돌릴 수 없다.
        """
        return tuple(s for s in self.stages if s.kind == "auto")

    def first_gate(self) -> Stage | None:
        gates = self.gate_stages()
        return gates[0] if gates else None

    def stage_no(self, name: str) -> int:
        """체인 내 순번(1-base). 정의에 없는 이름이면 `ValueError`."""
        for index, stage in enumerate(self.stages, start=1):
            if stage.name == name:
                return index
        raise ValueError(f"{self.source_kind} 파이프라인에 '{name}' 스테이지가 없다")


YOUTUBE = Pipeline(
    source_kind="youtube",
    stages=(
        Stage("collect", "auto"),
        Stage("summarize", "auto"),
        # route 가 아래 셋의 생성 여부를 결정한다 — 체인 길이는 여기서 정해진다.
        Stage("route", "gate"),
        Stage("source_note", "gate", optional=True),
        Stage("concept", "gate", optional=True),
        Stage("derived", "gate", optional=True),
    ),
)

DAILY_COMMIT = Pipeline(
    source_kind="daily_commit",
    stages=(
        # 조사는 LLM 이 아니다 — git 을 읽고 세는 일이다. `counts` 를 코드가 세는 이유이기도
        # 하다(SPEC-012 §5). WORK-017 P2 단계에서는 더미가 이 자리를 채우고, P5 에서
        # 진짜 git 조사로 갈아 끼운다. 더미가 SPEC-011 §4 계약을 통째로 내기 때문에
        # 그 교체가 이 스테이지 하나로 끝난다.
        Stage("collect", "auto"),
        # 유일하게 한 스테이지가 N 건을 제출한다 — 레포마다 하나씩.
        Stage("investigate", "auto"),
        Stage("compose", "auto"),
        # 게이트가 하나뿐이라 **승인이 곧 체인 종료이자 발행 트리거**다(SPEC-013).
        # route 게이트가 없는 이유는 목적지가 고정이라 고를 것이 없기 때문이다.
        Stage("daily", "gate"),
    ),
)

#: 등록된 정의. 블로그·스케줄은 해당 파이프라인을 만들 때 추가한다.
PIPELINES: dict[str, Pipeline] = {
    YOUTUBE.source_kind: YOUTUBE,
    DAILY_COMMIT.source_kind: DAILY_COMMIT,
}


def pipeline_for(source_kind: str) -> Pipeline | None:
    """정의가 없으면 `None`.

    없는 종류에 유튜브 정의를 갖다 붙이지 않는다 — 블로그에 `derived`(교안) 스테이지를
    열어 봐야 만들 것이 다르다. 정의가 없는 항목은 게이트 없이 큐에 남고, 그 상태가
    화면에 그대로 보이는 편이 조용히 엉뚱한 체인을 태우는 것보다 낫다.
    """
    return PIPELINES.get(source_kind)
