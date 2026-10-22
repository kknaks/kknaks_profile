# [planner] 머지 전 SPEC · WORK 동기화 — 10-21 이후 결정 · 구현 반영

너는 **cc-prototype `planner` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/planner/role.md`
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2`(문서 레포 · **public**). 코디가 같은 워크트리에 있다 — allowed_paths 밖 금지.

## 왜
SPEC-003 · SPEC-004 · WORK-003 · WORK-004 는 10-21 판이다. 그 뒤 결정 · 구현이 코드(main `329b543`)에 들어갔고 문서는 낡았다. **문서 PR 머지 전에 코드와 맞춘다.**

## SSOT(이 순서로 이긴다)
1. `orchestration/work/myeongdong-poc-v2/_RESUME.md` §2 결정 표(10-21 · 10-22 줄 전부 · 줄 친 것은 뒤집힘)
2. 피드백 처분: `orchestration/work/myeongdong-poc-v2/e2e-feedback-batch-1.md`(웹 E2E-1~12) · `e2e-app-feedback-batch-1.md`(A1~A7) · `e2e-device-feedback-batch-1.md`(T1~T8) · `fix-decisions-r1.md` · 리뷰 `review-*-report.md`
3. **코드 사실**(read-only): `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` 의 `procedure/`(= origin/main 329b543) — API 경로 · 응답 필드 · 오류 코드 · env 이름 · 권한은 **코드에서 읽어 적는다**(추측 금지)
4. 배포: infra PR #22~#24(차트 · APNs 마운트 /etc/apns · 이미지 태그 · ArgoCD 수동 동기화)

## 반영할 것(최소 — 전수는 1·2 를 다 읽고 세라)
- **정상 로그인**(OQ-601 닫힘): POST /api/auth/login {id, password} · bcrypt · /api/auth/accounts 제거 · 5회/1분 잠금 · env CCC_*_PASSWORD · 앱 서버 주소 칸 debug 만
- 알림: [수락] 액션(CALL 카테고리) · push_log · 관리자 수신 · 잘못된 토큰 삭제 · X-Accept-Source
- 웹 E2E: 방 배정 이어 보내기(방→담당자→호출) · 1.5초 확인 조회 · 귀가 대기 = KOS 방 배정 취소 + COMPLETED 까지 흐림 · 카드 높이(판 절반 · px 고정 없음) 등 E2E-1~12 처분대로
- 앱: T1~T8(태블릿 두 열 · 한 줄 머리 · 반응형 글자 · 필터 + 귀가 칩 · canCall 규칙 · 통역 칩 · iOS 15)
- 배포 사실(WP10 · 앱 WP 의 TestFlight 빌드 1~3) — WORK 의 각 WP 상태를 실제대로(done · 남은 것)
- **데모 환자 스킬**: 코드 레포 `.claude/skills/kos-demo-patients/` · `procedure/tools/kos_demo_patients.py` — WORK 에 한 줄(운영 도구)
- 열린 것 갱신: 닫힌 OQ 표시 · 남은 것(실기기 워치 [수락] · 통역 실음성 · KOS-DEMO 원장 목록 제외 여부 · 재내원/수납 API 없음 · 옛 cc-db PVC 정리)
- 각 문서 frontmatter version/updated_at · README 인덱스 상태

## allowed_paths
- `para/projects/summer-star/cc-prototype/20-spec/` · `30-work/` · `10-decision/decision-005-procedure-board.md`(**OQ 상태 표시만** — 결정 본문 수정 금지 · 새 결정이 필요하면 「열린 것」으로 보고) · `reference/2026-10-12-cc-prototype/workflow-v2.md`
- 그 외 read-only · 커밋 · push · PR 금지

## 하지 말 것
- 결정 발명 · 코드에 없는 기능 기술 · 키/토큰/비밀번호 값 · 실명 · 이메일 · KOS id · Apple 팀 id(public)

## 검증
- 바뀐 규칙 줄마다 근거(_RESUME 날짜 줄 · E2E-n · T-n · 코드 파일:줄)
- 코드 API 경로 전부(back router grep) ↔ SPEC API 표 대조 — 빠진 것 0 · 없는 것 0
- public grep(@ 메일 · 긴 토큰 · 비밀번호 값 · 한글 실명) 0 · 링크 · 인덱스

## 5-1. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "planner 완료: SPEC · WORK 동기화(머지 전)" \
  --body "변경 파일 / SPEC 절 요약 / WP 목록 / 열린 것 / DEC 대응표 누락 0 여부 / 검증"

orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] planner SPEC 동기화 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] planner: <질문>" --enter`
