# 발주서 — gold 설계안 + 시맨틱 매핑 + 질문 시범 · silver 별칭 정리 3

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub silver 55표(① 사전 · ② 시술 138 · 케이스 268 · ③ 관계 20표 · 상품 8표)가 통합 검사 PASS 로 완성됐다. 다음은 gold 와 시맨틱 레이어다. 정의(`../_RESUME.md` 「목표 참고 문서 §1~5」 — 반드시 읽을 것):
- **골드** = 특정 서비스 목적에 맞춰 실버를 조합 · 집계 · 가공한 층. 원문에 없는 사실을 임의로 추가하지 않는다.
- **시맨틱 레이어** = 공통 개념 · 관계 · 규칙을 실제 데이터 위치 · 조회 경로에 연결하는 논리 계층(네 번째 데이터 등급 아님).
- 확인 기준 = 예상 질문으로 필요한 정보 · 조건 · 근거를 꺼낼 수 있는가. 지원 질문 7범위: 시술 · 부위·고민 · 부작용 · 시술 조합 · 동시 가능 · 순서·간격 · 회피(같은 §1 표) + 상품(가격 · 수량).
이번 일: **설계안과 시범**(drafts 만). 그 전에 작은 silver 정리(A).

## 2. 읽을 것

- `../_RESUME.md` 「목표 참고 문서 §1~5」(70~165줄 부근) · 결정 표 · 끝 줄들(11-14 ~ 11-16)
- `notes/silver-erd.md` · `notes/silver-tables.md` · `drafts/silver-check/`(silver-schema.json · silver-check.py)
- `drafts/relation-pilot/relation-notes.md` §9-2(③ 구조 · 물려받기 규칙) · `notes/relation-notes.md` §4(입구 셈법) · `drafts/offer/offer-notes.md`
- `notes/ledger-check-list.csv` · `notes/external-fill-notes.md`(근거 종류: 원장 · 외부 확인 · 사용자 제공)
- `silver/` 전부

## 3. 사용자 결정 (11-16 「응」)

**A. silver 별칭 정리 3**(`drafts/offer/offer-finalize-notes.md` §4 — 코디 추천으로 바꿈):
1. 계열 alias 「에너지기기(HIFU/RF)」 → 「에너지기기」 · 「마이크로니들링(MTS)」 → 빼기(M12 에 MTS 별칭이 이미 있음). 근거 행도 맞춤.
2. 제품 alias 「쥬베룩 볼륨」 · 「리쥬란 아이」 · 「슈링크 유니버스」 · 「써마지 FLX」 빼기(띄어쓰기만 다른 별칭 — 11-15 A7 결정과 같음) · 그 근거 행도.
3. `notes/ledger-check-sheet.md` 에 G39 묶음 표 행 추가.
고치기 전 `silver/` · 바꿀 notes 를 `archive/silver-before-gold-a/` 에 복사 · `silver-check.py` → **PASS(WARN 0)** · 바뀐 것 = alias · source_ref 해당 행뿐.

**B. gold · 시맨틱 설계안**(`drafts/gold/` 만 — silver 변경 금지)
1. **질문 목록**: 위 8범위마다 실제 질문 꼴 3~5개(고민 · 시술 · 제품 · 상품 어디로 들어와도). 질문마다 필요한 정보 · 조건 · 근거를 적는다.
2. **시맨틱 매핑**: 개념(시술 · 케이스 · 제품 · 고민 · 부위 · 효과 · 부작용 · 사람 조건 · 상품 …)과 관계(적응 · 효과 · 부작용 위험 · 금기 · 보완 · 동시 · 순서 · 간격 · 회피 · 패키지 · 판매)를 정의하고, 각각이 silver 의 어느 표 · 칸 · 조인 경로에 있는지 표로. 의미 구분 규칙(보완 ≠ 같은 날 가능 · 시간 역할 · 빈도 수치 ≠ 서술 등급 · 부위 역할 · 원문/정규화/검증 상태)을 그 매핑에 붙인다. 물려받기(계열 → 시술 → 케이스 · 제품 → 케이스) 조회 규칙 포함.
3. **gold 표 설계**: 질문 범위별로 silver 를 조합한 표(예: 시술 상세 · 고민→시술 후보 · 시술별 부작용 요약 · 시술 쌍 관계 · 상품 가격). 원칙: 원문에 없는 사실 추가 금지 · 모든 행에 근거(source_ref 로 되짚기) · 근거 종류(원장 / 외부 확인 / 사용자 제공) 표시 · 물려받은 값은 「어디서 물려받았나」 칸 · 빈칸 · 미결은 빈칸으로 드러냄(지어 넣지 않음). 저장소(관계형 / 그래프)는 정하지 않았으니 CSV + 노드 · 엣지 내보내기 꼴 둘 다 가능한 구조로 · 판단 목록에 추천.
4. **빌드 스크립트**: silver → gold 를 만드는 스크립트(다시 돌리면 같은 결과).

**C. 질문 시범**: B-1 질문 전부를 gold 로 실제로 답해 본다(질문 · 쓴 gold 표 · 답 · 근거 포인터). 못 답하는 질문은 이유(silver 빈칸 · 원장 확인 목록 id · 구조 문제)로 분류 — **구조 문제는 0 이어야** 하고, 나오면 판단 목록.

## 4. 쓰기 규칙

- A 만 silver · notes 변경. B · C 는 `drafts/gold/`(`gold-build.py` · `gold-check.py` · `gold-notes.md` · `semantic-map.md` · gold CSV · `questions.csv`). CSV UTF-8 BOM · `;` 금지. 원장 변경 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- A: `silver-check.py` PASS(WARN 0) · silver diff = A 목록뿐.
- `gold-check.py`: gold 모든 행이 silver 로 되짚어짐(키 · 근거) · gold 에 silver 에 없는 값 0(문구 조립 · 집계만) · 근거 종류 칸 빈칸 0 · 시맨틱 매핑의 표 · 칸이 silver 스키마에 있음 · 질문 시범 전부 답 또는 이유 · 구조 문제 수 출력 · 재빌드 해시 같음 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/gold/gold-notes.md`, 짧게)

1. A 결과 2. 질문 목록 요약 3. 시맨틱 매핑 요약(정본 `semantic-map.md`) 4. gold 표 설계(표 · 칸 · 행 수 · mermaid) 5. 질문 시범 결과(답함 / silver 빈칸 / 원장 확인 / 구조 문제) 6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(저장소 선택 포함) 7. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(silver 에 새 값 · 표 추가 안 함 · 외부 조사 안 함 · 화면 · API 안 만듦).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/gold/gold-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "gold 설계안 · 시범 완료: drafts/gold/gold-notes.md" --enter`
