# WORK-001 · WORK-002 검수 지시서

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-review-doc-brief.md`(같은 폴더)의 역할 · 제약 · §9 완료 보고를 그대로 적용한다.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev`

## 읽을 것

1. 검수 대상: `$W/WORK-001-hub.md` · `$W/WORK-002-app.md`
2. 계약: `$W/SPEC-001-hub-gold-mcp.md` · `$W/SPEC-002-chat-eval.md`(0.4.1 PASS) · `$W/_RESUME.md` §2
3. 지시: `$W/work-write-instructions.md` · `$W/review-spec-001-002-r5.md` Z-1 ~ Z-3
4. 레포(읽기만): `~/git/PROCEDURE-HUB`(`git show origin/release/v1.2.0:`) · `~/git/clinic_chat`(`origin/main`) · 옛 틀 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` · `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(`git show HEAD:`)

## 볼 것

1. **SPEC ↔ WP 대응** — SPEC 구현 대상 절이 전부 WP 에 걸렸나 · WP 가 SPEC 에 없는 동작을 지어냈나(결정 위반 · 원칙 · 안전 강제 첨부 폐기 포함).
2. **실행 가능성** — 파일 경로 · 의존 · 진입점 · 검증 명령이 실제 레포 구조에서 돌 수 있나(`git ls-tree` · README 「검증」 절 · pyproject). 포트 18105 · 데이터 env · 키 env 이름.
3. **완료 조건이 검사 가능한가** — 문장마다 무엇을 돌려 무엇이 나오면 끝인지. 실물 확인 E1 ~ E6 이 「실물 호출 1회」 를 실제로 요구하는지.
4. **순서 · 병행 · 모의 허브 한계** 설명이 맞나(§11).
5. 코디가 받은 C-1 ~ C-3 제안(답 프롬프트 초안 먼저 · 추가 문항 워커 초안 → 사용자 확정 · 실물 확인은 워커 → 안 되면 코디)이 SPEC · 결정과 부딪히지 않나.
6. WORK-001 §10 H-1 ~ H-3 제안이 SPEC-001 계약을 바꾸는지(바꾸면 FAIL — SPEC 고침이 먼저).
7. 공개 레포 grep.

## 산출

`$W/review-work-001-002.md` 1개만. 문서별 판정 + 지적 표(문서:줄 · 심각도 · 근거 · 고칠 방향).
