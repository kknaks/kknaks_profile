# [PROCEDURE-HUB backend] 선택 관계·전역 메모 조회 구현

너는 PROCEDURE-HUB backend 코드 워커다. Orca dispatch preamble의 완료 보고 명령을 우선한다. 이 브리프 한 장으로 작업한다.

## 읽을 것

- 이 코드 레포 `AGENTS.md`, `.agents/skills/`의 관련 백엔드 규칙, `backend/README.md`, 관련 gold route/service/schema/tests
- 정본(코디 워크트리, 읽기 전용): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-005.md` 0.3.9 §5-5·§5-16·§6-9, `WORK-011.md`, `SPEC-006.md` 0.3.10 §3-4-1-5, `review-coverage-walk-spec-work-v2.md`

## 작업

WORK-011 WP-0~5를 구현한다. 현재 T4의 묶인 pairs/개수는 확정 단위 쌍의 resolved/claim/대안별 fact ID·원문·source·적용 범위를 보장하지 않는다. 확정 두 시술의 **선택 관계**를 반환하는 REST와 MCP의 공통 코어를 만들고, 방향·prior·조건부·sections·build·정규화 입력을 보존한다. `pair_scope.complete`의 found/empty/truncated/error를 실제 범위 완료에 맞춰 반환한다. claim/대안별 fact/source/적용 범위를 결속하고 Q139 전역 메모를 R8 edge owner와 별도 scope로 조회·완료 판정한다. 현재 T4는 회귀를 유지한다. 잘린/오류 응답을 empty나 complete로 오인하지 않는다.

Hub의 page=1 ID 순서, page≥2 `more`, 12줄, 40자/cut, peek 1쪽 bytes 계약을 유지하고 SPEC-005 §6-9 대표 사례를 시험한다. WORK-011의 64/32KiB는 제안치이므로 실제 응답 크기와 직렬화 비용을 재서 공개 schema/상한/오류 의미를 확정하고 결과를 코디에게 보고한다. Hub 호출별 상한을 앱 전체 탐색 상한으로 쓰지 않는다. 앱 SPEC-006 0.3.10은 고정 8/20/15KB 앱 탐색 배제를 폐기했다.

사용자 18005 포트와 `procedure-*` 컨테이너·개발/운영 DB를 조작하지 않는다. 격리 inprocess/별도 포트 시험만 한다. 원장 인용 본문을 공개 보고에 복사하지 않는다. 새 50/239×3 평가는 돌리지 않는다.

## 범위·검증

- 착수 때 HEAD `2edc190`, `git status --short`, 현재 Gold build hash를 기록한다. 차이가 있으면 조사해 코디에 알린다.
- 수정 허용: `backend/app/modules/gold/` 관련 파일, `backend/app/router/gold.py`, `backend/app/schema/gold.py`, `backend/app/swagger_docs/gold.py`, `backend/tests/test_gold_*`, `backend/tests/test_public_api_contract.py`, 새 선택 관계/전역 메모 시험. 다른 제품·프런트·설정/secret·DB 조작 금지. 필요 경로가 더 있으면 먼저 코디에게 보고한다.
- 의미 있는 시험: 확정 쌍/미확정 쌍/동일 ID/방향/prior/조건부, 묶인 pairs 속 단일 쌍, source 누락, Q139 별도 전역 메모, truncated/empty/error, 같은 build·정규화 입력 결정론, 기존 T4 회귀, 186 첫 쪽 ID 순서와 뒤 page 대표 사례. SPEC §6-9의 5문장/4질문과 Q139 scope를 fact ID로 확인한다.
- `uv run pytest`의 관련 gold 시험, `uv run ruff check` 만진 파일, 가능한 전체 unit suite(통합 DB 제외)를 실행한다. 환경 문제는 사유 보고. 코드 diff·시험 결과·공개 API JSON 예시·상한과 실제 측정·빌드 해시를 완료 메시지에 요약한다.
- 커밋·push·PR 금지. 완료 시 dispatch preamble대로 `worker_done` 한 번.
