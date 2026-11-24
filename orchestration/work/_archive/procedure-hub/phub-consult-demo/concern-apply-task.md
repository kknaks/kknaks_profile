# [data] 고민 → 케이스 적용 + 케이스 보충 판단 반영 → gold → JSON (사용자 승인 11-20 · 「추천으로 가고」)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · 사용자 포트(18105 · 18222) 손대지 마라 · 키 출력 0. 막히면 질문.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(gold 1a81ae83 · 케이스 351)

## 원칙(사용자 11-20 — 다시 묻지 마라)
케이스 = 단위 시술. **고민은 케이스에만** — 위층(procedure · modality · package) indication 줄은 **0**(내린 줄은 원래 근거를 새 케이스 줄의 source_ref 로 따라가게 · 내리지 않는 줄은 지움 — 원장 원문은 bronze 에 남음). 제품 층 indication 은 그대로. 우리 데이터는 완전히 채운다(원장 누락은 근거 종류 「보충」 + 근거 글 · 지어내기 금지). 케이스 코드 바꾸지 않음.

## 입력(설계 워커 산출 · 읽고 그대로 적용)
- 규칙 · 표: `$W/research-concern-link.md` · `concern-link-rules.md` · `concern-scope.csv` · `concern-link-map.csv`(928 줄 · 규칙 760 / 사람 판단 168 · 묶음 21) · `concern-link-empty-cases.csv`(고민 0 케이스 112)
- 케이스 보충 리포트: `$W/case-fill-report.md` §6(사람 판단 묶음 A~F) · §10

## 할 일(결정 — 전부 「추천」 칸대로)
1. **규칙 760 줄** 적용 → (케이스 × 고민) indication(target_table=procedure_case). 같은 쌍은 한 번(근거 여럿이면 source_ref 여럿).
2. **사람 판단 21 묶음** — `research-concern-link.md` §4 「추천」 그대로. 「안 내림」 = 위층 줄 삭제.
   - G01: 고민이 아닌 말(평가 · 제품명 · 빈 note) 줄 삭제 · 고민인 말(간 해독 · 피로 · 골밀도 등)은 고민 사전에 찾거나 새 고민(전신 상태 · 근거 · name_en)으로 두고 전신 투여 케이스에 붙임.
   - **새 케이스 만들기**(추천이 「새 케이스」인 것 전부): G10(실 · 기기 × 목 · 허벅지 · 팔뚝 등) · G06(보톡스 × 인중 · 턱밑) · G07(튼살 × 몸 케이스) · G2 M9 이중턱(턱밑) · G2 M3 목주름 · G2 M8 엑시머(시술 「엑시머 레이저」 새로 + 케이스 — 원장 문장 근거) · G04 질 부위(부위 사전 「질」 새로 + PRF 케이스). 새 케이스는 부위 · 방법 · 조직 · 재료 빈칸 0(case-fill 과 같은 방식).
3. **고민 0 케이스** — `concern-link-empty-cases.csv` 의 「같은 시술 · 같은 조직」 36 은 규칙으로 붙임(근거 종류 보충 · 같은 시술 다른 케이스). 나머지는 1 · 2 로 채워지는지 보고, 남는 것은 리포트 목록(0 이 목표 · 남으면 이유).
4. **concern_site 덮어쓰기 4**(국소 지방 · 마리오네트라인 · 바디 쳐짐 · 불독살 — `concern-scope.csv`) silver 반영.
5. **「몸」 부위 코드 새로**(site 1단 · 얼굴 SITE-007 과 나란히 · SITE-001 전신 아래). 몸 부위(팔 · 다리 · 복부 등)를 그 아래로 다시 달고(계층만 · 코드 그대로), case-fill 이 「몸만」 을 SITE-001 로 넣은 케이스는 「몸」 으로 · 얼굴 + 몸 / 전신 투여는 SITE-001 그대로. 근거 「사용자 결정 2026-11-20」.
6. **케이스 보충 사람 판단 A~F**(`case-fill-report.md` §6 추천 그대로): A 조직 사전 「침샘(샘 조직)」 추가 + CAS-100 · 101 · 102 · B 제네시스 진피 · 태반 근육 · IPL 129 · 130 멜라닌 · C 복합 재료 19 비움(시술 재료로 읽음 — 검사 예외 이유 리포트) · D · E 합치지 않음 · F 고주파 목 CAS-3028 → 3029 로 합칠 후보는 **합치지 않고** 리포트에만(코드 고정).
7. 해부 칸은 필수 아님 — 손대지 않음.
8. **명동점 BBL 매핑은 이번에 손대지 않는다**(사용자 조사 중).
9. 스크립트 `build_batch5.py`(재현) · 기준 사본 `archive/silver-before-clinic-a-20261119-b5/` · silver-check → gold-build → gold-check(검사 고치면 diff · 위층 indication 0 검사 추가). 매핑 JSON 두 경로 다시 만듦.
10. **확인 시험 다시**: `concern-link-check.md` 의 고민 15 를 새 gold 로 — 명동점 진료항목 (설계 때 「적용 뒤」 vs 실제) 표 · 엉뚱 · 빠짐.
11. 리포트 `$W/concern-apply-report.md`: 표별 전 → 후 · 위층 indication 0 확인 · 새 고민 · 새 케이스 · 새 부위(몸 · 질) · 새 시술(엑시머) · 고민 0 케이스(목표 0 · 남은 것 이유) · 검사 · 해시 · 확인 시험.

## 검증
위층 indication 0 · 케이스 고민 0 = 리포트 목록 수 · 새 케이스 부위 · 방법 빈칸 0 · 새 값 전부 source_ref · silver-check · gold-check PASS · 케이스 코드 바뀜 0 · JSON 324 두 경로 같은 해시 · 병원 이름 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_c3f59148-8ca7-4a86-8c2b-1ea060538176 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 고민 → 케이스 적용" --body "위층 0 / 고민 0 케이스 / 검사 / 해시 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca orchestration ask` 또는 `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
