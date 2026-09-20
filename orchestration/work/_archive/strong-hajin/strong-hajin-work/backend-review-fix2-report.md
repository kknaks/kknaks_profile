# 코드 재검수 잔여 R-1~4 최소 정정 — 결과 보고 (2026-09-16)

## 상태: done · R-1~4 네 건 처리 · 제품 코드 무변경

---

## 0. 검증

```
PYTEST_ADDOPTS="tests/contract/test_task_actor.py tests/contract/test_meeting_finalize.py \
                tests/contract/test_task_creation_contract.py" make test-contract
```

**exit 0 · 84 passed** (`scratchpad/r2-scoped.txt`). 전체 contract·verify 는 돌리지 않았다(브리프 §8).
`git diff --check` clean. allowed_paths 밖 변경 0.

## 변경 파일 (5개, 전부 allowed_paths 안)

| 파일 | 무엇 |
|---|---|
| `README.md` | R-1 — 요청/배정 거절 코드를 갈라 적음 |
| `docs/domain-model.md` | R-1 — 같은 내용 + 소스 심볼 근거 |
| `backend/tests/contract/test_meeting_finalize.py` | R-2 — 승격 actor·history 가드 |
| `backend/tests/contract/test_task_creation_contract.py` | R-3 — 담당 부재 순간의 열람 경계 |
| `backend/tests/contract/test_task_actor.py` | R-4 — 낡은 주석 + 넓은 단언 정정 |

---

## 1. R-1 — 요청/배정의 거절 코드를 갈라 적었다 (문서만)

**먼저 실제 분기를 돌려서 쟀다** (`ax_test` 아닌 임시 SQLite, 제품 무변경):

| 대상 | 호출자 | 실측 |
|---|---|---|
| `assigned` 요청 accept | 담당자 jiho(decide 보유) | **422** `work request is not awaiting a decision` |
| | 제3자 yuna(decide 보유) | **422** `only the requested assignee may decide` — **존재가 샌다** |
| | minseok·mina(decide 없음) | **403** `work_request.decide capability is required` |
| | 없는 식별자 | **404** (`WorkRequestNotFound` → `ResourceNotFound`) |
| `active` 배정 accept | 담당자 mina | **422** `task assignment is not awaiting acceptance` |
| | jiho(보낸 사람)·yuna·minseok | **404** `task assignment was not found` — 존재 은닉 |

소스 대조도 마쳤다: `requests.py:837` 이 평범한 `WorkRequestError` 를 던져 `http.py` 가 422 로 매핑하고,
`assignments.py:208·254·267` 은 `TaskNotFound` → 404 다. `request_errors.py:18` 의 `WorkRequestNotFound` 만
`ResourceNotFound` 를 상속한다.

**고친 문장** (두 자리 모두 같은 취지):

- 이전: 「받는 사람이 걸면 422, **관계 없는 사람에게는 존재 자체를 숨긴다**」 — 배정의 실측을 요청까지 일반화한 거짓.
- 지금: 「**배정**은 담당자에게만 422 이고 **그 밖의 모두에게는 404**(보낸 사람도 마찬가지). **요청**은 존재를
  숨기지 않는다 — 판단 역량이 없으면 403, 있어도 그 요청의 담당자가 아니면 422, 404 는 없는 식별자일 때뿐」.
- `docs/domain-model.md` 에는 소스 심볼(`_pending_target` 의 `TaskNotFound`, `_decision_target` 의
  `WorkRequestError`, `WorkRequestNotFound`)과 함께, **판단 역량을 가진 제3자가 422 로 존재를 얻는 것은
  W1 이전부터의 계약**이고 요청 계열의 404 통일은 별도 결정임을 적었다.
- **요청이 404 로 동작한다고 꾸미지 않았고, 코드의 기존 오류 계약도 건드리지 않았다**(§3 준수).

## 2. R-2 — 회의 승격의 생성 actor·history 가드 (테스트만)

`test_the_promoted_request_carries_the_source_columns_onto_the_task` 에 네 줄을 더했다.

- `task.created_by_actor_id == "mina"` — **누른 사람**이다. 요청자 자리에 앉은 `system:meeting` 도, 받는 사람도 아니다.
- `request["requester_kind"] == "system"` · `promoted_by_member_id == "mina"` — 두 사실이 **동시에** 참임을 한자리에서 고정.
- 진행 기록 첫 회차: `change_kind == "task.created"` · `actor_id == "mina"` — 하지 않은 일이 이력에 남지 않는다.

기존 출처 세 열(`source_meeting_id`·`source_agenda_id`·`origin_kind`) 단언은 그대로 두었다.

## 3. R-3 — 활성 담당이 없는 순간의 열람 경계 (테스트만)

신규 `test_the_read_boundary_holds_in_the_moment_no_one_holds_the_work`.
요청→업무 뒤 담당자 변경을 걸어 **`superseded` + `pending`, active 0** 인 상태를 만들고 그 자리에서 고정한다.

| 누구 | 결과 | 이유(코드) |
|---|---|---|
| 요청자 mina(=부른 사람) | 200 `read_only` | `_related_view` 의 출처 관계 |
| 전 담당자 jiho(넘긴 사람) | 200 `read_only` | `TASK_ASSIGN` + `assigned_by == self` |
| 조직 전체 독자 yuna | 200 `read_only` | `_may_read_beyond_holding` fallback |
| minseok · hyeon | **404** | 관계도 조직 자격도 없음 |
| 셋 다 `POST …/start` | **404** | 읽을 수 있다 ≠ 몰 수 있다 |

`created_by_actor_id == "mina"` 도 함께 단언해 **fallback 이 읽는 값**을 못 박았다.
**한계를 테스트 주석에 적었다**: 데모 조직은 회사가 하나라 조직 범위 교집합이 늘 겹쳐, 이 칼럼이 누구든
`work.read.all` 독자의 답은 같다 — 차이를 가르는 것은 그 자격의 범위이지 이 칼럼이 아니다. 즉 이 테스트는
**관측 가능한 경계**를 고정할 뿐 fallback 의 분기 자체를 가르지는 못한다(재검수 R-3 의 「중립적 변화」 판정과 일치).

## 4. R-4 — 낡은 주석 + 넓은 단언 (테스트만)

`test_only_someone_who_may_assign_can_change_the_holder`:

- 주석 「The assignment is still pending, so nobody holds it yet」 → 「배정은 수락을 기다리지 않으므로
  민아가 이미 들고 있다」로 교정.
- 같은 자리의 `in {403, 404, 422}` 두 줄을 **403 + `"task.assign"` 문구**로 좁혔다 — 실측으로 확인했다
  (담당자 민아도, 무관한 소라도 둘 다 `task.assign capability is required` 403). 넓은 집합은 담당자 변경이
  「역량이 없어서」 막히는 것인지 「못 읽어서」 막히는 것인지를 가리고 있었다.

---

## 5. 제품 회귀 — 발견 없음

검증 중 실제 제품 회귀는 나오지 않았다(84 passed, exit 0). 제품 코드는 한 줄도 바꾸지 않았다.
R-1 이 드러낸 **요청 계열의 존재 누출(제3자 422)** 은 코드 쪽 사안이지만 **W1 이전부터의 계약**이고
브리프 §3 이 변경을 금지했으므로 문서에 사실대로 적고 「404 통일은 별도 결정」으로 남겼다.

## 6. 계약 준수

- 제품 코드·Makefile·자료 worker 타이밍 테스트 **무변경**(§6).
- legacy fixture **확대 없음** — `tests/legacy_acceptance.py` 무수정, 새 테스트 둘 다 신규 POST 경로만 쓴다.
- 공유 트리 stash/checkout/reset **미사용**. 커밋·push·PR 없음. E2E 사용자 담당.
- allowed_paths 다섯 파일만 수정(확인함).

## 7. 인수인계 — 자료 worker 병렬 완화의 한계 (§6)

1차 보고의 계측을 다시 적어 둔다. 실패 기전은 **lease 를 잃은 worker 가 결과를 게시하지 않는 옳은 동작**이고,
깨지는 것은 「3초 안에 한 번은 CPU 를 받는다」는 테스트 전제다(부하에서 박동 호출 하나가 2.62s 블록,
결과 게시가 만료 0.42s 뒤에 실행).

**병렬도를 4로 낮추는 완화는 확률을 줄일 뿐 보장을 만들지 않는다.** 직렬화도 마찬가지다 — 같은 기계에서
도는 **외부 부하**(다른 워커, 빌드, FE 테스트, 브라우저)는 pytest 병렬도와 무관하게 worker 프로세스를
3초 이상 굶길 수 있고, 그 순간 이 두 테스트는 같은 이유로 실패한다. 시간 보장을 원하면 테스트가 쥔
`material_queue_visibility_timeout=3` 예산 자체를 바꾸거나(단언 의미가 바뀐다) 이 두 건을 시간 의존
마커로 분리해 CI 가 격리 실행하는 쪽이라야 한다 — 둘 다 W1 범위 밖의 결정이다.
