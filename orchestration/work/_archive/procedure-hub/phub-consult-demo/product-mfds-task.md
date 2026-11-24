# [researcher] 허브 추가 제품 — 식약처 · 약학정보원 조회로 정규화 (읽기만 · 사용자 승인 11-19)

너는 procedure-hub 조사 워커다. 앞 맥락 없음. 허브 · silver · KOS 쓰기 0 · 커밋 0 · 서브에이전트 0 · **키 · 토큰 출력 0**.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `R=$P/reference/2026-11-19-myeongdong-kos` · `W=$P/orchestration/work/phub-consult-demo`
조회 도구(메인 체크아웃 · 로컬 코드 · 고치지 마라):
- 식약처: `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-27-mfds-mcp/`(Python · uv · `.env` 키 준비됨 · smoke 통과 11-19). README 를 읽고 **MCP 서버를 띄우지 말고 그 패키지 코드를 직접 불러** 쓴다(`src/mfds_mcp/tools.py` — device_search · device_detail · device_company · drug_search · drug_detail(include_ingredients) · dur 은 불필요). 하루 상한(.env 기본 1000) 안에서 · 캐시 씀.
- 약학정보원: `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-28-kpic-mcp/`(Node · pnpm · 키 없음). README · NOTES 를 읽고 그 코드로 `search_drugs_by_name` · `get_drug_detail_by_id` 를 부른다(설치는 그 폴더 안에서만 · node_modules 는 gitignore 확인). 안 되면 사유를 적고 식약처만으로.

## 배경
명동점 KOS 진료항목 324 를 허브에 매핑하는 중. 허브 제품 목록에 없는 제품을 허브 silver 에 **추가**하기로 했다(사용자). 넣기 전에 정식 이름 · 업체 · 허가 · 성분을 공식 출처로 정규화한다. 필링제(라라필 · 블랙필 · 예스필 · 플라필 · 핑크필 · 펌킨필)는 이번에 **뺀다**.

## 대상
A. 추가 대상 19(명동점 KOS 표기 · 쓰인 진료항목 수): 하이톡스(32) · 피코라이트블랙(9) · 포트라(5) · 쥬베룩 스킨(4) · 올리디아120(3) · 올리디아365(3) · 소노케어(2) · 오투덤(2) · 라쥬니스 줄기세포(2) · 인주셀(2) · 엑소제(2) · 포텐자펌핑팁(2) · 프로디젠(1) · 이온자임(1) · 셀코어(1) · 크라이오셀(1) · 레스틸렌 아이라이트(1) · 플래티넘PTT(1) · 히알라제(1).
B. 정체 확인(후보만 · 명동점이 무엇을 쓰는지는 결정하지 마라): 하이랙스 · 페니 · 비본(세라핏 배합 성분 표기) · 하이주 · 태반주사(라엔넥 / 멜스몬 후보) · CO2 · 아쿠아필링기 · 이온토 · 울킨(기기 표기).
- 명동점 쪽 문맥(진료항목명 · KOS 설명)은 `$R/myeongdong-kos-medical-services-20261119.v4.csv` 에서 본다.
- 허브에 이미 비슷한 제품이 있는지(하위 제품 후보 — 쥬베룩 PRD-105 · 올리디아 PRD-110 · 포텐자 PRD-550 · 레스틸렌 PRD-051 등)는 로컬 PG(SELECT · `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 값 출력 금지) `s_product` · `s_product_organization` 로 확인.

## 정규화할 칸(제품마다)
KOS 표기 · 조회 질의 · 출처(식약처 의약품 / 식약처 의료기기 / 약학정보원) · 정식 제품명(한글 · 영문) · 업체(제조 · 수입 · 역할) · 허가 구분(전문의약품 · 의료기기 등급 등) · 허가번호 · 품목기준코드 · 주성분 / 기기 원리(허가 자료에 있는 만큼) · 취소 여부 · 허브 후보(새 제품 / 기존 PRD 의 하위 제품 / 기존 PRD 와 같음) · 허브 `kind` 후보(약제 · 장비 · 필러 · 스킨부스터 등 — 허브 기존 값 중에서) · 확신(확실 / 후보 여럿 / 조회 안 됨) · 메모. **추정 금지** — 조회 결과에 없는 칸은 비운다. 후보가 여럿이면 다 적고 하나로 고르지 마라.

## 산출
- `$R/product-normalize-20261119.csv`(utf-8-sig · 로컬) — 한 줄 = KOS 표기 하나(A 19 + B 9).
- `$W/research-product-normalize.md` — 확실 / 후보 여럿 / 조회 안 됨 수 · 표 요약 · 하위 제품 후보 · 호출 수.

## 검증
28 줄 · 조회 근거 칸(출처 · 허가번호 또는 품목기준코드) 빈 「확실」 0 · grep 으로 키 꼴 0 · `git -C $P status --short` 로 새 파일이 위 2 개뿐.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_e7f804bf-88ad-424f-b437-832b3bf38e60 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 제품 정규화" --body "확실 / 후보 여럿 / 조회 안 됨 · 호출 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] researcher 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
