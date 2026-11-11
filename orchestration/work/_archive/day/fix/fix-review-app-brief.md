# [reviewer] fix 앱 코드 검수 — WP-APP-1(시술현황 카드 + 후속 2) · WP-APP-2(채팅 · 설정)

너는 **day `reviewer` 워커**다. 앞 판(#240 검수)의 맥락이 있더라도 아래 파일을 기준으로 한다. 작성자가 아니다 — 독립으로 본다.

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 문서)
- 레포 규칙: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md` 「앱」
- **계약의 SoT**(미커밋 스펙 워크트리): `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-003-mobile-app.md`(개정 ⑧ · U-3 · U-4 · U-9 · U-12 · A-28 · A-33 · A-37 · A-41 ~ A-43 · OQ-A37 · A38 · A44) · `spec-004-internal-chat.md`(U-1 채팅 거절 · U-7 · U-8 · C-A19 ~ C-A21 · OQ-C11 ~ C15) · `spec-005-notifications.md`(U-3 · N-A13)
- 작업 계획 · 서버 ↔ 앱 계약 표: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/wp-plan.md` §2 「WP-APP-1」 「WP-APP-2」 · §3
- Delivery: CENTURION_DAY#241(승인됨)
- 사용자가 본 것: `…/work/fix/e2e-feedback.md` 「버그 기록」 1 ~ 4 · 6 · 7 · 그림 `e2e-shots/`
- 작성자 브리프 · 리포트: `…/work/fix/fix-app-code-brief.md` · `app-1-report.md` · `app-2-report.md` · 캡처 `…/work/fix/app-captures/`(12장)
- 서버 쪽 실제 구현(읽기 · 계약 대조용): `backend/day/routers/api/chat.py` · `services/chat.py` · `services/notifications.py` · `services/chat_push.py` — backend 워커가 **지금도 같은 워크트리에서 통역(WP-BE-2)을 짓는 중**이다. `backend/` 는 읽기만 하고, 통역 쪽 미완성 파일은 검수 대상이 아니다.

검수 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix` 의 **`app/` 미커밋 변경 전부**(`git diff -- app` · 29파일).

## 볼 것

1. **사용자 피드백이 실제로 풀렸나.** 1 · 4번(모두 완료 카드가 「시술 대기」로 보이던 것 · [귀가 대기]) · 2번(B안) · 3번(채팅 403) · 6번(그룹 이름) · 7번(「채팅」 스위치) · 후속 2(`version >=` · `calls[].canRecall`)를 코드 경로로 따라가 확인한다. 캡처 12장을 열어 스펙 와이어 · 겹침 표(7자리)와 대조한다.
2. **업무 규칙을 앱이 다시 계산하지 않는가.** [귀가 대기] 노출 = 서버 `canHome` + 판 편집 권한 · 방 상세와 같은 조건 · 같은 잠금 키. 「모두 완료」 계산 · 글자가 방 상세와 한 곳을 쓰는지(복사본이 둘이면 지적). 확인 필요 조건이 서버 `needs[]` 그대로인지.
3. **화면 문구.** 새로 들어간 문자열 상수를 `git diff` 에서 **전부 세고** 스펙 줄과 대조한다. 스펙에 없는 글자는 FAIL.
4. **서버 계약과 같은가.** 앱이 보내고 읽는 것(#22 요청 · 응답 · 오류 코드 · `chat_room` 이벤트 · 설정 `items` 의 `chat` · 없을 때 켜짐)을 `wp-plan.md` §3 표 **와** 서버 실제 코드 둘 다와 필드 단위로 대조한다.
5. **상태 · 경합.** 채팅 403: 스트림 재연결 멈춤 · 다시 보는 때(다시 로그인 · 앱 다시 열 때 · 앞으로 올 때 한 번)·세션이 바뀌었을 때 늦게 온 결과를 버리는지 · 조작 중 403 = 본문 안내만. 그룹 이름: 저장 중 다시 누름 · 실패 뒤 입력 유지 · 다른 사람이 바꾼 이벤트가 편집 중에 올 때. 「채팅」 스위치: 끈 뒤 앞에서 받은 채팅 푸시 배너.
6. **작성자가 「스펙 · 계획과 다른 곳」으로 적은 10건**(app-1 4건 · app-2 6건)을 하나씩 판정한다 — 스펙 안인지 · 사용자에게 물어야 하는지.
7. **시험이 조용히 통과하는 자리.** 새 시험이 실제로 실패할 수 있는지(더블이 답을 그대로 돌려주기만 하는 시험 · 기대값이 구현을 베낀 시험). 수용 항목마다 시험이 있는지.
8. **범위.** `app/lib/` · `app/test/` 밖 변경 · `app/lib/interpret/` 변경 · 의존성 추가가 없는지.

## 돌려 볼 것(각 1회)

```
cd app && fvm flutter analyze
cd app && fvm flutter test
```

## 하지 말 것

- 파일 수정 금지(리포트 1개만). 서명 · 빌드 업로드 · 배포 · 서버 호출 금지. 사용자 로컬 스택(`day-local-*` · 11040 · 11042 · 11043) · backend 워커의 격리 스택(`daybetest-*`) · 시뮬레이터 · 실기기 금지. `git stash` · `checkout` 금지(다른 워커가 같은 워크트리에서 일한다).

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/review-app-report.md`
— 판정 **FAIL / WARN / PASS** · 지적마다 `파일:줄` + 근거(스펙 절 · 서버 코드 줄) + 고칠 방향 한 줄 · 「새 화면 글자 표」 · 「작성자 10건 판정」 · 「조용히 통과하는 자리」 · 돌린 명령 수치.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_4afcc88b-79e9-4f89-82de-783b5f10c7c9 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: <판정 · 한 줄>" \
  --body "판정 / FAIL·WARN 목록(파일:줄) / 수치"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] reviewer 완료 — <판정 · 한 줄>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] reviewer: <질문>" --enter`
