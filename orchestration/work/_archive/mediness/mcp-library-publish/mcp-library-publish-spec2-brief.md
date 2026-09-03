# [planner] MCP 도서관 발행 — 스펙 확정 반영 + WP 초안

너는 **mediness `planner` 워커**다. 직전 태스크(SPEC-013·060 개정 초안)의 연속이다 — 역할 문서와 맥락 그대로.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec`
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness`

## 1. 확정된 결정 (사용자 리뷰 통과 — 이대로 반영, 재논의 금지)

1. **개정 초안 전체 승인.** reviewer_spec 판정 PASS (위반 0).
2. **OQ-a = 즉시형 예외 확정.** 보상 통제 4건(관리자 전용 노출·화이트리스트 파급 고정·전건 revert·오염 turn 차단) 그대로. **Action Runtime 배선이 baseline 도메인에 닿으면 카드형 승격을 재검토한다**는 조건을 명시적 문장으로 남긴다 (OQ-a 는 닫고, 승격 조건은 해당 절 본문 또는 잔여 OQ 로).
3. **W-1**: SPEC-003 §3.2 의 baseline 도메인 2행을 **한 행 병합** (같은-SPEC 다중 leaf 한 칸 나열 — 8건 선례를 따른다).
4. **W-2**: SPEC-013:202 부근의 「§6 머리 규약 그대로」 지시자를 실제 가리키는 대상이 존재하도록 문구 수정.
5. OQ-b(감사 origin 축)·OQ-c(leaf 부여 확대)는 **열린 채 유지.**

## 2. 구현 단계

1. **스펙 확정화**: ⏳ 「초안(사용자 리뷰 전)」 라벨을 확정 표기로 정리 (2026-08-28 사용자 승인). OQ-a 닫기 + 승격 조건 명시. W-1·W-2 수정. SPEC-060 인벤토리의 ⏳ 예고 주석은 **유지** — 착지(구현 머지) 시 갱신이라는 기존 논리 그대로.
2. **WP 신설**: `30-work/` 규약대로 WP 1건 — 구현 계획:
   - mcp: `mediness.baseline_publish` 도구 (tool_access `requires("baseline.publish.agent")` · requires_tools · 오염 등급 선언, 기존 도구 패턴)
   - back: `POST /api/v1/library/baseline/agent-publishes` 전용 라우트 (JSON body · 256 KiB 판정 · upload|update · 기존 `prepare_upload→BaselinePublisher.publish` 경유)
   - capability: `baseline.publish.agent` leaf 신설 + system_admin 부여 (시드·마이그레이션은 기존 leaf 신설 선례 — `landing_chat.usage.read` — 를 따른다)
   - 테스트: 두 층 차단 검증(비관리자 노출 안 됨 + 라우트 403), 화이트리스트·크기 상한·operation 범위
   - 완료 시 갱신할 것: SPEC-060 인벤토리 write 18→19 · /health 57→58
   - WP 는 **draft** — 사용자 리뷰 후 구현 발주
3. `30-work.md` 3자 일치(WP List·Status Board·Spec Coverage) + `log.md` 이력 + lint.

## 3. 하지 말 것

- 코드 작성 금지. 이번에도 문서까지다.
- 확정된 설계(전용 라우트·leaf 이름·256KiB·upload/update·즉시형)를 바꾸지 마라.
- rebase 하지 마라 — origin 1커밋 앞선 것은 코디네이터가 PR 전에 처리한다.

## 4. 검증

```
python3 scripts/lint-pipeline.py --strict → products/mediness/ 범위 ERROR 0 (30-work 3자 일치 포함)
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch context> \
  --dispatch-id <이 태스크의 dispatchId — dispatch context> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 / 요약 / 검증 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 헤매지 말고 같은 (2) 방식으로 물어라.
