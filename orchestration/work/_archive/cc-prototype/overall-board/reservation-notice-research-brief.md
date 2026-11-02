# [researcher] 예약 현황 공지 [수정하기] — KOS 공지 쓰기 확인 (HAR + 데모 실호출)

너는 **cc-prototype `researcher` 워커**다. **앞 판의 맥락이 없다** — 이 브리프와 아래 파일만 믿어라. 먼저 역할 문서를 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc` (코디 워크트리 — 공유. allowed_paths 밖은 건드리지 마라)

## 1. SSOT — 먼저 읽을 것

- HAR(**데모 테넌트** — 코디 확인): `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/공지사항.har` — 사용자가 KOS 웹 「병원 공지사항」에서 [수정하기] → 저장(+ 새 공지 쓰기)을 했다. 요청 = `get-roles` · `meta/notice/v1/queries/get-notices` · `meta/notice/v1/commands/change-content`
- 지금 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md` 의 공지 절(공지 = **그 날짜의 KOS 공지** · 스케줄 표 날짜와 같이 움직임 · 지금은 읽기 전용)
- 지금 코드(읽기만): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/back/app/kos/reservation_sync.py` · `app/service/reservations.py` · `app/schemas/reservations.py` 의 notice 부분, front 공지 패널(`procedure/front` 에서 grep `notice`)
- 내부 API 인증 방식: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md` 「인증 · 계정」(시스템 계정 sign-in → Bearer). 계정 값은 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/.env` 를 **읽기만**(출력 · 리포트에 값 금지)
- 시안 공지 [수정하기/저장]: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/design-prev/Ceramique 전체현황판.dc.html` `M:170-176` 근처(배치 참고만 — 웹은 구현본이 정본)

기대는 개념: 해당 없음.

## 2. 배경

예약 현황 오른쪽 패널 공지에 [수정하기]를 넣는다(사용자 결정 · E2E batch 2 #3). 저장 = **KOS 공지(그 날짜) 쓰기**. 쓰기 API 를 몰라 보류했고, 이제 HAR 이 왔다.

## 3. 계약

해당 없음(조사). 결과는 planner 가 SPEC-005 에 옮긴다.

## 5. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-notice-report.md` — 리포트 1개. 그 밖은 쓰지 마라(코드 · SPEC 수정 금지)

## 6. 할 일

1. **HAR 해부**(값은 모양만): `get-notices` 요청 · 응답 모양(필드 · 타입 · 날짜 범위 · 공지 여러 개인가 · 날짜별 하나인가) · `change-content` 요청 본문 모양 · 응답. **새 공지 쓰기**가 별도 명령인지, `change-content` 하나로 새로 쓰기 · 고치기를 같이 하는지(HAR 에 새 공지 쓰기가 있는지부터). 지우기 · 날짜 바꾸기가 있는지. 리치 텍스트(HTML)인지 일반 글자인지
2. **ccc 지금 읽는 값과 대조**: ccc 가 공지를 무엇으로 읽나(공개 · 내부 · 필드) ↔ 쓰기 API 가 가리키는 대상(id · 날짜)이 같은가
3. **데모 실호출 — 허가된 쓰기(이것만)**: 데모 테넌트에서 **앞으로의 날짜 하나**(2026-11-10 KST)에 대해 ① `get-notices` 로 그 날 공지 읽기 → ② `change-content` 로 `[ccc 시험] 공지 쓰기 확인` 쓰기(공지가 없으면 새로 쓰기 경로 — HAR 대로) → ③ 다시 읽어 반영 확인 → ④ 내용을 한 번 더 고쳐 덮어쓰기 확인 → ⑤ 원래 내용으로 되돌리기(원래 없었으면 비우기 · 지우기 경로가 있으면 그것). 전 · 후 응답 모양을 리포트에
   - 시작 전에 **테넌트가 데모인지 assert**(`.env` 의 데모 테넌트 값과 요청 경로 테넌트가 같은지 — 값은 출력 금지). 다르면 멈추고 물어라
4. 권한: `get-roles` 가 왜 같이 불리나(공지 쓰기 권한 확인?) · ccc 시스템 계정이 쓰기 권한이 있는지(③ 결과)
5. **「정할 것」**: Q-138 부터. 결정하지 마라(예: 같은 날 공지가 여럿이면 무엇을 고치나 · 동시 수정)

## 7. 하지 말 것

- **운영 명동점 키(`KOS_API_tenent`) 사용 금지** — 데모만. 허가된 쓰기는 §6.3 다섯 번뿐
- 리포트에 테넌트 id · 계정 · 토큰 · 사람 이름 · 공지 본문 실값 금지(모양 · 필드 이름 · 타입만). 이 레포는 public
- 코드 · SPEC 수정 금지

## 8. 검증

```
API 마다 근거(HAR entry 번호 · 웹앱 JS 위치) · 데모 호출 결과(상태 코드 · 반영 여부) · 리포트 id · 토큰 grep 0
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 브리프 작성 시점 값이다. preamble 과 다르면 **preamble 이 맞다.** preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_f235ff2f-91d3-4b96-a86f-78fcd7232b46 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

# (2) 직접 주입 — 코디를 깨운다
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 물어라:
  `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] researcher: <질문>" --enter`
