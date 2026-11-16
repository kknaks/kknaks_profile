# 1단계 D16 — 같은 제품인지 2쌍 국내 웹 확인

정본은 `step1-d16-web.json`. 생성 2026-10-27. 원장 · 결정 파일은 바꾸지 않았다(반영은 코디 판단).

- PHA필 ↔ 물톡스 — **시술 이름**
- 라라닥터 ↔ 라라필 — **같은 라인 다른 제품**

| 쌍 | ledger_id | 결과 | 근거 | 업체 | 판매사 | 충돌 · 참고 |
|---|---|---|---|---|---|---|
| PHA필 ↔ 물톡스 | `auto-M15-1775401670325` · `auto-M15-1775402148301` | **시술 이름** | 국내 병원 시술 페이지가 「PHA필링(물톡스)」 · 「물톡스(PHA필링)」 · 「순수 PHA(물톡스) 필링」처럼 두 이름을 한 시술로 묶어 쓴다. 톡스앤필 페이지는 PHA 성분 도포 필링의 시술명으로만 쓰고 제품명 · 제조사 · 브랜드를 표기하지 않음. 다손의원은 같은 「물톡스(PHA필링)」에 「엑스비앙스 정품」 제품을 쓴다고 표기 — 병원마다 쓰는 제품이 다르다. 따라서 물톡스는 특정 제품이 아니라 PHA 필링 시술의 통칭(③)이고, 원장 PHA필도 같은 시술의 이름이다(두 행 모두 제품 아님) · https://www.toxnfill.com/m/brand/detail.php?c=1246&i=5230 https://dashonclinic.com/service/detail/125 https://www.toxnfill46.com/m/detail.php?c=2389&i=13216 https://www.toxnfill40.com/m/detail.php?c=&i=1063 http://m.jwellclinic.com/page/page273 | 근거 없음 — 물톡스 · PHA필 이름의 제조사 · 브랜드 표기 0(시술 페이지) | 근거 없음 — 시술 이름이라 판매사 해당 근거 없음 | 같은 이름을 쓴 소비자 화장품 「메디필 PHA 물톡스 필링 크림 50ML」 판매 페이지 존재 — 병원 시술 제품인지 근거 없음(페이지 상세는 열람 실패) (https://www.11st.co.kr/products/2030386925)<br>다손의원 사용 제품: 엑스비앙스 정품(브랜드 표기만) (https://dashonclinic.com/service/detail/125)<br>화장품 여부: 시술에 쓰는 제품이 병원마다 달라 단일 제품의 화장품 · 의료기기 여부 판정 대상 아님. 원장 정체(kind=제품) ↔ 출처(시술명) 다름 — 반영은 코디 판단 |
| 라라닥터 ↔ 라라필 | `auto-M15-1775401788467` · `M15-1-7` | **같은 라인 다른 제품** | 에이치투메디(라라필 본사)가 2025-01 신제품 「라라닥터」 출시 — 「기존 라라필 성분을 기반으로」 INCUBE 플랫폼 · PLLA 입자 · QPT 특허 기술을 결합한 업그레이드 버전(INCUBE 501 · INCUBE 701(PLLA) · QPT · 칼슘 추가). 랩인큐브(INCUBE · H2sol 특허)와 공동 개발. 같은 회사 · 같은 라인의 별도 신제품이며 같은 제품의 다른 이름이 아님. 라라필 자체도 2025-04 「라라필 504」 신버전 출시 · https://www.ajunews.com/view/20250113163746036 https://www.hitnews.co.kr/news/articleView.html?idxno=74953 https://news.nate.com/view/20250417n06527 | (주)에이치투메디(H2MEDI) — 라라필 · 라라닥터 개발 · 출시(「라라필 본사」) · https://www.ajunews.com/view/20250113163746036<br>랩인큐브 — INCUBE · H2sol 특허 보유 · 공동 개발 · https://www.ajunews.com/view/20250113163746036 | 라라닥터: 동구바이오제약 — 국내 · 몽골 독점 유통 계약 · 2026-03-27 보도 · https://www.hitnews.co.kr/news/articleView.html?idxno=74953<br>라라닥터: 유벤타헬스케어 — 동구바이오제약과 공동 유통 전략 마련(기사 표현) · 2026-03-27 보도 · https://www.hitnews.co.kr/news/articleView.html?idxno=74953<br>라라필: (주)에이치투메디 — 라라필 본사(공급) · 2025-01 보도 · https://www.ajunews.com/view/20250113163746036 | 라라필 성분: 원천 taxonomy M15-1-7 extracted 「호박 추출물의 프로테아제 효소」 ↔ 보도 「LHA, H2sol, Lipid, INCUBE 504」 (https://www.ajunews.com/view/20250113163746036) — 덮어쓰지 않음<br>병원 도입 보도 「라라닥터 · 라라올레」 (https://www.goodkyung.com/news/articleView.html?idxno=263086)<br>화장품 · 의료기기 여부: 에이치투메디 제품 페이지(http://www.h2medi.com/doctor) 403 으로 열람 실패 · 보도에 구분 표기 없음 — 확인 불가. 원장 라라필 extracted 「호박 추출물 프로테아제 효소」 ↔ 보도 라라필 성분 「LHA, H2sol, Lipid, INCUBE 504」 — 원천 설명과 보도 성분이 다름(원장 반영은 코디 판단) |

## 질의 기록

- PHA필 ↔ 물톡스: 물톡스 필링 PHA 제품 / "물톡스" 필링 브랜드 회사 / WebFetch toxnfill 물톡스 · dashonclinic 물톡스 · 11번가 PHA 물톡스 필링 크림(내용 없음) · themalgeun.com/Multox(403)
- 라라닥터 ↔ 라라필: 라라닥터 라라필 에이치투메디 LHA PLLA / WebFetch ajunews 라라닥터 출시 · hitnews 동구바이오제약 독점 유통 · h2medi.com/doctor(403)
