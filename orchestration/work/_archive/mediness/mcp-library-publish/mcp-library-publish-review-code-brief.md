# [reviewer_code] backend 리뷰 — WP-123 구현 (leaf · 전용 라우트 · MCP 툴 · 테스트)

너는 **mediness `reviewer_code` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/roles/mediness/reviewer/` 5종.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/mcp-library-publish`
base: `origin/dev` → PR `dev`

**리뷰 모드: backend 리뷰.** read-only — 코드를 고치지 않고 **테스트도 돌리지 않는다.**
산출물 = 리뷰 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/sc-interview/orchestration/work/mcp-library-publish/review-code-report.md`

## 검수 대상·기준

- diff: `git diff origin/dev...HEAD` + untracked (예상 17파일 — back 9 · mcp 8)
- 계약 SoT: `/Users/kknaks/orca/workspaces/mediness-mediness/mcp-library-publish-spec/products/mediness/30-work/work-123-mcp-baseline-publish.md` + `20-spec/spec-013-baseline-publish.md` §3 MCP 계약
- 원 워커 allowed_paths: `back/` · `mcp/` · docker-compose 2종
- 기준 문서: `roles/mediness/backend/rules.md` + 리포 기존 패턴

## 특별 검수 항목 (일반 체크리스트에 추가)

1. **웹 발행 무변경 계약** — 기존 3 endpoint 핸들러의 시그니처·의존·본문이 실제로 diff 0 인가. `_publish_form`→`_publish_bytes` 어댑터 추출이 동작 보존 리팩터링인가 (동작 변화 지점이 있으면 FAIL 근거)
2. **재구현 부재** — 신규 라우트·툴이 화이트리스트·slug·frontmatter·publish_lock·git 을 재구현하지 않고 기존 서비스 계층을 경유하는가. 툴 쪽에 상한 숫자·경로 규칙이 숨어 있지 않은가
3. **계약값 일치** — leaf 이름·system_admin 단독 부여·256 KiB(경계 포함)·upload|update·400 코드 재사용(신규 코드 발명 없음)·delete 부재
4. **migration 0134** — 선례(0095) 동형·ON CONFLICT·downgrade 역순·down_revision 정확성
5. **테스트 상수 일괄 갱신(61·beyond_caller 2종)** — 하드코딩 4파일 갱신이 전부·정확한가, 갱신 누락 파일이 없는가 (grep 으로 확인)
6. **선재 실패 6건 분리** — 워커가 무관·선재로 분리한 근거(HEAD 동일 실패)가 리포트에 재현 가능한 형태로 남아 있는지 — 직접 테스트 실행은 하지 말고 워커 보고·코드 상태로만 판단, 판단 불가면 「코디 재확인」으로 표기

## 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 다르면 preamble 이 맞다.

- 커밋·push·PR 금지. subject 에 판정(PASS/WARN/FAIL)을 박는다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_915b3ecb-68dd-4d26-98f7-ef3f645318fb --from <네 워커handle> \
  --type worker_done \
  --task-id <taskId — dispatch context> --dispatch-id <dispatchId — dispatch context> \
  --subject "reviewer_code 완료: <판정 — 한 줄>" \
  --body "판정 / 위반(파일:줄+근거) / 확인한 것 / 리포트 경로"

# (2) 직접 주입
orca terminal send --terminal term_915b3ecb-68dd-4d26-98f7-ef3f645318fb \
  --text "[worker_done] reviewer_code 완료 — <판정> <한 줄>. 상세는 인박스." --enter
```
