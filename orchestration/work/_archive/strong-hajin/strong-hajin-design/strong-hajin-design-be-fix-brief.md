# [backend] BE 검수 지적 반영 — 누출 둘 · 테스트 구멍 셋 · 수치 정정

같은 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` 에서 이어서 한다.
네가 방금 만든 것을 고치는 판이다. **새로 조사하지 마라.**

## 0. 근거

- 검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/review-be-report.md`
- 판정은 **PASS · FAIL 0 · WARN 10** 이다. 아래 다섯만 고친다. **나머지 WARN 은 코디가 처분했다 — 손대지 마라.**

## 1. 고칠 것 — 다섯

### ① W-5 · 게이트 7 거절 문장이 못 읽는 자손의 제목을 낸다 — **누출**

게이트 6 은 같은 자리에서 제목을 가리는데 게이트 7 은 그대로 낸다.
**게이트 6 과 같은 규칙으로 맞춰라** — 못 읽는 업무의 제목은 문장에 담지 않고 건수로 접는다.

기존 함수에서 상속된 것이지만 **이번 이동 경로가 그 문장에 도달하는 길을 새로 열었다.**
그래서 이번 판에서 닫는다.

### ② W-6 · 못 읽는 프로젝트로 서브트리를 밀어 넣을 수 있다 — **누출**

`project_for(…, parent)` 가 프로젝트 **읽기 가드**를 지나지 않는다.

**이동 경로에만 읽기 가드를 건다.** 생성 경로는 건드리지 마라 — 거기는 이번 판 범위 밖이고
기존 계약·테스트가 그 모양에 걸려 있다. **두 경로가 갈리는 사실을 코드 주석과 리포트에 적어라.**

거절 코드는 기존 프로젝트 읽기 거절과 같은 것을 쓴다. 새 코드를 만들지 마라.

### ③ W-8 · 테스트 구멍 셋

- 후행의 **섞인 갈래**(읽을 수 있는 것 + 못 읽는 것이 함께 있을 때) 미검
- **응답 전용 입력 거절** 미검 (`successors`·`hidden_successor_count` 를 요청 본문에 넣으면 거절되나)
- **약한 단언 1줄** — `backend/tests/contract/test_task_successors.py:177`. 실제 값을 검사하게 고쳐라

### ④ W-1 · 리포트 수치 정정

`make test-unit` 실측은 **389 passed** 다. 네 리포트의 381 과 「8건이 더해진 수」 설명이 사실과 어긋난다.
`be-report.md` §4 를 **실측값으로 고쳐라.** 재측정해서 쓴다.

### ⑤ 인덱스는 코디가 데모 DB 에 적용했다

`ix_task_predecessors_predecessor_task_id` 가 `ax_demo` 에 붙었다. 네가 할 일 없다.
**리포트에 「코디가 적용 완료」로만 기록해라.**

## 2. 손대지 마라 — 코디가 처분한 것

| WARN | 처분 |
|---|---|
| W-2 `inventory.json` allowed_paths 밖 | **인정.** AGENTS.md 와 WORK-007 이 갱신을 명령했다 |
| W-3 `parent_for` 실제 순서가 SPEC 표와 다름 | **SPEC 표를 고친다.** 코드는 그대로. writer 몫 |
| W-4 회차 어긋남 409/422 공존 | **그대로 둔다.** Case Matrix 를 따른 결과다. 문서에 기록만 |
| W-7 AX 확인 카드에 두 칸 자동 개방 | **승인.** 같은 명령 경로라 일관된다 |
| W-10 `parent_task_id`+`project_id` 동시 PATCH 422 | **그대로.** FE 계약으로 넘긴다 |

## 3. 범위 제약

- `frontend/` 금지
- 위 다섯 밖의 것을 고치지 마라
- 알림 구현 금지 (여전히 범위 밖)
- 생성 경로(`parent_for` 의 create 갈래) 건드리지 마라
- 커밋·push·PR 금지

## 4. 검증

```
make test-unit · make test-contract
```

- **사용자 포트·프로세스 무접촉** — `8001`·`5176`·`54329`
- 수치를 **실측 그대로** 보고해라. 추정하지 마라

## 5. 리포트

`be-report.md` 를 **고쳐 쓴다**(새 파일 만들지 마라). 끝에 `## 8. 검수 반영` 절을 더해
다섯 각각 무엇을 어떻게 고쳤는지 `파일:줄` 로 적어라. §4 수치는 실측으로 교체한다.

## 6. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 검수 반영 완료: <한 줄>" \
  --body "다섯 각각 처리 / 변경 파일:줄 / 실측 검증 수치 / 남긴 것"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] backend 검수 반영 완료 — <한 줄>" --enter
```
