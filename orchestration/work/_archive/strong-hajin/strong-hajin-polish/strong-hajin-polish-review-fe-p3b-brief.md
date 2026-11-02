# [reviewer] WORK-008 Phase 3b 코드 검수 — frontend 리뷰 모드

너는 **strong-hajin `reviewer` 워커**다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only.**

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` 의 미커밋 변경(`frontend/` — HEAD `4a89650` 위). 새 파일 `features/action/AxDraftCard.tsx`·`.test.tsx`.

## 2. 기준
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 3b**(와이어프레임) · P-1·P-2·P-3
- SPEC: SPEC-002 §2.4·§2.9·S-7·§6 · SPEC-001 U-2·S-9·§6 (같은 레포 `20-spec/`)
- 발주서 `…/orchestration/work/strong-hajin-polish/strong-hajin-polish-fe-p3b-brief.md` · BE 계약 `review-be-p3a-report.md`
- 워커 보고 요약: AxDraftCard(두 kind) · CreateWorkModal axDraft 모드(갈래 고정, 제출=confirm+draft) · 홈 판단 대기·「AX 제안 N」 칩·AxDraftTable · 「SC AX」 노출 0 · 직렬 1164 중 기준선 5 실패 · tsc 0 · build. 워커가 스스로 연 미결: ① 수정 창 자료 탭 읽기 전용 → **예전 채팅 카드의 「업무나 자료 첨부」 입구가 두 kind 에서 사라짐** ② 채팅 카드엔 만든 지 며칠 없음 ③ 결재자 후보가 편집 계약 options 를 안 씀 ④ 채팅 거절은 옛 경로

## 3. 볼 것
1. **계약 충실도** — 와이어프레임·SPEC-002 §2.9 의 항목 하나하나(파일:줄): 4칸 바 · 호버 화살표 · 스와이프/키보드 · 빈 페이지 · 등록/거절/수정 · 등록 뒤 접힘 · 갈래 고정 · 모달 제출 = confirm+draft(새 업무를 따로 만들지 않음) · 닫으면 버림 · 칩 0건·자리·켰을 때만·수신함 미혼입 · 홈 카드 클릭
2. **회귀** — 워커 미결 ①(자료 첨부 입구 소실)이 기존 기능 회귀인지, SPEC·WP 와 맞는지. ③ 결재자 선택값이 안 보이는 경우가 실제로 생기는지. `CreateWorkModal` 의 일반 「새 업무 추가」 5곳 동작 불변인지(Phase 1 B-02 동작 포함)
3. **P-1** — 수정 창의 필수·검증이 새 업무 추가와 같은가, 초안 values 위에 덮는 draft 가 필드를 잃거나 더하지 않는가
4. Phase 2 규칙(기억한 envelope 로 명령 안 엶) · envelope 권한 판단 · api.ts 밖 fetch 0
5. 조용히 통과하는 자리 · P-2(토큰만, 새 모양은 DS-gaps)
6. **사용자가 실물에서 만날 자리** — 코디 화면 확인 + 사용자 E2E 목록 후보

## 4. 판정
FAIL · WARN · PASS. 파일:줄 + 근거. 테스트 직렬만, 서버·브라우저 금지.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p3b-report.md` 하나만

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-008 Phase 3b 코드 검수 <PASS|WARN|FAIL>" \
  --body "판정 / FAIL·WARN(파일:줄) / 미결 ①~④ 의견 / 화면·E2E 목록 / 리포트 경로"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] reviewer 완료 — Phase 3b 코드 검수 <판정>. 리포트 review-fe-p3b-report.md" --enter
```
