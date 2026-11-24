# 재검수 3 — SPEC-009 0.2.1(부위만)

> 검수자: procedure-hub reviewer(문서) · 2026-11-19 · read-only(이 파일 1 개만 씀)
> 대상: `SPEC-009-hub-clinic-supplement.md` 0.2.1(450 줄) · 수정 지시 `spec-009-fix3-instructions.md` · 앞 검수 `review-spec-009-r3.md`
> 대조: `_RESUME.md` §2(지금 판 — 11-19 행 21) · `silver-site-task.md` · `silver-site-addendum1.md` · `silver-site-addendum2.md` · `silver-site-report.md` · 작업 사본 `$S` = `$W/silver-model/`(silver · gold · 고친 스크립트 · `user.csv`) · 원본 `$SM`. 「SPEC :n」 = 0.2.1 파일 줄. `_R「…」` = 그 글로 시작하는 `_RESUME` §2 행.

## 판정 — **FAIL**

| 등급 | 수 | 요지 |
|---|---:|---|
| FAIL | 2 | ① 「근거 종류가 바뀌는 기존 입구 = SITE-120 1」 이 실물로 거짓 — **26**(이동 부위의 기존 별칭 25 + SITE-120). T3-1 은 제 기대로 FAIL 한다 ② 코디 답 `_R「silver 패치 1차 끝」`(A1 · A3 · G1 · G3 · 근거 종류 섞임)이 반영되지 않아 정해진 것을 아직 「정할 것」 · 「멈추고 질문」 으로 둔다 |
| WARN | 4 | 별칭 12 의 근거 · `description` 바뀜과 L-c · `user.csv` 꼴과 T1-2 · 고친 스크립트 범위 |
| PASS | — | r3 FAIL 3 · WARN 5 닫힘 · 범위 = 부위만 유지 · 근거 없는 정책 0(기본값 D-1 ~ D-5 는 `_R「코디 기본값」` 으로 받침) |

## 1. r3 지적 — 닫힘 여부

| # | r3 지적 | 0.2.1 자리 | 상태 |
|---|---|---|---|
| R1 | `_R「SPEC-009 범위 = 부위만」` 미반영 | G-2 · G-3 :72-73 · §2 · §3-2 · §3-5 · Q 에서 내림 | **닫힘** — 「눈」 안 함 · site + `anatomy_site` · 다른 이름 범위 · `user.csv` · 작업 사본 전부 G 로 |
| R2 | `_R` 줄 인용 밀림 | :38 「행 첫 글을 키로」 · 본문 전체 `_R「…」` · 부록 A 에만 줄 | **닫힘** — 본문 키 글 10 개를 지금 `_RESUME` 에 grep 해 보니 모두 한 행에 닿는다. 부록 A 의 줄(:38 ~ :57)은 이미 다시 **+3 밀렸다**(「코디 기본값」 = 지금 :41 · 「SPEC-009 범위」 = :42 · 「허브 보강 단계 시작」 = :43 …). 머리 :384 에 「밀린다」 고 적어 두었으니 그대로 둬도 된다 |
| R3 | silver-check 원장 경로 | F-8 :117 · §3-4 :236 · G-11 | **닫힘** — 작업 사본에서 `PHUB_REC = WORK/_archive/procedure-hub/phub-recommend` 로 고쳐져 S1 통과(리포트 §3 · 실물 diff 확인) |
| W1 | 새 부위 넷 자리 | D-1 :90 · §3-2 :214 | 닫힘 — `_R「코디 기본값(사용자 확인 대기)」` 와 같음 |
| W2 | 근거 종류 식 | E3 :142 · §2-3 :169 | 닫힘 — 작업 사본 세 곳이 같은 식 `startswith(('사용자', 'drafts/clinic-supplement/'))`(diff 확인) |
| W3 | 별칭 목록 | §3-2 :216 · D-4 | 닫힘 — 실물 alias +12 = SPEC 목록과 같음 · 「애교」 빠짐 |
| W4 | 겹침 목록 | §0-2 :61 · F-21 · T3-6 | 닫힘 — 리포트 §7 의 새 겹침(기타 · 승모근 · 쇄골 · 침샘)과 같음 |
| W5 | D3 · 묶음 부위 근거 | D-3 · D-5 · T4 | 닫힘 |

범위(④) — 본문 · 정할 것 · 다음 단계에 제품 · 시술 · 적용 부위 범위 없음. 부록 C :411-422 에 이름만 있다. **PASS.**

## 2. FAIL

### R4-1. 근거 종류가 바뀌는 기존 입구는 1 이 아니라 26 이다

- SPEC F-17 :126 · §0-2 :64 · §4-1 :258 · T3-1 :270 · §6-1 :338 — 「이름 · 행 근거가 없는 site 입구 행만 — 지금 SITE-120 1」.
- 실측: 원본 gold `g_entry` 와 작업 사본 gold `g_entry` 를 (`text`, `entity_table`, `entity_code`, `name_kind`)로 맞대면, 근거 종류만 바뀐 기존 행이 **26** 이다.
  - 모두 「원장」 → 「원장 + 사용자 제공」.
  - 이름 1(마리오네트라인) · 의학 용어 17 · 별칭 8.
  - 예: 하안면부 · 안검 · 애교 · 팔자 · 비순구 · 법령선 · 턱라인 · 두부 · 경부 · 대퇴부 · 배 · 하지 …
  - 새 행 38 · 없어진 행 0. 리포트 §4 와 같다.
- 까닭: 별칭 입구도 이름 입구와 같은 꼴로 근거를 고른다(`gold-build.py:147`). 그 부위에 `field = alias` 근거가 없으면 **부위 행 근거 전부**를 받는다. 이동한 부위에 붙은 `parent_code` 근거(`user.csv`)가 그 안에 섞인다. 지금 site 별칭에 `alias` 근거가 있는 부위는 5 곳뿐이다(리포트 §7).
  - SPEC F-17 은 `:147` 을 인용하면서도 셈을 이름 행 1 로만 적었다. 1차 검수(내 F2)도 같은 잘못을 했다.
- 결과:
  - T3-1 「바뀐 gold 행 = SITE-120 입구 행뿐」 은 이 판 실물에서 **제 기대로 FAIL** 한다.
  - 사용자에게 보이는 변화도 빠졌다. 상담 앱은 `evidence_kind` 를 `basis` 로 LLM 에 싣는다(`$A/clinic_chat/walk/material.py:97-98`). 「팔자」 「경부」 처럼 원장에서 온 별칭 25 개가 「원장 + 사용자 제공」 표지로 실린다.
- `_R「silver 패치 1차 끝」` 이 「이동 부위 별칭 25 + SITE-120 근거 종류 섞임 받아들임」 으로 이미 정했다.
- 고칠 것:
  - F-17 · T3-1 · §4-1 · §6-1 의 셈을 「이름 · 별칭 입구 가운데 자기 근거(`name_ko` · `name` · 빈칸 / `alias`)가 없는 것 — 이번 판 26」 으로.
  - 이 섞임을 「정해진 것(받아들임)」 으로 G 에.
  - §0-2 에 「원장 별칭 25 의 표지가 『원장 + 사용자 제공』 으로 바뀐다」 줄.
  - Q-4(SITE-120 근거 보충)는 대상이 26 으로 넓어짐을 적을 것.

### R4-2. 코디 답 `_R「silver 패치 1차 끝」` 이 반영되지 않았다

- `_RESUME.md` 맨 위 행 · `silver-site-addendum2.md` 가 정한 것은 넷이다.
  1. A1 = 묶음 기준 사본 `archive/silver-before-clinic-a-20261119/`
  2. A3 = 재현 대조(`silver-supplement.py` + `build_site_3tier.py`)
  3. G1 · G3 = 경로를 `phub-consult-demo/` 로 · **작업 사본 밖 변경은 WARN**
  4. 별칭 근거 섞임 받아들임
- SPEC 은 아직 이렇게 적고 있다.

| SPEC | 지금 적힌 것 | 정해진 것 |
|---|---|---|
| Q-5 :366 | A1 · A3 열림 | (a) 묶음 기준 사본 · A3 묶음 재현 — 정해짐 |
| §3-4 :240-241 · P6 :297 · §5-2 그림 :304 · §8 W-1 :376 | A1 · A3 「고치지 않는다 — 멈추고 질문」 | 작업 사본에서 고침(실물: 작업 사본 `gold-check.py` A1 이 묶음 기준 사본 · 허용 = `parent_code` · 「묶음 부위」 description · 끝 덧붙임 / A3 = 보강 + `build_site_3tier.py` 재현 대조) |
| G-11 :81 | 허용 = 경로 · G1 · 근거 종류 · D3 | + A1 · A3 · **G3**(silver-check · 원본 `silver-check.py:973-977` 의 옛 경로 — SPEC 어디에도 없다) · **A2**(silver-check 끝 줄이 「PASS (WARN n)」 이고 WARN 이 전부 G3 이면 통과 — 작업 사본 `gold-check.py` `a2`) |
| P5 :296 | silver 검사 「PASS(WARN 0)」 | 작업 사본 밖 변경 WARN 은 남는다(지금 5 — 리포트 §1) → 「FAIL 0 · WARN 은 작업 사본 밖 G3 만」 |
| P6 :297 · T3-5 | gold-check PASS | 같은 이유로 「FAIL 0 · WARN 은 G1 · A2 의 작업 사본 밖 변경만」(리포트 「WARN 10」) |

- 0.2.1(16:2x)이 addendum2 · `_R` 맨 위 행보다 먼저 쓰인 것으로 보인다. 그래도 결과는 「정해진 것을 다시 묻는 SPEC」 이다(CLAUDE.md). 고칠 것은 위 표대로 G-11 을 넓히고, Q-5 를 G 로 옮기는 것이다.

## 3. WARN

| # | SPEC 자리 | 지적 | 근거(실측) |
|---|---|---|---|
| W1 | E1 :140 · E6 :145 · §3-3 A5 :226 | **새 다른 이름 12 에는 `source_ref` 가 0 이다.** SPEC 은 E1 에서 「원장에 없는 다른 이름 → `user.csv` 줄」, E6 에서 「새 별칭마다 `source_ref` ≥ 1」 이라 했다. 실물은 `user.csv` 에 「다른 이름(기록만 · source_ref 없음)」 12 줄만 있고 `source_ref` 덧붙임 113 줄에 `field = alias` 는 0 이다. 까닭(리포트 §7): `source_ref` 는 (부위, 칸) 단위라 별칭 낱말 하나를 가리킬 수 없다. `(site, code, alias)` 를 달면 그 부위의 **기존 별칭 입구 17** 개 근거까지 사용자 근거로 바뀐다. 그래서 새 별칭 입구는 부위 행 근거를 받는다 — 「근거 없는 gold 행」 은 아니지만, 별칭 **글자**를 받치는 근거는 없다(A5 는 site 표에 안 걸린다 — `silver-check.py:170` `COVER['A5'] = {'procedure'}`). `_R` · addendum 어디에도 없는 **워커 판단**이다. SPEC 규칙을 실물에 맞추거나(「별칭 근거 = 부위 행 근거 · `user.csv` 기록」) 코디 · 사용자 확인으로 올릴 것 | `user.csv` kind 셈 · `source_ref.csv` 끝 113 줄 셈(site 빈칸 26 · `parent_code` 78 · `description` 6 · `anatomy_site` 3) |
| W2 | L-c :285 · §3-2 :212 · T5-2 :328 | 「기존 행은 덧붙이기만 — 예외는 `site.parent_code` 칸」 · 「`site.csv` 의 그 칸만 바뀐다」 라고 적었다. 그런데 T4 :201 · D-5 대로 **기존 묶음 부위 6 행의 `description` 이 바뀌었다**(사지 · 상체 · 체간 · 코안면 · 중안면 · 하안면 — `source_ref` `description` 근거 6). 작업 사본 A1 도 「`description` 이 『묶음 부위』 로 시작」 을 허용한다. SPEC 안에서 서로 어긋나므로 L-c · §3-2 · T5-2 에 예외 둘째를 적을 것 | 리포트 §2 · 작업 사본 `gold-check.py` A1 |
| W3 | §2-2 :148-160 · T1-2 :187 | 실물 `user.csv` 칸 = `line,kind,target_table,target_code,name,field,decision,basis,status`. SPEC 표는 `claim` · `quote` · `locator` · `note` 이고 **`status` 칸이 빠졌다**. `status` 는 작업 사본 `resolve` 가 「확인」 인지 보는 칸이다(E4 의 뜻 — 0.2.1 에서 E4 줄도 없어짐). T1-2 「`quote` 가 결정 행 한 줄에 정확히 들어 있음」 은 실물로 돌 수 없다. `basis` 가 모든 줄 같은 글(「사용자 결정 2026-11-19 · 명동점 KOS 진료항목명」)이고, `decision` 은 워커가 요약한 글이다(예 「위 부위 최상위 → 전신」). §2-2 를 실물 칸으로 고치고, T1-2 를 빼거나 「`decision` 이 어느 결정 행에서 왔는지」 를 담을 칸을 정할 것. 공개 쪽은 문제없다 — 「명동점」 글자는 로컬 `user.csv` 에만 있고 공개 silver grep 0 | `user.csv:1-3` · `grep 명동\|세라미크\|myeongdong silver/*.csv` = 0 |
| W4 | G-11 :81 · §3-4 | 작업 사본에서 실제로 고친 스크립트 범위가 SPEC 이 적은 것보다 넓다 — 원본 대비 diff: `silver-check.py`(원장 경로 · `resolve` 갈래 · `ref_kind` · D3 · **G3**) · `gold-build.py`(`ev_kind`) · `gold-check.py`(`ev_kind` · G1 · **A1 다시 씀** · **A3** · **A2** · WARN 출력). 이 가운데 A2 를 고친 것은 addendum2 의 「A2 도 다시 돌려라」(다시 돌림)보다 넓다. 그러나 WARN 정책을 따르려면 꼭 필요하다. 바뀐 A1 은 기준을 묶음 기준 사본으로 옮기면서 옛 허용 갈래(`procedure_relation` same_day · `concern_site` 8 · `external_code` 헤더만)를 「기준 사본과 바이트 같음」 으로 대신한다 — 기준 사본에 이미 들어 있으니 뜻은 지켜진다. R4-2 와 함께 G-11 에 적고, Q-6(정본 자리)이 이 diff 전부를 대상으로 함을 적을 것 | `diff $SM/… $S/…` |

## 4. 근거 없는 정책 · 공개

- 규칙 표(E · T · L · R · D)에서 결정 · 조사 · 코드에 닿지 않는 것은 없다. D-1 ~ D-5 는 `_R「코디 기본값(사용자 확인 대기)」` 와 3단 조사로 받쳐지고, 「사용자 확인 대기」 로 표시돼 있다. **0 건.**
- 공개: SPEC 파일 uuid · 진료항목 코드 · 가격 · 병원 실명 grep 0. 작업 사본 공개 silver 에 「명동 · myeongdong」 0 · 묶음 키 `clinic-a-20261119`.

## 5. 실측 수

| 셈 | 값 |
|---|---|
| 작업 사본 `site` · `alias` · `source_ref` 데이터 줄 | 115 · 992 · 48,226 |
| `source_ref` 끝 덧붙임 113 | `user.csv` 101(site 빈칸 17 · `parent_code` 78 · `description` 6) + 원장 12(새 부위 9 · `anatomy_site` 3) |
| `user.csv` kind | 위치 이동 69 · 새 부위 자리 9 · 새 부위(원장 근거 없음) 15 · 새 2단 2 · 묶음 부위 6 · 다른 이름(기록만) 12 = 113 |
| g_entry 전 · 후 | 근거 종류만 바뀜 26(원장 → 원장 + 사용자 제공) · 새 38 · 없어짐 0 |
| `_RESUME` §2 11-19 행 | 21 |
