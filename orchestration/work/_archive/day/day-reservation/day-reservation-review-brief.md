
# [reviewer] DAY 예약 현황 코드 검수 — Delivery #267 · #268 · #269 (미커밋 변경)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 워크트리의 **미커밋 변경## 1. SSOT — 먼저 읽을 것

- Delivery Issue 본문(계약 · Acceptance): `gh issue view 267 -R MediSolveAIDev/CENTURION_DAY` · 268 · 269
- 계약 보충: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/contract-v1-addendum.md`(V1 에 today · open_min · axis.time_gray_spans[] · 판정 = backend) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-3-report.md`(계약 S · T · V0 ~ V4 최종 문장)
- SPEC `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/20-spec/spec-006-reservation-board.md` (조건 C1 ~ C3 · 케이스 매트릭스) · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`(R1 ~ R41) · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html`
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/be-1-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/fe-1-report.md`
- 레포 규칙: 워크트리 루트 `AGENTS.md`

**기대는 개념**: 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY 예약 현황 조회 — ① #267 조회 라우트 · view model · 권한 키 · 최신화 task 넣기 ② #268 다른 날짜 최신화(`services/emr_date_sync.py` · `tasks/emr.py` 새 task · `emr_sync.py` 더하기) ③ #269 화면(템플릿 · day.js · CSS). 코디가 `tests/day/emr` + 예약 테스트 350 passed · 화면 테스트 12 passed 를 다시 돌려 확인했다 — 테스트가 초록인 것은 안다. **계약 · 조건이 실제로 지켜지는지 · 조용히 통과하는 자리**를 본다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음(검수).

## 4. 먼저 읽을 핵심 파일

`git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation status` · `git diff` + 새 파일(`??`) 전부.

제공)

<BE↔FE 계약이 있으면 필드명·shape·에러코드까지 명시. 없으면 "해당 없음".>

## 4. 먼저 읽을 핵심 파일

- `<파일:줄>` — <왜 봐야## 6. 구현 단계

1. 각 Delivery Acceptance 를 코드 · 테스트에 대조(행별 PASS/FAIL)
2. **#268 조건** — C1(일정 · 키 보충 · 구매 · 시술권 · 카드가 한 transaction · 중간 상태를 다른 읽기가 못 봄) · C2(오늘 10초 회차 잠금 때문에 건너뛰지 않음 · 실패면 이전 사본) · C3(구매 회차 「오늘」 가정 · 발행 순서 키에 버려지지 않음) · R40(같은 (병원, 날짜) 한 번 · 주기 없음) — 테스트가 그걸 **진짜로** 잡는가(가짜 · 우회로 통과하지 않는가)
3. **오늘 회차 회귀** — `emr_sync.py` · `tasks/emr.py` 의 변경이 오늘 10초 회차 동작을 바꾸지 않았는가
4. 계약 S(poll=1 이면 task 안 넣음 · 날짜 바꾸기만 넣음 · 오늘은 안 넣음) · T(task 이름 · 인자) · V0 ~ V4 + 보충 — backend 와 템플릿이 같은 이름을 쓰는가
5. R39(화면 요청 경로에서 KOS 호출 0) · 권한(reservation view · 403) · AGENTS.md 계층(repository 층 없음 · queries/) · 화면: 시안에 없는 문구 · 인라인 스크립트 · 손 CSS
6. 「직원이 실물에서 만날 자리」를 따로 모은다(2루프 재료) — be 리포트의 「해석 5곳」 · KOS 호출량 · 권한 행 지연 포함
7. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-code-1-report.md` — FAIL / WARN / PASS + 파일:줄 + 근거(Issue Acceptance · SPEC 절 · R 번호)

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 금지(리포트 1개만)
- 계약 · 결정 자체를 다시 논의하지 않는다
- 테스트를 돌려도 되지만 사용자 포트 · 프로세스 · 공유 DB 금지

d-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 구현 단계

1. <…>

## 7. 범위 제약 — 하지 말 것

- <…>

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
  --to term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --from term_096158dd-fa56-4eed-b30b-56b5c89f4097 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_28a8c525-c408-4f25-a0f2-ffd6c29fb56d --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
