# [backend] 앱 WORK-009 — WP-BE1 → BE2 ∥ BE3 → BE4 → BE5

너는 **cc-prototype `backend` 워커**다. **앞 판 맥락이 없다.** 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/roles/cc-prototype/backend/role.md`(+ 같은 폴더 rules · skills · tools · workflow)를 읽어라. 작업 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **`procedure/back/**` 만**(compose · .env.example 은 WP-INFRA 몫 — 필요하면 물어라).

## 계약 (SSOT)
- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` **0.4.1** · `10-decision/decision-007-app-v2.md` · `30-work/work-009-app-v2.md`(내 WP 줄 · 병렬 · 주의)
- 웹 규칙: `20-spec/spec-005-reservation-board.md` 0.4.0 · `spec-003-procedure-board.md` 0.6.0 · KOS 근거 `orchestration/work/overall-board/app-kos-report.md` · `app-wp-kos-report.md`
- 결정: `orchestration/work/overall-board/_RESUME.md` §2 10-27 앱 줄 — **E2E 는 먼저 iPhone 시뮬레이터**
- 코드: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` branch **`kknaksss/overall-board-2`**(최신 `95c64bc`)

## 할 일 — WORK-009 줄 그대로, 한 워커가 차례로
BE1 계정 · 기기 · 알림 바탕(`counselor` 역할 · 상담사 계정 동기화 · `device` 열 · `deviceId` · `notification` · 설정 · SSE · `push_log` — **F1 마이그레이션 방식 그대로**) → BE2 상담사 호출 푸시 ∥ BE3 띄우기 요청 → BE4 문진(KOS 공개 양식 · 제출 · 언어 표 · 이력) → BE5 여권 스캔 · 사진(`PROC_PHOTO_DIR` · KOS 이미지 = WP-KOS 결과 모양 · **법적 검토 주석**). 경로 수 50 시험.
- **데모 실호출 완료 조건**: BE4 문진 제출 1 · BE5 여권 수정 + 이미지 올리기 1(시험 고객 `[ccc 시험]` · **TEST 그림** · 운영 키 금지 · 데모 테넌트 assert)
- 앱 워커(mobile)가 **병렬로** 화면을 짠다 — 응답 모양을 바꿔야 하면 멈추고 물어라(SPEC 먼저)

## 검증 · 금지
- WP 마다 `cd procedure/back && uv run ruff check . && uv run pytest -q -k <WP 키>` · 끝에 전체 `pytest -q`
- 사용자 포트 3700 · 8700 · 그 프로세스 금지 · public 누출 금지
- 보고서 `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/app-backend-report.md`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** **커밋 · push · PR 금지**(코디가 한다).
- WP 하나 끝날 때마다 보고서에 절을 더하고 **아래 (2) 한 줄만** 보내 진행을 알린다. 전부 끝나면 (1) · (2) 둘 다.
```bash
# (1)
orca orchestration send --to term_678ac61d-2472-4a9b-ba73-61883337b957 --from term_dd19c7b3-c9f7-429b-9199-242250637a83 --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "backend 완료: <한 줄>" --body "보고서 경로 / 바뀐 파일 / 검증 수치 / 데모 흔적 / 미결"
# (2)
orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[worker_done] backend — <WP · 한 줄>. 상세는 보고서." --enter
```
- 막히면: `orca terminal send --terminal term_678ac61d-2472-4a9b-ba73-61883337b957 --text "[질문] backend: <질문>" --enter`
