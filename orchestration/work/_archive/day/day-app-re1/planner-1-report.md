# planner-1 결과 보고 — 앱 차트를 웹과 같은 기능으로 (DAY-SPEC-003 ㉑ · DAY-SPEC-002 ㉚)

## 상태: done

- 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` (base origin/main `b152d463`) · 커밋 · push 안 함
- 코드 기준 CENTURION_DAY `55e60aa4`(read-only `git show`)

## 수행 내용 — 바꾼 파일 · 절

| 파일 | 바꾼 곳 |
|---|---|
| `products/day/20-spec/spec-003-mobile-app.md` | frontmatter(last_updated · sources 3줄) · **개정 ㉑ 머리글 ① ~ ⑪** · §1 넣음 표(차트 행) · 뺌 표(「차트 작성」 · 「차트 API」 취소선 + [고객 차트] · 누른 시술 강조 · 지난 방문 행 + 여권 스캐너 · 문진 QR · 예약 탭 = 다음 작업 행) · Placement(Android 하단 「폰 차트 시트」 → 전체 화면 · 새 「차트 창」 줄) · Wireframe(차트 예시) · UX Contract 머리 · U-4 차트 줄(취소선 → U-23) · **새 U-23**(여는 곳 · 띄우는 자리 · 모양 · 머리 · 탭 · [저장] · 「최근 저장」 · 담당자 · 충돌 · 거절 토스트 · 닫기 표 · 사진 탭 · 값 원천 · 권한 · 까만 줄 · 탭바 겹침) · U-13 토스트 줄 · §3 API 표 차트 행 · 소비 기준 줄 취소선 · 새 「차트 · 사진 — 앱이 쓰는 칸」 · 케이스 매트릭스 10행 · §4 Frontend 화면 · 권한(D10) · Functional Rule 9 · **새 「개정 ㉑ — 결정 ↔ 바꾼 곳」 · 「웹 차트 기능 28행 처분」 · migration 판단** · 서버 의존 D-4(취소선) · 새 D-7 · A-17 · A-38(취소선) · 새 A-51 ~ A-60 · OQ-A30(차트 몫 닫음) · OQ-A34(닫음) · 새 「차트 — 정할 것」 OQ-A63 ~ A78 |
| `products/day/20-spec/spec-002-procedure-board.md` | frontmatter · **개정 ㉚ 머리글 ① ~ ⑤** · 1차 범위 「직원 앱 차트 쓰기 · 사진 탭 — 다음 스펙」 취소선 · U-16 마지막 줄 취소선 + 새 줄 · API 표 앱 칸 6행(차트 탭 저장 · 사진 목록 · 올리기 · 삭제 · 파일 · 다시 시도 — 「없음 — 웹만」 취소선 → `/api` 이름 제안) · 「JSON 짝 없음」 문장 → 있음 · **새 「차트 · 사진 JSON 짝」**(웹 ↔ 앱 대응 표 · 요청 · 응답 · 인증 · 오류 코드 · 앞단 100MiB) · 개정 ㉘ 결정 표 C15 행 · 새 §4 「개정 ㉚ — 앞 판과 달라진 곳」 · DB(migration 없음) · OQ-99 · OQ-100. 웹 동작 · 권한 · 규칙 23 · 31 · 39 본문 무수정 |
| `products/day/20-spec.md` | 최종 수정 · In Scope 직원 앱 줄 · 시술 현황 줄 · Out Of Scope(「직원 앱 차트 쓰기 · 시술전후사진」 취소선 · 여권 스캐너 · 문진 QR · 예약 탭 다음 작업 · [고객 차트] 안 넣음) |
| `products/day/10-decision.md` | last_updated · 현재 결론 한 줄(escalation 없음 · ESC-001 범위 안 넓힘 · D10 문구는 출시 준비) |
| `products/day/log.md` | 최종 수정 · 2026-11-25 spec-change 행 |
| `products/day/20-spec/spec-000-data-model.md` | **확인만 · 무수정** — `visit_photo` · `external_ref` · 차트 이력 칸 그대로(앱용 칸 없음) |

WORK(30-work) 안 씀 · `00-baseline/` 무수정.

## 결정 → 절 짝

SPEC-003 §4 「개정 ㉑ — 결정 ↔ 바꾼 곳」 표에 있음. 요약: 범위 → §1 · D1 → U-23 사진 · D2 → [저장] · D3 → Placement · 모양 · D4 → 띄우는 자리 · D5 → 담당자 · D6 → 닫기 표 · D7 → §3 · SPEC-002 ㉚ · D8 → 사진 대상 · D9 → 까만 줄 · 탭바 · D10 → 권한 문구 · D11 → 값 원천 · C7 → 권한.

## 전수표 28행 처분

**27행 넣음 · 1행 웹 전용(#4 [고객 차트] — 앱에 고객 차트 화면 없음) · 빠진 행 0.** #1 의 「누른 시술 강조(웹 `sec` 깜빡임)」만 웹 전용으로 따로 두고 OQ-A63. 표 = SPEC-003 §4 「웹 차트 기능 28행 처분」.

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error · 263 warning** — 작업 전과 같다(0 error · 263 warning). `products/day/` 범위 ERROR 0 · WARN 0. 263 WARN 은 전부 다른 제품(selly 등) 기존 것 — 무관.
- migration 판단 = **없음**(같은 service · 같은 칸 · 새 권한 키 · 새 테이블 없음 — D8 · C7). 앞단 Caddy 100MiB 한 줄은 배포 설정(D-7).

## 계약 준수 · 결정과 다른 점

- 결정 D1 ~ D11 · C1 ~ C36 다시 열지 않음. 웹 동작 · 권한 · 사진 대상 규칙 무수정.
- **D6 vs 웹 차이 기록**: 웹은 미저장이 없으면 바깥 누름으로 닫힘 · D6 문장은 「끌어 내림 · 바깥 누름으로 안 닫힘」 → D6 그대로 쓰고 차이를 U-23 · OQ-A71 에 적음.
- 글자: 기존 SPEC-002 · 003 글자만 씀(「저장」 · 「최근 저장 : 」 · E59 세 글자 · C26 · C27 · C29 · C36 · 「시술 전」 · 「시술 후」). 탭 글자 · 드로어 머리 · 사진 버튼 글자 · iOS 문구는 비워 OQ(A64 · A65 · A67 · A78).

## 미결 · 주의점

- **OQ-A63 ~ A78(SPEC-003)** · **OQ-99 · 100(SPEC-002)** — 전부 착수 비차단 · 기본값(planner 제안 · 코디 확인 전). 사용자 · 코디 확인 권장 순:
  1. OQ-A65 탭 글자 — 기본값 = 웹 글자 셋(「간호관리차트」 · 「의사차트」 · 「시술전후사진」)
  2. OQ-A71 미저장 없을 때 바깥 누름 — 기본값 = D6 그대로 늘 안 닫힘(웹과 다름)
  3. OQ-A76 아이패드 팝오버 · 창도 세션 Navigator 로 — 기본값 = 함께(D9 는 폰 시트 둘만 명시)
  4. OQ-A70 저장 · 올리기 중 닫기 — 기본값 = 끝날 때까지 닫기 꺼짐
  5. OQ-99 앱 JSON 응답 모양(409 걸린 줄을 `details.conflicts` 에) · OQ-100 사진 오류가 `/api` 공용 모양으로 나가는지 — WORK 에서 코드 확인
  6. OQ-A64 iOS 권한 문구 — 정식 출시 전 사용자 문구 필요(D10)
- 코드 사실(WORK 참고): 앱 `core/copy.dart` 가 C29 전 웹 표 복제(`chart_conflict` 뺌 · `chart_staff_required` · `staff_not_listed` 빈 글자) → C29 글자로 맞춰야 함(U-23 에 적음). 통역 시트 둘도 같은 탭 Navigator(OQ-A77 · 이번엔 그대로).
- 못 고친 앞 판 문장: A-38 「담당 원장 바꾸기 … 호출 0건」은 0.2.0 이후 사실과 다르지만 이번 범위(차트)가 아니고 OQ-A62(0.1.0 문장 정리 — 다음 cut)에 해당해 그대로 둠.
- SPEC-003 · 002 `status` 는 stable 그대로(앞 개정 관례 · 개정 머리글에 「코드 미반영」 기준선 주의).
