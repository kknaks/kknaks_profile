# Product Log

> 제품 단위 통합 변경 로그. baseline, decision, spec, work 변경 이력을 한 곳에 모은다.

| Date | Entry | Links |
|---|---|---|
| 2026-09-03 | 문서 파이프라인 재시작 — 프로젝트 세팅 커밋(config·roles·디자인 패키지), 문서 워커 workspace=coordinator 전환 | [README](README.md) |
| 2026-09-03 | 디자인 프론트 구조 분석 완료(designer) — P-01~72 · F-1~13 · C-01~49 · S-01~34 · Q-01~42. 총계 Page 24 · 오버레이 27 · 신규 컴포넌트 ~43 · 공용 34 | [리포트](../../../../orchestration/work/docs-v1/docs-v1-design-report.md) |
| 2026-09-03 | **사용자 확정 4건**: ① 홈화면.dc.html 패키지 제외(홈·채팅은 나중, Q-27) ② 자료함 정본 = 문서함.dc.html 확정안, 탐색안 화면 10개 폐기(Q-26) ③ 메시지함 v1 범위 보류(Q-35 open) ④ 문서화 순서 = 내 업무부터 → **인증·설정부터로 번복**(업무가 설정의 유형·프로젝트를 참조) | — |
| 2026-09-03 | docs-v1 전체 계획 합의(Phase 1 영역 6건 BASE+DEC → 2 SPEC → 3 코드). 문서는 발주 없이 **논의→코디 직접 작성→리뷰**, 워커는 분석·코드만 | [_RESUME](../../../../orchestration/work/docs-v1/_RESUME.md) |
| 2026-09-03 | **BASE-004+DEC-004(문서함) 작성** — PARA 4종 고정 트리(하위 자유), **폴더↔프로젝트 자동생성 없음(두 축 독립)**, v1은 **md만 업로드·업로드만·자동저장만**, AI 색인·버전·다중형식·새문서는 v2(「v2에서 제공됩니다」), 소프트 딜리트+휴지통(복구 창구는 영역별), 용량 표시만, 즐겨찾기는 정렬까지. DEC-002·003에 첨부 md 제약 소급. OQ 5건 | [BASE-004](00-baseline/baseline-004-library.md) · [DEC-004](10-decision/decision-004-library.md) |
| 2026-09-03 | **BASE-003+DEC-003(회의록) 작성** — **사람·AI 2트랙**(회의 중 AI는 AI탭만, 제안 없음), 배치 트리거(발화량+안건 flush+상한), 증분→종료 후 전체 재정리, 종료 파이프라인(스피너→마지막 배치→통합본=정본, 재생성 없음·실패 시만 다시 생성), 실패 정책(스키마 위반 폐기·없는 업무 화이트리스트·**설계 외 에러는 fallback 금지**), 녹음 v1 마이크만·릴레이, 유형=종류 미팅(3종 enum 폐기), 반복·알림 v2. OQ 7건 | [BASE-003](00-baseline/baseline-003-meeting-notes.md) · [DEC-003](10-decision/decision-003-meeting-notes.md) |
| 2026-09-03 | Soniox 실시간 STT 조사 — 직결/릴레이, 화자분리 유의사항(실시간 정확도·endpoint detection 상충), 300분 한도 | [조사](../../../../orchestration/work/docs-v1/soniox-study.md) |
| 2026-09-03 | **BASE-002+DEC-002(내 업무) 작성** — 원본 미결 Q-04~12 전부 확정: 유형 필수, 프로젝트 N:1 무소속 허용(M:N 없음), **완료 게이트**(결과자료 or 완료 결과 필수 — 05-status §완료 4 뒤집음·디자인 정정), 일정 없는 업무(정렬 맨아래·D-day 미표시·생성일 달), 상태 셀 변경+칸반 DnD 허용, 삭제=소프트 딜리트(취소와 구분). OQ 5건 | [BASE-002](00-baseline/baseline-002-my-tasks.md) · [DEC-002](10-decision/decision-002-my-tasks.md) |
| 2026-09-03 | 업무 설정 시안 보존(orchestration/work/docs-v1/) — DEC-001 기본 유형 「색만 편집」 정정, OQ-1 시안 확정 대기로 | [DEC-001](10-decision/decision-001-auth-settings.md) |
| 2026-09-03 | **BASE-001+DEC-001(인증·설정) 작성** — 로그인(아이디+비번, 8자 문자·숫자·특수, JWT 쿠키 access 1h/refresh 7d), 계정=DB 시드(가입·찾기 없음), 유형(종류 미팅\|업무+이름+색, 기본 3종 잠금)·프로젝트(이름+색), slug 없음(자동 키), 소프트 딜리트, 목 UI 4종(소셜·목소리·연동·계정삭제=v2). OQ 6건 | [BASE-001](00-baseline/baseline-001-auth-settings.md) · [DEC-001](10-decision/decision-001-auth-settings.md) |
