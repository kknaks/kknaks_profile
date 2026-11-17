
# [planner] SPEC-001 1층 스키마 · WORK-001 1층 적재 — 인스타그램 상담 DM

너는 **consult-analysis `planner` 워커**다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석/orchestration/roles/consult-analysis/planner/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석` (코디 워크트리에 직접 탄다 — 코디가 같은 트리를 쓴다. allowed_paths 밖은 절대 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/consult-analysis/10-decision/decision-001-two-layers.md` ← **결정의 SoT (accepted).** 여기 없는 정책은 발명하지 마라.
- `para/projects/summer-star/consult-analysis/00-baseline/baseline-001-consult-data.md` ← 원본 실측(코디네이터가 센 값 · 대략치 포함)
- `para/projects/summer-star/consult-analysis/README.md` ← 위치 · PUBLIC 주의
- 원본: `reference/2026-11-16-linky-data/` (gitignore · **read-only** · 1.8G). 대화 JSON 은 `your_instagram_activity/messages/{inbox,message_requests}/<방>/message_*.json`

**기대는 개념**

- `para/areas/concept/db/medallion-architecture.md` — 1층 = 원본을 펼치기만 한 층, 2층 = 판정 층. 1층에 판단을 섞지 않는다
- `para/areas/concept/db/data-lineage.md` — 1층 모든 행이 원본 파일 · 위치로 거슬러 올라갈 수 있어야 한다(원본 경로 · 순번 칸)
- `para/areas/concept/db/db-normalization.md` · `surrogate-key.md` — 방 · 고객 · 메시지 키를 어떻게 잡는지
- `para/areas/concept/db/pii-masking.md` — 문서는 PUBLIC. 실명 · 본문 예시 금지, 구조와 건수만

## 2. 배경 / 무엇을 바꾸나

지금 상태: 원본(Meta 내보내기 JSON)만 있고 스키마 · 스크립트가 없다. DEC-001 로 「1층(원본 정규화) 먼저, 판정(2층)은 나중」이 확정됐다.

이번 일: etl 워커가 그대로 구현할 수 있는 **SPEC-001(1층 SQLite 스키마 + 원본 필드 대응 + 건수 기준)** 과 **WORK-001(적재 작업 · 수용 기준)** 을 쓴다. 2층(라벨 · 예약 단계 · 국적)은 이번 범위가 아니다 — SPEC 에 「2층에서 붙는 자리」만 한 줄로 남긴다.

## 3. 계약

SPEC-001 이 etl 워커의 계약이 된다. 최소한 아래가 들어가야 한다.

1. **테이블 4개**(DEC-001 D-02): `customer` · `conversation` · `message` · `attachment`. 칸 이름 · 타입 · NULL 여부 · 키 · FK
2. **원본 필드 대응표 — 빠짐없이.** 원본 JSON 에 나오는 키를 **전부** 세어(방 최상위 · `participants[]` · `messages[]` · `photos[]`/`share`/`reactions[]`/`files[]`/`videos[]`/`gifs[]`/`audio_files[]` 안쪽 키까지) 각각 「어느 테이블 · 어느 칸」 또는 「버림 + 이유」로 처분한다. 기준: **담을 칸 없는 원본 키 0.** BASE-001 의 키 목록은 코디네이터 대략치다 — 너가 원본 510개를 직접 세어 확정한다
3. **키 규칙**: 방 키(폴더명 · `thread_path` 중 무엇을 쓰나), 고객 키(509방 1:1 · 2명이 방 2개 · 상대 없는 방 1개를 어떻게 담나), 메시지 순번(같은 `timestamp_ms` 가 있을 때), 우리 계정 판별(`sender_name` 이 우리 계정인지 — 계정명을 하드코딩하지 말고 규칙으로)
4. **변환 규칙**: 이중 인코딩 복원(D-04)을 어느 칸에 적용하나, 시각(ms → 저장 형식 · 시간대), `message_*.json` 이 방당 여러 개일 수 있는지 확인 결과
5. **reactions · share** 를 별도 테이블로 뺄지 `message`/`attachment` 에 담을지 — 4개 테이블 밖으로 늘려야 하면 **옵션 + 권장**으로 미결에 올린다(혼자 정하지 마라)
6. **건수 기준(D-03)**: 적재 후 맞아야 하는 수 — 방 · 메시지 · 첨부 종류별. 너가 원본에서 직접 센 값으로 적는다
7. 실행 인터페이스: 스크립트 위치(`scripts/`) · 인자(원본 경로 · DB 경로) · 재실행 시 동작(DB 새로 만들기 권장) · 표준 라이브러리만

## 4. 먼저 읽을 핵심 파일

- 위 §1 세 문서
- 원본 JSON 표본 몇 개(inbox · message_requests 각각, 첨부 있는 방 · `is_pending` 있는 방 포함) — 구조 확인용. **본문을 문서에 옮기지 마라**
- 다른 프로젝트 SPEC 형식 참고: `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 의 frontmatter · 절 구성 (형식만)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/consult-analysis/20-spec/`
- `para/projects/summer-star/consult-analysis/30-work/`

(원본 폴더에 파일 생성 금지. 원본을 세는 임시 스크립트는 `/tmp` 가 아니라 너 세션의 스크래치 경로나 메모리 안에서 — 레포에 남기지 마라. 원본을 읽는 Python 은 `python3 -I`)

## 6. 구현 단계

1. §1 문서 읽기 → 원본 키 전수 집계(510개 전부)
2. `20-spec/spec-001-layer1-schema.md` 작성 (frontmatter: type spec · id SPEC-001 · version 0.1.0 · status draft · links → DEC-001 · BASE-001). §3 의 1~7 을 전부 담는다
3. `30-work/work-001-layer1-load.md` 작성 — etl 단계(WP) · 수용 기준(건수 대조표 전부 일치 · 표준 라이브러리 · 출력에 고객 정보 0) · 검수(reviewer) 단계. 2층은 범위 밖으로 명시
4. `20-spec/README.md` · `30-work/README.md` 인덱스에 행 추가
5. §8 검증

## 7. 범위 제약 — 하지 말 것

- 2층(언어 · 국적 · 문의 유형 · 예약 단계) 설계 금지 — 자리 한 줄만
- 스크립트 작성 금지(etl 워커 몫)
- DEC-001 · BASE-001 · README 수정 금지 — 고칠 게 보이면 미결로 보고
- 고객 이름 · 메시지 본문 · 사진 내용을 문서에 쓰지 않는다. 예시가 필요하면 `<고객명>` 같은 자리표시로

## 8. 검증

```
SPEC 의 모든 절이 BASE-001 실측 · DEC-001 중 하나를 근거로 가리킨다. 원본 필드 대응표는 원본 JSON 을 직접 열어 확인한 것만. 근거 없는 정책 0 · 열린 것은 열린 것으로. 인덱스 갱신. public — 고객 이름 · 본문 인용 0(grep)
```

- 추가: 대응표에 처분 안 된 원본 키 0 (집계 결과와 표를 대조한 수치를 보고에)
- 추가: 고객 이름 grep — 원본 `participants[].name` 전체 목록을 메모리에 올려 SPEC · WORK 파일에 하나라도 나오는지 검사, 0 이어야 한다(목록 자체는 어디에도 쓰지 않는다)
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
