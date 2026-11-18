---
type: spec
id: SPEC-001
title: "허브 gold MCP — gold CSV 15 + source_ref + 보조 입력(계층 3표 · 원장 확인 목록) 메모리 적재 · 결정론 도구 9(속성 쪽 시작 · 입구 목록 · 정확한 이름 맞춤 · 정보 종류 셈 포함) · REST/MCP 같은 코어"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.8.2
created_at: 2026-11-16
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 0.8.2 근거 행 — 「SPEC-003 0.2.0 정할 것 코디 답」(O-S1 `unavailable` · 503 · O-S2 MCP 꺼짐 = HTTP 503) · 「gold MCP 421 고침」(GOLD_MCP_ALLOWED_HOSTS · _ORIGINS) · 「SPEC-003 stg 검수 WARN 코디 답」(R-2 시간 한도) · 「stg 반입 완료」(Gateway 가 Host 를 백엔드 내부 주소로 넘김)) · stg-runbook.md (실행 기록) · review-code-hub-stg.md · review-code-hub-v081.md (Low 3) · 허브 `d3d078c` (구현 결과가 정본)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 0.8.1 근거 행 — 「SPEC-008 검수 WARN 16 코디 답」 의 F-1 ⓒ(상담 0.4 서버는 끈 상태 새 대화 안 엶 · 옛 끈 대화 = 읽기만 · 0.4 켠 상태는 0.7.2 허브로도 돎) · 「나머지 리포트대로」(F-11 — 고칠 · 지울 허브 시험)) · review-spec-008.md (검수 — F-1 · F-11) · spec-008-fix1-brief.md (0.8.1 발주서 — 보조 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 0.8.0 근거 행 — 「상담 입구 결정 표 D-1~D-15 확정」 의 D-1(resolve 목록 꼴 그대로 · 맞춤 꼴은 정확한 이름 → 코드만 · 부분 · 줄임 · 겹침 규칙 지움) · D-2(시험 앱 B 열은 허브 0.7.2 옛 판에 묶고 안 고침) · 「허브 resolve = 최소 목록 꼴(입구 목록 출력) · 규칙을 더하지 않는다 · 입력 정리는 채팅(앱) 단에서」) · spec-008-brief.md (0.8.0 발주서 — 보조 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 0.7.2 근거 행 — 「규칙 변경 = 넣음(지금 · SPEC-001 0.7.2 + WORK-013 WP-3): 고민 + 부위 는 물은 부위가 그 고민의 부위(자기 + 하위) 안에 있을 때만 거름(HG3) · 아니면 거르지 않고 우선 표시(SP) — 보강 뒤 윗고민 뒤집힘 · O-31 함께 닫힘」) · research-concern-site.md (§0-5 · §5-1 · §6 — 윗고민 뒤집힘 · 까닭) · spec-hub-v072-instructions.md (0.7.2 지시서 — 보조 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 0.7.1 근거 행 — 「SPEC-006 U6-1~3 = (a) … ① 규칙(사용자 결정): concern_site 없는 고민 + 부위 질문은 부위로 거르지 않음 — 그 고민의 시술 전부 + 그 부위 케이스(행 부위 글자 일치)는 「우선 표시」 표지로 앞에 · concern_site 있는 고민은 HG3 그대로」 · 「A8 화면 구조 … SPEC-001 0.7 U7-1~3 = (a)」) · spec-hub-v071-instructions.md (0.7.1 지시서 — 보조 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 0.7.0 근거 행 — 「얼굴 점 = 대화에서 나온 고민 부위 · 점을 누르면 그 고민의 관련 시술 리스트 · 메뉴는 시술 아님 · 리스트는 우리 기준의 시술로」) · §1 「수정 2 목록」 00(시술로 내려가기) · 2(말 잘못 읽음) · 6(고민 부위 칸) · 9(메뉴 = 패키지 아님) · spec-hub-v07-instructions.md (0.7 지시서 — H1 · H2 · H3 · 보조 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §5 (2026-11-17 0.6.0 근거 줄 — 「허브 0.5.2 완료」(HG1 ~ HG3 · closure.py · 638 passed) · 「허브 0.5.2 코드 검수 PASS」 · 「37 batch 끝」) · impl-v052-hub-report.md (W-2 다시 센 수 · 구현 때 정한 것) · app-v052-report.md (미결 2 · 3)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 전 행 — 처음부터 다시 · SPEC 두 개 · D3~D12 추천 채택 · 3열 · D8 CLI 구독 · stg · D2 DB 없음 · 37 은 표본 · 검수 뒤 결정 4 · 재검수(r2) 뒤 결정 2 · 원칙 「폭은 빠짐없이, 깊이만 Jev 판단」 · 흐름(사용자 제안 채택) · 안전 정보를 처음부터 붙이지 않는다 · 테스트 ≠ 상담 · 재검수 2(r3) §5 결정 = 추천(A-1 ~ A-5 · §5 B 승인 · 시작 길 추가))"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 0.5.0 근거 행 — 길 찾기 재설계 진행 · 허브 검수 뒤(제품 offer role · distinct_rows) · WORK 수정 뒤(N1-1 = 제안 (a)) · 앱 검수 뒤(F-1 짧은 조각 빼기 없앰)) · §1 e2e 피드백 3 · 4"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 0.5.1 근거 행 — SPEC 0.5.0 검수 뒤 결정 3 = 추천(RQ1 은 하위에 자기 행이 있을 때만 · overview/mechanism 은 칸 값 있는 행으로 — coverage 와 같은 함수) · LLM 에는 필요한 것만)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 0.5.2 근거 행 — 답 키 검토(사용자 · 37 표로): Q10 = 윗고민 적응으로 층 밝혀 답함 · Q12 대상 = 계열 전체) · §1 「허브 묶음 발주」 줄(① 고민 윗고민 물려받음 ② 계열 → 케이스 펼침 ③ 고민 + 부위 → concern_site) · §1 e2e 피드백 4 · §5 2026-11-16 「허브 v05 완료」 줄(상품 셈 식 미결)"
    - "orchestration/work/phub-gold-jev/spec-fix3-instructions.md · spec-fix4-instructions.md (보조 근거 — 위 _RESUME §2 행들을 코디가 옮겨 적은 지시서. 0.4.1 부터 근거는 _RESUME §2 11-16 「재검수 2(r3) §5 결정」 행이다)"
  sources:
    - "orchestration/work/phub-gold-jev/research-input-space.md (§2 실패 층 — 후보 층 39 턴 · §3 목록 꼴 820 항목 · 45ms · 줄임 꼴 9 턴) · review-input-space.md (검수 WARN) · SPEC-008-consult-entry.md (상담 0.4 — 목록 꼴을 쓰는 쪽) · clinic_chat 워크트리 phub-gold-jev be1c622 (맞춤 꼴을 부르는 자리 — 읽기만) · PROCEDURE-HUB 워크트리 phub-gold-jev d97a9ad backend/app/modules/gold/resolve.py (0.7.2 구현 — 읽기만)"
    - "orchestration/work/phub-gold-jev/research-gold-connect.md (§0 D1~D12 · §1 · §3 · §5-2 · §6)"
    - "orchestration/work/phub-gold-jev/review-spec-001-002.md (검수 리포트 — W-7 ~ W-11 · N-6 ~ N-10)"
    - "orchestration/work/phub-gold-jev/review-spec-001-002-r2.md (재검수 리포트 — R-1 ~ R-5)"
    - "orchestration/work/phub-gold-jev/review-spec-001-002-r3.md (재검수 2 리포트 — X-2 · N-8 · §5 A-2 · B-1) · review-spec-001-002-r4.md (재검수 3 리포트 — N-2 · N-6)"
    - "orchestration/work/phub-gold-jev/review-spec-001-v07.md (0.7.0 검수 리포트 — WARN 6(W-1 ~ W-6) · NOTE 8(N-1 ~ N-8) · §2 재셈 · §3 줄임 표본)"
    - "orchestration/work/phub-gold-jev/spec-v05-instructions.md (0.5.0 지시서 — 보조 근거) · review-code-hub.md (허브 코드 검수 — W-1 · N-2 · N-3) · review-work-001-002.md (N1-1) · WORK-001-hub.md §9"
    - "orchestration/work/phub-gold-jev/review-spec-v05.md (0.5.0 검수 리포트 — F-1 · W-4 · W-5 · W-7 · W-8 · N-4 · N-5) · spec-v051-instructions.md (0.5.1 지시서 — 보조 근거)"
    - "orchestration/work/phub-gold-jev/spec-v052-instructions.md (0.5.2 지시서 — 보조 근거) · app-key-fix1-report.md (「코디 요청 셈」 · 미결 1 · 2) · review-code-v05-hub.md (허브 검수 v05 — N-1 · N-2 · N-3 · N-5 · N-8) · WORK-005-hub-v05.md §9 (A-1 ~ A-5)"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/silver/concern_site.csv (gitignore · 로컬 — 0.5.2 보조 입력 ③ 제안)"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (DB 판 — 두 판 응답 같음 · §5 P1 · P2 · §7 DT10) · orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/notes/glossary.md (계열 · 시술 · 케이스 · 제품 · 패키지 · 메뉴 뜻)"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/gold/README.md · semantic-map.md · gold-build.py · gold-check.py (gitignore · 로컬)"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/silver/concern.csv · adverse.csv · condition.csv · source_ref.csv · notes/ledger-check-list.csv (gitignore · 로컬 — 보조 입력)"
    - "para/resources/note/ai/llms.txt"
    - "para/areas/concept/cs/artifact-traceability.md"
  related:
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md"
    - "orchestration/work/phub-gold-jev/SPEC-008-consult-entry.md"
---

# SPEC-001 — 허브 gold MCP

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `HUB-OLD` = 옛 PR #31 워크트리 `PROCEDURE-HUB/phub-recommend`(커밋 `2edc190` · 읽기만) · `조사` = `$W/research-gold-connect.md`.
> 공개 레포 규칙: 이 문서에는 표 · 칸 이름 · 코드 · 셈 · 질문 id 만 싣는다. 시술 설명 · 원장 문장 · 답 원문 · 가격 값 · 질문 문장은 싣지 않는다.
> 근거 표기: `_RESUME §2 11-16 「…」` = 결정 표의 그 행 · `조사 §n` · `파일:줄` · `검수 X-n` = `$W/review-spec-001-002.md` 의 지적 번호 · `재검수 R-n` = `$W/review-spec-001-002-r2.md` 의 지적 번호 · `재검수2 X-n · N-n · A-n · B-n` = `$W/review-spec-001-002-r3.md` 의 지적 · §5 번호 · `재검수3 Y-n · N-n` = `$W/review-spec-001-002-r4.md` 의 지적 번호 · `_RESUME §2 11-16 「재검수 2(r3) §5 결정」` = 결정 표의 그 행(A-1 ~ A-5 · §5 B 승인 · 시작 길 추가 — 0.4.1 부터 이 행이 근거다) · `지시 3` = `$W/spec-fix3-instructions.md`(그 결정을 코디가 옮겨 적은 것 — **보조 근거**로만 남긴다). `_RESUME §2 11-16 「길 찾기 재설계 진행」` = 결정 표 맨 위 행(0.5.0 의 근거 — 「허브가 후보를 넓게 · 후보마다 행 수 셈 · 하위 층 자기 행 포함 · 층 표시」) · `허브 검수 W-n · N-n` = `$W/review-code-hub.md` 의 지적 번호 · `HUB` = 허브 구현 워크트리 `PROCEDURE-HUB/phub-gold-jev`(읽기만). `검수 v05 F-n · W-n · N-n` = `$W/review-spec-v05.md`(0.5.0 검수)의 지적 번호 · `_RESUME §2 11-16 「SPEC 0.5.0 검수 뒤 결정 3」` = 결정 표의 그 행(0.5.1 의 근거). 근거가 결정에 없는 것은 본문에 **「제안」** 으로 적고 §10 「열린 것」 에 번호로 모았다.

## 0. 요약

- 허브는 **gold CSV 15표 + silver `source_ref`** 와 **보조 입력 둘**(계층 3표의 `code` · `parent_code` / 원장 확인 목록의 id · 코드 — §2-1)을 시작 때 메모리로 읽고, **결정론 도구 9개**(0.5.0 에서 `coverage` 하나가 늘었다 — 제안 · O-19)를 REST 와 MCP 두 입구로 낸다. LLM 없음 · 쓰기 없음 · DB 없음(_RESUME §2 11-16 「D2 저장」 · 「검수 뒤 결정 4」 ② ③).
- 모든 응답 행은 `gold_table` + `gid` + `evidence_kind` 를 갖고, `evidence` 도구로 `gid → g_evidence → silver 행 → source_ref.ref` 까지 되짚힌다(§6).
- 계층은 router · MCP → service → repository. **DB 로 갈 때 repository 만 갈아 끼운다**(_RESUME §2 11-16 「repository 층만 바꾸면 되게」).
- 이번 판은 **로컬 시험까지**다. stg 로 올리는 길은 정해졌지만(§8) 머지 · 배포 · stg 데이터 반입은 각각 별도 승인이다.
- 0.1.0 에서 열려 있던 둘은 닫혔다(_RESUME §2 11-16 「검수 뒤 결정 4」): **3단 계층 펼침** = silver `concern` · `adverse` · `condition` 의 `code` · `parent_code` 를 보조 입력으로(② — §2-1 · §4-4 · §5-5) · **「원천 미확정」 판정 재료** = 원장 확인 목록의 id · 코드만 보조 입력으로 읽어 응답 머리 `ledger_check[]` 로(③ — §4-0 · §5-6). **gold 15표는 바뀌지 않는다.**
- 0.2.0 에서 열려 있던 둘도 닫혔다(_RESUME §2 11-16 「재검수(r2) 뒤 결정 2」): 부작용 · 조건의 「하위」 = **자손 전부**(§4-4) · `ledger_check[]` 대조 범위 = **요청 코드 + 상품 그대로**(§4-0 — holder 까지 넓힐지는 1회차 trace 뒤).
- **허브는 폭을 자르지 않는다**(_RESUME §2 11-16 「원칙: 질문에 빠지는 정보가 있으면 안 된다」): 조회는 쪽 넘김으로 **끝까지 전부** 나온다 — `limit` 은 쪽 크기일 뿐 결과의 상한이 아니고, 허브는 점수 · 순위로 행을 빼지 않는다(§4-0 「쪽 넘김」). 쪽 밖 목록에도 자르는 한도는 없다(재검수2 X-2).
- 0.4.0 에서 **시작 길 셋**이 늘었다(_RESUME §2 11-16 「재검수 2(r3) §5 결정」 A-2 · 시작 길 추가 — 도구 수는 8 그대로): ① **속성 쪽 시작** — 재료 · 방법 · 해부 · 부위 코드로 시작해 그 칸을 가진 행(= 대상)을 전부 낸다(`facets` 의 `node` — §4-4 「속성 쪽」 · §5-7) ② **입구 목록** — 이름이 안 풀린 질문에서 앱이 Jev 로 입구를 고를 수 있게 범위의 입구 전부를 쪽 넘김으로 낸다(`resolve` 의 목록 꼴 — §4-1) ③ **상품 이름 부분 일치** — `facets` offer 의 `offer_name_contains`(§4-4 · 옛 O-10 결정). **gold 15표 · gold 해시 · 보조 입력은 바뀌지 않는다.**

- 0.5.0 에서 **길 찾기 재료 셋**이 바뀌었다(_RESUME §2 11-16 「길 찾기 재설계 진행」 — 질문이 오면 맨 처음 Jev 가 「무엇에 대한 질문인가 · 어떤 정보가 필요한가」 를 판단하고, 허브는 그 위치만 찾아 읽는다 · SPEC-002 §3-1): ① **넓은 후보** — `resolve` 맞춤 꼴이 낱말 완전 일치 + 조사 떼기에서 **질문 글 안에 들어 있는 입구 이름 전부(부분 일치)** 로 바뀌었다. 조사 목록을 쓰지 않고, 긴 이름 안에 든 짧은 이름도 빼지 않는다(§4-1 · §5-1 R2 · R7) ② **정보 종류 셈** — 새 도구 `coverage` 가 후보마다 정보 종류 14 × 층(자기 · 하위 · 물려받음)의 행 수를 낸다(§4-9 · §5-8). 행 본문은 없다 ③ **하위 층 자기 행** — 앱이 `roles` 에 「하위 *」 를 명시해 부르면 그 층의 자기 행이 `layer` 와 함께 나온다(계약은 0.4.1 그대로 — 부르는 쪽 기본값만 바뀌었다 · §5-2 · §5-3 S5). 구현에서 정한 것 넷을 되적었다(제품 노드 offer 기본 role · `counts.distinct_rows` · `pair` 의 `b` 없는 `package_kinds` · `request` 의 `null`). **gold 15표 · gold 해시 · 보조 입력은 바뀌지 않는다.**

- 0.5.1 에서 **0.5.0 검수를 반영했다**(_RESUME §2 11-16 「SPEC 0.5.0 검수 뒤 결정 3」 · 변경 기록 0.5.1 — 도구 계약의 입력 · 출력 필드는 그대로다): ① `coverage` 의 `overview` · `mechanism` 은 **그 종류의 칸에 값이 있는 profile 행**으로 센다 — 앱의 required 판정(SPEC-002 §3-2 RQ1)이 이 셈과 같은 함수를 쓴다(§4-9 · §5-8) ② `facets` 의 **도구 설명에 「하위 층의 자기 행은 `roles` 에 하위 role 을 줘야 나온다」 를 적는다**(§4-4 · §5-3 S2) ③ 이 문서와 SPEC-002 가 semantic-map §5 를 바꿔 읽는 자리 셋을 밝히고 **두 글이 다르면 이 문서가 앞선다**고 적었다(§5 머리 · §5-3 S5) ④ 하위 한 단으로 **놓치는 수**를 적었다(§5-3 S6 · O-21).

- 0.5.2 에서 **구멍 셋을 막는 규칙**을 더하고(§5-9 — 사용자 원칙 「질문이 가리키는 대상 × 필요한 정보 안에서는 빠짐없이」 · 한 문항이 아니라 일반 규칙) **구현에서 정해진 것을 되적었다**(변경 기록 0.5.2): ① **HG1 고민 → 윗고민 물려받음** — 물은 고민의 행이 0 이면 가장 가까운(행이 있는) 윗고민의 행을 `hier.match` = `상위` 로 낸다(`concern_candidates` · `coverage`) ② **HG2 하위 = 자손 전부** — 「하위 *」 role 은 `g_scope` 의 하위 role 행을 **끝까지** 따라간다(`scope` · `facets` · `pair` · `coverage` — 0.5.1 의 「한 단」 · O-21 (a) 를 바꿨다) ③ **HG3 고민 + 부위 → `concern_site`** — `concern_candidates` 의 `site` 맞춤을 행의 부위 글자 일치에 「그 부위에 묶인 고민(과 그 하위 고민)의 행」 까지 넓힌다. **gold 15표 · gold 해시는 바뀌지 않는다.** HG3 은 보조 입력이 하나 는다(silver `concern_site` — **사용자 결정 U-4** · §10). 사용자가 정할 것은 §10 맨 위 표의 **U-3 · U-4** 둘이다(앱 쪽 U-1 · U-2 는 SPEC-002 §11).

- 0.7.0 에서 **상담 화면이 쓰는 재료 셋**을 더했다(§5-11 — _RESUME §2 11-17 「얼굴 점 = 대화에서 나온 고민 부위 …」 · §1 「수정 2 목록」 00 · 2 · 6. 한 문항의 예외가 아니라 일반 규칙이다): ① **DP 시술로 내려가기** — `concern_candidates` 가 시술 코드 없이 남기던 행(`modality_only[]` · `unreached[]` — 계열 · 메뉴(패키지) · 제품에 닿은 적응)을 `g_scope` 로 끝까지 따라가 **시술(PRC)** 로 내려 새 쪽 밖 목록 `descended[]` 에 **계열 단위 묶음**으로 낸다. 어디를 거쳐 내려왔는지(`from[].path[]`)를 붙이고, 메뉴 · 패키지 · 제품은 경로에만 남는다 — 시술 후보(`groups[]`)에는 들어가지 않는다 ② **CS 고민 부위** — `concern_candidates` 머리에 그 고민(과 하위 고민)의 부위 코드 목록 `sites[]`(silver `concern_site` — 이미 있는 보조 입력 ③) ③ **NM 이름 맞춤 보강** — `resolve` 맞춤 꼴에 **줄임 일치**(낱말 둘 이상인 이름의 앞 낱말을 줄여 말한 꼴 — `matched.how` = `줄임`)를 더한다. **기존 응답 필드 · 순서 · `total` 은 한 글자도 바뀌지 않는다**(필드가 늘 뿐이다 — 지시서 「응답 필드 추가는 기존 필드를 바꾸지 않음」). **gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 도 그대로다**(새 입력 0 — 셋 다 이미 메모리에 있는 `g_scope` · `concern_site` · `g_entry.text` 만 읽는다). CSV 판 · DB 판 응답은 같다(SPEC-003 §5 P2). 사용자가 정할 것은 §10 맨 위 표의 **U7-1 · U7-2 · U7-3** 셋이다. (0.7.1 — 셋 다 11-17 에 (a) 로 정해졌다 · §10)

- 0.7.1 에서 **0.7.0 검수의 WARN 6 · NOTE 8 을 닫고**(`$W/review-spec-001-v07.md` — 수 고침 · `lands` = `procedure` 꼴 · 도구 설명 문장 · 한 글자 낱말 규칙 · 줄임 오매칭 근거 · 변경 기록 0.7.1) **규칙 하나를 더했다**(§5-11 SP — _RESUME §2 11-17 「① 규칙(사용자 결정)」): **부위가 묶이지 않은 고민**(`sites[]` 가 `[]` 인 고민 — 260 가운데 160)에 `site` 를 걸면 **부위로 거르지 않는다** — 그 고민의 행을 전부 내고, 부위가 맞는 행에만 「우선 표시」 표지(`site_prefer`)를 단다. 응답 머리 `site_applied` 가 `filter`(거름 — HG3 그대로) 인지 `prefer`(안 거름)인지 알린다. **부위가 묶인 고민 100 은 0.7.0 과 같은 응답이다**(HG3 그대로 — 회귀 0). U7-1 ~ U7-3 은 11-17 에 (a) 로 닫혔다. gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 는 그대로다(새 입력 0). **WORK 전 사용자 결정 = 0.**

- 0.7.2 에서 **SP 의 기준 한 줄을 바꿨다**(§5-11 SP1 — _RESUME §2 11-17 「규칙 변경 = 넣음」 · 까닭은 `$W/research-concern-site.md` §0-5): 「고민 + 부위」 는 **물은 부위가 그 고민의 부위(자기 + 하위 고민 — `sites[]` 와 같은 집합) 안에 있을 때만** 부위로 거른다(HG3 · `site_applied` = `filter`). 그 밖 — 고민에 부위가 없거나, **부위가 있어도 물은 부위가 그 안에 없으면** — 거르지 않고 우선 표시(`prefer`)다. 0.7.1 은 「고민에 부위가 없을 때만 `prefer`」 였다. 고민 260 × 부위 이름 89 = 23,140 짝 가운데 `filter` 는 8,900 → **191** 짝 · `prefer` 는 14,240 → **22,949** 짝이고, 바뀌는 8,709 짝 가운데 0.7.1 에서 **0 행이던 8,444 짝이 전부 그 고민의 행을 낸다**(O-31 ① 닫힘). **물은 부위가 안에 있는 191 짝은 0.7.1 과 같은 행이다**(회귀 0). 새 필드 · 새 입력 · 이름 변화 0 — `site_applied` 를 정하는 식만 바뀐다. gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 그대로. **WORK 전 사용자 결정 = 0.**

- 0.8.0 에서 **`resolve` 맞춤 꼴을 「정확한 이름 → 코드」 로 줄였다**(§4-1 · §5-1 R2 — _RESUME §2 11-18 D-1 · 「허브 resolve = 최소 목록 꼴(입구 목록 출력) · 규칙을 더하지 않는다 · 입력 정리는 채팅(앱) 단에서」): `text` 의 `norm` 이 `g_entry.norm` 과 **같을 때만** 후보다. **부분 일치(0.5.0 R2) · 덮임(R7 `matched.covered_by`) · 줄임(0.7 NM · 입력 `abbr` · `matched.how` · `matched.full`)을 지웠다.** 문장에서 대상을 고르는 일은 허브가 아니라 부르는 쪽이 한다 — 상담(SPEC-008)은 **목록 꼴**(0.4.0 부터 있던 것 · **바뀌지 않는다**)로 입구 820 개와 별칭을 받아 소넷이 고른다. 까닭: 글자 맞춤이 관문이면 조사가 끼거나 어순이 바뀌거나 바꿔 말한 턴에서 정답이 후보에 없다(`$W/research-input-space.md` §2 — 채점 239 턴 가운데 후보 층 실패 39). **다른 도구 8 의 계약 · gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 는 그대로다.** 이 문서의 0.5.0 · 0.7.0 · 0.7.1 문단(위)은 그 판의 계약을 적은 것이고 `resolve` 에 대해서는 이 판이 앞선다. 시험 앱 B 열은 고치지 않고 허브 0.7.2 옛 판에 묶는다(D-2 — 변경 기록 0.8.0 「쓰는 곳별 영향」). **WORK 전에 볼 것 = O-32 · O-33**(§10 — 코디).

## 1. 목적 · 범위

### 1-1. 목적

11-16 확정한 새 gold 15표를 허브에서 읽을 수 있게 한다. 쓰는 쪽은 둘이다 — ① 채팅 시험 앱(SPEC-002 의 B 열은 REST 로 걷고, C 열은 LLM 이 MCP 로 직접 묻는다) ② 나중에 stg 에서 이 gold 를 쓸 다른 서비스(_RESUME §2 11-16 「stg 에 올린다 — 다른 서비스도 쓰게」).

### 1-2. 허브가 하는 것

| # | 하는 것 | 근거 |
|---|---|---|
| 1 | gold CSV 15 + `source_ref` + 보조 입력(계층 3표 · 원장 확인 목록)을 시작 때 메모리로 적재 · 파일 해시 기록 | _RESUME §2 11-16 「D2」 「D3」 · 「검수 뒤 결정 4」 ② ③ |
| 2 | 결정론 조회 도구 9(§4) — 같은 입력 · 같은 build 면 같은 응답 | 조사 §6-3 · _RESUME §2 11-16 「D4 추천대로」(8) + 0.5.0 `coverage`(제안 — O-19) |
| 3 | REST · MCP 두 입구 · 같은 service 코어 | 조사 §0 D5 · _RESUME §2 11-16 「D5 추천대로」 |
| 4 | 응답 머리에 build(gold 해시) · 행마다 되짚기 키 | 조사 §1-4 · `artifact-traceability.md` 「공통 식별자 · 관계 · 버전」 |

### 1-3. 범위 밖(이 스펙에서 만들지 않음)

| 범위 밖 | 이유 |
|---|---|
| gold 빌드 · 검사 | gold 는 이미 `gold-build.py` 가 만들고 `gold-check.py` 가 검사한 CSV 다. 허브는 적재만(조사 §3-3 「빌드 — 버린다」) |
| DB 적재 · alembic | 시험 뒤 「다음 범위」(_RESUME §2 11-16 「D2」 · semantic-map §7 결정 4) |
| LLM · Jev 호출 · 답 문장 · 추천 판단 | 허브 = 결정론. 판단은 앱(SPEC-002) |
| 질문 범위 고르기 · 걷기 · hard gate | 앱 몫(SPEC-002 §3 · §4). 허브는 gate 가 볼 칸을 빠뜨리지 않고 낸다 |
| `questions.csv` 적재 | 앱 시험 세트(조사 §6-2 「허브에 올리지 않음」) — 단 해시 식에는 들어간다(§2-3 · O-3) |
| 비교 · 문헌 · 번역 도구 | gold 표 없음(조사 §3-1 T6 · semantic-map §7 결정 5) |
| 옛 gold 체계(노드 13종 · fact section 18 · intent 12 · 봉투) | 이어 쓰지 않는다(_RESUME §2 11-16 첫 행) |
| 머지 · 배포 · stg 데이터 반입 | 각각 별도 승인(_RESUME §2 11-16 「stg」) |

### 1-4. 코드 자리

- 레포 PROCEDURE-HUB · base `release/v1.2.0` · **새 브랜치 · 새 모듈**(_RESUME §2 11-16 「stg」 행 「허브 새 브랜치(base release/v1.2.0)」 · 브리프 §2 D1 · 조사 §6-1 (a)).
- `release/v1.2.0` 에는 `graph_main.py` 도 MCP 도 없다(조사 §3-3 첫 행) — 옛 PR #31 에서 **틀만** 옮긴다(§7).
- 모듈 · 경로 · 서버 이름은 **제안**이다(O-5):

| 무엇 | 제안 이름 | 근거 |
|---|---|---|
| 모듈 | `backend/app/modules/gold/` | `release/v1.2.0` 에 같은 이름 없음(`git ls-tree origin/release/v1.2.0 backend/app/modules/`) |
| REST prefix | `/procedure-hub/gold` | Gateway 경로가 `/procedure-hub/*`(`deployment.md:134`) · 옛 틀 `HUB-OLD backend/app/modules/gold/config.py:23` |
| MCP 마운트 | `/procedure-hub/gold-mcp` | 옛 틀 `config.py:24` |
| MCP 서버 이름 | `procedure-hub-gold` | 옛 틀 `mcp_server.py:22` |

## 2. 입력 데이터

### 2-1. 파일

| 입력 | 파일 | 행(11-16 gold) | 근거 |
|---|---|---:|---|
| gold 15표 | `g_entry` · `g_scope` · `g_profile` · `g_indication` · `g_outcome` · `g_adverse` · `g_adverse_detail` · `g_recovery` · `g_contraindication` · `g_pair` · `g_package` · `g_offer` · `g_node` · `g_edge` · `g_evidence` (`.csv`) | 조사 §1-1 표 | `$SM/gold/README.md:7-22` |
| silver 근거 포인터 | `source_ref.csv`(헤더 `target_table,target_id,field,ref`) | 48,094 | `$SM/silver/source_ref.csv` · _RESUME §2 11-16 「D3 추천대로」 |
| 보조 입력 ① 계층 | silver `concern.csv` · `adverse.csv` · `condition.csv` — **`code` · `parent_code` 두 칸만** 메모리에 둔다 | 260 · 188 · 151 | `$SM/silver/` · _RESUME §2 11-16 「검수 뒤 결정 4」 ② |
| 보조 입력 ② 원장 확인 목록 | `ledger-check-list.csv` — **`id` 와 코드만** 메모리에 둔다. 코드는 `silver_now` · `what` · `name` 세 칸에서 뽑는다(아래) | 325 | `$SM/notes/ledger-check-list.csv` · _RESUME §2 11-16 「검수 뒤 결정 4」 ③ |

| 보조 입력 ③ 고민 ↔ 부위(**0.5.2 — 제안 · 사용자 결정 U-4**) | silver `concern_site.csv` — **`id` · `concern_code` · `site_code` 세 칸**(헤더가 이 셋뿐이다) | 95 | `$SM/silver/concern_site.csv` · `$W/_RESUME.md` §1 e2e 피드백 4 · 「허브 묶음 발주」 ③ · §5-9 HG3 |

- CSV 는 UTF-8 BOM · `,` 구분(`$SM/gold/README.md:24`). **칸은 전부 문자열로 둔다** — 숫자 칸(`*_min` · `*_max` · `price_*`)도 바꾸지 않는다(조사 §6-2 「값 변환 없이」 · gold 값 = silver 값).
- **레포에 CSV 를 커밋하지 않는다**(공개 금지 · 조사 §6-2 끝 줄). 경로는 env 로만 받는다.

**보조 입력이 지킬 것**(_RESUME §2 11-16 「검수 뒤 결정 4」 ② ③)

| # | 지킬 것 | 근거 |
|---|---|---|
| X1 | **gold 는 불변이다.** 보조 입력은 gold 에 칸 · 행을 더하지 않고 gold 해시에도 들어가지 않는다(§2-3) | 결정 ② 「gold 불변」 |
| X2 | 계층 3표는 `code` · `parent_code` 만 쓴다. 이름 · 설명 · `level` 같은 다른 칸은 메모리에 두지 않고 응답에 싣지 않는다 — 이름은 gold 행의 칸(`concern_name` …)에 이미 있다 | 결정 ② 「`code` · `parent_code`」 |
| X3 | 계층은 3표 모두 **3단**(뿌리에서 최대 2단 아래)이고 부모 없는 `parent_code` 는 0 이다(이 워커 셈: 부모가 있는 값 — 고민 243 / 260 · 부작용 173 / 188 · 조건 136 / 151) | `$SM/silver/*.csv` |
| X4 | 원장 확인 목록은 `id` 와 **코드만** 남긴다. 코드 추출식은 `gold-build.py` 와 같다 — `silver_now` · `what` · `name` 세 칸을 이어 붙인 글에서 「코드 접두어 9종 + `-` + 숫자」 꼴을 찾는다 | `gold-build.py:648-651` · 결정 ③ 「id · 코드만」 |
| X5 | 원장 확인 목록의 글 칸(`what` · `evidence` · `question` · `silver_now` …)은 **메모리에 남기지 않고 응답에 싣지 않는다.** 응답에는 id 와 코드만 나간다(§4-0 `ledger_check[]`) | 결정 ③ · 공개 레포 규칙 |
| X6 | 325 행 중 코드가 뽑히는 행은 251 · 서로 다른 코드 218 · 한 코드에 id 최대 4(이 워커 셈). 코드가 안 뽑히는 74 행은 `ledger_check[]` 에 닿지 않는다 — 그 한계는 문항 ↔ LCK 잇기(SPEC-002 O-10)와 같다 | `$SM/notes/ledger-check-list.csv` |

| X7 | (0.5.2 · U-4 를 (a) 로 정했을 때) 보조 입력 ③ 은 `id` · `concern_code` · `site_code` 만 있다 — 글 칸이 없다. **gold 에 칸 · 행을 더하지 않고 gold 해시에도 넣지 않는다**(X1 과 같다 · `aux_hash` 에 넣는다 — §2-3 4). 95 행 · 고민 85 · 부위 51(전부 `g_entry` 의 site 입구에 있고 이름이 같다) · `source_ref` 에 이 표의 행이 574 있다(이 워커 셈) | `$SM/silver/concern_site.csv` · `source_ref.csv` |

### 2-2. env(이름 제안 — O-5)

| env | 뜻 | 필수 | 없을 때 |
|---|---|---|---|
| `GOLD_CSV_DIR` | gold 폴더(15표가 있는 곳) | 필수 | 시작 실패 |
| `GOLD_SOURCE_REF_PATH` | `source_ref.csv` 경로 | 필수 | 시작 실패 |
| `GOLD_HIERARCHY_DIR` | 계층 3표(`concern.csv` · `adverse.csv` · `condition.csv`)가 있는 폴더. **0.5.2(U-4 (a)) — 같은 폴더의 `concern_site.csv` 도 여기서 읽는다**(silver 폴더 하나 — env 를 늘리지 않는다 · 제안) | 필수 | 시작 실패 |
| `GOLD_LEDGER_CHECK_PATH` | `ledger-check-list.csv` 경로 | 필수 | 시작 실패 |
| `GOLD_EXPECTED_HASH` | 기대 gold 해시(§2-3) | 선택 | 대조 없이 기록만(**제안** — O-12) |
| `GOLD_PAGE_LIMIT_DEFAULT` · `GOLD_PAGE_LIMIT_MAX` | 쪽 크기 기본 · 최대(§4-0) | 선택 | 제안 기본값(O-6) |
| `GOLD_MCP_ALLOWED_HOSTS` · `GOLD_MCP_ALLOWED_ORIGINS` | (0.8.2) MCP 의 Host · Origin 허용 목록 — 쉼표 목록 · 값은 `<호스트>` 또는 `<호스트>:*`(아무 포트). **DNS rebinding 보호는 늘 켠 채** 로컬 기본(`127.0.0.1` · `localhost` · `[::1]` 의 아무 포트)에 **더한다**(`assembly.py` `mcp_transport_security`). 목록 밖 Host = `421` · 목록 밖 Origin = `403` | 선택 | 로컬 기본만 — 로컬 밖에서 부르면 `421`. **stg 는 두 값을 둔다**: Gateway 공개 호스트 **와 백엔드 내부 주소**(`<백엔드 내부 주소>:<포트>`) — Gateway 가 Host 를 백엔드 내부 주소로 바꿔 넘기므로 공개 호스트만 두면 `421` 이다(stg 실측 · `stg-runbook.md` 실행 기록) |
| `GOLD_LOAD_TIMEOUT_SECONDS` | (0.8.2) `app.main` 에 붙인 gold 의 시작 적재 시간 한도(초) — 넘으면 gold 만 꺼짐(`unavailable` · 이유 「적재 시간 초과」). `gold_main` 에는 한도가 없다 | 선택 | 기본 `60`. stg 는 `30`(실측 적재 6.3초 — SPEC-003 §11-2 · §11-7) |

env 파일 규칙은 옛 틀(`HUB-OLD backend/app/modules/gold/config.py:15-20` — pydantic-settings · git 제외 env 파일 또는 프로세스 env)을 따른다.

### 2-3. 적재 · 해시

1. 서버 시작(lifespan) 때 **한 번** 읽는다. 요청은 메모리만 읽는다(옛 틀 `HUB-OLD backend/app/modules/gold/memory.py:1-3`). gold 가 바뀌면 **재시작**으로 반영한다.
2. 파일마다 `sha256(파일 바이트)` 와 행 수를 기록한다.
3. **gold 해시** = `gold-check.py` 와 같은 식(`$SM/gold/gold-check.py:46-50`): gold 폴더의 `*.csv` 를 이름순으로 `「파일 이름 + 공백 + sha256」` 줄로 모아 다시 sha256. 11-16 값 = `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c`(조사 §1-0).
   - 이 식은 폴더의 **CSV 전부**를 본다 — 15표 + `questions.csv` = 16 파일(이 워커가 같은 식으로 다시 셈 → 위 값과 같음). 허브는 `questions.csv` 를 **적재하지 않지만 해시에는 넣어야** gold-check 값과 같아진다(O-3).
4. `source_ref.csv` 와 보조 입력 4 파일(`concern.csv` · `adverse.csv` · `condition.csv` · `ledger-check-list.csv`)은 **gold 해시에 넣지 않고** 파일마다 sha256 을 따로 기록한다(gold-check 식에 없음 · §2-1 X1).
   - 0.5.2(U-4 (a)): 보조 입력 ③ `concern_site.csv` 가 더해지면 보조 파일은 **5**(+ `source_ref` = 6 파일)가 되고 `aux_hash` 식에 함께 들어간다 — 아래 「5 파일」 은 「6 파일」 로 읽는다. 0.5.1 build 의 `aux_hash` 와 값이 달라진다(cursor 는 build 에 묶여 있어 옛 cursor 는 `cursor_invalid`).
   - 이 5 파일도 응답을 바꾼다 — 그래서 **보조 해시** `build.aux_hash` 를 함께 낸다(**제안** — O-12): gold 해시와 같은 식을 이 5 파일(이름순 · `「파일 이름 + 공백 + sha256」` 줄)에 쓴 값. 「같은 입력 · 같은 build 면 같은 응답」 의 build = (`gold_hash`, `aux_hash`).
5. **적재 실패 = 시작 실패**(브리프 §3). 조건 — 결정이 정한 것: 필수 env 없음 · 파일 없음. **제안**(O-12): gold · `source_ref` 헤더가 부록 A 와 다름 · 보조 입력에 쓸 칸(부록 A 끝 다섯 줄)이 없음 · `GOLD_EXPECTED_HASH` 가 있는데 다름. 옛 틀은 발행본이 없어도 경고만 하고 떴다(`HUB-OLD backend/app/modules/gold/service.py:38-40`) — **그 동작은 가져오지 않는다.**
6. 허브는 gold 를 **다시 검사하지 않는다**(되짚기 · 값 ⊂ silver 등은 gold-check 책임 — 조사 §6-2). 다만 적재 때 센 값을 `health.integrity` 에 낸다(**제안** — O-12): 「근거 없는 gold 행」 · 「`source_ref` 짝 없는 참조」(11-16 gold 에서 둘 다 0 — 조사 §1-4) · 「같은 표에 부모가 없는 `parent_code`」(11-16 silver 에서 0 — §2-1 X3).

## 3. 계층

```
REST router ─┐
             ├─▶ service(도구 9 코어 · 입력 검증 · 쪽 넘김 · 층 표시) ─▶ repository(조회 메서드) ─▶ 메모리 색인
MCP server ──┘                                                            └ 나중: DB 구현으로 교체
```

| 층 | 하는 것 | 모르는 것 | 근거 |
|---|---|---|---|
| router(REST) | 경로 · 쿼리 → 코어 호출 · 응답 JSON | 색인 · CSV | 옛 틀 `HUB-OLD backend/app/router/gold.py`(코드가 놓일 PROCEDURE-HUB 의 틀). 프로필 레포의 `app/back/` 규약(`$P/CLAUDE.md` §4)과 **같은 꼴**일 뿐 그 규약이 근거는 아니다 |
| MCP server | 도구 정의 · 같은 코어 호출 · 도메인 예외 → 같은 문구의 tool 오류 | 색인 · CSV | 옛 틀 `mcp_server.py:55-59` |
| service | 도구 9 의 규칙(§5) · 입력 검증 · cursor · `layer` 붙이기 | HTTP · MCP · CSV · dict 꼴 | 옛 틀 `service.py:1` 「REST · MCP 공용」 |
| repository | 아래 조회 메서드만 연다. **지금 구현 = CSV 메모리** | 도구 규칙 | _RESUME §2 11-16 「repository 층만 바꾸면 되게」 |

- service 는 repository 의 **인터페이스(조회 메서드)** 만 쓴다. CSV 행 dict · 색인 dict 를 직접 만지지 않는다 — 그래야 DB 구현으로 바꿀 때 service · router · MCP 가 그대로다.
- 메모리 상태는 Singleton, 도구 서비스는 요청마다 새 인스턴스(옛 틀 `HUB-OLD backend/app/modules/gold/container.py:17-18`).

### 3-1. 메모리 색인(조사 §6-2 의 색인 열 그대로)

| 표 | 색인 키 |
|---|---|
| `g_entry` | `norm` · (`entity_table`, `entity_code`) · `entity_table`(입구 목록 — §4-1) |
| `g_scope` | (`subject_table`, `subject_code`) · (`holder_table`, `holder_code`) |
| `g_profile` | (`subject_table`, `subject_code`) — 유일 |
| `g_indication` | `asked_concern_code` · (`target_table`, `target_code`) · `procedure_code` · `concern_code` |
| `g_outcome` | (`target_table`, `target_code`) · `effect_code` |
| `g_adverse` | (`target_table`, `target_code`) · `adverse_code` |
| `g_adverse_detail` | `adverse_risk_id` · (`target_table`, `target_code`) |
| `g_recovery` | (`target_table`, `target_code`) |
| `g_contraindication` | (`target_table`, `target_code`) · `condition_code` |
| `g_pair` | (`from_table`, `from_code`) · (`to_table`, `to_code`) · `question_class` |
| `g_package` | `package_id` · `concern_code` · (`item_table`, `item_code`) |
| `g_offer` | `offer_id` · (`item_table`, `item_code`) · `procedure_code` |
| `g_node` | `node_id` |
| `g_edge` | (`src`, `edge_type`) · (`dst`, `edge_type`) |
| `g_evidence` | (`gold_table`, `gold_id`) |
| `source_ref` | (`target_table`, `target_id`) |
| (전 표) | `gid`(또는 `node_id` · `edge_id`) → 행 |
| 보조 ① 계층 — `concern` · `adverse` · `condition` | 표마다 `code` → `parent_code` · `parent_code` → 자식 `code[]` |
| 보조 ② 원장 확인 목록 | 코드 → `id[]`(id 오름차순) |
| 보조 ③ 고민 ↔ 부위(0.5.2 — U-4 (a)) | `site_code` → (`concern_code`, `id`)[] · `concern_code` → `site_code`[] |
| 하위 닫힘(0.5.2 — §5-9 HG2 · 계산) | 대상마다 「하위 *」 role 의 `g_scope` 행을 끝까지 따라간 holder 목록(`depth` · `via`) — 적재 때 한 번 세거나 요청 때 따라간다(구현 때 정함) |
| ~~줄임 열쇠(0.7 — §5-11 NM · 계산)~~ | **0.8.0 에서 없앴다** — 적재 때 줄임 열쇠를 짓지 않는다(0.7.2 까지: `g_entry.text` 의 낱말이 2 이상인 행마다 지은 열쇠 2,881 → `g_entry` 행). `norm` → `g_entry` 행 색인은 그대로다(맞춤 꼴 R2 가 그것 하나로 찾는다). 두 판(CSV · DB)에서 함께 없어진다 |
| 시술로 내려가기(0.7 — §5-11 DP) | **새 색인 없음** — `g_scope` 의 (`subject_table`, `subject_code`) 색인을 요청 때 따라간다(HG2 와 같은 꼴) |
| 고민 부위(0.7 — §5-11 CS) | **새 색인 없음** — 보조 ③ 의 `concern_code` → `site_code`[] 색인(0.5.2 부터 있다 — `HUB backend/app/modules/gold/repository.py:77` `sites_of_concern`) + 묶임 `id` |
| 속성 쪽(§4-4 · §5-7) — 재료 · 방법 · 해부 · 부위 | 맞춤 칸마다 **칸 값(항목) → 행**: `g_profile` 의 `materials` · `methods`(` · ` 로 나눈 항목) · `anatomy_name` · `site_name` / `g_indication` 의 `site_code` · `site_name` · `case_site_name` / `g_outcome` · `g_adverse` · `g_contraindication` 의 `site_name` / `g_adverse_detail` 의 `anatomy_name` · `site_name` / `g_offer` 의 `materials` · `sites`(항목) |

`g_entry` 의 (`entity_table`, `entity_code`) 색인은 값 대상의 **「gold 에 있음」 기준**으로도 쓴다(§4-0 「있음」).

repository 메서드는 이 색인 하나에 하나씩 대응한다(이름은 WORK 에서). DB 로 가면 같은 키가 테이블 색인이 된다(조사 §6-2 표) — 보조 입력 둘도 같은 repository 뒤에 둔다(service 는 「상위 · 하위 코드 묻기」 · 「코드의 원장 확인 id 묻기」 메서드만 안다).

## 4. 도구 9 계약

### 4-0. 공통

**대상 표기** — 노드는 `표:코드` 문자열(`g_node.node_id` 와 같은 꼴 — `$SM/gold/gold-build.py:606`). `scope` · `facets` · `pair` 는 `g_node` 에 없는 대상도 받는다(`g_node` 는 엣지 끝이 된 것만 — 조사 §1-2). `neighbors` 는 `g_node` 에 있는 것만.

**응답 머리**(모든 도구)

| 필드 | 뜻 |
|---|---|
| `build.gold_hash` | §2-3 의 gold 해시 |
| `build.aux_hash` | §2-3 4 의 보조 해시(**제안** — O-12) |
| `build.loaded_at` | 적재 시각(ISO 8601) |
| `request` | 기본값을 채운 입력 그대로. 기본값이 「전부」 인 입력(`scope.roles` · `pair.classes` · `coverage.kinds`)은 **`null` = 전부**로 돌려준다(되적기 — 허브 검수 N-3 · `HUB backend/app/modules/gold/service.py:65`) |
| `total` | 이 조회의 전체 수(쪽과 무관). **단위는 도구마다 다르다 — 아래 「`total` 단위」 표** |
| `next_cursor` | 다음 쪽이 있으면 문자열 · 없으면 `null` |
| `ledger_check[]` | 이 조회의 코드에 걸린 원장 확인 id(`concern_candidates` · `facets` · `pair` 만 — 아래 「원장 확인」) |

**`total` 단위**(검수 W-8) — 쪽 단위와 `total` 단위는 늘 같다. 「cursor 로 끝까지 넘긴 쪽 단위의 합 = `total`」(§9 T6).

| 도구 | `total` · 쪽 단위 | 쪽 밖 목록(첫 쪽에만) |
|---|---|---|
| `resolve` | `candidates` 수 — 맞춤 꼴(`text`)은 쪽 넘김 없음(부분 일치 후보 전부 — §4-1) · **목록 꼴(`text` 없이 `range` · `tables`)은 `candidates` = `g_entry` 행 · 쪽 넘김 있음**(§4-1) | — |
| `scope` | `holders` = `g_scope` 행 | — |
| `neighbors` | `items` = 엣지 | — |
| `facets` | `rows` = 그 facet 표의 행 | `ledger_check[]` |
| `concern_candidates` | **`groups` = 묶음** (`g_indication` 행 수는 `counts.rows`) | `modality_only[]` · `unreached[]` · `ledger_check[]` · **0.7**: `descended[]` · `sites[]` |
| `pair` | `rows` = `g_pair` 행 | `same_day_packages[]` · `ledger_check[]` |
| `evidence` | **`source_refs` 를 편 줄**(참조 × 그 참조의 `source_ref` 행 · `source_ref` 가 0 인 참조는 1줄로 센다). 한 쪽은 그 줄들을 참조별로 다시 묶어 `refs[]` 로 낸다 | — |
| `health` | 없음 | — |
| `coverage` | `items` = 요청한 노드 수 — 쪽 넘김 없음(§4-9) | — |

- **쪽 밖 목록은 첫 쪽(cursor 없는 요청)에만 싣고** 뒤 쪽에서는 뺀다. **크기 한도는 없다 — 통째로 싣는다**(재검수2 X-2). 쪽 밖 목록에는 쪽 넘김이 없어 한도를 두면 곧 잘라 내기가 되므로(원칙 — _RESUME §2 11-16 「원칙: 질문에 빠지는 정보가 있으면 안 된다」) 「자르는 한도」 는 선택지에 없다. 11-16 gold 에서 한 고민의 「계열 층만」 최대 40 행 · 못 닿은 행 최대 16 행(검수 W-8 셈)이라 지금은 작다. 커져서 한 응답에 싣기 어려워지면 그 목록을 **쪽 넘김 대상으로 옮긴다**(O-6 — 한도가 아니라 쪽 단위를 주는 것).
- `counts*` · `distinct_nodes` 같은 머리 셈은 쪽과 무관한 값이며 **모든 쪽에** 싣는다. `facets` 의 `counts.distinct_rows`(서로 다른 `gid` 수 — §4-4)도 같다.

**「있음」 — `not_found` 와 행 0 의 경계**(검수 W-7)

| 받는 것 | 「gold 에 있음」 기준 | 없으면 |
|---|---|---|
| 대상(modality · procedure · procedure_case · product) · 패키지 — `scope.node` · `facets.node`(대상 쪽) · `pair.a` · `pair.b` | `g_scope` 의 (`subject_table`, `subject_code`) 색인에 있음 | `not_found` |
| 값(concern · effect · adverse · condition · offer) — `facets.node`(값 쪽) · `concern_candidates.concern_code` | `g_entry` 의 (`entity_table`, `entity_code`) 색인에 있음 | `not_found` |
| 속성(material · method · anatomy · site) — `facets.node`(속성 쪽 — §4-4) | 같음 — `g_entry` 의 (`entity_table`, `entity_code`) 색인에 있음(11-16 gold: 재료 143 · 방법 49 · 해부 105 · 부위 89 — _RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) · 이 워커 재셈) | `not_found` |
| `neighbors.node_id` | `g_node.node_id` 에 있음 | `not_found` |
| `evidence` 의 (`gold_table`, `gold_id`) | 그 표의 키에 있음 | `not_found` |
| `coverage.nodes[]` 의 각 항목 | 위 대상 · 값 · 속성 기준 그대로(표에 따라) | 하나라도 없으면 `not_found`(어느 항목인지 문구에 적는다) |

- **있음 + 행 0 = `200` · `total: 0`**(오류 아님). `g_entry` 에는 있으나 `g_node` 에 없는 값(엣지 끝이 된 적 없는 값 — 검수 W-7 셈: concern 18 · condition 39 · adverse 15 · effect 14 · offer 18)이 이 꼴이다. Q10 이 그 예다(§9). 속성 4표는 **전부 `g_node` 에 없다**(노드가 아닌 입구 — 조사 §1-2) — 그래도 `g_entry` 에 있으므로 「있음」 이고, 맞춤 칸 어디에도 안 나오는 코드(재료 4 · 방법 10 · 해부 56 · 부위 36 — 이 워커 셈)는 `200` · `total: 0` 이다.
- 이 경계가 앱의 「입구 0」(`resolve` 맞춤 꼴 후보 0 — 앱은 여기서 입구 고르기로 간다 · SPEC-002 §3-1 단계 ①-4) · 「원천 미확정 / 후보 소진」(있음 + 행 0)을 가른다(SPEC-002 §5).

**행 필드**

- **gold 표 칸은 CSV 헤더 이름 그대로** · 값도 그대로(문자열). 도구가 행을 「그대로」 낸다고 적은 곳은 그 표의 전 칸이다(부록 A).
- 행마다 `gold_table`(표 이름) · `gid`(그 표의 키) · `evidence_kind`(헤더에 있음)가 있다. `g_edge` 행은 `edge_id` 가 키이고 `gold_table` + `gold_id` 가 속성 행을 가리킨다(헤더 그대로).
- `g_scope` 로 펼쳐 얻은 행에는 **`layer`**(계산 필드)가 붙는다: `layer.role` · `layer.path` · `layer.holder{holder_table, holder_code, holder_name}` · `layer.scope_gid`(그 `g_scope` 행의 `gid`). 값은 `g_scope` 칸 그대로. `role` 이 「자기」 여도 붙인다 — 앱이 층을 추측하지 않게(조사 §1-4 「행마다(물려받음일 때)」 를 전 행으로 넓힌 것 · hard gate 4 에 필요).
- 계층으로 넓혀 얻은 행에는 **`hier`**(계산 필드)가 붙는다: `hier.asked_code`(요청이 준 코드) · `hier.match`(`직접` \| `상위` \| `하위` — 그 행의 코드가 요청 코드 자신인가 · 그 상위인가 · 그 하위인가). 넓힘이 없는 조회에는 붙지 않는다(§4-4 · §5-5).
- 속성 쪽으로 얻은 행에는 **`attr`**(계산 필드)가 붙는다: `attr.asked_table` · `attr.asked_code`(요청이 준 속성 코드) · `attr.column`(그 행에서 맞은 칸 이름 — 여러 칸이 맞으면 전부 · 헤더 순서). 값은 요청 · 헤더 이름 그대로다(§4-4 「속성 쪽」).
- 계산 필드는 도구마다 표에 **「계산」** 으로 적는다. 그 밖의 필드는 전부 헤더다.

**원장 확인 — `ledger_check[]`**(머리 · 계산 · _RESUME §2 11-16 「검수 뒤 결정 4」 ③)

| 필드 | 뜻 |
|---|---|
| `code` | 원장 확인 목록에서 맞은 코드 |
| `lck_ids[]` | 그 코드에 걸린 원장 확인 id(`ledger-check-list.csv` 의 `id` 그대로 · 오름차순) |
| `on` | 그 코드가 어디서 왔나 — `request`(요청이 준 코드) \| `rows`(조회 전체 행의 키 코드) |

| 도구 | 대조하는 코드 | 근거 |
|---|---|---|
| `concern_candidates` | `request`: `concern_code` | `gold-build.py:705-706 · 716` |
| `facets` | `request`: `node` 의 코드 · `filters` 값 중 코드 꼴 / `rows`: facet = `offer` 일 때 **조회 전체 행**(쪽과 무관)의 `offer_id` | `gold-build.py:899-901` |
| `pair` | `request`: `a` · `b` 의 코드 | 같은 식을 두 끝에 |

- **순서**(재검수 R-2): 항목은 `on`(`request` 먼저 → `rows`) → `code` 오름차순(문자열 비교)으로 놓는다. 항목 안 `lck_ids[]` 는 오름차순이다. 같은 입력 · 같은 build 면 순서까지 같다(§9 T6 · T10).
- **겹침**(재검수 R-2): 같은 코드가 `request` 와 `rows` 양쪽으로 맞으면(예: 값 쪽 `node` = offer 이고 그 `offer_id` 가 조회 행에도 있음) **둘 다 낸다** — 항목 둘(`on` 만 다름). 앱의 「원천 미확정」 (나) 는 `on` = `rows` 항목을 보므로(SPEC-002 §5) 하나로 접으면 그 재료가 사라진다. (`code`, `on`) 짝은 응답 안에서 유일하다.
- 맞은 것이 없으면 **빈 목록 `[]`** 을 낸다(필드를 빼지 않는다) — 「원장 확인 항목 없음」 과 「대조하지 않음」 을 가르기 위해서다. 위 세 도구 밖의 응답에는 이 필드가 없다.
- `ledger_check[]` 는 **행 · `total` · 오류를 바꾸지 않는다.** 허브는 「원천 미확정」 을 판정하지 않는다 — 재료(id · 코드)만 낸다. 판정은 앱(SPEC-002 §5 의 세 조건).
- 허브는 대조하는 코드를 **넓히지 않는다** — `g_scope` 로 펼친 holder 코드 · 계층으로 넓힌 코드는 대조하지 않는다. gold-build 가 본 두 자리(물은 코드 · 못 닿은 상품의 `offer_id`)와 요청 코드까지다. **이 범위는 결정이다**(_RESUME §2 11-16 「재검수(r2) 뒤 결정 2」 — 「원장 확인 대조 범위 지금대로(요청 코드 + 상품)」 · 옛 O-14). holder 코드까지 넓힐지는 **1회차 trace 를 본 뒤** 다시 정한다 — 이번 판에서는 넓히지 않는다.
- 응답에는 id 와 코드만 나간다. 원장 확인 목록의 글은 나가지 않는다(§2-1 X5).

**쪽 넘김** — `cursor`(불투명 문자열) · `limit`. 순서는 결정론이다(도구마다 적음 · 기본은 CSV 파일 순서 = `gid` 오름차순). cursor 는 build 에 묶인다 — 다른 `gold_hash`(또는 `aux_hash`)에서 만든 cursor 는 오류(**제안** — O-12). `limit` 기본 · 최대는 설정값(제안 기본 100 · 최대 500 — O-6).

- **`limit` 은 쪽 크기이지 결과의 상한이 아니다**(_RESUME §2 11-16 「원칙: … 폭은 빠짐없이 … 쪽 넘김 끝까지」). `next_cursor` 를 `null` 까지 따라가면 그 조회의 `total` 전부가 나온다(§9 T6). 허브에는 「상위 N 개만」 · 점수 · 순위로 빼는 입력이 없다 — 거르는 것은 부르는 쪽이 명시한 `filters` · `roles` · `classes` 같은 정확 일치 입력뿐이다.

**행 0 은 오류가 아니다** — `200` · 빈 목록 · `total: 0`. 「이 조회 범위에 행 없음」 일 뿐 「정보 없음」 을 뜻하지 않는다(llms.txt §3-4). `total` 과 `next_cursor: null` 로 앱이 「끝까지 봤다」 를 안다.

**오류**(REST 상태 · MCP 는 같은 문구의 tool 오류 — 옛 틀 `mcp_server.py:55-59`). 코드 이름 셋과 REST 상태 값은 **제안**이다(O-12 · 0.8.2 의 넷째 `unavailable` 은 코디 답으로 닫힘 — O-S1) — 브리프 §3 은 「오류」 를 쓰라고만 했다.

| 코드 | REST | 언제 |
|---|---|---|
| `invalid_argument` | 422 | 필수 없음 · enum 밖 · 한도 밖 · `표:코드` 꼴 아님 |
| `not_found` | 404 | 대상 · 값 · `gid` 가 gold 에 없음 — 기준은 위 「있음」 표(`resolve` 의 후보 0 은 오류 아님) |
| `cursor_invalid` | 400 | cursor 해석 실패 · 다른 build 의 cursor · `hier` 처럼 응답을 바꾸는 입력이 cursor 를 만든 요청과 다름 |
| `unavailable` | 503 | **gold 꺼짐**(0.8.2 — SPEC-003 §11-2 · §11-3): `app.main` 에 붙인 gold 의 시작 적재가 실패했거나 시간 한도를 넘었거나 아직 안 돌았다. REST 는 `health` 를 포함한 gold 경로 전부 · **MCP 는 도구 오류가 아니라 HTTP `503`**(같은 본문 · `initialize` 부터 막는다 — 세션 · 도구 목록을 내지 않는다). 본문 `{"detail": "unavailable: gold 꺼짐 — <F 코드 + 짧은 사유>"}` — 접속 대상(호스트 · 포트 · DB 이름)은 싣지 않고 서버 로그에만 둔다(`errors.py` `UNAVAILABLE_CODE` · `UNAVAILABLE_STATUS` · `assembly.py` `public_reason`). 켜진 gold 는 이 오류를 내지 않는다 · `gold_main` 단독 실행은 적재 실패 = 시작 실패 그대로 |

**MCP 공통** — 전 도구 `readOnlyHint`(옛 틀 `mcp_server.py:23`) · 결과 크기 meta(`mcp_server.py:30` · 값은 설정 — O-6) · 입력 이름 · 기본값은 REST 와 같다 · 출력은 REST 응답 JSON 그대로.

**REST ↔ MCP 대응**(경로는 prefix 뒤 · 전부 `GET` — 읽기 전용 · 제안 O-5)

| # | MCP 이름 | REST | 읽는 표 |
|---|---|---|---|
| 1 | `resolve` | `GET /resolve` | `g_entry` |
| 2 | `scope` | `GET /scope` | `g_scope` |
| 3 | `neighbors` | `GET /neighbors` | `g_edge` · `g_node` |
| 4 | `facets` | `GET /facets` | `g_scope` + `g_profile` · `g_indication` · `g_outcome` · `g_adverse` · `g_adverse_detail` · `g_recovery` · `g_contraindication` · `g_offer` · `g_package` |
| 5 | `concern_candidates` | `GET /concern-candidates` | `g_indication` |
| 6 | `pair` | `GET /pair` | `g_scope` · `g_pair` · `g_package` |
| 7 | `evidence` | `GET /evidence` | `g_evidence` · `source_ref` |
| 8 | `health` | `GET /health` | 적재 기록 |
| 9 | `coverage` | `GET /coverage` | `g_scope` · `g_entry` + §5-8 표의 속성 표(셈만) |

도구 집합 = 조사 §6-3 초안 8(_RESUME §2 11-16 「D4 추천대로」) + **0.5.0 의 `coverage`**(_RESUME §2 11-16 「길 찾기 재설계 진행」 「후보마다 행 수 셈」 — 새 도구로 둘지 `resolve` 를 넓힐지는 제안 · O-19). 37문항의 「읽을 gold 표」 가 전부 이 안에 있다(조사 §5-2).

### 4-1. `resolve` — 이름 → 코드 · 입구 목록

**0.8.0 — 맞춤 꼴은 「정확한 이름 → 코드」 만 한다**(_RESUME §2 11-18 D-1 · 같은 날 「허브 resolve = 최소 목록 꼴 · 규칙을 더하지 않는다 · 입력 정리는 채팅(앱) 단에서」). 문장에서 입구를 찾는 일(0.5.0 의 부분 일치 · 덮임 · 0.7 의 줄임)은 허브가 하지 않는다 — 부르는 쪽이 아래 **목록 꼴**로 입구 전부를 받아 고른다(상담 = SPEC-008 의 이해 호출). 목록 꼴은 0.7.2 그대로다.

| 입력 | 타입 | 필수 | 기본 | 한도 · 뜻 |
|---|---|---|---|---|
| `text` | string | ✓(맞춤 꼴) | — | **이름 하나**(입구의 이름 · 별칭 글자). `text` 전체의 `norm`(§5-1 R1)이 `g_entry.norm` 과 **같을 때만** 그 행이 후보다(R2). 문장 · 이름의 일부 · 줄인 말은 후보 0 이다. **없으면 목록 꼴**(아래) |
| `range` | enum(범위 8 — §5-2) | — | 없음 | 맞춤 꼴: 있으면 정렬 · `in_range` 계산에만 쓴다. **후보를 버리지 않는다** / 목록 꼴: 그 범위의 시작 표(§5-2 `in_range` 표 — 속성 4표 포함)의 입구 전부 |
| `tables` | string[] | — | 없음 | 목록 꼴 전용 — `g_entry.entity_table` 값으로 고른다(정확 일치). `range` 와 함께 주면 교집합 |
| `cursor` · `limit` | | — | §4-0 | 목록 꼴 전용 |

0.7 의 입력 `abbr` 은 **없앴다** — 주면 `invalid_argument` 다(O-32).

출력 `candidates[]` — `g_entry` 행 그대로 + 계산 필드:

| 계산 필드 | 뜻 |
|---|---|
| `matched.span` | 맞은 글자 = 그 행의 `g_entry.norm`(= 입력의 `norm`). 맞춤 꼴의 `matched` 는 이 칸 하나다 |
| `in_range` | `range` 가 왔을 때 그 범위의 시작 표인가(§5-2 표) · 안 왔으면 `null` |
| `ambiguous`(머리) | 그 `norm` 에 개념이 2개 이상인가 |

0.8.0 에서 **없앤 계산 필드**: `matched.start`(늘 0 이다) · `matched.covered_by`(조각이 하나뿐이다) · `matched.how` · `matched.full`(줄임이 없다). 남길 것 · 지울 것 · 쓰는 곳별 영향은 변경 기록 0.8.0 의 표.

- 맞춤 규칙 = §5-1. 같은 (`entity_table`, `entity_code`) 는 한 번만(`gold-build.py:636-641`).
- 순서 = `gold-build.py:633-634` 의 표 순서(633 행의 `order` 목록 · 634 행이 그것으로 정렬) → `name_kind` 가 「이름」 인 것 먼저 → `gid`. `range` 를 줬으면 `in_range` 가 참인 것이 그 앞이다. 0.5.0 의 「맞은 조각이 긴 것 먼저」 는 없어졌다 — 맞은 조각의 길이가 전부 같다.
- 겹침(같은 `norm` 에 개념이 여럿 — norm 99개 · 최대 3개념 · 조사 §1-5)은 **고르지 않고 전부** 낸다. 고르는 것은 부르는 쪽이다.
- 맞춤 꼴은 쪽 넘김 없음 — 후보는 0 또는 그 `norm` 의 개념 수(최대 3)다.
- 맞춤 꼴의 후보 0 = `200` · 빈 목록. **허브는 여기서 멈춘다** — 문장 · 조사가 붙은 말 · 줄인 말 · 오타 · 구어를 풀지 않는다(R5). 부르는 쪽이 목록 꼴로 입구 목록을 받아 고른다.
- **MCP 도구 설명에 문장 하나를 적는다**(T29): 「`text` 는 이름 하나다 — 문장을 넣으면 후보가 0 이다. 문장에서 입구를 찾으려면 목록 꼴로 입구를 받아 고른다」. 0.5.0 ~ 0.7.1 의 부분 일치 · 덮임 · 줄임 문장은 지운다.

**목록 꼴 — 범위의 입구 전부**(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) · 지시 3 의 4 「resolve 가 0 이면 고른 범위의 입구 목록을 후보로」 — 허브 쪽 재료)

- `text` 없이 `range` 또는 `tables`(둘 중 하나는 필수 — 둘 다 없으면 `invalid_argument`)를 주면, 그 표들의 **`g_entry` 행 전부**를 쪽 넘김으로 낸다. 출력은 맞춤 꼴과 같은 `candidates[]`(`g_entry` 행 그대로)이고 `matched` 는 없다 · `in_range` 는 `range` 를 줬으면 전부 참.
- 순서 = `entity_table`(맞춤 꼴과 같은 표 순서) → `entity_code` → `gid`. `total` = `g_entry` 행 수 · `next_cursor: null` 까지 넘기면 전부 나온다(§4-0 「쪽 넘김」). 머리에 계산 `counts{by_table, entities}`(`entities` = 서로 다른 (`entity_table`, `entity_code`) 수)를 모든 쪽에 싣는다.
- **허브는 고르지 않는다 · 점수를 매기지 않는다 · 철자 거리 같은 비슷함 계산을 하지 않는다.** 목록을 그대로 낼 뿐이다 — 후보는 gold 에 있는 것뿐이라 Jev · LLM 이 없는 입구를 만들 수 없다(llms.txt §3-1 「Jev 가 존재하지 않는 노드 ID 를 생성하게 하지 않는다」). 「질문이 이것을 말하나」 는 앱이 Jev Noul 로 묻는다(SPEC-002 §3-1 단계 ①-4).
- 한 개념의 이름 · 별칭이 여러 행이다(`g_entry` 2,642 행 · 개념 수는 표마다 §5-2 아래 셈) — 개념 하나로 묶는 것은 앱이다.
- 목록 꼴을 `resolve` 의 입력으로 둘지 따로 도구로 둘지는 **제안**이다(O-18 — 본문 = `resolve` 입력 · 도구 수 8 그대로).
- **0.8.0 — 목록 꼴은 바뀌지 않는다**: `candidates[]` · 순서 · `total` · `counts` · 쪽 넘김이 0.7.2 와 같다. 달라지는 것은 머리 `request` 에서 `abbr` 칸이 없어지는 것 하나다(O-32). 0.8.0 부터 문장에서 입구를 고르는 길은 이 목록 꼴뿐이다 — 상담(SPEC-008 §2-1)은 `tables` = `concern` · `site` · `modality` · `procedure` · `product` 로 끝까지 넘겨 받은 개념 820(이름 + 별칭)을 `gold_hash` 마다 한 번 캐시해 소넷에 목록으로 준다(`$W/research-input-space.md` §3 — 목록 꼴 한 번 45ms). 위 불릿의 「앱이 Jev Noul 로 묻는다」 는 시험 앱 B 열(옛 판)의 길이다.

### 4-2. `scope` — 대상의 층 목록

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `node` | `표:코드` | ✓ | — | 묻는 대상(`subject_*`) |
| `roles` | string[] | — | 전부 | `g_scope.role` 값으로 거름 |

출력 `holders[]` — `g_scope` 행 그대로(`subject` = 입력) · 계산 필드 `counts_by_role`(머리). 순서 = `gid`. 쪽 넘김 있음.

- 읽는 방향은 **대상 → 층**(`subject` 로 묻는다)뿐이다. 반대 방향(층 → 대상)은 `neighbors` 가 낸다(`g_scope` 엣지 = holder → subject — `gold-build.py:567-568`).
- 대상이 `g_scope` 에 없으면 `not_found`(§4-0 「있음」).
- **「하위 *」 role 의 행은 자손 전부다**(0.5.2 — §5-9 HG2). `roles` 가 없거나(전부) 「하위 *」 를 품으면, 대상의 「하위 *」 행에 더해 **그 holder 를 다시 `subject` 로 삼은 「하위 *」 행**을 끝까지 따라가 낸다. 두 단 아래부터의 행은 `g_scope` 행 그대로이고(그 행의 `subject_*` 는 **중간 holder** 다 — 입력 대상이 아니다) 계산 필드 `depth`(1 = 대상의 행 · 2 이상 = 따라간 행) · `via[]`(대상에서 그 행의 `subject` 까지 거친 holder — `{holder_table, holder_code, scope_gid}` · 가까운 순 · `depth` 1 이면 `[]`)가 **모든 행에** 붙는다. `total` · `counts_by_role` 은 따라간 행을 품는다. 순서 = `depth` → `gid`. 한 단만 받으려면 `descend` = `one`(§5-9 HG2-6).

### 4-3. `neighbors` — 허용 관계의 이웃

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `node_id` | `표:코드` | ✓ | — | `g_node` 에 있는 노드 |
| `edge_types` | string[] | ✓(1개 이상) | — | `g_edge.edge_type` 값. **허용 관계를 부르는 쪽이 정한다**(llms.txt §3-1 「허용된 방향 · 관계에서만」) |
| `direction` | `out` \| `in` | — | `out` | `out` = `src` 가 이 노드 · `in` = `dst` 가 이 노드 |
| `cursor` · `limit` | | — | §4-0 | |

출력 `items[]` — 한 항목 = 엣지 하나:

| 필드 | 어디서 |
|---|---|
| `edge_id` · `src` · `dst` · `edge_type` · `gold_table` · `gold_id` · `evidence_kind` | `g_edge` 헤더 그대로 |
| `node` 안의 `node_id` · `node_table` · `node_code` · `label` | 반대쪽 끝의 `g_node` 헤더 그대로 |
| `counts_by_type`(머리 · 계산) | edge_type 별 엣지 수(쪽과 무관) |
| `distinct_nodes`(머리 · 계산) | 서로 다른 이웃 노드 수 |

- 순서 = `edge_type` → 이웃 `node_id` → `edge_id`.
- 한 항목(행) = 엣지이고, 그 행의 `evidence_kind` 는 **엣지 쪽**(`g_edge.evidence_kind`)이다. `node` 는 `g_node` 7 칸 중 4 칸만 싣는다 — **노드 쪽 `silver_table` · `silver_id` · `evidence_kind` 는 싣지 않는다**(§4-0 「행마다 `evidence_kind`」 는 엣지 것으로 채워진다). 노드의 근거가 필요하면 `evidence(g_node, node_id)` 로 묻는다(§4-7).
- 한 이웃에 엣지가 여럿일 수 있다(gold 행마다 엣지). 후보로 쓸 때 묶는 것은 앱.
- `both` 방향 · 깊이 2 는 **없다** — 방문 장부 `(build, 노드, edge_type, …)`(llms.txt §4)가 한 방향 한 홉 단위라서.
- **`neighbors` 로 닫히지 않는 것**(도구 설명에 적는다):
  - `g_pair` 904 행 중 한 끝이 빈 37 행(`to` 빈칸 31 · `from` 빈칸 6)은 엣지가 아니다(`gold-build.py:590-591`) → 시술 간 관계는 `pair` 로(조사 §1-3 주의).
  - `g_indication` 엣지는 `concern_match` 「직접」 행만이다(`gold-build.py:595-596`) → 고민 3단은 `concern_candidates` 로.
  - 부위 · 재료 · 방법 · 해부는 노드가 아니다(조사 §1-2) → 그 코드로 **시작**하면 `facets` 속성 쪽(§4-4) · 다른 입구에 곁들이면 칸 필터(`facets.filters` · `concern_candidates` 의 `site`).

### 4-4. `facets` — 대상 × 속성 묶음

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `node` | `표:코드` | ✓(아래 `offer_name_contains` 를 줄 때만 생략) | — | 묻는 대상 · 값 노드 · **속성 코드**(재료 · 방법 · 해부 · 부위 — 아래 「속성 쪽」) |
| `facet` | enum 9 | ✓ | — | `profile` · `indication` · `outcome` · `adverse` · `adverse_detail` · `recovery` · `contraindication` · `offer` · `package` |
| `roles` | string[] | — | `자기` · `물려받음` | 펼칠 `g_scope.role`. 기본값 = `gold-build.py:644` `holders` 기본. 범위별 role 은 부르는 쪽이 준다(§5-2). **facet = `offer` 이고 `node` 가 product 이면 기본 = `자기` · `하위 제품`** 이다(되적기 — _RESUME §2 11-16 「허브 검수 뒤」 · 허브 검수 W-1 · `HUB backend/app/modules/gold/facets.py:26-28`): 물려받은 시술 · 케이스 · 계열 층의 상품을 그 제품의 상품으로 내지 않는다(semantic-map §5 첫 불릿 · `gold-build.py:881-883`). 다른 대상(시술 · 케이스 · 계열)의 offer 기본 role 은 그대로다. **「하위 *」(`하위 시술` · `하위 케이스` · `하위 제품`)를 주면 그 층 holder 의 자기 행이 `layer` 와 함께 나온다** — 앱 B 는 0.5.0 부터 이 role 을 명시해 부른다(§5-2 · §5-3 S5). **0.5.2 — 「하위 *」 는 한 단이 아니라 자손 전부다**(§5-9 HG2 — 계열에 `하위 시술` · `하위 케이스` 를 주면 그 시술 아래 케이스의 자기 행까지 `layer.depth` · `layer.via[]` 와 함께 나온다). **도구 설명(MCP 의 도구 · 입력 설명 · REST 문서)에 「하위 층(`하위 시술` · `하위 케이스` · `하위 제품`)의 자기 행은 `roles` 에 그 role 을 줘야 나온다 — 기본값(`자기` · `물려받음`)으로는 나오지 않는다」 를 적는다**(0.5.1 — 검수 v05 W-4 (a): 계약 · 기본값은 그대로이고 설명만 더한다. 도구를 스스로 고르는 쪽(SPEC-002 의 C 열)이 기본값 때문에 하위 층 행을 구조적으로 못 읽는 일이 없게 한다 — 설명은 모든 부르는 쪽에 같다). **`node` 가 값 쪽 · 속성 쪽이면 `roles` 는 쓰이지 않는다**(펼칠 `g_scope` 가 없다 — 줘도 무시하고 `request` 에 그대로 되돌린다) |
| `filters` | 칸=값 목록 | — | 없음 | **그 facet 표의 헤더 칸**만 받는다 · 정확 일치. 예: `adverse` 에 `adverse_code` · `polarity` · `site_name` / `adverse_detail` 에 `adverse_risk_id`. 그 표에 없는 칸은 `invalid_argument` 다 — `question_class` 는 `g_pair` 칸이라 `facets` 에는 해당 없다(`pair.classes` 로) |
| `hier` | `expand` \| `exact` | — | `expand` | 계층 펼침(아래 「계층 펼침」). `exact` = 코드 정확 일치만. 기본값은 승인된 제안이다(O-12) |
| `offer_name_contains` | string | — | 없음 | **facet = `offer` 전용** — `g_offer.offer_name` 에 이 글이 **부분 일치**하는 행(아래 「상품 이름 부분 일치」). `node` 대신 준다 · 다른 facet 에 주면 `invalid_argument` |
| `cursor` · `limit` | | — | §4-0 | |

출력 `rows[]` — 그 gold 표 행 그대로 + `layer`(§4-0 — **대상 쪽으로 얻은 행에만.** 값 쪽 · 속성 쪽 조회의 행에는 `layer` 가 없다) + `hier`(§4-0 — 계층으로 넓힌 조회의 행에만) + `attr`(§4-0 — 속성 쪽 조회의 행에만) · 머리에 `counts`(계산: `by_role` · **`distinct_rows`**(서로 다른 `gid` 수 — 대상 쪽은 같은 행이 holder 를 달리해 되풀이될 수 있어 `total` 과 다를 수 있다 · 되적기 — 허브 검수 W-1 · `HUB facets.py:147-148`) · facet 별 뜻 있는 칸의 값 셈 — 예 `polarity` · 넓힌 조회면 `by_hier_match` · 속성 쪽이면 `by_column` · `subjects`) · `ledger_check[]`(§4-0).

**맞춤 규칙**(대상 쪽 = `g_scope` 로 펼친 holder 와 맞춤 · 값 쪽 = `node` 가 그 값 노드일 때)

| facet | 표 | 대상 쪽 | 값 쪽 | 근거 |
|---|---|---|---|---|
| `profile` | `g_profile` | `subject_*` = holder | — | `gold-build.py:672` |
| `indication` | `g_indication` | `target_*` = holder **그리고 `concern_match` = 직접** | `node` = concern → `concern_code` (직접만 · 3단은 §4-5) | `gold-build.py:675` |
| `outcome` | `g_outcome` | `target_*` = holder | `node` = effect → `effect_code` | `gold-build.py:676` |
| `adverse` | `g_adverse` | `target_*` = holder | `node` = adverse → `adverse_code` | `gold-build.py:731` |
| `adverse_detail` | `g_adverse_detail` | `target_*` = holder(+ `filters.adverse_risk_id`) | — | 조사 §1-1 |
| `recovery` | `g_recovery` | `target_*` = holder | — | `gold-build.py:908` |
| `contraindication` | `g_contraindication` | `target_*` = holder | `node` = condition → `condition_code` | `gold-build.py:861-865` |
| `offer` | `g_offer` | product → `item_*` = holder(`roles` 에 「하위 제품」 을 주면 그 제품들까지) · procedure → `procedure_code` · procedure_case → 그 케이스의 `procedure_code`(`g_profile.procedure_code`) | `node` = offer → `offer_id` | `gold-build.py:879-885` |
| `package` | `g_package` | `item_*` = holder | `node` = package → `package_id` · concern → `concern_code` | `gold-build.py:921-922` |

- 순서 = holder 의 `g_scope.gid` → 속성 행 `gid`.
- `indication` 의 대상 쪽에서 「직접」 만 내는 까닭: 나머지 행은 같은 적응을 물은 고민(상위)별로 되풀이한 것이다(`gold-build.py:595-596` 주석).
- `node` 가 값 쪽이고 그 값이 `g_entry` 에 있으면 행이 0 이어도 `200` · `total: 0` 이다(§4-0 「있음」).

**속성 쪽 — 재료 · 방법 · 해부 · 부위 코드로 시작**(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) · 지시 3 의 4 「그 칸을 가진 대상을 전부 돌려준다」)

재료 · 방법 · 해부 · 부위는 `g_entry` 에 입구가 있지만(143 · 49 · 105 · 89) `g_node` 에는 없다 — 대상 쪽 · 값 쪽 어느 길로도 시작할 수 없던 입구다. `node` 에 그 코드를 주면 **그 값을 칸에 가진 행을 전부** 낸다. 행의 대상 칸이 곧 「그 칸을 가진 대상」 이다.

| facet | 표 | `material` | `method` | `anatomy` | `site` |
|---|---|---|---|---|---|
| `profile` | `g_profile` | `materials`(항목) | `methods`(항목) | `anatomy_name` | `site_name` |
| `indication` | `g_indication` | — | — | — | `site_code`(코드) · `site_name` · `case_site_name` |
| `outcome` | `g_outcome` | — | — | — | `site_name` |
| `adverse` | `g_adverse` | — | — | — | `site_name` |
| `adverse_detail` | `g_adverse_detail` | — | — | `anatomy_name` | `site_name` |
| `contraindication` | `g_contraindication` | — | — | — | `site_name` |
| `offer` | `g_offer` | `materials`(항목) | — | — | `sites`(항목) |
| `recovery` · `package` | `g_recovery` · `g_package` | — | — | — | — |

- 이 표가 **맞춤 칸의 전부**다 — gold 15표 헤더에서 이름에 `site` · `material` · `method` · `anatomy` 가 든 칸을 전수로 뽑은 것이다(이 워커 헤더 grep — `g_pair` · `g_package` · `g_recovery` · `g_scope` 에는 그런 칸이 없다 · 부록 A 「속성 쪽 맞춤 칸」 줄로 기계 대조). 「—」 인 조합으로 부르면 `invalid_argument` 다(그 표에 맞출 칸이 없다 — 행 0 과 구분한다).
- **맞추는 법**: 요청 코드 → 그 (`entity_table`, `entity_code`) 의 `g_entry.entity_name`(코드마다 하나 — 네 표 모두 이름 수 = 코드 수 · 이 워커 셈) → 칸 값과 **글자 그대로 일치**. `(항목)` 칸은 여러 값이 ` · ` 로 이어져 있어 **나눈 항목 하나와 일치**해야 한다(부분 문자열 일치가 아니다). `site_code` 칸만 코드로 맞춘다. gold 칸이 이름을 담고 있어서 이렇게 한다 — 허브가 silver 를 더 읽지 않는다(보조 입력이 늘지 않는다).
- 한 행에서 여러 칸이 맞으면(`g_indication` 의 `site_name` 과 `case_site_name`) 행은 **한 번만** 내고 `attr.column` 에 맞은 칸을 전부 적는다. **부위는 칸마다 역할이 다르다**(시술 대상 부위 · 적응 자리 · 효과 자리 · 부작용 발생 부위 · 위험 요인 부위 · 금기 자리 · 상품 이름 속 조각 — semantic-map §3-4) — 허브는 섞어 한 뜻으로 바꾸지 않고 어느 칸에서 맞았는지만 붙인다.
- 순서 = `gid`. `total` = 맞은 행 수. `counts.by_column`(칸별 행 수) · `counts.subjects`(그 표의 대상 칸 — `subject_*` 또는 `target_*` · `g_offer` 는 `offer_id` — 의 서로 다른 값 수)를 모든 쪽에 싣는다. `layer` · `hier` 는 붙지 않는다(`g_scope` 로 펼치지 않고 · 계층으로 넓히지 않는다 — O-17).
- `filters` 는 대상 쪽과 같이 쓸 수 있다(그 facet 표의 헤더 칸 · 정확 일치). `roles` 는 쓰이지 않는다.
- 행이 0 인 코드도 `g_entry` 에 있으면 `200` · `total: 0` 이다(§4-0 「있음」).
- **한 속성 코드의 「대상 전부」 = 그 속성 표에 「—」 가 아닌 facet 을 전부 부른 것**이다(재료 2 · 방법 1 · 해부 2 · 부위 7 조회). 어느 facet 을 부를지는 허브가 정하지 않는다 — 부르는 쪽(앱은 전부 부른다 — SPEC-002 §3-2).
- 11-16 gold 의 크기(이 워커 셈): 한 코드에 맞는 행은 표 전부를 합쳐 재료 최대 51 · 방법 17 · 해부 9 · 부위 97. 맞는 행이 하나도 없는 코드 = 재료 4 · 방법 10 · 해부 56 · 부위 36.
- **이 길로 닿지 않는 것**(한계 — O-17): `g_offer.materials` 의 항목 3 종(10 행) · `g_offer.sites` 의 항목 9 종(59 행)은 어느 입구 이름과도 같지 않다(상품 이름에서 나온 조각 — semantic-map §3-4 끝에서 둘째 줄). 그 행은 상품 쪽 길(`node` = 대상 · offer · `offer_name_contains`)로는 그대로 나온다. `tissue_name` 은 입구가 아니다(`g_entry` 에 조직 표가 없다) — 칸 필터로만 쓴다.
- 속성 쪽을 `facets` 의 `node` 로 받을지 따로 도구로 둘지는 **제안**이다(O-16 — 본문 = `facets` 입력 · 도구 수 8 그대로 · 행 필드가 대상 쪽과 같아 부록 A 가 안 늘어난다).

**상품 이름 부분 일치**(결정 — _RESUME §2 11-16 「재검수 2(r3) §5 결정」 A-2 · 지시 3 의 1 A-2 「`facets` offer 에 `offer_name` 부분 일치 필터」 · 옛 O-10)

- facet = `offer` 에 `offer_name_contains` 를 주면 `norm(offer_name_contains)` 이 `norm(g_offer.offer_name)` 의 **부분 문자열**인 행을 전부 낸다. `norm` 은 §5-1 R1 과 같은 식(공백 제거 + 소문자)이다 — gold-build 시범과 같다(`gold-build.py:875-876`).
- `node` 와 함께 주면 `invalid_argument`(두 길을 섞지 않는다). 빈 문자열 · 공백뿐이면 `invalid_argument`.
- 출력 · 순서(`gid`) · `total` · `ledger_check[]`(`rows` 의 `offer_id` 대조 — §4-0)는 값 쪽 offer 조회와 같다. `layer` · `hier` · `attr` 는 붙지 않는다.
- 맞는 상품이 없으면 `200` · `total: 0` 이다 — 「그 이름이 gold 에 있음」 을 물을 대상이 없으므로 `not_found` 를 내지 않는다.
- 이 입력으로 Q33 의 전체 답 키를 뽑는다(SPEC-002 §9-5). 입력 이름은 제안이다(O-5).

**계층 펼침**(_RESUME §2 11-16 「검수 뒤 결정 4」 ② — 보조 입력 ① 의 `parent_code` 로 · gold 는 읽기만)

| facet | 어디에 걸리나 | 넓히는 방향 | `hier.match` | 근거 |
|---|---|---|---|---|
| `package` | 값 쪽 `node` = concern | 그 고민 + **상위 고민 전부**(뿌리까지) | `직접` · `상위` | `gold-build.py:319-325 · 921` |
| `adverse` | 값 쪽 `node` = adverse · 대상 쪽의 `filters.adverse_code` | 그 사건 + **하위 사건** | `직접` · `하위` | `gold-build.py:734` |
| `contraindication` | 값 쪽 `node` = condition · 대상 쪽의 `filters.condition_code` | 그 조건 + **하위 조건** | `직접` · `하위` | `gold-build.py:860` |

- **이 세 자리가 전부다.** 다른 facet · 다른 칸은 `hier` 값과 무관하게 정확 일치다 — `indication` 값 쪽(고민 3단은 gold 가 이미 펼쳐 둔 `asked_concern_code` 로 — §4-5) · `outcome` 값 쪽(효과 계층은 결정 ② 의 3표에 없다) · `offer` · `adverse_detail`(`adverse_code` 칸이 없다 — `adverse_risk_id` 로 잇는다).
- 「하위」 = **자손 전부**(3단이므로 최대 2단 아래). **결정이다**(_RESUME §2 11-16 「재검수(r2) 뒤 결정 2」 — 「부작용 · 조건 하위는 자손 전부 펼침(금기 빠짐 = 안전 문제 · 37 안 차이 0)」 · 옛 O-13). gold-build 질문 시범은 **자식 1단만** 폈다(`gold-build.py:734 · 860`) — 자식과 자손의 행 수가 다른 코드는 부작용 5 개(+ 390 행) · 조건 10 개(+ 77 행 — 전부 `polarity` 금기 행)이고, **37 문항 안에서는 차이가 0** 이다(사건 필터가 있는 Q12 · Q13 · Q14 와 조건이 입구인 Q29 · Q30 모두 손자 코드가 없는 값 — 재검수 R-3 셈). 차이는 추가 묶음에서만 난다.
- **효과 계층은 펼치지 않는다**(재검수 R-5). 효과도 `parent_code` 가 있지만(semantic-map §1) 결정 ② 의 보조 입력 3표에 없다 — `outcome` 값 쪽은 정확 일치다. 펼칠지는 O-15.
- 넓힌 행마다 `hier` 가 붙어 「물은 코드의 행」 과 「상위 · 하위 코드의 행」 을 앱이 가른다. 허브는 넓힌 행을 섞어 한 코드로 바꾸지 않는다(행의 `*_code` 칸은 gold 값 그대로).
- 순서는 넓힘과 무관하게 `gid`(값 쪽) 또는 holder `g_scope.gid` → 속성 행 `gid`(대상 쪽).
- `hier` = `exact` 이면 0.1.0 과 같은 「코드 정확 일치만」 이다.
- hard gate 가 볼 칸(`polarity` · `same_day` · `reach` · `price_mid_raw` …)은 거르지 않고 그대로 낸다. 거르는 것은 부르는 쪽의 `filters` 뿐이다.

### 4-5. `concern_candidates` — 고민 → 시술 후보

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `concern_code` | string | ✓ | — | 물은 고민(`asked_concern_code` 와 맞춤 — 3단이 이미 펼쳐져 있다 · semantic-map §5). `g_entry` 의 (`concern`, 코드)에 없으면 `not_found` · 있고 행이 0 이면 `200` · `total: 0`(§4-0 「있음」) |
| `site` | string | — | 없음 | `site_name` 또는 `case_site_name` 정확 일치(`gold-build.py:701`) **∪ 그 부위에 묶인 고민(과 그 하위 고민)의 행**(0.5.2 — §5-9 HG3 · 보조 입력 ③). 행마다 계산 `site_match[]` 로 어느 쪽으로 맞았는지 붙는다. **0.7.1 — 물은 고민에 묶인 부위가 하나도 없으면(`sites[]` = `[]`) 이 맞춤으로 행을 빼지 않는다**: 행을 전부 내고 맞은 행에 `site_prefer` 표지만 단다(§5-11 SP · 머리 `site_applied` = `prefer`). **0.7.2 — 기준을 넓혔다**: 행을 빼는 것은 **물은 부위가 그 고민의 `sites[]`(자기 + 하위 고민의 부위) 안에 있을 때뿐**이다. 안에 없으면 — `sites[]` 가 `[]` 일 때를 포함해 — 행을 빼지 않는다(§5-11 SP1) |
| `site_mode` | `auto` \| `filter` | — | `auto` | 0.7.1 — §5-11 SP. `auto` = **물은 부위가 그 고민의 `sites[]` 안에 있으면 거르고(HG3) 없으면 거르지 않는다**(0.7.2 — 0.7.1 은 「부위가 묶인 고민은 거르고 묶이지 않은 고민은 거르지 않는다」 였다) · `filter` = 늘 거른다(0.7.0 과 같은 응답). `site` 가 없으면 뜻이 없다(무시). 입력 이름은 제안(O-30) |
| `upper` | `auto` \| `none` | — | `auto` | 0.5.2 — §5-9 HG1. `auto` = 물은 고민의 행이 0 이면 가장 가까운(행이 있는) 윗고민의 행을 낸다 · `none` = 0.5.1 과 같이 0 그대로. 입력 이름 · 기본값은 제안(O-23) |
| `to_procedure` | `auto` \| `none` | — | `auto` | 0.7 — §5-11 DP. `auto` = 시술 코드 없는 행(`modality_only[]` · `unreached[]`)을 시술로 내려 `descended[]` 를 낸다 · `none` = `descended` · `counts.descended` **두 필드를 뺀다**(`null` · `[]` 로 싣지 않는다 — 0.6 과 같은 응답 + `sites[]` · `counts.sites`). 입력 이름은 제안(O-27) |
| `cursor` · `limit` | | — | §4-0 | 쪽 단위 = `total` 단위 = `groups`(묶음) |

출력:

| 필드 | 뜻 |
|---|---|
| `groups[]` | `procedure_code` 가 있는 행을 (`candidate_table`, `candidate_code`) 로 묶음. 묶음마다 헤더 칸 `candidate_table` · `candidate_code` · `candidate_name` · `procedure_code` · `procedure_name` + 계산 `reach[]`(서로 다른 값) · `concern_match[]`(서로 다른 값) · `n_rows` · `rows[]`(그 묶음의 `g_indication` 행 그대로) |
| `modality_only[]` | `reach` = 「계열 층만」 행 그대로 — **시술 후보에 섞지 않는다**(semantic-map §5 「계열 층만으로 따로」) |
| `unreached[]` | `procedure_code` 가 비고 「계열 층만」 도 아닌 행 그대로(`reach` = 「패키지 — 항목 코드 없음」 128 · 「제품 — 케이스 없음」 55 — 이 워커 셈) |
| `counts`(계산) | `rows` · `groups` · `procedures`(서로 다른 `procedure_code`) · `modality_only` · `unreached` · `unfiltered_rows`(`site` 를 안 걸었을 때 행 수) · **0.5.2**: `self_rows`(물은 고민 자신의 행 수 — `site` 거르기 앞 · 물려받은 응답이면 0) · `by_site_match`(`site` 를 걸었을 때 — `column` · `concern_site` 별 행 수 · 둘 다 맞은 행은 양쪽에 센다) |
| `inherited_from`(머리 · 계산 · 0.5.2) | HG1 로 윗고민의 행을 냈으면 `{concern_code, steps}`(`steps` = 몇 단 위인가 — 1 또는 2) · 아니면 `null`. **`null` 이 아니면 이 응답의 행 전부가 윗고민의 것이다** — 행마다 `hier{asked_code, match: 상위}` 가 붙는다(§4-0 `hier` 와 같은 꼴) |
| `ledger_check[]`(머리 · 계산) | `concern_code` 에 걸린 원장 확인 id(§4-0). 행이 0 이어도 낸다 — Q10 꼴의 재료 |
| `descended[]`(쪽 밖 · 계산 · 0.7) | §5-11 DP — **한 항목 = 계열 하나**(계열 단위 묶음): `modality_code` · `modality_name` · `unit`(= `계열` — 「이 적응은 계열 단위로 말한 것」 표지) · `procedures[]`(그 계열의 시술 전부 — `{procedure_code, procedure_name, scope_gid, in_groups}`) · `from[]`(이 계열로 내려온 행마다 `{gid, reach, lands, path[]}`). 꼴은 아래 표 |
| `sites[]`(쪽 밖 · 계산 · 0.7) | §5-11 CS — 물은 고민(과 그 하위 고민)에 묶인 부위: `{site_code, site_name, concern_code, csi_id, match}`(`match` = `직접` \| `하위`). 묶인 부위가 없으면 `[]`(필드를 빼지 않는다) |
| `counts.descended`(계산 · 0.7) | `{rows, modalities, procedures, new_procedures, undescended}` — 내린 행 수 · 계열 묶음 수 · 서로 다른 시술 수 · 그 가운데 `groups` 에 없는 시술 수 · **못 내린 행 수**(11-16 gold 에서 0 — 0 이 아니면 그 행은 `unreached[]` 에 그대로 있다). `to_procedure` = `none` 이면 **이 필드를 뺀다**(`descended` 와 함께 — 0.7.1 · 0.7.0 은 한 곳에 `null` 로 적었다) |
| `counts.sites`(계산 · 0.7) | `{direct, lower, distinct_sites}` — `direct` · `lower` 는 `sites[]` **항목 수**(묶임 행 수) · `distinct_sites` 는 서로 다른 `site_code` 수 |
| `site_applied`(머리 · 계산 · 0.7.1) | `site` 를 어떻게 썼나 — `null`(`site` 없음) \| `filter`(거름 — HG3) \| `prefer`(**거르지 않음** — 행 전부 · 표지만 · §5-11 SP) |
| `site_prefer`(행 · 계산 · 0.7.1) | `site_applied` = `prefer` 일 때 **모든 행**(`groups[].rows[]` · `modality_only[]` · `unreached[]`)에 붙는 「우선 표시」 표지 — `true` = `filter` 였다면 남았을 행(HG3-1 의 (i) 또는 (ii)) · `false` = 그 밖. `true` 인 행에는 까닭을 알리는 `site_match[]`(0.5.2 꼴 그대로)가 함께 붙는다. `filter` · `null` 일 때는 이 필드가 없다 |
| `groups[].n_site_prefer`(묶음 · 계산 · 0.7.1) | `site_applied` = `prefer` 일 때 그 묶음에서 `site_prefer` = `true` 인 행 수(0 이상). 그 밖에는 이 필드가 없다 |
| `counts.site_prefer`(계산 · 0.7.1) | `site_applied` = `prefer` 일 때 `{rows, groups}` — 표지가 붙은 행 수 · 표지 행이 1 이상인 묶음 수. 그 밖에는 `null` |

**`descended[]` 의 꼴**(0.7 — 전부 계산 필드이고 값은 `g_scope` · `g_indication` 칸 그대로다)

| 필드 | 어디서 |
|---|---|
| `modality_code` · `modality_name` | 내림이 닿은 계열 — `g_scope` 의 `holder_code` · `holder_name`(행의 대상이 계열이면 `g_indication.target_code` · `target_name`) |
| `unit` | 고정값 `계열`. **이 묶음의 시술 하나하나가 그 적응을 자기 것으로 가진 것이 아니다** — 적응은 `from[]` 의 행이 말한 층(계열 · 메뉴 · 제품)의 것이다(DP4) |
| `procedures[].procedure_code` · `procedure_name` · `scope_gid` | 그 계열을 `subject` 로 둔 role 「하위 시술」 `g_scope` 행의 `holder_code` · `holder_name` · `gid` — **그 계열의 시술 전부**(고르지 않는다) |
| `procedures[].in_groups` | 그 시술이 이 조회의 `groups` 전체(쪽과 무관)에 `procedure_code` 로 이미 있나 |
| `from[].gid` · `reach` | 내려온 `g_indication` 행(이 응답의 `modality_only[]` 또는 `unreached[]` 에 그대로 있는 행)의 `gid` · `reach` |
| `from[].path[]` | 그 행의 대상에서 계열까지 거친 층 — `{table, code, name, role, scope_gid}` 를 **대상부터 차례로**. 첫 항목 = 행의 대상(`role` · `scope_gid` 는 `null`) · 그 뒤 항목 = 따라간 `g_scope` 행의 holder 와 그 `role` · `gid`. 메뉴 · 패키지 · 제품 이름은 **여기에만** 나온다 |
| `from[].lands` | `modality`(계열에 닿아 그 하위 시술 전부로 내림) \| `procedure`(계열을 거치지 않고 시술에 바로 닿음 · 11-16 gold 에서 0 건). **`procedure` 의 꼴(0.7.1 — 검수 W-2)**: ① **어느 묶음** = 닿은 시술의 계열 묶음(`modality_code` = 그 시술을 `subject` 로 둔 role 「물려받음」 `g_scope` 행의 계열 holder — 11-16 gold 에서 시술 138 전부에 하나씩 · 닿은 시술이 계열 둘이면 묶음도 둘 · **계열이 없으면 못 내린 행**이다(DP9)) ② **`procedures[]` 는 그 계열의 시술 전부 그대로**다(묶음은 계열 하나에 하나라 길마다 달라지지 않는다) — 이 행이 닿은 시술은 `from[].procedure_codes[]` 로만 좁혀 알린다(`lands` = `modality` 면 이 필드는 `null`) · `path[]` 의 끝 항목은 닿은 시술이고 계열은 `path[]` 에 넣지 않는다 ③ **`unit` 은 `계열` 그대로**다(묶음의 단위) — 「이 행은 시술을 짚어 말했다」 는 `lands` = `procedure` 와 `procedure_codes[]` 가 알린다 |

- 순서 = 묶음의 첫 행 `gid`. `total` = `counts.groups` 다(행 수 `counts.rows` 가 아니다 — §4-0 「`total` 단위」). `modality_only[]` · `unreached[]` 는 쪽 밖 목록이라 첫 쪽에만 싣는다.
- **아래로는 보조 입력 ① (계층)을 쓰지 않는다.** 고민 3단은 gold-build 가 `g_indication` 을 만들 때 이미 **아래로** 펼쳤다(`gold-build.py:359` — 행마다 물은 고민별로 되풀이 · `concern_match` 가 「직접」 / 「하위 고민」). 그래서 `hier` 입력은 없다 — 같은 구분은 헤더 칸 `concern_match` 에 있다. **0.5.2 — 위로는 쓴다**: 물은 고민의 행이 0 일 때 `parent_code` 로 윗고민을 찾고(HG1), `site` 맞춤에서 묶인 고민의 하위 고민을 찾는다(HG3). 0.5.1 은 「쓰지 않는다」 였다(§5-5 H5 를 함께 고쳤다).
- **HG1 · HG3 의 계약은 §5-9 에 모았다.** 요약: (HG1) `counts.unfiltered_rows` 가 0 이면 → 가장 가까운(행이 있는) 윗고민 하나의 행을 같은 꼴(`groups` · `modality_only[]` · `unreached[]`)로 내고 머리 `inherited_from` · 행 `hier.match` = `상위` 를 붙인다. 행의 gold 칸(`asked_concern_code` 등)은 **그대로**다 — 물은 코드로 바꿔 쓰지 않는다. (HG3) `site` 를 주면 「행의 부위 글자 일치」 **또는** 「행의 `concern_code` 가 그 부위에 묶인 고민 · 그 하위 고민」 인 행을 낸다 — 행은 전부 물은 고민으로 이미 펼쳐져 있던 `g_indication` 행이고 새 행을 만들지 않는다.
- `ledger_check[]` 는 **요청 코드만** 대조한다 — 물려받은 윗고민 코드 · 묶인 하위 고민 코드로 넓히지 않는다(§4-0 「넓히지 않는다」 · O-14 그대로). 그래서 Q10 은 0.5.2 에서도 `LCK-010` 이 그대로 나온다.
- **0.7 — `descended[]` · `sites[]` 는 쪽 밖 목록이다**(첫 쪽에만 · 크기 한도 없음 — §4-0). **`groups[]` · `modality_only[]` · `unreached[]` · `total` · `counts` 의 기존 칸은 0.6 과 같다** — 내린 시술을 `groups` 에 섞지 않고, 내린 행을 `modality_only[]` · `unreached[]` 에서 빼지도 않는다(같은 행이 두 목록에서 `gid` 로 이어진다). 규칙은 §5-11 DP · CS.
- `unreached[]` 는 gold-build 질문 시범이 답에 안 쓰던 행이다(`gold-build.py:702-703`). 허브는 **버리지 않고 따로 낸다** — 「없음」 을 말하려면 끝까지 봐야 하므로(llms.txt §3-4).
- `site` 로 걸러 0 이면 0 그대로 낸다. gold-build 시범은 0 이면 필터를 풀었다(`gold-build.py:701` `or rows_`) — 허브는 조용히 풀지 않고 `counts.unfiltered_rows` 만 알린다(O-9). **0.7.1 — 이 줄은 `site_applied` = `filter` 일 때의 것이다**(0.7.2 — 물은 부위가 그 고민의 `sites[]` 안에 있는 짝 · 또는 `site_mode` = `filter`). 물은 부위가 `sites[]` 안에 없는 짝은 애초에 거르지 않는다 — 「조용히 푼 것」 이 아니라 머리 `site_applied` = `prefer` 와 행의 `site_prefer` 로 **밝히고** 낸다(§5-11 SP).
- **0.7.1 — `site_applied` = `prefer` 일 때의 셈**: `counts.rows` = `counts.unfiltered_rows`(전부 냈다) · `total` = `site` 를 안 건 조회와 같다 · `counts.by_site_match` 는 표지가 붙은 행으로 센다(`column` · `concern_site`) · `descended[]` 는 거르지 않은 행 전부에서 내린다(DP1 「`site` 로 거른 뒤」 의 행이 곧 전부다). **행 · 묶음의 순서는 바꾸지 않는다**(`gid` 순 그대로 — 표지가 붙은 행 · 묶음을 앞에 두는 것은 앱이다).
- **0.7.1 — MCP 도구 설명에 적을 문장**(검수 W-3 — 도구를 스스로 부르는 쪽은 설명만 본다 · 0.5.1 의 S2 · HG2-7 과 같은 꼴): ① 「`descended[]` 의 묶음은 계열 단위다(`unit` = `계열`) — 그 안의 시술 하나하나가 그 적응을 자기 것으로 가진 것이 아니라 `from[]` 의 행이 말한 층(계열 · 메뉴 · 제품)의 것이다」 ② 「`site_applied` = `prefer` 면 부위로 거르지 않은 응답이다 — `site_prefer` = `false` 인 행은 그 부위의 것이라고 말한 행이 아니다」. 문구는 구현 때 다듬되 두 뜻이 들어 있어야 한다(T24 · T28).

### 4-6. `pair` — 시술 간 관계

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `a` | `표:코드` | ✓ | — | 한 끝 |
| `b` | `표:코드` | — | 없음 | 다른 끝. 없으면 `a` 가 닿는 관계 전부 |
| `classes` | string[] | — | 전부 | `g_pair.question_class` 값 |
| `self_pair` | `only` \| `exclude` \| `any` | — | `any` | `g_pair.self_pair` = 「같음」 행만 / 빼고 / 상관없음(`gold-build.py:803-806`) |
| `same_day_only` | bool | — | `false` | `same_day` 가 채워진 행만(`gold-build.py:807-808`) |
| `package_kinds` | string[] | — | 없음 | 주면 그 `package_kind` 에서 두 끝이 함께 든 패키지를 찾는다. **`b` 가 없으면 `a` 쪽 집합과 항목이 겹치는 패키지 전부**다(되적기 — _RESUME §2 11-16 「WORK 0.2.0 수정 뒤 … N1-1 = 제안 (a)」 · `gold-build.py:821` 의 `b` 없음 갈래 · 구현 `HUB backend/app/modules/gold/pairs.py:103`) — 한 끝만 아는 질문에서 패키지가 폭에서 빠지지 않는다 |
| `cursor` · `limit` | | — | §4-0 | |

출력:

| 필드 | 뜻 |
|---|---|
| `rows[]` | `g_pair` 행 그대로 + 계산 `a_side`(`from` \| `to`) · `a_layer` · `b_layer`(각 끝이 어느 holder 로 맞았나 — `layer` 와 같은 꼴) |
| `same_day_packages[]` | `package_kinds` 를 줬을 때 — 두 끝이 함께 든 패키지의 `g_package` 행 그대로(패키지마다 묶음) |
| `counts`(계산) | `by_class` · `same_day`(값별 · 빈칸 포함) · `conflict`(`conflict_id` 있는 행) |
| `ledger_check[]`(머리 · 계산) | `a` · `b` 의 코드에 걸린 원장 확인 id(§4-0) |

- `total` = `g_pair` 행 수. `same_day_packages[]` 는 쪽 밖 목록이라 첫 쪽에만 싣는다(§4-0).
- **이 도구는 보조 입력 ① (계층)을 쓰지 않는다** — 두 끝은 대상이고(`g_scope` 로 펼침), 패키지 맞춤도 항목 코드(`item_table` · `item_code`)로 한다(`gold-build.py:814-823`). 고민으로 패키지를 찾는 길은 `facets` package(§4-4)다.
- `a` · `b` 가 `g_scope` 에 없으면 `not_found`(§4-0 「있음」).

규칙(= `gold-build.py:769-792` · semantic-map §5 끝 줄):

1. 두 끝을 `g_scope` 로 펼친다 — role `자기` · `물려받음` · `하위 케이스` · `하위 시술`. **0.5.2 — 하위 둘은 자손 전부다**(§5-9 HG2): 계열 끝은 하위 시술 **아래의 케이스**까지 펼친다(0.5.1 구현은 계열의 `g_scope` 행에 `하위 케이스` 가 없어 케이스 끝 관계를 놓쳤다). `a_layer` · `b_layer` 에 `depth` · `via[]` 가 붙는다. 패키지 맞춤(3)도 같은 닫힘이다.
2. `b` 가 있으면 (`from` ∈ A 그리고 `to` ∈ B) 또는 (`from` ∈ B 그리고 `to` ∈ A). `b` 가 없으면 `from` ∈ A 또는 `to` ∈ A — **한 끝이 빈 37 행도 이때 나온다.**
3. 패키지 맞춤은 위 role 에 `하위 제품` 을 더한 집합으로, 항목(`item_table` · `item_code`)이 양쪽 집합과 다 겹치는 `package_id`(`gold-build.py:814-823`).
4. **허브는 고르지 않는다** — 같은 쌍에 `same_day` 값이 엇갈려도 · `conflict_side` 가 「진 쪽」 이어도 전부 낸다(semantic-map §3-1). 옛 도구의 「resolved 하나」 는 가져오지 않는다(조사 §3-1 T4).
5. `same_day` 빈칸은 빈 문자열 그대로 낸다. 「가능」 으로 채우지 않는다.

순서 = `gid`. 세 끝 이상은 부르는 쪽이 쌍마다 부른다.

### 4-7. `evidence` — gold 행 → 근거

| 입력 | 타입 | 필수 | 기본 | 뜻 |
|---|---|---|---|---|
| `gold_table` | string | ✓ | — | `g_evidence.gold_table` 에 있는 표(속성 12표 · `g_node`) |
| `gold_id` | string | ✓ | — | 그 행의 `gid`(또는 `node_id`) |
| `cursor` · `limit` | | — | §4-0 | 쪽 단위 = `total` 단위 = `source_refs` 를 편 줄(§4-0 「`total` 단위」) |

출력 `refs[]`:

| 필드 | 어디서 |
|---|---|
| `gold_table` · `gold_id` · `silver_table` · `silver_id` · `fields` · `evidence_kind` | `g_evidence` 헤더 그대로 |
| `source_refs[]` 안의 `target_table` · `target_id` · `field` · `ref` | `source_ref` 헤더 그대로 |
| `n_source_refs`(계산) | 그 참조의 `source_ref` 행 수(쪽과 무관) |

- 잇는 규칙 = semantic-map §4: `target_table` = `silver_table` · `target_id` = `silver_id` · `fields` 가 있으면 `field` ∈ `fields`(`|` 로 나눔 · `(행 전체)` = `field` 빈칸) · `fields` 가 비면 그 silver 행의 `source_ref` 전부.
- 참조 하나에 `source_ref` 가 최대 557 행이다(조사 §1-4) — 그래서 쪽 넘김이 있고, **다른 도구 응답에는 근거를 싣지 않는다**(펼칠 때만 — 조사 §1-4 표 · `artifact-traceability.md` 「되짚기는 참조로, 복사로 하지 않는다」).
- `gold_table` = `g_edge` 는 `invalid_argument` — 엣지는 자기 `gold_table` + `gold_id` 로 속성 행을 가리키고, 근거는 그 행으로 묻는다.
- 행이 gold 에 없으면 `not_found`. 행은 있는데 참조가 0 이면 `200` · 빈 목록(11-16 gold 에는 그런 행 0).

### 4-8. `health`

입력 없음. 출력: `build{gold_hash, aux_hash, loaded_at}` · `files[]{name, sha256, rows, kind}`(15표 + `questions.csv` + `source_ref` + 보조 입력 4 파일 · `kind` = `gold` \| `hash_only` \| `source_ref` \| `aux`) · `expected_hash_checked`(bool) · `load_ms` · `integrity{gold_rows_without_evidence, evidence_without_source_ref, hierarchy_orphan_parents, scope_duplicate_subject_holder_rows}`(§2-3 6 · 넷째 = 같은 (`subject`, `holder`) 가 둘 이상인 `g_scope` 행 수 — 되적기 0.5.2: 허브 검수 v05 N-8 · `HUB backend/app/modules/gold/memory.py:110-118` · 11-16 gold 에서 0 · 옛 O-22 ①) · `aux{hierarchy{concern, adverse, condition}, ledger_check{rows, rows_with_code, codes}}`(적재한 수). 전부 계산 필드다. `integrity` · `aux` 의 꼴은 **제안**이다(O-12). `files[].rows` 는 파일 행 수이고, 보조 입력의 글 칸은 여기에도 싣지 않는다.

- **`questions.csv` 는 `kind` = `hash_only` 로 `files[]` 에 싣는다**(재검수 R-4): 적재하지 않지만 gold 해시 식에는 들어가는 파일이다(§2-3 3 · O-3). `name` · `sha256` 만 채우고 `rows` 는 `null` 이다(행을 읽지 않는다). 그래서 `kind` 가 `gold` 또는 `hash_only` 인 16 줄만으로 `gold_hash` 를 다시 셀 수 있고, `kind` 가 `source_ref` 또는 `aux` 인 5 줄로 `aux_hash` 를 다시 셀 수 있다.

### 4-9. `coverage` — 후보 × 정보 종류의 행 수 셈

(_RESUME §2 11-16 「길 찾기 재설계 진행」 — 「후보마다 행 수 셈」. **도구 꼴은 제안이다**(O-19 — 본문 = 새 도구 · 조사 §6-3 의 8도구에 하나를 더한다).)

앱이 Jev 에 「질문이 이 후보를 가리키나 · 어떤 정보가 필요한가」 를 묻기 **전에**, 후보마다 **어느 정보가 어느 층에 몇 행 있는지**를 한 번에 받는 도구다(SPEC-002 §3-1 단계 ①-1). **행 본문은 없다 — 셈뿐이다.**

| 입력 | 타입 | 필수 | 기본 | 한도 · 뜻 |
|---|---|---|---|---|
| `nodes` | `표:코드`[] | ✓ | — | 1 ~ 64 개(상한은 설정 — 제안 · O-6). 대상 · 값 · 속성 어느 것이든 받는다(§4-0 「있음」 기준). 넘으면 부르는 쪽이 나눠 부른다 — 허브가 잘라 내지 않는다(`invalid_argument`) |
| `kinds` | string[] | — | 전부 | §5-8 의 정보 종류 코드로 거른다(정확 일치 · 표 밖 값은 `invalid_argument`) |

출력 `items[]` — **`nodes` 순서 그대로** · 쪽 넘김 없음 · `total` = `items` 수. 전부 계산 필드다.

| 필드 | 뜻 |
|---|---|
| `node` | 요청의 `표:코드` |
| `name` | 그 개념의 `g_entry.entity_name`(입구가 없는 대상이면 `g_scope.subject_name`) |
| `kinds[]` | 정보 종류마다 `{kind, self, lower, inherited, lower_holders}` — §5-8 표에서 그 노드의 표에 「—」 인 종류는 **싣지 않는다**(0 과 구분) |

| 셈 | 뜻 |
|---|---|
| `self` | 그 종류의 조회(§5-8 표)를 그 노드로 불렀을 때 `layer.role` = `자기` 인 행 수. **`overview` · `mechanism` 은 그 종류의 칸에 값이 하나라도 있는 profile 행만 센다**(§5-8 — `lower` · `inherited` 도 같다 · 0.5.1). **값 쪽 · 속성 쪽 노드**는 role 이 없어 그 조회의 행 전부가 `self` 다(`hier` 기본값 `expand` 로 센다) |
| `lower` | role 이 「하위 *」(`하위 시술` · `하위 케이스` · `하위 제품`)인 holder 가 가진 **그 holder 의 자기 행** 수. **0.5.2 — holder 는 자손 전부다**(§5-9 HG2 · `facets` · `pair` · `scope` 와 같은 닫힘 — 불변식 T16 그대로). `pair` 로 읽는 네 종류(`avoid` · `combo` · `same_day` · `order_interval`)의 `lower` 는 `pair` 가 펴는 role(`하위 시술` · `하위 케이스` — `하위 제품` 없음)을 따른다(되적기 — 허브 검수 v05 N-5 · 도구 설명에 적는다) |
| `lower_holders` | 그런 행을 하나라도 가진 서로 다른 holder 수 |
| `inherited` | role `물려받음` holder 가 가진 행 수. **제품 노드의 `offer` 는 `0` 이다**(`null` 이 아니다 — 그 role 로 부르지 않는다 · §4-4 · 되적기 0.5.2: 허브 검수 v05 N-2 · `HUB backend/app/modules/gold/coverage.py:6`). **고민 노드의 `indication`** 은 0.5.2 부터 `inherited` 가 수다 — `self` 가 0 이면 HG1 이 낼 윗고민 행 수 · `self` 가 1 이상이면 `0`(§5-9 HG1-6) |

- 값 쪽 · 속성 쪽 노드는 `lower` · `lower_holders` · `inherited` 가 `null` 이다(펼칠 `g_scope` 가 없다) — **고민 노드의 `indication.inherited` 하나만 예외다**(0.5.2 — HG1).
- 되적기(0.5.2 — `$W/WORK-005-hub-v05.md` §9 A-2 ~ A-5 · 구현 때 정한 것): `lineup` 의 `lower_holders` = 「하위 *」 행의 서로 다른 holder 수 · `nodes` 에 같은 노드가 두 번 오면 준 대로 두 번 낸다 · `kinds[]` 순서 = §5-8 표의 행 순서(앱은 `kind` 코드로 찾는다) · 빈 `norm` 의 `g_entry` 행은 맞춤에서 건너뛴다(11-16 gold 에 0).
- 셈은 층마다 **서로 다른 `gid` 수**다. `pair` 로 읽는 종류(§5-8 — 회피 · 보완 · 같은 날 · 순서·간격)는 `a_layer.role` 로 가른다(`b` 없이 부른 것).
- **불변식**: `coverage` 의 수 = 같은 build 에서 §5-8 표의 조회를 그 노드 · 그 role 로 실제로 불러 센 수(§9 T16 — `overview` · `mechanism` 은 그 조회의 행 가운데 그 종류의 칸에 값이 있는 것). 셈과 조회가 어긋나면 앱이 「있다」 고 듣고 읽었는데 행이 없는 일이 생긴다.
- **앱의 required 판정(SPEC-002 §3-2 RQ1)은 이 셈과 같은 함수다**(0.5.1 — _RESUME §2 11-16 「SPEC 0.5.0 검수 뒤 결정 3」 ① · 검수 v05 F-1 · N-4). RQ1 은 (대상, 종류)의 `self` · `lower` · `inherited` 로 「자기 행 → 자기 0 이면 하위 층의 자기 행 → 아래층 어디에도 없으면 물려받은 값」 을 가른다 — 0.5.0 은 RQ1 이 행으로 · `coverage` 가 칸으로 세어 `mechanism` 에서 어긋났다. 이 불변식 하나(T16)가 둘을 함께 지킨다. 허브는 판정하지 않는다 — 셈만 낸다.
- **허브는 고르지 않는다** — 셈이 전부 0 인 후보도 그대로 낸다. 점수 · 순위 · 「가장 그럴듯한 후보」 가 없다. 고르는 것은 앱(Jev 대상 판단 — SPEC-002 §3-1).
- `ledger_check[]` 는 없다(§4-0 — 세 도구뿐). 층의 뜻은 semantic-map §5 그대로다 — 「하위」 는 그 대상 이름으로 일반화하지 않는 층이고(§5-3 S3), 「상위 제품」 · 「제품 경유」 · 「구성 항목」 은 세지 않는다.
- 11-16 gold 에서 이 셈이 드러내는 것(이 워커 셈 — `g_scope` · 속성 표 · 0.5.1 에 다시 세었다): 하위 층이 있는 대상 178(계열 18 · 시술 131 · 제품 29) 가운데 **`self` 0 이고 `lower` 가 1 이상**인 (대상, 종류) — 적응: 시술 33 · 제품 3 · 계열 1 / 효과: 시술 30 · 제품 3 · 계열 1 / 부작용: 시술 31 · 제품 3 / 상품: **계열 17 · 시술 0 · 제품 7**(0.5.2 — 아래 「상품 셈 식」 · 0.5.1 은 15 · 11 · 7 로 적었다) / 회복: 시술 4 / 금기: 시술 2. 그중 적응 34(시술 31 · 제품 3) · 효과 31(시술 28 · 제품 3)은 `inherited` 가 1 이상이라, 층을 가르지 않으면 윗층 행만으로 「있다」 로 보인다(SPEC-002 §3-2 RQ1 둘째 줄이 막는 꼴 · `$W/_RESUME.md` §1 e2e 피드백 3).
- **세는 식**(검수 v05 W-5): 위 수는 이 도구의 셈 그대로다 — holder = `g_scope` 의 그 role 행(`자기` 는 대상 자신) · 행 = §5-8 표의 조회가 맞추는 행. **적응은 `facets` indication 의 대상 쪽 맞춤(§4-4)대로 `concern_match` = 직접 인 행만** 센다 — 상위 고민으로 물었을 때만 나오는 펼침 행(`하위 고민` 2,498 · 빈칸 63)은 넣지 않는다. 검수가 다시 센 35(시술 31 · 제품 3 · 계열 1) · 32(시술 29 · 제품 3)는 그 펼침 행까지 넣어 `target_*` 칸으로 센 값이다(자기 행이 느는 만큼 「자기 0」 인 대상이 준다). 효과 · 부작용 · 상품 · 회복 · 금기는 두 식의 값이 같다.
- **상품 셈 식**(결정 0.5.2 — `$W/_RESUME.md` §5 11-16 「허브 v05 완료」 줄의 미결 「SPEC 되적기에서 정함」 · 허브 검수 v05 N-1 의 첫 선택지): `coverage` 의 `offer` 는 **§4-4 의 offer 맞춤 규칙 그대로** 센다 — procedure → `procedure_code` · procedure_case → 그 케이스의 `procedure_code` · product → `item_*`. 0.5.1 이 적은 15 · 11 은 `item_*` = holder 식으로 센 값이라 도구와 달랐다(구현은 계약 §4-4 에 맞았고 틀린 것은 SPEC 의 셈이었다 — `HUB backend/tests/test_gold_coverage.py:324-354` 가 두 식을 다 다시 센다). **§4-4 의 맞춤 규칙은 바꾸지 않는다**(0.4.1 결정 「허브 검수 뒤」 의 offer 규칙 그대로 — 바꾸면 계약 변경이다). 이 식에서 알아 둘 것 둘(허브 검수 v05 N-3 · U-3): 시술의 `self` 는 `procedure_code` 가 그 시술인 상품 전부라 하위 제품 · 케이스 항목의 상품까지 품고(그래서 「자기 0」 인 시술이 0 이다) · 시술의 `하위 케이스` 는 같은 `procedure_code` 로 맞추므로 `lower` 가 `self` 와 **같은 `gid`** 를 다시 센다(하위 케이스 상품이 전부 자기 행과 같은 시술 34 — 검수 셈). 「하위에 N 행」 이 새 정보가 아닐 수 있다 — 앱은 상품에서 `lower` 를 「하위에 따로 있는 정보」 로 말하지 않고 행의 `item_table` · `item_code` 로 가른다(SPEC-002 §3-2 RQ1 아래 0.5.2 불릿).
- **`self` 0 · `lower` 0 이고 `inherited` 만 1 이상**인 대상(0.5.1 — 같은 식 · 검수 v05 F-1 의 규모): 원리 — 입구 있는 제품 315 가운데 **314**(나머지 1 은 세 층 모두 0) · 케이스 3 / 적응 257(시술 15 · 케이스 180 · 제품 62 — 펼침 행까지 넣으면 246: 13 · 175 · 58) / 효과 221(시술 1 · 케이스 205 · 제품 15) / 부작용 194(시술 1 · 케이스 178 · 제품 15). 원리는 구조상 시술 · 계열 층에 있어 제품에서는 거의 늘 이 꼴이다 — 앱은 이것을 물려받은 값으로 채우고 층을 밝힌다(SPEC-002 §3-2 RQ1 셋째 줄).


## 5. 조회 규칙 — 도구가 지켜야 할 것

규칙의 정본은 `$SM/gold/semantic-map.md` 다. 여기에는 **허브 도구가 지킬 것**만 적고 원문은 절 번호로 가리킨다. **다만 §5-3 S5 와 SPEC-002 §3-2 RQ1 은 semantic-map §5 를 세 자리에서 바꿔 읽는다(S5 에 적었다) — 그 세 자리에서 두 글이 다르면 이 문서(와 SPEC-002)가 앞선다**(0.5.1 — 검수 v05 W-7 · 근거 = _RESUME §2 11-16 「길 찾기 재설계 진행」 · 「SPEC 0.5.0 검수 뒤 결정 3」 ①). semantic-map 파일(아카이브 · 로컬)은 고치지 않는다. 앱이 지킬 것(답에서 구분해 말하기)은 SPEC-002 §4.

### 5-1. resolve(semantic-map §1 · 조사 §1-5 · §3-1 T1)

| # | 규칙 | 근거 |
|---|---|---|
| R1 | 비교 키 = **`gold-build.py` 의 `norm` 과 같은 식** — 공백 연속 제거 + 소문자. 다른 정규화(NFKC · 괄호 지움 · 악센트 접기)를 **더하지 않는다** — 더하면 `g_entry.norm` 과 안 맞는다 | `gold-build.py:126-127` · 조사 §3-3 「resolve」 |
| R2 | **정확 일치**(0.8.0 — 0.5.0 의 「부분 일치」 를 바꿨다): 입력 **전체**를 R1 로 정규화한 문자열이 `g_entry.norm` 과 **같은** 행만 후보다. 부분 문자열로 훑지 않는다 · 낱말로 자르지 않는다 · 조사를 떼지 않는다 — 이름(또는 별칭) 하나를 글자 그대로 넣었을 때만 맞는다 | _RESUME §2 11-18 D-1(「맞춤 꼴은 정확한 이름 → 코드만」) · 같은 날 「resolve = 최소 목록 꼴 · 규칙을 더하지 않는다 · 입력 정리는 채팅 단에서」 · 까닭: 부분 일치가 관문이면 조사가 끼거나 어순이 바뀌거나 바꿔 말한 턴에서 정답이 후보에 없다(`$W/research-input-space.md` §2 — 후보 층 39 턴) · 0.5.0 ~ 0.7.2 의 규칙 = 「문장 `norm` 안에 부분 문자열로 든 `g_entry.norm` 전부」 |
| R3 | 조사 목록(옛 `PARTICLES` 16)은 **쓰지 않는다** — 목록에 없는 조사 하나로 입구가 0 이 되는 꼴이라 뺐다(R2) | 같음 |
| R4 | 옛 4단계 중 「끝말 떼기」 · 「접두」 는 **넣지 않는다** — 옛 `semantic.json resolve_rules` 기반이라 새 gold 에 근거가 없다 | 조사 §3-1 T1 |
| R5 | 오타 · 편집 거리 · 구어 풀이 · **문장 안의 이름 찾기** 없음 → 맞춤 꼴의 후보 0. 그 뒤는 부르는 쪽이 한다 — 목록 꼴(§4-1)로 입구 목록을 받아 고른다(상담 = SPEC-008 의 소넷 이해 호출 · 시험 앱 B 열 = 옛 판 0.7.2 에서 Jev Noul). 허브에 LLM · 점수가 들어오지 않는다 | 조사 §5-3 「오타」 · `$P/orchestration/work/phub-recommend/_RESUME.md:261`(10-30 「오타 처리 = 나중에 Jev 로」 — 허브 LLM 없음 경계 그대로) · _RESUME §2 11-18 「입력의 정리는 채팅 단에서」 |
| R6 | 겹침은 고르지 않고 전부 · 순서만 `gold-build.py:633-634` | §4-1 |
| R7 | ~~긴 조각이 먼저이되 짧은 조각도 남긴다(`matched.covered_by` 표지)~~ — **0.8.0 에서 지웠다.** 맞는 조각은 입력 전체 하나뿐이라 덮일 것이 없다. `norm` 길이 하한은 지금도 없다 — 한 글자 이름(16) · 두 글자 이름(235)도 그 글자를 그대로 넣으면 후보다 | _RESUME §2 11-18 D-1(「겹침 규칙 지움」) · 0.5.0 의 셈: 서로 다른 `norm` 2,541 가운데 다른 `norm` 의 부분 문자열인 것 551 — 0.7.2 까지 그 551 은 긴 이름을 말할 때마다 함께 후보였다 |
| R8 | 허브는 후보에 점수 · 순위를 매기지 않는다. 같은 `norm` 의 개념이 여럿이면 전부 내고 고르지 않는다(R6) — 「이 말이 무엇을 가리키나」 는 부르는 쪽이 정한다 | llms.txt §3-1 · _RESUME §2 11-18 「규칙을 더하지 않는다」 |
| R9 | ~~(0.7) 줄임 일치를 R2 위에 더한다~~ — **0.8.0 에서 지웠다**(§5-11 NM). 별칭 · 띄어쓰기는 지금도 규칙이 아니다 — 별칭은 이미 `g_entry` 행이고(`name_kind` 별칭 614 · 약어 61 · 다른 이름 46 · 의학 용어 76 — 0.7 재셈) 띄어쓰기는 R1 이 지운다 | _RESUME §2 11-18 D-1 |

문장 안에서 낱말을 어떻게 잘라 맞출지는 0.5.0 에서 「자르지 않는다 — 부분 문자열로 훑는다」 로 닫혔고(옛 O-4 의 (b)), **0.8.0 에서 「문장에서 찾지 않는다」 로 다시 바뀌었다**(R2). 0.4.1 구현은 (a) 공백 낱말 + 이웃 낱말 이어 붙임이었다(`HUB resolve.py:52-66` — 그때의 줄 번호).

### 5-2. 범위별 표 · role(semantic-map §5 · §6 · 조사 §6-4 표)

허브는 범위를 **판정하지 않는다.** 아래는 `resolve` 의 `in_range` 계산과, 부르는 쪽이 `roles` · `edge_types` · `hier` 를 고를 때 쓰는 고정 표다(앱 쪽 표는 SPEC-002 §3-2 — 같은 내용).

| 범위(8) | 시작 표(`in_range`) | 부를 도구 → 표 | role |
|---|---|---|---|
| 시술 | procedure · procedure_case · product · modality | `facets` profile · indication · outcome(+ 하위 목록 = `scope`) | 자기 · 물려받음 · **하위 *(0.5.0 — 앱이 명시 · S5)** |
| 부위·고민 | concern (+ site 는 칸 필터용) | `concern_candidates` · `facets` package(concern — 상위 고민 펼침) · (앱 B 가 폭에 더함 — SPEC-002 §3-2) `groups` 후보마다 `facets` profile | — (후보별 `facets` profile 은 `자기` · `물려받음` — 기본값) |
| 부작용 | 대상 4표 · adverse(값 쪽 시작 — 「이 사건이 나는 대상」 · 대상 쪽에서는 사건 필터) | `facets` adverse(대상 쪽 · 값 쪽 — 하위 사건 펼침) · adverse_detail · recovery | 자기 · 물려받음 · 하위 케이스 · **하위 시술 · 하위 제품(0.5.0 — S5)**(값 쪽 시작이면 role 없음) |
| 시술 조합 | 대상 4표 · concern | `pair`(보완) · `facets` package | + 하위 시술 |
| 동시 가능 | 대상 4표(두 끝) | `pair`(전 갈래 · `package_kinds` 같은 날 조합) | + 하위 시술 |
| 순서·간격 | 대상 4표 | `pair`(순서 · 간격 · 재시술 간격) | 같음 |
| 회피 | 대상 4표 · condition | `pair`(회피) · `facets` contraindication(하위 조건 펼침) | 같음 |
| 상품 | product · procedure · procedure_case · offer | `facets` offer | 제품 = 자기 · 하위 제품(**물려받음 없음** — §4-4 기본값 · 허브 검수 W-1) / 시술 · 케이스 · 계열 = 자기 · 물려받음 · 하위 *(S5) |

「대상 4표」 = modality · procedure · procedure_case · product. 부작용 범위의 값 쪽 시작은 역방향 조회다(조사 §3-2 6 · §6-3 끝 줄 「`facets` 의 필터로 닫힌다」 · 검수 W-3).

**속성 4표(material · method · anatomy · site)는 범위와 무관하게 시작 표다**(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가)). `resolve` 의 `in_range` 는 속성 4표 후보에 늘 참이고, 목록 꼴의 `range` 도 속성 4표를 품는다. 부를 도구 = `facets` 속성 쪽(§4-4 표) · role 없음. 그 범위의 대상 · 값 입구가 함께 풀렸으면 무엇으로 시작하고 속성을 칸 필터로 곁들일지는 앱이 정한다(SPEC-002 §3-1 단계 ① · §3-2) — 허브는 두 길을 다 연다.

입구 개념 수(11-16 `g_entry` 의 서로 다른 (`entity_table`, `entity_code`) — 이 워커 셈 · 목록 꼴 `counts.entities` 의 기대값): product 315 · concern 260 · adverse 188 · condition 151 · **material 143** · procedure 138 · offer 122 · package 119 · **anatomy 105** · **site 89** · effect 70 · **method 49** · procedure_case 44 · modality 18. 굵은 넷이 노드가 아닌 입구다(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) 셈과 같음). 속성 입구의 `norm` 이 다른 표와 겹치는 것은 59(재료 · 시술 40 · 고민 · 부위 13 · 방법 · 시술 3 · 재료 · 계열 2 · 해부 · 상품 1 — 이 워커 셈) — 고르는 것은 앱이다(§5-1 R6).

### 5-3. 물려받기(semantic-map §5)

| # | 도구가 지킬 것 |
|---|---|
| S1 | 펼침은 **`g_scope` 행으로만** 한다. 허브가 층을 새로 계산하지 않는다 |
| S2 | `roles` 기본은 `자기` · `물려받음` 뿐이다. 하위 · 경유 · 상위 제품은 부르는 쪽이 명시해야 나온다 — **이것을 `facets` · `pair` 의 도구 설명에 적는다**(§4-4 · 0.5.1 — 검수 v05 W-4) |
| S3 | 펼쳐 얻은 행마다 `layer`(role · path · holder)를 붙인다 — 「하위」 를 이 대상 이름으로 일반화하지 않게 하는 재료 |
| S4 | role 「상위 제품」 은 `scope` 가 그대로 내지만, `facets` 기본 role 에 없다(상위 제품 진술을 물려받지 않음 — semantic-map §5 첫 불릿) |
| S5 | **하위 층의 자기 행을 낸다 — 층을 밝혀서**(0.5.0). `roles` 에 「하위 *」 가 오면 그 holder 의 자기 행을 `layer.role` = 그 하위 role 로 붙여 낸다. 허브 기본값(S2)은 그대로이고, **앱 B 가 대상 쪽 조회에 `자기` · `물려받음` · `하위 시술` · `하위 케이스` · `하위 제품` 을 명시한다**(SPEC-002 §3-2). semantic-map §5 표의 「하위(이 대상 이름으로 일반화하지 않고 「하위」 표시)」 를 0.4.1 은 「표시만 — 읽을지는 Jev 깊이 판단」 으로 옮겼는데, 이것을 **「하위도 읽고 층을 밝힌다 · 상위 이름으로 일반화하지 않는다」** 로 바꾼 것이다. 일반화 금지(S3)와 상위 제품 진술을 물려받지 않는 것(S4)은 그대로다. **semantic-map §5 를 바꿔 읽는 자리는 셋이다**(0.5.1 — 검수 v05 W-7): (가) 표의 「하위」 칸 — 「표시만」 → 「읽고 층을 밝힌다」(위) (나) 같은 절 첫 불릿 「상품 질문에서만 하위 제품 상품을 모은다」 — 앱은 **적응 · 효과 · 부작용 등 대상 쪽 조회 전부에서** 하위 제품(과 하위 시술 · 케이스)의 자기 행을 읽는다. 층을 밝혀 그 하위의 것으로 말할 뿐 상위 이름으로 일반화하지 않으므로 그 불릿의 뜻(상위 ↔ 하위 진술을 섞지 않는다)은 그대로다 (다) 표 머리 「물려받음 = 위 층 진술이 이 대상에 적용」 — 앱의 required 판정(SPEC-002 §3-2 RQ1)은 **하위에 자기 행이 있는 종류에서는** 물려받은 행을 「보여 주기만 · 충족 아님」 으로 둔다(아래층 어디에도 자기 행이 없으면 semantic-map 그대로 물려받은 값으로 충족하고 층을 밝힌다). 이 셋에서 semantic-map 과 다르면 이 문서 · SPEC-002 가 앞선다(§5 머리) — 근거: _RESUME §2 11-16 「길 찾기 재설계 진행」(「대상 × 필요한 정보 안에서는 빠짐없이 · 하위 층 자기 행 포함 · 층 표시」) · `$W/_RESUME.md` §1 e2e 피드백 3(「자기 행 0 이고 g_scope 로 연결된 노드에 자기 행 있으면 Jev 무관 깊이 · 답은 층 밝힘」) · semantic-map §5 표 |
| S6 | **(0.5.2 — 바뀜 · §5-9 HG2 가 앞선다)** 「하위 *」 는 `g_scope` 의 하위 role 행을 **끝까지 따라간 자손 전부**다. 따라가는 것은 전부 `g_scope` 행이라 S1(「허브가 층을 새로 계산하지 않는다」)은 「허브는 `g_scope` 에 없는 관계를 만들지 않는다」 로 읽는다. 아래는 0.5.1 의 글이다(한 단이던 때의 한계와 셈 — 「놓치는 것」 은 HG2 로 잡힌다 · 「제품 경유」 는 여전히 하위가 아니라 따라가지 않는다): 하위는 **`g_scope` 의 하위 role 한 단**이다. 계열 → 시술 → 케이스처럼 두 단 아래(계열의 하위 케이스)는 `g_scope` 에 계열의 행으로 없어 나오지 않는다(S1 — 허브가 층을 새로 계산하지 않는다). 한 단으로 **놓치는 것**(0.5.1 — 검수 v05 W-8 · 이 워커 재셈): 두 단 아래에만 행이 있는 계열 — 상품 2 · 적응 · 효과 · 부작용 0 / 자기 0 이고 「제품 경유」 holder 에만 행이 있는 케이스 — 적응 80 · 효과 115 · 부작용 97(그중 입구 있는 케이스 8 · 14 · 5 — 「제품 경유」 는 하위가 아니라 읽지 않는다). 한계 = O-21 — 근거: `g_scope` role 셈(계열: 하위 시술 138 · 하위 제품 317 / 시술: 하위 케이스 268 · 하위 제품 309 / 제품: 하위 제품 37 — 이 워커 셈) |

### 5-4. 값을 바꾸지 않는다(semantic-map §3)

| # | 도구가 지킬 것 | 절 |
|---|---|---|
| V1 | `same_day` 빈칸을 채우지 않는다 · 보완 행을 같은 날 행으로 바꾸지 않는다 | §3-1 |
| V2 | 엇갈림 · 충돌 행을 고르거나 지우지 않는다 | §3-1 |
| V3 | 빈도 수치 칸과 서술 등급 칸을 합치지 않는다 · 부작용 지속과 회복을 한 표로 섞지 않는다(facet 이 다르다) | §3-2 · §3-3 |
| V4 | `polarity` 로 거르지 않는다(거르는 것은 `filters`) — 대신 `counts` 에 값별 셈을 낸다 | §3-5 |
| V5 | `price_mid_raw` 로 계산 · 정렬하지 않는다 | §3-6 |
| V6 | 숫자 칸을 숫자로 바꾸지 않는다(문자열 그대로) | §2-1 |

### 5-5. 계층 펼침(보조 입력 ① · _RESUME §2 11-16 「검수 뒤 결정 4」 ②)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| H1 | 펼침은 **보조 입력의 `parent_code` 로만** 한다. gold 행의 이름 · `adverse_top_name` 같은 글 칸으로 계층을 추측하지 않는다 | 결정 ② · semantic-map §1(고민 · 부작용 · 사람 조건 = 3단) |
| H2 | 펼치는 자리는 `facets` 의 세 곳뿐이다(§4-4 표) — 고민은 **위로**(패키지) · 부작용 · 조건은 **아래로** | `gold-build.py:921 · 734 · 860` |
| H3 | 넓힌 조회의 행마다 `hier{asked_code, match}` 를 붙인다. 행의 코드 칸은 바꾸지 않는다 | §4-0 |
| H4 | `hier` = `exact` 로 부르면 넓히지 않는다. 기본값(`expand`)은 제안이다 | O-12 |
| H5 | `pair` · `scope` · `neighbors` · `resolve` · `evidence` 는 보조 입력 ① 을 읽지 않는다. **`concern_candidates` 는 0.5.2 부터 읽는다** — 위로(HG1 윗고민) · 묶인 고민의 아래로(HG3) · `coverage` 의 고민 `indication` 도 같은 함수로 센다 | §4-5 · §4-6 · §5-9 |
| H6 | (0.5.2) HG1 은 **행이 0 일 때만** 위로 간다 — 자기 행이 있는 고민에 윗고민 행을 섞지 않는다(윗고민의 행은 형제 고민의 행이다). 넓힌 행마다 `hier{asked_code, match: 상위}` 를 붙이고 행의 코드 칸은 바꾸지 않는다(H3 과 같다) | §5-9 HG1 |

### 5-6. 원장 확인(보조 입력 ② · _RESUME §2 11-16 「검수 뒤 결정 4」 ③)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| L1 | `concern_candidates` · `facets` · `pair` 는 머리에 `ledger_check[]` 를 늘 낸다(없으면 `[]`) | §4-0 |
| L2 | 대조는 **코드 정확 일치**다 — 코드 → id 색인(§3-1)을 읽을 뿐 글을 다시 훑지 않는다 | `gold-build.py:648-651` |
| L3 | 허브는 「원천 미확정」 을 판정하지 않고 행을 빼거나 더하지 않는다 | SPEC-002 §5 |
| L4 | 응답에 원장 확인 목록의 글을 싣지 않는다 — id · 코드 · `on` 뿐 | §2-1 X5 |

### 5-7. 속성 쪽 시작(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) · semantic-map §1 · §3-4)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| A1 | 맞춤은 코드 → `g_entry.entity_name` → 칸 값 **글자 그대로 일치**다. `norm` · 부분 문자열 · 비슷함 계산을 쓰지 않는다(`site_code` 칸만 코드 일치) | §4-4 「속성 쪽」 · gold 칸이 이름을 담음(semantic-map §1 표의 「gold 칸」) |
| A2 | 여러 값 칸(`materials` · `methods` · `sites`)은 ` · ` 로 나눈 **항목 단위**로 맞춘다 | 이 워커 셈 — `g_profile.materials` 의 항목 139 종 · `methods` 39 종이 전부 입구 이름과 같다 |
| A3 | 맞춤 칸은 §4-4 표에 고정이다. 글 칸(`text` · `note` · `conditions` · `item_text` …)을 훑지 않는다 | 결정론 · 헤더 전수 |
| A4 | 맞은 행을 **전부** 낸다 — 쪽 넘김 끝까지 · 점수 · 상위 N 없음. 행마다 `attr.column` 을 붙여 부위의 역할을 섞지 않게 한다 | 원칙(_RESUME §2 11-16) · semantic-map §3-4 |
| A5 | 계층으로 넓히지 않는다 — 부위의 `parent_code` · 해부 ↔ 부위 잇기는 보조 입력에 없다. 정확 일치만 | _RESUME §2 11-16 「검수 뒤 결정 4」 ②(보조 입력 = 3표) · O-17 |
| A6 | 행의 칸 값은 gold 값 그대로다. 속성 이름을 행에 덧붙이거나 대상 이름으로 바꾸지 않는다 | §5-4 |

### 5-8. 정보 종류 표(_RESUME §2 11-16 「길 찾기 재설계 진행」 · 종류 나눔은 제안 — O-20)

`coverage`(§4-9)가 세는 단위이고, 앱이 「어떤 정보가 필요한가」 를 Jev 에 묻는 단위다(SPEC-002 §3-2a — 같은 표). **허브는 종류를 고르지 않는다** — 종류마다 어느 조회의 행을 세는지만 고정한다.

| `kind` | 이름 | 대상 쪽(대상 4표) — 세는 조회 | 값 · 속성 쪽 — 세는 조회 | 표 |
|---|---|---|---|---|
| `overview` | 개요 | `facets` profile 가운데 **개요 칸**(식별 칸 · 원리 칸을 뺀 칸 — `materials` · `methods` · `tissue_name` · `anatomy_name` · `site_name` · `product_kind` · `organizations` · `n_cases` · `n_products` · `overview` · `description`) 중 하나라도 값이 있는 행(0.5.1) | 속성 4표: `facets` profile 속성 쪽 | `g_profile` |
| `mechanism` | 원리 | `facets` profile 가운데 `mechanism_code` · `mechanism_name` · `mechanism_text` 중 하나라도 값이 있는 행 | — | `g_profile` |
| `indication` | 어디에 쓰나(적응) | `facets` indication | concern: `concern_candidates`(`counts.rows` — 쪽 밖 목록 포함 · 0.5.2: 자기 행은 `self` · HG1 로 물려받을 행은 `inherited`) · site: `facets` indication 속성 쪽 | `g_indication` |
| `outcome` | 효과 | `facets` outcome | effect: 값 쪽 · site: 속성 쪽 | `g_outcome` |
| `adverse` | 부작용 | `facets` adverse(딸린 `adverse_detail` 은 이 종류와 함께 읽는다 — 셈은 `g_adverse` 행) | adverse: 값 쪽 · site: 속성 쪽 | `g_adverse` |
| `recovery` | 회복 | `facets` recovery | — | `g_recovery` |
| `contraindication` | 금기(사람 조건) | `facets` contraindication | condition: 값 쪽 · site: 속성 쪽 | `g_contraindication` |
| `avoid` | 회피(같이 하면 안 되는 것) | `pair` `classes` = 회피 | — | `g_pair` |
| `combo` | 보완(같이 하면 좋은 것) | `pair` `classes` = 보완 | — | `g_pair` |
| `same_day` | 같은 날 | `pair`(갈래 전부 — `same_day` 칸은 어느 갈래 행에도 있다) | — | `g_pair` |
| `order_interval` | 순서 · 간격 | `pair` `classes` = 순서 · 간격 · 재시술 간격 | — | `g_pair` |
| `offer` | 상품 | `facets` offer(제품은 `자기` · `하위 제품` — §4-4) | offer: 값 쪽 · material · site: 속성 쪽 | `g_offer` |
| `package` | 패키지 | `facets` package | concern · package: 값 쪽 | `g_package` |
| `lineup` | 하위 목록(이 대상 아래의 시술 · 케이스 · 제품) | `scope` 의 「하위 *」 행 — `self` 는 0 · `lower` = 그 행 수(**0.5.2 — 자손 전부** · HG2) · `inherited` 는 `null` | — | `g_scope` |

- 「—」 = 그 표의 노드에는 이 종류가 없다(`coverage` 가 싣지 않는다). 패키지 노드는 `package`(값 쪽)뿐이다.
- **「이름」 칸은 사람이 읽는 말이다**(0.5.2 — _RESUME §2 11-17 「답 키 검토」 「「적응」 → 화면 · 표 말은 「어디에 쓰나」」): 화면 · 답 키 표 · 보고서에서 `indication` 은 **「어디에 쓰나」** 로 적는다. `kind` 코드 · gold 표 · 칸 이름(`g_indication` …) · Jev 에 주는 영어 이름은 그대로다. 이 문서 본문의 「적응」 은 gold 표를 가리키는 말로 남겨 둔다.
- 종류는 **행을 세는 단위**다 — `overview` 와 `mechanism` 은 같은 `g_profile` 행을 다른 칸으로 본 것이라 수가 겹친다(11-16 gold: `g_profile` 739 행 중 원리 칸에 값이 있는 것 420 · 개요 칸에 값이 있는 것 739 전부 — 이 워커 셈). **두 종류 모두 「칸에 값이 있는 행」 으로 센다**(0.5.1 — _RESUME §2 11-16 「SPEC 0.5.0 검수 뒤 결정 3」 ①): 0.5.0 은 `overview` 를 profile 행 전부로 적었다 — 지금 gold 에서는 수가 같지만(739) 식을 `mechanism` 과 맞췄다. 식별 칸 = `gid` · `subject_*` · `name_*` · `modality_*` · `procedure_*` · `silver_*` · `evidence_kind`.
- `same_day` 의 수는 `avoid` · `combo` · `order_interval` 의 수를 품는다(갈래 전부). 패키지(`package_kinds` 같은 날 조합)는 `coverage` 가 세지 않는다 — 두 끝이 있어야 뜻이 서는 값이다.
- 표의 조회 입력은 SPEC-002 §3-2 가 범위마다 고정한 것과 같다(`hier` = `expand` · 좁힘 입력 없음 — SPEC-002 §3-1 BR1 · BR2). 표를 바꾸면 두 문서를 함께 바꾼다.

### 5-9. 구멍 셋을 막는 규칙 — HG1 · HG2 · HG3(0.5.2)

(지시서 `$W/spec-v052-instructions.md` 의 H1 · H2 · H3 이다 — §5-5 의 H1 ~ H6 과 번호가 겹쳐 이 문서에서는 **HG** 로 적는다. 근거: `$W/_RESUME.md` §1 「허브 묶음 발주」 줄 · e2e 피드백 4 · _RESUME §2 11-17 「답 키 검토」 행 · 원칙(_RESUME §2 11-16 「길 찾기 재설계 진행」 「대상 × 필요한 정보 안에서는 빠짐없이」). **셋 다 한 문항의 예외가 아니라 일반 규칙이다.** 셈은 전부 이 워커가 로컬 CSV 로 다시 센 값이다 — `app-key-fix1-report.md` 「코디 요청 셈」 과의 대조는 규칙마다 적었다.)

**HG1 — 고민 → 윗고민 물려받음**(`concern_candidates` · `coverage`)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| HG1-1 | **걸리는 때** = 물은 고민의 `asked_concern_code` 행이 **0** 일 때다(`site` 거르기 **앞** · 쪽 밖 목록 포함 — `counts.unfiltered_rows` = 0). `site` 로 걸러 0 이 된 것은 해당 없다(O-9 그대로 — 0 과 `unfiltered_rows`). **기준을 「행 0」 으로 둘지 「묶음 0」 으로 둘지는 사용자 결정 U-3** — 본문 = 행 0 | `$W/_RESUME.md` §1 「허브 묶음 발주」 ① · 지시서 「고민 자기 적응 행 0 이고」 |
| HG1-2 | **어디까지 올라가나** = 보조 입력 ① 의 `parent_code` 로 한 단씩 올라가 **행이 1 이상인 첫 윗고민 하나**에서 멈춘다. 그 위는 더 가지 않는다 · 뿌리까지 행이 없으면 `200` · `total: 0` · `inherited_from: null`(0.5.1 과 같다). **「가까운 하나」 인지 「끝까지」 인지는 제안이다**(U-3 에 함께) | 아래 「몇 단」 셈 · _RESUME §2 11-17 「답 키 검토」(Q10 = 바로 위 윗고민 `CON-008` 의 적응으로) |
| HG1-3 | **무엇을 내나** = 그 윗고민을 `concern_code` 로 물었을 때와 **같은 행 전부**(`groups` · `modality_only[]` · `unreached[]` · 쪽 넘김 · `total` 단위 = 묶음 그대로). 윗고민의 「직접」 행만 고르지 않는다 — 윗고민으로 물은 행에는 형제 고민의 행(`concern_match` = 하위 고민)이 들어 있고, 그것은 행의 `concern_code` · `concern_match` 로 갈린다 | 답 키 K4(Q10 — 윗고민을 같은 도구로 부른 전체 행 · `app-key-fix1-report.md`) · 아래 셈(직접 행만 쓰면 13 가운데 5 가 다시 0 이다) |
| HG1-4 | **층 표시** = 머리 `inherited_from{concern_code, steps}` · 행마다 `hier{asked_code: 요청 코드, match: 상위}`. 행의 gold 칸(`asked_concern_code` · `concern_code` · `concern_match` …)은 **값 그대로**다 — 요청 코드로 바꿔 쓰지 않는다(§5-4 · §5-5 H3) | §4-0 `hier`(`package` 의 「상위」 와 같은 꼴) |
| HG1-5 | `ledger_check[]` 는 요청 코드만(넓히지 않는다 — O-14). `not_found` 기준은 그대로(`g_entry` 에 그 고민이 있나). `upper` = `none` 이면 이 규칙이 돌지 않는다 | §4-0 · §4-5 |
| HG1-6 | `coverage` 의 고민 노드 `indication` = `{self, inherited}` — `self` = 자기 행 수 · `inherited` = `self` 가 0 일 때 HG1-2 · HG1-3 이 낼 행 수(아니면 0) · `lower` · `lower_holders` 는 `null`. `concern_candidates` 와 **같은 함수**로 센다(T16 꼴) | §4-9 |
| HG1-7 | `facets` indication 값 쪽(`node` = concern — 직접만) · `facets` package(이미 상위 고민 전부로 넓힌다 — §4-4)는 바뀌지 않는다 | §4-4 |

- **RQ1 은 기존 물려받음 줄대로다**(SPEC-002 §3-2 RQ1 셋째 줄): 자기 행 0 · 물려받은 행 1 이상 → 물려받은 값으로 충족 + 답이 「윗고민의 것」 임을 밝힌다. 그래서 Q10 꼴은 「원천 미확정 (가)」 가 아니라 「근거 충족」 이 된다(행이 0 이 아니다) — _RESUME §2 11-17 「답 키 검토」 「윗층만 문항은 층 밝히면 정답」 과 같다.
- **셈 — 규모**(silver `concern` 260 · gold `g_indication` 4,866 행): 물은 고민의 **행이 0** 인 고민 = **13**(소분류 12 · 중분류 1 — `CON-012` · `105` · `106` · `107` · `136` · `203` · `205` · `206` · `230` · `239` · `250` · `257` · `259`). 13 전부 **바로 위 윗고민에 행이 있다**(바로 위는 0 이고 그 위에만 있는 고민 0). 13 전부 원장 확인 id 가 걸려 있다(`LCK-010` ~ `LCK-018` · `LCK-020` ~ `LCK-023` — Q10 과 같은 꼴이다).
- **앱 보고의 54 와 대조**: 앱은 `concern_candidates` 의 **`total`(= 묶음 수)** 이 0 인 고민을 세어 54 로 적었다. 이 워커가 같은 식으로 세면 **54 · 코드 목록까지 같다.** 그 54 = 행 0 인 **13** + 행은 있으나 묶음이 0 인 **41**(그 41 의 행 61 = `reach` 「계열 층만」 50 · 「패키지 — 항목 코드 없음」 8 · 「제품 — 케이스 없음」 3 — `modality_only[]` · `unreached[]` 로 나오는 자기 행이다). **단위가 다르다 — 행으로 0 은 13 · 묶음으로 0 은 54.** 41 은 자기 행으로 답할 것이 있어(RQ1 첫 줄) 본문은 13 만 올린다. 41 까지 올릴지가 U-3 이다.
- **셈 — 몇 단**: 13 가운데 윗고민이 한 단인 것 9 · 두 단인 것 4(`CON-012` · `203` · `205` · `206`). **0.6 고침 — 이 「단」 은 silver 조상 사슬의 길이다**(그 4 는 가까운 윗고민 위에 윗고민이 하나 더 있다). 응답 머리 `inherited_from.steps`(행이 있는 가장 가까운 윗고민까지 몇 단)는 **실물에서 13 전부 1** 이다 — `steps` 2 는 합성 시험으로만 선다(`$W/impl-v052-hub-report.md` WP-3 · `$W/app-v052-report.md` 미결 2). SPEC-002 §9-3d 의 HG1 (ii) 는 조상 사슬 길이로 고른다. 가까운 윗고민 하나의 행 합 = 1,033(고민마다 36 ~ 181) · 뿌리까지 다 합치면 1,695. **가까운 윗고민으로 물은 행은 그 위 윗고민으로 물은 행에 통째로 들어 있다**(두 단인 고민 51 전부에서 확인 — gold 가 아래로 펼쳐 두었기 때문) — 그래서 끝까지 올라가도 가까운 윗고민에 없던 「이 고민에 더 가까운」 행은 하나도 늘지 않고, 더 먼 가지(형제의 형제)의 행만 는다. 예: `CON-012` → `CON-008` 181 행(직접 42 · 하위 고민 139 · 묶음 65) / `CON-001` 까지면 524 행. **추천 = 가까운 하나.**
- 37 문항에서 바뀌는 것: **Q10 하나**(`CON-012`). 허브 응답이 `total` 0 → 윗고민 묶음 65(`inherited_from` · `hier` 표지) · `ledger_check[]` 는 그대로 `LCK-010`. 답 키는 키 전용 윗층 기준 대상(SPEC-002 §9-5 `key_upper_entries`)을 빼고 다시 뽑아 행이 같은지 대조한다(`app-key-fix1-report.md` 미결 1).

**HG2 — 「하위 *」 = 자손 전부**(`scope` · `facets` · `pair` · `coverage`)

0.5.1 은 하위를 `g_scope` 의 하위 role **한 단**으로 두고(§5-3 S6) 넓힐지를 1회차 trace 뒤로 미뤘다(옛 O-21 (a)). 그 trace 가 났다 — 계열을 대상으로 둔 Q12 의 표본 4 가운데 2(둘 다 케이스 행 — `gid` 는 `app-key-fix1-report.md` K4 에 있다)가 키에서 빠졌다(`app-key-fix1-report.md` K4 · 미결 2). 구현은 0.5.1 계약(S6)대로였고 **바뀌는 것은 계약이다** — 「하위 = 자손 전부」 를 부작용 · 조건 계층(§4-4)에 이어 `g_scope` 의 층에도 같게 둔다(`$W/_RESUME.md` §1 「허브 묶음 발주」 ② · _RESUME §2 11-17 「답 키 검토」 「Q12 대상 = 계열 전체」).

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| HG2-1 | **닫힘**: 대상의 「하위 *」 role `g_scope` 행의 holder 에서 시작해, 그 holder 를 `subject` 로 삼은 「하위 *」 행을 **더 없을 때까지** 따라간다. 따라가는 것은 전부 `g_scope` 행이다 — 허브가 관계를 만들지 않는다(S1) | `g_scope` role 셈(§5-3 S6) |
| HG2-2 | **따라가는 role = 요청이 준 「하위 *」 role 뿐**이다. `물려받음` · `제품 경유` · `상위 제품` · `구성 항목` 으로는 따라가지 않고, **`자기` · `물려받음` 으로 닿은 holder 에서 다시 내려가지 않는다**(윗층에서 내려가면 형제 대상의 행이 섞인다 — 이 워커가 그 식으로 잘못 세었을 때 한 제품의 조회에 형제 제품 행 153 이 붙었다) | 원칙(대상 × 필요한 정보 **안에서**) · semantic-map §5 |
| HG2-3 | **한 holder 는 한 번**이다 — 여러 길로 닿으면 가장 얕은 `depth` · 같으면 `scope_gid` 가 작은 길 하나. 닫힘에 순환은 없다(11-16 gold: 순환 0 · 자기 고리 0 — 이 워커 셈) · 있어도 방문한 holder 를 다시 가지 않는다 | 결정론(§9 T6) |
| HG2-4 | **층 표시**: 따라가 얻은 행의 `layer.role` · `layer.path` · `layer.holder` · `layer.scope_gid` 는 **마지막 단**의 `g_scope` 행 값 그대로이고, 계산 필드 `layer.depth`(1 부터) · `layer.via[]`(대상에서 그 holder 사이의 holder — `{holder_table, holder_code, scope_gid}` · `depth` 1 이면 `[]`)가 **모든 대상 쪽 행에** 붙는다. 이름 · 꼴은 제안(O-23) | §4-0 `layer` · S3(일반화 금지의 재료) |
| HG2-5 | **적용 자리**(같은 닫힘 함수 하나): ① `scope.holders[]`(§4-2) ② `facets` 대상 쪽 `rows[]` — `roles` 에 「하위 *」 가 왔을 때(§4-4 · 기본값 `자기` · `물려받음` 은 그대로) ③ `pair` 의 두 끝 펼침 · 패키지 맞춤(§4-6 규칙 1 · 3) ④ `coverage` 의 `lower` · `lower_holders` · `lineup`(§4-9 · §5-8). 계층 3표(부작용 · 조건 — §4-4 「계층 펼침」)와 `concern_candidates` 는 이 규칙과 무관하다 | §4-2 · §4-4 · §4-6 · §4-9 |
| HG2-6 | 입력 `descend` = `all`(기본) \| `one`(`scope` · `facets` · `pair`) — `one` 은 0.5.1 과 같은 한 단이다. **기본이 `all` 이어야** 도구를 스스로 고르는 쪽(SPEC-002 의 C 열)이 구조적으로 못 읽는 일이 없다(0.5.1 검수 v05 W-4 와 같은 까닭). 입력을 둘지 · 이름은 제안(O-23) | 검수 v05 W-4 |
| HG2-7 | 도구 설명에 「하위 role 은 그 아래의 아래까지 전부 · `layer.depth` 로 몇 단인지」 를 적는다 | §5-3 S2 |

- **셈 — 한 단으로 안 닿던 자손**(`g_scope` 4,202 행 · 이 워커 셈): 계열 → **케이스 268**(계열 **18 전부** · 계열별 하위 시술 수 / 그 아래 케이스 수 = M1 1/22 · M2 3/15 · M3 7/10 · M4 6/5 · M5 3/2 · M6 2/5 · M7 11/15 · M8 6/46 · M9 3/17 · M10 2/3 · M11 1/9 · M12 1/6 · M13 2/4 · M14 1/2 · M15 58/72 · M16 22/27 · M17 3/3 · M18 6/5) — **앱 보고의 18 계열 · 합 268 · 계열별 수와 전부 같다.** 앱 보고에 없던 것: 계열 → 제품 24(계열 7) · 시술 → 제품 7(시술 4) · 제품 → 제품 1. 가장 긴 길은 4 단(계열 → 시술 → 제품 → 제품 → 제품).
- **셈 — 그 자손이 가진 자기 행**(적응은 `concern_match` = 직접): 계열 → 케이스: 적응 243(계열 15 · 케이스 86) · 효과 158(12 · 61) · 부작용 415(14 · 90) · 회복 9(2 · 8) · 금기 0 · profile 268(18 · 268) · 상품(`item_*` = 그 케이스) 59(15 · 44) / 계열 → 제품 24: 적응 49 · 효과 64 · 부작용 73 · 금기 4 · profile 24 · 상품 2 / 시술 → 제품 7: 적응 4 · 효과 9 · 부작용 12 · profile 7 · 상품 4 / 제품 → 제품 1: 효과 4 · 부작용 3 · profile 1. 그 케이스를 한 끝으로 둔 `g_pair` 행 **100**(서로 다른 `gid` — 계열마다 더한 값은 104 · 0.6 고침: 0.5.2 의 129 는 구현에서 다시 나오지 않았다 — `$W/impl-v052-hub-report.md` W-2) · 그 케이스가 항목인 `g_package` 행 58.
- RQ1 판정이 바뀌는 (대상, 종류)는 작다 — 자기 0 · 한 단 하위 0 · 두 단 아래에만 행: 상품(`item_*` 식) 계열 2 뿐(0.5.1 S6 의 「상품 2」 와 같다). **바뀌는 것은 대부분 판정이 아니라 폭이다**(읽히는 행이 는다).
- 37 문항에서 바뀌는 것(답 키 명세의 호출을 두 식으로 다시 센 것 — 이 워커 셈 · `filters` 는 정확 일치로만 세었다): **6 문항** — Q03(계열 `M1` profile + 22 = 케이스 22) · **Q12**(계열 `M2` 부작용 + 2 = 빠졌던 표본 둘 · 딸린 `adverse_detail` + 188) · Q19(쌍 14 → 18) · Q20(9 → 12) · Q25(5 → 6) · Q27(7 → 9). 계열이 대상이지만 행이 안 느는 문항: Q18 · Q21 · Q22 · Q23 · Q28 · Q30 · Q36(쪽 밖 `same_day_packages[]` 는 이 셈에 넣지 않았다 — 다시 뽑을 때 대조한다). Q03 · Q12 는 키 전용 하위 기준 대상(SPEC-002 §9-5 `key_lower_entries`)을 빼고 다시 뽑아 행이 같은지 대조한다(`app-key-fix1-report.md` 미결 2).
- §4-9 끝 불릿들과 §5-3 S6 의 `lower` 수(0.5.1)는 **한 단 기준**이다 — HG2 뒤의 수는 WORK 에서 T16 으로 다시 센다(위 셈이 느는 양이다).

**HG3 — 고민 + 부위 → `concern_site`**(`concern_candidates` 의 `site`)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| HG3-1 | `site` 를 주면 물은 고민의 행(HG1 이 돌았으면 윗고민의 행) 가운데 **(i) `site_name` 또는 `case_site_name` 이 그 글자와 같은 행**(0.5.1 그대로) **또는 (ii) 행의 `concern_code` 가 「그 부위에 묶인 고민 · 그 하위 고민(자손 전부)」 인 행**을 낸다 | `$W/_RESUME.md` §1 e2e 피드백 4 · 「허브 묶음 발주」 ③ |
| HG3-2 | 「묶인 고민」 = 보조 입력 ③ 에서 `site_code` 가 그 부위인 `concern_code`. 부위 코드는 `site` 글자 → `g_entry` 의 site 입구 가운데 `entity_name` 이 **글자 그대로 같은** 것(§5-7 A1 과 같은 식 · 코드마다 이름 하나). 같은 이름의 부위 입구가 없으면 (i) 만 돈다 | §4-4 「속성 쪽」 맞추는 법 |
| HG3-3 | **새 행을 만들지 않는다 · 대상을 바꾸지 않는다.** (ii) 의 행은 전부 물은 고민으로 이미 펼쳐져 있던 `g_indication` 행이다(`asked_concern_code` = 물은 고민). `resolve` 는 건드리지 않는다 — 허브가 「이 말은 사실 하위 고민이다」 를 고르지 않는다(§5-1 R6 · R8) | 아래 「어디서 합치나」 |
| HG3-4 | 행마다 계산 `site_match[]` — `column`(글자 일치 · 어느 칸인지는 행의 칸 값으로 보인다) · `concern_site`(묶임 — `csi_ids[]` = 그 묶임의 `concern_site.id`). 둘 다면 둘 다 적는다. 머리 `counts.by_site_match` | 되짚기(`artifact-traceability.md` — 묶임의 silver id 를 남긴다) |
| HG3-5 | 부위 계층으로는 넓히지 않는다(상위 부위로 걸면 하위 부위에 묶인 고민은 안 맞는다 — O-17 ① · ⑤ 그대로 · 묶인 부위 51 가운데 부모가 있는 것 12) | O-17 |
| HG3-6 | `site` 로 0 이면 0 그대로 + `unfiltered_rows`(O-9 그대로) | §4-5 |
| HG3-7 | (0.7.1 · 기준 0.7.2) **HG3 으로 행을 거르는 것은 물은 부위가 물은 고민의 `sites[]`(자기 또는 하위 고민의 묶임) 안에 있을 때뿐이다**(0.7.2 — 23,140 짝 가운데 191 짝 · 고민 100). 그 밖의 짝 — `sites[]` 가 `[]` 인 고민(160) · `sites[]` 는 있으나 물은 부위가 그 안에 없는 짝(8,709) — 은 같은 맞춤을 **표지로만** 쓴다 — §5-11 SP. `site_mode` = `filter` 면 모든 짝에서 HG3-1 ~ HG3-6 그대로다. (0.7.1 은 「물은 고민에 묶인 부위가 있을 때」 였다 — 변경 기록 0.7.2) | _RESUME §2 11-17 「① 규칙(사용자 결정)」 · 「규칙 변경 = 넣음」 |

- **어디서 합치나 — 제안 = `concern_candidates` 안에서**(O-24): (a) **도구 안에서 `site` 맞춤을 넓힌다**(본문) (b) `resolve` 가 「고민 + 부위」 를 묶인 하위 고민으로 바꿔 낸다. (a) 를 고른 까닭: 물은 대상이 그대로라 글자 일치 행도 남고(아래 예에서 (b) 는 글자 일치 24 행을 잃는다) · 행이 전부 이미 gold 에 있는 행이라 `evidence` 길이 그대로이고 · 한 조회라 C 열도 같은 도구로 같은 행을 받고 · 허브 `resolve` 가 뜻을 고르는 일이 생기지 않는다. (b) 는 묶임이 둘 이상인 부위(한 부위에 고민 여럿)에서 대상을 여럿으로 쪼개야 한다.
- **`concern_site` 를 어디서 읽나 — 사용자 결정 U-4**: gold 15표 · `g_edge` · `g_evidence` 어디에도 이 표가 없다(`g_evidence.silver_table` = `concern_site` 0 행 · `g_edge` 관계 23 종에 없음 — 이 워커 셈). (a) **보조 입력 ③ 으로 허브가 silver 를 읽는다**(본문 — 계층 3표와 같은 길 · gold 불변) (b) gold 에 표 · 관계를 더한다(gold-build · gold-check · gold 해시 · 「15표」 가 바뀐다). 「gold 는 silver 값 그대로」 는 둘 다 지킨다. **추천 (a)** — 11-16 「검수 뒤 결정 4」 ② 가 같은 꼴(계층)을 「보조 입력 · gold 불변」 으로 정했다. 다만 **보조 입력이 느는 것은 0.5.1 이 「그때 사용자에게 묻는다」 로 적어 둔 결정**(O-17 (b))이라 본문에 제안으로만 넣었다.
- **셈 — 규모**(silver `concern_site` 95 행): 고민 85 · 부위 51(전부 `g_entry` 에 입구가 있고 이름이 silver 와 같다). (윗고민, 부위) 짝 = **97**(윗고민 20) — 그 가운데 글자 일치만으로는 **0 행인 짝 40** · HG3 으로 행이 느는 짝 89 · 안 느는 짝 8 · 97 짝의 행 합 289 → **1,722**(0.6 고침 — 0.5.2 의 1,700 은 구현 · 검수 셈과 달랐다: `$W/impl-v052-hub-report.md` W-2 · `$W/review-spec-v052.md`).
- **셈 — e2e 피드백 4 의 꼴**(`CON-001` × `SITE-014`): 글자 일치 **24 행 · 묶음 2**(전부 `case_site_name` 으로 맞음) → 묶인 `CON-005` 의 행 54(묶음 15)를 더해 **73 행 · 묶음 16**. `_RESUME` §1 의 「2행」 은 **묶음 2**(행은 24)다 · 「직접 54 행」 은 이 워커 셈과 같다.
- **셈 — 같은 구멍의 다른 꼴**: 묶인 고민 **자신**을 그 부위와 함께 물으면(예: `CON-005` + `SITE-014`) 0.5.1 은 글자 일치로만 걸러 **95 짝 가운데 58 이 0 행**(행이 주는 짝 86)이 된다 — 부위가 고민 이름에 이미 들어 있어 행의 부위 칸은 비어 있기 때문이다. HG3-1 (ii) 가 이것도 함께 막는다(묶인 고민 자신의 행은 전부 맞는다).
- 37 문항에서 바뀌는 것: **0**(답 키 명세 37 에 부위 입구 0 · `site` 를 건 `concern_candidates` 호출 0 — 이 워커 셈 · `app-key-fix1-report.md` K7 과 같다). 그래서 **시험 세트 묶음이 있어야 잰다**(SPEC-002 §9-3d).

**시험 세트 묶음 제안** — 문항 꼴 · 수는 SPEC-002 §9-3d 에 적었다(문장은 쓰지 않는다): HG1 3 · HG2 3 · HG3 4.


### 5-10. 0.6 되적기 — 0.5.2 구현에서 정해진 것(계약 변경 없음)

근거: `$W/impl-v052-hub-report.md` 「구현 때 정한 것」 · `$W/review-code-v052-hub.md`(PASS · WARN 0) · _RESUME §5 11-17 「허브 0.5.2 완료」 줄. §5-9 의 규칙을 바꾸지 않는다 — 본문이 열어 둔 꼴을 구현 값으로 닫아 적는다.

| # | 정해진 것 | §5-9 의 자리 |
|---|---|---|
| R1 | 하위 닫힘은 **요청 때 따라간다**(`g_scope` 를 대상별로 색인 하나 · 미리 펼친 표를 두지 않는다) — `scope` · `facets` · `pair` · `coverage` 가 같은 함수 하나를 쓴다 | HG2 |
| R2 | `health.aux.concern_site{rows, concerns, sites}`(실물 95 · 85 · 51) · 보조 입력 파일 6 · `aux_hash` 는 0.5.1 값과 다르다 | §2 보조 입력 ③ |
| R3 | `descend` = `one` 은 0.5.1 과 **같은 행 · 순서 · `total` · `counts`** 에 `depth` 1 · `via` [] · `request.descend` 만 더한 것이다 | HG2 |
| R4 | `counts.unfiltered_rows` = `site` 를 안 걸었을 때 그 응답이 낼 행 수(윗고민을 물려받았으면 윗고민의 행 수) | HG3 |
| R5 | `site_match[]` 의 꼴 = `{by: column}` · `{by: concern_site, csi_ids[]}` | HG3 |
| R6 | 대상 쪽 holder 순서 = (`depth`, 그 `g_scope` 행의 `gid`) → 행 `gid` · 같은 `depth` 의 길이 둘이면 **마지막 단 `g_scope` 행의 `gid` 가 작은 길**(너비 우선) | HG2 |
| R7 | `scope` 에 `roles` 가 없으면 하위 셋을 전부 따라간다 · `depth` 1 행은 0.5.1 처럼 전부 낸다 · 닫힘의 방문 집합에 대상 자신을 넣어 대상으로 돌아오는 고리에서 멈춘다 | HG2 |
| R8 | `concern_candidates` 응답 머리 순서 = `build` · `request` · `total` · `next_cursor` · `inherited_from` · `counts` · `groups`(+ 첫 쪽의 쪽 밖 목록 · `ledger_check`) | HG1 |
| R9 | 그래프로 센 가장 긴 하위 길 = **4 단** · 응답 `layer.depth` 의 실물 최댓값 = **2**(제품의 하위 제품을 거치는 길 13 건이 `depth` ≥ 2 · `via` 끝 = 그 제품) | HG2 셈 |
| R10 | **제품의 하위 제품 길도 자손이다** — 계열 → 제품 → 하위 제품의 자기 행이 대상 조회에 온다(Q12 꼴에서 `g_adverse_detail` 4 행 — 0.5.2 답 키 483 → 487 · 옛 키 전용 하위 시술 셋으로는 못 닿던 길) | HG2 「자손 전부」 |

- HG2 뒤 하위 행 합(한 단 → 전부 — 구현 셈): 적응 3,590 → 3,886 · 효과 2,321 → 2,556 · 부작용 3,854 → 4,357 · 회복 18 → 27 · 금기 62 → 66 · 상품 293 → 299 · 패키지 120 → 178 · `pair` 전 갈래 275 → 377. T16 의 자기 · 한 단 셈은 그대로다.
- **0.6 에서 SPEC-002 가 허브에 기대는 것**(계약 변경 없음 — 전부 이미 있는 입력): `scope` 의 `물려받음` · `하위 *` 행으로 대상의 계보를 본다(SPEC-002 §3-7-3 PR1) · `facets` adverse_detail 의 `filters.adverse_risk_id`(§4-4 — SPEC-002 §3-7-5 BR5) · `resolve` 목록 꼴의 `norm`(SPEC-002 §3-7-4 VP3). 구현 첫 확인에서 안 되는 것이 있으면 그때 계약으로 올린다.

### 5-11. 0.7 — 시술로 내려가기(DP) · 고민 부위(CS) · 이름 맞춤 보강(NM — 0.8.0 에서 지움) · 고민 + 부위: 거름 / 우선 표시(SP — 0.7.1 · 기준 0.7.2)

(지시서 `$W/spec-hub-v07-instructions.md` 의 H1 · H2 · H3 이다 — §5-5 의 H · §5-9 의 HG 와 번호가 겹쳐 이 문서에서는 **DP · CS · NM** 으로 적는다. 근거: _RESUME §2 11-17 「얼굴 점 = 대화에서 나온 고민 부위 · 점(고민 부위)을 누르면 그 고민의 관련 시술 리스트 · V라인주사 등 「메뉴」 는 시술 아님 · 리스트는 우리 기준의 시술(계열 M > 시술 PRC > 케이스 CAS · 제품 PRD 는 따로)로」 · `$W/_RESUME.md` §1 「수정 2 목록」 00 · 2 · 6 · 9. **셋 다 한 문항 · 한 고민의 예외가 아니라 일반 규칙이다.** 셈은 전부 이 워커가 로컬 CSV 로 다시 센 값이다 — 재셈 스크립트 · 결과는 완료 보고에 있다. 용어: 계열 = `modality`(M) · 시술 = `procedure`(PRC) · 케이스 = `procedure_case`(CAS) · 제품 = `product`(PRD) · 패키지 = `package`(PKG) — `$SM/notes/glossary.md` §1 ~ §3. 「메뉴」 = silver `package.kind` 의 값 하나다(57 패키지).)

**DP — 시술로 내려가기**(`concern_candidates` 의 `descended[]`)

0.6 까지 `concern_candidates` 는 `procedure_code` 가 빈 행을 `modality_only[]`(「계열 층만」) · `unreached[]`(「패키지 — 항목 코드 없음」 · 「제품 — 케이스 없음」)로 **따로 낼 뿐** 시술로 잇지 않았다. 그래서 그 행뿐인 고민은 묶음(`total`)이 0 이었다 — 앱은 「시술 이름 없음」 으로 읽었다(`$W/_RESUME.md` §1 「수정 2 목록」 8 ③).

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| DP1 | **무엇을 내리나** = 이 응답의 `modality_only[]` · `unreached[]` 행 전부(= `procedure_code` 가 빈 행). `site` 로 거른 뒤 · HG1 로 윗고민 행을 물려받았으면 그 행이다. `groups` 의 행은 이미 시술에 닿아 있어 내리지 않는다 | §4-5 · `HUB backend/app/modules/gold/concern.py:70-78` |
| DP2 | **어떻게 내리나** = 행의 대상(`target_table` · `target_code`)에서 **`g_scope` 행만** 따라 첫 계열 또는 시술에 닿을 때까지: 패키지 → role `구성 항목` 의 holder(계열 · 시술 · 케이스) / 제품 → role `물려받음` 의 holder 가운데 **가장 좁은 층 하나**(케이스가 있으면 케이스 · 없으면 시술 · 없으면 계열) / 케이스 → role `물려받음` 의 시술 / 계열 → 그대로. **계열에 닿으면 그 계열의 role `하위 시술` holder 전부**가 내린 시술이다. **시술에 먼저 닿으면**(`lands` = `procedure` — 실물 0) 그 시술의 계열 묶음에 넣고 닿은 시술은 `from[].procedure_codes[]` 로 알린다 — 꼴은 §4-5 `from[].lands` 줄(0.7.1 · 검수 W-2). 허브가 관계를 만들지 않는다(§5-3 S1) · silver 를 더 읽지 않는다 | 지시서 H1 「연결을 끝까지 따라가 시술(PRC)로」 · `g_scope` role 셈(패키지 `구성 항목` → 계열 144 · 케이스 58 · 시술 53 / 계열 `하위 시술` 138 — 재셈) |
| DP3 | **메뉴 · 패키지 · 제품 · 계열 이름은 시술이 아니다.** 내린 결과에서 그것들은 `from[].path[]` 에만 나온다. `descended[].procedures[]` 의 코드는 전부 `g_scope` 의 `procedure` holder 이고, `groups[]` 의 `candidate_table` 은 0.6 그대로 `procedure` · `procedure_case` 뿐이다 — **시술 자리에 패키지 · 메뉴 코드가 나오는 일은 0 이어야 한다**(T24) | _RESUME §2 11-17 「V라인주사 등 「메뉴」 는 시술 아님 → 시술로 내지 않음」 |
| DP4 | **하위 일반화 금지 = 계열 단위 표지.** 내린 시술은 **계열 묶음 안의 목록**으로만 나온다(`unit` = `계열`). 허브는 내린 시술마다 `g_indication` 꼴의 행을 **짓지 않는다** — 그 적응은 시술 하나하나의 것이 아니라 `from[]` 의 행이 말한 층의 것이다. `groups[]` 에 섞지 않는다 | 지시서 H1 「하위 일반화 금지는 계열 단위 표지로 지킨다(내린 시술 하나하나에 그 적응을 자기 것으로 적지 않음)」 · §5-3 S3 · semantic-map §5 「계열 층만으로 따로」 |
| DP5 | **경로를 붙인다** — `from[]` 의 항목마다 `gid`(내려온 `g_indication` 행) · `reach` · `path[]`(대상 → … → 계열 · 따라간 `g_scope` 행의 `gid` 포함). 근거 추적은 그 `gid` 로 `evidence` 를 부르는 기존 길 그대로다(§6) — `descended[]` 자신은 gold 행이 아니라 계산이다 | 지시서 H1 「어디를 거쳐 내려왔는지 층 표시(경로)」 · `artifact-traceability.md` |
| DP6 | **고르지 않는다 · 자르지 않는다.** 계열의 시술 전부 · 내려온 길 전부를 낸다(쪽 밖 목록 — 한도 없음). 이미 `groups` 에 있는 시술도 빼지 않고 `in_groups` 로만 알린다 — 무엇을 보여 줄지는 앱이다 | 원칙(_RESUME §2 11-16 「폭은 빠짐없이」) · §4-0 |
| DP7 | **순서**(결정론): `descended[]` = 계열의 `g_scope` 「자기」 행 `gid` 오름차순(없으면 `modality_code` 문자열) · `procedures[]` = `scope_gid` · `from[]` = `gid` · 같은 행이 한 계열에 여러 길로 닿으면 `path[]` 의 `scope_gid` 열이 작은 길 하나. 한 행이 계열 둘에 닿으면 두 묶음에 다 나온다. 「오름차순」 은 **`gid` 글자 순**이다(0.7.1 — 검수 N-8 · `gid` 는 표마다 자릿수가 같아 글자 순 = 수 순 · 기존 묶음 순서 — §4-5 「순서 = 묶음의 첫 행 `gid`」 — 와 같은 식) | §9 T6 |
| DP8 | **안 바뀌는 것**: `groups[]` · `modality_only[]` · `unreached[]` · `total` · 기존 `counts` 칸 · `inherited_from` · `ledger_check[]`(요청 코드만) · `coverage` 의 셈(T16 그대로 — 고민 `indication` 은 행 수다) · `facets` · `pair` · `scope`. `not_found` · 행 0 의 경계도 그대로다(행이 0 이면 `descended` = `[]`). **`to_procedure` = `none` 이면 `descended` · `counts.descended` 두 필드가 없다**(0.7.1 — 검수 N-3: 「싣지 않는다」 · `null` · 「필드 없음」 세 가지로 적혀 있던 것을 「필드를 뺀다」 하나로) | 지시서 「응답 필드 추가는 기존 필드를 바꾸지 않음」 |
| DP9 | 못 내린 행(대상에서 `g_scope` 로 계열 · 시술에 안 닿음)은 `unreached[]` 에 그대로 두고 `counts.descended.undescended` 에 센다. 조용히 버리지 않는다 | llms.txt §3-4 |

- **셈 — 내릴 행**(gold `g_indication` 4,866 행): `procedure_code` 가 빈 행 **722** = 「계열 층만」 539 · 「패키지 — 항목 코드 없음」 128 · 「제품 — 케이스 없음」 55. 서로 다른 대상 = 계열 17 · 패키지 36 · 제품 8. **그 61 대상 전부가 DP2 로 계열에 닿는다**(못 내리는 대상 0 · 못 내리는 행 0 · 내림이 끝난 자리 = 전부 계열 — 시술에 바로 닿는 길(`lands` = `procedure`)은 실물 0 이라 합성 시험으로만 선다). **722 행 가운데 23 행(계열 층 14 · 패키지 9)은 고민 코드가 빈 행**이라 어느 `concern_candidates` 응답에도 나오지 않는다(DP1 은 「이 응답의 행」 만 내린다) — 도구로 실제 내려지는 행은 **699** 다(0.7.1 — 검수 N-7 · 0.6 부터 그 행은 이 도구로 닿지 않았다 · 「못 내리는 행 0」 은 그대로 참).
- **셈 — 「항목 코드 없음」 패키지 36 은 전부 kind 「메뉴」 다**(silver `package` 의 메뉴 57 가운데 36). 그 항목은 전부 계열이다(`g_scope` 「구성 항목」 holder 47 행 전부 `modality`). 즉 「메뉴」 는 「계열 하나(또는 몇)의 병원 상품 이름」 꼴로 들어 있고(`$W/_RESUME.md` §1 「수정 2 목록」 9), 이 규칙은 그것을 경로로만 남기고 계열의 시술로 내린다. 제품 8 은 `g_scope` 에 `물려받음` → 계열 행뿐이다(케이스 · 시술 holder 0).
- **셈 — 고민 수**(코디 셈과 대조): 코디는 **고민 자신의 행**(`concern_code` = 물은 고민)으로 세어 「적응 있는 고민 243 · 직접 시술 0 = 43 → 규칙으로 41(패키지 항목 8 · 계열 36)」 로 적었다. 같은 식으로 다시 세면 **적응 있는 고민은 242 · 직접 시술 0 은 43** 이고(0.7.1 — 검수 W-1: 243 은 고민 코드가 빈 63 행 묶음을 고민 하나로 센 값이다 · 아래 「빈 고민 묶음」 줄), 43 의 길 = 계열 36 · 패키지 8 · 제품 4(겹침 있음). **코디의 41 은 제품 길을 뺀 값이다 — 제품 길(DP2)까지 넣으면 43 전부**에 시술이 생긴다(지시서 H1 이 「패키지 · 메뉴 · 계열 · 제품」 으로 적어 본문은 제품을 넣었다 → 43). **도구 응답 단위**(물은 고민으로 펼친 행 — 하위 고민 행 포함)로 세면: 행이 있는 고민 **247**(0.7.0 의 248 — 같은 까닭) · 묶음 0 인 고민 **41**(§5-9 HG1 의 41 과 같은 집합) → **41 전부**에 내린 시술이 생긴다(계열 35 · 패키지 7 · 제품 3 · 제품 길을 빼면 39).
- **셈 — 규모**(0.7.1 고침 — 검수 W-1 · 이 워커 재셈과 같다): 내린 것이 하나라도 있는 고민 **142 / 247**(그 가운데 `groups` 에 없던 시술이 느는 고민 **138**) · 고민당 내린 시술 중앙 15 · **최대 107**(계열 6 — `CON-226`) · 서로 다른 내린 시술 138(= 시술 전부).
- **빈 고민 묶음은 따로다**: `g_indication` 에 `asked_concern_code` · `concern_code` 가 **둘 다 빈 행이 63** 있다(silver `indication` 의 고민 없는 적응). 0.7.0 의 243 · 248 · 143 · 139 · 「최대 130(계열 13)」 은 그 63 행을 고민 하나로 센 값이었다 — 그 묶음의 시술 코드 없는 23 행을 내리면 계열 13 · 시술 130 이다. **고민이 아니므로 고민 수 · 최대치에 넣지 않는다**(`concern_candidates` 는 `g_entry` 에 있는 고민 코드만 받는다 — §4-5 입력).
- **폭**: 묶음이 0 이던 고민만이 아니라 **묶음이 있는 고민에도** 계열 층 행이 있으면 내린다(일반 규칙) — 넓은 고민에서는 계열의 시술이 통째로 붙어 목록이 커진다. 그 폭은 **U7-1 = (a) 로 정해졌다**(_RESUME §2 11-17 — 전부 내고 `in_groups` · `unit` 표지로 앱이 가른다 · 제품 길 포함).
- **예 — `$W/_RESUME.md` §1 「수정 2 목록」 00 의 꼴**: `CON-168` 의 행은 메뉴 패키지에 닿은 것뿐이라 묶음 0 → `descended` 1 묶음(`M18`) · 시술 6(`PRC-123` ~ `PRC-128`) · `from[].path` = 패키지(메뉴) → 계열. 코디가 적은 길과 같다.
- **새는 것 0 의 재셈**: `groups` 의 `candidate_table` = `procedure_case` 3,127 · `procedure` 1,017(패키지 · 제품 · 계열 0) · 내린 코드 가운데 시술 코드가 아닌 것 0.

**CS — 고민 부위**(`concern_candidates` 의 `sites[]`)

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| CS1 | 머리에 `sites[]` 를 늘 싣는다(첫 쪽 · 없으면 `[]`): 보조 입력 ③(`concern_site`)에서 `concern_code` 가 **물은 고민**(`match` = `직접`) 또는 **그 하위 고민 — 자손 전부**(`match` = `하위`)인 묶임 행마다 한 항목 | 지시서 H2 · `$W/_RESUME.md` §1 「수정 2 목록」 6 · 「하위」 = 자손 전부는 §4-4 · §5-9 HG3-1 과 같은 뜻 |
| CS2 | 항목 = `{site_code, site_name, concern_code, csi_id, match}` — `site_code` · `concern_code` · `csi_id`(= `concern_site.id`)는 보조 ③ 값 그대로 · `site_name` = `g_entry` 의 (site, 코드) `entity_name`(HG3-2 와 같은 식 — 코드마다 이름 하나). silver `site` 표를 더 읽지 않는다 | §2-1 X7 · §5-9 HG3-2 |
| CS3 | **윗고민의 부위는 싣지 않는다.** HG1 로 윗고민 행을 물려받은 응답에서도 `sites[]` 는 **물은 고민 기준**이다(윗고민에 묶인 부위는 형제 고민의 자리일 수 있다 — §5-5 H6 과 같은 까닭). 부위 계층으로도 넓히지 않는다(O-17 그대로) | §5-5 H6 · O-17 |
| CS4 | `site` 입력 · HG3 과 **무관하다** — `sites[]` 는 `site` 로 거르지 않는다(그 고민의 부위 전부). `site` 를 건 조회의 행 표지는 0.5.2 의 `site_match[]` 그대로다. **0.7.1 — 거꾸로는 쓰인다**: `sites[]` 가 `site` 를 거를지 말지를 정한다 — **0.7.2: 물은 부위의 코드가 `sites[]` 의 `site_code` 안에 있는가**(SP1 · 0.7.1 은 「`[]` 인가」 였다) | §5-9 HG3 |
| CS5 | 순서 = `match`(`직접` 먼저) → `site_code` → `csi_id`. 한 부위가 고민 여럿에 묶였으면 항목도 여럿이다(접지 않는다 — 어느 고민의 자리인지가 `concern_code` 로 남아 앱이 행의 `concern_code` 와 잇는다) | §9 T6 |
| CS6 | **행을 바꾸지 않는다.** `sites[]` 는 머리의 목록일 뿐 `groups` · `total` · 행의 칸을 바꾸지 않는다. 부위가 없는 고민은 `[]` 다 — 허브가 다른 고민 · 이름 글자로 부위를 짐작하지 않는다 | 「실제 필드로만」 · §5-4 |

- **셈**(silver `concern_site` 95 행 · 고민 260): 자기 부위가 있는 고민 **85**(소분류 76 · 중분류 9 · 대분류 0) · 하위 고민의 부위까지 치면 **100** · 한 고민의 부위 수 최대 자기 9 · 자기 + 하위 **서로 다른 부위 18(묶임 행으로는 23 — `sites[]` 는 접지 않으므로(CS5) 항목 수 최대는 23 이다 · 0.7.1 단위 밝힘)** · 부위 코드 51 은 전부 `g_entry` 의 site 입구에 있다. **묶음 0 이던 41 고민 가운데 자기 부위가 있는 것 25** · 행 0 인 13 고민 가운데 4.
- **`_RESUME` §1 「수정 2 목록」 6 과 다른 곳 하나**: 거기에는 「턱살 등 없음」 으로 적혀 있으나 이 워커 재셈에서 `CON-168` 은 묶임이 **1 행**(`SITE-072`) 있다. 「부위 있는 것 85」 는 같다. 어느 쪽이 맞는지는 코디 확인 거리로 완료 보고에 적었다 — 규칙에는 영향이 없다. **0.7.1 — 닫혔다**: 검수 N-1 이 `CSI-0054` · `SITE-072` 로 확인했고 `$W/_RESUME.md` §1 6 도 「턱살 CON-168 은 부위 있음(SITE-072)」 으로 고쳐졌다.
- 하위 고민의 부위를 싣는다 — **U7-2 = (a) 로 정해졌다**(_RESUME §2 11-17 · 싣고 `match` 로 가른다 — 넓은 고민을 물으면 응답의 행에 하위 고민 행이 이미 들어 있어(`concern_match` = 하위 고민) 그 행의 자리가 필요하다).
- 「얼굴 밖 부위」 · 좌표 · 점 그리기는 앱 몫이다(SPEC-004) — 허브는 코드와 이름만 낸다.

**NM — 이름 맞춤 보강: 줄임 일치 — 0.8.0 에서 지웠다**

0.7 은 `resolve` 맞춤 꼴에 줄임 일치(낱말 둘 이상인 이름의 앞 낱말을 줄여 말한 꼴 — 규칙 NM1 ~ NM6 · 줄임 열쇠 2,881 · 입력 `abbr` · `matched.how` = `줄임` · `matched.full` · 덮임에 줄임 조각 포함)를 더했다. **0.8.0 에서 전부 지웠다**(_RESUME §2 11-18 D-1 「맞춤 꼴은 정확한 이름 → 코드만 · 부분 · 줄임 · 겹침 규칙 지움」 · 같은 날 「0.5 부분 일치 · 0.7 줄임은 앱이 resolve 를 관문으로 쓰느라 덧댄 것」).

| 지운 것 | 0.7.2 | 0.8.0 |
|---|---|---|
| 규칙 NM1 ~ NM6 | 줄임 열쇠를 짓고 문장 `norm` 안에서 찾는다 | 없음 — 맞춤은 §5-1 R2(정확 일치) 하나 |
| 메모리 색인 | 줄임 열쇠 → `g_entry` 행(적재 때) | 짓지 않는다(§3-1) |
| 입력 `abbr` | `on`(기본) \| `off` | 없음(§4-1 · O-32) |
| `matched.how` · `matched.full` | `부분` \| `줄임` · 그 이름의 `norm` | 없음 |
| NM4(덮임에 줄임 조각) | `covered_by` | 덮임 자체가 없다(§5-1 R7) |

- 0.7 의 규칙 글 · 셈(열쇠 2,881 · 37 문항 새 후보 0 · 검수 표본의 1.6%)은 변경 기록 0.7.0 · 0.7.1 과 이 문서의 0.7.2 판(git 이력)에 남아 있다.
- **그 구멍은 어디서 받나**: 줄여 말한 이름(`$W/_RESUME.md` §1 「수정 2 목록」 2) · 조사가 낀 말 · 어순이 바뀐 말 · 바꿔 말하기는 허브가 아니라 **부르는 쪽**이 푼다 — 상담은 목록 꼴로 받은 입구 목록(별칭 포함)에서 소넷이 뜻으로 고른다(SPEC-008 §2-2 · §7 규칙 2). `$W/research-input-space.md` §3 의 셈: 줄임 꼴 9 턴의 대상 정답 = 지금(0.7.2 맞춤 + Jev) 56% · 목록 + 소넷 100% / 후보 층 실패 39 턴 가운데 38 턴을 목록 + 소넷이 맞혔다.
- 시험 앱 B 열은 줄임 후보(`matched.how` = `줄임`)를 받는 0.7.2 옛 판에 묶인다(D-2 · 변경 기록 0.8.0).

**SP — 고민 + 부위: 거름 / 우선 표시**(`concern_candidates` 의 `site` — 0.7.1 · 기준 넓힘 0.7.2)

HG3(§5-9)은 `site` 를 주면 「부위 글자 일치 ∪ 그 부위에 묶인 고민의 행」 만 남긴다. 그런데 고민에 묶인 부위가 **하나도 없으면** 남는 것은 부위 글자가 우연히 적힌 행뿐이다 — 그런 고민의 행은 대부분 부위 칸이 비어 있어(부위가 고민 이름이나 손님 말에만 있다) 「그 고민에 하는 시술」 이 통째로 사라졌다. 0.7.1 의 사용자 결정(_RESUME §2 11-17 「① 규칙(사용자 결정)」): `concern_site` 없는 고민 + 부위 질문은 부위로 거르지 않는다 — 그 고민의 시술 전부를 내고, 그 부위의 행은 「우선 표시」 표지로 앞에.

**0.7.2 — 같은 구멍이 「부위가 있는 고민」 에도 있었다.** 고민에 묶인 부위가 있어도 **물은 부위가 그 부위가 아니면** 남는 것은 역시 글자가 우연히 적힌 행뿐이다(0.7.1 의 O-31 ① — 8,709 짝 가운데 0 행 8,444). 그리고 이 기준은 데이터 보강과 부딪혔다: 하위 고민에 묶임 한 행을 넣으면 부위가 하나도 없던 **윗고민이 통째로 거름으로 뒤집혀**, 윗고민을 다른 부위로 물은 질문이 전부에서 0 행이 된다(`$W/research-concern-site.md` §0-5 · §5-1). 사용자 결정(_RESUME §2 11-17 「규칙 변경 = 넣음」): **물은 부위가 그 고민의 부위(자기 + 하위 고민 — CS 의 `sites[]` 와 같은 집합) 안에 있을 때만 부위로 거른다(HG3). 그 밖 — 고민에 부위가 없거나, 부위가 있어도 물은 부위가 그 안에 없으면 — 거르지 않고 우선 표시(SP).** 한 고민 · 한 부위의 예외가 아니라 일반 규칙이다.

| # | 도구가 지킬 것 | 근거 |
|---|---|---|
| SP1 | **기준(0.7.2) = 물은 부위가 물은 고민의 `sites[]` 안에 있는가.** 「물은 부위」 = `site` 글자와 `entity_name` 이 **글자 그대로 같은** `g_entry` site 입구의 코드다(HG3-2 와 같은 식 — 11-16 gold 에서 이름 89 = 코드 89 · 한 이름에 코드 하나 · 재셈). 「안에 있다」 = 그 코드가 `sites[]` 항목의 `site_code` 가운데 있다(CS1 — `match` 가 `직접` 이든 `하위` 든). **있으면 거른다**(`site_applied` = `filter` — HG3 그대로) · **없으면 거르지 않는다**(`prefer`). `sites[]` 가 `[]` 인 고민(0.7.1 의 기준)은 「없다」 의 한 경우다 — 0.7.1 의 `prefer` 짝은 전부 그대로 `prefer` 다. **부위 입구에 없는 글자**는 코드가 없으므로 「없다」 → `prefer`(끌어낸 것 — 변경 기록 0.7.2). HG1 로 윗고민 행을 물려받은 응답에서도 기준은 **물은 고민**의 `sites[]` 다(CS3). 부위 계층으로 넓히지 않는다 — 상위 부위로 물으면 하위 부위의 묶임은 「안」 이 아니다(O-17 · HG3-5) | _RESUME §2 11-17 「규칙 변경 = 넣음」(「자기 + 하위」) · `$W/research-concern-site.md` §0-5 · 0.7.1 의 기준 = 「`sites[]` 가 `[]` 인가」 |
| SP2 | `prefer` 면 그 응답이 `site` 없이 냈을 **행 전부**를 낸다(`groups[]` · `modality_only[]` · `unreached[]` · `total` · `descended[]` — `site` 를 안 건 조회와 같은 행 · 같은 순서). **행을 빼지 않는다 · 더하지도 않는다**(다른 고민 · 부위 계층으로 넓히지 않는다 — 「묻지 않은 것 안 붙임」) | _RESUME §2 11-17 「① 규칙」 「그 고민의 시술 전부」 · 원칙(_RESUME §2 11-16 「폭은 빠짐없이」) |
| SP3 | **우선 표시 표지** = 행마다 계산 `site_prefer`(`true` \| `false`). `true` = **`filter` 였다면 남았을 행** — HG3-1 의 (i) 부위 글자 일치(`site_name` 또는 `case_site_name` = 그 글자) 또는 (ii) 행의 `concern_code` 가 그 부위에 묶인 고민 · 그 하위 고민. `true` 인 행에는 `site_match[]`(0.5.2 꼴 — 어느 쪽으로 맞았나 · 묶임이면 `csi_ids[]`)가 함께 붙는다. 묶음에는 `n_site_prefer`(그 묶음의 표지 행 수) · 머리에는 `counts.site_prefer{rows, groups}` | 같은 결정 「그 부위 케이스(행 부위 글자 일치)는 우선 표시 표지로」 · 칸 이름은 지시서 「칸 이름 정함」(제안 — O-30) · (ii) 는 끌어낸 것(변경 기록 0.7.1) |
| SP4 | **허브는 순서를 바꾸지 않는다.** 표지가 붙은 행 · 묶음을 앞에 두는 것은 앱이다(허브의 순서는 `gid` — §9 T6 결정론 · 쪽 넘김이 표지와 무관하게 선다) | 지시서 「앱은 그 행을 앞에 둔다」 · §4-0 |
| SP5 | **표지가 0 이어도 그대로 낸다.** `prefer` 인데 `site_prefer` = `true` 인 행이 하나도 없으면(`counts.site_prefer.rows` = 0) 「이 고민의 행 가운데 그 부위를 짚은 것은 없다」 는 뜻이다 — 허브가 고민 이름 · 다른 고민으로 부위를 짐작해 표지를 달지 않는다 | 「실제 필드로만」 · CS6 |
| SP6 | **물은 부위가 `sites[]` 안에 있는 짝은 0.7.0 과 같은 응답이다**(HG3-1 ~ HG3-6 — 거름 · `site_match[]` · 0 이면 0 + `unfiltered_rows`) + 머리 `site_applied` = `filter` · `counts.site_prefer` = `null` 두 칸만 는다. **0.7.2**: 0.7.1 의 「묶인 부위가 있는데 그 부위가 아닌 부위로 걸어 0 이 되는 것도 그대로」 는 **없어졌다** — 그 짝은 SP1 로 `prefer` 다. `filter` 인데 0 행인 짝은 실물 5 뿐이다(아래 「셈 — 남는 0」 · O-31 ④) | _RESUME §2 11-17 「규칙 변경 = 넣음」 · 지시서 「이마 꼴(HG3) 회귀 0」 |
| SP7 | 입력 `site_mode` = `filter` 면 SP 가 돌지 않는다 — 모든 짝에서 0.7.0 과 같은 응답(+ `site_applied`)이다. 기본은 `auto` 다 — 도구를 스스로 부르는 쪽(SPEC-002 의 C 열)도 같은 행을 받는다(HG2-6 과 같은 까닭) | 기존 응답의 확인 길 · 검수 v05 W-4 |
| SP8 | 도구 설명에 「`site_applied` = `prefer` 면 부위로 거르지 않은 응답이다 — `site_prefer` = `false` 인 행은 그 부위의 것이라고 말한 행이 아니다」 를 적는다(§4-5 불릿) | §5-3 S2 와 같은 꼴 · 일반화 금지의 재료 |

- **셈 — 짝 가름(0.7.2 · 이 워커 재셈)**: 고민 260 × `g_entry` 의 부위 이름 89 = **23,140 짝**(HG1 로 물려받는 행 포함 — 260 고민 전부 낼 행이 있다). **`filter` = 191 짝**(물은 부위가 `sites[]` 안 — 자기 묶임 95(= `concern_site` 95 행) · 하위 고민의 묶임뿐인 짝 96 · 고민 100) · **`prefer` = 22,949 짝**(= `sites[]` 가 `[]` 인 160 고민의 14,240 짝 + `sites[]` 가 있는 100 고민의 「밖 부위」 8,709 짝). 0.7.1 은 `filter` 8,900 · `prefer` 14,240 이었다 — **바뀌는 것은 8,709 짝**이고 `prefer` → `filter` 로 바뀌는 짝은 0 이다.
- **셈 — 바뀌는 8,709 짝**: 0.7.1 에서 **0 행이던 8,444 짝 → 전부 그 고민의 행**을 낸다 · 일부만 남던 245 짝 → 전부(남던 행은 표지 행으로 남는다) · 전 행이 맞아 행 집합이 같은 20 짝. 행 합 971 → 272,918. 표지가 붙는 짝 **265**(글자 일치만 241 · 묶임만 22 · 둘 다 2) · 표지 행 **971**(0.7.1 이 내던 바로 그 행 — 한 줄도 잃지 않는다 · 글자 일치 754 · 묶임으로만 217).
- **셈 — `prefer` 전체의 표지**: 22,949 짝 가운데 표지 있는 짝 **497**(0.7.1 의 232 + 265) · 표지 행 **1,617**(646 + 971). 나머지 22,452 짝은 표지 0 이다(SP5).
- **셈 — 0 행 짝**: 0.7.0(전부 거름) 22,457 → 0.7.1 8,449 → **0.7.2 5**.
- **셈 — 「이마주름 + 볼」 꼴**(지시서 — 부위가 있는 고민을 그 부위가 아닌 부위로 · `CON-005` × `SITE-051` 이름 · `sites[]` = `SITE-014` 하나): 0.7.1 **0 행**(`unfiltered_rows` 54) → 0.7.2 **54 행 · 묶음 15** · `prefer` · **표지 0 행**(그 고민의 행에 그 부위 글자 · 묶임이 없다 — SP5). 같은 고민을 자기 부위로(`SITE-014` 이름): `filter` 54 / 54 행 · 묶음 15 그대로.
- **셈 — 회귀**: `filter` 191 짝은 행 · 순서 · `site_match[]` · `counts` 가 0.7.1(= 0.7.0)과 같다(같은 판정 함수 — 행 합 2,848 · 전 행이 맞는 짝 100). `CON-001` × `SITE-014` 이름 = 73 행 · 묶음 16(글자 일치 24 행 · 묶음 2) · `CON-001` × `SITE-051` 이름 = 11 행 · 묶음 3(`filter` — 그 부위가 하위 고민의 묶임에 있다). `sites[]` 가 `[]` 인 160 고민의 14,240 짝도 0.7.1 과 같다(`prefer` 그대로 — 아래 0.7.1 셈). 37 문항에서 바뀌는 것: **0**(답 키 명세 37 에 `site` 를 건 `concern_candidates` 호출 0 — §5-9 HG3 셈 그대로).
- **셈 — 남는 0**(SP6 · O-31 ④): `filter` 인데 0 행인 짝 **5** — 묶인 고민 자신의 행이 0 이라(`CON-206` · `CON-230`) 그 고민(물려받음) · 그 윗고민을 그 부위로 물은 짝이다(`CON-200` · `CON-206` · `CON-277` × `SITE-084` / `CON-226` · `CON-230` × `SITE-019`). 0.5.2 부터 0 이던 짝이고(T22 실물의 「그대로 0 인 3 짝」 + 물려받는 2) 결정이 「안에 있으면 거름」 이라 본문은 건드리지 않았다.
- **셈 — 부위 없는 고민(0.7.1 의 셈 — 그대로 참)**(silver `concern` 260 · `concern_site` 95 행): 자기 묶임이 있는 고민 85 · 하위 고민의 묶임까지 치면 100 → **`sites[]` 가 `[]` 인 고민 = 160**(소분류 131 · 중분류 23 · 대분류 6). 「자기 + 하위」 기준은 0.7.2 결정이 글로 못박았다 — 「자기 묶임만」 으로 보면 자기 묶임이 0 인 윗고민(예: `CON-001` — 자기 0 · 하위 13 항목)이 e2e 피드백 4 의 꼴(`CON-001` × `SITE-014` — 73 행 · 묶음 16)에서 「전부」 로 바뀐다. 160 가운데 자기 행이 있는 고민 151 · 행이 0 이라 윗고민 행을 물려받는 고민 9(HG1 의 13 가운데 — 나머지 4 는 자기 묶임이 있다: `CON-012` · `CON-136` · `CON-206` · `CON-230`).
- **셈 — 160 고민의 규모(0.7.1 의 셈 — 그대로 참)**(160 고민 × 부위 이름 89 = 14,240 짝): 0.7.0 규칙으로 **0 행인 짝 14,008** · 행이 남던 짝 232 의 행 합 646(묶음 합 353). **표지가 붙는 행 = 0.7.0 에서 남던 바로 그 646 행**이다(232 짝) — 글자 일치 417 행(224 짝 · 묶음 250) + 묶임으로만 맞는 229 행(17 짝 · 5 고민 — 윗고민이 그 부위에 묶인 고민 2(`CON-025` · `CON-190`) · 물려받은 윗고민 행 안에 그 부위에 묶인 형제 고민의 행이 있는 고민 3(`CON-250` · `CON-257` · `CON-259`)). SP3 이 표지를 글자 일치로만 달면 그 229 행(0.7.2 의 8,709 짝에서는 217 행 더)이 0.7.0 에 있던 `site_match[]` 를 잃는다 — 그래서 「`filter` 였다면 남았을 행」 으로 적었다.
- **셈 — 「볼 + 탄력 저하」 꼴**(_RESUME §2 11-17 의 실물 문장 — `CON-048` × `SITE-051` 이름 · `sites[]` = `[]`): 0.7.0 **0 행 · 묶음 0**(`unfiltered_rows` 105) → 0.7.1 · 0.7.2 **105 행 · 묶음 55** · **표지 0 행**(`site_name` 이 빈 행 103 · `case_site_name` 이 빈 행 101). 같은 낱말이 든 다른 고민 `CON-117` × 같은 부위: 0 → 3 행 · 묶음 1 · 표지 0.
- **보강 뒤 어림 ① — 추천 7 고민 8 행을 넣었다고 치면**(_RESUME §2 11-17 「concern_site 보강 판정 = 추천」 — 95 → 103 행 · 반영은 구현 뒤 · 이 워커가 보조 ③ 에 8 행을 더해 같은 스크립트로 센 값): `sites[]` 가 있는 고민 100 → **106** · `filter` 191 → **200 짝** · `prefer` 22,940 짝 · 0 행 짝 **5 그대로**(0.7.1 규칙이었다면 8,449 → 8,974 로 는다). **「흉터 + 볼」(`CON-140` × `SITE-051` 이름) = 113 행 · 묶음 40 그대로**다 — 추천 8 행에는 그 고민 · 하위 고민의 행이 없어 `sites[]` 가 `[]` 그대로다(두 규칙 모두 113). 새로 묶이는 고민의 꼴: `CON-193` × `SITE-103` 이름 → `filter` 6 / 6 행 · 묶음 4 · 같은 고민 × `SITE-110` 이름(밖 부위) → 0.7.1 규칙이면 **0** · 0.7.2 **6 행**(`prefer`).
- **보강 뒤 어림 ② — 윗고민을 뒤집던 행까지 넣는다면**(가정 — 조사 §4-1 · §4-2 가운데 결정이 뺀 4 고민 5 행: `CON-156` 2 · `CON-133` · `CON-269` · `CON-122` · 108 행): `sites[]` 가 있는 고민 114 · `filter` 210 짝. **`CON-140` × `SITE-051` 이름: 0.7.1 규칙이면 0 행 → 0.7.2 113 행 · 묶음 40**(`prefer` — 하위 고민의 묶임 `SITE-110` · `SITE-103` 이 `sites[]` 에 실리지만 물은 부위는 그 안에 없다) · 같은 고민 × `SITE-110` 이름 → `filter` 13 행 · 묶음 5 · `CON-128` × `SITE-051` 이름 40 행 · `CON-115` × `SITE-051` 이름 65 행(둘 다 0.7.1 규칙이면 0). 0 행 짝은 0.7.1 규칙이면 9,665 · 0.7.2 5. **즉 0.7.2 에서는 하위 고민에 묶임을 더해도 윗고민의 「다른 부위」 질문이 행을 잃지 않는다** — 보강이 규칙을 건드리지 않는다(보조 ③ 이 바뀌므로 `aux_hash` 만 바뀐다).
- 0.7.1 이 적은 보강 후보 10 의 상태: 8 이 지금 `sites[]` = `[]`(`CON-025` · `122` · `156` · `162` · `166` · `190` · `209` · `260`) · 2(`CON-200` · `CON-277`)는 묶임이 있다(하위 고민의 묶임). 판정은 `$W/research-concern-site.md` §6 · _RESUME §2 11-17 로 닫혔다(7 고민 8 행).

**두 판(CSV · DB)** — 넷(DP · CS · NM · SP) 다 새 입력이 없다. DB 판은 같은 `LoadedInputs` 로 같은 `GoldMemory` 색인을 세우므로(SPEC-003 §5 P2) 줄임 열쇠 색인도 같은 코드가 짓는다 · 도구 응답 동치 시험(SPEC-003 §7 DT10)이 0.7 필드까지 덮는다(T27). repository Protocol 에 메서드가 늘면(줄임 열쇠 찾기 · 고민의 묶임 `id`) SPEC-003 §5 P1 의 「메서드 29」 는 WORK 에서 수를 고친다 — SPEC-003 본문은 이 판에서 고치지 않았다(이번 allowed_paths 밖). **0.8.0** — NM 을 지워 줄임 열쇠 색인과 그 repository 메서드(`abbr_keys` · `entries_by_abbr`)는 두 판에서 함께 없어진다. 남는 것은 셋(DP · CS · SP)이다.

## 6. 근거 추적

```
도구 응답 행(gold_table · gid · evidence_kind)
  → evidence(gold_table, gid)
      → refs[]: g_evidence(silver_table · silver_id · fields · evidence_kind)
          → source_refs[]: source_ref(field · ref)      ← 원장 「파일:포인터」 · 외부 확인 URL · 판정 표 줄
```

| 추적성 구성(`artifact-traceability.md`) | 허브에서 |
|---|---|
| 공통 식별자 | `gid` · `node_id` · `edge_id` |
| 관계 | `g_evidence` · `g_scope.link` · `g_edge.gold_table` + `gold_id` |
| 버전 | `build.gold_hash`(모든 응답 머리) |

- **모든 응답 행이 `evidence` 한 번으로 원장 포인터까지 간다**(`g_edge` 행은 `gold_table` + `gold_id` 를 거쳐 한 번 더). 11-16 gold 에서 근거 없는 행 0 · 짝 없는 참조 0(조사 §1-4).
- `evidence_kind` 는 행에 늘 실려 있으므로 앱은 `evidence` 를 부르지 않고도 「원장 / 외부 확인」 을 구분한다(semantic-map §4).
- `source_ref` 를 올리지 않으면 관계가 silver 행에서 끊긴다 — 그래서 D3 = 적재(조사 §0 D3).

## 7. 옛 PR #31 에서 가져갈 틀 / 버릴 것(조사 §3-3)

경로는 `HUB-OLD/backend/` 아래 · 커밋 `2edc190`. **파일을 복사하지 않는다** — 틀(구조 · 패턴)만 새로 쓴다.

| 배관 | 판정 | 옛 파일 | 새 gold 에서 |
|---|---|---|---|
| 서버 골격(FastAPI · lifespan · MCP 마운트 · server-timing) | 틀만 | `app/graph_main.py:29-82` | lifespan 에서 CSV 적재(DB 연결 없음) · `streamable_http_app(stateless_http=True, json_response=True)` 한 번(`:30`) · 진입점을 따로 둘지는 O-7 |
| MCP 서버 틀(`_call` · READ_ONLY · meta) | 틀만 | `app/modules/gold/mcp_server.py:22-30 · 55-59` | 도구 정의 문구 · 입력은 §4 로 새로 |
| REST 라우터 · DI | 틀만 | `app/router/gold.py` · `app/modules/gold/container.py:14-18` · `service.py` | Singleton 상태 + Factory 서비스 · 한 코어 두 입구 |
| 적재 · 해시 | 틀만 | `app/modules/gold/inputs.py:16-63` | 입력 목록 = CSV 15 + `source_ref` + 보조 입력 4 파일 · 해시 식 = §2-3(옛 sha16 아님) |
| 메모리 색인 | 틀만 | `app/modules/gold/memory.py:13-60` | §3-1 색인으로 새로 |
| resolve 조사 목록 | 목록만 | `app/modules/gold/resolve.py:19` | §5-1 R3 |
| 설정 | 틀만 | `app/modules/gold/config.py:15-24` | §2-2 env · 옛 손잡이(`:27-60`)는 전부 버림 |
| 시험 틀(실물 경로 env · 없으면 skip) | 틀만 | `tests/gold_support.py:17-27` | §9 |
| 의존 | 그대로 | `pyproject.toml` 의 `mcp>=2.3,<3` · `httpx`(조사 §2-1) | `release/v1.2.0` 에 `mcp` 없음 — 더해야 함 |
| 빌드(G1~G22 · 가드) | **버림** | `app/modules/gold/build.py` · `pairs.py` · `facts.py` · `ids.py` | 허브는 적재만 |
| 봉투(envelope · claude_contract · companion · intent · sections · must_show_flags) | **버림** | `app/modules/gold/tools.py:225` 등 | 응답 머리는 §4-0 |
| DB 스키마 · alembic · 발행 테이블 | **버림(이번)** | `app/model/gold.py:23-156` · `b202610300001_gold_schema.py` | DB 없음(D2) |
| 옛 도구 11 + 미커밋 2 | **버림** | `mcp_server.py` · `router/gold.py` · `selected.py`(미추적) | §4 의 8 |
| 옛 시험 38 파일 · 스크립트(`gold_build` · `gold_quality_eval` · `gold_e2e` · `gold_speed` …) | **버림** | `tests/test_gold_*.py` · `scripts/gold_*.py` | 옛 데이터 기대값 |
| 원장 MCP(`raw_list` · `raw_get` · `raw_search`) | **이 스펙 범위 밖** | `app/modules/raw/` | A 열의 원장 도구는 **앱 로컬 stdio MCP** 다(_RESUME §2 11-16 「검수 뒤 결정 4」 ④ · SPEC-002 §2-3). 허브에 원장을 싣지 않는다 |

옛 워크트리의 미커밋 수정 8 · 미추적 2 는 손대지 않는다(`$W/_RESUME.md` §1).

## 8. stg

| 항목 | 정해진 것 | 근거 |
|---|---|---|
| 경로 | `feat/*` → `release/v1.2.0` → `stg` PR 병합 → Azure 자동 배포 | _RESUME §2 11-16 「stg」 · `deployment.md:9-12 · 93-95 · 100` |
| Backend CD | `stg` push 중 `backend/**` 변경에 반응 · GitHub Actions → 이미지 → VM 컨테이너 교체 | `deployment.md:93-95 · 108` |
| 승인 | **머지 · 배포 · stg 데이터 반입은 각각 별도 승인** | _RESUME §2 11-16 「stg」 |
| 데이터 gate | BE 배포가 끝나도 데이터 반입은 별도 gate | `deployment.md:40-41` |
| 이번 판 | **로컬 시험까지.** 브랜치를 올리거나 PR 을 열지 않는다 | 브리프 §3 · _RESUME §2 11-16 「발주 전 승인」 |

stg 로 가려면 닫아야 하는 것(전부 열린 것):

- **stg 데이터 반입 방법**(O-8) — CSV 는 레포에 못 넣는다(§2-1). 컨테이너가 어디서 읽을지 정해지지 않았다. 보조 입력 4 파일도 같이 가야 한다(원장 확인 목록은 글 칸이 든 원본 대신 id · 코드만 뽑은 것을 보낼지도 O-8).
- **진입점**(O-7) — stg 이미지는 `app.main:app` 하나를 띄우고 그 앞에 DB migration 을 돌린다(`release/v1.2.0` 의 `backend/Dockerfile:27`). 옛 틀처럼 별도 ASGI 진입점이면 stg 에서 뜨지 않는다.
- **접근 제어**(O-11) — 다른 서비스가 부를 때의 인증은 확인하지 않았다.
- 호스트 · 주소는 이 문서에 적지 않는다(「stg Gateway」 로만).

**0.8.2 — stg 에 올라갔다**(2026-11-18 · 허브 `d3d078c`). 위 「닫아야 하는 것」 의 진입점 · 반입 방법은 SPEC-003 §11(0.2.x — gold 를 `app.main` 에 붙임 · 레포 `data/medallion/` · 일회성 적재)이 정본이다. 이 문서에 남는 것은 오류 표의 `unavailable`(§4-0) · 설정 셋(§2-2 `GOLD_MCP_ALLOWED_HOSTS` · `GOLD_MCP_ALLOWED_ORIGINS` · `GOLD_LOAD_TIMEOUT_SECONDS`)이다.

## 9. 시험(허브 단위)

| # | 시험 | 기대 | 데이터 |
|---|---|---|---|
| T1 | 적재 | 15표 + `source_ref` + 보조 입력 4 파일의 행 수 = 파일 행 수 · gold 해시 = `gold-check.py` 식 값 · 보조 입력을 읽어도 gold 해시가 같다 · `health.files[]` 의 `gold` + `hash_only` 16 줄로 다시 센 값 = `gold_hash` | 실물 |
| T2 | 적재 실패 | env 없음 · 파일 없음 · 헤더 다름 · 보조 입력의 쓸 칸 없음 · 기대 해시 다름 → 시작 실패 | 합성 |
| T3 | 헤더 계약 | 도구 9 의 행 필드 ⊂ CSV 헤더 ∪ 「계산」 필드(부록 A 를 기계로 대조 — 보조 입력 칸도 실제 silver · 원장 확인 목록 헤더와) | 실물 · 합성 |
| T4 | 37문항 되짚기 | 문항마다 `gold_pointers` 의 `gid` 가 그 범위의 도구 길(§5-2)로 **전부 나온다**. `gold_pointers` 는 gold-build 가 앞에서 잘라 낸 **표본**이다(문항당 최대 9 — 검수 F-1) — 이 시험은 「표본 ⊂ 도구 길의 전체 행」 을 보는 것이고, 전체 행이 답 키다(SPEC-002 §9-5) | 실물 |
| T5 | 근거 | T4 의 모든 `gid` 에 `evidence` → 참조 1 이상 · `source_ref` 1 이상 | 실물 |
| T6 | 결정론 | 같은 입력 두 번 → 같은 응답(순서 포함) · cursor 로 끝까지 넘긴 **쪽 단위의 합** = `total`(단위는 §4-0 표 — `concern_candidates` 는 묶음 · `evidence` 는 편 줄) · 쪽 밖 목록은 첫 쪽에만 | 실물 |
| T7 | REST = MCP | 같은 입력에 두 입구의 JSON 이 같다 | 합성 |
| T8 | 범위별 규칙 | §5-3 S2 · S4 · §5-4 V1 · V2 가 응답에 그대로(빈칸 유지 · 충돌 행 둘 다 · 상위 제품 기본 제외) | 실물 |
| T9 | 계층 펼침 | §4-4 의 세 자리에서 `hier` = `expand` 면 상위 · 하위(**자손 전부** — 손자 코드의 행까지) 행이 `hier.match` 와 함께 나오고 `exact` 면 정확 일치 행만 · Q17 은 `exact` 0 행 · `expand` 4 행 · 다른 facet 은 `hier` 와 무관 | 실물 · 합성 |
| T10 | 원장 확인 | `ledger_check[]` 가 세 도구에 늘 있고(없으면 `[]`) · Q10 의 고민 코드 → `LCK-010` · Q33 의 `offer_id` → `LCK-308`(`on` = `rows`) · 글 칸이 응답에 없음 · 항목 순서 = `on` → `code`(§4-0) · 같은 코드가 `request` 와 `rows` 양쪽이면 항목 둘 | 실물 · 합성 |
| T11 | 「있음」 경계 | `g_entry` 에 있고 행 0 인 값 → `200` · `total: 0` / `g_entry` 에 없는 값 → `not_found` | 실물 · 합성 |
| T12 | 속성 쪽 시작 | 속성 4표의 코드마다 §4-4 표의 facet 을 전부 불러 — 나온 행 = 그 칸에 그 이름(항목)이 있는 행 **전부**(직접 센 수와 `total` 이 같다) · 행마다 `attr.column` · 「—」 조합은 `invalid_argument` · 맞는 행 없는 코드는 `200` · `total: 0` · `(항목)` 칸에서 부분 문자열만 같은 값은 안 나온다 | 실물 · 합성 |
| T13 | 입구 목록 | `resolve` 목록 꼴 — `range` 마다 끝까지 넘긴 행 수 = 그 표들의 `g_entry` 행 수 · `counts.entities` = §5-2 아래 셈 · 순서 결정론 · `text` 도 `range` · `tables` 도 없으면 `invalid_argument` | 실물 |
| T14 | 상품 이름 부분 일치 | `offer_name_contains` — `norm` 부분 일치 행 전부 · `node` 와 함께 주면 `invalid_argument` · 다른 facet 이면 `invalid_argument` · 맞는 것 없으면 `200` · `total: 0` · Q33 의 표본 `gid` 가 이 길로 나온다 | 실물 · 합성 |
| T15 | 정확한 이름(0.8.0 — 0.5.0 의 「넓은 후보」 를 바꿨다) | `resolve` 맞춤 꼴 — 후보 = `g_entry.norm` 이 입력의 `norm` 과 **같은** 행의 개념 전부(서로 다른 `norm` 2,541 마다 직접 센 것과 같다) · 띄어쓰기 · 대소문자를 바꿔도 같은 후보(R1) · 별칭 글자를 그대로 넣어도 그 개념이 나온다 · **이름이 든 문장 · 조사가 붙은 이름 · 이름의 앞이나 뒤 일부 · 두 이름을 이어 쓴 글 → 후보 0**(`200` · 빈 목록) · 같은 `norm` 에 개념이 여럿이면 전부 + `ambiguous` = 참(겹치는 `norm` 99) · 순서 = 표 순서 → 「이름」 먼저 → `gid`(`range` 를 주면 `in_range` 가 앞) · `matched` 의 키 = `span` 하나(`start` · `covered_by` · `how` · `full` · `particle` 없음) · 입력 `abbr` → `invalid_argument` | 합성 · 실물 |
| T16 | 정보 종류 셈(0.5.0) | `coverage` — 노드마다 종류별 `self` · `lower` · `inherited` 가 §5-8 표의 조회를 그 role 로 실제로 불러 센 서로 다른 `gid` 수와 같다(대상 4표 전 노드 × 14 종류) · 「—」 인 종류는 실리지 않는다 · `nodes` 순서 그대로 · 없는 노드가 하나라도 있으면 `not_found` · 상한을 넘으면 `invalid_argument` · §4-9 끝 줄의 셈(적응: 시술 33 · 제품 3 · 계열 1 …)이 다시 나온다 · **`overview` · `mechanism` 은 그 종류의 칸에 값이 있는 행만 세어진다**(원리 칸이 빈 자기 profile 행뿐인 제품은 `mechanism.self` = 0 — 0.5.1) | 실물 · 합성 |
| T17 | 제품 상품 role(되적기) | 제품 노드의 `facets` offer 를 `roles` 없이 부르면 행이 그 제품 · 하위 제품의 것뿐이다(`layer.role` ∈ `자기` · `하위 제품`) · 다른 대상의 기본 role 은 `자기` · `물려받음` 그대로 · `counts.distinct_rows` = 서로 다른 `gid` 수 | 실물 · 합성 |
| T18 | `b` 없는 패키지(되적기) | `pair(a, package_kinds)` — `a` 쪽 집합과 항목이 겹치는 패키지가 `same_day_packages[]` 로 전부 나온다 · `b` 를 주면 양쪽과 다 겹치는 것만 | 합성 |
| T19 | 하위 층 자기 행(0.5.0) | `facets` 에 「하위 *」 role 을 주면 그 holder 의 자기 행이 `layer.role` = 그 role 로 나온다 · 기본값으로 부르면 안 나온다(S2) · 「상위 제품」 은 명시해야만 나온다(S4) · **MCP 도구 설명에 「하위 층의 자기 행은 `roles` 에 하위 role 을 줘야 나온다」 문장이 있다**(§4-4 — 0.5.1) | 실물 |

| T20 | 윗고민 물려받음(0.5.2 — HG1) | 행이 0 인 고민마다 `concern_candidates` → 가장 가까운(행이 있는) 윗고민을 직접 물은 것과 **같은 `gid` 집합** · 머리 `inherited_from{concern_code, steps}` · 전 행에 `hier.match` = `상위` · 행의 `asked_concern_code` 는 gold 값 그대로 · `ledger_check[]` 는 요청 코드의 것 · **자기 행이 1 이상인 고민은 바뀌지 않는다**(`inherited_from: null` — 묶음만 0 인 고민 포함 · U-3 을 달리 정하면 이 줄을 고친다) · 두 단 위까지 있는 고민은 가까운 쪽에서 멈춘다 · `upper` = `none` 이면 `total` 0 · `coverage` 의 고민 `indication.inherited` = 그 조회의 행 수 · 실물 셈: 행 0 인 고민 13 · 전부 `steps` = 1 | 실물 · 합성 |
| T21 | 하위 = 자손 전부(0.5.2 — HG2) | `scope` · `facets`(「하위 *」 role) · `pair` · `coverage` 가 **같은 닫힘**을 쓴다: 계열의 `scope` 에 그 하위 시술 아래 케이스가 `depth` 2 로 전부 나온다(실물 — 계열 18 · 케이스 합 268 · 계열별 수 §5-9) · 계열의 `facets` adverse 에 케이스 행이 `layer.role` = `하위 케이스` · `layer.depth` 2 · `layer.via[]` = 그 시술로 나온다 · 계열 끝 `pair` 에 케이스 끝 관계가 나온다 · `coverage.lower` = 같은 조회를 끝까지 넘겨 센 수(T16 그대로) · **`자기` · `물려받음` 으로 닿은 holder 에서는 내려가지 않는다**(제품 조회에 형제 제품 행이 없다) · 한 holder 는 한 번(가장 얕은 `depth`) · `descend` = `one` 이면 0.5.1 과 같은 응답 · 순환 합성 fixture 에서 끝난다 · Q12 의 표본 4 가 계열 대상 조회만으로 전부 나온다 | 실물 · 합성 |
| T22 | 고민 + 부위(0.5.2 — HG3) | `concern_candidates(concern_code, site)` — 낸 행 = 「글자 일치 ∪ 묶인 고민 · 그 하위 고민의 행」 을 직접 센 것과 같다 · 행마다 `site_match[]`(`concern_site` 면 `csi_ids[]`) · `counts.by_site_match` · 묶인 고민 **자신**을 그 부위로 걸어도 0 이 되지 않는다 · 묶임 없는 (고민, 부위) 는 0.5.1 과 같다(0 이면 0 + `unfiltered_rows` — **0.7.2: `site_mode` = `filter` 일 때**. 기본 `auto` 에서는 물은 부위가 그 고민의 `sites[]` 안에 없는 짝이 전부 `prefer` 다 — T28 · 0.7.1 은 「부위가 묶인 고민에서 · 또는 `filter` 일 때」 였다) · 부위 입구에 없는 글자는 글자 일치만(0.7.2: `site_mode` = `filter` 일 때 · `auto` 면 `prefer` 에 글자 일치 표지) · 실물 셈: (윗고민, 부위) 97 짝 가운데 글자 일치 0 인 40 짝이 1 이상 · `CON-001` × `SITE-014` = 73 행 · 묶음 16 · 보조 입력 ③ 을 읽어도 gold 해시가 같다 | 실물 · 합성 |
| T23 | 되적기(0.5.2) | ~~`matched.covered_by` — 같은 조각이 두 번 나오고 한 번만 긴 조각 안에 들면 `null`~~(0.8.0 — 필드가 없어졌다) · 제품 노드 `coverage` 의 `offer.inherited` = `0`(`null` 아님) · `health.integrity.scope_duplicate_subject_holder_rows` 가 있다 · `coverage` 상품 셈이 §4-4 맞춤 규칙의 수(자기 0 · 하위 1 이상: 계열 17 · 시술 0 · 제품 7 — HG2 앞의 수 · HG2 뒤는 다시 센다) | 실물 · 합성 |

| T24 | 시술로 내려가기(0.7 — DP) | 고민 260 전부에 `concern_candidates` — `descended[]` 의 시술 집합 = 그 응답의 `modality_only[]` · `unreached[]` 행을 DP2 로 직접 따라가 센 것과 같다 · **`procedures[].procedure_code` 는 전부 `g_scope` 의 procedure holder**(패키지 · 메뉴 · 제품 · 계열 코드 0) · `groups[].candidate_table` ∈ {`procedure`, `procedure_case`} · 묶음 0 이던 41 고민 전부에 내린 시술 ≥ 1 · `counts.descended.undescended` 합 0 · `CON-168` → 계열 1 · 시술 6 · `path[]` 의 `scope_gid` 가 전부 실재하는 `g_scope` 행이고 그 role 이 DP2 의 role · `from[].gid` ⊂ 그 응답의 `modality_only[]` ∪ `unreached[]` · `in_groups` = `groups` 전체와 대조 · `to_procedure` = `none` 이면 `descended` · `counts.descended` **두 필드가 없다** · 못 내리는 행은 합성으로 · **0.7.1**: `lands` = `procedure` 합성 — 그 행이 **닿은 시술의 계열 묶음**에 들어가고 그 묶음의 `procedures[]` 는 계열의 시술 전부 · `from[].procedure_codes[]` = 닿은 시술만 · `unit` = `계열` · 계열이 없는 시술에 닿으면 `undescended`(「`descended[]` 의 시술 집합 = 직접 따라가 센 것」 은 `lands` = `modality` 행 기준이고, `procedure` 행은 `procedure_codes[]` 로 대조한다) · 실물 셈: 내린 것이 있는 고민 142 · 최대 107(`CON-226` · 계열 6) · **MCP 도구 설명에 「묶음은 계열 단위 — 시술 하나하나의 적응이 아니다」 문장이 있다**(§4-5) | 실물 · 합성 |
| T25 | 고민 부위(0.7 — CS) | `sites[]` = 보조 ③ 에서 물은 고민 · 그 자손 고민의 묶임 행을 직접 센 것과 같다(고민 260 전부 — 자기 85 · 자기 + 하위 100) · `match` · 순서(CS5) · `site_name` = `g_entry` 이름 · 부위 없는 고민은 `[]` · HG1 로 물려받은 응답(13 고민)에서도 물은 고민 기준 · `site` 를 걸어도 `sites[]` 는 같다 | 실물 · 합성 |
| T26 | ~~줄임 일치(0.7 — NM)~~ | **0.8.0 에서 지웠다** — NM 이 없다. 남는 확인(T15 와 함께): 낱말 둘 이름의 앞 낱말을 줄인 글(띄어 쓴 꼴 · 붙여 쓴 꼴) → **후보 0** · 응답 어디에도 `matched.how` · `matched.full` 이 없다 · 적재 뒤 메모리에 줄임 열쇠 색인이 없다 | 합성 |
| T27 | 기존 필드 불변 · 두 판(0.7) | 0.6 의 응답 기대(T1 ~ T23 · 답 키 37 명세의 호출)가 **그대로 통과**한다 — **단 맞춤 꼴에 문장을 넣던 기대는 뺀다**(0.8.1 — **T3** 의 실물 응답 검사 `test_T3_real_response_fields` 는 입력을 `entry_text` · 이름으로 바꾸고, 그 밖에 고칠 · 지울 시험 파일 · 함수는 변경 기록 0.8.1 「고칠 · 지울 허브 시험」 표) · `concern_candidates` 는 `site` 를 안 걸었을 때 새 필드(`descended` · `sites` · `counts.descended` · `counts.sites` · 0.7.1 의 `site_applied` · `counts.site_prefer`)와 `request.to_procedure` · `request.site_mode` 를 빼면 0.6 과 같은 JSON · `site` 를 걸었을 때는 `site_mode` = `filter` 로 같다(기본 `auto` 에서 달라지는 것은 물은 부위가 그 고민의 `sites[]` 안에 없는 짝뿐 — 0.7.2 · T28) · ~~`resolve` 는 `abbr` = `off` 일 때 `matched.how` 를 빼면 같은 JSON~~(0.8.0 — `resolve` 맞춤 꼴은 0.6 과 같은 응답이 아니다 · T15 · T29 가 본다) · `gold_hash` · `aux_hash` 가 0.6 과 같다(새 입력 0) · CSV 판 = DB 판(SPEC-003 §7 DT10 을 0.7 필드까지) · REST = MCP(T7) · 결정론(T6 — `descended[]` · `sites[]` 순서 포함) | 실물 · 합성 |
| T28 | 고민 + 부위: 거름 / 우선 표시(0.7.1 SP · 기준 0.7.2) | 고민 260 × 부위 이름 89(23,140 짝)에 `concern_candidates(concern_code, site)` — **기준**: `site_applied` = `filter` ⇔ 물은 부위의 코드가 그 응답 `sites[]` 의 `site_code` 안에 있다(직접 센 것과 같다 · `filter` **191** 짝 · `prefer` **22,949** 짝) · **`prefer` 짝**: 행 · 묶음 · 순서 · `total` · `descended[]` 가 `site` 를 안 건 조회와 같다 · 전 행에 `site_prefer` · `true` 인 행 집합 = 같은 조회를 `site_mode` = `filter` 로 불러 나온 행 집합(그 행의 `site_match[]` 도 같다) · `n_site_prefer` · `counts.site_prefer` = 직접 센 수 · 표지 0 인 짝도 `200` · 행 전부 · **`filter` 짝**: 0.7.0 과 같은 응답(`site_prefer` 필드 없음 · `CON-001` × `SITE-014` 이름 = 73 행 · 묶음 16) · `site` 가 없으면 `site_applied` = `null` · `site_mode` = `filter` 면 모든 짝이 걸러진다(0 이면 0 + `unfiltered_rows`) · 물려받은 응답(행 0 인 고민 13)은 **물은 고민의 `sites[]`** 기준이다(부위 없는 9 는 전 짝 `prefer` · 부위 있는 4 는 자기 부위로 물을 때만 `filter`) + `inherited_from` 그대로 · 부위 입구에 없는 글자 → `prefer` · 실물 셈: `sites[]` 가 `[]` 인 160 고민의 14,240 짝 전부 `prefer`(`filter` 로 0 행인 짝 14,008 포함 · 표지 행 합 646 · 232 짝) · **`sites[]` 가 있는 100 고민의 밖 부위 8,709 짝 전부 `prefer`**(`filter` 로 0 행인 짝 8,444 포함 · 표지 행 합 971 · 265 짝) · `CON-048` × `SITE-051` 이름 = 105 행 · 묶음 55 · 표지 0 · **`CON-005` × `SITE-051` 이름 = 54 행 · 묶음 15 · 표지 0**(같은 조회를 `site_mode` = `filter` 로 → 0 행 · `unfiltered_rows` 54) · `auto` 에서 0 행인 짝은 5 뿐(전부 `filter` — §5-11 「셈 — 남는 0」) · **MCP 도구 설명에 「`prefer` 면 거르지 않은 응답 — 표지 없는 행은 그 부위의 것이 아니다」 문장이 있다** · 합성: 묶임 없는 고민에 부위 글자가 적힌 행 둘 · 안 적힌 행 둘 → 넷 다 나오고 표지 둘 · **묶임 있는 고민을 그 고민의 부위가 아닌 부위로 → `prefer` · 행 전부 / 같은 고민을 자기 부위 · 하위 고민의 부위로 → `filter`** | 실물 · 합성 |
| T29 | 목록 꼴 불변 · 도구 설명(0.8.0) | `resolve` 목록 꼴 — `candidates[]` · 순서 · `total` · `counts{by_table, entities}` · 쪽 넘김이 0.7.2 와 같다(T13 그대로 통과) · 머리 `request` 에 `abbr` 칸이 없다 · 상담이 쓰는 다섯 표(`concern` · `site` · `modality` · `procedure` · `product`)를 끝까지 넘긴 개념 수 = **820**(고민 260 · 부위 89 · 계열 18 · 시술 138 · 제품 315 — `$W/research-input-space.md` §3 의 셈 · 데이터 판이 바뀌면 다시 센다) · REST = MCP(T7) · CSV 판 = DB 판(SPEC-003 §7 DT10) · 결정론(T6) · **MCP 도구 설명에 「`text` 는 이름 하나다 — 문장을 넣으면 후보가 0 이다 · 문장에서 입구를 찾으려면 목록 꼴로 받아 고른다」 문장이 있고 부분 일치 · 덮임 · 줄임 문장이 없다** · 다른 도구 8 의 응답이 0.7.2 와 같다(T1 ~ T14 · T16 ~ T25 · T28 그대로 통과) | 실물 · 합성 |

- **실물 데이터 시험은 `GOLD_CSV_DIR`(과 보조 입력 env)이 없으면 skip**(옛 틀 `tests/gold_support.py:25-27`). CI 에는 데이터가 없다.
- T4 의 `gold_pointers` 는 시험이 로컬 `questions.csv` 에서 읽는다 — 문항 · 답은 코드 레포에 넣지 않는다.
- 문항별 기대(질문 문장 없이):

| 범위 | 문항 | 도구 길 | 따로 볼 것 |
|---|---|---|---|
| 시술 | Q01~Q05 | `resolve` → `facets` profile · indication · outcome | Q04 — 상위 제품 진술이 하위 제품에 안 붙음(S4 — 0.5.0 에서도 그대로 · 거꾸로 하위 제품의 자기 행은 「하위 *」 role 을 주면 상위 제품 조회에 층 표시와 함께 나온다 · S5) |
| 부위·고민 | Q06~Q10 | `resolve` → `concern_candidates` | Q10 — **0.5.2(HG1)**: 자기 행 0 → 바로 위 윗고민의 묶음이 `inherited_from` · `hier.match` = `상위` 와 함께 나온다(`upper` = `none` 이면 0.5.1 처럼 `200` · `total` 0) · 값은 `g_entry` 에 있음(`not_found` 아님) · `ledger_check[]` 에 `LCK-010` 그대로(`gold_pointers` 빈칸 · 상태 「원장 확인」) |
| 부작용 | Q11~Q14 · Q35 | `scope` → `facets` adverse · adverse_detail · recovery | Q12 — **0.5.2: 대상 = 계열**(_RESUME §2 11-17 「답 키 검토」) · 「하위 *」 를 주면 케이스 행까지 나온다(HG2 — 표본 4 전부) · 행은 있고 `onset_text` · `duration_text` 가 빈칸(상태 「silver 빈칸」 — 빈칸 그대로 낸다) · Q35 — 회복과 부작용 지속이 다른 facet |
| 시술 조합 | Q15~Q18 · Q37 | `pair`(보완) · `facets` package | Q17 — 고민 상위 펼침으로 행이 나온다(`hier` = `expand` 4 행 · `exact` 0 행 — §4-4) |
| 동시 가능 | Q19~Q22 · Q36 | `pair`(전 갈래 · 패키지) | Q21 — `same_day` 채운 행 0(빈칸 유지) · Q19 — 충돌 행 둘 다 |
| 순서·간격 | Q23~Q26 | `pair`(순서 · 간격 · 재시술 간격) | Q24 · Q26 — `self_pair` |
| 회피 | Q27~Q30 | `pair`(회피) · `facets` contraindication | Q29 — 금기 행 전부(쪽 넘겨 끝까지) |
| 상품 | Q31~Q34 | `facets` offer | Q33 — `facets` offer 의 `offer_name_contains` 로 들어간다(§4-4 「상품 이름 부분 일치」 — 0.5.2: 답 키는 그 상품을 입구(값 쪽 `node` = offer)로 둔다 · `app-key-fix1-report.md` K4 · 두 길의 행이 같다) · 행 1 · `reach` 「못 닿음」 · `ledger_check[]` 에 `LCK-308`(`on` = `rows`) |

- 합성 fixture 는 가짜 코드 · 가짜 이름으로 만든 작은 CSV 15 + `source_ref` + 보조 입력 4 파일이다. **회사 데이터 본문을 fixture 에 넣지 않는다.**
- 속도 · 품질 측정은 이 스펙에 없다(SPEC-002).

## 10. 열린 것

「추천」 은 이 워커의 추천이고 결정이 아니다. **「결정됨」 으로 적힌 줄은 더 이상 열린 것이 아니다** — 어디로 옮겼는지만 남긴다.

**「상태」 칸** — 남은 것이 누구 · 언제의 몫인지 가른다.

| 상태 | 뜻 |
|---|---|
| 결정됨 | 사용자 결정이 났고 본문에 들어갔다 |
| 승인됨 | 사용자가 「본문 제안 그대로 시작」 을 승인했다(재검수2 §5 B · _RESUME §2 11-16 「재검수 2(r3) §5 결정」(§5 B = 승인)). 값은 구현 · 1회차에서 고칠 수 있다 |
| 1회차 trace 뒤 | 본문 값으로 1회차를 돌리고 그 기록을 본 뒤 정한다 |
| 구현 때 정함 | 이름 · 꼴 · 값처럼 WORK · 구현에서 정해도 계약의 뜻이 안 바뀐다. 본문 제안으로 시작한다 |
| 뒤 단계에서 사용자 확인 | **WORK 를 시작하는 데는 필요 없다.** 적힌 때(stg 반입 승인 · 배포 승인)에 사용자에게 묻는다 — 이번 판은 로컬 시험까지다(§8) |

**0.5.2 — 사용자가 정할 것(허브 쪽 둘 · 앱 쪽 U-1 · U-2 는 SPEC-002 §11).** 「추천으로」 한 마디면 본문 그대로 닫힌다. 이 둘 밖에는 WORK 전 사용자 결정이 없다.

| # | 정할 것 | 선택지 | 추천 | 근거 · 셈 |
|---|---|---|---|---|
| **U-3** | **HG1(윗고민 물려받음)이 걸리는 기준과 올라가는 단** | 기준: (a) 물은 고민의 **행이 0** 일 때(13 고민) (b) **묶음(`total`)이 0** 일 때(54 고민 = 13 + 행은 있으나 「계열 층만」 · 못 닿은 행뿐인 41) / 단: (가) 가장 가까운(행이 있는) 윗고민 하나 (나) 뿌리까지 전부 | **(a) · (가)** — 41 은 자기 행(계열 층 · 패키지)으로 답할 것이 있고, 윗고민의 행은 형제 고민의 것이라 섞으면 「이 고민의 것」 이 묻힌다. 13 은 전부 원장 확인이 걸린 Q10 꼴이다. (가): 가까운 윗고민의 행이 그 위 윗고민의 행에 통째로 들어 있어 더 올라가도 먼 가지의 행만 는다(13 고민 합 1,033 → 1,695 행) · 답 키 검토에서 Q10 을 바로 위 윗고민으로 정했다 | §5-9 HG1 · `app-key-fix1-report.md` 「코디 요청 셈」(54 는 묶음 기준) |
| **U-4** | **`concern_site`(고민 ↔ 부위 95 행)를 허브가 어디서 읽나**(HG3) | (a) silver `concern_site.csv` 를 **보조 입력 ③** 으로(gold 15표 · gold 해시 그대로 · `aux_hash` 만 바뀜) (b) gold 에 표 또는 관계를 더한다(gold-build · gold-check · gold 해시 · 표 수가 바뀐다) | **(a)** — 계층 3표를 같은 길로 정한 선례(11-16 「검수 뒤 결정 4」 ②)와 같고 gold 를 다시 뽑지 않는다. (b) 는 DB화 때 표로 올릴지와 함께 다시 본다 | §2-1 X7 · §5-9 HG3 · gold 에 이 표의 흔적 0 |

**0.7 — 사용자가 정할 것 셋 → 0.7.1: 셋 다 (a) 로 정해졌다**(_RESUME §2 11-17 「A8 화면 구조 … SPEC-001 0.7 U7-1~3 = (a)(전부 내려가기 · 하위 고민 부위 포함 · 줄임 일치 기본 on)」 — 아래 표는 기록으로 남긴다 · 수는 0.7.1 에서 고쳤다). 「추천으로」 한 마디면 본문 그대로 닫힌다(0.5.2 의 U-3 · U-4 는 11-17 에 추천으로 닫혔다 — _RESUME §2 11-17 「SPEC 0.5.2 사용자 결정(전부 추천)」). 번호는 다른 문서의 U 와 겹치지 않게 `U7-` 로 적는다.

| # | 정할 것 | 선택지 | 추천 | 근거 · 셈 |
|---|---|---|---|---|
| **U7-1** | **DP — 시술로 내려가기를 어느 고민에 거나** | (a) 시술 코드 없는 행이 있는 고민 **전부**(**142 고민** — 묶음이 이미 있는 고민에도 계열의 시술이 붙는다 · 고민당 **최대 107 시술** · 제품 길 포함 — 0.7.1 고침: 0.7.0 의 143 · 130 은 빈 고민 묶음을 센 값 · 검수 W-1 · N-5) + `in_groups` · `unit` 표지로 앱이 가른다 (b) **묶음이 0 인 고민에서만**(41 고민) — 묶음이 있으면 `descended` 는 `[]` | **(a)** — 「문항 맞춤 금지 — 일반 규칙」 · 허브는 폭을 자르지 않는다(무엇을 보여 줄지는 앱). (b) 는 같은 계열 층 행이 고민에 따라 내려가기도 안 내려가기도 해서 규칙이 「데이터가 얇을 때만」 이 된다. **결정됨 (a)** | §5-11 DP 셈(142 · 41 · 최대 107) · 지시서 H1 |
| **U7-2** | **CS — `sites[]` 에 하위 고민의 부위를 싣나** | (a) 자기 + **하위 고민(자손 전부)** — `match` 로 가른다(부위가 생기는 고민 100) (b) 자기 것만(85) | **(a)** — 넓은 고민의 응답에는 하위 고민 행이 이미 들어 있어 그 행의 자리가 필요하다 · 앱이 `match` = `직접` 만 쓰면 (b) 와 같다(정보를 잃지 않는 쪽). **결정됨 (a)** | §5-11 CS 셈 · 지시서 H2 「하위 고민 포함 여부 정함」 |
| **U7-3** | **NM — 줄임 일치를 기본으로 켜나** | (a) 기본 `abbr` = `on`(본문 — 붙여 쓴 꼴도 맞음) (b) 띄어 쓴 꼴만(질문 낱말 경계를 지킴 — 붙여 쓴 줄임은 놓침) (c) 기본 `off`(부르는 쪽이 켬) | **(a)** — 37 문항 새 후보 0 · **다른 표본에서는 0 이 아니다**(로컬 글 3,254 문장의 1.6% 에서 줄임 후보가 더 생긴다 — 검수 W-6 · §5-11 NM 「셈 — 오매칭」) · 줄임 후보는 `how` 표지가 붙어 앱이 Jev 로 한 번 더 묻는다 · C 열(LLM 이 도구를 스스로 부름)도 같은 후보를 받는다(HG2-6 과 같은 까닭 · 도구 설명 문장 — §4-1). **결정됨 (a)** · **0.8.0 — NM 을 지워 이 결정은 더 쓰이지 않는다**(_RESUME §2 11-18 D-1) | §5-11 NM 셈(0.8.0 에서 지움 — 변경 기록 0.7.0 · 0.7.1) |

- 지시서가 이미 정한 것(다시 묻지 않는다): 내린 결과는 시술(PRC)까지 · 경로 표시 · 메뉴 · 패키지 이름은 시술 후보가 아님 · 계열 단위 표지 · 제품도 내린다(「패키지 · 메뉴 · 계열 · 제품」) · `concern_candidates` 에 부위 코드 목록 · 기존 필드 불변 · 두 판 응답 같음.

**WORK(구현 계획)를 시작하기 전에 사용자가 정해야 할 것 = 0**(0.7.1 · 0.7.2 도 0 — SP1 의 기준 넓힘은 사용자 결정이 이미 난 것이다 · _RESUME §2 11-17 「규칙 변경 = 넣음」 · 거기서 끌어낸 것은 변경 기록 0.7.2 · O-31 ④). 0.7.0 의 셋(U7-1 ~ U7-3)은 11-17 에 (a) 로 닫혔고, 0.5.2 의 둘(U-3 · U-4)도 11-17 에 추천으로 닫혔다(0.7.0 은 이 줄에 0.5.2 의 문장 「위 2」 를 그대로 남겼다 — 검수 W-4). 0.7.1 의 규칙 SP 는 사용자 결정이 이미 난 것이고(_RESUME §2 11-17 「① 규칙」), 거기서 이 워커가 끌어낸 것은 O-30 · O-31 에 「구현 때 정함」 · 「1회차 trace 뒤」 로 놓았다 — 새 사용자 결정은 없다. 0.5.0 검수가 올린 사용자 결정 3 은 전부 추천으로 닫혔다(_RESUME §2 11-16 「SPEC 0.5.0 검수 뒤 결정 3」 — 허브에 닿는 것은 ① 의 「`coverage` 와 같은 함수」 하나이고 본문에 들어갔다 · §4-9 · §5-8). 0.5.0 에서 더한 O-19 ~ O-22 도 전부 「구현 때 정함」 · 「1회차 trace 뒤」 다. 0.3.0 의 「사용자 결정 대기」 는 O-10 이 결정됨으로 · O-12 가 승인됨으로 닫혔고, 남은 O-3 · O-7 의 stg 쪽 · O-8 · O-11 은 전부 stg 로 올릴 때의 것이다(재검수2 §5 C 「stg 승인 때」).

| # | 열린 것 | 선택지 | 추천 | 근거 | 상태 |
|---|---|---|---|---|---|
| O-1 | ~~3단 계층 펼침이 gold 15표에 없다~~ | — | **결정됨(11-16) → §2-1 · §3-1 · §4-4 「계층 펼침」 · §5-5** — (a) silver `concern` · `adverse` · `condition` 의 `code` · `parent_code` 를 보조 입력으로 · gold 불변 | _RESUME §2 11-16 「검수 뒤 결정 4」 ② | 결정됨 |
| O-2 | ~~「원천 미확정」 판정 재료가 허브 입력에 없다~~ | — | **결정됨(11-16) → §2-1 · §3-1 · §4-0 「원장 확인」 · §5-6** — (a) 원장 확인 목록의 id · 코드만 보조 입력으로 → 응답 `ledger_check[]` | _RESUME §2 11-16 「검수 뒤 결정 4」 ③ | 결정됨 |
| O-3 | gold 해시 식에 `questions.csv` 가 들어간다(16 파일) | (a) 폴더 그대로 읽어 gold-check 값과 맞춤 (b) 15표만으로 허브 해시를 따로 정의 | **(a)** 로컬 판 — `health.files[]` 에 `hash_only` 로 실어 다시 셀 수 있게(§4-8 · 재검수 R-4). stg 반입 때 다시 정함(`questions.csv` 는 질문 · 답 본문) | `gold-check.py:46-50` · 이 워커 재셈 16 파일 = 조사 §1-0 값 | 구현 때 정함(로컬 = (a)) · stg 쪽은 뒤 단계에서 사용자 확인(O-8 과 함께 · stg 반입 승인 때) |
| O-4 | ~~`resolve` 가 문장에서 낱말을 찾는 법~~ | — | **결정됨(11-16) → §4-1 · §5-1 R2 · R3 · R7 · R8** — (b) `g_entry.norm` 을 문장 `norm` 의 부분 문자열로 훑는다 · 긴 것 먼저이되 짧은 것도 남김 · 조사 목록을 쓰지 않는다. 0.4.1 구현은 (a) 였다 · **0.8.0 — 다시 바뀌었다: 문장에서 찾지 않는다 — `norm` 이 같은 이름만**(§5-1 R2 · _RESUME §2 11-18 D-1) | _RESUME §2 11-16 「길 찾기 재설계 진행」(「허브가 후보를 넓게(질문 안 입구 이름 전부 · 조사 무관)」) · `$W/_RESUME.md` §1 e2e 피드백 4 | 결정됨 |
| O-5 | 이름 — 모듈 · REST prefix · MCP 마운트 · 서버 이름 · env · REST 경로 · 0.4.0 에서 늘어난 입력 · 필드 이름(`offer_name_contains` · `tables` · `attr` · `counts.subjects` · `counts.by_column` · `counts.entities`) | §1-4 · §2-2 · §4-0 의 제안 / 옛 PR #31 과 겹치지 않게 다른 이름 | 제안 그대로(`release/v1.2.0` 에 충돌 없음 · PR #31 은 이어 쓰지 않음) | `git ls-tree origin/release/v1.2.0` | 구현 때 정함 |
| O-6 | 쪽 크기 기본 · 최대 · MCP 결과 크기 값 · 쪽 밖 목록(`modality_only[]` · `unreached[]` · `same_day_packages[]` · `ledger_check[]`)이 커질 때 | 쪽 크기: 기본 100 · 최대 500 / 다른 값 · 쪽 밖 목록: **한도 없음(통째로) / 커지면 쪽 넘김 대상으로 옮김** — 「자르는 한도」 는 선택지에서 뺐다(재검수2 X-2 · 쪽 넘김이 없는 목록의 한도 = 잘라 내기) | 제안값으로 시작 · 쪽 밖 목록은 한도 없이 통째로(실물 최대 40 · 16) · 시험 trace 로 조정. 쪽 크기 값은 **쪽 크기만 바꾼다 — 끝까지 넘기면 전부 나온다**(§4-0). 쪽 밖 목록은 어느 선택지에서도 전부 나온다 | 큰 사례: 근거 557 행(조사 §1-4) · 고민 524 행 · 역방향 379(조사 §5-2) · 검수 W-8 셈 · 원칙(_RESUME §2 11-16) | 1회차 trace 뒤 |
| O-7 | 진입점 | (a) 옛 틀처럼 별도 ASGI(`graph_main`) (b) 기존 `app.main` 에 라우터 · MCP 마운트 | 로컬 시험 = (a) · stg 이미지는 `app.main:app` 하나만 띄우므로 (b) 가 필요해 보임 — 배포 승인 때 정함 | `HUB-OLD backend/app/graph_main.py:1` · `release/v1.2.0` `backend/Dockerfile:27` | 구현 때 정함(로컬) · stg 쪽은 뒤 단계에서 사용자 확인(배포 승인 때) |
| O-8 | stg 데이터 반입 방법 — gold 15 + `source_ref` + 보조 입력 4 파일. 원장 확인 목록은 글 칸이 든 원본을 보낼지 · id · 코드만 뽑은 것을 보낼지 | 이미지에 넣기(레포 밖 빌드 단계) · VM 볼륨에 올리기 · 스토리지에서 받기 | 추천 보류 — 인프라 확인 필요 | `deployment.md:40-41` 「데이터 반입은 별도 gate」 · §2-1 X5 | 뒤 단계에서 사용자 확인(stg 반입 승인 때) |
| O-9 | `concern_candidates` 의 `site` 로 0 행일 때 | (a) 0 그대로 + `unfiltered_rows` (b) gold-build 처럼 필터를 풂 | **(a)** — 조용히 넓히지 않음 | `gold-build.py:701` | 구현 때 정함(본문 = (a)) |
| O-10 | ~~상품 이름 부분 일치 입구(Q33)~~ | — | **결정됨(11-16) → §4-4 「상품 이름 부분 일치」 · §9 T14** — (a) `facets` offer 에 `offer_name` 부분 일치 필터(입력 `offer_name_contains` — 이름은 O-5) | _RESUME §2 11-16 「재검수 2(r3) §5 결정」 A-2(재검수2 §5 A-2 = 추천) · `gold-build.py:875-876` | 결정됨 |
| O-11 | stg 에서의 접근 제어(인증) | 기존 허브 미들웨어를 따름 / 따로 | 확인 안 됨 — `release/v1.2.0` 의 `app/middleware` 를 읽지 않았다 | — | 뒤 단계에서 사용자 확인(배포 승인 때) |
| O-12 | **제안 모음** — 결정 · 조사에 값이 없어 이 워커가 본문에 「제안」 으로 적은 것(검수 W-9): ① `GOLD_EXPECTED_HASH` 가 다르면 시작 실패 · 없으면 기록만(§2-2 · §2-3 5) ② 헤더 · 보조 입력 칸이 다르면 시작 실패(§2-3 5) ③ `health.integrity` · `health.aux` 의 셈과 꼴(§2-3 6 · §4-8) ④ 오류 코드 3(`invalid_argument` · `not_found` · `cursor_invalid`)과 REST 상태 422 / 404 / 400(§4-0) ⑤ cursor 를 build 에 묶음(§4-0) ⑥ 보조 해시 `build.aux_hash` 와 그 식(§2-3 4) ⑦ `facets.hier` 의 기본값 `expand`(§4-4) | 제안 그대로 / 항목별로 고침 | 제안 그대로 — 내용에 무리 없음(검수 W-9). ⑦ 은 gold-build 시범이 늘 넓혔으므로 `expand` | 브리프 §3 은 「적재 실패 = 시작 실패」 · 「오류」 를 쓰라고만 함 · `gold-build.py:734 · 860 · 921` · 재검수2 N-8 · §5 B-1 | **승인됨(11-16 — 제안 그대로 시작)**. ④ ⑤ ⑥ 은 다른 서비스도 쓰는 응답 계약이라 「구현 때 정함」 이 아니라 사용자 승인으로 닫았다(_RESUME §2 11-16 「재검수 2(r3) §5 결정」(§5 B = 승인) · 지시 3 의 6 「r3 §5 B = 승인」) |
| O-13 | ~~부작용 · 사람 조건의 「하위」 가 몇 단인가~~ | — | **결정됨(11-16) → §4-4 「계층 펼침」** — (a) 자손 전부. 금기 행이 빠지면 안전 문제이고 37 문항 안에서는 자식 1단과 차이가 0 이다 | _RESUME §2 11-16 「재검수(r2) 뒤 결정 2」 · 셈: 자식 ≠ 자손인 코드 — 부작용 5 개(+ 390 행) · 조건 10 개(+ 77 행 · 전부 금기 행) · 37 안 차이 0(재검수 R-3) | 결정됨 |
| O-14 | ~~`ledger_check[]` 가 대조할 코드를 어디까지 넓히나~~ | — | **결정됨(11-16) → §4-0 「원장 확인」** — (a) 요청 코드 + 상품 `offer_id` 그대로. **holder 코드까지 넓힐지는 1회차 trace 를 본 뒤**(넓히면 물은 것과 먼 원장 확인이 섞여 「원천 미확정」 이 과하게 난다) | _RESUME §2 11-16 「재검수(r2) 뒤 결정 2」 · `gold-build.py:705-706 · 716 · 899-901` · 이 워커 셈(**서로 다른 코드** 기준): 원장 확인 코드 218 개 중 제품 **161** · 고민 24 · 상품 18 · 시술 11 · 케이스 2 · 효과 2 — 제품이 대부분이라 holder 확대의 영향이 크다. ((행, 코드) 쌍으로 세면 273 중 제품 213 — 0.2.0 은 이 둘을 섞어 적었다 · 재검수 R-1) | 결정됨 — holder 확대만 1회차 trace 뒤 |
| O-15 | 효과 계층을 펼칠지(재검수 R-5) — 효과도 `parent_code` 가 있으나 결정 ② 의 3표에 없어 `outcome` 값 쪽은 정확 일치다 | (a) 펼치지 않음(본문) (b) silver `effect` 의 `code` · `parent_code` 를 보조 입력에 더해 하위 효과까지 | **(a)** 로 1회차 — 37 문항에 효과가 입구인 문항이 없다. 추가 묶음 · 자유 질문에서 효과 입구가 행을 놓치는지 trace 로 보고 정함 | `semantic-map.md:23` · §4-4 | 1회차 trace 뒤 |
| O-16 | 속성 쪽 시작(재료 · 방법 · 해부 · 부위 코드)을 어느 도구로 내나 — _RESUME §2 11-16 「재검수 2(r3) §5 결정」(시작 길 추가) · 지시 3 의 4 「새 도구로 할지 기존 도구 입력으로 할지는 제안 + 열린 것(구현 때)」 | (a) `facets` 의 `node` 로 받는다(본문 — facet 마다 한 조회) (b) 새 도구 하나가 맞춤 칸 전부를 한 응답에 낸다(표마다 묶음 · 쪽 넘김은 표별) | **(a)** — 도구 수 8 이 그대로이고 행 필드 · 쪽 넘김 · `total` 단위 · `ledger_check[]` · 답 키 뽑기(SPEC-002 §9-5 `calls[]`)가 대상 쪽과 같은 꼴로 선다. (b) 는 부위 하나에 조회 7 을 1 로 줄이지만 응답에 표가 섞여 `total` 단위를 새로 정해야 한다 | §4-4 「속성 쪽」 · 헤더 전수(부록 A) | 구현 때 정함(본문 = (a)) |
| O-17 | 속성 쪽 시작의 한계 ① 부위 계층 — 부위에 `parent_code` 가 있으나(semantic-map §1) 넓히지 않는다(상위 부위로 물으면 하위 부위 행이 안 나온다) ② 해부 ↔ 부위 잇기(`anatomy_site`)도 안 쓴다 ③ `g_offer.materials` 3 종(10 행) · `g_offer.sites` 9 종(59 행)은 입구 이름과 달라 안 닿는다 ④ `tissue_name` 은 입구가 아니다 ⑤ **같은 한계가 `concern_candidates` 의 `site` 필터에도 있다** — 정확 일치라 상위 부위로 걸면 하위 부위 행이 안 맞는다(SPEC-002 §3-1 BR1). ① · ⑤ 를 정할 때 쓸 셈: silver `site` 89 행 중 부모(`parent_code`)가 있는 것 21(재검수3 N-6 셈) | (a) 지금대로 — 정확 일치만 (b) silver `site` 의 `code` · `parent_code` 를 보조 입력에 더해 하위 부위까지(부작용 · 조건과 같은 꼴) | **(a)** 로 1회차 — 37 문항에 속성으로 시작하는 문항이 없다. 추가 묶음(SPEC-002 §9-2 「속성 시작」) trace 에서 상위 부위로 물어 행을 놓치는지 본 뒤 정한다. (b) 는 보조 입력이 느는 결정이라 그때 사용자에게 묻는다 | `semantic-map.md:20 · 21 · 96` · 이 워커 셈(§4-4) · _RESUME §2 11-16 「검수 뒤 결정 4」 ② | 1회차 trace 뒤 |
| O-18 | 입구 목록을 어느 도구로 내나(§4-1 목록 꼴) | (a) `resolve` 에 `text` 없는 꼴(본문) (b) 따로 도구(`entries`) | **(a)** — 같은 `g_entry` 행 · 같은 `candidates[]` 꼴이라 도구를 늘릴 까닭이 없다 | §4-1 | 구현 때 정함(본문 = (a)) |

| O-19 | 정보 종류 셈을 어느 도구로 내나(§4-9) — _RESUME §2 11-16 「길 찾기 재설계 진행」 「후보마다 행 수 셈」 · `$W/spec-v05-instructions.md` 「새 도구 또는 resolve 확장 — 제안 + 열린 것」 | (a) 새 도구 `coverage`(본문 — 노드 목록을 받아 셈만) (b) `resolve` 맞춤 꼴의 `candidates[]` 에 셈 필드를 붙인다(도구 수 8 그대로) (c) 둘 다 | **(a)** — 입구 후보뿐 아니라 깊이 후보(값 쪽 시작의 대상 · 상대 끝)의 셈도 같은 도구로 받을 수 있고(SPEC-002 §3-3 「후보 설명에 행 수」), `resolve` 의 응답 꼴(`g_entry` 행 그대로)이 안 바뀐다. (b) 는 왕복이 하나 줄지만 입구가 아닌 후보의 셈을 못 낸다. C 열에 이 도구를 줄지는 SPEC-002 O-15 | §4-9 · 조사 §6-3(8도구) | 구현 때 정함(본문 = (a)) |
| O-20 | 정보 종류 나눔(§5-8 의 14) · `coverage.nodes` 상한 64 | 표 그대로 / 종류를 합치거나 쪼갬(예: `overview` + `mechanism` 을 하나로 · `adverse` 에서 `adverse_detail` 을 따로 · `same_day` 의 패키지를 따로) / 상한 값 | 표 그대로 1회차 — 종류는 **읽는 단위**라 틀려도 그 종류 안의 행은 빠지지 않는다. Jev 가 종류를 가르는 정확도(SPEC-002 O-24)를 trace 로 보고 합치거나 쪼갠다 | `$W/spec-v05-instructions.md` A ② 의 종류 열거(「개요 · 원리 · 효과 · 적응 · 부작용 · 금기 · 회복 · 같은 날/간격/순서 · 상품 · 패키지 · 제품 목록 …」) · `$W/WORK-004-speed-tab.md`(속도 탭의 묶음 목록) | 1회차 trace 뒤(본문 = 14 · 64) |
| O-21 | ~~하위 층의 한계(§5-3 S6) — 두 단 아래(계열의 하위 케이스)는 `g_scope` 에 없어 안 나온다~~ → **결정됨(0.5.2) → §5-9 HG2 · §4-2 · §4-4 · §4-6 · §4-9 · §9 T21** — 허브가 `g_scope` 의 하위 role 행을 끝까지 따라간다(아래 선택지에 없던 길 — (b) 를 앱이 아니라 허브가 하는 꼴 · gold 불변). trace = Q12 표본 2 빠짐. **남은 것**: 케이스의 「제품 경유」 는 여전히 하위가 아니라 세지 않는다(아래 0.5.1 의 글 · 1회차 trace 뒤) | (a) 지금대로 — `g_scope` 한 단 (b) 앱이 하위 시술마다 다시 `scope` 를 불러 두 단을 펼친다 (c) gold 에 role 을 더한다(gold 가 바뀐다) | **(a)** 로 1회차 — 계열 노드에서 `self` 0 · `lower` 1 이상인 (대상, 종류)는 적응 1 · 효과 1 · 상품 15 뿐이다(§4-9 끝 줄 셈). 이 수는 한 단으로 **잡히는** 수다 — **놓치는 수**는 따로다(0.5.1 — 검수 v05 W-8 · §5-3 S6): 두 단 아래에만 행이 있는 계열 = 상품 2 · 적응 · 효과 · 부작용 0 / 자기 0 이고 「제품 경유」 holder 에만 행이 있는 케이스 = 적응 80 · 효과 115 · 부작용 97(입구 있는 케이스는 8 · 14 · 5). 규모가 작고 케이스는 답에서 그 시술로 말하므로(SPEC-002 §4 G10) (a) 그대로 간다. 계열을 물어 케이스 행을 놓치는 수를 trace 로 본 뒤 정한다. (c) 는 gold 를 바꾸는 결정이라 그때 사용자에게 묻는다 | §5-3 S1 · S6 · 이 워커 셈 | 1회차 trace 뒤 |
| O-22 | 구현 뒤 남은 허브 NOTE(허브 검수 N-2 · N-10 — 계약 밖) ① `pair` 가 (subject, holder) 마다 첫 `g_scope` 행 하나만 `a_layer` 로 남긴다 — 지금 그런 짝은 0 ② `async` 핸들러가 동기 코어를 바로 부른다(로컬 단일 사용자는 문제없음) | ① 적재 때 「(subject, holder) 중복 0」 을 `health.integrity` 에 센다 / `a_layer` 를 목록으로 ② stg 동시 호출 전에 `def` 핸들러로 | ① 셈을 더한다(계약은 그대로) ② stg 올릴 때 | `$W/review-code-hub.md` N-2 · N-10 | ① **결정됨(0.5.2 — 구현에서 정해짐)** → §4-8 `integrity.scope_duplicate_subject_holder_rows`(허브 검수 v05 N-8) · 뒤 단계에서 사용자 확인(② — 배포 승인 때) |
| O-23 | **[0.6 — 구현에서 정해진 꼴을 §5-10 에 되적었다(본문 그대로 구현됨)]** 0.5.2 에서 더한 이름 · 꼴(§5-9) — 입력 `upper`(`auto` · `none`) · `descend`(`all` · `one`) · 필드 `inherited_from{concern_code, steps}` · `counts.self_rows` · `counts.by_site_match` · `site_match[]`(`column` · `concern_site` · `csi_ids[]`) · `layer.depth` · `layer.via[]` · `scope` 행의 `depth` · `via[]` · 닫힘을 적재 때 세어 둘지 요청 때 따라갈지 | 본문 그대로 / 이름 · 꼴을 고침 / `upper` · `descend` 입력을 두지 않음(늘 넓힘) | 본문 그대로 — 두 입력은 0.5.1 응답을 다시 볼 수 있게 하는 길이고 기본값이 넓히는 쪽이라 폭이 줄지 않는다 | §5-9 · 검수 v05 W-4(기본값이 C 열을 막지 않게) | 구현 때 정함 |
| O-24 | HG3 을 어디서 합치나 | (a) `concern_candidates` 의 `site` 맞춤을 넓힘(본문) (b) `resolve` 가 「고민 + 부위」 를 묶인 하위 고민으로 바꿔 냄 (c) 앱이 묶인 고민을 따로 불러 합침(앱이 silver 를 읽어야 한다) | **(a)** — 대상이 그대로 · 글자 일치 행도 남음 · 새 행 0 · C 열도 같은 도구로 받음 · `resolve` 가 뜻을 고르지 않음(§5-9 HG3 아래) | §5-9 HG3 · §5-1 R6 · R8 | 구현 때 정함(본문 = (a)) |
| O-25 | HG1 이 내는 행의 범위 — 윗고민으로 물은 행 전부(본문 · 형제 고민의 행 포함) / 윗고민의 「직접」 행만 | 전부 / 직접만 | **전부** — 직접만 쓰면 13 가운데 5 가 다시 0 이고, 사용자가 본 답 키(Q10)가 전부 기준이다. 형제 고민 행이 답에서 「이 고민의 것」 처럼 읽히는지는 1회차 답으로 본다(SPEC-002 G12 꼴) | §5-9 HG1-3 · 셈 | 1회차 trace 뒤(본문 = 전부) |
| O-26 | **[0.6 — 37 batch 로 봄: 사건 하나를 물은 계열 조회의 B 입력 206 KB · 상세 464 행 가운데 그 사건의 것 34 행 → 둘째 선택지(앱이 `filters.adverse_risk_id` 로 좁힘)를 SPEC-002 §3-7-5 BR5 로 제안 · 사용자 결정 SPEC-002 U-8 · 허브 계약은 그대로]** HG2 뒤 응답이 커지는 자리 — 계열의 `facets` adverse_detail(예: Q12 의 계열 조회 + 188 행) · 계열 끝 `pair` | 지금대로(쪽 넘김 끝까지) / 계열 조회에서 딸린 상세를 사건 필터로 좁히는 길을 앱이 쓴다 | 지금대로 — 폭은 자르지 않는다(원칙). 크기 · 시간은 1회차 trace 로 본다 | §5-9 HG2 셈 | 1회차 trace 뒤 |

| O-27 | 0.7 에서 더한 이름 · 꼴(§5-11 DP · CS) — 입력 `to_procedure`(`auto` · `none`) · 필드 `descended[]{modality_code, modality_name, unit, procedures[], from[]}` · `from[].lands` · `path[]` 항목 꼴 · `counts.descended` · `sites[]` 항목 꼴 · `counts.sites` · 쪽 밖 목록으로 둘지(지금 한 응답 최대 107 시술 · `sites[]` 23 항목(서로 다른 부위 18) — 0.7.1 고침 · 커지면 O-6 대로 쪽 단위를 준다) | 본문 제안 / 다른 이름 · 꼴 | 본문 제안으로 시작 | §4-5 · §5-11 | 구현 때 정함 |
| O-28 | DP 의 한계 ① **케이스로는 내리지 않는다** — 리스트의 단위가 시술이다(_RESUME §2 11-17 「리스트는 우리 기준의 시술로」). 내린 시술의 케이스 · 제품은 앱이 `scope` · `facets` 로 읽는다 ② 제품 → 계열 길(「제품 — 케이스 없음」 8 제품)은 그 제품이 실제로 쓰이는 시술을 모르는 채 계열의 시술 전부로 내린다 — `path[]` 에 제품이 남아 「제품 기준」 임이 보이지만 가장 넓은 내림이다(코디 셈 41 은 이 길을 뺀 값 — §5-11 DP 셈) ③ 메뉴의 원리 · 개요 같은 원장 글은 silver 에 없다(`$W/_RESUME.md` §1 「수정 2 목록」 9 — 모델링 다시 보기는 0.3 설계 때 사용자 몫) | ① 그대로 ② 그대로 / 제품 길을 뺌 ③ 범위 밖 | ① · ② 그대로(지시서가 제품을 넣었다) | §5-11 DP | 1회차 trace 뒤(②) · 뒤 단계에서 사용자 확인(③) |
| O-29 | ~~NM 의 값 · 한계 — 접두 하한 2 글자 · 열쇠 길이 하한 4 · 입력 `abbr` · 필드 `matched.how` · `matched.full`~~ | — | **0.8.0 에서 닫혔다 — NM 을 지웠다**(§5-11 NM). 줄여 말한 이름 · 가운데 낱말 빠짐 · 오타 · 바꿔 말하기는 부르는 쪽의 일이다(상담 = SPEC-008 의 이해 호출 · 목록의 별칭) | _RESUME §2 11-18 D-1 · 변경 기록 0.8.0 | 닫힘 |
| O-30 | 0.7.1 에서 더한 이름 · 꼴(§5-11 SP) — 입력 `site_mode`(`auto` · `filter`) · 머리 `site_applied`(`null` · `filter` · `prefer`) · 행 `site_prefer` · 묶음 `n_site_prefer` · `counts.site_prefer{rows, groups}` · **표지의 뜻을 「`filter` 였다면 남았을 행」(글자 일치 ∪ 묶임)으로 둔 것** — 결정 문장은 「행 부위 글자 일치」 다. 둘이 갈리는 곳은 5 고민 · 17 짝 · 229 행뿐이다(§5-11 SP 셈 — 윗고민이 그 부위에 묶인 고민 2 · 물려받은 윗고민 행 안의 형제 고민 행 3). **0.7.2 — 이름 · 꼴은 그대로다**(새 필드 · 새 입력 0). `prefer` 짝이 늘어 갈리는 곳도 는다: 묶임으로만 맞는 행이 있는 짝 17 → 41(+ 24 · 고민 17) · 그 행 229 → 446(+ 217) | (a) 본문 — 글자 일치 ∪ 묶임(0.7.0 이 내던 행이 전부 표지 행으로 남는다) (b) 글자 일치만(결정 문장 그대로 — 그 229 행은 나오되 표지가 없다) / 이름을 고침 / `site_mode` 입력을 두지 않음 | **(a)** — 「그 부위의 것」 이라는 정보를 잃지 않는 쪽이고 `site_match[]` 로 어느 쪽으로 맞았는지 갈라 (b) 는 앱이 고를 수 있다(`by` = `column` 만 쓰면 (b)) | §5-11 SP3 · 셈 | 구현 때 정함(본문 = (a)) |
| O-31 | SP 의 한계 ① ~~부위가 묶인 고민을 그 고민의 부위가 아닌 부위로 걸면 0~~ — **0.7.2 에서 닫혔다**(SP1 — 그 8,709 짝이 `prefer` 가 되어 0 행이던 8,444 짝이 전부 행을 낸다 · _RESUME §2 11-17 「규칙 변경 = 넣음」) ② `prefer` 인데 **표지가 0** 인 응답이 대부분이다(0.7.2 — 22,949 짝 가운데 표지 있는 짝 497 · 그 고민의 행에 부위 글자가 드물다 · 실물 `CON-048` × `SITE-051` 이름 · `CON-005` × `SITE-051` 이름 둘 다 표지 0) — 「우선 표시」 가 실제로 앞에 놓을 것이 생기려면 데이터 보강(_RESUME §2 11-17 「concern_site 보강 판정 = 추천」 — 7 고민 8 행 · 구현 뒤)이 있어야 한다 ③ 부위 계층으로 넓히지 않는 것은 그대로다(O-17 ① · ⑤ — 상위 부위로 물으면 하위 부위의 묶임은 「안」 이 아니라 `prefer` 다) ④ (0.7.2) **`filter` 인데 0 행인 짝 5** — 묶인 고민 자신의 행이 0 이라(`CON-206` · `CON-230`) 그 고민 · 그 윗고민을 그 부위로 물으면 0 + `unfiltered_rows` 다(§5-11 「셈 — 남는 0」 · 0.5.2 부터 같다) | ① 닫힘 ② 그대로 ③ 그대로 ④ 그대로 / 「`filter` 로 0 이면 `prefer` 로 낸다」(O-9 (b) 꼴 — 조용히 풀지 않고 표지로 밝힘) | ① 닫힘 ② 데이터 몫 ④ 그대로 — 결정이 「안에 있으면 거름」 이고 5 짝뿐이다 · 그 고민의 적응 행이 생기면 풀린다(바꾸면 사용자 결정) | §5-11 SP 셈 · _RESUME §2 11-17 「① 규칙」 · 「규칙 변경 = 넣음」 | ① 닫힘(0.7.2) · ② 뒤 단계(보강 반영 뒤) · ④ 1회차 trace 뒤 |
| O-32 | 0.8.0 `resolve` 의 남기는 꼴 — 입력 `abbr` 을 **없앰**(주면 `invalid_argument` · 목록 꼴 머리 `request.abbr` 칸도 없어진다 · cursor 는 `request` 로 서명하므로 0.7.2 가 낸 cursor 를 0.8.0 이 받지 않는다 — 쪽 넘김 도중에 판이 바뀔 때만) · `matched` = `{span}` 하나 | (a) 본문 (b) `abbr` 을 받되 쓰지 않는다(목록 꼴 응답 · cursor 가 0.7.2 와 글자까지 같다 — 죽은 입력이 남는다) (c) `matched` 를 통째로 없앤다(답 키 명세 `name_to_entry` 가 `matched.span` 을 읽는다) | **(a)** — 결정이 「부분 · 줄임 · 겹침 규칙 지움 · 최소 꼴」 이고 옛 응답을 쓰는 쪽(시험 앱)은 0.7.2 에 묶인다 | _RESUME §2 11-18 D-1 · D-2 · 변경 기록 0.8.0 | WORK 전(코디) |
| O-33 | 시험 앱을 옛 판에 묶는 범위 · 방법 — 결정(D-2)은 **B 열**이다. C 열(LLM 이 MCP `resolve` 를 스스로 부름)과 답 키 명세(이름 → 입구)도 맞춤 꼴을 부른다(변경 기록 0.8.0 「쓰는 곳별 영향」) | (a) 시험 앱 전체(B · C · 답 키)를 같은 옛 판 허브에 붙인다 (b) B 열만 옛 판 · C 열 · 답 키는 0.8.0(C 열 측정값이 0.7.2 때와 견줘지지 않는다) / 묶는 방법 — 옛 커밋(`3a5da4a` 또는 `d97a9ad`)의 워크트리로 허브를 따로 띄운다 | **(a)** — 세 열을 같은 gold · 같은 도구로 견주는 것이 시험 앱의 전제다(SPEC-002) | _RESUME §2 11-18 D-2 | 시험 앱을 다시 돌릴 때(코디) |
| O-S1 | (SPEC-003 §11-9) 꺼짐 오류 코드 — `unavailable` · REST `503` · 본문 꼴 §4-0 그대로 | — | **닫힘(0.8.2)** — §4-0 오류 표 넷째 줄 | _RESUME §2 11-18 「SPEC-003 0.2.0 정할 것 코디 답」 | 닫힘 |
| O-S2 | (SPEC-003 §11-9) MCP 꺼짐 = HTTP `503`(세션은 열고 도구 오류 아님) | — | **닫힘(0.8.2)** — §4-0 오류 표 `unavailable` 줄 | 같은 행 | 닫힘 |
| L-v081 | 0.8.1 코드 검수 Low 3(`review-code-hub-v081.md` L-1 ~ L-3) — 시험 주석 · docstring 에 옛 줄임 뜻이 남음(`tests/gold_fixture.py` 머리말 · `tests/test_medallion_repo.py` `test_dt10_…` docstring · `tests/test_gold_mcp.py` 의 「없어야 할 조각」 `how`). 동작 영향 0 | 고침 / 그대로 | 다음 허브 판에서 한 번에 고침 | 허브 `d3d078c` 에 셋 다 그대로 남음(이 워커 확인) | **남음**(다음 작업) |


## 부록 A. 도구 출력 필드 ↔ gold CSV 헤더

「그대로」 = 그 표의 전 칸. 이 표는 기계 대조용이다(§9 T3) — 셋째 칸의 이름이 그 CSV 헤더에 전부 있어야 한다.

| 도구 | 표 | 헤더 필드 |
|---|---|---|
| resolve | g_entry | gid, text, norm, entity_table, entity_code, entity_name, name_kind, silver_table, silver_id, evidence_kind |
| scope | g_scope | gid, subject_table, subject_code, subject_name, holder_table, holder_code, holder_name, role, path, link, silver_table, silver_id, evidence_kind |
| neighbors | g_edge | edge_id, src, dst, edge_type, gold_table, gold_id, evidence_kind |
| neighbors | g_node | node_id, node_table, node_code, label |
| facets | g_profile | gid, subject_table, subject_code, name_ko, name_en, name_en_source, modality_code, modality_name, procedure_code, procedure_name, mechanism_code, mechanism_name, materials, methods, tissue_name, anatomy_name, site_name, product_kind, organizations, n_cases, n_products, overview, mechanism_text, description, silver_table, silver_id, evidence_kind |
| facets | g_indication | gid, asked_concern_code, asked_concern_name, concern_code, concern_name, concern_match, site_code, site_name, target_table, target_code, target_name, reach, candidate_table, candidate_code, candidate_name, procedure_code, procedure_name, case_site_name, conditions, note, silver_table, silver_id, evidence_kind |
| facets | g_outcome | gid, target_table, target_code, target_name, effect_code, effect_name, site_name, onset_text, onset_min, onset_max, onset_unit, onset_qualifier, peak_text, peak_min, peak_max, peak_unit, peak_qualifier, duration_text, duration_min, duration_max, duration_unit, duration_qualifier, note, silver_table, silver_id, evidence_kind |
| facets | g_adverse | gid, target_table, target_code, target_name, adverse_code, adverse_name, adverse_top_name, site_name, polarity, severity_text, onset_text, onset_min, onset_max, onset_unit, onset_qualifier, duration_text, duration_min, duration_max, duration_unit, duration_qualifier, freq_value_text, freq_min, freq_max, freq_unit, freq_qualifier, freq_denominator, freq_grade_text, ratings, n_factor, n_guidance, note, silver_table, silver_id, freq_silver_id, evidence_kind |
| facets | g_adverse_detail | gid, detail_kind, adverse_risk_id, adverse_name, target_table, target_code, target_name, kind, timing_text, level_text, text, condition_name, site_name, anatomy_name, silver_table, silver_id, evidence_kind |
| facets | g_recovery | gid, target_table, target_code, target_name, text, min, max, unit, qualifier, silver_table, silver_id, evidence_kind |
| facets | g_contraindication | gid, target_table, target_code, target_name, condition_code, condition_name, site_name, polarity, level_text, period_text, period_min, period_max, period_unit, period_qualifier, period_from, reason_text, silver_table, silver_id, evidence_kind |
| facets | g_offer | gid, offer_id, offer_name, modality_code, modality_name, price_low, price_high, price_mid_raw, currency, quantities, item_table, item_code, item_name, item_text, item_note, reach, procedure_code, procedure_name, sites, concerns, effects, materials, variant_text, condition_text, product_origin, silver_table, silver_id, evidence_kind |
| facets | g_package | gid, package_id, package_name, package_kind, concern_code, concern_name, conditions, step, item_table, item_code, item_name, session_text, item_procedure_code, text, expected_text, duration_text, evidence_text, n_schedule, silver_table, silver_id, evidence_kind |
| concern_candidates | g_indication | gid, asked_concern_code, asked_concern_name, concern_code, concern_name, concern_match, site_code, site_name, target_table, target_code, target_name, reach, candidate_table, candidate_code, candidate_name, procedure_code, procedure_name, case_site_name, conditions, note, silver_table, silver_id, evidence_kind |
| pair | g_pair | gid, from_table, from_code, from_name, to_table, to_code, to_name, kind, question_class, self_pair, level_text, interval_text, interval_min, interval_max, interval_unit, interval_qualifier, order, same_day, same_day_text, text, evidence_text, goal_effects, conflict_id, conflict_side, silver_table, silver_id, evidence_kind |
| pair | g_package | gid, package_id, package_name, package_kind, concern_code, concern_name, conditions, step, item_table, item_code, item_name, session_text, item_procedure_code, text, expected_text, duration_text, evidence_text, n_schedule, silver_table, silver_id, evidence_kind |
| pair | g_scope | role, path, holder_table, holder_code, holder_name |
| evidence | g_evidence | gold_table, gold_id, silver_table, silver_id, fields, evidence_kind |
| evidence | source_ref | target_table, target_id, field, ref |
| (속성 쪽 맞춤 칸) facets | g_profile | materials, methods, anatomy_name, site_name |
| (속성 쪽 맞춤 칸) facets | g_indication | site_code, site_name, case_site_name |
| (속성 쪽 맞춤 칸) facets | g_outcome | site_name |
| (속성 쪽 맞춤 칸) facets | g_adverse | site_name |
| (속성 쪽 맞춤 칸) facets | g_adverse_detail | anatomy_name, site_name |
| (속성 쪽 맞춤 칸) facets | g_contraindication | site_name |
| (속성 쪽 맞춤 칸) facets | g_offer | materials, sites |
| (속성 쪽 이름 읽기) facets | g_entry | entity_table, entity_code, entity_name |
| (상품 이름 부분 일치) facets | g_offer | offer_name |
| (입구 목록) resolve | g_entry | gid, text, norm, entity_table, entity_code, entity_name, name_kind, silver_table, silver_id, evidence_kind |
| (정보 종류 셈 — 읽는 칸) coverage | g_scope | subject_table, subject_code, subject_name, holder_table, holder_code, role |
| (정보 종류 셈 — 읽는 칸) coverage | g_entry | entity_table, entity_code, entity_name |
| (정보 종류 셈 — 원리 칸) coverage | g_profile | gid, mechanism_code, mechanism_name, mechanism_text |
| (정보 종류 셈 — 개요 칸) coverage | g_profile | materials, methods, tissue_name, anatomy_name, site_name, product_kind, organizations, n_cases, n_products, overview, description |
| (넓은 후보 — 맞추는 칸) resolve | g_entry | norm |
| (보조) facets | concern | code, parent_code |
| (보조) facets | adverse | code, parent_code |
| (보조) facets | condition | code, parent_code |
| (보조 · 0.5.2 HG1 · HG3) concern_candidates · coverage | concern | code, parent_code |
| (보조 ③ · 0.5.2 HG3 — U-4 (a)) concern_candidates | concern_site | id, concern_code, site_code |
| (0.5.2 HG3 — 부위 이름 읽기) concern_candidates | g_entry | entity_table, entity_code, entity_name |
| (0.5.2 HG3 — 맞추는 칸) concern_candidates | g_indication | site_name, case_site_name, concern_code, asked_concern_code |
| (0.5.2 HG2 — 따라가는 칸) scope · facets · pair · coverage | g_scope | gid, subject_table, subject_code, holder_table, holder_code, role |
| (0.7 DP — 따라가는 칸) concern_candidates | g_scope | gid, subject_table, subject_code, holder_table, holder_code, holder_name, role |
| (0.7 DP — 내릴 행을 고르는 칸) concern_candidates | g_indication | gid, reach, target_table, target_code, target_name, procedure_code |
| (보조 ③ · 0.7 CS) concern_candidates | concern_site | id, concern_code, site_code |
| (0.7 CS — 부위 이름 읽기) concern_candidates | g_entry | entity_table, entity_code, entity_name |
| ~~(0.7 NM — 줄임 열쇠를 짓는 칸) resolve~~ — 0.8.0 에서 없앴다(맞춤 꼴이 읽는 칸 = `norm`) | g_entry | norm |
| (0.7.1 SP — 우선 표지를 다는 칸) concern_candidates | g_indication | site_name, case_site_name, concern_code |
| (보조) ledger_check — 메모리에 남김 | ledger-check-list | id |
| (보조) ledger_check — 코드 추출에만 읽음 | ledger-check-list | silver_now, what, name |

「(보조)」 줄은 보조 입력이다(0.5.1 의 다섯 줄 + 0.5.2 의 두 줄 = 일곱 줄) — 표 이름은 gold 가 아니라 silver 표(`$SM/silver/` — `concern` · `adverse` · `condition` · `concern_site`)와 원장 확인 목록(`$SM/notes/ledger-check-list.csv`)의 헤더와 대조한다. 이 칸들은 **읽는 칸**이지 응답 필드가 아니다(응답에는 `hier` · `ledger_check[]` 계산 필드로만 나간다).

「(정보 종류 셈)」 네 줄(개요 칸 줄은 0.5.1) · 「(넓은 후보)」 한 줄은 0.5.0 에서 더한 **읽는 칸**이다 — `coverage` 의 응답은 전부 계산 필드라 헤더 필드가 없고(§4-9), 세는 표는 §5-8 표의 조회가 읽는 표(위 `facets` · `pair` · `scope` 줄)와 같다.

「(속성 쪽 맞춤 칸)」 일곱 줄은 **맞추는 칸**이다(§4-4 「속성 쪽」 표 — 응답 행은 위 `facets` 줄의 전 칸 그대로). 반대 방향 대조도 한다: gold 15표 헤더에서 이름에 `site` · `material` · `method` · `anatomy` 가 든 칸은 이 일곱 줄에 **전부** 있어야 한다(§9 T3 · T12).

`health.files[]` 의 `hash_only` 줄(`questions.csv`)은 이 표에 없다 — 칸을 읽지 않고 파일 바이트의 sha256 만 낸다(§4-8).

계산 필드(헤더 아님 — 전부): `gold_table`(행 표지 · `g_edge` · `g_evidence` 에서는 헤더이기도 함) · `layer`(+ `layer.scope_gid`) · `hier`(`asked_code` · `match`) · `attr`(`asked_table` · `asked_code` · `column`) · `ledger_check`(`code` · `lck_ids` · `on`) · `build.aux_hash` · `matched.span`(0.8.0 — `matched.start` · `matched.covered_by` 를 없앴다 · 0.4.1 의 `matched.particle` 도 없다) · `counts.distinct_rows` · `coverage` 의 전 필드(`items` · `node` · `name` · `kinds` · `kind` · `self` · `lower` · `lower_holders` · `inherited`) · **0.5.2**: `inherited_from`(`concern_code` · `steps`) · `site_match`(+ `csi_ids`) · `layer.depth` · `layer.via` · `scope` 행의 `depth` · `via` · `counts.self_rows` · `counts.by_site_match` · `in_range` · `ambiguous` · `counts*` · `distinct_nodes` · `total` · `next_cursor` · `n_rows` · `n_source_refs` · `a_side` · `a_layer` · `b_layer` · `groups` · `modality_only` · `unreached` · `same_day_packages` · `build` · `request` · `health` 의 전 필드.

0.7 의 계산 필드(헤더 아님): `concern_candidates` 의 `descended[]`(`modality_code` · `modality_name` · `unit` · `procedures[]{procedure_code, procedure_name, scope_gid, in_groups}` · `from[]{gid, reach, lands, procedure_codes[], path[]{table, code, name, role, scope_gid}}`) · `sites[]{site_code, site_name, concern_code, csi_id, match}` · `counts.descended` · `counts.sites` · ~~`resolve` 의 `matched.how` · `matched.full`~~(0.8.0 에서 없앴다). 값은 전부 위 「0.7」 다섯 줄의 칸에서 온다 — 허브가 짓는 글은 고정값 `unit` = `계열` · `match` · `lands` · `how` 의 어휘뿐이다.

0.7.1 의 계산 필드(헤더 아님): `concern_candidates` 의 `site_applied`(머리) · `site_prefer`(행) · `n_site_prefer`(묶음) · `counts.site_prefer`(`rows` · `groups`) · `request.site_mode`. 값은 위 「0.7.1 SP」 한 줄의 칸과 보조 ③ 에서 온다 — 허브가 짓는 글은 `site_applied` 의 어휘(`filter` · `prefer`)뿐이다. **0.7.2 — 새 계산 필드 · 새로 읽는 칸 0**: `site_applied` 를 정하는 식만 바뀐다(물은 부위의 코드 ∈ `sites[].site_code` — 둘 다 0.5.2 · 0.7 에 이미 있는 값이다 · `g_entry` 의 site 입구 `entity_name` · 보조 ③).

0.8.0 — 새 계산 필드 · 새로 읽는 칸 0. **없어진 계산 필드**: `resolve` 의 `matched.start` · `matched.covered_by` · `matched.how` · `matched.full` · 머리 `request.abbr`. 맞춤 꼴이 읽는 gold 칸은 `g_entry.norm` 하나다(줄임 열쇠를 짓던 `text` 는 응답 행의 칸으로만 남는다).

## 변경 기록

### 0.8.2 — 2026-11-18 · stg 판 되적기(SPEC-003 0.2.0 §11 · 구현 `d3d078c`) — 오류 `unavailable` · 설정 셋

근거: `$W/_RESUME.md` §2 2026-11-18 「SPEC-003 0.2.0 정할 것 코디 답」(O-S1 · O-S2) · 「gold MCP 421 고침」 · 「SPEC-003 stg 검수 WARN 코디 답」(R-2) · 「stg 반입 완료」 · `$W/stg-runbook.md` 실행 기록 · `$W/review-code-hub-stg.md` · `$W/review-code-hub-v081.md` · 허브 `d3d078c`(`app/modules/gold/config.py` · `errors.py` · `assembly.py` — 구현 결과가 정본). **도구 9 의 입력 · 출력 계약 변경 0** — 켜진 gold 의 응답은 0.8.1 그대로다.

- §4-0 오류 표에 넷째 줄 `unavailable` · REST `503` · MCP HTTP `503`(gold 꺼짐 — SPEC-003 §11-3). 본문은 F 코드 + 짧은 사유만(접속 대상은 로그만).
- §2-2 설정 셋: `GOLD_MCP_ALLOWED_HOSTS` · `GOLD_MCP_ALLOWED_ORIGINS`(DNS rebinding 보호는 켠 채 허용 목록에 더함 · **Gateway 는 Host 를 백엔드 내부 주소로 넘기므로 그 값도 둔다**) · `GOLD_LOAD_TIMEOUT_SECONDS`(기본 60 · stg 30).
- §8 끝에 「stg 에 올라갔다 — 진입점 · 반입은 SPEC-003 §11 이 정본」 한 단락.
- §10: O-S1 · O-S2 닫음 · 0.8.1 코드 검수 Low 3(옛 줄임 주석 — L-1 ~ L-3)을 「남음(다음 작업)」 줄로.

### 0.8.1 — 2026-11-18 · 검수(`review-spec-008.md`) F-1 · F-11 — 끈 상태 대화의 영향 행 · 고칠 · 지울 허브 시험

근거: `$W/_RESUME.md` §2 2026-11-18 「SPEC-008 검수 WARN 16 코디 답」 행(F-1 ⓒ · 「0.4 켠 상태는 0.7.2 허브로도 돎」 · 「나머지 리포트대로」) · `$W/review-spec-008.md` F-1 · F-11 · `$W/spec-008-fix1-brief.md`(발주서 — 보조). **계약(§4 · §5) 변경 0** — 0.8.0 의 규칙 · 응답 필드는 그대로다. 이 워커는 허브 · DB · 앱을 부르지 않았다 · 시험 파일은 읽기만 했다(`$H` HEAD `d97a9ad` 의 줄 번호).

**쓰는 곳별 영향 — 0.8.0 표를 이 표로 고친다**(0.8.0 표의 나머지 줄 — 시험 앱 B 열 · C 열 · 답 키 · 자체 점검 · REST · DB 판 — 은 그대로다)

| 쓰는 곳 | 지금 부르는 꼴 | 0.8.0 허브에서 |
|---|---|---|
| 앱 상담 0.4 **켠 상태**(SPEC-008) | **목록 꼴만**(다섯 표 · `gold_hash` 마다 한 번) — 맞춤 꼴을 부르지 않는다 | 영향 0. **상담 0.4 켠 상태는 목록 꼴만 써서 0.7.2 허브로도 돈다 — 허브 0.8.0 과 같이 올리는 것이 필수는 아니다**(0.7.2 목록 꼴과 0.8.0 목록 꼴은 머리 `request.abbr` 칸 하나만 다르다 — §4-1 · O-32 · 앱 클라이언트는 `abbr` 을 싣지 않는다) |
| 앱 상담 0.3(앱 `be1c622` — 지금 떠 있는 판) | 턴마다 맞춤 꼴에 **손님 문장**(`walk/front.py:225` · 거둠용 `consult/state.py:272`) | 0.8.0 허브에 붙이면 후보가 사실상 0 이 되어 모든 턴이 입구 고르기로 간다 → **0.3 앱을 0.8.0 허브에 붙이지 않는다**(허브를 먼저 올리면 앱 0.4 도 함께 · 앱 0.4 만 먼저는 된다 — 위 줄) |
| **앱 상담 끈 상태**(`consult_state` = `off` — 0.4 서버 안 · **새 줄**) | 0.1 그대로 `walk()` → `front()` — 맞춤 꼴에 **손님 문장**(`walk/front.py:225-226`). 상담 서버의 허브 주소는 하나다(`config.py:41` `hub_rest_url`) · 끈 대화는 켠 서버에서도 대화 첫 값으로 이어 돈다(`consult/ledger.py:195-201` `state_at_start`) · 기본값 `chat_state = "off"`(`config.py:82`) | **코디 결정 F-1 ⓒ — 상담 0.4 서버는 끈 상태 대화를 새로 열지 않는다**(`chat_state` 기본 `on` · 끈 상태로 시작하는 새 대화 없음 — SPEC-008 CP1 · CP7). 0.4 이전에 시작된 끈 대화는 열면 「옛 판 대화」 로 **읽기만** 한다(새 턴을 막는다 — 막는 화면 문구는 빈칸 · SPEC-008 U8-3). 그래서 0.4 서버에서 맞춤 꼴에 문장을 넣는 길이 없다 — 0.8.0 허브에서 끈 대화의 후보가 0 이 되는 꼴이 생기지 않는다 |

**고칠 · 지울 허브 시험**(검수 F-11 — 0.8.0 이 깨뜨리는 시험을 다 센다 · 줄 번호 = `$H` `d97a9ad` · 「고침」 = 기대를 0.8.0 계약으로 바꿔 남김 · 「지움」 = 대상 규칙이 없어져 지움)

| 파일 | 함수 · 자리 | 왜 깨지나 | 처분 |
|---|---|---|---|
| `backend/tests/test_gold_contract.py` | `test_T3_real_response_fields`(241 ~ 262) | 맞춤 꼴에 **질문 문장**을 넣는다(`resolve(text=q["entry_text"] or q["question"])` · 끝에서 `resolve(text=q["question"])`) · `seen > 0` 단언 — 0.8.0 에서 후보 0 이 될 수 있다 | **고침** — 입력을 `entry_text`(없으면 그 문항 기대 입구의 **이름**)로 · 끝의 `resolve(text=q["question"])` 줄은 이름 입력으로 바꾼다. T27 의 「그대로 통과」 에서 T3 를 뺀 까닭 |
| `backend/tests/test_gold_v07_resolve.py` | T26 함수 전부(`test_T26_keys_equal_independent_build` · `_base_fixture_has_no_keys` · `_abbr_matches_and_covers_last_word` · `_one_word_prefix_no_candidate` · `_no_match_shapes` · `_abbr_inside_full_name_is_covered` · `_short_abbr_inside_long_abbr` · `_part_wins_and_not_repeated` · `_one_key_two_concepts` · `_same_span_part_first` · `_matched_shape_and_order` · `_abbr_off_is_06` · `_abbr_off_base_same_as_on` · `_abbr_invalid` · `_tool_description_and_schema` · `_real_counts_and_37_questions`) | 줄임(NM) · 입력 `abbr` · `matched.how` · `matched.full` · 덮임을 단언한다 | **지움**(파일째) — 0.8.0 T26 의 남는 확인(줄인 글 → 후보 0 · `how` · `full` 없음 · 줄임 열쇠 색인 없음)은 T15 시험 자리에 새로 쓴다 · `_abbr_invalid` 의 뜻(`abbr` → `invalid_argument`)은 T15 로 옮긴다 |
| `backend/tests/test_gold_v07_compat.py` | `test_T27_resolve_abbr_off_06_shape`(79 ~ ) · `test_T27_real_hash_and_06_shape` 의 `resolve(text=q["question"], abbr="off")`(129) | `abbr="off"` 입력(0.8.0 = `invalid_argument`) · 문장 입력의 0.6 꼴 대조 | **고침** — `resolve` 0.6 꼴 대조 함수는 **지움**(T27 이 「`resolve` 맞춤 꼴은 0.6 과 같은 응답이 아니다」 로 이미 뺐다) · `test_T27_real_hash_and_06_shape` 는 `resolve` 줄만 빼고 남긴다 · `test_T27_descriptions_three_sentences`(90)는 `resolve` 설명 문장 수가 바뀌면 그 기대를 T29 문장으로 |
| `backend/tests/test_gold_tools_synthetic.py` | `test_resolve_overlap_all_and_order`(36) · `test_resolve_one_per_entity_longest_span`(43) · `test_T15_resolve_wide_candidates`(64) · `test_T15_covered_only_when_every_occurrence_covered`(83) · 문장을 넣는 그 밖의 `resolve` 단언(36 ~ 97) | 겹침 · 긴 조각 · 넓은 후보 · `covered_by` · 문장 입력 | **지움** 셋(`overlap_all_and_order` · `one_per_entity_longest_span` · `covered_only_when_every_occurrence_covered`) · **고침** 하나(`test_T15_resolve_wide_candidates` → 0.8.0 T15 「정확한 이름」 — 이름 · 별칭 · 띄어쓰기 · 대소문자 = 후보 · 문장 · 조사 붙은 이름 · 일부 · 이어 쓴 글 = 후보 0) · `test_resolve_range_never_drops`(91) · `test_resolve_zero_is_200`(97) · `test_T13_resolve_listing`(102)은 입력이 문장이면 이름으로만 바꾼다 |
| `backend/tests/test_gold_mcp.py` | `test_tool_list`(38)의 44 ~ 45 행(도구 설명에 「부분 문자열」 · 「조사를 떼지 않는다」 단언) | 0.8.0 도구 설명은 그 문장이 없다(§4-1 · T29) | **고침** — 「`text` 는 이름 하나다 — 문장을 넣으면 후보가 0 이다」 문장 있음 · 「부분 문자열」 · 「조사를 떼지 않는다」 · 줄임 문장 없음을 단언(T29) |
| `backend/tests/test_gold_mcp.py` | `SAME` 의 66 행(`resolve` `{"text": "겹침 시술가", "abbr": "off"}`) · `ERRORS` 의 104 행(`abbr` = `x` → 422) · `SAME_V07` 의 112 행(`{"text": "가나 마바사 어때"}` — 문장 · 줄임 꼴) | `abbr` 입력 · 문장 입력 | **고침** — 66 = 이름 하나(`{"text": "겹침"}` 등 · `abbr` 뺌) · 104 = `abbr` 을 주면 0.8.0 의 `invalid_argument`(REST 상태 코드는 §4-0 의 그 오류 꼴 그대로) · 112 = 이름 입력으로 바꾸거나 지움(줄임 꼴 표본이라 대상 규칙이 없다) |
| `backend/tests/test_medallion_repo.py` | `test_dt9_same_memory_index`(87)의 색인 이름 목록(84 행 `"entry_by_abbr"`) · `test_dt9_same_memory_index_v07`(96 ~ 100 — `entry_by_abbr` · `abbr_keys()` 단언) | 줄임 열쇠 색인 · repository 메서드(`abbr_keys` · `entries_by_abbr`)가 두 판에서 없어진다(§5-11 「두 판」) | **고침** — 색인 이름 목록에서 `entry_by_abbr` 를 빼고 · 100 행 단언은 「줄임 열쇠 색인이 없다」 로 바꾼다 · DT10(`test_dt10_tool_responses_equal` · `_v07`)은 0.8.0 응답 꼴로 그대로 돈다 |
| `backend/tests/gold_fixture.py` | 합성 gold(121 ~ 126 — 「겹침」 `norm` 하나에 개념 둘 · 부분 문자열만 같은 항목 — 머리말 5 행) · v07 판 줄임 꼴 표본 | 줄임 열쇠 표본 · 부분 문자열 표본은 0.8.0 규칙에 닿지 않는다 | **고침**(필요한 만큼) — 「겹침」(같은 `norm` 개념 둘 → `ambiguous`)은 0.8.0 T15 에도 쓰이므로 **남긴다** · 줄임 꼴 전용 행은 지워도 되고 남겨도 된다(남기면 「줄인 글 → 후보 0」 확인 재료) — WORK 가 시험 이름별로 적는다 |

- 위 표는 **시험 파일 이름 · 함수 이름 · 처분**만 정한다. 고친 뒤 시험 수(통과 · 지움)는 WORK 의 보고 몫이다. 이 표 밖의 시험에서 맞춤 꼴에 문장을 넣는 곳이 더 나오면 같은 처분(이름 입력으로 고침 · 대상 규칙이 없으면 지움)이다 — WORK 는 `rg -n 'resolve\(' backend/tests` 로 전수를 다시 센다.

| 무엇 | 고친 것 | 어디 |
|---|---|---|
| 쓰는 곳별 영향 | 「앱 상담 끈 상태」 줄을 더함(F-1 ⓒ) · 「0.4 켠 상태는 0.7.2 허브로도 돈다 — 같이 올리는 것이 필수는 아니다」 · 0.8.0 표의 「앱 상담 0.3」 줄에 「0.8.1 에서 고침」 표지 | 변경 기록 0.8.1 · 0.8.0 |
| 시험 | T27 의 「그대로 통과」 에서 T3(문장 입력)를 뺌 · 고칠 · 지울 시험 표 | §9 T27 · 변경 기록 0.8.1 |

### 0.8.0 — 2026-11-18 · `resolve` 맞춤 꼴 축소(정확한 이름 → 코드만) — 부분 일치 · 덮임 · 줄임(NM) 지움

근거: `$W/_RESUME.md` §2 2026-11-18 「상담 입구 결정 표 D-1~D-15 확정」 행의 **D-1**(resolve 목록 꼴 그대로 · 맞춤 꼴은 정확한 이름 → 코드만 · 부분 · 줄임 · 겹침 규칙 지움) · **D-2**(시험 앱 B 열은 허브 0.7.2 옛 판에 묶고 안 고침 — 이번 일 = 상담만) · 같은 날 「허브 resolve = 최소 목록 꼴(입구 목록 출력) · 규칙을 더하지 않는다 · 입력 정리는 채팅(앱) 단에서(0.5 부분 일치 · 0.7 줄임은 앱이 resolve 를 관문으로 쓰느라 덧댄 것)」 행 · `$W/research-input-space.md` §2(지금 시스템 실패 124 턴 가운데 **후보 층 39** — 정답이 resolve 후보에 없음) · `$W/spec-008-brief.md`(발주서 — 보조). 이 워커는 허브 · DB · 앱을 부르지 않았다 — 아래 수는 이 문서의 앞 판과 조사에서 온 것이다.

**규칙 한 줄**: `resolve` 맞춤 꼴은 `text` 의 `norm` 이 `g_entry.norm` 과 **같을 때만** 그 행의 개념을 후보로 낸다. 문장 안에서 이름을 찾지 않는다(0.5.0 의 부분 일치 R2 · 덮임 R7 · 0.7 의 줄임 NM 을 지웠다). **목록 꼴은 그대로다.**

**응답 필드 — 남길 것 · 지울 것**

| 무엇 | 0.7.2 | 0.8.0 |
|---|---|---|
| 입력 `text`(맞춤 꼴) | 질문 문장 그대로 | **이름 하나** — `norm` 이 같은 행만 후보(문장이면 후보 0) |
| 입력 `range` | 정렬 · `in_range` 계산 | 그대로 |
| 입력 `abbr`(`on` \| `off`) | 줄임 일치 켬 · 끔 | **지움** — 주면 `invalid_argument`(O-32) |
| 입력 `tables` · `cursor` · `limit`(목록 꼴) | — | 그대로 |
| `candidates[]` 의 행(`g_entry` 칸 그대로) | — | 그대로 |
| `matched.span` | 맞은 조각 | **남김** — 값 = 그 행의 `norm`(= 입력의 `norm`) |
| `matched.start` | 조각의 첫 자리 | **지움**(늘 0 이다) |
| `matched.covered_by` | 덮은 긴 조각 | **지움**(조각이 하나뿐이다) |
| `matched.how`(`부분` \| `줄임`) · `matched.full` | 0.7 | **지움** |
| `in_range` | — | 그대로 |
| 머리 `ambiguous` | 개념이 2 이상인 조각이 있나 | 그 `norm` 에 개념이 2 이상인가(뜻 같음 — 조각이 하나) |
| 순서 | 긴 조각 먼저 → 표 순서 → 「이름」 먼저 → `gid` | 표 순서 → 「이름」 먼저 → `gid`(`range` 를 주면 `in_range` 가 그 앞 — 그대로) |
| 후보 수 | 문장 안에 든 입구 이름 수(37 문항 1 ~ 7) | 0 또는 그 `norm` 의 개념 수(겹치는 `norm` 99 · 최대 3 개념 — §4-1) |
| 목록 꼴 응답 | — | `candidates[]` · 순서 · `total` · `counts` · 쪽 넘김 **그대로** · 머리 `request.abbr` 칸만 없어진다(O-32) |
| 메모리 색인 | 줄임 열쇠 2,881(§3-1) | **없앰**(`norm` → 행 색인은 그대로) |
| MCP 도구 설명 | 문장 그대로 · 부분 · 덮임 · 줄임 문장 | 「`text` 는 이름 하나 — 문장을 넣으면 후보 0 · 문장에서 찾으려면 목록 꼴」 한 문장으로(T29) |

**쓰는 곳별 영향**

| 쓰는 곳 | 지금 부르는 꼴 | 0.8.0 에서 |
|---|---|---|
| 앱 상담 0.4(SPEC-008) | **목록 꼴만**(다섯 표 · `gold_hash` 마다 한 번) — 맞춤 꼴을 부르지 않는다 | 영향 0. 문장에서 대상을 고르는 일은 앱의 소넷 「이해」 호출이 한다 |
| 앱 상담 0.3(앱 `be1c622` — 지금 떠 있는 판) | 턴마다 맞춤 꼴에 **손님 문장**(`walk/front.py:225` · 거둠용 `consult/state.py:272`) | 0.8.0 허브에 붙이면 후보가 사실상 0 이 되어 모든 턴이 입구 고르기로 간다 → **허브 0.8.0 과 앱 0.4 는 같이 올린다**(허브만 먼저 올리지 않는다) — **0.8.1 에서 고침**: 이 줄의 「같이 올린다」 는 필수가 아니다 · 끈 상태 대화가 빠져 있었다(0.8.1 표) |
| 시험 앱 **B 열**(gold + Jev — `walk.front` ①-1 맞춤 꼴 · 입구 고르기 · 값 고르기의 목록 꼴) | 맞춤 꼴에 질문 문장 | **D-2 — 고치지 않고 허브 0.7.2 옛 판에 묶는다.** 0.7.2 계약의 구현 = `HUB` 커밋 `3a5da4a`(그 뒤 `d97a9ad` 는 데이터 판 — `resolve` 계약은 0.7.2 그대로다). 0.8.0 허브에 붙여 재지 않는다. 어느 커밋 · 어떻게 띄우나는 O-33 |
| 시험 앱 **C 열**(LLM 이 MCP 도구를 스스로 부름) | LLM 이 `resolve` 에 문장 · 낱말을 넣는다(도구 설명이 「질문 문장 그대로」) | 도구 설명이 바뀐다 — 이름 하나만 맞고, 문장에서 찾으려면 목록 꼴을 스스로 불러 골라야 한다. 0.7.2 때의 측정값과 견줘지지 않는다 → B 열과 같은 옛 판에 묶을지는 **O-33**(D-2 는 B 열만 말했다) |
| 답 키 명세(시험 앱 `evalset/key_calls.py:83` `name_to_entry` — 이름 → 입구) | 맞춤 꼴에 **이름 하나** · `matched.span` 이 이름과 같은 후보를 먼저 고른다 | 이름 그대로 넣는 길이라 정확히 맞는 후보는 그대로 나온다 · 부분 일치로 딸려 오던 다른 개념이 없어진다. `matched.span` 은 남는다. 37 명세가 같은 입구를 고르는지는 시험 앱을 다시 돌릴 때 대조(O-33) |
| 앱 허브 클라이언트 자체 점검(`clients/hub_rest.py:266-282`) | 목록 꼴 첫 행의 `text` 로 맞춤 꼴 한 건 · `matched` 의 키를 적는다 | 후보는 나온다(이름 그대로) · 적히는 `matched` 키가 `span` 하나로 준다 |
| 허브 REST `/resolve` · swagger 문서 | — | 입력 `abbr` · 필드 넷이 없어진 대로 |
| DB 판(SPEC-003) | 같은 `GoldMemory` 코드로 줄임 열쇠 색인을 짓는다 · repository 의 줄임 열쇠 메서드(`abbr_keys` · `entries_by_abbr`) | 색인 · 메서드가 두 판에서 함께 없어진다 · 응답 동치 시험(DT10)은 0.8.0 꼴로. SPEC-003 본문의 메서드 수는 WORK 에서 고친다(이번 allowed_paths 밖) |

| 무엇 | 고친 것 | 어디 |
|---|---|---|
| 맞춤 꼴 계약 | 입력 표 · 계산 필드 표 · 불릿(순서 · 겹침 · 후보 0 · 도구 설명) · 줄임 불릿 지움 · 목록 꼴에 「그대로」 한 줄 | **§4-1** |
| 규칙 | R2 = 정확 일치 · R5 고침 · R7 · R9 지움 · R8 문장 맞춤 | **§5-1** |
| NM | 규칙 NM1 ~ NM6 · 셈 블록을 지우고 지운 까닭만 남김 · 「두 판」 문단 한 줄 | **§5-11** |
| 메모리 색인 | 줄임 열쇠 줄 지움 | §3-1 |
| 시험 | T15 고침(정확한 이름) · T26 지움 · T23 · T27 문장 맞춤 · T29 새로(목록 꼴 불변 · 도구 설명) | §9 |
| 열린 것 | O-29 닫힘 · O-4 · U7-3 한 마디 · O-32 · O-33 새로 | §10 |
| 부록 A | 없어진 계산 필드 · 줄임 열쇠 칸 | 부록 A |

- **다른 도구(`scope` · `neighbors` · `facets` · `concern_candidates` · `pair` · `evidence` · `health` · `coverage`)의 계약은 한 글자도 바뀌지 않는다.** gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 그대로(새 입력 0 · 읽는 칸이 준다).
- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① 「정확한 이름」 = `g_entry.norm` 과 같음 — `g_entry` 에는 이름 행과 함께 별칭 · 약어 · 다른 이름 · 의학 용어 행이 있어(§5-1 옛 R9 의 셈 — 별칭 614 · 약어 61 · 다른 이름 46 · 의학 용어 76) **별칭 글자도 정확히 맞으면 후보다**(발주서 「`g_entry.norm` 과 같을 때만」) ② `matched` 는 `span` 하나로 남겼다 — 통째로 없애면 답 키 명세가 읽는 칸이 사라진다 ③ 입력 `abbr` 은 받되 무시하지 않고 **없앴다**(O-32 — 그래서 목록 꼴의 머리 `request` 한 칸이 달라진다) ④ 겹치는 `norm`(99)은 0.7.2 처럼 전부 낸다 — 「겹침 규칙 지움」 은 덮임(`covered_by`)을 지운 것으로 읽었다(같은 글자의 개념 가운데 허브가 하나를 고르지 않는 것은 R6 그대로).
- **0.5.0 · 0.7.0 · 0.7.1 의 변경 기록과 §0 의 그 판 문단은 그때의 계약을 적은 것이라 고치지 않았다** — `resolve` 에 대해서는 이 판이 앞선다.

**따라 고칠 곳(다른 문서 · 다른 사람)** — SPEC-008(상담 0.4 — 이 판과 함께 썼다 · 목록 꼴을 쓰는 쪽) / SPEC-002 §3-1 단계 ①-1 · ①-2(B 열 걷기가 맞춤 꼴에 문장을 넣는다 — D-2 로 옛 판에 묶여 고치지 않는다 · 문서에 「허브 0.7.2 기준」 한 줄은 코디) / SPEC-006 TW8(줄임 후보 — 0.4 에서 켠 상태가 쓰지 않는다 · SPEC-008 §5) / SPEC-003 §5 P1(메서드 수) / 허브 구현 `HUB backend/app/modules/gold/resolve.py` · `memory.py` · `repository.py` · `mcp_server.py` · `swagger_docs/gold.py`(WORK).


### 0.7.2 — 2026-11-17 · SP1 기준 넓힘(물은 부위가 그 고민의 부위 안에 있을 때만 거름)

근거: `$W/_RESUME.md` §2 2026-11-17 「규칙 변경 = 넣음(지금 · SPEC-001 0.7.2 + WORK-013 WP-3)」 행(정본 — 사용자 「응 추천으로 가면 된다」) · `$W/research-concern-site.md` §0-5 · §5-1 · §6(까닭 — 하위 고민에 묶임을 넣으면 윗고민이 HG3 로 뒤집힌다) · `$W/spec-hub-v072-instructions.md`(지시서 — 보조) · 이 워커 재셈(로컬 CSV — 명령 · 결과는 완료 보고).

**규칙 한 줄**: `site` 를 건 `concern_candidates` 는 **물은 부위의 코드가 물은 고민의 `sites[]`(자기 + 하위 고민의 부위) 안에 있을 때만** 거른다(`filter` — HG3). 그 밖은 거르지 않고 표지만 단다(`prefer`). 0.7.1 은 「`sites[]` 가 `[]` 일 때만 `prefer`」 였다.

| 무엇 | 고친 것 | 어디 |
|---|---|---|
| 기준 | 「`sites[]` 가 `[]` 인가」 → 「물은 부위의 코드가 `sites[].site_code` 안에 있는가」 · 부위 입구에 없는 글자 = `prefer` · 물려받은 응답은 물은 고민 기준 그대로 | **§5-11 SP1** · SP6 · 머리 두 문단 · §5-9 HG3-7 · §5-11 CS4 |
| 입력 · 출력 설명 | `site` · `site_mode`(`auto` 의 뜻) · 「0 이면 0」 불릿 | §4-5 |
| 재셈 | 23,140 짝 = `filter` 191 · `prefer` 22,949(0.7.1 8,900 · 14,240) · 바뀌는 8,709 짝(0 행 8,444 → 전부 · 표지 265 짝 971 행) · 0 행 짝 8,449 → 5 · `CON-005` × `SITE-051` 이름 0 → 54 행 · 묶음 15 · 회귀(191 짝 같은 행 · 160 고민 14,240 짝 같은 응답) · 보강 뒤 어림 둘 | §5-11 SP 셈 · §0 |
| 시험 | T28 고침(기준 · 밖 부위 짝 · 실물 수) · T22 · T27 문장 맞춤 | §9 |
| 열린 것 | O-31 ① **닫힘** · ④ 새로(남는 0 5 짝) · O-30 한 마디(갈리는 곳이 는다) | §10 |
| 부록 A | 새 계산 필드 · 새로 읽는 칸 0 | 부록 A 끝 문단 |

- **계약이 바뀌는 곳**: `site` 를 건 `concern_candidates` 의 기본(`auto`) 응답이 **부위가 묶인 100 고민 × 그 고민의 부위가 아닌 부위(8,709 짝)** 에서 넓어진다(`filter` → `prefer` — 행을 안 뺀다). 0.7.1 의 `prefer` 짝(14,240) · 물은 부위가 안에 있는 짝(191) · `site` 없는 조회 · `site_mode` = `filter` · 다른 도구는 그대로다. **필드 · 입력 · 이름 · cursor 서명은 0.7.1 과 같다**(`site_applied` 를 정하는 식만 바뀐다). 0.7.1 은 아직 구현되지 않았으므로(구현된 것은 0.6) WORK-013 은 0.7.0 + 0.7.1 + 0.7.2 를 한 번에 받는다.
- gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 는 그대로다(새 입력 0).
- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① **부위 입구에 없는 글자 = `prefer`** — 결정 문장은 「물은 부위가 그 고민의 부위 안에 있을 때만 거른다」 이고, 입구에 없는 글자는 코드가 없어 「안」 일 수 없다. 0.7.1 에서는 부위가 묶인 고민이면 글자 일치로만 걸렀다(HG3-2). 실물에서 행의 부위 글자 41 종은 전부 부위 입구 이름이라(재셈) 이 갈림은 「행에도 입구에도 없는 글자」 에서만 난다 — 0.7.1 은 0 행 · 0.7.2 는 행 전부 + 표지 0 ② 「안」 = `sites[]` 의 `site_code` **글자 그대로**(`직접` · `하위` 가리지 않음 · 부위 계층으로 넓히지 않음 — CS3 · O-17 과 같게) ③ 물려받은 응답의 기준 = 물은 고민의 `sites[]`(0.7.1 ⑤ 그대로) ④ **`filter` 인데 0 행인 5 짝은 그대로 뒀다**(O-31 ④ — 결정이 「안에 있으면 거름」).
- **변경 기록 0.7.1 의 「SPEC-002 되적기 후보」 가운데 바뀌는 줄**(SPEC-002 는 이 판에서도 건드리지 않았다): #4 의 기대 「부위가 묶인 고민의 다른 부위(0 그대로)」 → **「전부 + 표지」**(0 그대로인 것은 `site_mode` = `filter` 일 때뿐) · 문항 묶음에 「부위가 묶인 고민 + 밖 부위」 꼴을 더한다 / #2(BR6 — 거른 조회 + 안 거른 조회)는 `prefer` 짝이 22,949 로 늘어 「한 조회로 닫는」 경우가 대부분이 된다. #1 · #3 · #5 ~ #7 은 그대로다.

**따라 고칠 곳(다른 문서 · 다른 사람)** — WORK-013(0.2 — 이 판에서 함께 고쳤다: WP-3 판정 · 기존 시험 기대 · 실물 수) / SPEC-006(앱 상담): `site_applied` · `site_prefer` 를 읽는 자리는 그대로다(새 필드 0) — 다만 `prefer` 응답이 「부위 있는 고민」 에서도 나온다는 것 · 얼굴 점을 눌러 부르는 조회는 그 점이 `sites[]` 의 부위라 늘 `filter` 다 / `$W/research-concern-site.md` §5-1 의 「새로 거름이 되는 고민」 표는 0.7.1 기준이다 — 0.7.2 에서는 「그 부위로 물을 때만 거름」 이라 윗고민 뒤집힘이 없다(위 「보강 뒤 어림 ②」) / `_RESUME` §2 11-17 「0.7.1 코디 확인 … O-31 … HG3 그대로 둠(다음 판 후보)」 은 이 판으로 닫혔다(코디).

### 0.7.1 — 2026-11-17 · 0.7.0 검수 고침 + 규칙 SP(부위 없는 고민 + 부위)

근거: `$W/_RESUME.md` §2 2026-11-17 「SPEC-006 U6-1~3 = (a) … ① 규칙(사용자 결정)」 행 · 「A8 화면 구조 … SPEC-001 0.7 U7-1~3 = (a)」 행(정본) · `$W/review-spec-001-v07.md`(0.7.0 검수 — FAIL 0 · WARN 6 · NOTE 8) · `$W/spec-hub-v071-instructions.md`(지시서 — 보조) · 이 워커 재셈(로컬 CSV — 명령 · 결과는 완료 보고).

**검수 지적 → 고친 곳**

| 지적 | 고친 것 | 어디 |
|---|---|---|
| W-1 고민 수 · 최대치 | 243 → **242** · 248 → **247** · 143 → **142** · 139 → **138** · 최대 130(계열 13) → **107(계열 6 · `CON-226`)** · 빈 고민 묶음 63 행(시술 코드 없는 행 23 → 계열 13 · 시술 130)은 따로 적음 | §5-11 DP 「셈 — 고민 수」 · 「셈 — 규모」 · 「빈 고민 묶음」 · §10 U7-1 · O-27 · §9 T24 |
| W-2 `lands` = `procedure` 꼴 | ① 닿은 시술의 계열 묶음 ② `procedures[]` 는 계열의 시술 전부 · 좁힘은 `from[].procedure_codes[]` ③ `unit` = `계열` 그대로 · 계열 없는 시술이면 못 내린 행 · T24 문장 맞춤 | §4-5 `from[].lands` · §5-11 DP2 · §9 T24 |
| W-3 MCP 도구 설명 문장 | `concern_candidates`(계열 단위 묶음) · `resolve`(`줄임` 후보) 한 문장씩 + 시험 | §4-5 불릿 · §4-1 · §9 T24 · T26 |
| W-4 낡은 문장 | 「WORK 전 사용자 결정 = 위 2」 → **0**(U7 셋 · U-3 · U-4 전부 닫힘) | §10 |
| W-5 한 글자 앞 낱말 | 「한 글자 낱말은 줄이지 않고 통째로」 한 꼴로(2,881 이 나오는 꼴) | §5-11 NM1 · NM3 ③ · §9 T26 |
| W-6 줄임 오매칭 근거 | 37 문항 0 과 함께 검수 표본(이름 12 · 3,254 문장의 52 = 1.6% · 어긋나는 꼴 둘)을 적음 · 규칙은 그대로 · T26 합성 한 줄 · 줄임 후보끼리의 덮임 | §5-11 NM4 · 「셈 — 오매칭」 · §10 U7-3 · §9 T26 |
| N-1 `CON-168` 부위 | 닫힘으로 적음(`_RESUME` 가 고쳐졌다) | §5-11 CS |
| N-3 `to_procedure` = `none` | 「두 필드를 뺀다」 하나로 | §4-5 · §5-11 DP8 · §9 T24 |
| N-7 내릴 행 722 가운데 23 | 고민 코드 빈 행이라 도구로는 699 | §5-11 DP 「셈 — 내릴 행」 |
| N-8 순서 | `gid` 글자 순(= 수 순) | §5-11 DP7 |
| N-5 제품 길 | U7-1 에 「제품 길 포함」 한 마디 | §10 U7-1 |
| §2 재셈 표의 단위 | `sites[]` 최대 = 서로 다른 부위 18 · 항목 23 | §5-11 CS 셈 · §4-5 `counts.sites` · O-27 |

- N-2(메뉴 수 — `_RESUME` 의 83 은 행 수 · 패키지는 57) · N-4(`g_entry` 에 `kind` 칸이 없어 앱이 `resolve` 응답만으로 메뉴를 못 가른다) · N-6(SPEC-006 의 「최대 130」)은 **이 문서에서 고칠 것이 없다** — 본문(57 · `g_package.package_kind`)은 맞고, 고칠 곳은 코디 · 앱 writer 몫이다(아래 「따라 고칠 곳」).
- 0.7.0 변경 기록의 「앱이 `sites[]` · `descended[]` 를 읽는 자리(SPEC-004 · SPEC-005)」 는 **SPEC-006** 이 받는다(검수 §4 — LS4 · FD1 · TW8). 0.7.0 기록은 그대로 두고 여기 적는다.

**규칙 SP(사용자 결정 11-17) → 문서 자리**

| 무엇 | 넣은 것 | 어디 |
|---|---|---|
| 부위 없는 고민 + 부위 = 거르지 않음 | `sites[]` = `[]` 이면 행 전부(`site_applied` = `prefer`) · 아니면 HG3 그대로(`filter`) | §4-5 `site` · 불릿 · §5-9 HG3-7 · **§5-11 SP1 · SP2 · SP6** |
| 우선 표시 표지 | 행 `site_prefer`(+ `site_match[]`) · 묶음 `n_site_prefer` · `counts.site_prefer` · 허브는 순서를 안 바꿈(앱이 앞에 둠) | §4-5 출력 · §5-11 SP3 ~ SP5 · 부록 A |
| 되돌려 볼 길 · 도구 설명 | 입력 `site_mode` · 도구 설명 문장 | §4-5 · §5-11 SP7 · SP8 |
| 재셈 | 부위 없는 고민 160(하위 포함 기준 · 자기 기준 175) · 14,240 짝 가운데 0 행 14,008 → 전부 · 표지 행 646 · `CON-048` × `SITE-051` 이름 0 → 105 행(표지 0) · 부위 있는 100 고민 회귀 0 | §5-11 SP 셈 |
| 시험 | T28(새) · T22 · T27 문장 맞춤 | §9 |
| 열린 것 | O-30(이름 · 표지의 뜻) · O-31(한계) | §10 |

- **계약이 바뀌는 곳**: `site` 를 건 `concern_candidates` 응답이 **부위가 묶이지 않은 160 고민에서** 넓어진다(행을 안 뺀다). 부위가 묶인 100 고민 · `site` 없는 조회 · 다른 도구는 필드 둘(`site_applied` · `counts.site_prefer`)이 느는 것 말고 그대로다. 0.7.0 은 아직 구현되지 않았으므로(구현된 것은 0.6) WORK 는 0.7.0 + 0.7.1 을 한 번에 받는다.
- cursor 는 요청에 묶여 있어(§4-0) `request.site_mode` 가 없는 옛 cursor 는 `cursor_invalid` 다(0.7.0 의 `to_procedure` 와 같은 꼴).
- gold 15표 · gold 해시 · 보조 입력 · `aux_hash` 는 그대로다(새 입력 0 — 이미 읽는 `g_indication` 칸과 보조 ③ 뿐).
- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① 「`concern_site` 없는 고민」 을 **자기 + 하위 고민의 묶임이 모두 없는 고민(`sites[]` = `[]` · 160)** 으로 읽었다 — 자기 묶임만 보면(175) 결정이 「HG3 그대로」 라고 한 윗고민 + 부위 꼴(e2e 피드백 4)이 바뀐다 · 지시서의 「160」 과 같다 ② **표지의 뜻을 「`filter` 였다면 남았을 행」 으로 넓혔다** — 결정 문장은 「행 부위 글자 일치」 다. 갈리는 229 행(5 고민)이 0.7.0 에 있던 `site_match[]` 를 잃지 않게 한 것이고 O-30 에 선택지로 남겼다 ③ 표지가 붙은 행을 앞에 두는 것을 **앱**에 둔 것(허브 순서 불변 — 지시서 「앱은 그 행을 앞에 둔다」) ④ 입력 `site_mode` 를 둔 것(`upper` · `descend` · `to_procedure` · `abbr` 과 같은 「옛 응답을 다시 보는 길」) ⑤ 물려받은 응답의 기준을 **물은 고민**으로 둔 것(`sites[]` 의 CS3 과 같게).
- **실물 문장의 결과를 숨기지 않는다**: 결정 행이 든 「볼 + 탄력 저하」 꼴은 규칙 뒤에 시술이 전부(105 행 · 묶음 55) 나오지만 **표지는 0 행**이다 — 그 고민의 행에 그 부위 글자가 없다. 「그 부위 케이스가 앞에」 는 이 꼴에서는 놓을 것이 없다(O-31 ②).

**SPEC-002 되적기 후보**(이 판은 SPEC-001 한 파일만 고쳤다 — 아래는 목록만이고 SPEC-002 는 건드리지 않았다)

| # | SPEC-002 자리 | 되적을 것 |
|---|---|---|
| 1 | §3-1 BR1(「고민 + 부위는 `concern_candidates(concern_code, site)` 한 길」 · 행의 `site_match[]` 를 층 표지와 함께) | 응답 `site_applied` 를 읽는다 — `prefer` 면 **거르지 않은 재료**다: 「그 부위로 좁힌 것」 표지를 붙이지 않고, `site_prefer` = `true` 인 행 · 묶음을 앞에 둔다(같은 걷기 함수) |
| 2 | §3-7 BR6(yes 가 아닌 부위 입구 = 거른 조회 + 안 거른 조회) | `prefer` 면 두 조회의 행이 같다 — 한 조회로 닫고 표지만 읽는다(같은 `gid` 표지 합침 규칙 §7-3 과 부딪히지 않게) |
| 3 | §9-5 전체 답 키 뽑기(`calls[]` 로 허브를 부르는 키 함수) | `site` 를 건 `concern_candidates` 호출의 키 행 = 응답 그대로(`prefer` 면 그 고민의 행 전부) — **걷기와 같은 함수 · 같은 `site_mode` 기본값**을 써야 키와 B · C 가 같은 폭을 본다 |
| 4 | §9-3d 구멍 묶음 「고민 + 부위(HG3)」 (iv) 「묶임이 없는 (고민, 부위)」 | 기대가 갈린다 — 부위가 묶인 고민의 다른 부위(0 그대로) / 부위가 묶이지 않은 고민 + 부위(전부 + 표지). 뒤 꼴 문항 · 이마 꼴 회귀 문항을 묶음에 더한다(_RESUME §2 11-17 「시험(부위 없는 고민+부위 · 이마 회귀)」) |
| 5 | §4 틀린 말 검사 · §6-3 답 프롬프트 원칙 | `site_prefer` = `false` 인 행을 「그 부위에 하는 것」 으로 말하지 않는다(그 고민에 하는 것으로 말한다) — 검사 · 프롬프트 한 줄 |
| 6 | §7-3 trace | 조회마다 `site_applied` · `counts.site_prefer` 를 남긴다 |
| 7 | §2-4 C 의 도구 | C 열은 도구 설명 문장(§4-5 ① ②)으로 같은 뜻을 받는다 — 도구 목록 설명 갱신 |

**따라 고칠 곳(다른 문서 · 다른 사람)** — SPEC-006(앱 상담): 리스트에서 `site_prefer` 묶음을 앞에 · 「고민당 최대 130 시술」 → 107(LS4-1 — 검수 N-6) · 메뉴 여부는 `g_package.package_kind` 에서(검수 N-4) / SPEC-003(DB 판): §7 DT10 동치 시험이 0.7.1 필드까지 · §5 P1 메서드 수(늘면) / `_RESUME` §1 「수정 2 목록」 00 의 「243」 → 242 · 9 의 「57 패키지(행 83)」 확인(검수 W-1 · N-2 — 코디).

### 0.7.0 — 2026-11-17 · 시술로 내려가기(DP) · 고민 부위(CS) · 이름 맞춤 보강(NM)

근거: _RESUME §2 11-17 「얼굴 점 = 대화에서 나온 고민 부위 · 점을 누르면 그 고민의 관련 시술 리스트 · 메뉴는 시술 아님」 행 · `$W/_RESUME.md` §1 「수정 2 목록」 00 · 2 · 6 · 9 · `$W/spec-hub-v07-instructions.md`(H1 · H2 · H3 — 보조 근거) · 이 워커 재셈(로컬 CSV).

| 무엇 | 바뀐 것 | 어디 |
|---|---|---|
| DP 시술로 내려가기(지시 H1) | `concern_candidates` 에 쪽 밖 목록 `descended[]`(계열 단위 묶음 · 경로) · `counts.descended` · 입력 `to_procedure` | §4-5 · §5-11 DP · §9 T24 |
| CS 고민 부위(지시 H2) | `concern_candidates` 에 쪽 밖 목록 `sites[]` · `counts.sites` | §4-5 · §5-11 CS · §9 T25 |
| NM 줄임 일치(지시 H3) | `resolve` 맞춤 꼴에 줄임 열쇠 맞춤 · `matched.how` · `matched.full` · 입력 `abbr` · 덮임에 줄임 조각 포함 | §3-1 · §4-1 · §5-1 R9 · §5-11 NM · §9 T26 |
| 기존 필드 불변 · 두 판 | 새 시험 T27 · 새 입력 0(gold 해시 · `aux_hash` 그대로) | §0 · §5-11 끝 · §9 T27 |
| 사용자 결정 | U7-1 ~ U7-3(추천 전부 (a)) | §10 |
| 열린 것 | O-27 ~ O-29 | §10 |
| 부록 A | 「0.7」 읽는 칸 다섯 줄 · 계산 필드 문단 | 부록 A |

- **계약 변경은 더하기뿐이다**: 0.6 의 필드 · 순서 · `total` · 오류는 그대로다. 예외 하나 — NM4: 줄임 조각 안에 통째로 든 `부분` 후보의 `matched.covered_by` 가 `null` 에서 그 줄임 조각으로 바뀐다(`abbr` = `off` 면 0.6 그대로 · 37 문항에서는 0 건).
- cursor 는 요청에 묶여 있어(§4-0) 0.6 에서 받은 `concern_candidates` cursor 는 `request.to_procedure` 가 없어 `cursor_invalid` 다(다시 첫 쪽부터).
- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① 지시서의 「41」 은 고민 자신의 행 기준 · 제품 길을 뺀 셈이다 — 본문은 지시서 문장(「패키지 · 메뉴 · 계열 · 제품」)대로 제품 길을 넣어 43(같은 기준) · 도구 응답 단위로는 41 / 41 이다 ② 내린 시술을 `groups` 에 넣지 않고 따로 목록으로 둔 것은 「계열 단위 표지」 와 「기존 필드를 바꾸지 않음」 을 함께 지키려는 꼴이다 ③ `sites[]` 를 `concern_candidates` 머리에 둔 것은 지시서 H2 그대로이고, 하위 고민 포함은 본문 제안(U7-2) ④ H3 의 「별칭 · 부분 일치 · 띄어쓰기」 가운데 별칭 · 띄어쓰기는 이미 되는 것이라 새 규칙은 줄임 하나다.
- SPEC-003(DB 판) · SPEC-002 · SPEC-004 · SPEC-005 는 고치지 않았다(이번 allowed_paths = 이 파일 하나). 따라 고칠 곳: SPEC-003 §5 P1 의 메서드 수(늘면) · 앱이 `sites[]` · `descended[]` 를 읽는 자리(SPEC-004 · SPEC-005 — 다른 writer).

### 0.6.0 — 2026-11-17 · 수 고침 + 구현 되적기(계약 변경 없음)

근거: `$W/_RESUME.md` §5 2026-11-17 「허브 0.5.2 완료」 · 「허브 0.5.2 코드 검수 PASS」 · 「37 batch 끝」 줄 · `$W/impl-v052-hub-report.md` · `$W/app-v052-report.md` 미결 2 · 3 · `$W/spec-v06-instructions.md` C(지시서 — 보조). 앱 쪽은 SPEC-002 0.6.0.

| 무엇 | 고친 것 | 어디 |
|---|---|---|
| HG1 「한 단 9 · 두 단 4」 | 「단」 = silver 조상 사슬 길이임을 밝힘 · 응답 `steps` 는 실물 13 전부 1 | §5-9 HG1 「셈 — 몇 단」 |
| 케이스 끝 `g_pair` 129 | → 100(서로 다른 `gid`) · 계열마다 더하면 104 | §5-9 HG2 「셈 — 그 자손이 가진 자기 행」 |
| 97 짝 행 합 1,700 | → 1,722 | §5-9 HG3 「셈 — 규모」 |
| 구현 때 정한 것 10 | R1 ~ R10 | §5-10(새 절) |
| Q12 키 +4 | 제품의 하위 제품 길 = 자손(R10) | §5-10 |
| O-23 · O-26 | 상태 머리말(0.6) — O-26 의 둘째 선택지는 SPEC-002 BR5 · U-8 로 | §10 |

- 도구 9 의 입력 · 출력 · 오류 · 부록 A 는 한 글자도 바꾸지 않았다. 사용자가 정할 것은 이 문서에 없다(SPEC-002 §11 U-5 ~ U-8).

### 0.5.2 — 2026-11-17 · 구멍 셋 규칙(HG1 ~ HG3) + 구현 결정 되적기

근거: `$W/_RESUME.md` §2 2026-11-17 「답 키 검토」 행 · §1 「허브 묶음 발주」 줄 · e2e 피드백 4 · §5 11-16 「허브 v05 완료」 줄(정본) · `$W/spec-v052-instructions.md`(지시서 — 보조) · `$W/app-key-fix1-report.md` · `$W/review-code-v05-hub.md` · `$W/WORK-005-hub-v05.md` §9. 앱 쪽은 SPEC-002 0.5.2.

**결정 · 지시 → 문서 자리**

| 무엇 | 넣은 것 | 어디 |
|---|---|---|
| HG1 고민 → 윗고민 물려받음(지시 A · H1) | 행 0 일 때 가장 가까운 윗고민의 행 · `inherited_from` · `hier.match` = `상위` · `upper` 입력 · `coverage` 고민 `indication.inherited` | §4-5(입력 · 출력 · 불릿) · §4-9 `inherited` · §5-5 H5 · H6 · §5-8 · **§5-9 HG1** · §9 T20 · Q10 줄 · U-3 · O-25 |
| HG2 하위 = 자손 전부(지시 A · H2) | `g_scope` 하위 role 을 끝까지 · `layer.depth` · `layer.via[]` · 적용 자리 넷 · `descend` 입력 | §3-1 · §4-2 · §4-4 `roles` · §4-6 규칙 1 · §4-9 `lower` · §5-3 S6 · §5-8 `lineup` · **§5-9 HG2** · §9 T21 · Q12 줄 · O-21(결정됨) · O-26 |
| HG3 고민 + 부위 → `concern_site`(지시 A · H3) | `site` 맞춤 = 글자 일치 ∪ 묶인 고민 · `site_match[]` · 보조 입력 ③(제안 — U-4) | §2-1(표 · X7) · §2-2 · §2-3 4 · §3-1 · §4-5 · **§5-9 HG3** · §9 T22 · 부록 A · U-4 · O-24 |
| 상품 셈 식(지시 B) | `coverage` 의 `offer` = §4-4 맞춤 규칙 그대로 → 자기 0 · 하위 1 이상 = 계열 17 · 시술 0 · 제품 7(0.5.1 의 15 · 11 은 `item_*` 식) · §4-4 는 그대로 | §4-9 수 · 「상품 셈 식」 불릿 · §9 T23 |
| 제품 offer `inherited` = 0(지시 B) | `null` 이 아니라 `0` | §4-9 `inherited` 줄 · T23 |
| A-1 `covered_by`(지시 B) | 같은 조각이 여러 번이면 나온 자리가 **전부** 덮였을 때만 | §4-1 `matched.covered_by` · T23 |
| 구현에서 정해진 그 밖(허브 검수 v05 N-5 · N-8 · WORK-005 A-2 ~ A-5) | `pair` 종류의 `lower` 는 하위 제품 없음 · `integrity.scope_duplicate_subject_holder_rows` · `lineup.lower_holders` · 같은 노드 두 번 · `kinds[]` 순서 · 빈 `norm` | §4-9 · §4-8 · O-22 ① (결정됨) |
| 화면 말 「적응」 → 「어디에 쓰나」(지시 B) | `indication` 의 사람이 읽는 이름 | §5-8 표 · 아래 불릿 |
| Q33 답 키 입구(답 키 검토) | 상품을 입구(값 쪽)로 | §9 문항별 기대 Q33 줄 |

- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다): ① 지시서는 HG2 를 「SPEC 『하위 = 자손 전부』 를 허브가 어김」 으로 적었으나, 0.5.1 본문(§5-3 S6 · O-21 (a))은 `g_scope` 층을 **한 단**으로 명시했고 허브 구현은 그 계약대로였다(「자손 전부」 는 §4-4 의 부작용 · 조건 계층 문장이다). 그래서 0.5.2 는 **계약을 바꾼 것**으로 적었다(O-21 결정됨) ② HG1 의 「대상 54 고민」 은 **묶음 0** 기준이고 **행 0** 기준은 13 이다 — 본문은 13(U-3) ③ HG2 에서 「`자기` · `물려받음` 으로 닿은 holder 에서는 내려가지 않는다」(HG2-2) ④ HG3 을 `resolve` 가 아니라 `concern_candidates` 에서 합친 것(O-24) ⑤ 묶인 고민 자신 + 그 부위에서 0 행이 되던 꼴(95 짝 중 58)을 HG3 에 함께 넣은 것.
- gold 15표 · gold 해시는 그대로다. 바뀌는 것: `aux_hash`(보조 입력 ③ — U-4 (a) 일 때) · `scope` · `facets` · `pair` · `coverage` · `concern_candidates` 의 응답(넓어지는 쪽). **WORK 전 사용자 결정 = 2(U-3 · U-4 — 추천 있음).**
- 고치지 않은 것: §4-9 끝 불릿들 · §5-3 S6 의 `lower` 수(0.5.1 · 한 단 기준)는 그대로 두고 「한 단 기준」 임을 적었다 — HG2 뒤의 수는 WORK 에서 T16 으로 다시 센다.


### 0.5.1 — 2026-11-16 · 0.5.0 검수 반영

근거: `$W/_RESUME.md` §2 2026-11-16 「SPEC 0.5.0 검수 뒤 결정 3 = 추천」 행(정본) · `$W/review-spec-v05.md`(검수 v05 — SPEC-001 은 WARN 2 · NOTE 2 + SPEC-002 F-1 의 허브 쪽) · `$W/spec-v051-instructions.md`. 앱 쪽은 SPEC-002 0.5.1.

| 지적 · 결정 | 고친 것 | 어디 |
|---|---|---|
| 결정 3 ① · F-1 · N-4 — `overview` / `mechanism` 은 칸 값 있는 행 · RQ1 과 `coverage` 는 같은 함수 | `self` · `lower` · `inherited` 를 그 종류의 칸에 값이 있는 profile 행으로 · `overview` 의 개요 칸 정의 · RQ1 과 같은 함수임을 불변식 옆에 · `inherited` 만 있는 대상의 규모(원리 314 / 315 등) | §4-9 셈 표 · 불릿 · §5-8 `overview` 행 · 불릿 · §9 T16 · 부록 A(개요 칸 줄) |
| W-4 — C 열이 하위 층 행을 구조적으로 못 읽음 → (a) | 도구 설명에 「하위 층의 자기 행은 `roles` 에 하위 role 을 줘야 나온다」 — 계약 · 기본값은 그대로 | §4-4 `roles` · §5-3 S2 · §9 T19 |
| W-5 — 적응 셈 | 수는 그대로(37 = 시술 33 · 제품 3 · 계열 1 / 34)이고 **세는 식**을 밝힘 — `concern_match` = 직접 인 행(허브 `facets` indication 의 맞춤). 검수의 35 · 32 는 펼침 행까지 넣은 값 | §4-9 「세는 식」 불릿 |
| W-7 — semantic-map §5 를 바꾸는 자리 | 바꿔 읽는 자리 셋((가) 「하위」 칸 (나) 「상품 질문에서만 하위 제품 상품」 불릿 (다) 「물려받음 = 이 대상에 적용」 과 RQ1) + 「그 셋에서는 이 문서가 앞선다」 | §5 머리 · §5-3 S5 |
| W-8 — 한 단으로 놓치는 수 | 두 단 아래 계열 상품 2 · 「제품 경유」 케이스 적응 80 · 효과 115 · 부작용 97(입구 있는 케이스 8 · 14 · 5) — 추천 (a) 그대로 | §5-3 S6 · O-21 |

- N-5(셈을 새 도구로 · 종류 14 · `matched.particle` 폐기)는 「맞게 놓였다」 라 고치지 않았다.
- 도구 9 의 입력 · 출력 필드 · gold 15표 · gold 해시 · 보조 입력은 그대로다(바뀐 것은 `coverage` 의 `overview` 세는 식 한 줄과 도구 설명 문장). **WORK 전 사용자 결정 = 0.**


### 0.5.0 — 2026-11-16 · 길 찾기 재설계 + 구현 결정 되적기

근거: `$W/_RESUME.md` §2 2026-11-16 「길 찾기 재설계 진행」 행(정본) · 같은 표의 「허브 검수 뒤」 · 「WORK 0.2.0 수정 뒤」 · 「앱 검수 뒤」 행 · §1 e2e 피드백 3 · 4 · `$W/spec-v05-instructions.md`. 앱 쪽 흐름은 SPEC-002 0.5.0.

| 무엇 | 바뀐 것 | 어디 | 근거 |
|---|---|---|---|
| 넓은 후보 | `resolve` 맞춤 꼴 = 문장 `norm` 안의 입구 이름 **부분 일치 전부** · 조사 목록 폐기 · 긴 것 먼저이되 짧은 것도 남김(`matched.covered_by`) · `matched.particle` 없앰 · `matched.start` | §4-1 · §5-1 R2 · R3 · R7 · R8 · §9 T15 · O-4(결정됨) | 「길 찾기 재설계 진행」 · e2e 피드백 4 · 「앱 검수 뒤」 F-1 |
| 정보 종류 셈 | 새 도구 `coverage`(도구 9) — 후보 × 정보 종류 14 × 층(자기 · 하위 · 물려받음)의 행 수 · 정보 종류 표 | §4-0 · §4-9 · §5-8 · §9 T16 · 부록 A · O-19 · O-20 | 「길 찾기 재설계 진행」(「후보마다 행 수 셈」) — 도구 꼴 · 종류 나눔은 제안 |
| 하위 층 자기 행 | 앱이 「하위 *」 role 을 명시해 부른다 — 허브 계약 · 기본값은 그대로. semantic-map §5 의 「하위는 표시만」 을 「하위도 읽고 층을 밝힘 · 일반화 금지」 로 | §4-4 `roles` · §5-2 표 · §5-3 S5 · S6 · §9 T19 · O-21 | 「길 찾기 재설계 진행」 · e2e 피드백 3 |
| 되적기 — 제품 상품 role | 제품 노드 `facets` offer 기본 role = `자기` · `하위 제품` · `counts.distinct_rows` | §4-0 · §4-4 · §5-2 상품 행 · §9 T17 | 「허브 검수 뒤」(허브 검수 W-1) |
| 되적기 — N1-1 | `pair` 에 `b` 없이 `package_kinds` = `a` 쪽과 항목이 겹치는 패키지 전부 | §4-6 · §9 T18 | 「WORK 0.2.0 수정 뒤」(N1-1 = 제안 (a)) |
| 되적기 — `request` 의 `null` | 기본값이 「전부」 인 입력은 `null` = 전부 | §4-0 응답 머리 | 허브 검수 N-3 |

- **끌어낸 것**(다르게 읽을 수 있어 따로 밝힌다 — 전부 제안 · §10): ① 셈을 **새 도구**로 둔 것(O-19 — 지시서는 「새 도구 또는 resolve 확장」 을 열어 두었다) ② 정보 종류를 **14 로 나눈 것**(O-20 — 지시서의 열거를 gold 표 · `pair` 갈래에 맞춰 나눴다) ③ 하위를 `g_scope` **한 단**으로 둔 것(O-21) ④ `matched.particle` 을 없앤 것(부분 일치에는 뗀 조사가 없다 — 응답 필드가 하나 준다).
- gold 15표 · gold 해시 · 보조 입력 · 0.4.1 의 여덟 도구 입력은 그대로다(`resolve` 의 맞춤 규칙과 `matched` 필드만 바뀜). **WORK 전 사용자 결정 = 0.**


### 0.4.1 — 2026-11-16 · 수정 4회차(문구 고침)

근거: `$W/review-spec-001-002-r4.md`(재검수 3 — SPEC-001 PASS · NOTE 2) · `$W/_RESUME.md` §2 2026-11-16 「재검수 2(r3) §5 결정 = 추천」 행 · `$W/spec-fix4-instructions.md`. **결정은 새로 만들지 않았다 — 문구 고침이다.** 본문 줄 수는 0.4.0 과 같다(아래 줄 번호는 0.4.0 · 0.4.1 에 같이 선다). 도구 8 · 부록 A · 규칙 · 시험 번호는 그대로다.

| 지적 | 고친 것 | 고친 곳(SPEC-001:줄) |
|---|---|---|
| 재검수3 N-2 | §5-2 부위·고민 행에 「(앱 B 가 폭에 더함) `groups` 후보마다 `facets` profile」 · role 칸에 그 호출의 role(`자기` · `물려받음` — 기본값). 허브 도구 계약은 그대로다 | 557 |
| 재검수3 N-6 | O-17 에 ⑤ `concern_candidates` 의 `site` 필터도 같은 한계(정확 일치) · 셈(silver `site` 89 중 부모 있는 것 21) | 752 |
| 근거 표기 | 본문의 「지시 3 의 1 A-2 · 4 · 6」 → `_RESUME §2 11-16 「재검수 2(r3) §5 결정」`(A-2 · 시작 길 추가 · §5 B = 승인). 지시서의 글귀를 그대로 든 자리만 지시 3 을 보조 근거로 곁에 남김 · frontmatter · 근거 표기 줄 | 18 · 19 · 24 · 37 · 48 · 227 · 319 · 398 · 424 · 545 · 567 · 569 · 610 · 727 · 745 · 747 · 751 |

- 열린 것의 상태는 0.4.0 과 같다. **WORK 전 사용자 결정 = 0.**

### 0.4.0 — 2026-11-16 · 수정 3회차

근거: `$W/review-spec-001-002-r3.md`(재검수 2 — FAIL 0 · WARN 6 · NOTE 8 · §5 WORK 전 결정 목록) · `$W/_RESUME.md` §2 2026-11-16 맨 위 다섯 행(「테스트 ≠ 상담」 · 「안전 정보를 처음부터 붙이지 않는다」 · 「흐름(사용자 제안 채택)」 · 「원칙」 · 「재검수(r2) 뒤 결정 2」) · `$W/spec-fix3-instructions.md`(재검수 2 뒤 사용자 결정 = 추천 — 「지시 3」). 줄 번호는 이 판(0.4.0) 기준이다.

| 지적 · 결정 | 고친 것 | 고친 곳(SPEC-001:줄) |
|---|---|---|
| 지시 3 의 1 A-2(옛 O-10) | 상품 이름 부분 일치 = `facets` offer 의 `offer_name_contains`(`norm` 부분 일치 · `node` 대신) · 시험 T14 · Q33 의 길 · 열린 것 「결정됨」 | 375 · 424 · 698 · 745 |
| 지시 3 의 4(시작 길 — 허브 쪽 ①) | **속성 쪽 시작** — 재료 · 방법 · 해부 · 부위 코드로 시작해 그 칸을 가진 행(대상)을 전부. 맞춤 칸 표(헤더 전수) · 맞추는 법 · `attr` · 「있음」 기준 · 색인 · 규칙 A1 ~ A6 · 시험 T12 · 부록 A 일곱 줄 | 398 · 240 · 227 · 181 · 610 · 696 · 780 |
| 지시 3 의 4(시작 길 — 허브 쪽 ②) | **입구 목록** — `resolve` 목록 꼴(`text` 없이 `range` · `tables` · 쪽 넘김) · 허브는 고르지 않고 비슷함 계산도 안 함 · R5 · 시험 T13 · 입구 개념 수 | 319 · 301 · 545 · 697 · 567 |
| 재검수2 X-2(WARN) | 쪽 밖 목록 — 「한도 둠」 선택지를 뺌 · 「한도 없음(통째로) / 커지면 쪽 넘김 대상으로 옮김」 · 본문에 「자르는 한도는 없다」 | 218 · 741 |
| 재검수2 N-8 · §5 B-1 | O-12(오류 코드 · REST 상태 · cursor 를 build 에 묶음 · `aux_hash` · `hier` 기본값 …) 상태 = 「승인됨 — 제안 그대로 시작」 | 747 |
| 지시 3 의 7 | 「상태」 칸에 「승인됨」 · 「뒤 단계에서 사용자 확인」 을 더하고 「사용자 결정 대기」 를 없앰 · 「WORK 전 사용자 결정 = 0」 한 줄 · 새 열린 것 O-16 · O-17 · O-18 | 727 · 732 · 751 · 752 · 753 |
| 요약 · 머리 | 0.4.0 요약 한 불릿 · frontmatter(title · version · decisions · sources) · 근거 표기에 `재검수2` · `지시 3` | 48 · 37 |

- **도구 수는 8 그대로다.** 늘어난 것은 입력 셋(`facets.node` 의 속성 코드 · `facets.offer_name_contains` · `resolve` 의 목록 꼴 `tables` · `cursor` · `limit`)과 계산 필드 하나(`attr`) · 머리 셈(`counts.by_column` · `counts.subjects` · `counts.entities`)이다. gold 15표 · gold 해시 · 보조 입력 · 0.3.0 까지의 도구 입력 · 행 필드는 바뀌지 않았다.
- 결정을 새로 만들지 않았다. 지시 3 이 정한 것 = 「재료 · 방법 · 해부 · 부위 코드로 시작하는 결정론 길 — 그 칸을 가진 대상을 전부」 · 「`offer_name` 부분 일치 필터」 · 「resolve 0 이면 범위의 입구 목록을 후보로」 까지다. 그 밖(어느 도구 입력으로 받나 · 맞추는 법 · 필드 이름 · 계층을 안 넓힘)은 「제안」 으로 적고 O-5 · O-16 · O-17 · O-18 에 남겼다.
- 안전 정보 강제 첨부 grep: 이 문서에 「질문이 안 물은 금기 · 부작용을 붙인다」 성격의 규칙 · 필수 facet 은 **0** 이다 — 허브는 부르는 쪽이 고른 facet 의 행만 낸다(§4-4 · §5-4 V4). 「hard gate 가 볼 칸을 거르지 않고 낸다」 는 틀린 말을 막는 재료를 빼지 않는다는 뜻이며 그대로 둔다.
- 남은 열린 것(상태별): 승인됨 — O-12 / 1회차 trace 뒤 — O-6 · O-15 · O-17 · (O-14 의 holder 확대) / 구현 때 정함 — O-3(로컬) · O-4 · O-5 · O-7(로컬) · O-9 · O-16 · O-18 / 뒤 단계에서 사용자 확인(stg) — O-3 · O-7 의 stg 쪽 · O-8 · O-11. **WORK 전 사용자 결정 = 0.**

### 0.3.0 — 2026-11-16 · 수정 2회차

근거: `$W/review-spec-001-002-r2.md`(재검수 — FAIL 0 · WARN 6 · NOTE 9) · `$W/_RESUME.md` §2 2026-11-16 「재검수(r2) 뒤 결정 2」(O-13 · O-14 = 추천 · 지적의 고칠 방향 = 리포트 첫 선택지) · 같은 표 「원칙: 질문에 빠지는 정보가 있으면 안 된다」(`$W/spec-fix2-addendum.md`). 줄 번호는 이 판(0.3.0) 기준이다.

| 지적 · 결정 | 고친 것 | 고친 곳(SPEC-001:줄) |
|---|---|---|
| 결정(O-13) | 부작용 · 조건의 「하위」 = 자손 전부 — 본문에 결정 근거(금기 빠짐 = 안전 · 37 안 차이 0) · 열린 것 표 「결정됨」 · T9 에 손자 코드 행 | 390 · 627 · 676 |
| 결정(O-14) | `ledger_check[]` 대조 범위 = 요청 코드 + 상품 그대로 · holder 확대는 1회차 trace 뒤로 명시 · 열린 것 표 「결정됨」 | 255 · 677 |
| R-1(WARN) | O-14 숫자를 서로 다른 코드 기준으로 — 218 개 중 제품 161(고민 24 · 상품 18 · 시술 11 · 케이스 2 · 효과 2) · (행, 코드) 쌍 273 중 213 은 단위를 밝혀 따로 | 677 |
| R-2(WARN) | `ledger_check[]` 항목 순서 = `on`(`request` → `rows`) → `code` · 겹치면 둘 다 낸다((`code`, `on`) 유일) · T10 에 순서 · 겹침 | 251 · 252 · 628 |
| R-3(NOTE) | O-13 근거에 「37 문항 안 차이 0」 · 조건 + 77 행은 전부 금기 행 | 390 · 676 |
| R-4(NOTE) | `health.files[]` 에 `questions.csv` 를 `kind` = `hash_only` 로 — `files[]` 만으로 `gold_hash` 를 다시 셀 수 있게 · T1 · O-3 · 부록 A 한 줄 | 478 · 480 · 619 · 666 · 713 |
| R-5(NOTE) | 효과 계층은 펼치지 않음을 본문 한 줄 + 열린 것 O-15 | 391 · 678 |
| 사용자 원칙 11-16 | 「폭은 빠짐없이」 의 허브 쪽 — `limit` 은 쪽 크기이지 상한이 아니다 · 허브에 상위 N · 점수로 빼는 입력이 없다 · 요약 · O-6 | 45 · 260 · 669 |
| 지시서 4 | 열린 것 표에 「상태」 칸(결정됨 / 사용자 결정 대기 / 1회차 trace 뒤 / 구현 때 정함) | 653 · 662 |

- 결정을 새로 만들지 않았다. 지적의 고칠 방향이 둘이면 첫 선택지로 썼다(R-1 = 서로 다른 코드 기준 · R-2 = `on` → `code` · 둘 다 낸다 · R-4 = `hash_only` 표지).
- gold 15표 · gold 해시 · 도구 8 의 입력 · 행 필드는 바뀌지 않았다. 바뀐 응답 꼴은 `ledger_check[]` 의 순서 · 겹침 규칙과 `health.files[]` 의 한 줄(`hash_only`)뿐이다.
- 남은 열린 것(상태별): 사용자 결정 대기 — O-8 · O-10 · O-11 · (O-3 · O-7 의 stg 쪽) / 1회차 trace 뒤 — O-6 · O-15 · (O-14 의 holder 확대) / 구현 때 정함 — O-3 · O-4 · O-5 · O-7(로컬) · O-9 · O-12.

### 0.2.0 — 2026-11-16 · 수정 1회차

근거: `$W/review-spec-001-002.md`(검수 — FAIL 1 · WARN 11 · NOTE 10) · `$W/_RESUME.md` §2 2026-11-16 「검수 뒤 결정 4」(사용자 결정 4 + SPEC-002 O-3 · O-4 · O-6 · O-12 · O-13 · O-14 추천대로 + 검수 고칠 방향 추천대로). 줄 번호는 이 판(0.2.0) 기준이다.

| 지적 · 결정 | 고친 것 | 고친 곳(SPEC-001:줄) |
|---|---|---|
| 결정 ② | SPEC-001 O-1 → 보조 입력 ① (silver `concern` · `adverse` · `condition` 의 `code` · `parent_code`) — 입력 · env · 해시 · 색인 · `facets.hier` · 규칙 · 시험 | 93 · 116 · 130 · 173 · 374 · 526 · 617 · 645 |
| 결정 ②(쓰는 곳 전수) | 계층을 쓰는 도구 = `facets` 세 자리뿐 · `concern_candidates` · `pair` 는 안 씀을 명시(gold-build grep: `:319-325 · 359 · 734 · 860 · 921` · 패키지 맞춤 `:814-823`) | 382 · 408 · 434 · 534 |
| 결정 ③ | SPEC-001 O-2 → 보조 입력 ② (원장 확인 목록 id · 코드) · 응답 `ledger_check[]` 꼴 · 대조 범위 · 규칙 · 시험 | 94 · 106 · 117 · 174 · 234 · 536 · 618 · 646 |
| W-7 | 「있음」 기준 — 값은 `g_entry` 색인 · 대상 · 패키지는 `g_scope` · 있음 + 행 0 = `200` · `total: 0` | 214 · 262 · 393 · 619 · 628 |
| W-8 | `total` 단위를 도구마다 표로 · 쪽 밖 목록은 첫 쪽에만 · T6 문구 | 198 · 211 · 395 · 453 · 614 · 650 |
| W-9 | 표시 없던 정책 5 를 「제안」 으로 표시 + §10 O-12 「제안 모음」 | 118 · 131 · 132 · 253 · 257 · 656 |
| W-10 | `graph_main.py` 인용 줄 `:31` → `:30` | 570 |
| W-11 | 「D1」 꼬리표 → 「stg」 행 · 브리프 §2 D1 | 74 |
| N-6 | `gold-build.py:634` → `:633-634`(두 곳) | 299 · 485 |
| N-7 | `filters` 뜻 칸 — 예시와 「해당 없음」 을 나눠 적음 | 350 |
| N-8 | `neighbors` 의 노드 쪽 `evidence_kind` 는 싣지 않음을 한 줄로 | 335 |
| N-9 | 계층 근거 — 옛 틀 인용을 근거로 · 프로필 규약은 「같은 꼴」 임을 밝힘 | 144 |
| N-10 | `facets` 값 쪽 — `roles` 무시 · `layer` 없음 | 349 · 354 |
| W-3(허브 쪽) | 부작용 범위에 값 쪽 시작을 더해 SPEC-002 §3-2 표와 같게 | 497 · 504 |
| F-1(허브 쪽) | T4 — `gold_pointers` 는 표본 · 「표본 ⊂ 전체 행」 을 보는 시험 | 612 |
| 지시서 4 | 새로 열린 것 — O-13(「하위」 가 몇 단인가) · O-14(`ledger_check[]` 대조 범위) | 657 · 658 |

- 결정을 새로 만들지 않았다. 결정 · 조사에 값이 없는 것은 「제안」 으로 적고 O-12 에 모았다.
- gold 15표 · gold 해시는 바뀌지 않는다. 0.1.0 의 「값 쪽 조회는 코드 정확 일치만」 은 `facets.hier` = `exact` 로 남아 있다.
