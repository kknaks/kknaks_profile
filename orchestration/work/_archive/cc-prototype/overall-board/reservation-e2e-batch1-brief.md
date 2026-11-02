# [backend · frontend] E2E batch 1 수정 — 사용자 지적 23건

너는 **cc-prototype `backend` 또는 `frontend` 워커**다(dispatch 에 적힌 역할). **앞 판 맥락이 없다.** 먼저 역할 문서(`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/<역할>/role.md` + 같은 폴더 rules · skills · tools · workflow)와 앞 판 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-<역할>-brief.md`(SSOT · allowed_paths · 금지 · 검증 · 완료 보고)를 읽어라.

작업 워크트리(코드): `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — 최신 커밋 `3c3c6ad`(예약 현황 구현). backend · frontend 가 같은 워크트리(back / front 나눠서).

## 1. 기준 (이 순서로 우선)

1. **`/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-e2e-feedback.md` — 사용자 지적 23건 · 「처분」 칸이 곧 할 일**(사용자 원문 · 지금 동작 · 고칠 것)
2. `_RESUME.md` §2 의 **2026-10-27 줄**(시간축 06–22 · 이름 경고 뺌 · 신분 조건 뺌 · 상담 추가 넣음 · 등록 모달 칸 뺌 · 수납 반영 폴링 · 진행 경로 ≠ KOS 체크) — SPEC-005 0.2.0 과 다르면 **이쪽이 맞다**(planner 가 SPEC 0.3.0 을 병렬로 쓰는 중)
3. SPEC-005 0.2.0 · 시안 `reference/2026-10-23-cc-overall-board/design/Ceramique 전체현황판.dc.html` 「예약 현황」 `M:93-715`

## 2. 몫

| # | backend | frontend |
|---|---|---|
| 1 고객 검색 목록 | 조건 없이도 목록(내부 `get-visitors` 빈 조건 · 페이지) — 빈 조건 400 없앰 | 모달 열면 첫 페이지 목록 · 조건 없이 [검색] 허용 |
| 2 · 9 · 6 DS 컨트롤 · 달력 | — | 예약 현황 화면 전체의 select · date · time 을 **DS(medikit · Ceramique) 컴포넌트**로. `procedure/front` 에 이미 있는 DS 컴포넌트를 먼저 찾고(Select · DatePicker · Calendar · TimePicker), **없으면 질문**(만들지 말고) · 제목 줄 날짜 글자 클릭 → 달력 |
| 3 칸 안 카드 나란히 | 필요하면 카드에 겹침 줄 번호(지금 `resourceIndex`) 확인 | 그룹 칸 폭 = 시안 식 `13 + mx·196 + (mx−1)·6` · 한 시각 겹치는 카드 수만큼 나란히(정원 3 → 3장) |
| 4 시간축 06–22 · 지금 시각 스크롤 | 축 = 06:00–22:00 고정 · 운영 시간은 칸마다(회색) | 06–22 그리기 · 첫 렌더 지금 시각 줄로 자동 스크롤(안 되는 원인 찾기) |
| 5 · 20 공지 높이 · 19 「00:00」 | — | 공지 영역 = 패널 안 화면 높이 비례(지금보다 크게) · 넘치면 안에서 스크롤 · 공지 시각 글자 뺌 |
| 7 15분 칸 [+] 넘침 · 칸 머리 표기 | (머리 표기용 값이 모자라면) | [+] 상자 · 드래그 미리보기 · 카드가 줄 경계에 딱 맞게(최소 높이로 줄을 넘지 않음) · 칸 머리 정원 표기 한 꼴로 |
| 8 이름 같은 고객 경고 | 검색 응답의 경고용 값이 있으면 그대로(안 씀) | 경고 문구 + 고객 버튼 뺌(KOS `duplicated_visitor` → [이 고객으로]는 남김) |
| 10 카드 2줄 | — | 카드 = 내용 2줄 높이 콤팩트(예약 길이로 늘리지 않음) · 시안 `M:130-149` |
| 11 타이포 | — | 상세 모달 제목류 시안 타이포 대조 |
| 12 접수 신분 조건 | `can.receive` · 접수 묶음에서 신분 조건 뺌(`identity_incomplete` 안 씀) | 꺼짐 이유 · 빈 칸 표시 뺌 |
| 13 진행 경로 | `route` 쓰기(KOS `update-reservation{consultationRequired}`) 없앰 · 접수 요청에 `route`(consultation · direct) 받음 → 끝 단계 · `can.editRoute` = 접수 전이면 초진 · 재진 모두 | 라디오 = 접수 때 고르는 값 · 기본 상담 필요 · 바꿔도 API 호출 없음 · [접수 완료] 요청에 실음 |
| 14 접수 → 시술 대기 느림 | **단계별 소요 시간 측정**(데모 · 가짜 시계 시험) → 다시 읽기 횟수 · 간격 줄일 곳 · 성공 뒤 즉시 응답 · 보고에 수치 | 접수 성공 뒤 즉시 낙관 표시 + 다시 읽기 |
| 15 [+ 상담 추가] | 아래 §3 | 「내원 현황」 머리에 [+ 상담 추가](시안 `M:415-521`) |
| 16 · 18 귀가 | — | 「수납 필요 N건이 남아…」 문구 뺌 · [귀가 완료] 성공 → 모달 닫기 + 토스트 |
| 17 수납 반영 | (상세 GET 이 캐시 없이 KOS 를 읽는지 확인) | 상세 모달 열려 있는 동안 5초 폴링 |
| 21 · 22 등록 칸 | 등록 본문에서 당일 지정 의사 · 상담 필요 · 수면마취 안 보냄(form 응답에서도 뺌) | 칸 뺌 |
| 23 SNS 종류 | form 에 KOS `snsType` enum(etc · kakaotalk · line · instagram · whatsapp · wechat) | DS 드롭다운(한글 표시) · 등록 · 상세 둘 다 |

## 3. [+ 상담 추가] KOS 동작 (backend)

KOS 동작이 확인되지 않았다. **데모 쓰기 허가 범위에서 1회 시험**(데모 테넌트 assert · 운영 키 금지 · 일회성 스크립트): 상담 진행/완료 뒤 고객에게 **공개 `changeFlowStep(CONSULTATION_WAITING)`**(뒤로 가는 변경 — 리포트상 받음)을 보내 받는지 · 다른 값이 바뀌는지. 받으면 [+ 상담 추가] = 그 호출(+ ccc 이벤트 로그) · 상담 기록은 만들지 않는다(KOS [상담 시작]이 만든다 — `_RESUME` 10-26). 안 받으면 멈추고 질문. 결과를 보고에 적는다.

## 4. 검증 · 금지 · 보고

- 앞 판 브리프 §4 · §5 · §6 그대로(사용자 포트 3700 · 8700 · 프로세스 금지 · 커밋 금지 · KOS 쓰기는 §3 시험만 · public 누출 금지)
- 끝 보고에 **# 1 ~ 23 처리 여부 줄마다**(네 몫만) · 측정 수치(#14) · §3 시험 결과
- 보고 대상 = 예약 코디 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3`(preamble 과 다르면 preamble)
