# 리뷰 리포트 — prod-deploy-re1 / doc 재리뷰 (2026-11-11)

범위는 두 가지만 본다: review-doc-1 의 W1~W6 과 코디 결정 (a)~(f) 가 반영됐는지, 그리고 이번 수정으로 새로 생긴 어긋남. 전체 재리뷰는 아니다.
대상
- mediness 워크트리의 미커밋 diff(spec-000 · deployment.md · log.md)
- v2 request `…/8d8c24d2-…/scratchpad/delivery/prod.v2.request.json`(apply 안 함)
- planner 「수정 1」 절

## 판정: WARN

W1~W6 와 (a)~(f) 는 **모두 반영됐다**. FAIL 은 없다. 다만 새 어긋남이 3건 있다. N1 은 결정 (b) 와 문서가 서로 반대로 적힌 경우라, 스펙 PR 과 v2 apply 전에 고치기를 권한다.

검증
- `lint-pipeline.py --strict` 결과는 exit 0 · 0 error · 263 warning 이다. 이 중 `products/day` 에 걸린 것은 0건이다. 나머지는 다른 제품에 원래 있던 것이라 이번 변경과 무관하다.
- diff 에서 이메일 모양 문자열은 0건이다.

## 반영 확인

| 항목 | 결과 | 위치 |
|---|---|---|
| W1 KOS IP | 닫힘 | deployment.md:254(필요 · 403 `IPBlocked`) · :220 절차 5-1 · :222 절차 7 · v2 `predeploy[1]` · `open_questions` 비움 · A6 「IP 허용 뒤」 |
| W2 prod 브랜치 | 닫힘 | deployment.md:218 · 레포 docs 수정은 v2 `code_surface[5]` 와 `review_surface[3]` 으로 코드 PR 에 넘김 |
| W3 Environment prod | 닫힘 | deployment.md:238 · :224 · v2 L3 근거(`review_surface[1]`) |
| W4 baseline | 닫힘(v2 에서) | v2 `contract_version 2` · `spec_baseline_revision` 자리표시 · `review_surface[0]` 에 「v1 승인 안 함」. Issue #243 본문은 아직 v1 이다. v2 apply 때 바뀌므로 그 전에는 v1 plan_digest 를 승인하지 않는다 |
| W5 Non-Goal 문구 | 닫힘 | v2 `non_goals[5]` |
| W6 ADMIN 칸 | 닫힘 | deployment.md:162 |
| (a) 거절 | 반영 | spec-000:31 · :1384 · v2 A2b · verification[2] |
| (b) 실행 = 코디 | **일부만** | spec-000:31 · :1384 · 절차 6 「누가」 · v2 A6 은 반영됨. 남은 곳은 N1 |
| (c) 가드 없음 | 반영 | spec-000:1384 · 절차 6 「prod api 컨테이너에서만」 · v2 `non_goals[6]`. 근거 표기는 N2 |
| (d) `DAY_SEED_*` 안 씀 | 반영 | spec-000:1384 · v2 `review_surface[2]` |
| (e) log 종류 | 반영 | log.md:17 `spec-change, arch-change` |
| (f) Soniox | 반영 | deployment.md:170 |

## WARN (새로 생긴 어긋남)

### N1. 「사용자가 1회」가 세 곳에 남아 있다. 결정 (b)(실행 = 코디)와 반대다
- `deployment.md:255`: 닫은 미결 행 「prod api 컨테이너 안에서 사용자가 1회」. 같은 문서 절차 6 의 「누가 = 코디」와 다르다.
- `log.md:17`: 같은 요약 안에 「prod api 컨테이너 안에서 사용자가 1회」와 「실행 = 코디」가 함께 있어 한 줄 안에서 모순된다.
- v2 request `target_delta[0]`: 「prod api 컨테이너 안에서 사용자가 1회 돌린다」. v2 A6 · `review_surface[2]`(코디)와 다르다. apply 하면 Issue 본문에 그대로 들어간다.
- 고칠 것: 세 곳 모두 「사용자가 1회」를 「코디가 1회」로 바꾼다. 「prod api 컨테이너에서만」을 덧붙여도 된다.

### N2. 「환경별 가드 금지」에 붙은 날짜 2026-11-09 가 원문과 맞지 않는다
- 위치: `spec-000:1384`(「사용자 2026-11-09 「환경별 가드 금지」」) · v2 `non_goals[6]`(같은 문구)
- 근거
  - 이 문구는 mediness 어디에도 없다(`grep`). 2026-11-09 사용자 원문은 `spec-000:41` 의 「demo 에서 되는 기능이 prod 에서 왜 안 돼야 하냐 · prod 배포도 안 했는데 코드로 막는 이유가 뭐냐」다.
  - 「환경별 가드 금지」는 코디가 2026-11-11 에 전달한 말이다(재리뷰 요청 (c)).
- 지금 표기는 따옴표 인용과 날짜가 어긋나서, 원문 추적이 끊긴다.
- 고칠 문장: `(dev · APP_ENV 로 막는 가드는 두지 않는다 — 사용자 「환경별 가드 금지」(코디 전달 2026-11-11) · 같은 취지 2026-11-09 개정(:41 · 「환경」 :234))`. v2 `non_goals[6]` 도 같은 방식으로 고친다.

### N3. 절차 5 의 `git push origin <sha>:prod` 는 이제 아무 일도 하지 않는다
- 위치: `deployment.md:219`
- 근거: 수정된 절차 4 에서 이미 같은 SHA 로 prod 를 fast-forward 했다. 그래서 5 에서 같은 push 를 하면 바뀌는 것이 없고, deploy-prod 도 다시 돌지 않는다. 실제 경로는 「deploy-prod Re-run」 하나뿐이다.
- 고칠 문장: `| 5 | **deploy-prod** — 4 의 push 로 멈춘 deploy-prod 실행을 다시 실행(Re-run) · 헬스 · `https://day.medisolveai.com` TLS | 사용자 · 코디 | — |`
- 레포 docs 「첫 배포 절차」 5(`git push origin <sha>:prod`)도 코드 PR 에서 함께 맞춘다(v2 `code_surface[5]` 범위).

## 참고
- 5-1(KOS IP 허용)은 외부 업체 처리라 시간이 걸릴 수 있다. 절차 번호는 5 뒤에 있지만, 요청은 1~3 과 같이 미리 넣어도 된다. 굳이 문서를 고칠 필요는 없다.
