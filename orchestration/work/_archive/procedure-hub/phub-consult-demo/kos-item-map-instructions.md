# [researcher] 매핑 단위를 KOS **진료항목**으로 다시 — 전체 받기 · 진료항목 코드 키 매핑 초안

## 왜 다시 하나 (사용자 11-19 — 반드시 지켜라)
앞 판은 KOS **시술 이름**(바디보톡스 · 올리디아120 …) 124 개 단위로 매달았다. 틀렸다.
- 매핑 단위 = **KOS 진료항목**(KOS 화면 관리 › 진료항목 목록의 한 줄). **키 = 진료항목 코드**(예: `26-BDBT-KR-100UNIT`).
- 한 줄 칸 = KOS 화면과 같은 칸 그대로: 표기명/진료항목명 · 진료항목 코드 · 시술 · 기기 · 약물 · 용량 및 단위 · 게시 여부 (+ 설명). **원문 값만. 상품 카테고리 같은 다른 곳 값을 끌어와 붙이지 마라.**
- 그 한 줄 → 허브 시술 PRC + 부위 SITE + 제품 PRD.
- 예(사용자 화면): 시술 「바디보톡스」 의 진료항목은 2 개 — 「보톡스(국산) 100unit」 26-BDBT-KR-100UNIT 약물 보톡스 · 「보톡스 하이톡스 100unit」 26-BDBT-HTS-100UNIT 약물 하이톡스. 우리 v2 JSON 에는 상품 옵션에 걸린 1 개만 있다 → **진료항목 전체를 받아야 한다.**

## 1. 진료항목 전체 받기
- 우리 v2 의 `treatment_items`(300)는 상품 옵션이 가리키는 것만이다. KOS 화면 진료항목 목록 전체가 필요하다.
- 길 1(먼저): KOS **open API** `getMedicalServices`(앞 조사 10-30 이 316 을 받음 · 공식 스펙 · 조회 전용). 수집기 `/Users/kknaks/git/ax-clinic-project/scripts/kos_query_catalog.py` · `kos_collect.py` 의 방식(API 키 → 토큰 교환 · 조회 경로 화이트리스트)을 읽고 그대로 쓴다. 키는 ax-clinic-project `.env`(`KOS_API_KEY` 또는 구 이름) — **값 출력 금지**. 명동점(세라미크의원 명동점 · DEMO 아님) 것만. 그 레포 파일은 고치지 마라 — 스크립트가 필요하면 `reference/2026-11-19-myeongdong-kos/` 안에 새로.
- 길 2(길 1 이 안 되면): 내부 API 가이드(`reference/2026-11-19-myeongdong-kos/kos-product-json-guide.md`)와 같은 로그인(`~/.config/day/kos-test-account.env`)으로, KOS 화면 진료항목 목록이 부르는 조회 경로를 찾는다(`…/queries/…` 만 · 쓰기 0 · 세션 표시 ` (product-json)` · 끝나면 내 세션 해제). 경로를 못 찾으면 멈추고 코디에게 물어라.
- 원응답은 `reference/2026-11-19-myeongdong-kos/raw/`(gitignore) 에 `G_medical_services*.json` 로. 게시 · 미게시 모두.
- 확인: 전체 수 · 우리 300 과 겹침(id) · 300 밖의 수 · 바디보톡스 진료항목 2 개가 다 나오는지.

## 2. 진료항목 코드 키 매핑 초안
`reference/2026-11-19-myeongdong-kos/kos-item-map-draft-20261119.csv` — 한 줄 = 진료항목 1 개. 칸:
`kos_item_code, kos_item_title, kos_procedure_name, kos_machines, kos_medicines, kos_unit, kos_published, kos_description, in_product_option(○/✗), hub_procedure_code, hub_procedure_name, hub_site_code, hub_site_name, hub_product_codes, hub_product_names, status(확실|애매|허브 없음|시술 아님), basis, note`
- **가격 칸 넣지 마라** · KOS id 넣지 마라(보조 JSON 에만).
- 시술 PRC · 부위 SITE: 앞 판 시술 단위 CSV(`kos-procedure-map-draft-20261119.csv`)의 그 KOS 시술 줄 값을 출발점으로 쓰되, **진료항목명에 부위가 더 구체적으로 있으면**(예: 「보톡스 승모근 …」 · 「아발란체 제모 (팔 하완)」) 그 부위를 쓴다. 근거는 `research-site-evidence.md`(원장 근거 있음/없음) — 원장 근거 없는 부위(부유방 · 손가락 · 발가락 · 발등 · 하완 · 뒷목)는 허브 기존 상위 부위만 · 「애매」.
- 사용자 확정: 제모 = PRC-002 + 부위(초안대로) · 세라핏 지방분해주사 = PRC-123 + 부위 + PRD-729 밀리핏(진료항목 설명 · 병원 확인 8/25).
- 제품 PRD: **진료항목의 약물 · 기기**로만. 글자 그대로 맞추지 마라 — KOS 약물 이름표 문제:
  - 「보톡스」 = 톡신 일반 이름표(「보톡스(국산)」 · 「국산 주름 보톡스 3부위 (코어톡스)」 등에도 씀) → 허브 PRD-001(앨러간 보톡스)로 매달지 마라 · 진료항목명에 브랜드가 있으면 그것 · 없으면 비움 + 「애매」
  - 「앨러간」 = 회사 이름 → 앨러간 보톡스 제품인지는 허브 제품 원장(이름 · 다른 이름 · 회사)으로 확인되면만
  - 「수입」 = 원산지 → 비움 + 「애매」
  - 그 밖은 정확 · 공백/괄호 정규화 일치만 「확실」 · 나머지 「애매」 · 허브 제품에 없으면 「허브 없음」 표시는 note 에.
- 진료항목명의 브랜드(예: 「… 제오민 100unit」)와 약물 칸이 다르면 둘 다 note 에.

## 3. 리포트
`orchestration/work/phub-consult-demo/research-kos-item-map.md` — 한눈 표(전체 진료항목 · 옵션에 걸린 것/안 걸린 것 · status 별 수 · 제품 칸 status) → 받기 확인 → 「보톡스 · 앨러간 · 수입」 이름표 처리 결과 → 애매 · 허브 없음 목록(진료항목 코드 · 이름 · 왜) → 확인 안 됨. 이름 · 코드 · 수만 · 가격 0.

## 하지 말 것
쓰기 API 0 · ax-clinic-project 파일 수정 0 · 허브 · 앱 수정 0 · 커밋 0 · 서브에이전트 0 · 키 · 토큰 · 테넌트 id · 사람 이름 출력 0.

## 검증
CSV 줄 수 = 받은 진료항목 수 · 진료항목 코드 중복 0(중복이면 그대로 보고) · 허브 코드 전부 실재(SELECT) · 바디보톡스 2 줄 확인 · grep 이메일 · 토큰 꼴 0 · `git status --short` 로 변경이 위 파일뿐(JSON 은 ignore).

## 완료 보고
앞과 같은 2채널 · subject 「researcher 완료: 진료항목 단위 매핑」.
