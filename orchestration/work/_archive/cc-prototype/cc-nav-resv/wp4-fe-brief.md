# [frontend] WP4-FE — 예약관리 화면 `/reservations` (시안 「Ceramique 예약관리 v1」 그대로)

너는 **cc-prototype `frontend` 워커**다(WP1 · WP2 를 한 그 워커). 역할 문서는 이미 읽었다.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/cc-nav-resv` — WP1 · WP2 변경은 미커밋으로 남아 있다. 되돌리지 마라.

⚠ backend 워커가 같은 워크트리 `cc/back/` 에서 WP4-BE(`/api/reservations`)를 **지금 만들고 있다** — `cc/back/` 은 건드리지 마라. 계약(아래 §3)대로 짓고, BE 가 끝나면 코디가 실제 응답 예시를 보내 준다. 그 전에 끝나면 계약 기준으로 마치고 「BE 실응답 대조 pending」으로 보고.

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/20-spec/spec-002-cc-nav-reservation.md` (0.2.0) **§3 전부** ← 계약의 SoT
- 화면 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/design-upload/Ceramique 예약관리 v1.dc.html` — 장면 9개(`scene` prop). 문구 · 칸 · 상태 색 · 모달 · 데모 상자 모양 **그대로**
- 시안 해설: `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/orchestration/work/cc-nav-resv/design-report.md` §A(장면별) · 「와이어와 바꾼 것」
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc프로토타입/para/projects/summer-star/cc-prototype/10-decision/decision-004-cc-nav-reservation.md` D-10 ~ D-21 — 특히 **D-21: 1차 화면 · 컴포넌트 모양을 고치지 마라. 새 화면은 1차 front 의 medikit 컴포넌트(Button · Modal 등) · Ceramique 테마 · 1차 화면 관례(`cc-btn` · `text-typo-*` · `text-ms-*` 등)로 짓는다**
- KOS 카드 모양(스크린샷 모달) 참고: 시안의 스크린샷 모달이 정본. 실제 캡처 파일은 열 필요 없다

## 2. 배경

예약관리는 데모다. 데모 버튼이 Linky 요청을 대신 만들고, 병원이 [KOS 등록하기] → 미리보기 → [등록하기] → 확정 · 스크린샷, 또는 [변경 요청하기](사유 텍스트) → 본사가 고친 수정 요청 → [KOS 수정하기] → 수정 확정. 지금 `/reservations` 는 WP1 의 빈 페이지다 — 이걸 채운다.

## 3. 계약 (BE 와 합의 — 이대로 쓴다)

SPEC-002 §3.1 · §3.2. 응답 키는 §3.1 필드 이름(camelCase).
- `GET /api/reservations` → `{ rows: ResvRequest[], counts: { needCheck, changeRequested, confirmed, total }, version }` — rows 는 묶음(`groupId`) 단위 최신 묶음이 위, 묶음 안은 오래된 줄이 위
- `POST /api/reservations/demo/request` · `POST /api/reservations/demo/modify`(대상 없으면 409) · `POST /api/reservations/{id}/register` · `POST /api/reservations/{id}/change-request` `{reason}`(빈 사유 400) — 응답 `{version}`
- 갱신 = 1차와 같은 SSE(`/api/events`) 알림 → 다시 읽기(1차 `useLive` 방식)
- [링키 수정 요청 생성] 막힘 판단: rows 에 `change_requested` 또는 `confirmed`/`modified` 줄이 있는가(BE 409 는 보조)
- 스크린샷 모달 = `snapshot` 값을 시안 KOS 카드 모양 HTML 로. `snapshot` 이 null 인 superseded 줄 = 「KOS 등록 전에 바뀌어 스크린샷이 없어요」

## 4. 먼저 읽을 핵심 파일

- `cc/front/app/(main)/reservations/page.tsx` — WP1 빈 페이지
- `cc/front/lib/api.ts` · `lib/types.ts` · `lib/hooks.ts`(`useLive` · `useWide`) — API · 타입 · 실시간 갱신 관례
- `cc/front/components/desk/CheckInModal.tsx` · `ResvDetail.tsx` · `useDeskActions.ts` — 1차 모달 · 토스트 · 조작 관례(같은 모양으로)
- `cc/front/components/desk/Aside.tsx` `VisitChip` — 첫 방문/재내원 칩 재사용

## 5. allowed_paths

- `cc/front/`

## 6. 구현 단계

1. 타입 · API 함수(`lib/`) — §3 계약
2. `/reservations` 화면 — 시안 장면 1~7: 제목 · 요약 칩 · 데모 상자 · 테이블(본사 요청 | 병원 상태 | 비고) · 묶음 머리(이력 2건 이상) · 수정 줄 이어 붙임(↳ · 취소선 → 새 값) · 빈 상태
3. 모달 — KOS 등록/수정 미리보기(수정은 바뀐 항목 강조) · 스크린샷 · 변경 요청(사유 비면 막힘)
4. 토스트 · 새 줄 강조 · 버튼 중복 클릭 막기
5. 폭 < 760px 은 가로로 넘치지만 않게(시안 없음)
6. 1차 [초기화](현황판)가 예약도 비운다 — 예약관리 화면은 SSE 로 따라 비워지는지

## 7. 하지 말 것

- 1차 화면 · 공용 컴포넌트 모양 변경(재사용은 OK, 고칠 필요가 있으면 질문)
- 시안에 없는 기능 · 문구 발명
- `cc/back/` · 사용자 포트 · 프로세스(코디의 3610/8610 서버 포함)

## 8. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 가 없는지 확인. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 보고에: 시안 장면 1~7 ↔ 구현 대응 표 · 재사용한 1차 컴포넌트 · 시안과 다르게 한 곳(이유)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_adf432d6-a97d-4457-a02d-041df0075fb7 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend(WP4) 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 \
  --text "[worker_done] frontend(WP4) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_adf432d6-a97d-4457-a02d-041df0075fb7 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
