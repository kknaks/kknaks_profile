# 재검수 2 — SPEC-009 0.2.0(부위만)

> 검수자: procedure-hub reviewer(문서) · 2026-11-19 · read-only(이 파일 1 개만 씀)
> 대상: `SPEC-009-hub-clinic-supplement.md` 0.2.0(432 줄 · 16:19) · 수정 지시 `spec-009-fix2-instructions.md` · 앞 검수 `review-spec-009.md` · `review-spec-009-r2.md` · 참고 `silver-site-task.md`(코디 silver 발주)
> 대조: `_RESUME.md` §2(지금 판 · 16:17) · `$R/hub-site-tree-draft.csv` · `research-site-tree.md` · `research-kos-site-3tier.md` · `$SM` silver · gold-check · silver-check · 작업 사본 `$W/silver-model/`(존재 · gitignore `.gitignore:161`). 「SPEC :n」 = 0.2.0 파일 줄.

## 판정 — **FAIL**

| 등급 | 수 | 요지 |
|---|---:|---|
| FAIL | 3 | ① 새 결정 `_R :37`(범위 = 부위만 · 이번 판 기본값)이 반영되지 않았다 — 그 결정이 닫은 것 여섯을 아직 「정할 것」 으로 연다 ② `_R` 줄 인용이 또 전부 한 줄 밀렸다 ③ silver-check 의 원장 경로가 낡아 P5 silver 검사가 패치와 상관없이 깨진다(SPEC · 앞 검수 둘 다 놓침) |
| WARN | 5 | 새 부위 넷의 자리 근거 · silver 발주와 SPEC 의 어긋남(근거 파일 · 작업 공간 · 별칭 목록 · D3 처리) |
| PASS | — | ① 범위 = 부위만 · ② 결정 반영(배치) · ③ 사실 · 코드 인용 대부분 |

## PASS — 맞은 것

| 볼 것 | 결과 |
|---|---|
| ① 범위 = 부위만 | **PASS.** 본문 · 정할 것(Q-1 ~ Q-12) · 다음 단계(W-1 ~ W-3)에 적용 부위 범위 · 제품 · 시술 추가 · 보강 목록 · 병원 무관 원칙 · `basis` 가 남지 않았다. `grep 제품\|시술\|product\|procedure\|site_scope\|부위 범위\|보강 목록\|basis` 에 걸린 곳은 머리 메타(:6 · :12) · 출처 경로 · G-2 의 「빼낸 것」 설명 · F-11(gold-build 가 `parent_code` 를 쓰는 곳 — 사실) · F-20(SITE-019 를 가리키는 표 이름) · F-13(A1 허용 목록 원문)뿐이다. 빼낸 것은 부록 C :401-410 에 한 줄씩 이름만 있다 |
| ② 배치 결정 | G-4 :72 · G-5 :73 · G-6 :74 · T1 ~ T9 가 11-19 배치 결정(3단 · 머리 · 귀 · 귀밑샘 · 턱밑샘 · 팔자 · 마리오네트 · 헤어라인 · 잇몸 · 구강 · 비강 · 부비동 · 눈 · 구레나룻 · 수염 · 묶음 · 관절 → 몸 > 기타 · 추가 15)과 같다. 바꾼 것 없음 |
| ② 결정 새로 만듦 | 규칙 표(E · T · L · R · M)에서 결정 · 조사 · 코드에 닿지 않는 규칙은 「(제안)」 또는 Q 로 표시됨 — 0 건(아래 W1 · W5 는 근거가 조사 처리인 것) |
| ③ 사실 · 코드 인용 | F-1 ~ F-22 의 수 · 파일:줄을 앞 두 판에서 실측한 값과 다시 대조 — 같음. F-13 의 새 인용 `gold-check.py:86-92`(source_ref) · `:93-96`(concern_site) · `:97-98`(그 밖 파일 한 바이트도 FAIL) 맞음. Q-8 의 `research-site-tree.md:138` · `:260`(T-5) · `hub-site-tree-draft.csv:46` · `:82` 맞음 |
| 앞 검수 r2 남은 WARN | N1(T1-2 `quote` 유일 시험 :173) · N2(Q-8 근거 줄 :361) · N3(E5 예외 :127 · M5 :236) · N5(흐름 그림 :293-294 · G1 · T3-7) 닫힘 · N4 는 제품 절이 빠져 대상 없음 — 맞다 |
| 공개 | SPEC 파일 uuid · 진료항목 코드 꼴 · 가격 꼴 · 병원 실명 grep 0 · 「myeongdong」 예시도 `<묶음>` 으로 바뀜 |

## FAIL

### R1. 새 결정 `_R :37` 이 빠졌다 — 닫힌 것 여섯을 다시 연다

- `_RESUME.md:37`(지금 판 맨 위 행): 「**SPEC-009 범위 = 부위만** · **silver 바로 고침**(작업 사본 `silver-model/` · gitignore) · 이번 판 기본값: 「눈」 합침 안 함 · 침샘 · 쇄골 · 승모근 = site + anatomy_site · 다른 이름은 허브 부위 다른 이름만(거미스마일 · 러브핸들 · 측두근 제외) · 원장 근거 없는 부위 근거 = 로컬 `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`(병원 이름 · 코드 공개 0)」.
- SPEC 은 이 행을 인용하지 않는다. G-2 :70 의 근거는 `spec-009-fix2-instructions.md`(코디 지시서)이고, 머리 결정 목록 :18 · 부록 A :379-388 에도 없다.
- 그래서 이미 닫힌 것이 아직 「정할 것」 이다(CLAUDE.md 「정해진 것을 다시 논의하지 않는다」):

| SPEC | 지금 적힌 것 | `_R :37` 이 정한 것 |
|---|---|---|
| Q-7 :360 · §3-5 :226-240 · T3-7 | (a) 합침 M1 ~ M5 / (b) 미룸 | **(b) 이번 판 합침 안 함** — SITE-018 은 3단 밖 예외 1 |
| Q-6 :359 · §3-3 :210 | (a) site 안 만들고 `anatomy_site` (b) 다른 이름 (c) D3 바꿈 | **site 를 만들고 `anatomy_site` 로 잇는다** — SPEC 선택지에 없는 꼴이다. 이 꼴이면 이름이 그대로라 **D3 는 여전히 FAIL** → 사실상 (c) D3 규칙 바꿈이 따라온다(W5) |
| Q-8 :361 · §3-2 :201 | 넣나 / 안 넣나 | **넣지 않음**(거미스마일 · 러브핸들 · 측두근 제외) |
| Q-2 :355 · E3 :125 · §2-2 | (a) 줄 내용 `source_kind` / (b) 경로 머리 | 근거 파일 = `…/user.csv` — **원천별 경로(b) 꼴** |
| Q-3 ① ② :356 · §2-2 :146 | 공개 범위 · 묶음 이름 | 묶음 키 = **`clinic-a-20261119`** · 병원 이름 · 코드 공개 0. ③(조사 리포트 마감 커밋)만 남는다 |
| Q-11 :364 · `$SM` 정의 :37 · P3 :284 · P4 :285 | 아카이브 silver-model 을 이어 쓰나 · 새 자리 | **작업 사본 `$W/silver-model/`**(원본은 읽기만 — `silver-site-task.md`) |

- 고칠 것: `_R :37` 을 머리 · G-2 · 부록 A 에 넣는다. 위 여섯을 「정해진 것(이번 판 기본값)」 으로 옮긴다. `$SM` · P3 · P4 의 자리를 작업 사본으로, §2-2 의 `evidence.csv` · `source_kind` 꼴을 `user.csv` 꼴로 맞춘다. Q-6 은 「D3 를 어떻게 바꾸나」 만 남긴다.

### R2. `_R` 줄 인용이 다시 전부 한 줄 밀렸다

- `_R :37` 행이 맨 위에 들어오면서 SPEC 의 `_R :n` 21 곳이 모두 한 줄 위를 가리킨다.

| SPEC 이 쓴 줄 | 실제 그 줄 | SPEC 이 말한 결정의 지금 줄 |
|---|---|---|
| :37 「허브 보강 단계」 | 범위 = 부위만(새 행) | :38 |
| :40 「추가 15 · 거미스마일」 | 부위 범위 값 | :41 |
| :41 「3단 나머지 · 관절」 | 추가 15 · 거미스마일 | :42 |
| :42 「머리 · 귀」 | 3단 나머지 | :43 |
| :43 「3단 · 위 → 아래」 | 머리 · 귀 | :44 |
| :45 「허브 보강한다」 | 기준 표 | :46 |
| :47 「일하는 방식」 | slug | :48 |
| :54 「매핑 새 세션」 | 124 직접 검수 | :55 |

  `:14` · `:17`(워크트리 줄)은 맞다.
- F-23 :115 · 부록 B ⑥ :399 「11-19 행 18」 → 지금 **19**(`grep -c '^| 2026-11-19' _RESUME.md`).
- 두 번째 같은 지적이다(1차 검수 F5). `_RESUME` 은 새 결정을 **맨 위에** 넣으므로 줄 번호는 판마다 밀린다. SPEC 이 근거 파일 `locator` 에서 줄 번호를 버린 것(§2-2 :140)과 같은 이유로, SPEC 자신의 `_R` 인용도 **결정 글 인용(「…」)을 키로**, 줄은 덧붙이는 정도로 하기를 권한다.

### R3. silver-check 의 원장 경로가 낡았다 — P5 가 패치와 상관없이 깨진다

- `silver-check.py:30-37` — `WORK` = 위로 올라가며 찾은 `orchestration/work` · `LEDGER = WORK/phub-recommend/bronze/phub-ledger` · `STEP1 = WORK/phub-recommend/step1-products.json`. 주석 :30-31 은 「원장은 열린 작업 work/phub-recommend/bronze/ 에 있다」 고 한다.
- 실측: `phub-recommend` 는 아카이브로 옮겨졌다.
  - 프로필 main 체크아웃: `orchestration/work/phub-recommend/bronze/phub-ledger` **없음** · `_archive/procedure-hub/phub-recommend/bronze/phub-ledger` 있음 · `step1-products.json` 도 `_archive/…` 에만 있음.
  - 이 워크트리(`$W/silver-model` 작업 사본이 쓰는 쪽): 같다. `orchestration/work/phub-recommend/` 없음 · `_archive/procedure-hub/phub-recommend/bronze/phub-ledger` 있음.
- 결과: `resolve` 가 원장 파일을 못 찾는다 — `if not os.path.exists(os.path.join(LEDGER, fn)): raise KeyError(fn)`(`:114-115`) · step1 도 같다. 그러면 원장 근거(source_ref 48,113 의 대부분)가 전부 **S1 「근거 포인터가 원장 · 출처에 없음」 FAIL**(`:343-345`)이 된다. P5 「PASS(WARN 0)」(:286)는 부위 패치와 상관없이 닿을 수 없다.
- SPEC F-13 · §3-4 는 G1 의 낡은 경로는 짚었지만 이 경로는 없다. 앞 두 검수(내 리포트)도 놓쳤다.
- 고칠 것: §3-4 「깨지는 자리」 와 Q-11(작업 공간)에 `silver-check.py:30-37` 의 원장 · step1 경로를 더한다. silver 발주(`silver-site-task.md`)는 「검사 스크립트 수정 0」 이므로, 워커가 P5 에서 멈추는 것이 정상임을 코디가 미리 알 것.

## WARN

| # | SPEC 자리 | 지적 | 근거(실측) |
|---|---|---|---|
| W1 | §3-2 :200 · T3 :186 | **새 부위 6 가운데 넷(침샘 · 나비존 · 부유방 · 쇄골)의 2단 자리가 SPEC 에 없다.** 배치안은 2단을 비워 둔 「자리 후보」 다(`hub-site-tree-draft.csv:109-112` · `research-site-tree.md:34-35` · `:52-53` · `:167-170`). 3단 조사가 정규화 결과로 얼굴 > 턱 > 침샘 · 얼굴 > 볼 > 나비존 · 몸 > 가슴 > 부유방 · 몸 > 목 > 쇄골 에 두었고(`research-kos-site-3tier.md:77` · `:88` · `:89` · `:98`), silver 발주는 이 넷을 「확정 변경」 으로 적었다. 그러나 `_RESUME` §2 에는 이 넷의 자리 결정이 **없다**(grep 0). T3 「1단 아닌 부위는 `parent_code` 가 있다」 를 지키려면 자리가 필요하다. `_RESUME` 에 기록(사용자 확인)하거나 Q 로 둘 것. 귀밑샘(귀 아래) · 턱밑샘(턱 아래)은 결정이 있다(`_RESUME.md:44`) | `grep -n '나비존\|부유방\|쇄골\|침샘' _RESUME.md` = 0 |
| W2 | E1 :123 · §2-3 :153-155 | `_R :37` 꼴(`drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`)은 **지금 식으로는 「원장」 으로 분류된다.** `ev_kind` · `ref_kind`(`gold-build.py:50-57` · `gold-check.py:173-178` · `silver-check.py:128-134`)는 `사용자` 머리만 「사용자 제공」 으로 본다. 이 ref 는 머리가 다르고 `:` 가 있으므로 「원장」 이다. 또 `resolve` 에 이 갈래가 없어 원장 파일로 찾다가 S1 FAIL 이다(`:114-115`). §2-3 에 「`drafts/clinic-supplement/<묶음>/user.csv` → 사용자 제공」 을 세 곳 같은 식으로 넣는다고 구체적으로 적을 것. silver 발주는 검사 스크립트를 못 고치므로, 이것도 P5 에서 멈추는 자리다. 멈추지 않고 gold 까지 가면 사용자 결정이 「원장」 표지로 앱에 실린다(F-19 쪽 · `basis`) | 코드 |
| W3 | §3-2 :201 vs `silver-site-task.md` 「다른 이름」 | silver 발주의 별칭 13 이 SPEC 이 말한 입력(배치안 「다른 이름 추가」 칸 + 하관)과 다르다. ① **「애교 → 애교살」 은 이미 있다**(`alias.csv:308` `site,SITE-034,애교,별칭`) → 넣으면 **A1 「alias 중복」 FAIL**(`silver-check.py:499-502`). 배치안에도 없는 낱말이다. ② 「팔 상완」 · 「하관」 은 배치안 글자(「상완」 · 「하관전체」 — `hub-site-tree-draft.csv`)와 다르다. A5(별칭 글자가 근거 글에 있음)를 받칠 `quote` 가 무엇인지 정해야 한다. SPEC 쪽은 「배치안 16 낱말 가운데 허브 부위 다른 이름 + 하관」 이 맞고, 발주 목록을 그에 맞출 것 | 실측 |
| W4 | 「사용자가 만날 자리」 §0-2 :61 | 「두 갈래로 갈린다」 목록에 거미스마일 · 러브핸들 · 측두근이 남아 있다. `_R :37` 로 이 셋은 넣지 않으므로, 이번 판에 실제로 생기는 겹침은 **기타(CON-278) · 승모근 · 침샘 · 쇄골**(새 site)뿐이다 | F-21 · `_R :37` |
| W5 | Q-6 :359 · §3-3 :210 | (R1 과 이어짐) 「site + `anatomy_site`」 를 고르면 D3(`silver-check.py:543-550`)는 이름만 보므로 FAIL 이 남는다. 「D3 를 어떻게 바꾸나」(예: `anatomy_site` 로 이어진 같은 이름 짝은 허용)가 진짜로 정할 것이다. 4 번째 선택지로 적을 것. 사지 · 상체 · 체간 · 코안면을 2단에 두는 것(T3 · T4)은 사용자 결정이 아니라 3단 조사의 처리(`research-kos-site-3tier.md:285` 「기준에 단이 없었다 … 두었다」)다 — 근거 칸에 그렇게 적을 것 | 코드 · 조사 |

## silver 발주(`silver-site-task.md`)와 SPEC 0.2.0 의 어긋남 — 요약

| 자리 | SPEC 0.2.0 | silver 발주 · `_R :37` | 어느 쪽을 고치나 |
|---|---|---|---|
| 작업 공간 | `$SM` = 아카이브 원본(:37 · P3 · P4) | `$W/silver-model/` 작업 사본 | SPEC(R1) |
| 근거 파일 | `evidence.csv` + `source_kind` | `user.csv` | SPEC(R1 · W2) |
| 묶음 이름 | `<병원 키>-<날짜>`(Q-3) | `clinic-a-20261119` | SPEC(R1) |
| 「눈」 | Q-7 열림 | 합침 안 함 | SPEC(R1) |
| 침샘 · 쇄골 · 승모근 | Q-6 (a) ~ (c) | site + anatomy_site(D3 FAIL 이면 멈춤) | SPEC(W5) |
| 거미스마일 · 러브핸들 · 측두근 | Q-8 열림 | 제외 | SPEC(R1 · W4) |
| 침샘 · 나비존 · 부유방 · 쇄골 자리 | 없음 | 「확정 변경」 | `_RESUME` 기록 또는 Q(W1) |
| 별칭 목록 | 배치안 16 + 하관 | 13(애교 중복 · 팔 상완 · 하관) | 발주(W3) |
| 원장 경로 · 근거 종류 식 | 원장 경로 언급 없음 · 식은 §2-3 | 스크립트 수정 0 | 둘 다 — P5 에서 멈추는 것이 정상(R3 · W2) |
