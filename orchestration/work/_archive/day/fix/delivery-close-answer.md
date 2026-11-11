# 코디 답 — Delivery 마감 방법 (2026-11-11)

질문: `spec-sync` 가 제품 레포 Delivery 에서 돌지 않아(mediness#749 · OPEN) 도구로 닫을 수 없다 — A · B · C · D 중?

## 답: (A) 로 끝까지 가고, 마지막에 (D) 로 닫는다

근거:
- 사용자 지시가 명시적이다: 「스테이블에 올리고 **다 닫자**」 · 「이제 다 한 거잖아. 검증은 다음에 하자니까. **닫는 데 문제가 있어?**」.
- 막는 것은 도구의 알려진 결함(#749)이지, 닫으면 안 된다는 규칙이 아니다. 금지된 우회(`--github-repo mediness`)는 **하지 않는다.**
- 전례: 1차 Delivery CENTURION_DAY#224 ~ #227 은 라벨이 `spec-baseline:pending` 인 채 **CLOSED** 다(도구 밖에서 닫았다).

## 할 것 — Delivery 마다 (#241 → #234 → #236 → #239 → #235)

1. scope delta(실물 검증 항목 빼기) → 재결속 → 승인 → **review-delivery 기록까지** — 브리프 그대로. #241 은 이미 됨.
2. per_spec 이 `update-required` 인 SPEC 이 있으면 **문서 sync 변경을 PR 로 연다** — 도구가 못 하므로 스펙 워크트리에서 네가 문서를 고치고(낡은 「구현 전 · 서버 없음 · 다음 WP」 문장을 지금 사실로 · `30-work.md` Delivery 대시보드), **커밋 · push · PR 은 하지 말고** 코디에게 알린다:
   `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[sync 준비] planner: Delivery #<번호> 문서 sync 변경 준비됨 — 커밋·PR 요청" --enter`
   코디가 커밋 · PR · 스쿼시 머지하고 `[머지됨] #<PR> <sha>` 를 보낸다. **여러 Delivery 의 sync 변경을 한 PR 로 묶어도 된다**(도구의 「Delivery 당 하나」는 도구가 못 도는 지금 지킬 수 없다 — 묶었으면 PR 본문에 Delivery 번호를 전부 적는다). 묶는 쪽이 빠르면 **다섯 건의 review 를 먼저 다 끝내고 sync 변경을 한 번에** 준비하라.
3. **닫기** — sync PR 이 머지된 뒤(또는 `update-required` 가 없으면 바로) Delivery Issue 에 **마감 댓글**을 달고 `gh issue close <번호> -R MediSolveAIDev/CENTURION_DAY --reason completed` 로 닫는다. 댓글에 적을 것:
   - 코드 PR · 머지 SHA · 스펙 baseline revision · contract_version · plan_digest(승인) · review-delivery 결과(`conformant`)
   - 문서 sync PR(있으면) · 머지 SHA
   - **다음 작업의 검증으로 넘긴 수용 항목**(뺀 것 그대로)
   - 「`spec-sync` · `complete-delivery` 는 도구 제약(mediness#749)으로 실행하지 못해 Issue 를 직접 닫는다 — 사용자 2026-11-11 결정」 한 줄
   라벨은 도구가 붙인 그대로 둔다(손으로 바꾸지 않는다).
4. 막히는 Delivery(범위 · 근거 판단이 갈리는 것 — 특히 #235)는 **닫지 말고** 그 건만 보고하고 다음으로 넘어간다. 근거 없는 `pass` 금지는 그대로다.

끝나면 브리프의 완료 보고(두 명령).
