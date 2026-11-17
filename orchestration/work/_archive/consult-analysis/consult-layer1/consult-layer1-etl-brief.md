
# [etl] WORK-001 WP1 · WP2 — 1층 적재 · 대조 스크립트 (상담 DM → SQLite)

너는 **consult-analysis `etl` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석/orchestration/roles/consult-analysis/etl/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석` (코디 워크트리에 직접 탄다 — 코디가 같은 트리를 쓴다. allowed_paths 밖은 절대 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md` **0.2.0 accepted** ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `para/projects/summer-star/consult-analysis/30-work/work-001-layer1-load.md` ← WP1 · WP2 · 수용 기준 1 ~ 8
- `para/projects/summer-star/consult-analysis/10-decision/decision-001-two-layers.md` ← D-01 ~ D-15
- 원본: `reference/2026-11-16-linky-data/` (gitignore · **read-only**)

**기대는 개념**

- `para/areas/concept/db/medallion-architecture.md` — 1층은 펼치기만. 판단 칸(언어 · 국적 · 단계 · 자동응답 여부) 0
- `para/areas/concept/db/data-lineage.md` — 모든 행이 `source_file` + 순번으로 원본 자리로 돌아간다
- `para/areas/concept/db/pii-masking.md` — 출력 · 코드 · 리포트에 이름 · 본문 · 폴더명 · `thread_path` · `uri` 0

## 2. 배경

SPEC-001 0.2.0 이 확정됐다. 범위 = 인스타그램 DM(511방 · 7,094건) + 페이스북 메신저(1,405방 · 21,612건). 테이블 5개(`conversation` · `customer` · `message` · `attachment` · `reaction`). 분석의 중심은 **고객 문의**다 — 우리 계정은 발신 구분(`is_owner`)에만 쓰이고, 계정명은 채널별 규칙으로 원본에서 구한다(SPEC §4.3).

## 3. 계약

SPEC-001 전부. 특히:
- §2 스키마(칸 · 타입 · NULL · UNIQUE · FK · CHECK) 그대로
- §3 원본 키 43개 처분 — 모르는 키는 G-1 로 **멈춘다**. 통과시키는 `else` 금지
- §4 키 규칙 · §4.5 대체 키 순서(다시 돌려도 같은 id)
- §5 변환(이중 인코딩 · 시각 · 방당 파일 수) · §5.4 멈추는 자리 G-1 ~ G-12 전부
- §6 인자 `--source` · `--db` 필수 · `<db>.tmp` 뒤 바꿔치기 · 한 트랜잭션 · 출력은 건수와 규칙 번호만
- §7 건수 기준 전 줄 — `verify_layer1.py` 가 기준 · 원본 재집계 · DB 세 값을 비교

## 4. 먼저 읽을 핵심 파일

- 위 §1 문서. 원본 표본은 구조 확인용으로만 — 본문을 코드 · 주석 · 테스트 · 리포트에 옮기지 마라

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/consult-analysis/scripts/`
- `para/projects/summer-star/consult-analysis/data/` (gitignore — 생성물만)

(`scripts/.gitkeep` 은 지워도 된다. 시험용 가짜 방 JSON 은 `scripts/tests/` 아래 — 원본을 복사해 고치지 않는다 · 이름은 `<고객1>` 같은 자리표시)

## 6. 구현 단계

1. **WP1** `scripts/load_layer1.py` — SPEC §1 ~ §6. 끝에 테이블별 행 수
2. **WP2** `scripts/verify_layer1.py` — 적재 코드를 **import 하지 않고** 원본을 따로 다시 센다. §7 전 줄 · 전부 같으면 종료 0 · 아니면 1
3. 멈추는 자리 시험: `scripts/tests/` 에 가짜 방 JSON 으로 G-1 ~ G-12 각각 멈추는지(표준 라이브러리 `unittest`)
4. 실행:
   ```
   python3 -I para/projects/summer-star/consult-analysis/scripts/load_layer1.py --source reference/2026-11-16-linky-data --db para/projects/summer-star/consult-analysis/data/layer1.sqlite
   python3 -I para/projects/summer-star/consult-analysis/scripts/verify_layer1.py --source reference/2026-11-16-linky-data --db para/projects/summer-star/consult-analysis/data/layer1.sqlite
   ```
5. WORK-001 수용 기준 1 ~ 8 을 하나씩 확인(6 = 두 번 적재해 같음 · 7 = 원본 파일 수 · 총 크기 앞뒤 같음)

## 7. 범위 제약 — 하지 말 것

- 2층 금지(언어 · 국적 · 예약 단계 · 자동응답 판별 칸 · 뷰 전부)
- SPEC · WORK · DEC 수정 금지 — 기준과 다른 값이 나오면 **스크립트를 기준에 맞추지 말고** 원본에서 어느 쪽이 틀렸는지 확인해 질문 채널로
- 외부 패키지 0(표준 라이브러리만) · 원본 폴더에 쓰기 0
- 출력 · 코드 · 주석 · 테스트 · 리포트에 고객 이름 · 계정명 · 본문 · 폴더명 0

## 8. 검증

```
python3 -I 로 적재 스크립트 1회 실행 → 원본 대비 건수 대조표(방 · 메시지 · 첨부 종류별)가 SPEC 기준과 전부 일치. 표준 라이브러리만(sqlite3 · json). 검증은 1회만
```

- verify 출력 전체(줄마다 기준 · 재집계 · DB · 일치)를 보고 본문에 붙인다 — 건수뿐이라 붙여도 된다
- 고객 정보 0 검사: 두 스크립트 출력 + `scripts/` 전체를 원본 `participants[].name` 전체 · 방 폴더명 전체(메모리에서만)와 대조 → 일치 0. 3자 이하 일반 낱말 오탐은 따로 적는다
- `git status --short --ignored` 로 DB 가 `!!`(ignored)인지 확인
- `python3 -I -m unittest discover -s para/projects/summer-star/consult-analysis/scripts/tests` 통과

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "etl 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c \
  --text "[worker_done] etl 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] etl: <질문>" --enter`
