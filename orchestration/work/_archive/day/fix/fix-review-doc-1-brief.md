# [reviewer_doc] fix 스펙 개정 1 · 2판 검수 — 실기기 피드백 + 통역 서버 계약

너는 **day `reviewer_doc` 워커**다. **너는 앞 판의 맥락이 없다.** 작성자가 아니다 — 독립으로 본다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 문서)
- **사용자 원천(무엇을 확정했나)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/e2e-feedback.md` 「버그 기록」 1 ~ 7 · 그림 `e2e-shots/` · 결정 `…/work/fix/_RESUME.md` §2
- 작성자 브리프 · 리포트: `…/work/fix/fix-spec-1-brief.md` · `spec-1-report.md` · `fix-spec-2-brief.md` · `spec-2-report.md`
- 통역 근거: `…/work/fix/research-interpret-report.md`
- 코드(읽기 전용 · 스펙이 말하는 「지금 구현」이 맞는지): `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix`

검수 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec` 의 **미커밋 변경 전부**(`git diff` — `products/day/` 8개 문서). read-only.

## 볼 것

1. **사용자 확정과 같은가.** 피드백 1 ~ 7 과 `_RESUME.md` §2 의 결정이 스펙에 그대로 들어갔는지 한 줄씩 대조한다. 사용자가 말하지 않은 것이 **확정처럼** 적힌 곳 · 사용자 말이 바뀌어 적힌 곳을 찾는다. 코디가 기본값으로 닫은 것(1판 OQ-A37 · A38 · C11 · C12 · 2판 OQ-A39 ~ A42)이 「기본값 · 뒤집을 수 있음」으로 구별돼 있는지.
2. **지어 넣은 화면 문구 0.** 새로 들어간 화면 글자를 **전부 세어 표로** 내고, 각각의 출처(사용자 말 · 기존 스펙 줄 · 원천 코드 줄)를 확인한다. 출처 없는 글자는 FAIL.
3. **문서 안 · 문서 사이 모순.** 같은 사실이 본문 · 케이스 매트릭스 · 수용 항목 · OQ · 「프로토와 다른 곳」 · 다른 SPEC · 배포 문서에서 서로 다른 말을 하지 않는지. 고친 절과 **안 고쳐진 옛 문장**이 같이 남은 자리를 grep 으로 찾는다(예: 「테두리 빨강」 · 「4상태」 · 「바꾸기 없음」 · 「원장 호출 하나」 · 「서버 내부는 구현 몫」).
4. **통역 계약 ↔ 앱 실제 코드.** 스펙 §3 「통역」의 프레임 · 필드 · 언어 코드 · 닫힘 · 오류 처리를 앱 `app/lib/interpret/` 코드와 **직접** 대조한다(조사 리포트 표를 믿지 말고 코드를 본다). 「앱 무수정」이 참인지 — 특히 새 오류 `session_limit` 을 앱이 실제로 어떻게 그리는지, 상한에 찼을 때 직원이 보는 화면이 무엇인지.
5. **서버가 이 스펙만으로 지을 수 있는가.** 인증 순서 · 상한을 세는 자리와 돌려주는 자리(오류 · 끊김 · 취소 전부) · 키 없음 · 깨진 시드 · 배포(선택 비밀 이름 · env 이름)에서 구현자가 물어야만 하는 구멍. DAY `AGENTS.md` 규칙(계층 · `day.public` 경계 · 동시성 상한 명시 · 루프 막지 않기)과 부딪히는 문장.
6. **수용 항목이 시험이 되는가.** 새 A- · C-A · N-A 항목이 통과 · 실패를 가를 수 있게 적혔는지. 실물 확인(A-45 ~ A-47)의 누구 몫 표시. 조용히 통과하는 자리.
7. **채팅 · 알림 규칙의 빈 곳.** 그룹 이름: 나간 멤버 · 동시 변경 · 1:1 · 빈 값 · 푸시 제목. 「채팅」 전체 알림: 방별 설정과의 겹침 4조합 · 앱 안 배너 · 받는 종류 조건 · 시스템 계정. 채팅 403 안내의 진입 · 해제. 서버 코드(`services/chat.py` · `chat_push.py` · `notifications.py`)가 지금 하는 것과 스펙의 「이미 있음 / migration 없음」 주장이 맞는지.
8. **배포 문서.** Unlisted · 두 앱 · 지금 상태가 사실과 같은지(`orchestration/config/projects/day.json` `apple` · `_RESUME.md`). 값(Key ID · Team ID · IP · Vault 이름 · 리소스 ID)이 문서에 없는지.

## 돌려 볼 것

```
python3 scripts/lint-pipeline.py --strict     # products/day/ ERROR 0
```

## 하지 말 것

- 파일 수정 금지(리포트 1개만). 커밋 · push 금지. Soniox · KOS · 서버 호출 금지. 사용자 포트 · 프로세스 금지.
- 사용자가 확정한 내용 자체의 옳고 그름은 판정하지 않는다 — 스펙이 그것을 **정확히** 담았는지만 본다. 다만 확정끼리 서로 부딪히면 그건 지적한다.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-doc-1-report.md`
— 판정 **FAIL / WARN / PASS** · 지적마다 `문서:줄` + 근거(사용자 원천 줄 · 코드 `파일:줄`) + 무엇으로 고치면 되는지 한 줄 · 「새 화면 글자 표」 · 「조용히 통과하는 자리」 절 · lint 수치.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_fe17c0ae-13ad-4046-abb8-f9e9280f8932 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer_doc 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(문서:줄) / lint"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer_doc 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] reviewer_doc: <질문>" --enter`
