# 실버 빌드 7차 발주서 — 빌더 v3.2 반영 + 노드 게이트 자료 (2026-11-05)

## A. 빌더 v3.2 반영 (코드)
ERD 입력 `erd-v3.2.json`·`erd-v3.2-dictionaries.json`. 참조 구현 `erd-v3.2-tuples.py` · 대조 `erd-v3.2-tuples.json`(결정 적용 전 수치 차이 0). 규칙 정본 `erd-v3.2.md`(§0 원칙 · §1.1 norm_v2 · §1.3 tokenize · §1.4 what(ingredient·장비 자동 등록) · §1.5 phrase_kinds·핵심어 규칙(S-1) · §1.7 씨앗 · §2 개체 22(post_procedure_timeline · emergency_sign) · §3 R33/R34/R35 · R15.inheritance · §5 · §11).
핵심 구현: ① 문구 종류 분류 → 부작용 문구만 단위에, 타임라인·응급 징후·고지·문헌은 자기 개체 + 참조 ② 부작용 문구: 사전 사건 exact / 남은 토큰 속성(side) 또는 토막 새 노드 / 사전 사건 없으면 핵심어 새 노드(status=unreviewed · origin=ledger · 설명·locator) — **unlinked 상태 없음** ③ ⑦ 노드끼리(strong/weak) ④ 장비 → 제품 자동 등록(origin=taxonomy · 허가 미확인) · 성분 what ⑤ 토큰화·변형 목록(보존) ⑥ R15 3층 상속(참조·basis) ⑦ 타임라인 개체·줄 참조. 
- 기존 결정 전부 적용(v3.1 raw_name 대상 adverse_tuple_assign 10건은 새 구조로 옮겨 적용 — 사유 로그). 거부 0 목표.
- `tests/` 열거기가 v3.2 json 을 읽어 새 경우를 요구 → 테스트 채우고 구멍 고침. `run_tests.py`·`check.py`(v3.2 항목) 전부 PASS.

## B. 7차 빌드
`build.py` → `check.py` → `tests/run_tests.py`. report.md 「7차 · ERD v3.2」: 6차 대비 변화표 · 부작용 문구 분포(exact/new/메모/설명문) · 새 노드 수 · ⑦ strong/weak · 타임라인 줄 분포 · 항목 자신/제품 승격 · ⑨ · R15 상속 basis 분포.

## C. 게이트 자료 — **노드 단위** (2B 스키마 `out/gate/batch5.json`·`.md` · `apply_gate.py --gate` 지원)
1. **새 사건 노드 목록**(262): 노드마다 핵심어 · 원장 횟수 · 어느 계열·항목에서 · 원문 예 3 · 설명 · 옵션 = 「부작용 맞음(종류: 국소/염증/혈관/신경/색소/구조/전신/기능)」/「부작용 아님 → 메모」/「접기 → (⑦ strong 상대 노드)」. 추천 = 원장 칸이 종류를 말할 때만.
2. **⑦ strong 98 쌍**: 쌍마다 두 노드의 원문·횟수 · 옵션 「같다(접기, keep 쪽)」/「다르다」/「보류」. 병기 쌍은 추천 「같다」.
3. **씨앗 승인**(부위 14 · 성분 17 · 줄임말 29): 사전별 표, 옵션 승인/제외.
4. **묶음 3 미결 15**(`out/gate/batch3.json` 그대로 포함 · 공기색전은 v3.2 물질 칸 기준으로 옵션 갱신).
5. weak 207 은 별도 파일(`batch5-weak.json`), 게이트에 안 올림.
각 옵션 decision_payload 완성형 · 원장 원문 읽기 실패 0 · 추정 금지.

## 규칙·보고
ERD v3.2 정본 · 원장 불변 · provenance · 재실행 동일 · 표준 라이브러리 · 커밋 금지 · 금지 목록 이전과 같음.
보고: A 반영·거부·tests/check · B 변화표 · C 항목 수(1~4) · 추천 수 · 읽기 실패. 본문 재붙임 금지.
