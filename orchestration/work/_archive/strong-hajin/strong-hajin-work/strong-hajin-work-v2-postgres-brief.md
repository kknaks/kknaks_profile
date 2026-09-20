# WORK002 PostgreSQL 동시성·스키마 검증 분담

## 1. 역할·위치
코드 워크트리 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work 의 PG 검증 담당. 원BE가 제품/공통테스트/SQL/Phase6를 수정하고, 계약워커가 SQLite/API 신규파일을 쓰는 동안 너는 PostgreSQL 테스트만 담당한다. 신규 워크트리/브랜치/커밋/push/PR 금지.
원BE term_c2b0c982-7078-4d5b-b14d-9342eef7f699, 계약워커 term_84ab1149-5aef-4981-aa60-2c48e3be004c. 제품결함은 둘과 코디에 단문 근거를 전달하고 직접 제품을 고치지 않는다.

## 2. 입력
코드 AGENTS.md. docs /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md Phase1/3/5/8 및 §8 검증, 같은 제품 20-spec/spec-003-task-lifecycle-v2.md §3 S-16, §4/5/6 C1·C2. 이 문서들이 계약이다. 코드는 구현 실물이며 기대값의 유일한 출처가 아니다. 원BE브리프 전체를 다시 조사할 필요 없음.

## 3. 범위
1. backend/tests/integration/postgres/ 기존 8파일의 v2 계약 변경에 필요한 픽스처/단언만 갱신한다. W1 보장을 삭제/skip/약화하지 않고 새 계약으로 정확히 대체한다. 관련 없는 자료worker 실패는 원인 증거로 분리하고 timeout 올리기/오류무시로 숨기지 않는다.
2. 같은 디렉터리에 test_task_lifecycle_v2_postgres.py 등 신규 파일을 추가해 C2 실제 경합을 검증한다:
   - 같은 요청 수락 vs 철회: 같은 원회차, 둘 다 적용되지 않음, 승자 우선순위 임의 고정 금지(EU17).
   - 담당교체 수락 vs 거절: active 최대1이고 공백없음, 원자적으로 이전종료/새활성, 같은답 동시재전송은 영수증이며 판정/담당 중복없음.
   - 상위완료 vs 하위재개: 완료된 상위 아래 열린 하위가 생기지 않음. 결정적 barrier/event로 경쟁을 실제 유발하고 우연히 순차로 돈 것을 동시성 증거로 쓰지 않는다.
   - 생성 같은키 동시호출의 1Task/1Request 및 current권한 재검사. 기존 정확한 테스트가 있으면 중복하지 말고 이름으로 연결한다.
3. WORK Phase1 기존표 인덱스 결손 재현: 아래 격리DB에서 대상 인덱스를 내리고 schema_sync만으로 복구 안됨을 확인, manual/2026-09-17-w2-indexes.sql 적용·반복적용·pg_index validity 확인. concurrent판도 같은 정의인지 비교하고 트랜잭션 밖 autocommit으로 적용/재적용/valid 확인, transaction안에서는 못도는 제약을 검증한다. SQL 파일은 고치지 말고 문제시 원BE에 알린다.
4. 신규 work_requests.parent_task_id FK(use_alter 포함) 및 supersedes FK, 신규 표/컬럼과 active부분unique/pending제안unique가 실제 PostgreSQL에 존재·valid인지 확인하고 잘못된 행이 거절되는 의미있는 사례를 남긴다. SQLite 선언이나 create_all 호출성공만을 근거로 삼지 않는다.

## 4. 데이터·실행 경계
격리 DB **ax_test_v2_pg**만 생성/초기화/fixture/인덱스 DDL을 수행한다. 기존 이 워크트리 PostgreSQL localhost:54329 사용, 기본5432는 다른 프로젝트라 접근금지. 사용자 ax_demo 및 기존 ax_test_w1/ax_test 데이터 수정금지. PostgreSQL 서버/사용자 스택/포트·프로세스 시작·종료 금지. 필요시 동일54329 postgres 관리DB에는 격리DB 생성 확인만, 다른 사용자 데이터조회/변경금지.
DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_demo 와 POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_v2_pg 를 명시해서 둘이 다름을 확인한다. 기존 PG 테스트는 reset_database가 있으므로 실제 연결대상을 두 번 확인한다.
최종 make test-postgres는 전체 새코드 PG결과이며 기준선65pass를 재사용하지 않는다. 지금 원BE가 SQLite 계약 테스트를 수행 중이므로 무거운 최종실행 전에 코디·BE에 시작을 알리고 부하를 겹치지 않게 조율한다.

## 5. 최근 결함·정정
- 원BE가 PG 디렉터리 미착수·소유권 이전을 확인했다. 단 test_material_owners.py, test_material_upgrade.py, test_postgres_assignment_decision_replay.py, test_postgres_integration.py 의 기존 M 표시는 W1 미커밋 변경이다. v2-code-baseline/manifest.json 해시와 동일함을 확인한 기준선이며 HEAD로 되돌리거나 v2 변경으로 오인하지 않는다. SQL 두 파일은 원BE 소유, 적용검증만 한다.

- 재배정 이전 active→superseded를 flush한 뒤 newactive로 만들어 부분unique UPDATE순서 오류를 고쳤다(동일tx, 격리읽기에서 공백없음 검증).
- 승인후재개 _as_utc로 SQLite naive/aware비교정렬, PG aware의 유효승인회차 판정 보존 필요.
- 실제 HTTP response_model이 신규derived/시간/child_progress를 자르던 결함 고침. 검증은 실제응답과DB 양쪽.
- 원BE가 현재 영수증 처리 정정 중: 같은 actor/command/원expected_version/같은답 재전송은 현재읽기권한 재검사 후200영수증+effect0, 다른회차/다른답은 충돌. 최신version을 다시 조회해 보내는 것은 재전송이 아니다. 새멱등키를 상태명령에 요구하지 않는다(생성/발송만key필수).
- 요청자조상읽기는 requester_id/promoted_by 본인만. CC직접요청읽기 기존규칙이 하위전체로 확장되지 않는다. 요청읽기권한 회수시 관계로열린목록/상세/자료 함께닫힘(다른독립권한보존).

## 6. 미정
OQ203 완료보고 하위선차단은 새로걸지 않고 현행보존, 최종승인은 반드시막음. OQ206 회의시스템요청 승인자 임의지정/자동승인 금지. 선행후행 강제·부모취소후수락 우선순위 등 미정을 테스트로 확정하지 않는다. 실제운영DB 빈데이터 여부는 이번PG fixture통과와 다른 사안이며 배포직전 실데이터재확인 조건은 남긴다.

## 7. 허용 파일·명령
backend/tests/integration/postgres/ 전체만 쓰기 가능. 보고서 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-work/v2-postgres-report.md. 제품/공통conftest/legacy_acceptance/Makefile/migrationSQL/FE/제품문서 무수정. 공통fixture 문제가 있으면 원BE가 고친다.
테스트 진입은 **make test-postgres만**, PYTEST_ADDOPTS의 -k로 신규/실패 파일을 좁혀 실행. 직접 uv run pytest 금지. make 직후 실제 rc를 보존하고 full stdout/stderr와 .exit를 /tmp/v2-pg-logs/에 남긴다. 최종 소유PG 전체1회, 이유없는반복금지. 전체 make verify는 코디소유.

## 8. 보고·완료
C1/C2 세경합·schema/index/FK별 테스트명·실제DB·명령/exit·증거·미완료를 표로 적는다. 제품결함은 실패테스트를 유지하고 원BE 수정후 해당묶음 재확인. 인수조건과 무관한 대량새테스트 금지. 브라우저E2E 미실행. 두채널 완료 후 idle. 신규워커 발주금지.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_2e64fd06-507c-460d-accd-2c91b8863dd8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "postgres 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] postgres 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] postgres: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
