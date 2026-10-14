# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-10-10 | 제품 착수. 사용자 입력(기능별 front/back 실험 · 고객 데모 · 빈 레포 `kknaksss/cc-prototype`)을 BASE-001 로, 대화에서 닫은 것(FastAPI + Next.js · 기능 완전 독립 · 기능 내용은 이름만)을 DEC-001(proposed)로. 배포 대상은 OQ-001 로 열어 둠. 코드 미착수 | [입력](00-baseline/baseline-001-feature-lab.md) · [결정](10-decision/decision-001-feature-lab.md) |
| 2026-10-10 | sts 아이디어를 BASE-002(아이디어 노트)로. Soniox 공식 문서 조사 결과(STT 번역 내장 + TTS 두 연결 · 한국어 전부 지원 · 공식 FastAPI 데모 · TTS 동시 3 한도) 요약 포함. 결정 없음 | [입력](00-baseline/baseline-002-sts-idea.md) · [조사](../../../../orchestration/work/sts-prototype/research-soniox-report.md) |
| 2026-10-10 | cc 아이디어를 BASE-003(아이디어 노트)로 — 병원 현황판, 도면 위 직원·의사·상담사·고객 실시간 위치. 참고 도면 사진 assets/ 에 보관. 사용자 「cc 에 다 통합」 — sts 가 cc 로 묶일 수 있음(방식 미정). 결정 없음 | [입력](00-baseline/baseline-003-cc-idea.md) |
| 2026-10-10 | 예약 아이디어를 BASE-004 로 — AS-IS(SNS 다섯 갈래 + 병원과 카톡 · 결과는 스크린샷) → TO-BE(Linky 가 예약폼을 cc 로, 병원은 cc 에서 KOS 등록·결과 저장). 흐름도 2장 assets/ 보관. BASE-003 에 「도면·시술실 정보는 나중에 매칭」 추가. 결정 없음 | [입력](00-baseline/baseline-004-reservation-idea.md) |
| 2026-10-10 | BASE-004 사용자 확인 — 흐름 해석·색 구분 맞음. 스크린샷은 「스냅샷 성격의 기록」으로 필요(KOS API 응답이 될 수도, 변경 요청 대비), 형태는 기능 구현 때 | [입력](00-baseline/baseline-004-reservation-idea.md) |
| 2026-10-10 | 인플루언서 협찬 아이디어를 BASE-005 로 — Casty 탐색 → Linky 대화 생성(아웃바운드). 채널별 「먼저 말 걸기」 제약은 확인 전 메모로만. 결정 없음 | [입력](00-baseline/baseline-005-influencer-outreach-idea.md) |
| 2026-10-12 | DEC-001 개정 — 사용자 지시(researcher 세션에서). D-02 첫 기능 sts·cc → cc, D-06 신설(sts 는 cc 직원용 화면 안의 통역 기능 · Soniox 연결은 cc/back). OQ-004(통역 넣을 화면: 직원용 뷰 vs 시안 「Ceramique 의사 모바일」) · OQ-005(코드 레포 sts/ 뼈대 처리) 추가. 모바일 주의: Soniox 자동 포맷에 mp4 없음(iOS MediaRecorder) | [결정](10-decision/decision-001-feature-lab.md) |
