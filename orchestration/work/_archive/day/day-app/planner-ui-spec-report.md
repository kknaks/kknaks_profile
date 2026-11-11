# planner-ui-spec 결과 보고 — DAY 직원 앱 UI 교정 (스펙만)

## 상태: done (커밋 · push · PR 없음 — 워크트리 변경만)

- 작업 트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec` · branch `kknaksss/day-app-spec` · 시작 HEAD `78f3ee59c8a10e0abb1bde8896302873a46d0732`(변경 없음 · 미커밋)
- 원천: `_RESUME.md` §2(2026-11-10 UI 교정 7개 절) · `research-prototype-toasts.md` · `research-prototype-board.md` · 브리프 §3(최신 「토스트 안 되돌리기 없음」 「응」) · DAY dev 코드 read-only 대조(`backend/day/services/board_rules.py` 스냅샷 칸 · `schemas/auth.py` `MeOut` · `styles/app.css` 토큰) · 프로토 `lib/interpret/langs.dart` `_natLang`

## 변경 파일 (allowed_paths 안 2개)

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | +229 / −89. frontmatter `last_updated` 2026-11-10 · `sources` 에 `research-prototype-toasts.md` 추가 · `status: stable` · `version: 0.0.1` 유지 · 머리에 「2026-11-10 개정」(대체한 기존 계약 ①~⑧) + 「기준선 주의」(코드 미반영 · 리뷰 기준선이 78f3ee59 판과 다름 · 승인/머지 전) |
| `products/day/20-spec.md` | `최종 수정` 날짜 · In Scope / Out Of Scope 의 DAY-SPEC-003 두 줄만 정합 |

새 SPEC ID · 새 문서 · 30-work.md · Delivery #235 · SPEC-000/001/002 · 배포 문서 · 코드 수정 없음.

## 확정 사항 반영표 (브리프 §3)

| # | 확정 | SPEC 반영 자리 |
|---|---|---|
| 1 | 하단 4메뉴 · 프로토 폰 탭바/아이패드 레일 · 예약현황 「곧 출시 예정」 · 채팅/설정 상세 후속 · 5번째 탭 없음 · 인박스 탭과 혼동 없음 | 개요 · §1 범위(넣음/뺌) · Placement · Wireframe · U-2 · A-25 · OQ-A3 닫음 · OQ-A18(채팅 본문 글자) |
| 2 | 공통 머리 DAY · 탭 제목 · 종 + 실제 미읽음 배지 · 계정은 설정 · 알림 API 없음은 별도 의존 | U-2 · U-16 · §3 API 표 행 추가 · §4 서버 의존 **D-5**(계약 없음 · 발명 안 함) · 규칙 8 · 케이스 매트릭스 · A-26 · A-27 · OQ-A19 |
| 3 | 필터 4개 · `inbox.section` 만 | U-2 그대로 유지(변경 없음 · OQ-A2) |
| 4 | 카드 네 줄 · 수납 필요 서버 조건 · 없는 값 발명 금지 | Wireframe · U-3 · A-28. 3행 「기타 제공 정보」= 지금 카드가 싣는 나머지 바이탈 `gender` 만(해석 — 아래 주의) |
| 5 | 마취 중 한 줄 · 연보라 · `anesthesia.long` 빨강 · 마취 완료 {N}분 / 담당의 | U-3 · U-8 · 규칙 1 · A-29. N = `lastMinutes` · 기준 = `limits.anesMin` · 시각 = `runningSince`(모두 dev 구현 · SPEC-002 에 있는 칸 — 부족분 없음) · OQ-A20(색 토큰) |
| 6 | 호출 뒤 목록 카드(대상 · 수락 대기 · 시술명 · 경과 · 건수 · 수락) · 카드에서 수락 · 상세 강조 상자 | U-3 「호출 뒤 카드」 · U-4 1번 · A-30 · A-31 · S-2 |
| 7 | 원장 「수락 · N건」 즉시 본인 · 간호사 「원장 골라 수락 · N건」 드로어 대리 · 목록/상세/호출 탭 공통 · 서버 권한 유지 | U-6(분기 기준 = `/me` `staff.id` ∈ 스냅샷 `doctors[]`) · U-10 · A-2 개정 · 프로토 차이표 · OQ-A23(관리자 등 비간호 수락권자 글자 — 동선 · 권한은 간호사와 같게, 축소 없음) |
| 8 | 상세 「< 시술현황 {방}」 · 오더 메모 여백 축소(수치 없음) · 카드형 시술 · 진행중 강조 · 완료 회색 아래 · DAY 색 버튼 · 세로 ⋮ · canUndo* 확인 없이 | U-4 · U-7 · 테마 표 · A-31 |
| 9 | 상시 체크박스 없음 · [의사 호출] → 시트 안 시술 + 원장 · 마법사 금지 · pickable/canCall · 재호출 A-22 | U-4 · U-5 · U-7 · A-32 · S-7 · OQ-A22(시트 처음 체크 없음) |
| 10 | 모두 완료 상자 · 마지막 종료 · [귀가 대기] · 머리 글자 · 서버 계약 유지 · 표시 글자 ≠ 업무 상태 | U-4 5번 · U-9 · A-33 |
| 11 | 통역 드로어 원형 · 빠른 말하기 스피커 · 둥근 칩 · 가로 스크롤 · [통역하기] · 기존 문구만 | U-15 · A-36 |
| 12 | TW → `zh-Hant` 확정 · 빠른 말하기/WS 같은 언어 · 앞 고객 언어가 덮지 않음 · 수동 변경 · 다른 국적 근거 · vi/yue 칩 없음 유지 · 「중국어(번체)」 | U-15 · S-8 · A-35 · OQ-A9 닫음(TW) / 남김(HK · VN · 그 밖) · OQ-A26 |
| 13 | 프로토 원문 성공 토스트 · 어두운 상단 · 2.6초 · 덮어쓰기 · 되돌리기 버튼 없음 · DAY 오류 글자 · 격리 · 본인 조작 기준 | U-13(글자 표 10행) · 규칙 7 · 케이스 매트릭스 · 프로토 차이표 · A-34 · OQ-A24 · OQ-A25(재호출 원문 없음 → 토스트 없음) |

## 남은 의존 · OQ

- **서버 의존**: D-1(로그인 환경 연결) · D-2(기기 등록 · APNs) · D-3(통역 WS) · D-4(방 이동 등) 그대로 + **D-5 신규 — 알림 목록 · 미읽음 수 계약 없음**(DAY 에는 `notification` 데이터 표만 · API/경로를 정하지 않음 · 그 전엔 종만 · 배지 없음).
- **정책 OQ**: OQ-A1 · OQ-A9(남은 것 — HK 는 프로토 번체 vs interpret-pwa `yue` 로 원천이 갈림 · VN 프로토 대응 없음 · 비코드 국적 값) · OQ-A11(vi · yue 빠른 말하기 — 유지).
- **문구 OQ**: A5 · A6 · A7 · A8(「전체」 대상 글자 — 카드/상세는 DAY 웹 「전체 의사」로 두고 사용자 원본 「전체 호출」과 차이 기록) · A10 · A16 · **A18**(채팅 본문) · **A25**(재호출 성공 글자).
- **UI 선택 OQ(기본값 진행 · 리뷰 확인)**: A2 · A3(남은 것 — 첫 메뉴 = 시술현황) · A4 · A13 · A14 · **A19 · A20 · A21 · A22 · A23 · A24 · A26**. 특히 **OQ-A21**(시술 중 카드 · 담당의 여럿 · 마취와 호출 겹침)은 사용자가 아직 정하지 않은 카드 상태라 사용자 확인 권장.
- **SPEC 정정 OQ-A12**(SPEC-002 주인 몫) 그대로.

## 기존 계약 보존

- 업무 규칙 · 권한 · API 경로 · 서버 값 · 오류 코드 · SSE · 세션 보관 · 연결 대상 검증 · 푸시 · 통역 WS 계약 · 인수 조건 A-1 · A-3 ~ A-24 · 재호출 노출 A-22 · 필터 4개 · 1차 기능 범위 축소 없음.
- 대체한 기존 계약은 SPEC 머리 「2026-11-10 개정」 ①~⑧ 과 각 U 본문 「2026-11-09 판 … 을 대신함」으로 출처 날짜와 함께 기록. 닫은 것은 §5 「닫은 것 — 사용자 2026-11-10」 표.

## 검증

- `git diff --check` → 통과(출력 없음)
- `python3 scripts/lint-pipeline.py --strict` → exit 0 · **0 error, 263 warning** · `products/day/` 경고 · 오류 **0건**(경고는 전부 다른 제품의 doc_no 등 기존 것)
- `git status --short` → `M products/day/20-spec.md` · `M products/day/20-spec/spec-003-mobile-app.md` 두 개만

## 미결 · 주의점 (reviewer_doc · 코디 확인)

1. **카드 3행 「기타 제공 정보」 = `gender`** 로 해석했다(dev 스냅샷 `customer` 칸 = name · phoneticName · gender · birthDate · nationality · isNew 중 2026-11-09 판 카드가 이미 싣던 나머지 값). `isNew` 는 새 칸이라 넣지 않음. 다르면 사용자 확인.
2. **원장 판정 = `doctors[]` 에 로그인 `staff.id` 가 있는가**(서버 원장 목록 · 기존 SPEC 이 쓰던 기준). `/me.job_role` 이름 글자로 판정하지 않음.
3. 원장이 **다른 원장 지정 호출**을 눌러도 본인 수락으로 보낸다(사용자 「원장을 다시 고르게 하지 않는다」) — 받아들일지는 서버 판정. 서버 규칙이 거절하면 실패 토스트만.
4. `zh-Hant` 한국어 이름만 「중국어(번체)」로 바꾸고 자기 표기 「臺灣 · 繁體中文」은 interpret-pwa §5.5 원문 유지. 자기 표기도 바꿔야 하면 사용자 확인.
5. 국적 대응 중 `US` · `PH` · `IN` → `en` 과 「그 밖 = en」은 프로토 `_natLang` 근거로 반영(사용자 「기존 매핑은 원본 · 지원 언어와 대조해 반영」) — 리뷰에서 범위 확인.
6. **타 문서 후속(이번에 손대지 않음)**: `log.md` 에 `spec-change` 행(DAY-SPEC-003 · 2026-11-10 UI 교정) · Delivery #235 / 코드 PR #237 재기준(코드 미반영) · CENTURION_DAY 앱 코드 교정 · D-5 알림 계약은 그 기능 SPEC(DAY-SPEC-000 `notification` 기반) · SPEC-002 OQ-19 기본 선택 문장과 앱 직무 분기 차이(앱 쪽 적응 — SPEC-002 주인 참고).
