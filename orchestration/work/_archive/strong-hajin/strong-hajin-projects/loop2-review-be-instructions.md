# 루프2 BE-3 검수 — 게이트 제거와 체크리스트 읽기 범위가 계약대로인가

**read-only.** 코드·문서 수정 0건. 커밋 금지. **서버·사용자 포트 금지**(사용자 E2E 스택이 떠 있다).
**쓰는 파일 하나**: `orchestration/work/strong-hajin-projects/review-loop2-be-report.md`

## 읽을 것

- 역할: `.../roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- **계약**: `spec-005-projects.md` v0.2.0 — §4 「체크리스트·업무 내용의 읽기 범위」 · 자동 초대 절 · §6 의 **L-01~L-13**
- **계획**: `work-005-projects.md` **Phase BE-3**
- **결정**: `decision-004-projects.md` — **D-28**(게이트 제거, ~~D-12~~ 대체) · **D-29**(읽기 범위) · **D-38**
- **워커 리포트**: `loop2-be-report.md` ← **주장을 믿지 말고 실측하라**
- 1루프: `review-be-report.md` · `be-fix-report.md`(같은 지적이 재발했는지)

검수 대상: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` —
**`git diff` 로 이번 판 변경 전부**를 본다. ⚠ 워크트리에는 **1루프·Phase 0 변경도 함께 쌓여 있다**
(커밋 0건). **이번 판(BE-3)이 만진 6파일만** 검수 대상이다 — 리포트가 그 목록을 준다

## 판정

**FAIL**(계약과 다른 것이 돈다) / **WARN**(모호하다) / **PASS**. **각 지적에 `파일:줄` + 근거.**
**「조용히 통과하는 자리」를 따로 본다** — 개명뿐인 변경 · 빈 단언 · 항상 참인 가드 ·
예외를 삼키는 폴백 · **목만 검사하는 테스트**.

## 반드시 확인할 것

1. **게이트가 «자동 초대에서만» 빠졌나** — `may_assign_in` 참조가 **4자리**였고 자동 초대는 1자리다.
   **나머지 3자리가 그대로인가.** 특히 **「업무를 올리는 문」(`POST /projects/{id}/tasks`)은 여전히
   거절해야 한다**(L-03). 둘 다 빠졌으면 **FAIL**
2. **붙는 kind 가 `member` 인가** — `lead` 로 붙으면 FAIL (읽기만 주는 것이 이 결정의 전제다)
3. **읽기 범위가 ⓑ 방식인가** — **`access` 값을 3분화하지 않고** `checklist` 를 싣는 조건만 따로.
   `access` 를 늘렸으면 FAIL(SPEC 이 그 길을 기각했다). 그 값을 읽는 자리가 함께 움직였는지 grep 으로 확인
4. **쓰기 가드가 한 줄도 안 움직였나** — `POST/PATCH/DELETE /api/tasks/{id}/checklist` ·
   `POST .../checklist/order`. **참여자·리드가 쓰기를 시도하면 거절**되는지 테스트가 실제로 재는가(L-11)
5. **프로젝트 밖에서는 안 오는가**(L-12) — 범위가 새지 않았나
6. **`tasks[]` 가 안 넓어졌나**(D-38) — 프로젝트 상세 응답에 `checklist`·`description` 이 실렸으면 FAIL
7. **다시 쓴 테스트가 새 계약을 «재는가»** — 워커는 「삭제·skip·단언 약화 아님」이라 주장한다.
   **세 자리를 직접 읽고 확인하라**: ① `test_assigning_is_the_whole_condition_…`
   ② 신설 `test_…_taken_back_off_when_they_decline` ③ `test_projects.py` 의 재작성.
   **대비군이 「올리는 문」으로 옮겨진 것이 실제로 게이트를 재는가**
8. **RED 확인이 사실인가** — 「구현 전 3 failed / 4 passed」. 구현을 되돌리는
   **뮤테이션으로 확인하라**(조건 한 줄을 무력화하면 그 테스트가 실제로 빨강이 되는가)
9. **테스트 수치를 네가 다시 재라** — `make test-unit` · `make test-contract`(두 패스) ·
   `make test-postgres`. **이제 기준선은 「실패 0」이다**(Phase 0 닫힘).
   **`-p no:randomly` 금지**(미설치·무동작), 직렬은 `-n0`
10. ⚠ **워커가 든 「첫 회차 병렬 실패 5건, 이후 재현 안 됨」을 따로 보라** —
    `test_reference_read_receipt.py` 등. **Phase 0 의 부류(자식 프로세스 + 실시간 창)인가,
    아니면 이번 변경이 만든 것인가.** `@pytest.mark.serial` 마커가 없는데 자식을 띄우면
    `conftest` 걸개가 즉시 실패시키므로, **걸개가 침묵했다면 그 부류가 아니다** — 그 사실을 확인하고 적어라
11. **범위** — `frontend/` 0줄 · `demo_work.py` 0줄 · 커밋 0건 · `reset-demo` 0회

## 범위 밖 — 지적하지 마라

- FE 몫(L-49~L-52 · L-10 의 FE 절반 · 화면 9건) · 루프3 이월 · 1루프·Phase 0 변경
- SPEC §7 의 미결(OQ-604~607) 자체

## 리포트 형식

판정 한 줄 → 지적마다 `[FAIL-n] / 무엇이 / 파일:줄 / 어느 계약·인수조건과 어긋나나 / 수정안 한 줄`
→ **11항목 각각의 결과** → **테스트 실측 수치** → **§10 의 판정**(그 5건이 무엇인가).

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_d70e6b09-2c7f-4ac1-9be0-74bdd5b5e7be \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 루프2 BE-3 검수" \
  --body "판정(FAIL n·WARN n) / 큰 지적 3개 / 11항목 결과 / 테스트 실측 / 첫 회차 5건의 정체 / git status"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] reviewer 완료 — 루프2 BE 검수. 상세는 인박스." --enter
```
