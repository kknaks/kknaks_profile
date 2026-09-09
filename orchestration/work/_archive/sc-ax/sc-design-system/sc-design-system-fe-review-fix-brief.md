# [frontend] PR #2 리뷰 수정 — F3 권한 부여 대상 불일치 · F7 조직 전환 후 더 보기 합쳐짐 · F6 Select Esc 가 Drawer 까지 닫음

너는 **sc-ax `frontend` 워커**다. 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/sc-ax/orchestration/roles/sc-ax/frontend/`.
워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `58c9ed4`, PR MediSolveAIDev/ax-workspace#2). **같은 워크트리에서 backend 워커·frontend 워커·사용자의 디자인 시스템 세션이 동시에 작업한다** — 자기 영역 밖 파일은 절대 만지지 않고, `git status` 에 남의 변경이 보여도 되돌리지 않는다. 커밋·push 는 코디가 한다.

리뷰: PR #2 의 zeroam 리뷰(2026-09-09, 코드 위치별 인라인 코멘트 8건). 원문은 `gh api repos/MediSolveAIDev/ax-workspace/pulls/2/comments` 로 읽어라 — 각 코멘트에 **재현 방법**이 적혀 있으니 그 재현을 먼저 테스트로 옮겨 RED 를 만든 뒤 고친다. 리뷰어가 「별도 판단」으로 분리한 2건(부서 관리자의 전사 개인정보 열람 정책 · null=비공개/없음 동일 표현)은 **손대지 않는다.**

## 3. 계약 — 고칠 것 3건 (리뷰 번호 그대로)
- **F3 [높음]** `OrgPage.tsx` 상세 조회 응답 경합: A 요청 지연 중 B 선택 → B 응답 뒤 A 응답이 상세를 덮고, `AccessDrawer` 는 A 를 보여주면서 `grant()` 는 `selectedMember.member_id`(B) 로 보낸다. **요청 세대(또는 member_id 일치)로 늦은 응답을 폐기**하고, Drawer 가 표시하는 대상과 변경 대상 ID 를 **같은 상태 하나**에 고정. 지연 fetch mock 회귀 테스트(payload 의 member_id 가 표시된 사람과 같은지).
- **F7 [중간]** 변경 기록 「더 보기」 append 가 요청 당시 조직과 현재 선택 조직을 비교하지 않고, `loadActivity()` 첫 페이지도 이전 응답을 폐기하지 않는다. 조직별 요청 세대로 첫 페이지·추가 페이지 모두 현재 선택에 유효한 응답만 반영. 지연 응답 회귀 테스트.
- **F6 [중간]** `Popover.tsx` 의 document keydown 과 Drawer 의 window keydown 이 같은 Escape 를 둘 다 처리 → Select 를 닫으려던 Esc 가 Drawer 까지 닫아 사유 입력이 사라진다. **가장 위 오버레이만 Esc 를 처리**(예: 오버레이 스택, 또는 Popover 가 처리한 이벤트는 Drawer 가 무시). 부모 편집 상태·포커스 유지. 「Drawer 안 Select 열고 Esc → 목록만 닫힘, 사유 유지」 회귀 테스트.

## 5. allowed_paths
- `frontend/src/OrgPage.tsx` · `frontend/src/org/*` · `frontend/src/Popover.tsx` · `frontend/src/Modal.tsx`(Drawer Esc 처리) · `frontend/src/Select.tsx`(필요하면) · 옆자리 테스트
- **금지**: `backend/` · `api.ts` 계약 변경 · `.design-sync/` · `ds-entry.tsx` · `package.json` · 커밋·push. 사용자 디자인 세션이 만지는 파일(`DatePicker.tsx`·Toast 등)은 건드리지 않는다.

## 8. 검증
```
cd frontend && npx tsc --noEmit (0) + npx vitest run <만진 테스트 + 새 회귀 테스트 3개>. hex 0 · api.ts 밖 fetch 0. 보고에 F3·F7·F6 각각 「재현 테스트(RED) → 수정 → GREEN」 표. git status 에 네 변경 = 위 allowed 만.
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e9a4432b-f153-45a5-97d4-63887e3329f1 --from term_84848caa-720e-43c6-a5e8-cace7ddfd166 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e9a4432b-f153-45a5-97d4-63887e3329f1 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e9a4432b-f153-45a5-97d4-63887e3329f1 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
