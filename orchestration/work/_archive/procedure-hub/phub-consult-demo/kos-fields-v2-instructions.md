# [researcher] KOS 응답 칸 전수 · JSON v2 · 매핑 초안 갱신

앞 판(`research-kos.md` · `research-kos-map.md`)에 이어서. **KOS API 다시 부르지 마라** — 원응답은 코디가 `reference/2026-11-19-myeongdong-kos/raw/`(A ~ F · gitignore)로 옮겨 두었다. 이 원응답만 읽는다.

## 왜
가이드 §4 출력 꼴에 없는 칸을 빼고 옮겨서, **시술 항목(medicalService) `description` 에 있던 병원 확인 배합**(세라핏 지방분해주사 15 항목 — 「하프셀라인 100cc + … + 밀리핏 1A + …」)을 놓쳤다. 사용자 지시: **KOS 가 주는 데이터를 먼저 전부 본다.**

## 할 일
1. **칸 전수** — raw A ~ F 의 모든 키 경로(중첩 · 배열 안까지)를 표로: 경로 · 타입 · 채워진 수 / 전체 · 서로 다른 값 수 · 값 보기 3개(이름 · 코드 · 짧은 글만 — **가격 원값 · 사람 이름 · 전화 · 토큰 · 테넌트 id 금지**, 가격 칸은 「숫자」 로만) · 지금 JSON v1 에 옮겼나(○/✗). 특히 description · caution · badges · translsMap · promotionConfigurations · displayPeriod/offeringPeriod · frequentlyUsedOption · 상품/옵션 단위 medicineAndMachines · targetCountryCodes. 「-」 같은 빈 표지 값은 따로 센다.
   → `orchestration/work/phub-consult-demo/research-kos-fields.md`
2. **JSON v2** — v1 꼴(가이드 §4) 그대로 두고, 1 에서 ✗ 였던 칸 중 **상품 정보에 쓸 수 있는 것을 전부** 더한다(최소: 시술 항목 `description` · `caution` · 상품/옵션 `description` · `caution` · 기간 · 배지 · 번역 · 상품/옵션 단위 약품·기기). 이름은 snake_case · 빈 표지 「-」 는 null. 개인정보 · 테넌트 id 0. 스크립트 `fetch_kos_products.py` 의 `--from-raw` 경로를 고쳐 다시 만든다(호출 코드는 건드리지 마라).
   → `reference/2026-11-19-myeongdong-kos/myeongdong-kos-products-20261119-v2.json`(gitignore) · v1 은 두라.
3. **설명 칸에서 매핑 근거 찾기** — 채워진 description · caution 전부를 KOS 시술별로 모아, 약품 · 기기 · 성분 이름이 허브 제품(`s_product` · 로컬 PG SELECT)에 닿는지 셈.
4. **매핑 CSV 갱신** — `kos-procedure-map-draft-20261119.csv` 를 고쳐 쓴다(같은 칸 · 124 줄). 사용자 결정(11-19):
   - 매핑 방식 (A) PRC + SITE(+ CAS 참고) + PRD.
   - **세라핏 지방분해주사(시술 항목 설명에 밀리핏 1A) → PRC-123 DCA 지방분해 주사 + 부위 + 제품 PRD-729 밀리핏주사.** basis 에 「KOS 시술 항목 설명(병원 확인 8/25) 배합 · 밀리핏 1A = PRD-729 DCA · 보조 성분(아미노필린 · 카르니틴 · 알포콜린 등) 있음」. status = 확실. 부위는 이미 있는 부위 규칙 그대로(부위 없는 줄은 비움 · 「애매」 유지).
   - 벨라콜린 이중턱은 이미 PRC-123 · PRD-724 — 세라핏 이중턱과 같은 KOS 시술이면 제품 칸에 둘 다.
   - 3 에서 새로 닿는 근거가 있으면 반영하고 basis 에 「설명 칸」 이라 적는다. **추정 금지.**
   - 제모 20 줄은 사용자가 「초안대로」 확정 → status 는 그대로 두되 note 에 「사용자 11-19 초안대로 확정」.
   - CSV 에 칸 하나 더: `kos_item_descriptions`(그 KOS 시술의 시술 항목 설명 · 고유 · ` / ` 로 이음 · 없으면 빈칸). 가격 칸은 넣지 마라.
5. `research-kos-map.md` 의 한눈 표 · status 수 · 정할 것을 새 CSV 에 맞게 고친다(바뀐 줄 목록 절 하나 추가).

## 하지 말 것
KOS · 허브 · 앱 쓰기 0 · 커밋 0 · 서브에이전트 0 · 리포트 · CSV 에 가격 원값 · 개인정보 0.

## 검증
CSV 124 줄 · status 합 124 · 허브 코드 전부 실재(SELECT 대조) · v2 JSON 의 counts 가 v1 과 같음 · grep 으로 이메일 · 토큰 · 휴대폰 꼴 0 · `git status --short` 로 변경이 위 파일뿐.

## 완료 보고
앞 태스크와 같은 2채널(worker_done 인박스 + 코디 터미널 주입) · subject 「researcher 완료: KOS 칸 전수 · v2 · 매핑 갱신」.
