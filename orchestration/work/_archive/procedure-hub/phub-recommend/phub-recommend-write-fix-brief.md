# [writer] SPEC-001 · WORK-001 수정 — 문서 검수 FAIL 7 · WARN 반영

너는 직전에 SPEC-001 · WORK-001 을 쓴 **procedure-hub `writer` 워커**다. 역할 문서는 그대로다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` (코디 워크트리 공유)

## 1. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-001-report.md` ← 검수 결과. FAIL 7 · WARN 8 · §5 · §7
- 수정 대상: 같은 폴더 `SPEC-001.md` · `WORK-001.md`
- 기준: 같은 폴더 `DEC-001.md` — **DEC 는 바꾸지 않는다**

## 2. 할 일

1. **FAIL 7건을 전부 닫는다.** 원칙:
   - **F1** 실측 106 · 7 을 만든 세 규칙(제품으로 풀린 끝점 → `*_category` 시술군으로 되돌림 · 자기쌍 제거 · `sequence_order` 는 양 끝이 시술군인 쌍에만)을 SPEC §3.3 · §3.3.1 에 **명시**한다. 제품끼리 같은 이름일 때 고르는 규칙도 적는다. 규칙을 적은 뒤 기대값이 그 규칙에서 나오는지 다시 센다
   - **F2** `coverage_gap` 정의와 기대값을 하나로 맞춘다(정의를 고치든 기대값을 고치든, 고른 쪽과 이유를 적는다)
   - **F3** `treats` 엣지 단위(원천 행마다 vs 쌍마다)와 `edge_id` 원천 키를 정한다. D-04 · D-13e(원천 보존 · 합치지 않음)에 맞는 쪽으로
   - **F4** `products.energy_device.category_id` 배열을 처리하는 규칙
   - **F5** CC → 고민 항목 동률 4건의 결정론 타이브레이크(검수가 제시한 `cc_group = label` 을 검토). 못 가르면 엣지를 만들지 않고 검증 리포트로
   - **F6** 부분 그래프 방향(정방향 / 양방향 · 엣지 타입별)과 크기 제한(truncated 규칙)을 정하고 S-1 기대값을 그 규칙으로 다시 적는다
   - **F7** WORK:98 과 경계 테스트(WORK:153 · SPEC:435) 허용 목록을 일치시킨다
2. **WARN** — 구현 · E2E 에 영향 있는 것은 반영한다(특히 S-4 「엣지 1개」 실측 17 · S-7 재적재는 `--from-dir` 로 stg 2회 호출 회피 · 응답 크기). 반영하지 않은 WARN 은 SPEC 「열린 것」에 이유와 함께
3. 리포트 §7 「사용자가 실물에서 만날 자리」(응답 수 MB · 같은 이름 제품 57쌍 · 이소트레티노인이 시술 항목)를 SPEC E2E 절에 **알려진 이상**으로 적는다
4. 문서 맨 위 변경 이력에 「검수 반영 — F1~F7」 한 줄

## 3. allowed_paths

- `SPEC-001.md` · `WORK-001.md` 수정만. 리포트 · DEC · _RESUME · 코드 금지

## 4. 검증

수정한 기대값은 stg 응답(필요하면 엔드포인트당 1회 GET)에 바뀐 규칙을 적용해 다시 센 숫자여야 한다. 셈 방법을 한 줄씩. 키 · 토큰 · 실명 · stg 주소 0(grep).

## 5. 완료 보고 — 문구 변경 금지

- 커밋 · push 하지 마라. 끝나면 아래 두 명령을 모두 실행한다.

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: SPEC 검수 반영" \
  --body "F1~F7 처리 / WARN 반영·미반영 / 다시 센 기대값 / 미결"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — SPEC 검수 반영. 상세는 인박스." --enter
```
