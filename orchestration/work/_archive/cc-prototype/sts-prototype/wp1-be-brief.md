# [backend] WORK-001 WP1 — cc/back 뼈대 · 시드 · 상태 · API · SSE · 로그인

너는 **cc-prototype `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` (브랜치 `kknaksss/sts-prototype`)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커가 같은 워크트리의 `cc/front/` 에서 병렬 작업 중 — `cc/front/` 는 건드리지 마라.**
너는 앞 맥락이 없다. 맥락은 아래 파일에만 있다.

## 1. SSOT — 먼저 읽을 것

- **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`** ← 계약의 SoT. **여기 없는 건 발명하지 마라.** 이번 판은 §1 · §3 · §4 · §5 · §6 · §8 · §9-1 · §9-5
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/30-work/work-001-cc-poc.md` — WP1 행
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/10-decision/decision-002-cc-poc.md` — 왜(D-09 · D-12 · D-13 · D-20~D-24 · D-26 · D-28 · D-29)
- **현황판 동작의 정본**: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/design/Ceramique 현황판 v3.dc.html` 의 스크립트 — `LAYOUT` · `capOf` · `statusOf` · `waitLabel` · `buildOrder` · `commit` · `assign` · `complete` · `removeStaff` · `place` · `checkIn` (줄 550~680 근처). 이 로직을 서버로 옮긴다
- 데이터 조사(시드 재구성 근거): 같은 폴더 `orchestration/work/sts-prototype/` 의 `research-cc-data-fit-report.md`(§B · §B-4 · §C-8) · `research-patient-detail-report.md`(§A 메모 양식 · §D) · `design-staff-r2-report.md` · `design-staff-r3-report.md`(샘플 고객 · 이름 치환 주의) · `room-map-provisional.md`(방 대응표)
- **KOS 캡처**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/reference/2026-10-12-cc-prototype/2026-10-12T161224-5b4603da` (= `CC_CAPTURE_DIR`) — 읽기만

**기대는 개념** — 해당 없음.

## 2. 배경

2026-10-16 지점 시연용 PoC. `cc/back` 은 아직 `.gitkeep` 뿐이다. 이번 판(WP1)은 통역을 **뺀** 백엔드 전부 — 시드 만들기, 현황판 상태를 서버가 들고 데스크·직원 화면이 SSE 로 같은 상태를 보게 하는 것. 통역(SPEC §7)은 WP2 다.

## 3. 계약 — frontend 워커가 이대로 소비한다

SPEC-001 §5.2 · §5.3 · §5.5 · §6 의 경로 · 메서드 · 필드 이름 그대로. 응답 모양을 바꿔야 하면 **먼저 `[질문]` 으로 물어라**(frontend 가 병렬로 이 계약을 쓰고 있다).
- 응답은 JSON, 필드는 camelCase. 오류는 `{ "error": { "code", "message" } }` + 4xx
- `GET /api/board` 응답에 시안 `renderVals` 가 쓰는 원재료(customers · staff · resv · rooms(LAYOUT + 대응) · version)를 담아라. 화면 계산(배지 색 등)은 front 몫
- 응답 어디에도 실제 고객 이름 · 전화 · 차트번호 · 생년월일이 없어야 한다

## 4. 먼저 읽을 핵심 파일

- 위 시안 스크립트의 `commit` — 모든 변경이 지나는 길(스냅샷 → 변경 → 큐 정리 → 타이머 리셋). 서버도 같은 순서로
- 캡처 `raw/getScheduleDetail/*.json` 몇 개 — 필드 트리는 data-fit 리포트 §B

## 5. allowed_paths — 이 밖은 건드리지 마라

- `cc/back/` 전부
- `cc/.env.example` 이 필요하면 `cc/back/.env.example` 로 둔다(루트 공용 파일 만들지 않는다)
- 레포 루트 `sts/` **삭제**(SPEC §8 · DEC-002 D-30)
- `cc/front/` · `cc/design/` · 레포 루트 다른 파일 금지

## 6. 구현 단계

1. `cc/back` 뼈대 — FastAPI · uv · Python 3.12 · router → service → repository · SQLite(`CC_DB_PATH`) · `.env.example`(SPEC §8 키 전부, 값 비움 — `SONIOX_API_KEY=` 포함) · `.gitignore`(`.env` · `data/`) · CORS(`CC_FRONT_ORIGIN`)
2. 시드 `python -m app.seed build --date 2026-10-09 --at 14:45` (SPEC §4.1) — 참조 데이터 적재 · 이름 치환 · 직원 · 현황판 상태 재구성 · `data/seed.json`
3. 상태 모델 · 조작(SPEC §5.1 · §5.3) — 시안 로직 이식 · `history` · `undo` · version
4. 읽기 API(§5.2) · 환자 상세 계산(§5.5 — 양식 파싱) · SSE `/api/events`
5. 로그인(§6) · reset(§4.2) · `seed save`(§4.3)
6. `cc/back/README.md` — 설치 · 시드 · 실행 명령(포트 8600)

## 7. 범위 제약 — 하지 말 것

- **KOS API 호출 금지**(어떤 것도). 캡처 원본을 `cc/back` 으로 복사하지 마라
- 통역(§7) 은 이번 판 아님 — WS 엔드포인트 만들지 마라
- 서버를 띄워 확인하려면 **8600 이 아닌 임시 포트**로, 끝나면 그 프로세스만 끈다. 사용자 포트 · 프로세스를 건드리지 마라
- 커밋 · push · PR 금지

## 8. 검증

```
cc/back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- **이번 WP 항목만 시험한다**(통합 시험은 WP5). 최소: 시드 build 가 10-09 로 돈다 · 응답 전체에서 캡처 `visitor.name` 177건 · 메모 「이름 :」 값 대조 0건 · assign/complete/place/checkIn/undo 각 1개 · reset 이 시드로 돌아감 · 환자 상세 ⚠ 주의가 오더·상담 양쪽에서 모임(design-staff-r2 의 예시 고객) · SSE 가 변경 때 version 을 보냄
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp1-be-report.md` (rules.md 형식) — 시드 재구성이 어색한 곳(근사)을 따로 적어라
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_eb0f5374-235a-4757-bb3a-1b2768c7e255 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
