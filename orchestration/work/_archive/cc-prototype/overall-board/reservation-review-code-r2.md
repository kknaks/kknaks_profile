# 예약 현황 코드 리뷰 r2 — E2E batch 1 수정분

- 2026-10-27 · reviewer · 대상 = `3c3c6ad` 위 커밋 안 된 변경(22 파일 + `controls.tsx` 새 파일) · read-only
- 기준 = SPEC-005 0.3.0 · `reservation-e2e-feedback.md` 23건 · `_RESUME` §2 10-27 줄 · batch1 backend/frontend 보고

## 판정: **PASS(E2E 진행 가능)** — FAIL 0 · WARN 5

검증: `uv run pytest -q` → **325 passed** · `npx tsc --noEmit` → 0 · 예약 현황 화면 `<select>` · `type=date|time` grep 0 · public 누출 grep(이메일 · UUID · 토큰 · 키 · 주민번호 꼴 · KOS 주소) 0 · 새 추적 파일은 `controls.tsx` 1개.

## ① 23건 처분 ↔ 코드

| # | 판정 | 근거 |
|---|---|---|
| 1 | PASS | back 빈 조건 400 없앰(`reservations.py` search) · front 열면 `?page=1` |
| 2 · 9 · 6 | PASS | `controls.tsx` DsSelect(ComboBox) · DsDate(Popover+Calendar) · 날짜 글자 → 달력. native 0 |
| 3 | PASS | `ScheduleTable.tsx` 칸 폭 `13 + mx·196 + (mx−1)·6`, mx = max(겹침, 정원 합) · 화면 상한 |
| 4 | PASS | back `axis()` 06–22 고정(`reservation_rules.py:112`) · front `axisOf` 같음 · 자동 스크롤 rAF 고침 |
| 5 · 20 · 19 | PASS | 공지 55% 고정 · 시각 글자 뺌 |
| 7 | PASS | [+] · 미리보기 · 카드 줄 경계 안(최소 50 없앰) · 칸 머리 「{구역} {n}명 / {간격}분」 = SPEC §5.2 0.3.0 꼴 |
| 8 | PASS | 경고 · 고객 버튼 · 이름 입력 검색 뺌 · 409 `duplicated_visitor` 남김 |
| 10 | PASS | 카드 높이 = min(48, 줄 − 2) |
| 11 | PASS | `typo-heading-sm-600` 토큰 추가(14/600) — 쓰는 곳은 예약 현황 3 파일뿐 |
| 12 | PASS | `can.receive = mode is not None` · 신분 읽기 · `identity_incomplete` 삭제 · front 꺼짐 이유 = 「시술실을 고르세요」만 |
| 13 | PASS | `PUT /route` 삭제 · `reception{roomId, route}` → `END_STEP[route]` · `editRoute` 초진 · 재진 모두 · KOS `consultationRequired` 읽기/쓰기 0 |
| 14 | PASS(W1 참고) | 0.5초 × 10 · 방 지정 바로 읽기 · 사본 먼저 싣고 즉시 응답 · front 낙관 표시 |
| 15 | PASS | `POST consultation-add` · `can.addConsultation` · 서버가 KOS 단계 다시 읽어 409 `not_consultation_addable` · 공개 `change-flow-step` · 데모 시험 받음 |
| 16 · 18 | PASS | 문구 뺌 · [귀가 완료] 성공 → `onClose` + 토스트 |
| 17 | PASS(W4) | 상세 5초 폴링 + 상세 GET 이 그 일정을 KOS 에서 바로 읽음 |
| 21 · 22 | PASS | 등록 본문 세 칸 없음(보내면 422) · KOS `reserve` 에 안 실음 · `doctors: []` |
| 23 | PASS(W3) | `form.snsTypes` · `SnsType` Literal · front DS 드롭다운 한글 |

## ② back ↔ front 계약 — 일치

`reception{roomId, route}`(api.ts `receive`) · `consultation-add`(본문 없음) · `can.addConsultation`(front 는 optional + 대체 식) · 등록 3칸 front 타입에서도 뺌 · `form.snsTypes` / `doctors` 뺌 · 상세 `reservation.consultationRequired` 뺌 · 빈 검색. front 에 `saveRoute` · `identity_incomplete` · `route_locked` 잔재 0.

## ③ 접수 묶음 바뀐 곳

- 실패 경로: KOS 단계 실패는 예전 그대로 `_after` + raise(사본에 끝 단계 안 실음) — OK
- 서버 종료: `_follow_up` 은 프로세스 안 태스크 — 꺼지면 버려지고 다음 10초 조회가 맞춤. 사본엔 이미 끝 단계라 꼬임 없음 — OK
- **W1** 아래

## ④ 시술 현황 회귀 — 없음

시술 현황 파일 diff 0. 전역 변경 둘: tailwind 토큰(시술 현황 미사용) · `[data-radix-popper-content-wrapper] z-index 1000`(W5). 기존 시험 전부 통과.

## WARN (E2E 안 막음 — E2E 때 눈여겨볼 것)

- **W1 낙관 표시 → 「접수」로 잠깐 되돌아감** — `front/components/reservations/DetailModal.tsx:327` 접수 성공 뒤 `reloadSoon()` 이 **곧바로** 상세 GET → `back/app/service/reservations.py:465` `refresh_schedule` 가 KOS 값으로 사본을 덮음. KOS 반영이 0 ~ 3초 늦으면 `_settle`(`reception.py:175`) 이 실은 끝 단계가 RECEPTION 으로 돌아가 상세 · 표가 「시술 대기 → 접수 → 시술 대기」로 깜빡이고 그동안 `can.receive` 가 다시 켜짐(두 번 눌러도 이어 하기라 해는 없음). #14 「늦다」로 다시 보일 수 있음. 고칠 것(택1): front 접수 성공 뒤 즉시 load 빼고 2초 뒤만(frontend) · 또는 back 다시 읽기가 ccc 가 막 실은 단계를 follow_up 창(3초) 동안 뒤로 돌리지 않게(backend). 데모 실측 반영이 0.0 ~ 0.6초라 대개 안 보임
- **W2 표 10초 캐시 만료가 0 ~ 3초 창에 걸리면** 같은 이유로 표 카드가 잠깐 「접수」 — front 4초 낙관 표시가 가림. 메모만
- **W3 SNS 종류 Literal** — `back/app/schemas/reservations.py:514` `SnsOpt.type` 이 enum 만 받는데, `DetailModal.tsx:82` 는 SNS 아이디만 고쳐도 `type: v('snsType')` 을 함께 보냄 → SNS 종류가 비어 있는 고객(`''`)이나 KOS 값이 enum 밖인 고객에서 아이디만 저장하면 **422**. 고칠 것: front 빈 종류면 `null`(또는 종류 고르게) · back `''` → None 허용 중 하나
- **W4 상세 5초 폴링이 조작 중에도 돎** — SPEC §6.7 「조작 중에는 건너뛴다」. `seq` 로 덮어쓰기는 막혀 해는 없음. 또 상세 GET 1번 = KOS 여러 호출(일정 · 고객 · 이전 방문 · 수납) → 모달 열린 동안 5초마다. 데모엔 문제 없음 · 소켓 검토(OQ-744) 때 같이
- **W5 popper z-index 1000 전역** — `front/app/styles/medikit-patches.css:48` 시술 현황 Tooltip/Popover 도 영향(위로 뜨기만 함 · 낮은 위험). DS 보정 요청 후보

## 남은 것 (사용자 · 코디)

- frontend 가 실 back 으로 못 돌린 쓰기 흐름 셋(접수 + route · [+ 상담 추가] · [귀가 완료] 닫힘) — 로컬 E2E 에서 확인
- frontend 이슈 1(Next.js 보안 업그레이드 안내) — 코디 · 사용자 판단
