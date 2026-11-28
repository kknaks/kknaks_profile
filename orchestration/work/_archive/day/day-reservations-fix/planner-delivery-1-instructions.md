# [planner] R4-1 긋기 → SPEC 커밋 · draft PR → WP 나누기 · Delivery Issue 발행

같은 터미널이면 앞 맥락 그대로. Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md`(이 워크트리).

문서 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec`(branch `kknaksss/day-reservations-fix-spec` · base `origin/main` `b9ac374e` · 미커밋 변경 = 고침 1 ~ 4)
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix`(origin/dev `65506f35` · 변경 없음)

## 할 것
1. **R4-1**(`review-doc-4-report.md` 같은 폴더) 고칠 방향 글자 그대로 `spec-006:613` 한 줄. 그 밖 SPEC 문장 바꾸지 마라. lint `--strict` products/day ERROR 0.
2. SPEC **커밋 · push · draft PR**(→ `main`) — 제목 예 `docs(day): 예약 현황판 F1 ~ F6 · 문진 6개월 · KOS 문진 읽기 (SPEC-006 ⑯ · 007 · 000 ④ · 002 · 003)`. **머지하지 마라**(최초 Delivery = pending baseline · 승인은 사용자).
3. WP 나누기 — backend · frontend · 앱 **병렬**이 되게(의존은 실제 순서만). 최소:
   - BE: F6 origin 4곳(`routers/reservation_detail.py` · `routers/api/reservations.py`) + GET 라우트 실제 service 시험 · Rule 15 배치 값(`rows` · `lane` · `line` · `start_min` · `end_min` — 웹 · 앱 하나) · `open_min = 0` 그룹 볼 것 · KOS 문진 읽기 별도 태스크(내부 legacy 경로 · mapper · `external_ref` · 6개월 건너뜀 · 400 = 없음) · `questionnaire.expired` · 팝오버용 기기 목록 · 요청 생성 흐름(고르면 그때 생성)
   - FE(웹): F1 오른쪽 70 · 점선 [+] · 툴팁 · Rule 15 그리기(1시간 행 140 · 줄 접기) · [문진 QR] 한 단계 팝오버 · [여권 스캔] 기기 팝오버 · F5 카드 제거 · 「6개월 경과」
   - 앱: 예약현황 표 Rule 15(30분 칸 × 2) · 상세 「6개월 경과」
   - 각 WP: 범위 · BE ↔ FE/앱 계약(SPEC 절 인용) · 완료 조건(로컬 KOS 데모 지점 실물 e2e 1회 · D46 ② 제출 id = 읽은 id · D45 팝오버 안 닫힘) · migration(있으면 alembic head 이어짐) · 되돌리기
4. Delivery Issue 발행 — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservations-fix-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = 2 의 커밋 sha(머지 전 · spec-baseline:pending). 막히면 우회하지 말고 출력 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/delivery/`
5. `30-work.md` Spec Coverage 행 · `log.md` 한 줄 → 커밋 · push 해서 같은 PR 에 얹어라(lint 0 error).

## 금지
코드 수정 · SPEC 계약 변경(필요하면 멈추고 보고) · PR 머지 · 공개(open) KOS 호출 · 화면 문구 짓기.

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/delivery-1-report.md` — SPEC PR 번호 · baseline sha · Issue 번호 · WP 표 · 계약 · 막힌 것. 완료 보고 두 명령(subject 「planner 완료: Delivery 1」 · 이번 dispatch 값 · 코디 `term_99b025fc-f3ef-403e-8162-509c41545e2e` — preamble 이 다르면 preamble).
