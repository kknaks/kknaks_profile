
# [reviewer] 리뷰 — KOS 데모 지점 테스트 데이터 스크립트(seed_demo_board.py)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

backend 워커는 끝났다(커밋 전 · 워크트리에 미추적 파일로 있음). 너는 읽기만 한다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-be-brief.md` ← 계약의 SoT(§2 · §3 · §6 · §7). 스펙 문서는 없다(개발 도구).
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-09-cc-day/har/고객예약접수시술.har` — KOS 웹 HAR(데모 지점 · 내부 API). 쓰기 요청 순서 · 본문 모양의 원천. 고객 값은 보지도 옮기지도 마라
- 레포 루트 `AGENTS.md`

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

backend 워커가 KOS **데모 지점**에 「30분 한 타임 · 국적별 1명 · 시술 대기까지 · 오더 메모 · 시술 아무거나」 테스트 데이터를 넣는 스크립트를 만들었다. 실물: 14:30 칸 10명 전부 PROCEDURE_WAITING(워커 보고). 이 스크립트가 브리프대로인지, 그리고 **잘못 돌렸을 때 실제 병원 · 실제 사람에게 닿는 자리가 없는지**를 본다.

워커 보고의 주의점(확인 대상): ① 재시도 버그(exc.args → exc.status) 고친 뒤 처음부터 끝까지 한 번에 다시 돌려 보지는 않았다 ② 국적은 meta/codes 에 없어 ISO alpha-2 ③ 전화 · 이메일 안 보냄 ④ 방은 기타 작업(seq 1)에만 ⑤ 시술 대기 전환은 HAR 에 없어 writes.py 와 같은 내부 경로 ⑥ 수납은 CASH.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 사용법은 be 브리프 §3(`--slot` · `--date` · `--count` · `--dry-run`).

## 4. 먼저 읽을 핵심 파일

- `scripts/seed_demo_board.py` — 대상 전체
- `backend/tests/scripts/test_seed_demo_board.py` · `backend/tests/scripts/__init__.py`
- `backend/day/emr/kos/client.py` · `writes.py` — 재사용이 맞는지 · 같은 경로인지

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-seed-demo-board-report.md`

## 6. 구현 단계

1. be 브리프 §3 · §6 · §7 을 항목마다 코드와 대조(지킴 / 어김 / 확인 못 함)
2. **안전 가드**: 데모 테넌트 가드가 **어떤 KOS 호출보다 먼저** 걸리는지(토큰 교환 포함) · `--dry-run` 이 정말 아무것도 쓰지 않는지 · 명동점 키로 돌면 어디서 멈추나
3. HAR 쓰기 순서 · 본문 모양과 코드 비교(경로 · 필드 · 앞 응답에서 넘겨받는 id). HAR 에 없는 것을 지어낸 자리 표시
4. 실패 처리: 한 명 실패가 다음 사람 · 전체를 망치지 않나 · 반쯤 만든 방문이 어떻게 보고되나 · 재시도가 쓰기 요청을 **두 번 보내** 중복을 만들 자리가 없나(이게 「조용히 통과하는 자리」 1순위)
5. 개인 값 · 키 · 토큰이 출력 · 로그 · 예외 메시지로 새는 자리
6. 테스트가 슬롯 계산(KST · 30분 경계 · 자정 넘김) · 국적 순환 · 가드를 실제로 막는지
7. 실행하지 마라 — KOS 에 쓰는 실행 금지. pytest · ruff 는 돌려도 된다

## 7. 범위 제약 — 하지 말 것

- 코드 수정 금지 · 커밋 금지
- KOS 호출 금지(조회 포함) — 실물 확인이 필요하면 「확인 못 함」으로 적는다
- HAR 원문 · 고객 값을 리포트에 붙이지 않는다

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_b915fb18-742f-4779-962c-79848020b8d5 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
