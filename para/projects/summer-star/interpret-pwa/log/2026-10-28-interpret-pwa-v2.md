# 작업 요약 — interpret-pwa-v2 (interpret-pwa)

기간: `2026-10-27` ~ `2026-10-28`
결과: 머지 · 배포 완료 — 코드 `kknaksss/interpret-pwa#10`(main 17c26b5 · 시드 2026-10-27.6) · infra `MediSolveAIDev/k8s_infra_mac#35` · `#36` · 문서 `kknaks/kknaks_profile`(DEC D-39 ~ D-41 · SPEC 0.6.1 — 이 PR 과 아카이브 PR)

## 1. 무엇을 했나

통키 사전은 Procedure Hub 157 term 이 전부였고, 대륙 중국어는 출처 검증 없이 Procedure Hub 값 그대로였다. 사용자 요청 세 가지 — 대륙 중국어를 중국 클리닉에서 확인 · 사전에 없는 시술을 현지 피부과 표기로 7개 언어 모두 추가 · 「어떤 통역을 했는지」 내부 검토용 기록 — 를 한 작업으로 묶었다.
언어권별 조사 워커 셋(대륙 · 일본/영어/대만 · 태국/베트남/홍콩)을 동시에 돌려 새 시술 13개 × 7개 언어와 기존 표기 정정을 근거(URL)와 함께 받고, 처분표로 닫아 시드 `.6`(170 term)으로 넣었다. 통역 기록은 화면 · API 없이 back PVC 에 날짜별 JSONL 로 쌓고 7일 뒤 지운다. 배포에서 PVC 고정 노드의 CPU 예약이 꽉 차 새 pod 가 못 뜨는 문제를 만나 back 예약을 낮춰 풀었다.

## 2. 적용한 기술·개념

- **언어권 병렬 조사 → 처분표 → 시드** [[translation-glossary-normalization]] — 조사 워커 셋을 같은 브리프 틀로 동시에 돌리고, 새 시술 목록은 한 워커(r1)가 확정해 나머지가 따르게
  - 왜: 언어마다 현지 출처가 다르다(대륙 = NMPA · 업계 플랫폼, 대만 = 衛福部 허가 목록 · 클리닉 가격표, 태국 · 베트남 = 영문 메뉴). 목록이 워커마다 다르면 합칠 수 없다 → 목록 확정을 한 곳에
  - 무엇이 어려웠나: 처분할 것이 세 리포트 합쳐 20건 + planner 가 처분 밖이라 남긴 5건(OQ-018). 대부분 이미 정한 규칙(현지 허가명 우선 · 현지에 없으면 영문 · 모호어 제외 · 출처 2+ 만 reviewed)으로 답이 나와 기본값 통보로 닫았다. 사전에 없던 규칙 하나 — **홍콩(yue)은 대만과 독립**(같은 번체라도 Neuramis 優美施 · AestheFill 精靈針 처럼 다르게 부름)
  - 근거: `research-r1-zh-report.md` · `research-r2-ja-en-tw-report.md` · `research-r3-th-vi-yue-report.md` · `research-dispositions.md` · DEC D-39 · D-40
- **현지 공식명과 「번역 단계에서 만든 이름」 가르기** [[chinese-script-conversion]] — 대륙 zh 는 Procedure Hub 에 「검수됨」 표시가 있었지만 근거를 따로 찾았다
  - 무엇을: 대륙 공식명과 다른 6개(리즈톡스 解索橙 · 레티보 乐提葆 · 엘라비에 艾莉薇 · 스컬트라 塑妍萃 · 써마지FLX 超玛吉FLX · 리쥬란 丽驻兰) · 대륙 미허가 톡신(나보타 · 메디톡신 · 뉴럭스 · 타임버스) · 한국 전용 음역명(时光巴士 · 艾芙莱恩 · 贝尔菲恩 …)은 대륙 근거 0건 → 영문 name · 옛 표기 alias
  - 무엇이 어려웠나: 新氧 · 바이두 · 知乎는 봇 차단으로 못 읽었다 → 업계 플랫폼 · 경제지 · 공시 · 대리상 페이지 원문(curl)으로 대신. 못 읽은 곳은 리포트에 그대로
  - 근거: `research-r1-zh-report.md` §5 · §7
- **브랜드 별칭이 세대를 덮는 오역** [[context-catalog-injection]] — 한국어 별칭 「써마지」를 FLX 에 두었더니 새 term 「써마지 CPT」 문장이 대만어 鳳凰電波(FLX)로 번역됐다
  - 왜 이렇게 됐나: Soniox `translation_terms` 는 우리가 기대한 「더 긴 짝 우선」으로 동작하지 않았다. 대륙 zh 에서 热玛吉 단독을 뺀 것과 같은 이유가 한국어 쪽에도 생긴 것 — 새 term(CPT)을 넣는 순간 기존 별칭이 모호어가 된다
  - 무엇을: ko 별칭 「써마지」 삭제(OQ-018 ⑤ 처분을 실물 결과로 뒤집음) → zh-Hant 「써마지 CPT」 → 黃金電波(맞음)
  - 근거: `live-check-wp16-newterms.json` · `-newterms-2.json` · `wp16-be-report.md` 「처분 2」
- **한도는 언어별로** [[empirical-limit-probing]] — 모든 언어를 가장 작은 실측치(ja) 하나로 자르면 다른 언어가 쓸데없이 잃는다
  - 무엇을: 시드 `.6` 로 7개 언어 통과 최대치를 다시 이분 탐색(en 26,027 · ja 22,688 · zh-Hant 24,099 …) → **언어별 × 0.9** 표 한 곳(`langs.CONTEXT_MAX_CHARS`) · env 는 값이 있으면 모든 언어를 덮는 하나의 값. zh-Hant 역방향 별칭 손실 63 → 33 · th 38 → 0
  - 근거: `live-check-wp16-ceiling.json` · `-seed-3.json` · `back/app/service/interpret/langs.py`
- **화면 · API 없는 내부 기록** [[minimal-api-surface]] — 「어떤 통역을 했는지」 보려는 내부 검토용
  - 왜: D-37(밖으로는 통역만)을 지키면서 기록을 남기려면 읽는 길을 서버 밖에 두지 않는다 → 날짜별 JSONL(세션 시작/발화/끝 · 원문 · 번역 · 걸린 term id) · 음성 · 토큰 · IP · 계정값 없음 · 7일 삭제(기동 + 하루 한 번) · 쓰기 실패는 통역을 끊지 않음 · 꺼내기 = kubectl. 허용 경로 6개 고정 시험이 그대로 통과하는 것으로 「새 입구 0」 을 확인
  - 근거: `back/app/service/records.py` · `back/tests/test_records.py` · `test_api_surface.py` · DEC D-41 · SPEC §5.9
- **PVC 고정 노드의 CPU 예약 포화** [[kubernetes-workload]] — local-path 가 `lima-worker-1` 디스크에만 PV 를 만들어 저장이 필요한 앱이 그 노드에 몰렸다
  - 무엇이 어려웠나: 배포 뒤 새 back pod 가 Pending · PVC 도 `WaitForFirstConsumer` 로 Pending → 이벤트 「1 Insufficient cpu」. 실제 사용량이 아니라 **requests 합**(3,950m / 98%)이 꽉 찬 것 — 메트릭 서버가 없어 사용량은 못 봤다. 롤링 업데이트라 옛 pod(worker-2)가 계속 응답해 끊김은 없었다
  - 무엇을: 우리 back request 100m → 50m(통역 중계만 · limit 1 그대로) · 다른 앱은 건드리지 않음
  - 근거: infra #36 · `wp17-infra-report.md`

## 3. 막혔던 것 / 사고

- **처분 하나를 실물 앞에서 정했다가 뒤집음**(OQ-018 ⑤ 「써마지」 유지) → 「FLX 가 지금 세대라 대부분 FLX」 라는 추측이었다. 새 term 을 넣을 땐 기존 별칭이 새 term 을 덮지 않는지 실물로 먼저 본다
- **PVC 노드 자리 부족** → 차트 검증(lint · template · kubeconform)은 다 통과했지만 스케줄링은 클러스터에서만 드러난다. 저장 공간을 새로 붙이는 배포는 그 노드의 `Allocated resources` 를 먼저 본다
- **코디 핸들이 또 바뀜**(98e52 → ab9c7) → 브리프의 「보고 직전 제목으로 찾기」 로 보고는 유실 없음
- **중국 사이트 차단**(新氧 · 바이두 · 知乎) → 다른 1차 출처로 대신했지만, 대륙 손님이 가장 많이 보는 플랫폼의 표기는 확인 못 함

## 4. 결정

| 날짜 | 결정 | 왜 |
|---|---|---|
| 2026-10-27 | 사전 밖 시술 13개 × 7개 언어 추가 · 현지 피부과 표기 · 울트라셰이프 제외(D-39) | 사용자 「없는 시술은 모든 언어 추가 · 현지 피부과에서」 · r2 처분 7(단종 · 드묾) |
| 2026-10-27 | 대륙 zh 검증 · 공식명 · 한국 전용은 영문(D-40) | 사용자 「중국 피부과들 접속해서 확인」 |
| 2026-10-27 | 통역 기록 — 서버만 · 화면 · API 없음 · 7일(D-41 · Scope 개정) | 사용자 「어떤 통역을 했는지 궁금 · 화면이 필요 없다 · 내부 검토용」 |
| 2026-10-27 | ~~ko 별칭 「써마지」 유지(OQ-018 ⑤)~~ → 삭제(10-27 실물 ⑳ 로 뒤집음) | 「써마지 CPT」 → FLX 오역 |
| 2026-10-27 | 한도 = 언어별 실측 × 0.9 | 공통 최소값이 zh-Hant 별칭 63 을 버림 |
| 2026-10-28 | back cpu request 50m | PVC 노드 예약 98% |

## 5. 날짜별 로그

- `2026-10-27` 착수(D-39 ~ D-41) · 조사 3갈래 병렬(새 시술 14 → 13 확정) · 처분 · SPEC 0.6.0 · WP16(시드 .6 · 기록 · 처분 2 · 3) · WP17(PVC) · 코드 #10 · infra #35
- `2026-10-28` 배포 — PVC 노드 CPU 포화로 Pending → infra #36(50m) → 롤아웃 · 시드 .6 로드 · 기록 파일 확인 · SPEC 0.6.1 · 마감

## 6. 산출물

- code PR: https://github.com/kknaksss/interpret-pwa/pull/10
- infra PR: https://github.com/MediSolveAIDev/k8s_infra_mac/pull/35 · /pull/36
- spec PR: kknaks/kknaks_profile — DEC D-39 ~ D-41 · SPEC 0.6.1(이 마감의 문서 PR)
- 리포트: `research-r1-zh-report.md` · `research-r2-ja-en-tw-report.md` · `research-r3-th-vi-yue-report.md` · `research-dispositions.md` · `wp16-be-report.md` · `wp17-infra-report.md` · `live-check-wp16-*.json` · `tts-samples/`(합성 음성 — 브랜드명만)

## 7. 잔여

- **OQ-019 대문자 영문 TTS** — `tts-samples/` 의 EXION · DENSITY · EMFACE 를 사람이 듣고 표기(대문자 / 첫 글자만) 결정
- **PWA 설치 안내** — Android 설치 단추 · iPhone 「홈 화면에 추가」 안내(사용자에게 제안만 함)
- **대륙 주요 플랫폼(新氧 등) 표기 미확인** · 뉴럭스 정체 · 리쥬란 상자 표기(白盒/黑盒/红盒) 출처
- **zh-Hant 역방향 별칭 33 손실** — 사전이 더 커지면 언어별 한도 재측정
- **lima-worker-1 CPU 예약 98%** — 다른 앱 requests 정리나 노드 자원은 사내 인프라 판단
- **데모 원탭 로그인 끄기**(이전 작업부터 남음)
- `.6` 대만 「검수 전」 항목 · 사람 목소리 E2E(이전 작업부터 남음)
