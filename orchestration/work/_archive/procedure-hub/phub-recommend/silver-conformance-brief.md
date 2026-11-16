# 빌더 ERD 적합성 시험 발주서 — WP-S2 (코디 · 2026-11-05 · 사용자 「계속 보강해야 하나」→ 한 번에 완성)

## 목적
실버 빌더 `silver-v3/` 가 **ERD v3 가 정한 경우의 수 전부**를 구현했는지를 기계로 증명하는 시험 묶음. 실제 데이터가 아직 안 건드린 경우(오늘의 R16 사람 조건 끝처럼)를 미리 전부 돌려, 이후 새 데이터·새 결정이 들어와도 빌더를 손대지 않게 한다. 빌더를 고치는 건 ERD 가 바뀔 때뿐.

## 경우의 수 (erd-v3.json 에서 기계로 뽑는다 · 손으로 열거 금지)
1. 결정 kind 17 × target/new_value 구조체의 모든 분기(§5.2). kind 마다 최소 1 fixture, 분기가 있으면 분기마다.
2. edge_create ref 구조체 종류 5(anchor · locator · procedure_tuple · adverse_tuple · dict_value) × 관계 31 의 허용 양끝 종류 조합. 허용되지 않는 조합은 **거부**되는 것도 시험.
3. 분해 규칙 전부(§1.3~1.5 · resolve_rules): 괄호·조합 기호 `+`/`/`·회사 괄호·stopwords·multi_tuple·qualifier·layer 금지·course 멤버 규칙·raw_name·표현 exact/unlinked. 규칙마다 양성·음성 fixture.
4. 충돌 ④⑥⑦⑧⑨ 생성·닫힘(auto_resolved·fold 로 ⑦ 닫힘·conflict_close·override).
5. 적용 순서 ①~⑦ 과 안정 키(파생 id target 거부 · #s<i> anchor 허용 · 결정 간 순서 의존).
6. 브론즈 판 교체(HASHES.txt) · provenance 필수(출처 없는 값 FAIL) · 재실행 바이트 동일.

## 방법
- `silver-v3/tests/` 에 표준 라이브러리 `unittest` 로. fixture 는 **합성 원장 조각**(실제 원장 형식을 따르되 작은 가짜 데이터)과 합성 결정. 실제 원장·실제 결정은 시험에 쓰지 않는다(그건 check.py 가 함).
- 경우의 수 생성기 `tests/enumerate_cases.py` 가 erd-v3.json 을 읽어 「시험해야 할 경우 목록」을 JSON 으로 내고, 시험 러너가 그 목록의 **모든 경우에 대응하는 테스트가 존재하는지** 검사(없으면 FAIL). 즉 ERD 가 바뀌면 빠진 테스트가 자동으로 드러난다.
- 빌더에 구멍이 나오면 **고친다**(이 발주의 일부). 고친 뒤 실제 5차 빌드 `build.py` → `check.py` 19/19 PASS 와 바이트 동일(또는 달라진 이유를 report 에) 확인.
- `README.md` 에 「빌더 완성 조건 = tests 전부 PASS + check.py 전부 PASS」와 실행법.

## 보고
경우의 수(kind·ref×관계·규칙·충돌·순서 각 몇 건) · 테스트 수 · 처음 돌렸을 때 FAIL 수와 고친 구멍 목록 · 최종 PASS · 실제 빌드 영향(수치 변화 있으면 이유). 본문 재붙임 금지. 커밋 금지.
