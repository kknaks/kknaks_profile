# 제품 사전 수정 — 4~7번 반영 (사용자 조사 2026-11-11)

대상: `silver-model/drafts/product/product.csv` · `organization.csv` · `product-notes.md` (UTF-8 BOM 유지, 원장은 고치지 않는다)

## 0. 공통 기준 (이번에 정함)
- **제품의 manufacturer_code = 현재 회사.** 원래 회사(인수·합병 전)는 조직 행으로 남기고 제품 description 에 「원 제조사 ○○ — 연도 △△에 인수/합병」을 적는다(시크릿 = 클래시스 · 원 제조사 이루다와 같은 방식).
- **organization.csv 에 칼럼 추가: `current_org_code`** — 인수·합병으로 다른 회사에 들어간 회사면 그 회사 코드, 아니면 빈칸. `description` 칼럼도 추가해 연혁 한 줄(예: 「2024-10-01 클래시스에 흡수합병」). 이루다(ORG-085)도 current_org_code = 클래시스로 채운다.
- 같은 회사의 옛 이름·사명 변경 전 이름은 별도 행이 아니라 **aliases**.

## 4번 — 아그네스
- 원장 「제니스 · AGNES · 고우리엔티」는 이름을 잘못 붙인 것으로 본다. AGNES 의 한글 이름은 **아그네스**, 제조사는 **아그네스메디컬**(AGNES MEDICAL CO., LTD.).
- 아그네스 제품 행: name_ko 아그네스 · name_en AGNES · manufacturer = 아그네스메디컬(새 조직 행, name_en AGNES MEDICAL) · 원장의 아그네스 항목(「여드름피지선RF」, problem 쪽 「피지선 파괴 · 니들RF」) basis 유지 + products.json/taxonomy 제니스 행의 name_en·type 포인터를 근거로 합친다.
- 제니스 제품 행: name_en·manufacturer 비움, description 「원장 표기 — 이 이름의 장비는 확인되지 않음(AGNES 는 아그네스)」. 행은 남긴다.
- 조직 고우리엔티: 다른 제품이 안 쓰면 삭제하고 원장 오류 표로(초기 FDA 신청자 Gowoonsesang Cosmetics 의 오기 가능성 — 추정이라고 적는다).

## 5번 — 캔델라
- 캔델라 · 시너론캔델라 · 시네론캔델라 · 시너론은 **한 조직 캔델라**(2010 시너론·캔델라 합병 → 2019 사명 캔델라). 캔델라 행 하나만 남기고 aliases = 시너론캔델라;시네론캔델라;시너론(Syneron Candela;Syneron 영문도). 다른 행은 지우고 제품을 캔델라로 다시 연결.
- 캔델라 제품: 피코웨이 · 젠틀맥스프로 · 젠틀맥스프로+ · 젠틀레이즈 · E-MAX · 시너론 아이플러스 · **브이빔퍼펙타**(원장 「시너론595nm」 — 원래부터 캔델라).
- **벡터스** → 사이노슈어 루트로닉(아래), 원 제조사 팔로마(2013 사이노슈어가 팔로마 인수). 조직 「팔로마」 행: current_org_code = 사이노슈어 루트로닉.
- **펠레베** → 사이노슈어 루트로닉, 원 제조사 엘먼(Ellman, 2014 사이노슈어가 인수). 조직 「엘먼」 행 추가: current_org_code = 사이노슈어 루트로닉.

## 6번 — 두 회사 붙은 표기
- **사이노슈어 · 루트로닉 → 한 조직 「사이노슈어 루트로닉」**(Cynosure Lutronic, 2024 합병). aliases = 사이노슈어;루트로닉;Cynosure;Lutronic. 원장의 사이노슈어 제품 · 루트로닉 제품(클라리티2 · 피코플러스 · 피코코어 · 에코2 · 에코2에볼루션 · 할리우드스펙트라 · 인피니 등) 모두 이 조직으로.
- **아발란체** → 포토나(Fotona). 「루트로닉」 부분은 원장 표기만 기록(국내 유통 여부 미확인).
- **아포지엘리트플러스** → 사이노슈어 루트로닉.
- **에스테필** → 제조사 **리젠바이오텍**(새 조직 행). description 에 「국내 독점 유통 휴메딕스」. 원장 「레지메드」는 오류. **kind = 콜라겐 자극 주사제**(PDLLA 기반 주사제 — 장비 아님)로 맞는지 확인해 고친다.

## 7번 · 원장
- 영어 이름 빈칸은 그대로 둔다(추측해 채우지 않음). 원장(브론즈)은 고치지 않고 실버와 오류 기록에서만 바로잡는다.

## notes
- 7절 원장 오류 표에 이번 오류 전부 추가(위치 · 원장 값 · 바른 값 · 출처): 제니스/AGNES/고우리엔티 · 시너론 표기(브이빔퍼펙타) · 벡터스 「팔로마/시너론」 · 펠레베 「시너론모노폴라」 · 에스테필 「레지메드」. 출처: 사용자 조사 2026-11-11 — FDA 510(k) K243713·K250217·K160469(AGNES) · K230990(Vbeam) · K223540(AvalancheLase) · Plastic Surgery Practice(시너론·캔델라 합병) · Practical Dermatology(캔델라 사명) · Cynosure 10-Q 2013(팔로마 인수) · MedEsthetics(엘먼 인수) · EMDT(사이노슈어·루트로닉 합병) · 데일리팜·토요경제(에스테필 · 휴메딕스).
- 6절 표 4~7번을 「해결」로 갱신. 1절 행 수 갱신.
- 조직 합치기·삭제 전후 표(옛 코드 → 새 코드)를 한 절로.

## 완료
조직을 지운 뒤 product.csv 의 manufacturer_code 가 전부 organization.csv 에 있는지 확인. `git status` 확인 후 preamble 의 worker_done(--outcome, --report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/product/product-notes.md) 한 번, 그리고 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "product 4~7번 수정 완료" --enter`
