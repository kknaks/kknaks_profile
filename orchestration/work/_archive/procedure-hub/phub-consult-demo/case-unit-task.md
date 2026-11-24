# [data] 케이스 = 단위 시술 — 제품 연결 케이스 층 통일 · 케이스 고민 직접 붙이기 → gold 재빌드 → 매핑 JSON 갱신 (사용자 승인 11-20)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 수정 0 · 사용자 포트(18105 · 18222) 프로세스 건드리지 마라 · 키 출력 0. 막히면 질문(아래).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `R=$P/reference/2026-11-19-myeongdong-kos` · `S=$W/silver-model`(silver 작업 사본 — 부위 3단 + 2차 반영 · gold d84e4b8e · 앞 작업 리포트 `$W/final-map-silver2-report.md`)

## 결정(사용자 11-20 — 다시 묻지 마라)
- **시술(PRC)** = 기술 종류(개요 · 원리 · 재료 · 부위 모름). **케이스(CAS)** = 단위 시술 = 시술 + 부위 + 고민 + 제품(제품은 케이스의 **키가 아니라 연결**, 여럿). 진료항목(KOS)은 병원 메뉴 — 허브에 안 넣음.
- 그래서 모든 케이스가 **고민과 제품을 같은 층(케이스)에 직접** 가진다.

## 지금(코디 셈 · `$S/silver/` · 다시 세어 확인)
- 케이스 341 · `product_procedure` 81 행(제품 81 · 시술 12: PRC-100 21 · PRC-001 17 · PRC-111 9 · PRC-110 6 · PRC-122 5 · …) · `case_product` 469.
- 예: 보톡스 제품 22 중 5(보톡스 · 하이톡스 · 나보타 · 보툴렉스 · 티엠버스)는 케이스에, 17(제오민 · 코어톡스 · 디스포트 …)은 시술 PRC-001 에만 → 「입꼬리보톡스」 CAS-006 에 제오민이 안 보임.
- `indication`(target_table=procedure_case)이 붙은 케이스 91 · **없는 케이스 250** → 시술 고민을 통째로 물려받아 CAS-006 입꼬리 보톡스에 다한증 · 사각턱까지 나옴.
- `product_procedure` 시술 중 케이스 0: PRC-101 · PRC-102 · PRC-112.

## 할 일
1. **제품 → 케이스 층 통일:** `product_procedure` 행 전부(81)를 그 시술의 케이스마다 `case_product` 로 옮긴다(「제품 → 시술」 = 「그 시술의 모든 케이스에 씀」 이므로 그대로 펼침 · 이미 있는 쌍은 건너뜀). 근거(source_ref)는 원래 행 근거를 그대로 따라간다. 케이스 0 시술(3)은 그 시술의 **부위 빈 일반 케이스**를 새로 만들어 연결. 케이스 `material_code` 가 제품 재료와 맞지 않는 쌍은 넣지 말고 목록으로. 옮긴 뒤 `product_procedure` 0 행(헤더만) — gold-build · gold 계약이 그 표 행을 요구해 깨지면 멈추고 질문.
2. **케이스 고민 직접 붙이기:** 고민 없는 케이스 250 각각에 대해, 그 시술의 `indication` 고민 중 `concern_site.csv` 에서 **그 케이스 부위(자기 · 조상 · 자손)와 닿는 고민**만 `indication`(target_table=procedure_case) 으로 붙인다. 근거 = 시술 indication 행 + concern_site 행(둘 다 source_ref 따라감). **지어 붙이기 금지** — 닿는 고민이 0 이면 비우고 목록(케이스 · 시술 · 부위)으로. 부위 빈 케이스(일반 케이스)는 시술 고민 그대로(붙이지 않음 · 물려받기 유지).
3. silver-check → gold-build → gold-check(작업 사본 스크립트 · 앞 작업과 같은 기준 꼴 · 기준 사본 `archive/silver-before-clinic-a-20261119-b3/` 새로). C12 · K7(「한 제품이 둘 다」)은 이제 0 이어야 함. 그 밖 FAIL 은 멈추고 질문. 검사 기준을 고쳐야 하면 diff 를 리포트에.
4. **매핑 JSON 다시 만듦**(같은 두 경로 · 같은 꼴 · meta 해시 새로): 앞 작업 생성 스크립트로. v5 코드는 그대로(케이스 · 제품 코드 바뀌지 않음 — 바뀌면 보고).
5. 리포트 `$W/case-unit-report.md`: 표별 바뀐 수 · 옮긴 제품 연결 수(시술별) · 새 일반 케이스 · 재료 불일치로 뺀 쌍 · 고민 붙인 케이스 수 / 0 이라 비운 케이스 목록 · 검사 · 새 해시 · 확인 예: CAS-006(입꼬리) 의 고민 · 제품 목록 · CAS-003(눈가) 제품 목록.

## 검증
`product_procedure` 0 · 시술 층에만 있는 제품 0 · 고민 없는 케이스 = 리포트 목록 수와 같음 · silver-check · gold-check PASS · 공개 silver 에 병원 이름 · 진료항목 코드 0(grep) · JSON 324 · 두 경로 같은 해시.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_c3f59148-8ca7-4a86-8c2b-1ea060538176 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 케이스 단위 시술" --body "옮긴 연결 / 고민 / 검사 / 해시"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
