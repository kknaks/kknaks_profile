# [frontend] WORK-008 Phase 3b — AX 업무 초안 요약 카드 · 「수정」= 새 업무 추가 모달 · 「AX 제안」 칩

너는 Phase 1·2 를 끝낸 **strong-hajin `frontend` 워커**다. 같은 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` — 지금 HEAD `4a89650`(Phase 1 `9255028` · Phase 2 `1ef8db0` · BE 3a `4a89650`).
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/frontend/role.md` (+ rules 등)

## 1. SSOT
- **WP** `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` — **Phase 3b**(와이어프레임 포함) + 원칙 P-1·P-2·P-3
- **SPEC (정본 — WP 와 다르면 SPEC 이 맞다)**: `…/strong-hajin/20-spec/`
  - SPEC-002 **§2.4**(AX 초안이 보이는 자리) · **§2.9**(AX 업무 초안 카드) · **S-7** · **§6**
  - SPEC-001 **U-2**(「AX 제안 N」 칩) · **S-9** · **§6**
- BE 계약 검수: `…/orchestration/work/strong-hajin-polish/review-be-p3a-report.md` (FE 계약 표·필드 대조표)
- 조사: `fe-survey-report.md` §5(D-02 카드) · §6(A-01)

## 2. BE 계약 (3a 커밋 `4a89650` — 이대로 소비)
- 대상 kind: `ax.task.create_self`(업무 생성 → 「내 업무」 갈래) · `ax.work_request.create`(업무 요청 → 「요청 업무」 갈래). 다른 AX 카드는 **바꾸지 않는다**
- `GET /api/action-items`(홈 판단 대기와 같은 응답) · `GET /api/action-items/{id}` 의 AX 봉투:
  - `edit_contract.values` — 초안 필드 **전체**(title · description · start_date · due_date · checklist · reference_task_ids · parent_task_id · project_id · cc_member_ids · preceding_task_ids · approver_id · assignee_id, 요청은 + supersedes_request_id). **카드 요약과 모달 초깃값은 이것에서 읽는다**
  - `edit_contract.fields` — 편집 칸 목록(필수 표시 포함). 기한은 이제 **선택**
  - `created_at` — ISO 8601 문자열(「만든 지 며칠」)
  - 명령: `allowed_commands`(확인·거절). 확인(`POST /api/action-items/{id}/commands/confirm`)은 **고친 초안(`draft`)을 함께 실을 수 있다** — 회차·diff 는 서버가 남긴다. 실을 값의 모양·버전 필드는 지금 `ActionTaskCard` 가 보내는 confirm 본문 그대로
- 자료: 생성 명령의 필드가 아니다 — 기존 AX 자료 초안 경로(`action_material_drafts` · `attachment_draft_ids`)를 그대로 쓴다

## 3. 계약 (WP 3b · SPEC-002 §2.9)
1. **요약 카드** — 채팅의 두 kind 카드를 높이 고정 요약 카드로:
   - 헤더: 배지 「AX」(「SC AX」 → 「AX」) · 「초안 · N회차」 · 종류(업무 생성/업무 요청) · 제목 · **4칸 바**(현재 칸 검정, 나머지 옅게, 누르면 그 페이지) · 현재 페이지 이름
   - 본문: 새 업무 추가 모달의 탭 4개(`CreateTab` = 기본 정보 · 체크리스트 · 업무 연결 · 자료)의 **읽기 전용 요약**, 페이지·필드 1:1. 빈 페이지는 「없음」 한 줄
     - 기본 정보: 갈래 · 시작일→마감일 · 담당 후보(요청) · 내용 두 줄 · 참조자 · 결재자
     - 체크리스트 「N개 · 첫 항목…」 / 업무 연결 「상위 · 프로젝트 · 참고 N · 선행 N」 / 자료 「파일 N · 링크 N」
   - 넘김: 본문 **호버 때만** 좌우 ‹ ›(첫/끝 페이지는 해당 화살표 숨김, 본문 위 겹침) · 트랙패드 좌우 스와이프 · 키보드 ← → · 바 클릭
   - 아래: [거절] [수정] [등록]. [등록] = 초안 그대로 확인 · [거절] = 기존 거절 · [수정] = 아래 2
   - 등록 뒤: 한 줄 요약(제목 · 기한 · 담당) + [업무 열기]로 접힌다
2. **「수정」= 「새 업무 추가」 모달 그대로** — `CreateWorkModal` 을 AI 초안 값으로 채워 연다. 탭·필드·검증 모두 모달 것(**새 폼을 만들지 마라**)
   - 갈래는 초안 kind 로 **고정**(바꾸면 다른 명령이 된다 — 갈래 전환 비활성)
   - 모달의 제출 단추 = **고친 값으로 확인(confirm + draft)**. 새 업무를 따로 만들지 않는다. 닫으면 고친 것을 버리고 카드는 초안 그대로
   - 모달을 이 모드로 여는 방법(prop 등)은 기존 `initial` 경로를 넓히는 쪽으로. 쓰는 곳 전부 세어 일반 「새 업무 추가」 동작이 바뀌지 않게
   - 자료 탭: 기존 AX 자료 초안 흐름을 쓸 수 있으면 쓰고, 못 쓰면 읽기 전용으로 두고 DS-gaps·보고에 적는다
3. **A-01 보이는 자리** (SPEC-002 §2.4 · SPEC-001 U-2)
   - 홈 판단 대기: 두 kind 카드를 누르면 **같은 요약 카드**(모달)로 거절·수정·등록
   - 업무 › 내 업무 칩 바: **「AX 제안 N」** — 다른 칩과 같은 필터 칩(하나만 켜짐), 자리는 `받은 요청` 바로 뒤, `기한 지남` 맨 끝 유지, **0건이어도 「AX 제안 0」**
   - 칩을 켜면 목록이 **AX 초안 줄**로: 업무 행과 같은 열 틀(업무명 · 요청자 자리 「AX」 · 기한 · 상태 「초안」 · 만든 지 며칠), 행 액션 칸 비움. 줄을 누르면 요약 카드
   - AX 초안 줄은 **그 칩을 켰을 때만** — 「전체」·다른 칩·「받은 요청」 수신함에는 섞지 않는다(`MyWorkPage.test.tsx` 의 기존 단언 유지)
   - 자동 만료 없음. 「만든 지 며칠」
   - Phase 2 의 화면 기억(`screenCache`)을 쓰는 화면이면 같은 규칙(기억한 envelope 로 명령 열지 않음)을 지킨다
4. **P-2** — DS 부품·토큰만. 시안 없는 자리(4칸 바·호버 화살표 등)는 기존 부품 조합으로 만들고 DS-gaps 에 적는다

## 4. P-3 전수조사 (보고에 개수)
`ActionTaskCard` 를 쓰는 곳 · `scax-actioncard` 계열 · `SC AX` 문자열 · `CreateWorkModal` 여는 곳 · action item 을 그리는 곳(홈 `ActionCenter` 등) · 칩 정의(`labels.ts` 등)

## 5. allowed_paths
- `frontend/src/` 만. `src-tauri/`·`backend/` 금지

## 6. 하지 말 것
- 커밋·push 금지. **서버·브라우저 금지** — 코디 로컬 스택(8001·5176, 3a 백엔드로 재시작됨)이 떠 있다
- 결정되지 않은 것을 메우지 마라 → [질문]

## 7. 검증
- 직렬 vitest(`npx vitest run --no-file-parallelism`) — 바뀐 파일 + 마지막 전체 1회. 기준선 실패 5(`flaky-baseline-evidence.md`) 외 새 실패 0
- `npx tsc --noEmit` · `make frontend-build`
- 테스트: 카드 4페이지 넘김(바·화살표·키보드) · 빈 페이지 「없음」 · 수정 → 모달이 초안 값으로 열림·갈래 고정 · 모달 제출이 confirm+draft · 닫으면 버림 · 등록 뒤 접힘 · 칩 0건 표시·켰을 때만 초안 줄·줄 클릭 카드 · 홈 판단 대기 카드 클릭 → 같은 카드 · 「SC AX」 0건

## 8. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다.
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 3b" \
  --body "변경 파일 / 계약 1~4 체크 / 전수조사 개수 / 테스트·tsc·build / DS-gaps / 미결"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — WORK-008 Phase 3b. 상세는 인박스." --enter
```
막히면: `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] frontend: <질문>" --enter`
