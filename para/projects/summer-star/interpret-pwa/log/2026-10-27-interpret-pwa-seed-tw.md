# 작업 요약 — interpret-pwa-seed-tw (interpret-pwa)

기간: `2026-10-27` ~ `2026-10-27`
결과: 머지 · 배포 완료 — 코드 `kknaksss/interpret-pwa#9`(시드 2026-10-27.5) · infra `MediSolveAIDev/k8s_infra_mac#34`(back 2a9d5a5) · 문서 `kknaks/kknaks_profile#109`(DEC-001 D-38)

## 1. 무엇을 했나

통키 마감 뒤 사용자가 「대만명 못 찾은 80개가 뭐야 · 리즈톡스 대만에서 안 써?」를 물었다. 대만 클리닉 사이트를 직접 조사하게 해서(톡신 허가 목록 · 사이트 3곳 tresure-clinic · muskin · koreabeautydream 전수 311쪽) 사전의 대만어(zh-Hant) 40 term 을 고쳤다 — 한국 톡신은 대만 허가명(保提拉 · 優力柔 · 娜柏塔), 대만에 없는 한국 전용 제품 19개는 영문 브랜드명, 대륙식 · s2twp 오변환 표기 정리, 모호한 별칭 제거. 백엔드 이미지만 다시 배포했다.

## 2. 적용한 기술·개념

- **수출명 ≠ 국내명 — 현지 허가명으로 매핑** [[translation-glossary-normalization]] — 한국 톡신은 대만에 수출명으로 들어가 있다(보툴렉스 · 레티보 → Letybo 保提拉 · 메디톡신 → Neuronox 優力柔 · 나보타 → 娜柏塔)
  - 왜: 한국 국내명은 대만 클리닉에서 안 쓰인다. 사전 1차는 클리닉 색 별명(白毒 · 粉毒 · 綠毒)이 대표 이름 자리에 앉아 있었다 → 허가명을 name, 수출명 · 별명을 alias
  - 무엇이 어려웠나: 「목록에 없음」은 부재 근거일 뿐이다(리즈톡스). 대만 클리닉 6곳이 적은 衛福部 허가 6종 목록과 허가증 번호로 판정하고, 판매 안 함을 명시한 출처가 없다는 점을 그대로 남겼다
  - 근거: `research-kr-brands-report.md` · `back/seed/glossary.json` ph-027 · 031 · 041 · 042 · 코드 #9
- **현지에 없는 제품은 영문 브랜드명** [[translation-glossary-normalization]] — 대만 클리닉 3곳 어디에도 한국 전용 제품(리즈톡스 · 신펄 · 더채움 · 리쥬란 주사 등)의 중문명이 없다(대만 허가 품목만 판다)
  - 왜: 대만판 플랫폼도 한국 제품은 영문 + (韓國產)로 쓴다 → 대만 손님은 영문으로 듣고 말할 가능성이 크다. 중문명을 지어 넣으면 틀린 짝이 된다
  - 근거: `research-tresure-report.md` §0-3 · D-38 ②
- **사이트 전수 대조와 모호어 분리** [[chinese-script-conversion]] — 한 사이트를 sitemap 으로 전부 받아 사전 term 과 같은 것 / 새 후보 / 모호한 말로 나눔
  - 무엇이 어려웠나: 「音波拉提」가 울쎄라 alias 이면서 HIFU name 으로 이중 등록 · 「鳳凰」 계열(鳳凰電波 = 써마지 · 鳳凰光 = 레이저) · 「黃金微針」(바늘 종류) · 「素顏針」 vs 「素妍針」(한 글자 차이로 다른 제품) — 잘못 걸리면 다른 시술로 번역되므로 넣지 않음. s2twp 오변환(匯入 · 專案 · 裝置)이 1차 정리 때 「鐳射」만 고쳐서 남아 있었다 → 이번에 전부
  - 근거: `research-tresure-report.md` 표 C · `seed-tw-be-report.md`

## 3. 막혔던 것 / 사고

- **1차 오변환 정리가 덜 됐다** — D-35 때 「鐳射 → 雷射」만 일괄로 고치게 해서 같은 계열(匯入 · 專案 · 裝置)이 배포본에 남았다 → 「못 찾은 80」 질문에 답하며 배포 시드를 직접 grep 해서 발견. 오변환을 고칠 땐 한 단어가 아니라 그 변환기가 만든 값 전체를 다시 만든다
- **브리프 범위 밖 판단**(포텐자 name 黃金微針) — 브리프가 alias 만 지시해서 워커가 멈춤 → 모호어 규칙(D-38 ④)으로 name 無限電波(검수 전) · 黃金微針 삭제

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-27 | 대만어 사전 2차 — 톡신 대만 허가명 · 한국 전용 제품 영문 · 대륙식/오변환 정리 · 모호어 제거 · 사전 밖 새 시술은 안 넣음 · zh(대륙) 그대로(D-38) | 사용자 「대만클리닉으로 검색해바」 · 「한국 제품은 그럼 영어로 표기하자」 |
| 2026-10-27 | 포텐자 zh-Hant = 無限電波(검수 전) · 黃金微針 삭제 | 표 C-3 모호어 |

## 5. 날짜별 로그

- `2026-10-27` 한국 톡신 대만 조사 → 대만 클리닉 3곳 전수 대조 → 시드 .5(zh-Hant 40 term) · 코드 #9 · infra #34 · 문서 #109 · 실물 保提拉 → 레티보 · 彩虹肉毒 → 나보타

## 6. 산출물

- code PR: https://github.com/kknaksss/interpret-pwa/pull/9
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/34
- spec PR: https://github.com/kknaks/kknaks_profile/pull/109
- 리포트: `research-kr-brands-report.md` · `research-tresure-report.md` · `seed-tw-be-report.md`

## 7. 잔여

- 사전 밖 새 시술(써마지 CPT · 소프웨이브 · 엑시온 · 프로파일로 · 쥬베룩 · 스컬트라 · 뉴라미스 · 엠페이스 등) — 넣을지 · 범위는 사용자 결정(`research-tresure-report.md` 표 B)
- 뉴럭스(ph-028)가 대만 Neuronox 와 같은 제품인지 불명
- zh(대륙)의 한국 전용 제품 표기(Procedure Hub 값 그대로) — 영문으로 바꿀지
- infra `values-prod.yaml` 에 `back.imageTag` 오버라이드가 다시 있다 — 다음에 back · front 가 같이 빌드되면 `image.tag` 하나로 정리
