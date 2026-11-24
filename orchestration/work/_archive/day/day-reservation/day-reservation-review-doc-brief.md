
# [reviewer_doc] DAY-SPEC-006 예약 현황(조회 · 웹) 1차 검수

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 워크트리에는 planner 가 남긴 **미커밋 변경**이 있다 — 그게 검수 대상이다. 파일을 고치지 마라(stash · checkout · reset 금지).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` ← **사용자 결정 R1 ~ R16 · 열린 것 O1 · O2. 대조 기준.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` ← 시안(생김새 · 문구 정본 · 3MB 한 파일 — grep 으로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md` ← planner 가 받은 브리프(범위 · 금지 목록)

**기대는 개념**

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/para/areas/concept/cs/read-side-effect.md` — 조회 경로에 부작용(KOS 호출 · DB 쓰기)이 없어야 한다

## 2. 배경 / 무엇을 바꾸나

planner 가 새 SPEC `products/day/20-spec/spec-006-reservation-board.md`(draft)를 쓰고 `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md` 를 고쳤다(`git -C /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec status` · `git diff`). 사용자 리뷰 전에 이것을 결정 · 시안 · 코드 실물에 대조해 판정한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음.

## 4. 먼저 읽을 핵심 파일

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-006-reservation-board.md` — 검수 대상 본문
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-002-procedure-board.md` · `spec-000-data-model.md` — 형식 본 · 칸 계약. SPEC-006 이 이들과 어긋나는지
- DAY 코드 실물(read-only): `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` — `backend/day/models/room.py` · `visit.py` · `customer.py` · `purchase.py` · `notification.py` · `enums/visit.py` · `services/emr_sync.py`(동기화 범위 — today_window) · `emr/kos/mapper.py`
- cc 참고(read-only): `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/service/reservations.py` 등

## 5. allowed_paths — 이 밖은 건드리지 마라

- (read-only — 리포 파일 수정·생성 금지. 산출물은 리뷰 리포트 파일 1개뿐: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-1-report.md`)

## 6. 구현 단계

1. 결정 R1 ~ R16 이 SPEC 에 빠짐없이 · 뒤집히지 않고 반영됐는지 행마다 대조한다
2. O1 · O2 · R12 를 「시안으로 닫음」이라 했다 — 인용한 시안 줄(L1492 · L1498 · L1502 · L1571 · L1661 · L1664 등)을 직접 열어 맞는지 확인한다
3. SPEC 이 말하는 DAY 칸 · 동기화 원천(파일:줄)을 코드 실물로 확인한다 — 없는 칸 · 없는 동기화를 있다고 쓴 곳, 반대로 있는데 없다고 쓴 곳
4. **범위 누락 · 범위 초과**: 조회만 · 상세 모달 · 예약 요청 내용 · 근무표 · 앱 보내기가 범위에 새어 들어왔는지 / 시안에 있는 조회 요소가 표에서 빠졌는지
5. **지어낸 것**: 시안에 없는 화면 문구 · 근거 없는 정책 · 결정 없이 「정함」으로 적은 것(OQ 여야 할 것)
6. OQ 목록(OQ-R01 ~ R16) — 각 OQ 의 「기본안」이 결정처럼 본문에 섞여 들어가지 않았는지. 특히 OQ-R02(동기화가 오늘만 → 날짜 이동 범위) · OQ-R15(수납 필요 원천이 SPEC-002 와 다름)는 사실 근거를 코드로 확인한다
7. 「조용히 통과하는 자리」 — 빈 데이터(데모 지점 공지 없음 · 그룹 없는 방문 · 구역 0) 에서 화면이 어떻게 보이는지 SPEC 이 답하는가
8. 판정 FAIL / WARN / PASS + 지적마다 파일:줄 + 근거(R 번호 · 시안 줄 · 코드 ref)로 리포트를 쓴다

## 7. 범위 제약 — 하지 말 것

- 리포 파일을 고치지 않는다 — 고칠 내용은 리포트에 「고칠 것」으로만
- 결정 R1 ~ R16 자체를 다시 논의하지 않는다(결정이 SPEC 에 잘못 옮겨진 것만 지적)
- 범위 밖 기능을 넣자는 제안을 FAIL 로 두지 않는다

## 8. 검증

```
SPEC·WORK 를 DEC·baseline 에 대조. lint-pipeline --strict 로 products/day/ ERROR 0. 각 지적에 파일:줄 + 근거. 판정 FAIL/WARN/PASS
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
  --to term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --from term_608f78e2-e84c-40c0-929b-467d1bb5d971 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
