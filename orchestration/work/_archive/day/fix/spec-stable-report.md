# DAY-SPEC-000 stable + Delivery 마감 계획 확인

## 상태: 1 done · 2 확인만(적용 0)

## 1. DAY-SPEC-000 → `stable`

브랜치 `kknaksss/fix-app-re1-spec-stable`(= `origin/main` `1a450bcf`) · 커밋 · push · PR 0(코디 몫). 근거 = 사용자 2026-11-11 「아 그럼 스테이블에 올리고 다 닫자」.

| 문서:줄 | 바꾼 것 |
|---|---|
| `products/day/20-spec/spec-000-data-model.md:6` | `status: draft` → `stable` |
| `spec-000-data-model.md:31-32` | 머리 한 줄 — 2026-11-11 status stable(사용자 인용 · 내용 · 열린 OQ · 버전 `0.0.1` 그대로 · 상태만) |
| `products/day/20-spec.md:69` | SPEC List 상태 칸 `draft` → `stable` |
| `products/day/10-decision.md:6` · `:27` | `last_updated` 2026-11-11 · 「현재 결론」 「DAY-SPEC-000(draft)」 → 「(stable · 2026-11-11)」 |
| `products/day/log.md:17` | spec-change 1줄 |

- **전례 확인**: DAY-SPEC-001 이 draft → stable 된 #921(`0d69a207`)은 frontmatter `status` 와 `20-spec.md` SPEC List 칸만 바꿨다 — 같은 방식(+ log · 머리 한 줄 · 10-decision 의 「(draft)」 표기). 버전은 규칙상 문서 개정으로 올리지 않는다(`version` = 제품 버전 · document-pipeline §YAML).
- **`last_updated`**: SPEC-000 은 이미 2026-11-11 · `20-spec.md` 「최종 수정」 이미 2026-11-11.
- 「SPEC-000 은 draft」라고 적은 다른 자리: grep(`products/day` 의 20-spec · 40-architecture · README · 10-decision · 30-work) → `10-decision.md:27` 하나뿐(고침). 40-architecture · README · 다른 SPEC 에는 없음.
- **DAY-SPEC-002 는 건드리지 않음**(draft 그대로).
- **막는 규칙: 없음.** lint 는 stable 에 대해 「열린 OQ 수 · 필수 절」을 보지 않는다(stable 관련 검사 = 「draft SPEC 에 work 진행 금지」(5→6)와 cut 때 「draft SPEC 없음」뿐). 다른 stable SPEC(001 · 003 · 004 · 005)도 열린 OQ 를 갖고 있다. harness 도 frontmatter `status == "stable"` 만 본다(`tools/harness/src/mediness_harness/surfaces.py` — `missing = target 중 stable 아닌 것`).
- lint: `python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0.

## 2. 계획 확인 (적용 0)

### #241 — 닫기까지

main 의 다른 target(SPEC-003 · 004 · 005)은 이미 `stable`(`1a450bcf` 에서 확인). SPEC-000 이 stable 로 main 에 들어가면 `missing_target_specs = []` → **baseline ready** 가 된다(harness 판정 규칙). 앞서 v6 `--plan`(`1a450bcf`) 결과 `plan_digest` 가 v5 승인 digest(`sha256:3fb28dfcc23cf85cf8e6804faf752d47e34fa951119b4ed18a32f50eb7d78288`)와 **같았다** — baseline revision 만 바뀌면 재승인 없이 가는 모양.

| # | 단계 | 명령 | 요구하는 것 | 사람 gate |
|---|---|---|---|---|
| 0 | 스펙 PR(SPEC-000 stable) 머지 | — | 위 1 의 변경 | **사람 머지** |
| 1 | 재결속 v6 | `start-delivery` · 같은 key · `contract_version 6` · `spec_baseline_revision = 새 origin/main` → `--plan` → `--apply` | 결과 계약 v5 그대로(보관 request `…/work/fix/delivery/fix.v6.request.json` 의 revision 만 새 SHA 로) · plan_digest 가 v5 승인과 같으면 승인 유지 | 없음(digest 가 달라지면 재승인 receipt 필요 — 그때 멈춤) |
| 2 | review-delivery | `review-delivery` · `code_pr 242` · head `87cf2dec…` · merge `7b099e8f…` · `merged: true` · v6 contract_digest · 새 baseline | ① baseline ready ② 현재 plan_digest 승인 표시 ③ Execution ready ④ 모든 target SPEC 결과 하나씩(`update-required` / `none` / `undetermined`) ⑤ **모든 Acceptance(A1 ~ A14) 결과 하나씩** ⑥ **`conformant` 이면 모든 Acceptance 가 `pass` + 근거** | per_spec `undetermined` 가 있으면 `resolve-spec-impact`(사람) |
| 3 | spec-sync | `spec-sync` → 문서 sync PR(30-work.md Delivery 대시보드 + `update-required` 인 SPEC) | 머지 SHA · 지금 코드 HEAD · sync PR head | **sync PR 사람 머지** |
| 4 | 닫기 | sync PR 머지 뒤 fresh evidence(`current` · `changed:false` · digest 같음) → `complete-delivery` | — | — |

**「사용자 실기기」 · 「TestFlight」 몫이 `undetermined` 인 채로 닫을 수 있나 → 없다.** harness `review_delivery` 는 `implementation = conformant` 일 때 **모든 Acceptance 가 `pass` + 근거**가 아니면 거절한다(`conformant review requires passing evidence for every Contract Acceptance`). #241 의 사용자 몫 = **A7**(통역 긴 세션 · 실기기 확인 묶음) · **A11**(8 · 9 · 10 실기기) · **A14**(TestFlight 사진 · 동영상). 길은 셋:

| 길 | 무엇 | 사람 결정 |
|---|---|---|
| (가) 실기기 · TestFlight 확인을 끝낸다 | 사용자가 A7 · A11 · A14 를 확인 → 근거(날짜 · 무엇을 봤는지)를 받아 `pass` 로 review | 사용자 확인 결과 |
| (나) 결과 계약에서 그 몫을 뺀다 | `start-delivery` 로 scope delta(v7 — 실기기 확인을 이 Delivery 밖 후속으로) → 새 plan_digest → **사람 승인 receipt** 필요 → 그 뒤 review conformant | 범위 변경 승인(receipt `human` · `kknaksss`) |
| (다) `conflict` 로 review | `resolve-implementation-conflict`(사람) → 결국 (나) 와 같은 scope delta | 같음 |

코디 실물 확인(dev 서버 — 사전 로그 · 저장소 올리기 → 읽기 → 지우기 · 오류 로그 0)은 A4 · A8 · A13 근거로 쓸 수 있다. 서버 · 앱 단위 시험(A1 ~ A3 · A5 · A6 · A9 · A10 · A12)은 코드 워커 리포트 · CI 근거가 필요하다.

per_spec 판단(review 때 사람 · 에이전트): 스펙 PR #929 가 코드보다 먼저 머지돼 SPEC-003 · 004 · 005 · 000 이 이미 구현 내용을 담고 있으므로 각 `none`(sync 는 대시보드만)일 가능성이 크다 — 구현과 스펙의 실제 차이를 review 때 diff 로 확인해 정한다(추측해 적지 않음).

### 2차 Delivery (읽기만 — 라벨 · 본문 · 재결속 0)

코드: 모두 **PR #238**(→ `dev` · 2026-11-11 머지 `aa7853cd` · head `b8a59cc3`)에 들어갔다 — #238 커밋에 #234 · #236 · #239(「차트 작성 · 방 이동 · 「방 배정」 판정 (#239)」) · #235 앱(「merge: #237 채팅·알림·앱을 #238 최신 board 위에 합침」 등)이 있다. #238 은 PR(merged · 라벨 없음).

| Delivery | 제목(줄임) | 라벨 | contract v · 위험 | baseline(지금 기록) | target SPEC | SPEC-000 stable 뒤에도 막는 것 |
|---|---|---|---|---|---|---|
| #234 | 데모/운영 연결 구분 없앰 | approved · exec ready · **pending** | v3 · L3 | pending @ `3f57c1af` | 000 · 001 · **002** | **DAY-SPEC-002 draft** · 재결속(새 SHA · version+1) · review(Acceptance 6 전부 pass) · spec-sync |
| #235 | 직원 앱 iOS 1차(v8 — 시술 현황 · 수락 · 통역 · 채팅 · 알림) | approved · exec ready · **pending** | v8 · L3 | pending @ `9692e1fb` | 003 · 001 · 004 · 000 | SPEC-000 stable 이면 target 모두 stable → **재결속으로 ready 가능**. 남는 것: review 에서 **Acceptance 53 개 전부 pass** — 실기기 · TestFlight · APNs 수신 · 통역 서버(D-3 — #241 로 지어짐) 같은 실물 항목이 많다 · 일부는 #241 이 뒤에 바꾼 계약(채팅 · 알림 · 통역)과 겹친다 |
| #236 | 기획안 맞추기 1차 | approved · exec ready · **pending** | v3 · L3 | pending @ `3f57c1af` | **002** | **DAY-SPEC-002 draft** |
| #239 | 차트 작성 · 방 이동 | approved · exec ready · **pending** | v1 · L3 | pending @ `9692e1fb` | **002** · 000 | **DAY-SPEC-002 draft** |

## 사용자가 정할 것

1. **스펙 PR(SPEC-000 stable) 머지** — 코디 PR · 사람 머지.
2. **#241 의 실기기 · TestFlight 몫(A7 · A11 · A14)** — (가) 확인을 끝내고 닫기 / (나) 그 몫을 이 Delivery 밖으로 빼는 범위 변경을 승인하고 닫기. 확인 없이 「통과」로 적어 닫을 길은 harness 규칙상 없다.
3. **DAY-SPEC-002(시술 현황)를 stable 로 올릴지** — #234 · #236 · #239 세 건이 이것 때문에 pending 이다(이번 지시는 SPEC-000 만이라 안 건드림).
4. **#235 를 어떻게 닫을지** — target 은 SPEC-000 stable 로 풀리지만 Acceptance 53 개 중 실물 항목이 많고 #241 과 겹친다. (가) 실물 확인 뒤 닫기 / (나) 실물 · 겹치는 항목을 범위 변경으로 정리하고 닫기(재승인) — 사람 판단.
5. 닫는 순서 — 코드는 #238 · #242 로 이미 dev 에 있으므로, 각 Delivery 는 review-delivery(merge SHA = #238 `aa7853cd` / #242 `7b099e8f`) → spec-sync PR(사람 머지) → 닫기. sync PR 을 Delivery 마다 따로 낼지 묶을지는 규칙상 「Delivery 당 최대 하나」다.
