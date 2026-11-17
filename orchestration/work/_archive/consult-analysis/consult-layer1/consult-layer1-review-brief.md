
# [reviewer] WORK-001 WP3 — 1층 적재 스크립트 검수 (read-only)

너는 **consult-analysis `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석/orchestration/roles/consult-analysis/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석` (코디 워크트리 · **read-only** — 리포 파일을 고치지 마라)

## 1. SSOT

- `para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md` 0.2.0 accepted ← 대조 기준
- `para/projects/summer-star/consult-analysis/30-work/work-001-layer1-load.md` ← WP3 검수 항목 ① ~ ⑦ · 수용 기준 1 ~ 8
- `para/projects/summer-star/consult-analysis/10-decision/decision-001-two-layers.md` ← D-01 ~ D-15
- 원본 `reference/2026-11-16-linky-data/` (read-only)

## 2. 검수 대상

- `para/projects/summer-star/consult-analysis/scripts/load_layer1.py`
- `para/projects/summer-star/consult-analysis/scripts/verify_layer1.py`
- `para/projects/summer-star/consult-analysis/scripts/tests/test_load_layer1.py`
- 생성물 `para/projects/summer-star/consult-analysis/data/layer1.sqlite` (gitignore)

## 3. 볼 것 — WORK-001 WP3 ① ~ ⑦ 전부 + 아래

1. 스키마(칸 · 타입 · NULL · UNIQUE · FK · CHECK)가 SPEC §2 와 같다 — DB 의 `sqlite_master` 를 직접 읽어 대조
2. 원본 키 43개가 코드에서 전부 처분된다 · 모르는 키는 G-1 로 멈춘다(통과시키는 `else` · `.get()` 로 조용히 버리는 경로 없음)
3. G-1 ~ G-12 가 전부 있고 시험이 각각을 실제로 건드린다(이름만 있는 시험 아님)
4. `verify_layer1.py` 가 적재 코드를 import 하지 않고, 기준값을 DB 에서 베끼지 않는다(기준은 SPEC §7 값 · 재집계는 원본에서)
5. **직접 다시 돌린다** — 아래를 **임시 DB 경로**(너 세션 스크래치 경로)로 실행해 274칸 일치 · 종료 0 확인. 리포의 `data/layer1.sqlite` 는 덮어쓰지 마라
   ```
   python3 -I para/projects/summer-star/consult-analysis/scripts/load_layer1.py --source reference/2026-11-16-linky-data --db <스크래치>/l1.sqlite
   python3 -I para/projects/summer-star/consult-analysis/scripts/verify_layer1.py --source reference/2026-11-16-linky-data --db <스크래치>/l1.sqlite
   ```
   그리고 `data/layer1.sqlite` 와 테이블별 행 수 · id 범위가 같은지(재현성 · 수용 기준 6)
6. 대체 키 순서가 SPEC §4.5 대로인지(표본 몇 개로 확인)
7. **고객 정보 0** — 스크립트 · 주석 · 시험 · 두 스크립트 출력에 원본 `participants[].name` · 방 폴더명 · 계정명 0(목록은 메모리에서만). 3자 이하 일반 낱말 · 보관함 이름(`inbox` 등) 오탐은 따로 적는다
8. 2층 값이 1층에 없다(언어 · 국적 · 단계 · 자동응답 칸 · 뷰 0)
9. 원본 폴더에 쓰기 0 · 외부 패키지 0
10. 고객 문의가 분석 중심이다 — `is_owner = 0` 메시지가 `customer_id` 로 빠짐없이 이어지는지(NULL 0)

## 5. allowed_paths

- 산출물 1개만: `orchestration/work/consult-layer1/review-layer1-report.md`
- 그 밖 리포 파일 수정 · 생성 금지

## 8. 검증 · 리포트 형식

- 판정 **PASS · WARN · FAIL**. 모든 지적에 `파일:줄` + 근거(SPEC 절 · DEC D-번호 · WORK 수용 기준 번호)
- 직접 돌린 명령과 결과 수치를 붙인다
- 리포트에도 고객 이름 · 본문 · 폴더명을 쓰지 않는다

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "reviewer 완료: <판정> <한 줄>" \
  --body "판정 / 지적 목록 / 직접 실행 결과 / 리포트 경로"

orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] reviewer: <질문>" --enter`
