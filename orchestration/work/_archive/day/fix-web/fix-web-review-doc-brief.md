
# [reviewer_doc] fix-web 스펙 개정 ⑳ · ⑬ 리뷰

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ planner 가 쓴 미추적/미커밋 변경을 읽기만 한다.

## 1. SSOT — 먼저 읽을 것

### 사용자 결정 — 최종 작업 목록(2026-11-12 · 이 표가 정본)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/e2e-feedback.md`(W1~W11 · 보충 · 결정 A) · 조사 `research-1-report.md`(같은 폴더 · 파일:줄 근거).

**백엔드**
- **W5** 확인 필요 상황 = **대기(wait) · 마취 초과(anes) · 호출 안 옴(call) · 귀가 대기 필요(home) 4가지**. **수락 뒤 미시작(accept)은 서버에서 뺀다**(결정 A — `needs()` 에서 제거 · `_accepted_unstarted` · `accept_min` · `limits.acceptMin` · env `BOARD_ACCEPT_MIN` · 관련 테스트 정리). `inbox_section` · `urgency` 는 **앱이 쓰므로 그대로**(값 이름 `need`/`startable`/`waiting` 유지). 앱 코드 수정 · 새 빌드 없음 — 앱 화면에서도 accept 가 안 보이게 되는 것은 사용자 확인.

**웹 — 왼쪽 사이드바(받은함)**
- **W2** 탭 「호출 n」 → 「수락 대기 n」 (n = 수락 안 된 호출 수 · 지금 그대로)
- **W3** 탭 「현황」 → 「확인 필요 n」 (n = 목록에 보이는 확인 필요 카드 수 = 상황 수)
- **W6** 확인 필요 탭: **아코디언 없이 확인 필요 카드만**. 시작 가능 · 시술 대기 목록 삭제(웹 전용 `rules.inbox()` 의 startable·waiting 계산 · `inbox_card` 매크로 삭제)
- **W7** 수락 대기 탭: **아코디언 없이 수락 대기 카드만**. 수락함 목록 삭제(API `calls[]` 는 앱이 쓰므로 그대로)
- **W4** **확인 필요 카드(need_card)만** 구조 변경: 머리 = 「룸 이름 · 상태 · 경과」 / 다음 줄 = 사람 이름 / 그 아래 줄 = 버튼(지금 버튼 칸 위치). 상태 글자 = 대기 · 마취 · 호출 · 귀가대기. 경과 형식은 지금 그대로(분).
- **W10** 확인 필요 카드의 [귀가 대기] 버튼 삭제 → 확인 필요 카드 버튼은 호출 상황의 [재호출] 하나뿐
- **W11** 수락 대기 카드(call_card)는 **구조 그대로**, [재호출] 버튼만 삭제 → 버튼 [수락] 하나
- **W9** 탭 변경 · 카드 밖 클릭(문서 어디든) 시 카드 선택 포커스 해제. 팝오버 · 창(dialog) 안 클릭은 해제하지 않음. 다시 그릴 때 선택 복원(`day.js` :437/:472)과 충돌 금지

**웹 — 오른쪽 방 카드**
- **W1** 오더 메모(`.day-memo__box`) 글자 10px → 12px · 접힘 높이(`--day-memo-max-h`)도 같이 늘려 5줄 유지 · `static/day.css` 재빌드
- **W8** 시술 줄 [수락] 버튼 삭제(수락은 사이드바에서만 · 팝오버 · 엔드포인트 · 권한은 그대로)

**그대로 둠**: 앱 · 「시술 완료 n」 탭 · 방 카드 [귀가 대기] · 엔드포인트 · 권한 · migration 없음.

- 리뷰 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/fix-web-spec` 미커밋 4파일(`git diff`) — `products/day/20-spec/spec-002-procedure-board.md`(개정 ⑳) · `spec-003-mobile-app.md`(개정 ⑬) · `20-spec.md` · `log.md`
- planner 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/spec-report.md` · Delivery Issue #249(`gh issue view 249 -R MediSolveAIDev/CENTURION_DAY`)
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/research-1-report.md` · backend 결과 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/be-1-report.md`(계약 사실)

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

사용자 결정 표(W1~W11 · 결정 A)를 스펙이 빠짐 · 넘침 없이 담았는지 검토한다.

## 3. 계약

backend 실제 계약: `needs[].why` ∈ {wait, anes, call, home} · `doctorName` 칸 삭제 · `limits` = {waitMin, anesMin, callMin} · `inbox.section`/`urgency`/`calls[]` 그대로 · 웹 `inbox` = need 만.

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정·생성 금지. 산출물은 브리프가 지정한 리뷰 리포트 파일 1개뿐)`

## 6. 구현 단계 (검토 항목)

1. 결정 표 W1~W11 · 결정 A 하나하나가 스펙에 있는가(절 · 줄) — 빠짐.
2. 결정 표에 없는 정책 · 화면 문구가 들어갔는가 — 넘침(사용자 말 아닌 글자 · 추측 규칙).
3. 옛 문구 잔재 — `수락 뒤 미시작` · `acceptMin` · `doctorName` · `시작 가능` · `시술 대기`(웹 인박스 칸 뜻) · `수락함` · `호출 탭` · `현황` 탭 · 방 카드 줄 [수락] · 사이드바 [귀가 대기] 를 products/day/ 전체에서 grep — 취소선/기록 문맥이 아닌 살아 있는 문장이 남았는지.
4. 앱 쪽 서술(spec-003)이 「앱 무수정 · 칩 4개 그대로 · inbox.section 유지」와 맞는가, backend 계약(§3)과 맞는가.
5. OQ-56 · OQ-57 이 열린 것으로 정직하게 적혔는가.
6. `python3 scripts/lint-pipeline.py --strict` — products/day/ ERROR 0.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지(리포트 1개만). 커밋 · push · Issue 수정 · 승인 금지.

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web/orchestration/work/fix-web/review-doc-1-report.md` (판정 FAIL/WARN/PASS · 지적마다 파일:줄 + 근거)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b1db5638-c143-4f48-b35e-4550ff2d45d4 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
