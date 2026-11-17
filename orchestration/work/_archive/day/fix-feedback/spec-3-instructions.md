# [planner] spec-3 — 2루프: E2E 피드백 · F-5 · 검수 잔여를 스펙에

너는 앞 맥락이 없다. 먼저 읽어라:

1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-spec-brief.md` — 역할 · allowed_paths(`products/day/`) · 범위 제약(화면 문구 발명 금지 · 기획안 수정 금지) · 검증이 그대로 적용된다. (그 브리프의 「F-5 범위 밖」은 **이번에 뒤집혔다** — 아래 표가 우선.)
2. **사용자 결정 정본**: `…/fix-feedback/e2e-feedback.md` — 위 표 F-5 행 · 아래 「E2E 피드백」 E1 ~ E6 · `…/fix-feedback/_RESUME.md` §2 결정 표(2026-11-17 행 전부)
3. 앞 판: `spec-report.md` · `spec-2-report.md` · 검수 `review-doc-2-report.md`(D1 ~ D5) · 코드 검수 `review-code-1-report.md`(W1 ~ W9) · 구현 `be-1-report.md` · `fe-1-report.md`
4. 코드(읽기만 · 1루프 구현이 들어 있음): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback`(미커밋 diff 포함)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec`(앞 판 미커밋 위에 이어서). 커밋 · push · PR · 승인 · Delivery 수정 금지.

## 이번에 스펙에 넣을 것 (사용자 2026-11-17 E2E)

| # | 결정 | 스펙 |
|---|---|---|
| **F-5 (= E4)** | 시술 줄 ⋮ 더보기 = **준비중 줄은 ⋮ 없음 · 그 뒤 단계마다 ⋮ → 한 단계 되돌림**: 호출 줄 → **「호출 취소」**(준비중으로 + **호출 취소 알림**) · 진행중 → 시작 취소(이미 있음) · 완료 → 완료 취소(이미 있음) | SPEC-002 U-3 · 줄 상태 · API(새 엔드포인트 — 호출 취소) · 매트릭스 · 규칙 · SPEC-005(새 알림 종류 · 받는 계정 · 웹 OS 알림 · 앱 푸시는 아래 「정할 것」) |
| E3 | 바로 시작으로 시스템 계정이 집도의인 줄의 원장 칸 = **「간호관리」**(「간호관리 · 진행 mm:ss」 · 완료 「간호관리 · n분」) · 원장 이름을 눌러 원장 바꾸기는 원장 줄과 **똑같이** 열림 | SPEC-002 OQ-62 닫기 · U-3/줄 글자 · 원장 변경 |
| E5 | 웹 OS 알림은 **늘 띄운다** — DAY 탭이 열려 있으면 앞 · 뒤 · 다른 모니터 상관없이. 기본값 OQ-N9 「`document.hidden` 일 때만」을 사용자 결정으로 뒤집음 | SPEC-005 OQ-N9 · U-5 · S-6 |
| E6 | 차트 창을 여는 곳 = **시술 이름 글자만** · 이름에 마우스를 올리면 **「차트 작성」** 표시. 줄 전체가 열던 규칙(규칙 23 · U-12 · U-13 · U-14 · E30 문장) 바꿈 | SPEC-002 |
| E2 | 의사 호출 팝오버 — 기본 선택 원장이 목록 아래쪽이면 팝오버 위쪽(제목 · 검색 · 추천 · 선택됨)이 잘리고 아래가 빔. 정상 = 늘 위부터 다 보임 | 스펙 변경 없음이면 「없음」 — 버그. 스펙에 팝오버 열림 규칙이 있으면 확인만 |

**호출 취소의 KOS 쓰기**: 지금 KOS 쓰기 경로(`emr/kos/writes.py` :46-56)에 「호출 취소」 명령이 **없다**. 사용자에게 HAR 을 요청해 둠(아직 없음). → KOS 쓰기 표에는 「KOS 명령 미확인 — HAR 대기」로 열어 두고, **기본값(코디 2026-11-17 · HAR 받으면 바꿈)**: DAY 만 되돌린다가 아니라 — 코드 사실을 보고 ① `change-tasks-doctors`/상태로 되돌릴 수 있는 기존 명령이 있는지 ② 없으면 DAY 만 · 다음 동기화 때 어떻게 되는지를 적고 「정할 것」에 올린다. 지어내지 마라.

## 검수 잔여 — 이번에 같이 닫는다

- review-doc-2 **D1**: spec-002 :586 귀가 대기 취소 웹 응답 = **판 전체 다시 받기**(코드 = 본문 없음 + `HX-Trigger day:board-refresh` · `X-Day-Version` 없음 — fe-1) · :584 「조작 응답도 같은 sort」→ 「판 전체를 다시 그리는 응답만」 · **`sort` 는 GET 쿼리로만**. **D2** 판 렌더가 `hx-get` 에 `sort` 를 박음 · 탭 = 링크 이동. **D3** `log.md:17` PR 칸. **D4** 옛 `room.order` 3곳 → `sort_order`.
- review-code-1 **W5**: 직전 단계가 판 단계가 아니면 `procedure` 로(be 해석 — `_step_before_home`) → OQ-58 ⓐ 에 적어 닫음. **W6**: 연결 없는 병원은 KOS 쓰기 없이 DAY 만 시작 → 규칙 34 한 줄. **W8**: §3 D1 · sort 문장. **W3**: `conflict` 거절 토스트 글자 — 사용자 글자 없음 → 「정할 것」 유지.

## 정할 것으로 올릴 것(지어내지 말고)

- 호출 취소 알림: 알림 종류 이름 · 제목/본문 글자(기존 원장 호출 알림 글자 규칙에서 따라 나오는 게 없으면 비움) · 받는 계정(원래 호출을 받은 계정과 같게가 자연스러움 — 기본값으로 적되 꼬리표) · **앱 푸시까지 보낼지**(앱 코드는 범위 밖 — 앱이 모르는 알림 종류를 받으면 어떻게 되는지 코드 사실로).
- 호출 취소 거절 코드 · 이미 수락된 호출은 취소 가능한지(기본값 = 수락 전 「호출」 줄만 · 수락된 줄은 ⋮ 에 없음 — 꼬리표).

## 검증 · 보고

- `python3 scripts/lint-pipeline.py --strict` → products/day/ ERROR 0.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/spec-3-report.md` — 고친 곳 파일:줄 · 결정 반영 위치 표 · 새 계약(호출 취소 엔드포인트 · 알림) · 정할 것.
- 완료 보고는 dispatch preamble 의 `worker_done`.
