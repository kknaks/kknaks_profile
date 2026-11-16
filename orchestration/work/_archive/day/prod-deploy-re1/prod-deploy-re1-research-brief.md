
# [researcher] 웹 피드백 W3 · W4 · W5 원인 · 판정 조사 (read-only)

너는 **day `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 코디 워크트리다 — 리포트 파일 1개 외 수정 · 생성 금지. 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` 에서 frontend 워커가 작업 중 — **읽기만**.

## 1. SSOT — 먼저 읽을 것

- 사용자 피드백: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/e2e-feedback.md` **W3 · W4 · W5**(사용자 말 그대로 · 코디 메모)
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec/products/day/20-spec/spec-002-procedure-board.md` — :162(방 옮기기 팝오버 「방 이름만」) · U-15 · 규칙 29(복귀 · `cancel-flow-tasks` `reason = CANCEL`) · 규칙 33(취소된 「방 배정」으로 원래 방 판정) · 방 이동 · 점유 이동 규칙 · :211(원장 목록 「비어 있음」 방식)
- 코드(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1` — `backend/day/emr/kos/writes.py`(:22 · :82 · :186 · 「방 배정」 만들기 · `change-tasks-room`) · `backend/day/emr/sync.py`(:1318 `is_room_assign` · `card_room_of`) · 방 이동 · 복귀 서비스 · 방 팝오버 템플릿
- KOS 실물(사용자 HAR · 값 출력 금지): `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/reference/2026-11-06-repo-structure/har/시술삭제.har` — **사용자: 「삭제라고」** = KOS 웹 시술 삭제. 코디가 본 것: `change-tasks-complete`(`complete: false`) → `cancel-flow-tasks`(`reason: "DELETE"`). 다른 HAR 도 같은 폴더.

기대는 개념: 해당 없음.

## 2. 배경

사용자 2026-11-11 웹 피드백. 수정 발주 전에 원인 · 판정 기준을 사실로 모은다. **결정하지 않는다** — 고칠 방향 후보와 「정할 것」만.

## 3. 계약

해당 없음.

## 4. 먼저 읽을 핵심 파일

위 §1.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 브리프가 지정한 리포트 파일 1개만 생성)`

## 6. 구현 단계 (질문)

**W3 방 옮기기 목록 — 「비어 있음」 / 「이미 다른 사람이 배정됨」**
1. 지금 팝오버 목록은 어디서 · 무엇으로 만드나(방 목록 원천 · 정렬).
2. 「다른 사람이 배정된 방」으로 볼 수 있는 DAY 값 후보를 전부(판 카드의 `visit.room_id` · 살아 있는 「방 배정」 작업의 방 · 진행중 시술의 방 · 점유 띠 …) — 각 후보가 지금 데이터로 얻어지는지 · 판 화면 기준과 어긋나는 경우(같은 고객의 다른 카드 · 귀가 대기 · 완료 방문).
3. 원장 목록 「비어 있음」(:211 규칙 19) 구현 방식 — 재사용할 수 있나.

**W4 「방 배정」 없는 카드에서 [점유 이동]이 오래 걸림**
4. 그 경로의 KOS 쓰기 순서(「방 배정」 새로 만들기 → 이동 …)와 각 단계가 기다리는 것(outbox · 확인 조회 · 재시도 · 지연 상수).
5. dev 서버 실물: `ssh day-vm` 에서 **읽기만** — `docker logs day-dev-api-1` · worker 로그 · dev DB(`ssh day-db` 터널 · 읽기 쿼리만)의 outbox · event_log 시각으로 최근 [점유 이동] 한 건의 단계별 시간. 값(고객 이름 · 키 · 토큰)은 리포트에 쓰지 않는다 — 시각 · 단계 · 상태만.

**W5 [복귀하기] — 「방 배정」을 취소가 아니라 삭제**
6. HAR 의 삭제 요청 두 개(순서 · 본문 키 · `reason` 값 · `complete` 값)와 응답. DAY 지금 복귀 요청과 차이.
7. 삭제한 「방 배정」 행을 KOS 조회(DAY 가 쓰는 일정 조회)가 돌려주나 — HAR · 코드 · 데모 지점 기존 데이터로 확인 가능한 만큼(쓰기 금지 — 확인 못 하면 「확인 안 됨」).
8. 규칙 33(취소된 「방 배정」 행으로 원래 방 판정)이 삭제로 바뀌면 무엇이 깨지나 · 대신할 기준 후보.
9. 같은 코드 경로를 쓰는 다른 동작([귀가 대기] `cancel-flow-tasks` `CANCEL` · 시작 취소 등)에 번질 위험.

## 7. 범위 제약 — 하지 말 것

- 파일 수정(리포트 외) · 커밋 금지. KOS 쓰기 · DAY 화면 조작 · dev DB 쓰기 금지. 사용자 포트 · 프로세스(로컬 11040 · `day-local`) 금지.
- 고객 값 · 키 · 토큰 · 계정 이메일 출력 금지.

## 8. 검증

```
질문마다 답 + 근거(파일:줄 · git ref · 문서 URL). 확인 못 한 것은 「확인 안 됨」. 결정하지 않고 「정할 것」으로 모은다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/research-1-report.md` — 질문 1 ~ 9 각각 답 + 근거(파일:줄 · 로그 시각 · HAR 항목 번호) · 「확인 안 됨」 · 고칠 방향 후보 · 정할 것.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_271773e9-6e8f-4e4e-8141-cd9bcebd3ac5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
