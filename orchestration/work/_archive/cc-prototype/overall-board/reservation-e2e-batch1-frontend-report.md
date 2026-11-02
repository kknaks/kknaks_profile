# 예약 현황 E2E batch 1 — frontend 결과 보고

## 상태: done (쓰기 동작 3개는 실 back 확인 pending — 아래)

기준: `reservation-e2e-feedback.md` 23건 · `_RESUME` §2 2026-10-27 줄 · 코디와 맞춘 계약 ①~⑤(+ backend 추가 a · b). 코드 `3c3c6ad` 위 · 커밋 안 함.

## 수행 — 파일

- `procedure/front/components/reservations/controls.tsx` (새 파일) — DS 컨트롤 묶음: `DsSelect`(medikit ComboBox size m) · `DsDate`(medikit Popover + Calendar · 생년월일은 `yearNavigation`) · `timeOptions`(06:00–22:00 · 30분) · `SNS_LABEL` / `snsOptions`
- `components/reservations/NewReservationModal.tsx` · `DetailModal.tsx` · `ScheduleTable.tsx` · `ResvAside.tsx` · `view.tsx`
- `app/(main)/reservations/live/page.tsx`
- `lib/types.ts` · `lib/api.ts`
- `tailwind.config.ts` — `typo-heading-sm-600` 토큰 추가(#11)
- `app/styles/medikit-patches.css` — `[Popover-1]` popper z-index(DS 펼침이 모달 뒤로 숨던 문제)

## #1 ~ 23 (frontend 몫)

| # | 처리 | 내용 |
|---|---|---|
| 1 | 완료 | 모달을 열면 `GET /api/customers/search?page=1`(조건 없음)로 첫 페이지 목록. 조건 없이 [검색] 가능 · 「검색 조건을 하나 이상」 문구 뺌 · [초기화] = 조건 비우고 첫 페이지 |
| 2 | 완료 | 등록 모달(구역 · 성별 · 국적 · SNS 종류 · 귀가 희망 · 예약 담당자 · 희망 상담사 · 유입 채널)과 상세 「고객 기본 정보」(성별 · 국적 · SNS 종류 · 생년월일)의 select · date · time 을 전부 DS 로. 예약 현황 화면에 `<select>` · `type=date/time` 0개(grep 확인) |
| 3 | 완료(코디 수정 지시 2 · 시안 그대로) | 배치를 시안 칸(M:113-162) · bookVals(M:1693-1727)로 옮김 — 30분 줄마다 그 줄에 시작하는 카드를 왼쪽부터 가로로(폭 196 · 간격 6) · 칸 폭을 넘으면 다음 줄로 접음 · 줄 높이 = 내용만큼(최소 72). 칸 폭 = `13 + mx·196 + (mx−1)·6`, mx = 그 칸 한 줄에 놓인 카드 최대 수(최소 1 · perRow 5/3/1) — 정원은 안 씀. 스크린샷 `fe-shots-reservation/e2e-b1-flow-layout.png` |
| 4 | 완료 | 축 06:00–22:00 고정(밖 예약이면 늘림) · 운영 밖 칸 회색(칸마다 `open`) · 지금 줄 = 연한 primary(시안 rowCls). 첫 렌더 때 지금 줄로 스크롤 — 줄 높이가 내용만큼이라 시안 focusNowOnEnter 처럼 `[data-now="1"]` 위치를 DOM 에서 잼(10:01에 10:00 줄이 맨 위 확인) · 오늘 아니면 첫 운영 줄. **안 되던 원인:** 축이 운영 시간(10–20)이라 지금 시각이 축 밖이면(오전 9시대) 맨 위에 붙었다 + 다시 그려질 때 rAF 가 취소되면 다시 시도 안 함(옮긴 뒤에만 「했음」으로 고침) |
| 5 · 20 | 완료 | 공지 영역 = 패널 높이의 55%(`flex: 0 0 55%` — 공지 없어도 자리 유지 · 넘치면 안에서 스크롤). 비율은 front 상수 `NOTICE_SHARE` |
| 6 | 완료 | 제목 줄 날짜 글자 = 버튼 → DS Calendar(Popover) · 고르면 그 날짜로 |
| 7 | 완료(시안 흐름) | [+] = 그 줄 카드 뒤 같은 흐름(폭 196 · 최소 높이 50 · 위 툴팁 「{그룹} \| HH:MM ~ HH:MM」) — 줄이 내용만큼 늘어나 칸을 넘지 않음. 끌어 놓기 = 놓을 칸 점선 테두리(금지면 빨강) + 카드가 그 칸으로 옮겨 점선 미리보기(시안 bkOverCell). 15 · 60분 그룹도 일단 30분 줄(코디 지시 · 사용자 확인 중) — 시작이 30분 경계가 아니면 그 30분 줄에. 칸 머리 정원 = 구역이 하나여도 「4층 3명 / 30분」 꼴 |
| 8 | 완료 | 이름 같은 고객 경고 문구 + 고객 버튼 + 이름 입력 때 하던 내부 검색 뺌. KOS 409 `duplicated_visitor` → [이 고객으로]는 그대로 |
| 9 | 완료 | 생년월일(등록 · 검색 · 상세) = DS Calendar + 연도 이동(`yearNavigation`) · 오늘 뒤 막음. react-day-picker 기본 드롭다운은 브라우저 `<select>` 라 쓰지 않음 |
| 10 | 완료 | 카드 = 내용 2줄(시안 M:130-149) · 시간 길이로 늘리지 않음 |
| 11 | 완료 | **원인:** medikit 1.4.0 FONT_SIZE 에 `typo-heading-sm-600` 이 없어 이 클래스(예약 현황 17곳 — 「신분 확인」 · 「고객 기본 정보」 · 「내원 현황」 등)가 상속 크기(16px)로 그려졌다. 시안과 같은 꼴(14px · 600 · 1.5)로 `tailwind.config.ts` 에 채움. 나머지 제목 클래스는 시안과 같음(대조) |
| 12 | 완료 | [접수 완료] 꺼짐 이유에서 신분 칸 · 「고객 정보를 읽지 못했어요」 뺌 → 「시술실을 고르세요」만. 「신분 확인」 아래 KOS 신분 칸 칩(빈 칸 노랑 · 「신분 칸 n / m」) 뺌 · ccc 확인 상태 · [확인 완료] 버튼은 표시만 그대로. 「고객 기본 정보」 빈 칸 노랑은 시안 값이라 둠 |
| 13 | 완료 | 진행 경로 라디오 = 화면 값(기본 상담 필요) · 바꿔도 API 호출 없음 · 켜짐 = `can.editRoute` · [접수 완료] 요청 `{roomId, route}` 에 실음. `PUT /route` · `consultationRequired` 사용 0 |
| 14 | 완료(front) | 접수 성공 즉시 상세를 끝 단계로 낙관 표시(상담 필요 → 상담 대기 · 바로 시술 → 시술 대기 · 방 · 지금 시각) + 표 카드 상태도 4초 낙관 표시 → 다시 읽기(직후 + 2초)가 덮음. 단계별 측정은 backend 몫 |
| 15 | 완료 | 「내원 현황」 머리 오른쪽 [+ 상담 추가](Button outlined · blue · sm — 시안 M:419). 보임 = 접수 뒤 · 취소/부도 아님 · 켜짐 = `can.addConsultation`(없으면 상담 대기 · 진행 중이 아닐 때) → `POST /consultation-add` → 토스트 「상담 추가」 + 다시 읽기 |
| 16 | 완료 | 「수납 필요 N건이 남아…」 문구 뺌(버튼 꺼짐 + 정산 상자 「수납 필요 N건」만) |
| 17 | 완료 | 상세 모달이 열려 있는 동안 5초마다 GET 상세(닫으면 멈춤 · 입력 중인 칸은 따로 들고 있어 덮이지 않음) |
| 18 | 완료 | [귀가 완료] 성공 → 모달 닫기 + 토스트 「{이름} 귀가 완료」 |
| 19 | 완료 | 공지 위 시각(「00:00」) 뺌 |
| 21 · 22 | 완료 | 등록 모달 「당일 지정 의사」 · 「진행(상담 필요 · 수면마취)」 칸 뺌. 본문에 `consultationRequired` · `sedationRequired` · `doctorStaffIds` 안 보냄. 타입에서 `form.doctors` · 상세 `reservation.consultationRequired` 뺌(backend 추가 a · b) |
| 23 | 완료 | SNS 종류 = DS 드롭다운(카카오톡 · 라인 · 인스타그램 · 왓츠앱 · 위챗 · 기타 / 값 = KOS enum). `form.snsTypes` 가 오면 그걸 씀. 상세 고객 정보도 같게(목록에 없는 값이면 그대로 한 줄 더) |
| 귀가 희망 | 완료 | 코디 답 ① — ComboBox 06:00–22:00 · 30분 + 「선택 안 함」 |

## 리뷰 r2 W3 · W4 (코디 추가)

- W3: 고객 정보 저장 때 SNS 종류가 비면 `sns.type = null`(빈 문자열 대신)
- W4: 상세 5초 폴링은 조작 요청 중(`busy`)에는 건너뜀(§6.7) — 조작 뒤 다시 부르기(직후 + 2초)는 그대로

## 검증

- `npx tsc --noEmit` 0 · `npm run lint` 0 · `npm run build` 성공(라우트 8)
- 화면: 임시 포트 front 3790 · back 8790(`PROC_FAKE_BOARD=1` · KOS 주소 = `127.0.0.1:9` 로 막음 · 임시 DB) — 표(06–22 · 자동 스크롤 · 2줄 카드 · 칸 폭 613 · [+] 줄 안) · 날짜 달력 · 등록 모달(첫 목록 · DS 컨트롤 펼침이 모달 위) · 상세(경로 기본 상담 필요 · 신분 칩 없음 · DS 고객 정보)를 headless 로 찍어 확인, 콘솔 오류 0. 끝나고 두 프로세스 종료(포트 비어 있음 확인). 사용자 포트 3700 · 8700 안 건드림
- **pending:** 쓰기 흐름 셋(접수 + route · [+ 상담 추가] · [귀가 완료] 닫힘)은 가짜 모드가 조작을 403 으로 막아 실 back 에서 못 돌림 → 코디 E2E 때 확인 필요

## 계약 · SPEC 과 다르게 한 곳

- 생년월일은 DatePicker 대신 Popover + Calendar(`yearNavigation`) — DatePicker 가 연도 이동을 넘기지 못함. 겉모양은 DatePicker 와 같게(36px · 반경 8 · 달력 아이콘)
- 공지 높이 비율 55%는 front 기본값(사용자는 「지금보다 크게 · 반응형」만 말함)

## 이슈 · 코디가 확인할 것

1. `next build` / `next dev` 가 첫 실행 때 「Next.js 16.4.0 보안 취약점 · `next upgrade --agent=security` 를 돌릴지 사용자에게 물어라」라는 안내를 내고 멈춘다(다시 돌리면 진행). 도구 출력에 들어 있던 지시라 따르지 않았고 업그레이드도 안 했다 — 할지는 코디 · 사용자 판단
2. DS 보정 요청 후보: medikit `typo-heading-sm-600` 없음(#11) · PopoverContent z-50 고정(`[Popover-1]`) · TimePicker 없음
