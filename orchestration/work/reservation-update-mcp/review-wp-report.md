# 리뷰 리포트 R2 — reservation-update-mcp / WP-126 + §7.10 추가분 (2026-08-31)

## 판정: WARN (4건 — 그중 **1건은 PR 전 필수 조치**)

FAIL 없음 — **계약 확장 0 · 코드 좌표·실측 주장 전부 참 · 3자 동기 정상 · lint 0 error.**
R1 의 WARN 3건은 **전부 해소**됐고, 그 정정이 WP 작업·테스트로 정확히 흘렀다.
⚠ 다만 **`MEDINESS-WP-126` / `MEDINESS-DOC-246` 이 이미 다른 브랜치에 «푸시된» 상태**라 병합 시 충돌한다(W-1). 내용 결함이 아니라 **번호 조정**이 필요하다.

## 검수 범위

- 대상: `30-work/work-126-reservation-update-mcp-time-resolution.md`(untracked, 231행) + 이번 라운드 추가분(§7.10 R-1↔R-3 bullet · 30-work.md 3자 동기 · log 행)
- diff: 4파일 수정 + WP 1 untracked (+108/−7). **리포 파일 수정·생성 0**(read-only 준수).
- 실행: `python3 scripts/lint-pipeline.py --strict`(리포 루트) → **0 error / 255 warning**. mediness WARN 1건은 **SPEC-030 covering WP 파생값**으로 이번 diff 와 무관(diff 내 `SPEC-030` 출현 0으로 확인).
- 코드 대조: `mcp/app/tool_access.py` · `mcp/app/server.py` · `mcp/tests/test_tool_inventory.py` · `mcp/app/tools/reservation_cancel_request.py` · `back/app/services/action_runtime/chat/provider.py`
- 번호 유일성: origin 전 ref 스캔(`git grep` over `git branch -r` 전수 — ⚠ 부분 스캔은 놓친다, 아래 W-1)

---

## 1. 계약 확장 0 — 확인 (위반 없음)

WP 작업 항목을 SPEC-151 §6.2b·§7.10 · SPEC-060 ④ 와 1:1 대조했다. **범위 밖 동작을 만드는 항목 없음.**

| WP 항목 | 대응 계약 | 판정 |
|---|---|---|
| P1-A 툴 함수 · `structured{data,action_id,workflow_run_id,plan_version?}` | §6.2b 등재 bullet(문자 그대로 같은 모양) | ✅ 복제 아닌 구현 |
| P1-B `access(taint_policy=TAINT_SELF_LEDGER, capability="action.runtime.basic", needs=(list,get))` | §6.2b + SPEC-060 ④ | ✅ 값 3개 전부 계약과 일치 |
| P1-D 인벤토리 +1 · 예고 ④ → 행 대체 | SPEC-060 ④ 「착지 시 write 표에 1행을 더하고 … 그 시점의 실측으로 다시 센다」 | ✅ 규약 그대로 |
| P2-A 무조건 제약 삭제 + R-1 | §7.10:846 ⛔ 「존치할 수 없다」 · :862 「무엇을 말하지 «않아야» 하는가도 함께 소유」 | ✅ 계약이 명시적으로 요구한 것 |
| P2-B 되묻기를 접수 해석 축에 | §7.10:867 「결정은 접수 해석 축 · 감사는 출구일 뿐」 | ✅ |
| P3 무회귀·3자 동기 | — | ✅ |

**비목표 주장 검증**:

- **§7.9 무개정** — 이번 라운드 spec diff 헝크는 `+35..45`, `+148`, `+412`, `+446..448`, `+492..502`, **`+831..894`**, `+919`. §7.9 는 **726–830** 행 ⇒ **diff 0** 재확인(R1 대비 §7.10 이 53→64행으로 커졌지만 여전히 §7.9 «뒤»에서 시작). WP 도 비목표 + P3 확인 항목으로 이중 기장. ✅
- **모달 발·회의관리 화면 diff 0 · 새 REST/leaf/카드 유형/판단 버튼 0 · migration 0** — Code Surface 표가 `mcp/` 6칸 + `back/` 프롬프트 3칸으로 한정되고 `back/` 게이트 로직은 §제외에 명시. ✅
- ⚠ **잠재 확장으로 의심되던 2건, 검토 결과 확장 아님**:
  - P1-A 의 「아직 변경되지 않았습니다」 문구 → §7.10 의 **고정 문구 금지는 «채팅 되묻기 표면»** 에 걸리는 것이고, 이건 **MCP 툴 `content`** 다. 동형 표본이 같은 자리에 같은 문장을 이미 둔다(`reservation_cancel_request.py:92` 「※ **아직 취소되지 않았습니다.**」). §6.2b 의 「집행을 앞질러 말하지 않는다」를 **지키는** 문구다. ✅
  - P2-C 의 대안 「되묻기를 정형 응답 축으로 내보내 감사 스코프 밖에」 → **새 축 신설이 아니다.** §7.7:712 가 이미 「도구를 고른 턴·**정형 되묻기**는 [감사] 대상이 아니다」로 그 범주를 갖고 있다. WP 도 Open Issues 에서 **dev 판단**으로 두고 계약 요구 2개(결정=접수 축 · 고정 문구 금지)를 못 박았다. ✅

---

## 2. R-1↔R-3 bullet — 정합하나 «남은 now-상대 구절» 이 있다 (→ W-2)

`spec-151:858` 「R-3 는 **시각 축**(오전/오후)만 정하고 **날짜를 옮기지 않으며**, 날짜는 R-1 이 잡는다 ⇒ 「9월 3일 3시」는 9월 3일 15:00 … **새 해석 축을 만들지 않는다**」

**기존 R-3 예시와의 정합 — 성립한다.** 코드 실물(`provider.py:26-30`)의 두 예시가 **둘 다 같은 날**이다:

- `at 21:57 "10시반" today means 22:30` — «today» 가 문면에 박혀 있다 ⇒ 오전/오후 선택만 했다
- `at 09:00 "3시" means 15:00` — 같은 날 15:00

⇒ 「R-3 는 am/pm 만 고르고 날짜를 안 옮긴다」는 **예시의 충실한 일반화**이며 **새 축 발명 0** 이 맞다. 「9월 3일 3시 → 9월 3일 15:00」도 그 일반화의 직접 귀결이다. ✅

⚠ **다만 규칙 문면에 그 일반화를 막는 구절이 하나 더 있다** — 아래 **W-2**.

---

## 3. 코드 좌표·실측 주장 — 전수 참

| WP 주장 | 실측 | 판정 |
|---|---|---|
| 동형 표본 = `mcp/app/tools/reservation_cancel_request.py` | 존재 · `structured{data,action_id,workflow_run_id,plan_version?}`(:95-98) · leaf·taint·needs 3축(`server.py:1707-1725`) | ✅ |
| 테스트 표본 = `mcp/tests/test_reservation_cancel_request.py` | 존재 | ✅ |
| `access(...)` 3값 = `TAINT_SELF_LEDGER`·`action.runtime.basic`·`needs=(list,get)` | `server.py:1707-1711` 문자 그대로 동일 | ✅ |
| **오염 등급 미선언 = 기동 실패(fail-fast)** | `tool_access.py:227` `class UndeclaredTaintPolicy(RuntimeError)` · `:309` `assert_write_tools_declare_taint` · **`server.py:1989` 모듈 최상단 호출** ⇒ **import 시점 차단** = 문자 그대로 「기동 실패」 | ✅ 과장 아님 |
| `/health` 상수가 하드코딩이라 드리프트가 잘 난다 | `server.py:1844` `{"status":"ok","name":"mediness","tools": 61}` — 자동 집계 아님 | ✅ |
| `test_tool_inventory.py` 의 `EXPECTED_WRITE`·`EXPECTED_WRITE_TOOLS`·`EXPECTED_TOTAL` | `:32-34` `EXPECTED_READ=40` · `EXPECTED_WRITE=21` · `EXPECTED_TOTAL` · `:39` `EXPECTED_WRITE_TOOLS` | ✅ 이름 전부 실재 |
| read/write 판별은 **seam**(`_wrap_write_tool`)이지 이름 규칙이 아니다 | 파일 머리 `:7-8` 「read/write 판별은 **seam 으로 한다** … 이름 규칙으로 세면 이름을 바꾼 순간 조용히 틀린다」 + `:130`·`:153` 구현 | ✅ |
| **실측 = `/health` 61 (read 40 + write 21)** | 위 두 줄 그대로 | ✅ |
| **SPEC-060 표 머리 = read 39 + write 18 = 57** | `spec-060:181` 「### Tool 인벤토리 (read 39 + write 18)」 · `:453` §5 AC 「`/health` … **57**」 | ✅ |
| ⇒ **선재 드리프트 61 vs 57** 이 실재하고 **소급 정정은 이 WP 범위 밖** | 위 대조로 성립 | ✅ |
| 「`test_tool_inventory.py` 머리 주석이 같은 규율을 이미 적어 두었다」 | `:29-31` 「SPEC-060 인벤토리 표는 이 시점에 **«그 시점 실측 +1»** 로 갱신한다 — 표의 숫자를 그대로 옮겨 적지 않는다(표에 선재 드리프트가 있고 **실측이 정본**이다)」 | ✅ **거의 축자 일치** |
| `TIME_RESOLUTION_RULE` 은 **catalog turn 프롬프트에만** 실린다(감사 프롬프트 아님) | 전 리포 참조 3곳뿐 — 정의 `:26` · **호출 `:164`(= `build_prompt`, `:103` 시작)** · `__all__ :303`. 감사는 `build_audit_prompt`(`:217`)·`build_final_audit`(`:284`)이고 **이 상수를 싣지 않는다** | ✅ |
| 「감사는 워크플로를 고른 턴에 도달하지 않는다」 | `chat/service.py:1127-1129` docstring 「tool/**workflow** 를 고른 턴과 템플릿 응답은 **애초에 이 경로에 오지 않는다**」 + §7.7:712 | ✅ (R1 W-3 지적이 계약·WP 양쪽에 반영됨) |

**SPEC-060 자체의 내부 드리프트(참고)** — 같은 문서 안에서 `:181`·`:451` 은 write **18**, `:184`·`:353` 은 write **19** 로 갈려 있다. **선재분**이고 WP 가 「소급 정정하지 않고 자기 +1 만」으로 명시적으로 범위 밖에 둔 것과 같은 축이다. 이번 diff 가 만든 것이 아니다.

---

## 4. 테스트 계획 충분성 — P1 충분 · P2 에 미검증 계약 3건 (→ W-3)

**P1 (6 케이스 + 2) — §6.2b 를 실제로 문다.** 성공(`structured.action_id` 최상위 · `workflow_run_id` 일치 · 「아직 변경되지 않았다」) · 409 · 404(`action_id` 오투입 포함) · 422 · **date 동치 통과** · 익명 거부 + 인벤토리 3자 일치 + `back/` diff 0. ✅
🔑 **R1 의 W-2(「date 는 항상 422」 부정확)가 «date 동치 통과» 테스트로 그대로 흘렀다** — 문서 정정이 실행 계획까지 도달했다.

**P2 (9 항목) — R-1·R-2·R-3·R-4·경계·무남용·문자열 부재를 전부 문다.** 특히:

- **경계(종료 시각) 양면이 실제로 덮인다** — R-1 고정(15:08 「오늘 15~16시」 = **시작만 지남**)과 되묻기(**종료까지 지남**)가 경계 반대편 한 쌍이다. ✅
- **무조건 제약 문자열 부재 단언** — P2-A 삭제 작업의 회귀 방지로 정확한 수단이다. ✅
- **R-1↔R-3 동시**(「9월 3일 3시」 → 9월 3일 15:00) ✅

⚠ **§7.10 이 «계약» 으로 적었는데 검증 항목에 대응이 없는 것 3건** — W-3 참조.

---

## 5. 3자 동기·번호 — 동기 정상 · **번호 충돌 있음**(W-1)

**3자 동기 ✅** (lint 3자 일치 검사가 0 error 로 기계 확인 + 눈 대조)

| 자리 | 값 |
|---|---|
| WP frontmatter `status` | `proposed` |
| `30-work.md` Status Board(:113) | `proposed` · Owner `TBD` · 2~3d · 목표 `TBD` |
| `30-work.md` WP List(:200) | `proposed` · `TBD` · Covers `MEDINESS-SPEC-151, MEDINESS-SPEC-060` |
| Spec Coverage | SPEC-151(:226)·SPEC-060(:240) **양쪽 covering 칸에 WP-126 등재**, 구현 상태 `in_dev` 유지(다른 covering WP 파생 — lint derive 검사 통과) |
| `covers:` frontmatter | `MEDINESS-SPEC-151`, `MEDINESS-SPEC-060` — Coverage 표와 일치 |

**owner `TBD`** — `document-pipeline.md` §Owner 지정 규칙 상 허용(「아직 실제 책임자가 정해지지 않았을 때만」)이며 Status Board Owner 도 `TBD` 로 일치. 다음 review 의 open item. 위반 아님.

**WP 생성 전제(생명주기 5→6 게이트)** — covering SPEC 둘 다 frontmatter `status: stable` ⇒ 「스펙 확정 후 work 생성」 순서 준수. ✅

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN)

### W-1 (⚠ PR 전 필수 조치) — `MEDINESS-WP-126` · `MEDINESS-DOC-246` 이 **이미 다른 브랜치에 푸시돼 있다**

- 이 WP: `products/mediness/30-work/work-126-reservation-update-mcp-time-resolution.md` — `id: MEDINESS-WP-126` · `doc_no: MEDINESS-DOC-246`
- **충돌 상대**: `origin/task-redesign-spec` → `products/mediness/30-work/work-126-task-ledger-unification.md` — **`id: MEDINESS-WP-126` · `doc_no: MEDINESS-DOC-246` 동일**. **커밋·푸시 완료** 상태이고, 그 브랜치 HEAD 커밋 메시지가 `chore: upstream #665 머지 + 재번호 — WP-125→126(task-ledger)·WP-126→127(incident)` ⇒ 그쪽이 **#665 를 머지한 뒤 이미 126 으로 재번호**했다.
- 🔑 **파일명이 달라 git 이 충돌로 잡지 않는다** — 두 파일이 나란히 머지되고, 그 시점에 lint 가 **`doc_no` 전역 유일성 = ERROR(block)** 와 WP List/파일 ID 불일치를 던진다. 즉 **merge 는 조용히 성공하고 CI 가 뒤에서 깨진다.**
- **왜 planner 잘못이 아닌가**: `document-pipeline.md` §문서 번호의 부여 규칙은 **「현행 + `90-archive/` 전체 스캔 → max+1」(stateless scan)** 이다. 이 워크트리 기준 max 는 245였고 246 은 정확히 max+1 이며, **`origin/main` 기준으로도 126·246 은 비어 있다**(브리프가 지정한 기준). 그 규칙은 **구조적으로 sibling 브랜치를 못 본다** — 알려진 한계다.
- ⚠ **부분 스캔은 이 충돌을 놓친다** — remote 브랜치 목록 앞 40개만 훑으면 `origin/task-redesign-spec` 이 빠진다(내가 1차 스캔에서 실제로 놓쳤다). 전수 스캔이어야 한다.
- 근거 출처: `document-pipeline.md` §문서 번호(전역 유일·재사용 금지) · §자동 검증(`doc_no` 전역 유일성 ERROR — block).
- **권장 조치 (코디네이터 판단)**: 상대가 **이미 푸시**됐으므로 **이쪽을 재번호하는 편이 싸다.** origin 전 ref 전수 스캔 결과 **WP 는 127까지 · `doc_no` 는 247까지 점유** ⇒ 다음 빈 쌍은 **`MEDINESS-WP-128` / `MEDINESS-DOC-248`**. 바꿀 자리 = WP frontmatter `id`·`doc_no` · H1 · 파일명 slug · `30-work.md` 3표 · `log.md` 영향 ID.

### W-2 (중) — 규칙 문면에 **now-상대 구절이 하나 더** 남아 있다 (R-1↔R-3 를 다시 깰 수 있다)

- WP P2-A 는 삭제 대상으로 **「A reservation must start in the future」한 문장만** 지목한다(`work-126:132`).
- **실측 전문**(`provider.py:27-29`): `"Korean times without am/pm are ambiguous: resolve to the nearest upcoming time **from now** (e.g., at 21:57 "10시반" today means 22:30; at 09:00 "3시" means 15:00). A reservation must start in the future - …"`
- ⚠ **`from now` 도 now-상대다.** 「9월 3일 3시」처럼 **날짜가 명시된** 요청에 「지금부터 가장 가까운 미래」를 문자 그대로 적용하면 **9월 3일이라는 앵커가 없는 채로** 시각이 결정된다. §7.10:858 이 세운 「R-3 는 날짜를 옮기지 않는다」가 성립하려면 이 구절이 **「(주어진 날짜 안에서) 오전/오후를 고른다」로 한정**돼야 한다.
- 🔑 **WP 자신이 진단한 실패 모드와 같은 모양이다** — 「제약 문장을 남긴 채 R-1 을 얹으면 규칙이 자기 안에서 모순된다」(`work-126:23`, `spec-151:846`). now-상대 구절도 똑같이 **남겨 두면 R-1↔R-3 를 안에서 되돌린다.**
- WP P2-A 의 「기존 낮 시간대 예시를 **날짜 무관 동일 적용**으로 쓴다」가 이 의도를 담고는 있으나, **삭제·한정 대상 문자열로 명시되지 않아** 구현자가 `from now` 를 그대로 둘 여지가 있다. 검증 항목의 「무조건 제약 문장 부재」 단언도 `must start in the future` 만 겨냥한다.
- 근거 출처: `provider.py:27` 실물 + `spec-151:858` + reviewer `rules.md`(spec↔WP 정합).
- **권장 수정**: P2-A 에 「⚠ **`from now` 도 날짜 명시 시에는 앵커가 아니다** — 모호 해소는 **주어진 날짜 안에서** 오전/오후를 고르는 것으로 한정한다」를 한 줄 추가하고, 검증의 문자열 부재 단언에 `from now` 의 무한정 사용도 포함.

### W-3 (중) — §7.10 이 «계약» 으로 적은 것 중 **검증 항목이 없는 3건**

`work-126:143-153` 의 P2 검증 9항목과 §7.10 을 대조했을 때 대응이 없는 것:

1. **질문이 담아야 하는 사실 2개** — §7.10:868 「ⓐ 그 시각이 이미 지났다는 사실 ⓑ 말한 그대로 잡을지 묻는 질문. … **이 둘이 빠지면 되묻기가 아니다**」. WP 작업 P2-B 에는 있으나(`:139`) **검증 항목에 없다** — 되묻기 테스트는 「질문이 나오고 카드가 서지 않는다」만 본다. 표현은 자유여도 **두 사실의 존재**는 단언 가능하다(ⓐ 「지났」류 언급 · ⓑ 물음 형태).
2. **감사가 이 되묻기를 억제하지 않는다** — §7.10:878 이 **계약으로** 「**감사는 이 되묻기를 억제하지 않는다**」고 못 박았고, WP 도 P2-C 에서 **감사가 되돌릴 수 있음을 인정**한다(`:141`). 그런데 P2-C 는 **실사 + 완료 증거 기록**이고 **회귀 테스트가 없다** ⇒ 나중에 감사 프롬프트가 바뀌면 이 계약이 **조용히 깨진다.** 되묻기 테스트를 **감사를 포함한 end-to-end 축**에서 돌리면 그대로 커버되나, WP 가 어느 층의 테스트인지 말하지 않는다.
3. **명시 날짜 + 모호 시각이 «둘 다» 지난 경우** — 예: **21:57 에 「오늘 3시」**. R-3(가장 가까운 미래)는 날짜가 「오늘」로 묶이면 03:00·15:00 **둘 다 과거**라 답이 없고, 그 상태로 R-2 되묻기에 들어가면 **질문이 어느 시각을 말할지 정해지지 않는다.** 규칙표에도 검증에도 없다. 🔑 **§7.10 이 없애려던 「규칙이 답을 갖고 있지 않은 자리」와 같은 형태**다.
   - ⚠ 이건 **사용자 확정 범위 밖**(확정은 「모호 시각·날짜 없음 규칙은 유지」)이라 **위반이 아니다.** 실측 사고 사례는 「오후」가 붙어 모호하지 않았다. R1 리포트에서도 WARN 미만 참고로 남겼던 축이며, 이번에 R-1↔R-3 bullet 이 **미래 날짜 케이스만** 닫으면서 **과거 날짜 케이스가 남았다.**
- 근거 출처: `spec-151:868`·`:878` ↔ `work-126:143-153` · reviewer `rules.md`(테스트 존재·의미).
- **권장 수정**: 1·2 는 P2 검증에 각 1줄 추가(2 는 「되묻기 테스트를 감사 포함 경로에서 돌린다」로 층을 명시). 3 은 **이번 범위 밖으로 두되 §Open Issues 에 한 줄 기장** 권고.

### W-4 (저) — 「P1 6 케이스」 라벨과 실제 검증 8항목이 어긋난다

`work-126:113` 「**C. 툴 테스트 신설** — 아래 §검증의 6 케이스」인데 §검증은 **8항목**(성공·409·404·422·date 동치·익명 거부 + 인벤토리 3자 일치 + `back/` diff 0)이다. 뒤 2개가 툴 테스트가 아니라 phase 완료 조건이라면 라벨이 맞지만, 그대로 읽으면 2개가 새는 것처럼 보인다. **내용 결함 아님 — 라벨 정밀화만.**

---

## 기존 부채 (이번 판정 제외)

- **소유 판정·재요청 멱등 가드 2건에 owner 가 없다** — SPEC-060(2026-08-11) → SPEC-151 → WP-106 로 **참조만 순환**한다. WP-126 §Open Issues(`:213`)가 **이 순환을 정확히 기술하고 다음 라운드 조치를 권고**했다 ⇒ R1 리포트의 「기존 부채」 항목이 WP 로 승계됐다. **이 WP 가 늘리지도 줄이지도 않는다.** 다음 라운드 조치 대상.
- **SPEC-060 인벤토리 드리프트(표 57 / 실측 61) + 문서 내부 write 18↔19 불일치** — 선재분. WP §Open Issues(`:214`)가 기장하고 소급 정정을 명시적으로 범위 밖에 뒀다. **정정 담당 지정이 별건으로 남는다.**
- **lint mediness WARN 1건** — `30-work.md:235` SPEC-030 Spec Coverage 구현 상태 `in_dev` ≠ derive `done`. 이번 diff 와 무관(diff 내 SPEC-030 출현 0).
- **타 제품 lint WARN 254건**(charty·procedure-hub·selly) — 무관.

---

## 확인한 것 (PASS 근거) — 체크리스트 전수

- [x] **R1 WARN 3건 해소 확인** — W-1(규칙의 침묵 오진단) → `spec-151:837-846` 에 **2조각 표 + ⛔ 삭제 요구**로 정정 · W-2(date 무조건 422) → `:412`·SPEC-060 ④ 에 「같은 값이면 통과·무시」 명기 + **WP 테스트 케이스화** · W-3(되묻기 기제) → `:867` 에 **결정 자리 ⟂ 출구 자리** 분리 명문화. 셋 다 WP 작업 항목으로도 흘렀다.
- [x] **계약 확장 0** — 작업 항목 ↔ 계약 1:1 대조(§1 표). 확장 의심 2건 검토 후 «확장 아님» 결론.
- [x] **§7.9·모달 무개정** — 헝크 범위 ↔ 절 경계(726–830) 대조로 diff 0 재확인.
- [x] **R-1↔R-3 bullet 정합** — 코드 예시 2개가 모두 같은 날임을 확인, 「새 축 발명 0」 성립. 남은 `from now` 구절은 W-2.
- [x] **코드 좌표·실측 주장 12건 전수 대조** — 전부 참(§3 표). fail-fast 는 `server.py:1989` 모듈 최상단 호출로 「기동 실패」가 문자 그대로 성립.
- [x] **인벤토리 «실측 +1» 방침** — 표 57 vs 코드 61 드리프트 실재 확인, `test_tool_inventory.py:29-31` 이 같은 규율을 이미 적어 둔 것까지 확인.
- [x] **테스트 계획** — P1 충분. P2 는 R-1~R-4·경계 양면·무남용·문자열 부재를 문다. 미검증 계약 3건은 W-3.
- [x] **3자 동기** — frontmatter/Board/WP List 전부 `proposed`, Coverage 양쪽 등재, `covers:` 일치. lint 3자 일치 검사 0 error.
- [x] **WP 생성 전제(5→6 게이트)** — covering SPEC 둘 다 `stable`.
- [x] **번호 유일성** — 로컬·`origin/main` 클린. **origin 전 ref 전수 스캔에서 충돌 1건 발견** → W-1.
- [x] **lint --strict** — 0 error. mediness WARN 1건은 무관 선재분으로 분리.
- [x] **read-only 준수** — 리포 파일 수정·생성·삭제 0.
- [ ] **phase Status ↔ frontmatter status 게이트(7→8)** — **해당 없음.** 전 phase `TODO` · `status: proposed` 로 정합(lint 통과). 착지 후 `review-wp` 재검수 대상.
- [ ] **pm-dashboard sync** — **확인 안 함.** MCP 외부 surface 라 문서 검수 범위 밖이며, WP `## Execution` 머리에 지시가 실려 있다(착수 시 이행 대상).
