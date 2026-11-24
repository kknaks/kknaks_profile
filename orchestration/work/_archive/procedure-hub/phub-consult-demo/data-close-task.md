# [data] 데이터 마감 — 고민 0 케이스 35 채움 · 엑시머 개요 · 원리 · BBL 매핑 → gold → JSON (사용자 승인 11-20 「응!」)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · 사용자 포트(18105 · 18222) 손대지 마라 · 키 출력 0. 막히면 질문.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(gold 43b95e4e · 케이스 386) · `R=$P/reference/2026-11-19-myeongdong-kos`

## 원칙(다시 묻지 마라)
케이스 = 단위 시술 · 고민은 케이스에만(위층 indication 0 유지) · 완전히 채움(출처 필수 · 지어내기 금지) · 케이스 코드 바꾸지 않음 · 공개 silver 에 병원 이름 · 진료항목 코드 0.

## 할 일
1. **고민 0 케이스 35** — `$W/concern-zero-fill.csv`(142 줄 · 조사 워커 산출 · `research-concern-zero.md`) 전부 indication(target_table=procedure_case)으로. 확신 「후보」 줄도 넣되 note 에 「후보」 표시. 새 고민 3(필러 부작용 · 귀밑샘 비대 · 부유방 — 이름 · 상위 · name_en 은 조사 표대로) 고민 사전에 추가. 근거 종류별 source_ref(원장 포인터 · 외부 URL · 사용자 제공 `bbl-research-user-20261120.md` · 같은 시술 다른 케이스).
2. **엑시머 레이저 PRC-030** — `$W/excimer-overview.md` 문안 그대로 overview · mechanism · 새 원리(MEC 「자외선 광면역조절」 · 설명 문안대로)로 mechanism_code. 근거 = 문서의 원장 포인터 · 논문 URL. (새 원리 그림 없음 → 검사 예외면 diff 와 「그림 없는 원리」 목록에.)
3. **BBL 매핑** — `$W/bbl-research-user-20261120.md` 「사용자 결정 매핑」 표 그대로:
   - 새 케이스 **IPL(PRC-006) × 몸 × 피지샘**(부위 · 방법(광 조사) · 조직 · 재료 빈칸 0 · 고민 = 몸 여드름 계열 · 근거 BBL 조사 Forever Clear) + case_product BBL클리어(PRD-323).
   - CAS-064 고민은 1 번(조사 표)에 이미 있음 — 확인만.
   - 진료항목 매핑: `$R/myeongdong-kos-medical-services-20261119.v5.csv` 의 BBL 8 줄 허브 케이스 칸을 표대로 고침(여럿이면 ` + `) · HERO 1/2 모드는 상태 「매핑됨(확인 필요: BBL 필터)」 + 채움 메모. 다른 줄 손대지 않음(바이트 대조).
   - 케이스에 BBL 제품 연결(case_product)이 바뀐 케이스(060 · 061 · 063 · 130 · 새 케이스)에 맞는 BBL 제품이 붙는지 확인 · 없으면 추가(PRD-321 히어로 · 320 포에버영 · 323 클리어).
4. 스크립트 `build_batch6.py`(재현) · 기준 사본 `archive/silver-before-clinic-a-20261119-b6/` · silver-check → gold-build → gold-check(검사 고치면 diff) · 매핑 JSON 두 경로 다시 만듦(BBL 8 줄 케이스 바뀜 확인 · 그 밖 316 줄 같음).
5. **확인 시험**: 고민 15(`concern-apply-report.md` §9 와 같은 15) + 「여드름(바디)」 · 「피부 처짐」 · 「문신」 · 「부유방」 — 명동점 진료항목 전 → 후 · 빠짐 · 엉뚱.
6. 리포트 `$W/data-close-report.md`: 표별 전 → 후 · **고민 0 케이스 = 0** 확인 · 위층 indication 0 · 케이스 부위 · 방법 빈칸 0 · 새 고민 · 원리 · 케이스 · BBL 8 줄 전 → 후 · 검사 · 해시 · 시험.

## 검증
고민 0 케이스 0 · 위층 indication 0 · 새 값 전부 source_ref · silver-check · gold-check PASS · 케이스 코드 바뀜 0 · v5 CSV 는 BBL 8 줄만 바뀜 · JSON 324 두 경로 같은 해시 · 병원 이름 grep 0.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 데이터 마감" --body "고민 0 / BBL / 검사 / 해시 / 시험"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
