---
type: spec
id: SPEC-009
title: "허브 부위 보강(명동점) — 부위 3단 · 새 부위 · 다른 이름 · 부위 근거 꼴 · 반영 절차(gold 빌드까지)"
status: draft
product: procedure-hub
feature: phub-consult-demo
version: 0.2.2
created_at: 2026-11-19
updated_at: 2026-11-19
tags:
  - product/procedure-hub
  - feature/phub-consult-demo
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-consult-demo/_RESUME.md §2 — 행 첫 글로 인용(줄은 0.2.2 기준 · 부록 A): 「silver 패치 1차 끝」 :42 · 「코디 기본값(사용자 확인 대기): 새 부위 자리」 :43 · 「SPEC-009 범위 = 부위만 · silver 바로 고침 · 이번 판 기본값」 :44 · 「허브 보강 단계 시작」 :45 · 「원장 근거 없는 추가 부위 15」 :48 · 「부위 3단 나머지 확정」 :49 · 「부위 3단 배치 결정(일부)」 :50 · 「허브 부위 3단」 :51 · 「허브 보강한다」 :53 · 「워커 전부 opus」 :55 · 「순서 변경 — ② 명동점 매핑은 새 코디 세션」 :62"
    - "orchestration/work/phub-consult-demo/silver-site-task.md · silver-site-addendum1.md · silver-site-addendum2.md (코디 silver 발주 · 작업 사본 스크립트 수정 허용 범위 · 멈춘 자리 넷 답)"
    - "orchestration/work/phub-consult-demo/silver-site-report.md (silver 작업 결과 — 실측 수 · 해시 · 고친 스크립트 줄 §6 · 확인 필요 §7)"
  sources:
    - "orchestration/work/phub-consult-demo/research-site-tree.md (트리 §1 :20-60 · 이동 48 §2 · 다른 이름 §3-1 · 거미스마일 :138 · 정할 것 T-5 · T-7 :260-262)"
    - "orchestration/work/phub-consult-demo/research-kos-site-3tier.md (한눈 표 :10-18 · 새 부위 자리 :77 · :88 · :89 · :98 · 기준과 다르게 처리한 것 §3 :281-292)"
    - "orchestration/work/phub-consult-demo/research-site-evidence.md (한눈 표 :13-25 — 원장 근거 · anatomy)"
    - "reference/2026-11-19-myeongdong-kos/hub-site-tree-draft.csv (113 줄 — 미추적 · 읽기만)"
    - "orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-003-hub-gold-db.md (§2-5 빌드 기록 · §11-4 갱신 · 끄기)"
    - "orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-001-hub-gold-mcp.md (HG3-2 · HG3-5 — concern_candidates 의 site · 부위 계층으로 넓히지 않음)"
    - "(프로필 레포 main 체크아웃) orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/ (원본 · 읽기만 — silver/ 59 · gold/{gold-build,gold-check,silver-supplement}.py · drafts/silver-check/{silver-check.py,silver-schema.json} · notes/)"
    - "PROCEDURE-HUB 워크트리 phub-consult-demo (HEAD aa46a86) — data/medallion/README.md · backend/app/modules/gold/{headers,inputs,db_inputs,concern,cursor,resolve,medallion_load,memory}.py"
    - "clinic_chat 워크트리 phub-consult-demo — clinic_chat/consult/turn.py · clients/hub_rest.py"
  related:
    - "orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-003-hub-gold-db.md"
    - "orchestration/work/_archive/procedure-hub/phub-gold-jev/SPEC-007-image-data.md"
---

# SPEC-009 — 허브 부위 보강(명동점)

경로 접두어: `$W` = 이 폴더 · `$S` = **작업 사본** `$W/silver-model/`(gitignore `.gitignore:161` · silver 를 여기서 고친다) · `$SM` = 원본 `(프로필 레포 main 체크아웃) orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(**읽기만** — 이 문서의 스크립트 `파일:줄` 은 원본 = 작업 사본 수정 전 기준) · `$R` = `reference/2026-11-19-myeongdong-kos`(미추적 · 읽기만) · `$H` = PROCEDURE-HUB 워크트리 `phub-consult-demo` · `$A` = clinic_chat 워크트리 `phub-consult-demo` · `$P` = `orchestration/work/_archive/procedure-hub/phub-gold-jev`.
「_R「…」」 = `$W/_RESUME.md` §2 의 **그 글로 시작하는 결정 행**(새 결정이 맨 위에 들어와 줄 번호가 판마다 밀리므로 행 첫 글을 키로 쓴다 · 0.2.2 기준 줄은 부록 A) · 「리포트」 = `$W/silver-site-report.md`(silver 작업 결과 · 이 판의 수 · 사실은 이 리포트 실측으로 맞춘다) · 「배치안」 = `$W/research-site-tree.md` + `$R/hub-site-tree-draft.csv` · 「3단 조사」 = `$W/research-kos-site-3tier.md` · 「재셈」 = 이 워커가 파일을 읽어 다시 센 값(부록 B).
이 문서에는 표 · 칸 이름 · 코드 꼴 · 셈만 있다 — 가격 · KOS id · 진료항목 코드 · 병원 이름 · 키 · 개인정보는 없다.

## 0. 범위

### 0-1. 요약

| 무엇 | 이 스펙이 정하는 것 |
|---|---|
| 목표 | 사용자가 정한 **허브 부위 3단 · 새 부위 · 다른 이름**을 작업 사본 silver `site` · `alias` · `anatomy_site` · `source_ref` 에 싣고 **gold 빌드 · gold-check 까지** 가는 꼴 · 규칙 · 시험 |
| 근거 | 원장 근거가 없는 부위 사실은 로컬 근거 파일 `drafts/clinic-supplement/clinic-a-20261119/user.csv` 한 줄을 가리키는 `ref`(외부 조사 전례) · 근거 종류 = **사용자 제공**(새 값 없음)(§2) |
| 부위 3단 | `site.parent_code` 재배치(배치안 이동 48 + 3단 밖 21 = 실물 69) · 새 부위 24 + 새 2단 2(귀 · 기타) = 새 site 26 · 다른 이름 12 · 묶음 부위 6 · 몸 > 기타. **「눈」 합침은 이번 판에 하지 않는다**(§3-5) |
| 영향 | 허브 · gold 는 부위 계층을 **읽지 않는다** — 그래도 근거 줄 · 새 입구 때문에 `gold_hash` 가 바뀐다(§4) |
| 반영 절차 | silver 수정 → silver 검사 → gold 빌드 → gold-check → 허브 레포 `data/medallion/` 교체 · 해시 → (stg 반입 = 절차만)(§5) |
| 깨지는 자리 | 원본 검사 스크립트는 **원장 경로 · 근거 종류 식 · D3 · G1 · G3 · A1 · A3 · A2** 때문에 패치와 상관없이 · 또는 패치 때문에 멈춘다 → **작업 사본 스크립트에 한해** 고쳤다(§3-4 · G-11 · G-13 · 리포트 §6) |
| 이번 판 끝 | **gold 빌드 · gold-check PASS 까지**(_R「허브 보강 단계 시작」) — **끝났다**(_R「silver 패치 1차 끝」 · 리포트 §3: silver-check PASS (WARN 5) · gold-check PASS(FAIL 0 · WARN 10) · `gold_hash` `ece5d2be…` · `aux_hash` `e0813c0a…`). 허브 레포 교체는 절차를 적고 WORK 가 한다 · stg 반입은 다음 단계 |
| 허브 계약 | **바뀌지 않는다** — 표 · 칸을 더하지 않으므로 silver 59 · 헤더 · gold 헤더 그대로(F-14). 마이그레이션 0 |

### 0-2. 사용자가 실물(상담 앱 · 허브 응답)에서 만날 자리

| 바뀜 | 이 판으로 보이는 것 | 자리 |
|---|---|---|
| 부위 3단(계층) | **앱에서 보이는 변화 0.** 허브 · gold 가 site 계층을 읽지 않는다(F-11 · F-12). 결정 「조회는 위 → 아래」(_R「허브 부위 3단」)는 **이 판으로는 생기지 않는다** — 정한 3단은 silver 에만 있고 앱에는 안 보인다. 보고 때 이 점을 먼저 말한다 | §4 · Q-7 |
| 새 부위 | 허브 `resolve` 후보가 는다. 새 site 이름 가운데 **넷이 두 갈래로 갈린다** — 「기타」(이미 고민 CON-278) · 「승모근」(해부 ANA-064 + 오퍼 OFR-0009) · 「침샘」(ANA-075) · 「쇄골」(ANA-106) → `ambiguous`. 새 다른 이름 12 는 겹침 0 | F-21 · §4 |
| 「눈」 | **이번 판에 「눈 → 눈 주변」 이 들어가지 않는다** — 정해진 배치 하나가 빠진다(_R「SPEC-009 범위 = 부위만」 기본값). 「눈」 으로 물으면 지금처럼 SITE-018 | §3-5 |
| 근거 표지 | 사용자 결정 · KOS 진료항목명 근거는 gold 에서 「사용자 제공」 으로 실린다(원장으로 실리면 안 됨 — §3-4). 원장 근거가 없는 새 부위 17 의 입구 = 「사용자 제공」 | §2 · 리포트 §4 |
| **원장 별칭 25 의 표지** | **이동한 부위의 기존 별칭 25(팔자 · 비순구 · 법령선 · 경부 · 하지 · 두부 · 대퇴부 · 배 …) 와 SITE-120 마리오네트라인 이름 입구 1 의 표지가 「원장」 → 「원장 + 사용자 제공」 으로 바뀐다.** 상담 앱은 `evidence_kind` 를 `basis` 로 LLM 에 싣는다 — 원장에서 온 별칭이 「원장 + 사용자 제공」 표지로 실린다. 이번 판은 받아들임(G-13) | F-17 · `$A/clinic_chat/walk/material.py:97-98` · 리포트 §4 · §5-4 |
| `gold_hash` 바뀜 | 허브에 새 판이 뜨면 열린 대화가 다음 턴에 `build_changed` 로 끝난다 — **계층만 바꾼 판도 지금 데이터로는 `gold_hash` 가 바뀐다**(자기 근거 없는 입구 26 — T3-1) | §6-2 |
| 이번 판 끝(gold 빌드까지) | 허브 레포 교체 · 적재 전이므로 **이 판이 끝나도 앱 · stg 는 그대로** | §5 |

### 0-3. 정해진 것(다시 묻지 않는다)

| # | 정해진 것 | 근거 | 이 문서에서 |
|---|---|---|---|
| G-1 | 허브 보강 단계 — 스펙 → silver 수정 → gold 빌드까지 · stg 반입은 다음 | _R「허브 보강 단계 시작」 | §0-1 · §5 |
| G-2 | **SPEC-009 범위 = 부위만**(제품 · 시술 · 적용 부위 범위 빼냄) · **silver 바로 고침**(작업 사본 `silver-model/` · gitignore) | _R「SPEC-009 범위 = 부위만」 | §0-4 · 부록 C · §5 |
| G-3 | 이번 판 기본값(같은 행): ① **「눈」 합침 안 함** ② **침샘 · 쇄골 · 승모근 = site + `anatomy_site`** ③ **다른 이름은 허브 부위 다른 이름만** — 거미스마일 · 러브핸들 · 측두근 제외 ④ 원장 근거 없는 부위 근거 = **로컬 `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`** · 병원 이름 · 코드 공개 0 | _R「SPEC-009 범위 = 부위만」 | §2 · §3-2 · §3-3 · §3-5 |
| G-4 | **허브를 보강한다** — 10-30 「허브는 병원 데이터로 안 바뀐다」 를 이번에 넘어선다 | _R「허브 보강한다」 | §2 |
| G-5 | **허브 부위 3단** — 1단 얼굴 / 몸(전신) → 2단 큰 부위 → 3단 상세 · 조회는 위 → 아래 · 「바디」 · 「페이스」 = 메뉴 분류 말 · 정규화 판정 = 허브에 있음 / 다른 이름 추가 / 상세 부위 추가 / 새 부위 | _R「허브 부위 3단」 · _R「원장 근거 없는 추가 부위 15」 | §3 |
| G-6 | 배치 확정분: 머리(두피 · 정수리) · 귀(이개 · 이주 · 이하부 · 귀밑샘) = 얼굴 2단 · 턱밑샘 = 턱 아래 · 팔자주름 → 볼 3단 · 마리오네트라인 → 입 3단 | _R「부위 3단 배치 결정(일부)」 | §3-2 |
| G-7 | 배치 확정분: 헤어라인 → 머리(두피) 3단 · 잇몸 · 구강 → 입 3단 · 비강 · 부비동 → 코 3단 · 눈 → 「눈 주변」 다른 이름(이번 판은 G-3 ① 로 안 함) · 구레나룻 → 볼 3단 · 수염 → 턱 3단 · 하안면 · 중안면 = 얼굴 2단 묶음(하관 = 하안면) · 사지 · 상체 · 체간 · 코안면 = 묶음 부위로 남김 · 관절 → 몸 > 기타 | _R「부위 3단 나머지 확정」 | §3-2 |
| G-8 | **원장 근거 없는 추가 부위 15 도 3단에 넣는다** · 거미스마일 = 잇몸(진료항목 부위 판정) | _R「원장 근거 없는 추가 부위 15」 | §2 · §3-2 |
| G-9 | 진료항목 → 허브 부위 연결(매핑 표)은 **새 코디 세션** — 이 스펙은 허브 쪽 부위만 | _R「순서 변경」(② 명동점 매핑은 새 코디 세션) | §0-4 |
| G-10 | 일하는 방식 — 워커 opus · 단계 끝나면 자동 검수 · 발주 전 사용자 승인 · 시험은 WP 파일만 · stg 는 코디가 bastion 경유 직접 | _R「워커 전부 opus」 | §5 |
| G-11 | **작업 사본 검사 · 빌드 스크립트에 한해** 고쳐도 되는 것(실제로 고친 범위 = 리포트 §6 diff 전부): ① 추가 지시 1 — `silver-check.py` 원장 · step1 경로(`PHUB_REC`) · `resolve` 의 `drafts/clinic-supplement/` 갈래(`L<줄>` · `status = 확인` 줄만) · `ref_kind` · D3(`anatomy_site` 로 이어진 같은 이름 짝 허용) · `gold-build.py` · `gold-check.py` `ev_kind`(`drafts/clinic-supplement/` → 사용자 제공) · `gold-check.py` G1 경로 ② 추가 지시 2 — `silver-check.py` **G3**(원본 `silver-check.py:973-977` 의 옛 경로 `phub-ledger-redesign/` → `phub-consult-demo/` · 작업 사본 밖 변경 = WARN) · `gold-check.py` **A1 다시 씀**(G-14) · **A3**(G-14) · **A2**(silver-check 끝 줄이 「PASS (WARN n)」 이고 WARN 이 전부 G3 이면 통과 · 그 줄을 WARN 으로 옮겨 적음) · G1 = WARN · WARN 출력 줄 · `build_site_3tier.py` 의 `<기준> <폴더>` 인자(A3 재현 대조용). **원본은 금지 · 그 밖 검사 실패는 고치지 말고 멈춰서 질문** | _R「코디 기본값(사용자 확인 대기)」 · _R「silver 패치 1차 끝」 · `silver-site-addendum1.md` §2 · `silver-site-addendum2.md` · 리포트 §6-1 · §6-2 | §3-4 |
| G-12 | 허브 데이터는 **원천에서 다시 지어 통째로** 바꾼다 · 손으로 고치지 않는다 · 판은 한 벌 · 옛 판은 git 이력 | `$H/data/medallion/README.md:4` · `:27` | §5-3 · §6-3 |
| G-13 | **근거 종류 섞임 받아들임(이번 판)** — 자기 근거(이름 입구: `field` ∈ {`name_ko`, `name`, 빈칸} / 별칭 입구: `alias`)가 없는 site 입구는 부위 행 근거 전부를 받는다(`gold-build.py:140` · `:147`). 그래서 이동한 부위의 기존 별칭 25 + SITE-120 이름 입구 1 = **26 의 근거 종류가 「원장」 → 「원장 + 사용자 제공」**. gold-build 는 고치지 않는다 | _R「silver 패치 1차 끝」 · `silver-site-addendum2.md` 4 · 리포트 §4 · §5-4 | §0-2 · F-17 · §4 · §6-1 |
| G-14 | **gold-check A1 · A3 · G1 · G3 의 꼴** — A1 = 기준을 **묶음 기준 사본 `archive/silver-before-clinic-a-20261119/silver/`**(패치 전 silver · 원본 아카이브 silver 와 바이트 같음)로 · 허용 = site 기존 행은 `parent_code` 칸과 「묶음 부위」 로 시작하는 `description` 만 · 새 행은 끝 덧붙임 / `alias` · `anatomy_site` = 기준 바이트 + 끝 덧붙임 / `source_ref` = 기준 바이트 + 끝 덧붙임(`ref` 머리 `drafts/clinic-supplement/` 또는 대상이 새 site · `anatomy_site` 행) / 그 밖 표 바이트 · 표 목록 · `external_code` · `drafts/gold` 그대로. A3 = 기준 사본에서 `silver-supplement.py` 재현 위에 `build_site_3tier.py <기준> <폴더>` 재현을 겹쳐 7 파일 + `user.csv` 바이트 대조. G1 · G3 = 경로를 `phub-consult-demo/` 로 · **작업 사본(`silver-model/`) 밖 변경은 WARN 으로만**(코디 변경 — 데이터 아님) | _R「silver 패치 1차 끝」 · `silver-site-addendum2.md` 1 ~ 3 · 리포트 §5 · §6-2 | §3-4 · §5-2 · T3-5 |

### 0-3a. 코디 기본값 — 사용자 확인 대기

`_RESUME` 에 「코디 기본값(사용자 확인 대기)」 로 적힌 것. silver 발주는 이 값으로 진행하고, 사용자가 다르게 정하면 WORK 에서 바꾼다(결정이 아니라 기본값 — 보고 때 확인받는다).

| # | 기본값 | 근거 |
|---|---|---|
| D-1 | 새 부위 넷의 자리 — **침샘 → 얼굴 > 턱 · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목**(배치안은 2단을 비운 「자리 후보」 였다 — `hub-site-tree-draft.csv:109-112`) | 3단 조사 :77 · :88 · :89 · :98 · _R「코디 기본값(사용자 확인 대기)」 |
| D-2 | 근거 종류 — `drafts/clinic-supplement/` 머리 = 기존 「사용자 제공」 · **새 값 만들지 않음**(순서 목록 그대로) | 같은 행 · `silver-site-addendum1.md` §2 |
| D-3 | D3 — `anatomy_site` 로 이어진 같은 이름 짝(침샘 · 쇄골 · 승모근)은 허용 | 같은 행 |
| D-4 | 별칭 「애교 → 애교살」 은 넣지 않음(이미 있음 — `alias.csv:308`) · 「상완」 · 「하관전체」 는 배치안 글자 그대로 | 같은 행 · `silver-site-addendum1.md` §1 |
| D-5 | 사지 · 상체 · 체간 · 코안면의 2단 자리 · 묶음 부위 표현 = 부위 행 + `description` 「묶음 부위(3단 조사 처리)」 — 사용자 결정이 아니라 **3단 조사의 처리**(「기준에 단이 없었다 … 두었다」) | 3단 조사 :285 · `silver-site-addendum1.md` §3 |

### 0-4. 범위 · 범위 밖

| 이 스펙에서 정한다 | 범위 밖 |
|---|---|
| 부위 근거 꼴(§2) | 진료항목 → 허브 부위 매핑 표(G-9) |
| `site` · `alias` · `anatomy_site` · `source_ref` 의 바뀜 꼴 · 새 검사(§3) | 부위 없는 145 줄의 부위 채우기(_R「부위 3단 나머지 확정」 「남은 것」 — 진료항목 쪽 일) |
| 허브 동작 영향 · 전후 비교 · gold-build / gold-check · silver-check 깨지는 자리(§3-4 · §4) | 허브 도구가 부위 계층을 읽는 코드(Q-7) |
| 반영 절차 · 허브 레포 교체 · stg 절차(§5) | stg 반입 실행 · 「눈」 합침(다음 판) |
| 해시 영향 · 되돌리기(§6) | 결정 · 조사 전 항목 — 부록 C |

## 1. 현재 사실

| # | 사실 | 자리 · 셈 |
|---|---|---|
| F-1 | silver 59 CSV · 허브 레포 `data/medallion/silver/` 와 **바이트가 같다** · gold 16 파일 sha256 도 같다 | 재셈 ① |
| F-2 | `site` 89 행 · 최상위(`parent_code` 빈칸) **68** · `parent_code` 뜻 = 「상위 행(같은 표) — **원장이 포함 관계로 적은 것만**」 | 재셈 ② · `$SM/drafts/silver-check/silver-schema.json` `tables.site.columns[parent_code].meaning` |
| F-3 | 1단 자리 — `SITE-001` 전신(별칭 「바디」 · 「Body」) · `SITE-007` 얼굴(별칭 「얼굴 전체」 · 「안면」 등 · 설명 빈칸) | `$SM/silver/site.csv:2` · `:6` · `alias.csv:301-302` · `:330-332` · `:362-363` |
| F-4 | `alias` 980 행 · site 대상 59 · `kind` 6 값(별칭 762 · 의학 용어 76 · 약어 62 · 다른 이름 46 · 원장 항목 이름 27 · 영어 7) | 재셈 ② |
| F-5 | `source_ref` 48,113 행 · 꼴 `target_table,target_id,field,ref` · 원장 JSON 포인터 대부분 · 외부 조사 전례 `drafts/external-research/external-research.csv:L<줄>` 174 · **「사용자…」 0 · `drafts/clinic-supplement/` 0** | 재셈 ③ · `silver-schema.json` `tables.source_ref` |
| F-6 | 근거 종류 3 값 — `원장` · `외부 확인` · `사용자 제공` · **`ref` 머리 글자로 정한다**(`사용자` 로 시작 → 사용자 제공 · `http(s)` · `step1-products.json:` · `drafts/external-research/` · `notes/product-research.csv:` · `:` 없음 → 외부 확인 · **그 밖 원장**). 같은 식이 **세 곳** — `gold-build.py:50-57` · `gold-check.py:173-178` · `silver-check.py:128-134`. 순서 목록 두 곳 — `gold-build.py:100-101` · `gold-check.py:170`. → 지금 식으로는 `drafts/clinic-supplement/…/user.csv:L<줄>` 이 **「원장」** 으로 분류된다 | `$SM/gold/` · `drafts/silver-check/` |
| F-7 | 근거 포인터는 **풀려야 한다** — `resolve` 가 파일별로 읽어 글을 돌려준다 · 원장으로 분류된 ref 는 원장 폴더에서 파일을 찾고 없으면 `KeyError`(`:114-115`) → S1 「근거 포인터가 원장 · 출처에 없음」 FAIL(`:343-345`). `drafts/clinic-supplement/` 갈래는 **없다** | `silver-check.py:77-127` · `:96-97` |
| F-8 | **silver-check 의 원장 · step1 경로가 낡았다** — `WORK` = 위로 올라가며 찾은 `orchestration/work` · `LEDGER = WORK/phub-recommend/bronze/phub-ledger` · `STEP1 = WORK/phub-recommend/step1-products.json`(주석 「원장은 열린 작업 work/phub-recommend/bronze/ 에 있다」). 지금 `phub-recommend` 는 `orchestration/work/_archive/procedure-hub/phub-recommend/` 에만 있다(원본 쪽 프로필 main 체크아웃 · 작업 사본 쪽 이 워크트리 둘 다) → 원장 근거 대부분이 F-7 의 S1 FAIL — **부위 패치와 상관없이 silver 검사가 깨진다** | `silver-check.py:28-37` · 재검수 r3 R3 |
| F-9 | 부위에 걸리는 검사 — 사전 행 근거 D4(`:482-488`) · 별칭 A1 ~ A8(A1 중복 `:499-502` · A3 같은 표 다른 행 이름 `:515-516` · A5 별칭 글자가 근거에 있음) · D1 순환 · **site 깊이 검사 없음**(D1 깊이 ≤ 3 은 `level` 칸 있는 표만 — `:442-471`) | `silver-check.py` |
| F-10 | **D3** = site ∪ anatomy 의 `name_ko` **글자** 겹침(접두어가 다른 행끼리) → FAIL — `anatomy_site` 연결은 보지 않는다. 배치안 추가 24 에서 걸리는 것 = **침샘(ANA-075) · 쇄골(ANA-106) · 승모근(ANA-064)** 셋 · 귀밑샘 · 턱밑샘은 안 걸린다(anatomy 는 「이하선」 ANA-076 · 「침샘」 — 뜻만 겹침) | `silver-check.py:543-550` · `$SM/silver/anatomy.csv` · `$R/hub-site-tree-draft.csv:108` · `:111-114` |
| F-11 | **gold-build 는 `site.parent_code` 를 읽지 않는다** — `parent_code` 를 쓰는 곳은 제품 · 고민 · 부작용 · 조건뿐(`:218-222` · `:324` · `:405-406` · `:734` · `:860`). site 는 이름(`name('site', …)`)과 입구(`g_entry`)로만 나간다 | `$SM/gold/gold-build.py`(grep) |
| F-12 | **허브도 부위 계층을 읽지 않는다** — 보조 계층 3표 = `concern` · `adverse` · `condition` · `concern_candidates` 의 `site` 는 「부위 계층으로는 넓히지 않는다」 · 부위는 site 입구 `entity_name` 글자 일치 | `$H/backend/app/modules/gold/headers.py:67` · `db_inputs.py:6-7` · `concern.py:11` · `:183-185` · `$P/SPEC-001-hub-gold-mcp.md` HG3-2 · HG3-5 |
| F-13 | gold-check — **A1** = 기준 사본 `archive/silver-before-gold-final/` 대비 파일마다 허용한 바뀜만: `source_ref.csv` 는 앞쪽 바이트 불변 + 덧붙인 행이 목록(`product_procedure` · `same_day_text` · `concern_site` 8) 안(`:86-92`) · `concern_site.csv` 는 「기준 + 끝 8 줄」 만(`:93-96`) · **그 밖 파일(`site.csv` · `alias.csv` · `anatomy_site.csv` 포함)은 한 바이트라도 바뀌면 FAIL**(`:97-98`). **A3** = `silver-supplement.py` 재현본과 지금 `source_ref.csv` 등을 바이트 대조(`:113-125` — 줄을 더하면 FAIL). **G1** = git status 에서 옛 경로 `orchestration/work/phub-ledger-redesign/` 밖 변경 0(`:426-430`) · **A2** = silver-check 끝 줄이 「PASS (WARN 0)」 여야 한다. silver-check **G3** 도 같은 옛 경로 밖 변경을 FAIL(원본 `silver-check.py:973-977`). (원본 기준 — 작업 사본에서 고친 꼴은 G-14) | `$SM/gold/gold-check.py` · `$SM/drafts/silver-check/silver-check.py` |
| F-14 | 적재기 — 계약 밖 CSV 가 있으면 V3 · 헤더가 다르면 V5 · gold 헤더가 계약과 다르면 허브 시작 실패. **이 판은 표 · 칸을 더하지 않으므로 걸리지 않는다** | `$H/backend/app/modules/gold/medallion_load.py:116-124` · `:139` · `inputs.py:109-114` |
| F-15 | 해시 — `gold_hash` = gold 16 파일 · `aux_hash` = `source_ref` + 보조 5(`concern` · `adverse` · `condition` · `concern_site` · `ledger-check-list`) | `$H/backend/app/modules/gold/inputs.py:129-178` · `$H/data/medallion/README.md:11-14` |
| F-16 | 쪽 넘김 cursor 는 `gold_hash` · `aux_hash` 둘에 묶인다 · 상담 앱은 **턴 사이 `gold_hash` 가 바뀌면** 대화를 `build_changed` 로 맺는다 | `$H/backend/app/modules/gold/cursor.py:1` · `:41` · `$A/clinic_chat/consult/turn.py:133-134` · `:377-379` · `clients/hub_rest.py:162` · `:217` |
| F-17 | g_entry 입구 근거는 **자기 근거**로 고르고 — 이름 입구는 `field` ∈ {`name_ko`, `name`, 빈칸}(`:140`) · 별칭 입구는 `field = alias`(`:147`) — **없으면 그 silver 부위 행 근거 전부** 로 넘어간다. 그래서 위 부위를 옮기거나 묶음 `description` 을 바꿔 그 부위에 `user.csv` 근거 줄이 붙으면, 자기 근거 없는 입구의 `evidence_kind` · g_evidence 가 바뀐다. 이번 판 실측 **26**(원장 → 원장 + 사용자 제공) = 이름 입구 1(SITE-120 마리오네트라인 — source_ref 5 줄이 전부 `description` · `alias`) + 이동한 부위의 기존 별칭 입구 25(`name_kind` 의학 용어 17 · 별칭 8). 지금 site 별칭에 `alias` 근거가 있는 부위는 5 곳(SITE-036 · 070 · 073 · 077 · 120)뿐이다 | `gold-build.py:84-101` · `:140` · `:147` · `$SM/silver/source_ref.csv:22340-22344` · 리포트 §4 · §7 · 검수 r4 R4-1 |
| F-18 | g_entry `gid` 는 **순번**이다 — 표 순서(`ENTRY_T` · site 는 6 번째)대로 이름 행을 센 뒤 별칭 행을 센다 → 앞 표에 행이 늘면 **뒤 gid 가 전부 밀린다** | `gold-build.py:122-147` |
| F-19 | 「눈」 은 이미 **site 행 SITE-018**(설명 빈칸 · 최상위 · 배치안 「3단 밖 · 눈 주변과 합침」). 가리키는 행: `adverse_risk` 23(**실명 22** · 자극감 1) · `concern_site` 1(CSI-0042 = CON-062 눈 꺼짐) · `source_ref` 16(전부 `field` 빈칸 · 원장) · alias 0 · g_entry GEN-00786 | `$SM/silver/site.csv:12-13` · `$R/hub-site-tree-draft.csv:12` · `concern_site.csv:42` · `source_ref.csv:4295-4310` |
| F-20 | `SITE-019` 눈 주변을 가리키는 행: `adverse_risk` 0 · `concern_site` 4 · `offer_site` 4 · `anatomy_site` 8 · `procedure_case` 2 · `outcome` 1 · alias 5 | 재셈 ⑤ |
| F-21 | 허브 `resolve` 는 같은 입구 글자가 다른 (표, 코드)에 닿으면 `ambiguous`. **이번 판에 넣는** 새 site 24 · 다른 이름 12 × 지금 입구(g_entry `norm`) → 겹침 넷 — 「기타」 = concern CON-278 · 「승모근」 = anatomy ANA-064 + offer OFR-0009 · 「침샘」 = ANA-075 · 「쇄골」 = ANA-106. 다른 이름 12 는 겹침 0(거미스마일 · 러브핸들 · 측두근은 G-3 ③ 로 안 넣음). D3 · A3 는 표를 건너는 겹침을 안 본다 | `$H/backend/app/modules/gold/resolve.py:47` · `$H/data/medallion/gold/g_entry.csv` · 재셈 ④ |
| F-22 | 적재 뒤 허브는 `GOLD_EXPECTED_HASH`(env)를 gold 해시와 대조한다(V9) · `health.integrity` = `gold_rows_without_evidence` · `evidence_without_source_ref` 등 | `medallion_load.py:173-175` · `$H/data/medallion/README.md:36` · `:44` · `memory.py:116-131` |
| F-23 | 배치안 113 줄 = 허브 89 + 추가 24(상세 18 · 새 6) · 이동 48(그대로 19) · 3단 밖 22 · 추가 중 원장 근거 0 = 15 · 「다른 이름 추가」 칸이 찬 줄 15(낱말 16 — 「페이스 · 풀페이스」 한 줄) | 배치안 :8-18 · 재셈 ④ |

## 2. 부위 근거 꼴(부위에 한정)

### 2-1. 규칙

| # | 규칙 | 근거 |
|---|---|---|
| E1 | 원장 근거가 없는 부위 사실(새 부위 15 · 새 2단 「귀」 · 「기타」 · 위 부위 이동 · 묶음 부위 `description` · 원장에 없는 다른 이름)은 **근거 파일의 한 줄**로 받친다(다른 이름은 E6 대로 `user.csv` 기록만). `source_ref.ref` = `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`(줄 = 그 파일 줄 · 헤더 = 1줄) — 근거 글은 그 줄에 · `ref` 에는 자리만 | G-3 ④ · 외부 조사 전례 `notes/external-fill-notes.md:4` |
| E2 | 원장 근거가 있는 부위 사실(심부볼 · 승모근 · 허벅지 안 · 밖 · 승마 · 쇄골 · 침샘 · 귀밑샘 · 턱밑샘 — 배치안 「원장 근거」 칸 「있음」)은 **원장 포인터 그대로**(기존 꼴) | 배치안 §3 · `silver-site-task.md` 「새 부위 근거」 |
| E3 | 근거 종류 — `drafts/clinic-supplement/` 머리 → **「사용자 제공」**(있는 값 · 새 값 없음 · 순서 목록 그대로). 종류는 **공개 `ref` 경로 머리**로 정해진다 — 허브 레포 데이터만으로 `evidence_kind` 가 재현된다(지금 꼴 그대로) | G-3 ④ · D-2 · F-6 |
| E4 | 근거 파일 · 묶음 이름 — 묶음 키 = **`clinic-a-20261119`**(병원 이름을 담지 않는다) · 근거 파일은 로컬(작업 사본 · gitignore) · 공개 silver 에는 `ref` 자리만. `resolve` 는 `status = 확인` 줄만 푼다(그 밖이면 S1 FAIL) | G-3 ④ · 리포트 §6-1 `resolve` |
| E5 | 원장 근거 행은 **지우지 않고 바꾸지 않는다** — 근거는 덧붙이기만(이번 판에 예외 없음 — 「눈」 합침을 안 하므로) | `notes/external-fill-notes.md:6` · `:10` · G-3 ① |
| E6 | 「근거 없는 gold 행 0」 은 그대로 — 새 site 행 · 바꾼 `parent_code` · 바꾼 묶음 `description` · 새 `anatomy_site` 행마다 `source_ref` ≥ 1. **새 다른 이름 12 는 `source_ref` 0 — 별칭 입구는 부위 행 근거를 받고(F-17), 별칭 글자의 근거는 `user.csv` 줄(kind 「다른 이름(기록만 · source_ref 없음)」)에 기록만 한다.** `source_ref` 는 (부위, 칸) 단위라 별칭 낱말 하나를 가리킬 수 없고, `(site, code, alias)` 를 달면 그 부위의 기존 별칭 입구 17 의 근거까지 사용자 근거로 바뀌기 때문이다. A5(별칭 글자가 근거에 있음)는 site 표에 걸리지 않는다(`silver-check.py:170` `COVER['A5'] = {'procedure'}`). **이 꼴은 silver 워커 판단 — 확인 대기(Q-8)** | F-9 · `gold-check.py:195-230`(K2 · K3) · 리포트 §7 · 검수 r4 W1 |
| E7 | 원장 · 진료항목 CSV · 원본 silver-model 은 **읽기만**. 근거 파일은 silver 수정 단계(§5)가 짓는 산출물 | G-12 · G-2 |

### 2-2. 근거 파일 꼴 — `user.csv`

silver 워커가 지은 실물 꼴(리포트 §2) — 칸 `line,kind,target_table,target_code,name,field,decision,basis,status` · 113 줄(+헤더).

| 칸 | 값 | 뜻 |
|---|---|---|
| `line` | 줄 번호(헤더 = 1줄) | `source_ref.ref` 의 `L<줄>` 과 같은 값 |
| `kind` | 위치 이동 69 · 새 부위 자리 9 · 새 부위(원장 근거 없음) 15 · 새 2단 2 · 묶음 부위 6 · 다른 이름(기록만 · source_ref 없음) 12 | 이 줄이 받치는 바뀜의 갈래 |
| `target_table` · `target_code` · `field` | `site` · `alias` · 코드 · 칸(빈칸 17 = 행 전체 · `parent_code` 78 · `description` 6 · `alias` 12) | 이 줄이 받치는 silver 자리(`alias` 12 줄은 `source_ref` 가 가리키지 않는 기록만 — E6) |
| `name` | 부위 이름 · 다른 이름 글자 | 받치는 값 |
| `decision` | 글자(예 「위 부위 최상위 → 전신」) | 바뀜 요약 — **silver 워커가 요약한 글**(결정 행 글자 그대로가 아님) |
| `basis` | 모든 줄 같은 글 「사용자 결정 2026-11-19 · 명동점 KOS 진료항목명」 | 근거 글 · 로컬 파일에만(공개 silver grep 0) |
| `status` | 모두 「확인」 | `resolve` 가 푸는 줄 표지(E4) |

- `resolve` 는 `name + decision + basis` 를 근거 글로 돌려준다(리포트 §6-1).
- **`decision` 이 `_RESUME` 의 어느 결정 행에서 왔는지 담는 칸은 없다** — 0.2.1 의 「`quote` 가 결정 행 한 줄에 들어 있음」 시험(옛 T1-2)은 이 꼴로 돌 수 없어 뺐다. 추적 칸을 둘지는 Q-9.
- **넣지 않는 것**: 진료항목 코드 · 가격 · KOS id(uuid) · 키 · 토큰 · 사람 이름 · 연락처(G-3 ④). 병원 이름은 로컬 `basis` 칸에만 있고 공개 silver 에는 0.
- 자리 = `$S/drafts/clinic-supplement/clinic-a-20261119/user.csv`(작업 사본 · gitignore) · 짓는 스크립트 = 같은 폴더 `build_site_3tier.py`(기준 사본에서 네 파일 + `user.csv` 를 다시 씀 · 다시 돌려도 같은 바이트).

### 2-3. 고칠 자리(작업 사본 스크립트 — G-11)

| 자리 | 고칠 것 | 근거 |
|---|---|---|
| `silver-check.py` `resolve` | `drafts/clinic-supplement/<묶음>/user.csv` 갈래 — `L<줄>` 을 풀어 근거 글(`name + decision + basis`)을 돌려준다(없는 줄 · `status ≠ 확인` 이면 S1 FAIL) — **고쳤다**(리포트 §6-1) | F-7 · 외부 조사 갈래 `:89-97` 와 같은 꼴 |
| `silver-check.py:128-134` · `gold-build.py:50-57` · `gold-check.py:173-178` | 세 곳 **같은 식** `ref.startswith(('사용자', 'drafts/clinic-supplement/'))` → `사용자 제공` 을 「원장」 판정보다 먼저(K2 · K3 이 세 함수를 대조) — **고쳤다**(리포트 §6-1) | F-6 · D-2 |
| 순서 목록(`gold-build.py:100-101` · `gold-check.py:170`) · `notes/vocabulary.csv` | **바꾸지 않는다** — 새 값이 없다 | D-2 |

### 2-4. 예

```text
# $S/drafts/clinic-supplement/clinic-a-20261119/user.csv (로컬 · 줄 2)
2,위치 이동,site,SITE-003,사지,parent_code,위 부위 최상위 → 전신,사용자 결정 2026-11-19 · 명동점 KOS 진료항목명,확인

# silver source_ref.csv 에 덧붙는 줄(공개 · 병원 이름 없음)
site,SITE-003,parent_code,drafts/clinic-supplement/clinic-a-20261119/user.csv:L2
```

### 2-5. 시험

| # | 시험 | 기대 |
|---|---|---|
| T1-1 | 새 갈래 `ref` 전부 풀림(S1) · 없는 줄을 가리키는 깨뜨린 사본은 S1 FAIL(부정 시험 — `silver-check.py:1313-1358` 전례) | FAIL 0 · 부정 시험 FAIL 1 |
| T1-2 | `user.csv` 줄마다 `status = 확인` · `source_ref` 가 가리키는 `L<줄>` 이 모두 있음 · `kind` 「다른 이름(기록만)」 줄을 가리키는 `source_ref` 0 | 어긋남 0(옛 「`quote` ⊂ 결정 행」 시험은 §2-2 꼴로 돌 수 없어 뺌 — Q-9) |
| T1-3 | 세 함수의 근거 종류가 같은 `ref` 전부에서 같은 값 · `drafts/clinic-supplement/` = 사용자 제공 | 어긋남 0(K3) · 「원장」 0 |
| T1-4 | 이 묶음이 더하거나 바꾼 silver 행에서 uuid 꼴 · 가격 꼴 · 진료항목 코드 꼴 · 병원 이름 grep | 0 |
| T1-5 | gold K2 · K3 · gold-build 끝까지 | FAIL 0 · `evidence_kind` ⊆ 근거 종류 3 값 |

## 3. 부위 3단

### 3-1. 규칙

| # | 규칙 | 근거 |
|---|---|---|
| T1 | 1단은 **둘** — `SITE-007` 얼굴 · `SITE-001` 전신(몸). 1단 행의 `parent_code` = 빈칸 | G-5 · F-3 |
| T2 | 깊이 ≤ **3**. 3단의 하위는 같은 2단 아래 3단에 나란히 | G-5 · 배치안 §1 |
| T3 | 1단 아닌 부위는 `parent_code` 가 있다 — 3단 밖 22 는 배치가 끝나면 **1**(SITE-018 「눈」 — §3-5 · S-1 예외 1) | 배치안 :12 · G-3 ① |
| T4 | 묶음 부위(하안면 · 중안면 = 얼굴 2단 묶음 — 결정 · 코안면 = 얼굴 2단 · 사지 · 상체 · 체간 = 몸 2단 — 3단 조사 처리)는 **부위 행 그대로** 두고 `description` 을 「묶음 부위」 로 시작하는 글로 바꾼다(기존 6 행 — 사지 · 상체 · 체간 · 코안면 「묶음 부위(3단 조사 처리).」 · 중안면 「묶음 부위(얼굴 가운데).」 · 하안면 「묶음 부위(하관).」 — 리포트 §2). 칸을 더하지 않는다(F-14) | G-7 · D-5 · Q-3 |
| T5 | 몸 > **기타**(새 2단) > 관절 | G-7 · 3단 조사 §3 :286 |
| T6 | 「바디」 · 「페이스」 는 새 별칭으로 넣지 않는다(「바디」 는 이미 전신 별칭 — F-3 · 배치안 「얼굴 ← 페이스 · 풀페이스」 의 「페이스」 도 넣지 않음) | G-5 |
| T7 | 새 부위 · 다른 이름은 정규화 판정 넷 중 하나로만 들어온다 | G-5 |
| T8 | `parent_code` 뜻을 「원장 포함 관계 또는 사용자 배치(근거 = `source_ref` field `parent_code`)」 로 바꾼다 — 스키마 글 · `notes/silver-erd.md` · `silver-tables.md` 는 `--write-docs` 로 다시 쓴다(**Q-2**) | F-2 · SPEC-007 §4 「`--write-docs`」 |
| T9 | 위 부위를 바꾼 행마다 근거 줄 하나(`field = parent_code` · 원장 포함 관계가 없으면 `user.csv` 줄) | E1 · E6 |

### 3-2. 바뀌는 것

| 무엇 | 입력 | 꼴 |
|---|---|---|
| 기존 89 행의 `parent_code` | 배치안 이동 48 + G-6 · G-7 확정 변경(3단 조사 §3 :281-292 가 적용한 표) — 실물 **69 행**(이동 48 + 3단 밖 21 이 자리를 잡음) · SITE-018 「눈」 은 **그대로**(G-3 ①) | `site.csv` 의 그 칸 |
| 기존 묶음 부위 6 행의 `description` | T4 | `site.csv` 의 그 칸 — 「묶음 부위」 로 시작(기존 행 바뀜의 **두 번째 예외**) |
| 새 2단 | 귀 SITE-121 · 기타 SITE-122(머리는 기존 행을 2단으로) | 새 행 — 끝에 덧붙임 |
| 새 3단 · 새 부위 24(SITE-123 ~ 146) | 배치안 상세 18(자리 = 배치안) · 새 6 — 귀밑샘 → 귀 아래 · 턱밑샘 → 턱 아래(G-6) · **침샘 → 얼굴 > 턱 · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목(D-1 · 사용자 확인 대기)**. 원장 근거 없는 15 포함(G-8) | 새 행 · 근거 = 원장 포인터(E2) 또는 `user.csv` 줄(E1) |
| `anatomy_site` | 침샘 → ANA-075 · 쇄골 → ANA-106 · 승모근 → ANA-064(G-3 ②) | 새 행 3 · 기존 꼴 · 행 근거 ≥ 1 |
| 다른 이름 **12** | 배치안 「다른 이름 추가」 16 낱말 가운데 허브 부위 다른 이름만(G-3 ③): 풀페이스 → 얼굴 · 하관전체 → 하안면 · 아이 → 눈 주변 · 눈썹뼈 → 안와상부 · 콧볼 → 비익 · 양볼 → 볼 · 입술위 → 윗입술 · 넥 → 목 · 구렛나루 → 구레나룻 · 겨 → 겨드랑이 · 상완 → 팔뚝 · 힙 → 엉덩이. 뺀 것: 페이스(T6) · 거미스마일 · 러브핸들 · 측두근(G-3 ③) · 「애교」(이미 있음 — D-4 · 배치안에 없는 낱말) | `alias` 새 행 — `kind` 는 지금 값 6 가운데 · 글자는 배치안 글자 그대로(A5 — `quote` 에 그 글자) · 12 낱말 모두 지금 alias · site 이름과 겹침 0(재셈 ④) |

- 실측(리포트 §2): site 89 → **115**(+26) · 깊이 1단 3(전신 · 얼굴 · 눈) · 2단 30 · 3단 82 · 깊이 4 이상 0 · `alias` 980 → **992**(+12) · `anatomy_site` 89 → **92**(+3 · ANS-0090 ~ 0092) · `source_ref` 48,113 → **48,226**(+113 끝 덧붙임 = `user.csv` 근거 101 · 원장 포인터 12).
- 새 행 `description` 은 근거 글이 있을 때만(site 는 설명 빈칸 검사 대상 아님 — F-9) · 묶음 부위는 T4.

### 3-3. 걸리는 검사

| 검사 | 걸리는 자리 | 처리 |
|---|---|---|
| **D3** | 침샘 · 쇄골 · 승모근(F-10) — site 를 만들고 `anatomy_site` 로 잇지만(G-3 ②) 이름이 그대로라 원본 D3 는 **FAIL** | 작업 사본 D3 를 「`anatomy_site` 로 이어진 같은 이름 짝은 허용」 으로(D-3 · G-11) |
| A1 · A3 · A5 | 새 다른 이름 12 | 중복 0 · 같은 표 다른 행 이름 0(재셈 ④) · A5 는 site 표에 걸리지 않는다(`silver-check.py:170` `COVER['A5'] = {'procedure'}`) — 별칭 글자 근거는 `user.csv` 기록만(E6 · Q-8) |
| D4 · D1 | 새 site · `anatomy_site` 행 · `parent_code` 순환 | 행 근거 ≥ 1 · 순환 0 |
| **새 S-1** | site 깊이 ≤ 3 · 1단 = 얼굴 / 전신 둘 · 1단 아닌데 부모 없음 = **SITE-018 1 뿐**(예외 목록) | FAIL — 지금 site 깊이 검사 없음(F-9) · **아직 안 넣음**(W-2). 이번 판 실측은 리포트 §2(깊이 4 이상 0 · 최상위 = 전신 · 얼굴 · 눈) |
| **새 S-2** | 위 부위를 바꾼 행 = `field = parent_code` 근거 ≥ 1 | FAIL · **아직 안 넣음**(W-2). 이번 판 실측 = 이동 69 + 원장 근거 새 부위 9 = `parent_code` 근거 78 |
| (검사 없음) 표를 건너는 입구 겹침 | 기타 · 승모근 · 침샘 · 쇄골(F-21) | 시험 T3-6 으로 목록을 남긴다 |

### 3-4. 깨지는 자리 — 검사 · 빌드 스크립트

| 자리 | 왜 깨지나 | 처리 |
|---|---|---|
| **silver-check 원장 · step1 경로**(`silver-check.py:28-37`) | `orchestration/work/phub-recommend/…` 는 없다 — 지금은 `orchestration/work/_archive/procedure-hub/phub-recommend/…`(F-8) → 원장 근거 대부분 S1 FAIL · **패치와 상관없이** P5 가 닿을 수 없다 | 작업 사본에 한해 이 워크트리에 실제로 있는 경로(`PHUB_REC = WORK/_archive/procedure-hub/phub-recommend`)로 — **고쳤다**(G-11 · 리포트 §6-1) · S1 통과(user.csv 101 줄 풀림) |
| **근거 종류 식 · `resolve`** | `drafts/clinic-supplement/…:L<줄>` 이 지금 식으로는 「원장」(F-6) → `resolve` 가 원장 폴더에서 찾다 `KeyError` → S1 FAIL. 멈추지 않고 gold 까지 가면 **사용자 결정이 「원장」 표지로 앱에 실린다** | §2-3 — 세 곳 같은 식 + `resolve` 갈래 — **고쳤다**(G-11 · D-2 · 리포트 §6-1) |
| **D3** | §3-3 | 작업 사본 D3 수정 — **고쳤다**(G-11 · D-3 · 리포트 §6-1) |
| **gold-check G1**(`:426-430`) · **silver-check G3**(원본 `silver-check.py:973-977`) | 옛 경로 `orchestration/work/phub-ledger-redesign/` 밖 변경 = FAIL — 작업 사본은 `orchestration/work/phub-consult-demo/silver-model/` 이고 이 워크트리의 코디 변경(`.gitignore` · config · README · work-index · `reference/`)도 걸린다 | 경로를 `phub-consult-demo/` 로 · **작업 사본 밖 변경은 WARN 으로만** — **고쳤다**(G-14 · 리포트 §6-1 · §6-2) |
| **gold-check A2** | silver-check 끝 줄이 「PASS (WARN 0)」 이 아니면 FAIL — G3 가 WARN 을 남기면 걸린다 | 끝 줄이 「PASS (WARN n)」 이고 WARN 이 전부 G3 이면 통과 · 그 줄을 A2 WARN 으로 옮겨 적음 — **고쳤다**(G-11 · 리포트 §6-2) |
| **gold-check A1** | `site.csv` · `alias.csv` · `anatomy_site.csv` 는 「한 바이트도 안 바뀜」 파일(`:97-98`) · `source_ref.csv` 덧붙임은 목록 밖이면 FAIL(`:89-92`) | 기준 = 묶음 기준 사본 · 허용 목록(G-14) — **다시 썼다**(리포트 §6-2). 옛 허용 갈래(`procedure_relation` same_day · `concern_site` 8)는 「기준 사본과 바이트 같음」 으로 대신한다 — 기준 사본에 이미 들어 있으므로 뜻은 지켜진다 · `external_code` 헤더만 검사는 그대로 |
| **gold-check A3** | `silver-supplement.py` 재현본과 `source_ref.csv` 바이트 대조 — 근거 줄을 더하는 순간 FAIL(`:113-125`) | 보강 재현 위에 `build_site_3tier.py` 재현을 겹쳐 7 파일 + `user.csv` 대조(G-14) — **고쳤다**(리포트 §6-2) |

- 원본 스크립트는 고치지 않는다(G-11). 고친 줄 = 리포트 §6(고치기 전 사본 `$S/archive/scripts-before-addendum1/` · `scripts-before-addendum2/`). 작업 사본 수정분 **전부**(위 표 · 리포트 §6 diff)를 원본 · 다음 레인에 어떻게 넘기나는 Q-6.
- 부정 시험 1회(리포트 §3): SITE-014 `name_ko` 를 바꾸면 A1 FAIL 1 · A3 FAIL 1 로 잡힌다(되돌린 뒤 해시 같음).

### 3-5. 「눈」 — 이번 판에 합치지 않는다

- 결정(_R「부위 3단 나머지 확정」 「눈 → 『눈 주변』 다른 이름」)은 그대로이고, **이번 판 기본값으로 싣지 않는다**(G-3 ①). SITE-018 은 지금 위 부위(최상위) 그대로 → 3단 밖 예외 1(T3 · S-1).
- 싣지 않는 까닭이 된 충돌(다음 판 꼴의 출발점): 「눈」 은 이미 site 행이라 `alias(site, SITE-019, 눈)` 은 A3 FAIL · 입구 `ambiguous` · SITE-018 을 가리키는 행 40(F-19)을 옮기면 「실명 @ 눈」 22 행이 「실명 @ 눈 주변」 으로 읽힌다 · 원장 근거 행을 바꿔야 해 E5 · A1 과 부딪힌다. 합침 꼴(가리킴 옮김 · 행 지움 · A1 예외)은 0.1.1 §3-5 에 적었다(변경 기록).
- **보고 때 사용자에게 말할 것**: 정해진 배치 하나(눈 → 눈 주변)가 이번 판에 빠진다.
- 「아이 → 눈 주변」 다른 이름은 넣는다(「눈」 과 무관 — §3-2).

## 4. 허브 동작 영향 · 전후 비교

### 4-1. 영향

| 무엇 | 지금 | 이 스펙 뒤 | 근거 |
|---|---|---|---|
| `site.parent_code` 를 읽는 곳 | gold-build 0 · 허브 0 | **그대로 0** — 계층 자체는 gold · 도구 응답을 안 바꾼다. 단 `parent_code` · 묶음 `description` 근거 줄은 자기 근거가 없는 site 입구(이름 · 별칭)의 근거로 넘어간다 — 이번 판 **26**(SITE-120 이름 1 + 이동 부위 기존 별칭 25 — F-17 · G-13) | F-11 · F-12 · F-17 |
| `concern_candidates` 의 `site` | site 입구 글자 일치 + `concern_site` 묶임 · 계층으로 안 넓힘 | 같다. 새 부위 이름으로 물을 때만 그 이름이 입구에 생긴다 — 묶인 `concern_site` 가 없으면 결과 변화 0 | `concern.py:183-185` · HG3-2 · HG3-5 |
| 고민 부위 · `concern_site` | 103 행 | **더하지도 옮기지도 않는다** | G-3 ① |
| `resolve` | 입구 글자 → (표, 코드) · 둘 이상이면 `ambiguous` | 「기타」 · 「승모근」 · 「침샘」 · 「쇄골」 이 `ambiguous` 로(F-21) | `resolve.py:47` |
| 입구(`g_entry`) | 2,642 행 | **2,680**(+38 = 새 site 26 + 별칭 12) · 없어진 행 0 · 뒤 `gid` 밀림(F-18 · 바이트로는 1,779 줄 다름) → `gold_hash` 바뀜. `g_evidence` 27,740 → 27,779(+39) · 나머지 gold 13 표 + `questions` 바이트 0 차이 | `gold-build.py:122-147` · 리포트 §4 |
| 근거 표지 | site 입구 전부 「원장」(새 근거 0) | site 입구 186 = 원장 135 · 원장 + 사용자 제공 34 · 사용자 제공 17. 「사용자 제공」 만 = 원장 근거 없는 새 부위 17 · 「원장 + 사용자 제공」 34 가운데 **26 은 기존 입구**(원장 → 원장 + 사용자 제공 · 받아들임 G-13) | F-6 · F-17 · 리포트 §4 |
| 「조회는 위 → 아래」 | 소비자 0 | **생기지 않는다** — 누가 할지는 Q-7 | F-12 |

### 4-2. 전후 비교 시험

| # | 시험 | 기대 |
|---|---|---|
| T3-1 | 계층만 바꾼 판(새 행 · 별칭 0)으로 gold-build | 바뀐 gold 행 = **자기 근거(이름: `name_ko` · `name` · 빈칸 / 별칭: `alias`)가 없는 이름 · 별칭 입구 가운데 근거 줄이 더해진 부위의 것 — 이번 판 26**(SITE-120 이름 1 + 이동 부위 기존 별칭 25 · 모두 `evidence_kind` 원장 → 원장 + 사용자 제공 · 그 g_evidence) · 그 밖 바이트 같음 → 지금 데이터로는 `gold_hash` **바뀜**(안 바꾸는 길 = Q-4) · `aux_hash` 바뀜 |
| T3-2 | 새 행 · 별칭 · `anatomy_site` 까지 넣은 판 | 바뀐 파일 = `g_entry` · `g_evidence` 가 중심 · `anatomy_site` 새 행이 엣지 · 노드를 만들면 `g_node` · `g_edge` 도(목록으로 남김 — `gold-build.py:577-600`). 기존 입구 행은 `gid` 를 빼고 (`text`, `entity_table`, `entity_code`, `name_kind`, `silver_id`) 로 대조해 그대로(T3-1 의 26 행 제외). 실측(리포트 §4): 새 38 · 근거 종류만 바뀜 26 · 없어짐 0 · `g_node` · `g_edge` 등 13 표 바이트 0 차이 |
| T3-3 | `questions.csv` 37 답 키 | 전 · 후 같음 |
| T3-4 | 허브 단위 — (고민, 부위 이름) 짝 전부로 `concern_candidates` 전 · 후 | 기존 부위 이름 짝 응답 같음 · 달라진 짝 = 새 부위 이름 짝뿐(목록) · 셈법은 SPEC-001 §5-11 과 같게 |
| T3-5 | S-1(예외 SITE-018 1) · S-2 · D3(작업 사본 규칙) · A1 ~ A5 · gold-check A1 · A2 · A3 · G1(G-14) | FAIL 0 · WARN 은 작업 사본 밖 변경(G3 · G1 · A2)만. 이번 판 실측 = silver-check PASS (WARN 5) · gold-check FAIL 0 · WARN 10(리포트 §3) · S-1 · S-2 는 W-2 |
| T3-6 | 입구 글자가 다른 (표, 코드) 둘 이상에 닿는 낱말 목록 전 · 후 | 늘어난 낱말 = 기타 · 승모근 · 침샘 · 쇄골 넷뿐 |

## 5. 반영 절차

### 5-1. 원칙

| # | 원칙 | 근거 |
|---|---|---|
| L-a | 한 번 = **한 묶음**(`clinic-a-20261119`) — 근거 파일 · silver 수정 · 기준 사본이 같은 묶음 이름 | E4 · 전례 `archive/silver-before-<이름>` |
| L-b | silver 수정은 **작업 사본에서** · 원본은 읽기만 · 다시 돌려도 같은 바이트(스크립트 · 기록) | G-2 · `silver-supplement.py:4-6` |
| L-c | 기존 행은 **덧붙이기만** — 예외 둘: ① `site.parent_code` 칸(목록에 있는 행만) ② 묶음 부위 6 행의 `site.description`(「묶음 부위」 로 시작 — T4). 작업 사본 gold-check A1 이 이 둘만 허용한다(G-14) | `gold-check.py:69-111`(원본) · G-14 · G-3 ① |
| L-d | 게이트를 넘지 않은 것은 다음 단계로 가지 않는다 · 허용 밖 검사 실패는 멈추고 질문 | G-10 · G-11 |

### 5-2. 단계

| 단계 | 입력 | 산출 | 자리 | 게이트 |
|---|---|---|---|---|
| P1 확정 배치표 | 배치안 CSV + G-6 · G-7 · D-1 | 부위 전 · 후 표(이동 · 새 부위 · 다른 이름 · 셈) | `silver-site-report.md` | 자동 검수(reviewer) |
| P2 근거 파일 | P1 + 결정 행 글 · 진료항목 이름 낱말 | `user.csv`(§2-2) | `$S/drafts/clinic-supplement/clinic-a-20261119/` | — |
| P3 기준 사본 | 작업 사본 silver(패치 전 · 원본 아카이브 silver 와 바이트 같음) | `$S/archive/silver-before-clinic-a-20261119/silver/` = **묶음 기준 사본**(gold-check A1 · A3 의 기준 — G-14) | 복사(지우지 않는다) | — |
| P4 silver 수정 | P3 + P1 + P2 | `site.csv` · `alias.csv` · `anatomy_site.csv` · `source_ref.csv` | `$S/silver/` | — |
| P5 silver 검사 | silver | **FAIL 0 · WARN 은 G3 작업 사본 밖 변경만**(이번 판 PASS (WARN 5)) | `$S/drafts/silver-check/silver-check.py`(경로 · `resolve` · 근거 종류 · D3 · G3 수정 — §3-4 · + S-1 · S-2 는 W-2) | 자동 검수 |
| P6 gold | silver | gold 16 | `$S/gold/gold-build.py` → `gold-check.py`(근거 종류 · G1 · A1 · A2 · A3 수정 — §3-4 · G-14) | **gold-check FAIL 0 · WARN 은 G1 · A2 의 작업 사본 밖 변경만**(이번 판 WARN 10) **· 전후 비교 T3-1 ~ T3-6** |
| P7 허브 레포 교체 | silver · gold · 원장 확인 목록 | `data/medallion/` **통째 교체** · `README.md` 판 · 해시 · 행 수 · 로컬 dry-run · 적재(`GOLD_EXPECTED_HASH` 갱신 — F-22) · 허브 시험 | 복사 · README 갱신 · `backend/scripts/load_medallion.py` | **PR 머지**(허브 `release/v1.2.0` — `_RESUME` 「워크트리」 `code` 줄) |
| P8 stg 반입 | P7 머지 판 | stg DB | SPEC-003 §11-4 「갱신」 | **다음 단계** |

```text
기준 사본(P3) ─┐
확정 배치표(P1) ┼─ silver 수정(작업 사본 · build_site_3tier.py) ─→ silver ─→ silver-check(경로 · resolve · 근거 종류 · D3 · G3=WARN · S-1 · S-2)
근거 파일(P2) ─┘        ─→ gold-build ─→ gold-check(A1 · A3 = 묶음 기준 사본 · A2 · G1=WARN · K1~K7 · H1) ─→ 전후 비교 T3-1 ~ T3-6
```

- 다음 스냅샷에서 새 부위 낱말이 나오면 같은 단계를 새 묶음 이름으로 다시 돈다(_R「허브 보강 단계 시작」 「반복 레인」 의 부위 몫).

### 5-3. 허브 레포 교체(P7)

| # | 정한 것 | 근거 |
|---|---|---|
| R-1 | `data/medallion/silver/` · `gold/` · `notes/ledger-check-list.csv` 를 **통째로** · 한 파일만 고치지 않는다 | G-12 |
| R-2 | `README.md` 의 판 · `gold_hash` · `aux_hash` · 표 수 · 행 수 = 적재기 dry-run 이 찍는 값 | `$H/data/medallion/README.md:8-15` |
| R-3 | 근거 파일 · 진료항목 CSV 는 허브 레포에 **안 넣는다**(`ref` 는 자리만) | G-3 ④ |
| R-4 | 교체 전 대조 — 허브 레포 silver = 원본 silver 바이트(지금 같다 — F-1) | F-1 |
| R-5 | 적재 뒤 `health.build` = README 해시 · `health.integrity` 의 `gold_rows_without_evidence` · `evidence_without_source_ref` = 0 | F-22 |

### 5-4. stg 반입(절차만)

SPEC-003 §11-4 「갱신」 그대로 — 레포 갱신 PR 머지 → VM 반입 폴더에 새 판 → dry-run → 적재 → `GOLD_EXPECTED_HASH` env 갱신 → 재시작 → `health` 해시 · `integrity`. 표 · 칸이 그대로라 revision 0(F-14). stg 는 코디가 bastion 경유로 직접(G-10).

### 5-5. 시험(절차)

| # | 시험 | 기대 |
|---|---|---|
| T5-1 | silver 수정을 기준 사본에서 다시 돌림(`build_site_3tier.py` · gold-check A3) | silver 바이트 같음 · `user.csv` 같음(리포트 §2 · §3 — 확인함) |
| T5-2 | 기준 사본 대비 바뀜 = 묶음 목록뿐(`site` · `alias` · `anatomy_site` · `source_ref`) · `site` 기존 행은 `parent_code` 와 「묶음 부위」 `description` 만(L-c 예외 둘) | 목록 밖 0(gold-check A1) |
| T5-3 | 허브 dry-run(로컬 · DB 접속 0) | exit 0 · 표 수 · 행 수 = README |
| T5-4 | 로컬 적재 뒤 허브 시험(WP 파일만) · R-5 | 해시 같음 · integrity 두 값 0 |

## 6. 영향 · 되돌리기

### 6-1. 바뀌는 해시

| 바뀜 | silver 파일 | `gold_hash` | `aux_hash` | 근거 |
|---|---|---|---|---|
| 부위 계층만 | `site.csv` · `source_ref.csv` | **바뀜**(지금 데이터 — 자기 근거 없는 입구 26 = SITE-120 이름 1 + 이동 부위 기존 별칭 25). 옮긴 부위의 입구가 모두 자기 근거를 가진 판(Q-4)에서만 안 바뀜 | 바뀜 | F-17 · G-13 |
| 새 부위 · 다른 이름 · `anatomy_site` | `site.csv` · `alias.csv` · `anatomy_site.csv` · `source_ref.csv` | 바뀜(`g_entry` · `g_evidence` · `gid` 밀림 · 이번 판 `g_node` · `g_edge` 는 바이트 같음) | 바뀜 | F-18 · 리포트 §4 |
| **이번 판 실측** | 위 네 파일 | `8accbb21…` → **`ece5d2be6e93723fdc4dd6b254ae259aab5ea4e114e0536ab428db612ed39062`**(gold 16 · 허브 `inputs.py` 와 같은 식) | `93ec89fd…` → **`e0813c0a30fee732a4940f6edc704660cf532564c0161923fbfd2ea9a8e3344b`**(`source_ref` 만 바뀜) | 리포트 §4 — gold-build 끝 줄의 「gold 해시」(`e07d20cd…`)는 다른 식이라 쓰지 않는다 |

### 6-2. 상담 앱

| 상황 | 일어나는 일 | 근거 |
|---|---|---|
| `gold_hash` 가 바뀐 판이 허브에 뜸 | 열린 대화는 다음 턴에 `build_changed` 로 맺힘 · 쪽 넘김 도중이면 그 조회가 `build_changed` | F-16 |
| `aux_hash` 만 바뀜 | 대화는 이어진다 · 넘기던 cursor 는 무효 → 쪽 넘김 `build_changed`. 이 판은 지금 데이터로 늘 `gold_hash` 도 바뀐다(위 줄) | `cursor.py:41` |

- stg 반입은 열린 대화를 끊는다 — 반입 시각은 코디가 사용자에게 알린다.

### 6-3. 되돌리기

| 층 | 되돌리는 법 | 근거 |
|---|---|---|
| 작업 사본 | `archive/silver-before-clinic-a-20261119/` 를 silver 로 되씌우고 gold-build 를 다시 · 원본은 손대지 않았으므로 그대로 | L-b |
| 허브 레포 | 교체 PR 을 되돌리는 PR | G-12 · `$H/data/medallion/README.md:27` |
| 로컬 · stg DB | 옛 판 폴더로 다시 적재(한 트랜잭션 · 실패면 옛 판 그대로) · `GOLD_EXPECTED_HASH` 도 옛 값으로 | `$H/data/medallion/README.md:48` · SPEC-003 §11-4 |

## 7. 정할 것

| # | 무엇 | 선택지 · 이 문서의 제안 | 막는 단계 |
|---|---|---|---|
| Q-1 | 진료항목 코드가 본문에 든 조사 리포트(`research-site-tree.md` · `research-kos-site-3tier.md` · `research-kos-item-map.md`)를 마감 커밋에 넣나(코디 마감 체크 — G-3 ④ 「코드 공개 0」 과의 관계) | 빼거나 가림(제안) / 넣음 | 마감 |
| Q-2 | `site.parent_code` 뜻에 「사용자 배치」 를 더함(T8) | 받음 / 계층을 다른 표로 | P4 |
| Q-3 | 묶음 부위 표현 — 지금 발주는 (a)(D-5) | (a) 부위 행 + 설명(헤더 불변) (b) 새 칸 · 표(허브 계약이 바뀜) | 다음 판 |
| Q-4 | 자기 근거가 없는 site 입구에 이름 · 별칭 근거를 먼저 대나 — 대상은 SITE-120 1 이 아니라 **26**(SITE-120 이름 1 + 이동 부위 기존 별칭 25 · 다음 묶음에서 부위를 더 옮기면 늘어난다). 대면 계층만 바꾼 판의 `gold_hash` 가 안 바뀌고 원장 별칭이 「원장」 표지로 남는다. 이번 판은 섞임 받아들임(G-13) | 받음(이번 판 — G-13) / 다음 판에 근거 보충(지을 원천이 있는지 모름) | 다음 판 |
| Q-6 | 작업 사본 스크립트 수정분 **전부**(리포트 §6 diff — `silver-check.py` 원장 경로 · `resolve` · `ref_kind` · D3 · G3 / `gold-build.py` `ev_kind` / `gold-check.py` `ev_kind` · G1 · A1 다시 씀 · A3 · A2 · WARN 출력 / `build_site_3tier.py` 인자)의 정본 자리 — 원본(아카이브)에 되돌려 넣나 · 레인 자리를 새로 두나 | 사용자 · 코디 | 다음 묶음 |
| Q-7 | 「조회는 위 → 아래」(G-5)를 누가 하나 | 허브(부위 계층 보조 입력 + 도구) / 링크 층(G-9) | 다음 스펙 |
| Q-8 | 새 다른 이름 12 의 근거 꼴 — 지금 판 = `source_ref` 0 · 별칭 입구는 부위 행 근거 · 별칭 글자 근거는 `user.csv` 기록만(E6 · silver 워커 판단 — 리포트 §7). `_RESUME` · addendum 에 없는 처리라 확인을 받는다 | 받음(지금 꼴) / 별칭 낱말 단위 근거 자리를 새로(예: `alias` 행을 가리키는 `source_ref` 꼴 — 그러면 E6 · gold-build 근거 고르기도 바뀜) | 다음 판(이번 판 gold 는 지금 꼴로 PASS) |
| Q-9 | `user.csv` 의 `decision` 이 `_RESUME` 어느 결정 행에서 왔는지 담는 칸 — 지금 꼴(§2-2)에는 없다(`basis` 는 모든 줄 같은 글 · `decision` 은 워커 요약) | 칸 없이 둠 / 결정 행 키 칸 더함(그러면 T1-2 에 「결정 행 대조」 를 되살림) | 다음 묶음 |

- 옛 Q-5(gold-check A1 · A3 꼴)는 정해져 G-14 로 옮겼다 — 번호는 비워 둔다(본문 참조가 밀리지 않게).
- 사용자 확인 대기 기본값 D-1 ~ D-5 는 §0-3a(정할 것이 아니라 확인).

## 8. 다음 단계 — WORK 로 넘길 것

| WORK(제안) | 담는 것 | 선행 |
|---|---|---|
| W-1 부위 silver · gold — **끝남**(`silver-site-task.md` · addendum 1 · 2 · 리포트) | 확정 배치표 재셈 → 근거 파일 → 작업 사본 silver 수정 → 작업 사본 스크립트 수정(§3-4 · G-11 · G-14) → silver-check PASS (WARN 5) → gold-build · gold-check FAIL 0 · WARN 10 · 부정 시험 1(A1 · A3) | — (D-1 ~ D-5 는 사용자 확인 대기 · 다르면 다시 돎) |
| W-2 검사 보탬 | S-1 · S-2 · T1-2 · T3-1 ~ T3-6 전후 비교 · 부정 시험(T1-1) | W-1 |
| W-3 허브 반입 | `data/medallion/` 교체 PR · README 해시 · 로컬 적재 · `GOLD_EXPECTED_HASH` · 시험 · integrity · (다음) stg | W-1 · Q-1 |

- 각 WORK 끝은 reviewer 자동 발주(G-10).

## 부록 A. 결정 → 본문

`_RESUME.md` §2 행 첫 글 · 0.2.2 를 쓸 때의 줄(`grep -n '^| 2026-11-19'` — 다음 결정이 맨 위에 들어오면 밀린다).

| 결정(_R 행 첫 글) | 0.2.2 줄 | 본문 |
|---|---|---|
| 「silver 패치 1차 끝」(A1 · A3 · G1 · G3 · 근거 종류 섞임) | :42 | G-11 · G-13 · G-14 · §0-1 · §0-2 · §3-4 · §4 · §5-2 · §6-1 · §8 |
| 「코디 기본값(사용자 확인 대기): 새 부위 자리」 | :43 | G-11 · §0-3a D-1 ~ D-4 · §3-4 |
| 「SPEC-009 범위 = 부위만 · silver 바로 고침 · 이번 판 기본값」 | :44 | G-2 · G-3 · §2 · §3-2 · §3-3 · §3-5 · 부록 C |
| 「허브 보강 단계 시작」 | :45 | G-1 · §0-1 · §5 |
| 「원장 근거 없는 추가 부위 15」 | :48 | G-5 · G-8 · T6 · §3-2 |
| 「부위 3단 나머지 확정」 | :49 | G-7 · §3-2 · §3-5 |
| 「부위 3단 배치 결정(일부)」 | :50 | G-6 · §3-2 |
| 「허브 부위 3단」 | :51 | G-5 · T7 · §4-1 · Q-7 |
| 「허브 보강한다」 | :53 | G-4 · §2 |
| 「워커 전부 opus」 | :55 | G-10 · §5 |
| 「순서 변경」(② 명동점 매핑은 새 코디 세션) | :62 | G-9 · §0-4 |
| 워크트리 `code` 줄(허브 = `release/v1.2.0`) · 로컬 PG 줄 | :14 · :17 | §5-2 P7 |

## 부록 B. 재셈

| # | 셈 | 값 |
|---|---|---|
| ① | `$SM/silver` CSV 수 · 허브 레포 silver 와 `diff -rq` · gold 16 sha256 | 59 · 차이 0 · 같음 |
| ② | `site` 행 · 최상위 · `alias` 행 · site 별칭 · `kind` 값 | 89 · 68 · 980 · 59 · 6 값 |
| ③ | `source_ref` 행 · 「사용자」 로 시작 · `drafts/clinic-supplement/` | 48,113 · 0 · 0 |
| ④ | 배치안 CSV 줄 · `구분` 값 · 「다른 이름 추가」 · 이번 판 다른 이름 12 의 지금 alias · site 이름 겹침 · 새 이름 × g_entry 입구 겹침 | 113 · 기존 67 · 3단 밖 22 · 추가-상세 18 · 추가-새 6 · 원장 근거 「없음」 15 · 15 줄(16 낱말) · 0 · 기타 · 승모근 · 침샘 · 쇄골 4 |
| ⑤ | SITE-018 · SITE-019 를 가리키는 행 | F-19 · F-20 |
| ⑥ | `_RESUME` §2 의 2026-11-19 행 | 21(0.2.2 쓸 때) |
| ⑦ | 작업 사본 실측(리포트 · 검수 r4 §5 와 맞춤) — `site` · `alias` · `source_ref` 데이터 줄 · `user.csv` `field` 셈 · `source_ref` 의 `user.csv:L2` | 115 · 992 · 48,226 · 빈칸 17 · `parent_code` 78 · `description` 6 · `alias` 12 · 1 줄(`site,SITE-003,parent_code`) |

## 부록 C. 이 판 범위 밖(결정 · 조사 전)

- 원장 밖 근거 원천 중 외부 출처 · KOS 상품 · 옵션 글
- 시술 · 제품 적용 부위 범위(`site_scope` 표 · 범위 7 값 · 대상 · 합치는 규칙 · gold 칸 · 허브 계약 · 마이그레이션)
- 제품 추가(명동점 약물 · 기기 · 판정 규칙 · 필수 칸 · 연결 표)
- 시술 추가(새 시술 · 개요 · 원리 글)
- 보강 목록 CSV · 사람 검수 꼴
- 반복 레인 중 스냅샷 수집 · 진료항목 표 · 제품 · 시술 허브 대조 단계
- 병원 무관 원칙을 넘어선 범위 문장 · 병원끼리 사실이 갈릴 때 · 두 번째 병원
- 상담 앱 `basis` 표지의 새 근거 종류 처리
- 「눈 → 눈 주변」 합침(이번 판 기본값으로 안 함 — 다음 판)
- 거미스마일 · 러브핸들 · 측두근의 허브 별칭(진료항목 쪽 판정)

## 변경 기록

### 0.2.2 — 2026-11-19 · 재검수 3(`review-spec-009-r4.md`) FAIL 2 · WARN 4 반영 · silver 결과(리포트) 실측으로 맞춤

- R4-1 · F-17 · §0-2 · §4-1 · T3-1 · T3-2 · §6-1 · Q-4: 근거 종류가 바뀌는 기존 입구 1 → **26**(SITE-120 이름 1 + 이동 부위 기존 별칭 25 · 이름 입구 자기 근거 = `name_ko` · `name` · 빈칸 / 별칭 입구 = `alias`). §0-2 에 「원장 별칭 25 의 표지가 『원장 + 사용자 제공』 으로 바뀐다」 줄. Q-4 대상 26 으로 넓힘.
- R4-2 · G-11 · G-13 · G-14 · §3-4 · P3 · P5 · P6 · §5-2 그림 · T3-5 · §8 W-1: 코디 답 _R「silver 패치 1차 끝」 · `silver-site-addendum2.md` 를 결정으로 — A1 = 묶음 기준 사본 `archive/silver-before-clinic-a-20261119/` · A3 = 보강 + `build_site_3tier.py` 재현 대조 · G1 · G3 = 경로 `phub-consult-demo/` + 작업 사본 밖 변경 WARN · A2 = G3 WARN 만이면 통과 · 근거 종류 섞임 받아들임(G-13). Q-5 를 G-14 로 옮김(번호 비움). 「멈추고 질문」 → 「고쳤다」(리포트 §6 인용). P5 · P6 게이트 = 「FAIL 0 · WARN 은 작업 사본 밖 변경만」.
- W1 · E1 · E6 · §3-3 · Q-8: 새 다른 이름 12 의 `source_ref` 0 · `user.csv` 기록만(silver 워커 판단)을 실물대로 적고 확인 대기 Q-8 로 올림.
- W2 · T4 · §3-2 · L-c · T5-2: 기존 묶음 부위 6 행 `description` 바뀜을 기존 행 바뀜의 두 번째 예외로.
- W3 · §2-2 · §2-4 · T1-2 · Q-9: `user.csv` 를 실물 칸(`line,kind,target_table,target_code,name,field,decision,basis,status`)으로 · `status` 뜻(E4) · 옛 T1-2(`quote` ⊂ 결정 행)는 돌 수 없어 바꿈 · 결정 행 추적 칸은 Q-9.
- W4 · G-11 · Q-6: 작업 사본에서 실제로 고친 스크립트 범위 전부(G3 · A1 다시 씀 · A3 · A2 · WARN 출력 · `build_site_3tier.py` 인자) · Q-6 대상 = 리포트 §6 diff 전부.
- 수 · 해시: site 115 · 이동 69 · 새 site 26 · alias 992 · `anatomy_site` 92 · `source_ref` 48,226 · g_entry 2,680 · g_evidence 27,779 · `gold_hash` `ece5d2be…` · `aux_hash` `e0813c0a…`(리포트 §2 · §4). 부록 A 줄을 지금 `_RESUME` 으로(+5 밀림 · 새 행 「silver 패치 1차 끝」 :42).

### 0.2.1 — 2026-11-19 · 재검수 2(`review-spec-009-r3.md`) FAIL 3 · WARN 5 반영

- R1 · 머리 · G-2 · G-3 · 부록 A: _R「SPEC-009 범위 = 부위만 · silver 바로 고침 · 이번 판 기본값」 을 결정으로 반영 — 「눈」 합침 안 함 · 침샘 · 쇄골 · 승모근 = site + `anatomy_site` · 다른 이름은 허브 부위 다른 이름만 · 근거 = `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>` · 작업 공간 = `$W/silver-model/` 작업 사본. 「정할 것」 에서 내림(옛 Q-1 근거 종류 값 · Q-2 줄 내용 vs 경로 · Q-3 ① ② 공개 범위 · Q-6 D3 선택지 · Q-7 눈 · Q-8 별칭 · Q-11 작업 공간). §3-5 를 「이번 판에 합치지 않는다」 로 · T3-7 · E5 예외 · M1 ~ M5 뺌.
- R2 · 전체: `_RESUME` 인용을 **행 첫 글을 키로** 바꾸고 0.2.1 줄은 부록 A 에만(맨 위에 결정이 들어올 때마다 밀림). 11-19 행 수 18 → 21.
- R3 · F-8 · §3-4 · P5: `silver-check.py:28-37` 원장 · step1 경로 낡음(패치와 상관없이 P5 가 깨짐) — 작업 사본에 한해 고침(G-11).
- W1 · §0-3a D-1 · §3-2: 새 부위 넷 자리(침샘 → 얼굴 > 턱 · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목) = 3단 조사 결과 · 코디 기본값 · 사용자 확인 대기.
- W2 · E3 · §2-3 · §3-4: 근거 종류 식 세 곳 + `resolve` 에 `drafts/clinic-supplement/` → 「사용자 제공」(새 값 없음 · 순서 목록 그대로).
- W3 · §3-2 · D-4: 다른 이름 12 목록(애교 빼고 · 「상완」 · 「하관전체」 배치안 글자) · 지금 alias · site 겹침 0 재셈.
- W4 · §0-2 · F-21 · T3-6: 겹침 목록 = 기타 · 승모근 · 침샘 · 쇄골 넷(거미스마일 · 러브핸들 · 측두근 뺌).
- W5 · §3-3 · D-3 · D-5: D3 = `anatomy_site` 로 이어진 같은 이름 짝 허용(코디 기본값) · 사지 · 상체 · 체간 · 코안면 2단 = 3단 조사 처리로 근거 정정.
- G-11 · §0-3a · §3-4: 코디 silver 추가 지시(`silver-site-addendum1.md`)의 작업 사본 스크립트 수정 허용 범위(경로 · G1 · 근거 종류 식 · D3) · 허용 밖(A1 · A3)은 멈추고 질문.
- §7: 정할 것을 Q-1 ~ Q-7 로 새로 매김 · §8: W-1 을 발주 중인 silver 작업으로.

### 0.2.0 — 2026-11-19 · 범위를 부위로 줄임(사용자 11-19)

- 적용 부위 범위 · 제품 · 시술 추가 · 보강 목록 · 제품 · 시술 대조 · 병원 무관 원칙 · 두 번째 병원 · 앱 `basis` 를 빼고 부록 C 에 이름만 · 정할 것 Q-1 ~ Q-12 · 재검수 r2 N1 · N2 · N3 · N5 반영.

### 0.1.1 — 2026-11-19 · 검수 FAIL 5 · WARN 11 반영(`review-spec-009.md`)

- `_R` 인용 재정렬 · D3 = 침샘 · 쇄골 · 승모근 · T2-1 정정(SITE-120) · 근거 종류 식 세 곳 + 순서 목록 둘 · 「눈」 합침 꼴(M1 ~ M5 — 가리킴 옮김 · 원장 근거 16 행 바꿈 · 행 지움 · A1 예외) · 실물 표 · 허브 계약 · A3 · G1 · `GOLD_EXPECTED_HASH` · 재셈 정정.

### 0.1.0 — 2026-11-19 · 초안

- S1 ~ S6 첫 판 · 정할 것 Q9-1 ~ Q9-16 · 다음 단계 W-1 ~ W-5.
