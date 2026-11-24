# [data] 최종 매핑 v5 → 허브 silver 2차 → gold 빌드 → 새 코드 채우기 → 매핑 JSON (사용자 승인 11-19)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 수정 0 · 키 출력 0. 막히면 질문(아래).

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `R=$P/reference/2026-11-19-myeongdong-kos` · `S=$W/silver-model`(silver 작업 사본 — 부위 3단이 이미 반영 · gitignore · 검사 스크립트 작업 사본 고침 있음)

## 결정(전부 정해짐 — 다시 묻지 마라)
- **`$W/_RESUME.md` §2 의 2026-11-19 행 전부**가 정본이다. 특히: 매핑 단위 = KOS 진료항목 · 규칙 R1~R8(진료항목명 제품 우선 · 「(국산)」 톡신 = 하이톡스 · 세라핏 = PRC-123 + 밀리핏 PRD-729(배합 나머지 성분은 「해당 없음(세라핏 배합 성분)」 · 하이랙스 포함) · 26-CERAFIT-30 = 세라핏 · A/B 메뉴 = 케이스 1 + 제품 2 · 얼굴 전체 · 부위 없는 진료항목 = 그 시술의 부위 빈 케이스 · 이름 다른 제품은 코드 직접 · 얼굴 · 몸 가능 = 1단 얼굴 + 몸 · 제품명은 허브 원본 이름) · 대표 제품(엑소좀 → PRD-170 · 순수톡신 → PRD-008 · 스킨보톡스 제품명 없는 줄 → 하이톡스 · CO2 → PRD-315 · 태반주사 → PRD-720 · 하이주 → 하이주(히알루론산나트륨 · 휴온스)) · 시술(수액 · 감초주사 → 해당 없음 · 필러 용해 → 허브 시술 추가 · 혈액 줄기세포 → 뺌 · **포트라 → PRC-007 + CAS-064**(근적외선 타이트닝 · 사용자 확인) · KK주사 → PRC-120 · 엑소제 → PRC-122 · 필링 1종 선택 · 예스필 → 필링 계열 대표 시술 · KS주사 · 셀코어 · 이온자임 · 라라젯 · 플래티넘PTT → 시술 「확인 필요」 유지) · 제품 뺌(필링제 6 · 아쿠아필링기 · 이온토) · 제품 추가(확실 7 = 하이톡스 · 피코라이트블랙 · 히알라제 · 쥬베룩 스킨 · 올리디아120 · 올리디아365 · 포텐자펌핑팁 / 웹 확인 5 = 포트라(클래시스) · 소노케어(뉴퐁) · 오투덤(트리시스) · 울킨(메딕콘) · 레스틸렌 아이라이트(갈더마) / 브랜드 2 = 프로디젠 PROSYS · 라쥬니스 / 미확인 6 = 크라이오셀 · 이온자임 · 플래티넘PTT · 인주셀 · 셀코어 · 엑소제 · 하이주(휴온스)) — 하위 제품: 쥬베룩 스킨 → PRD-105 · 올리디아120/365 → PRD-110 · 포텐자펌핑팁 → PRD-550 · 레스틸렌 아이라이트 → PRD-051.
- 허브에 넣는 것: **일반 케이스(시술 × 부위 — 병원 이름 · 배합 없음)** · **케이스 ↔ 제품 연결(case_product)** · 새 제품(+ 회사 · 재료 · 계열 연결은 근거 있는 만큼) · 시술 필러 용해(히알루로니다제). **진료항목은 허브에 넣지 않는다.**
- 근거: 원장 아닌 행은 부위 묶음과 같은 꼴 — 로컬 근거 파일 `$S/drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`(줄마다 대상 · 결정 · 근거 글 「사용자 결정 2026-11-19 · 명동점 진료항목」 / 「식약처 <허가번호>」 / 「웹 확인(사용자 조사) · 식약처 허가 미확인」). 공개 silver 에 병원 이름 · 진료항목 코드 · 가격 0.

## 입력
- 진료항목 채움 v4: `$R/myeongdong-kos-medical-services-20261119.v4.csv`(324 × 82)
- 제품 정규화: `$R/product-normalize-20261119.csv` · `$W/research-product-normalize.md`
- 부위 묶음 리포트(근거 꼴 · 검사 방법): `$W/silver-site-report.md` · 지시 `$W/silver-site-task.md` · `silver-site-addendum1.md` · `addendum2.md`
- SPEC: `$W/SPEC-009-hub-clinic-supplement.md`(0.2.2 — 부위 규칙 · 근거 · 검사 · 반영 절차)
- 허브 silver 표 꼴: `$S/silver/*.csv` · 로컬 PG(SELECT · 값 출력 금지)

## 할 일(순서대로 · 단계마다 산출 확인)
1. **v5 최종 매핑** — v4 에 결정을 전부 적용해 `$R/myeongdong-kos-medical-services-20261119.v5.csv`(v4 칸 + 필요하면 `상태`). 빈칸 0. 「허브 추가 필요」 는 2 단계 뒤 코드로 바뀔 자리.
2. **silver 2차 패치**(`$S/silver/` · 부위 묶음 위에 덧붙임 · 스크립트 `$S/drafts/clinic-supplement/clinic-a-20261119/build_batch2.py` 로 재현 가능하게): 새 제품 · 시술 · 일반 케이스 · case_product · 근거. 코드는 기존 꼴로 다음 번호.
3. **silver-check → gold-build → gold-check**(작업 사본 스크립트 · 부위 묶음 때 고친 경로 · 근거 종류 식 그대로). 묶음 기준 사본은 부위 묶음 뒤 상태로 새로(`archive/silver-before-clinic-a-20261119-b2/`). 그 밖 FAIL 은 멈추고 질문. 새 gold_hash · aux_hash.
4. **새 코드 채우기** — v5 의 「허브 추가 필요」 를 2 단계 새 코드로 바꿔 `…v5.csv` 갱신. 남는 「확인 필요」 는 시술 6 줄뿐이어야 한다(그 밖이면 보고).
5. **매핑 JSON** — `myeongdong-mapping-20261119.json`(utf-8):
   ```
   { "meta": {"clinic": "명동점", "kos_snapshot": "2026-11-19", "hub_gold_hash": "<새>", "hub_aux_hash": "<새>", "made_at": "..."},
     "items": [ { "kos_item_code", "kos_item_name", "kos_procedure", "kos_machine", "kos_medicine", "kos_unit", "kos_description", "kos_option_count",
                  "site_tiers": {"t1","t2","t3"}, "site_scope",
                  "hub": {"procedure_codes": [], "case_codes": [], "site_codes": [], "products": [{"code","name","from": "구성n"}]},
                  "status": "매핑됨 | 시술 확인 필요", "note" } ],
     "groups": [ {"kos_procedure", "items": [kos_item_code...]} ] }
   ```
   가격 · KOS id 0(상품 · 옵션 가격은 이번에 넣지 않는다). 둘 곳(**둘 다 git 제외 자리**):
   - `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261119.json`
   - `/Users/kknaks/git/clinic_chat/data/kos/myeongdong-mapping-20261119.json`(사용자 메인 로컬 — 파일 하나 복사만 · 그 체크아웃의 다른 것은 건드리지 마라)
   두 경로 모두 `git check-ignore` 로 무시되는지 확인(안 되면 멈추고 질문).
6. 리포트 `$W/final-map-silver2-report.md`: v5 상태별 수 · silver 바뀐 수(표별) · 검사 결과 · 해시 · 새 코드 목록(제품 · 시술 · 케이스) · JSON 건수 · 남은 확인 필요 6 줄.

## 검증
v5 324 줄 · 빈칸 0 · 「허브 추가 필요」 0 · 코드 전부 새 silver 에 실재 · silver-check · gold-check PASS(WARN 은 사유) · JSON 항목 324 · 두 경로 git 무시 확인 · 공개 silver 에 병원 이름 · 진료항목 코드 0(grep).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_c3f59148-8ca7-4a86-8c2b-1ea060538176 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: v5 · silver 2차 · gold · JSON" --body "상태별 수 / 검사 / 해시 / JSON"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
