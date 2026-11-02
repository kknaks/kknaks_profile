# [writer] strong-hajin-polish3 회고를 개념으로 소화한다

너는 **strong-hajin `writer` 워커**다. **맥락이 없다** — 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/planner/role.md`
- 규약 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/areas/area.md` **§3 전부**(3.3 규약 · 3.4 맵) · 양식 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/templates/concept.md`
- 회고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/log/2026-10-05-strong-hajin-polish3.md` **§2 「적용한 기술·개념」** 네 항목
- 선례 커밋: `git -C /Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화 show daac38b` (polish 회고 소화 — 신규 둘·보강 셋, 회고 §2 역링크)

작업 위치: 코디 워크트리에 직접 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화` (브랜치는 main 과 같은 상태)

## 할 일
회고 §2 의 각 항목을 **3.4 맵에서 먼저 찾아**(파일명 + `aliases` grep) 기존 노트가 있으면 **보강**(`up:` 에 출처 더하고 본문에 녹임), 없을 때만 **신규**(영문 kebab-case · `up:` 필수 · 3.4 맵 한 줄). 후보(판단은 네가 — 근거 보고):
1. 인라인 즉시 저장을 서버 낙관적 잠금(version +1·422)에 맞춰 **한 줄 대기열로 직렬화** — 「version 을 올리는 명령 전부」를 세야 닫혔다
2. 상태 전이 UI = **서버 허용표를 비추기만**(화면이 규칙을 만들지 않음 · 선행 막힘을 미리 막지 않고 서버 문장 토스트)
3. **Tauri/wry 웹뷰의 첨부 응답** — 응답 헤더를 못 보고 표시 가능 MIME 을 Allow → 셸이 요청 단계에서 가로채 쿠키를 실어 직접 받음 · inline 은 아무것도 안 함 · eval+CustomEvent 로 권한 0 알림
4. 와이어프레임으로 사용자와 좁혀 가기 — 개념이 아니라고 판단되면 건너뛰고 이유 보고
- 각 항목에 회고 §2 쪽 **`[[개념]]` 역링크**를 단다(회고 파일 수정 허용 — §2 역링크만)
- 사람 실명·메일 금지(공개 레포)

## allowed_paths
- `para/areas/concept/**` · `para/areas/area.md`(3.4 맵 줄 추가만) · 회고 파일 §2 역링크
- 커밋·push 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "writer 완료: polish3 개념 소화" --body "신규 / 보강 목록(파일) / 건너뛴 것과 이유"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] writer 완료 — polish3 개념 소화." --enter
```
