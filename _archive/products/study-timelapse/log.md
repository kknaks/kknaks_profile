# Product Log

| Date | Type | IDs | Summary | Links |
|---|---|---|---|---|
| 2026-08-10 | doc-change | STL-SPEC-004, 006, 007 | Spec Coverage 에 「이관 전 구현(WP 없음)」 행 추가. 2026-06-09 이관이 계약 표면만 옮겨 구현 WP 가 없는 spec 이라, 소급 WP 대신 derived view 에 사실을 적었다 | `30-work/README.md` |
| 2026-06-21 | work-add | STL-WORK-003 | 다음날 기록이 사라져 보이는 문제 조사 결과, daily_focus 집계 날짜/Stats 기본 날짜/모바일 today 계산/세션 완료 idempotency/PUT 실패 무시 리스크를 닫기 위한 bugfix WP 추가 | `30-work/work-003-session-stats-persistence-timezone.md`, `30-work/README.md` |
| 2026-06-21 | work-add | STL-WORK-002 | TestFlight/App Review 전 모바일 Apple Sign-In 미연동 gap을 닫기 위한 WP 추가. 구현 전 capability/bundle id/backend client id 확인부터 진행 | `30-work/work-002-mobile-apple-sign-in.md`, `30-work/README.md` |
| 2026-06-20 | work-change | STL-WORK-001 | E2E 확인 결과 앱 전반 사용자 노출 한글 없음. Phase 3 완료 및 WP done 처리 | `30-work/work-001-english-app-copy-audit.md`, `30-work/README.md` |
| 2026-06-20 | work-change | STL-WORK-001 | 저장 완료 후 back 시 preview로 돌아가는 navigation stack 이슈 방지. saving 화면 hardware back/error OK를 home 이동으로 보강, 타입체크 통과 | `30-work/work-001-english-app-copy-audit.md` |
| 2026-06-20 | work-change | STL-WORK-001 | Phase 2 영어 copy 교체 완료. 모바일 사용자 노출 패턴 grep 0건, `npx tsc --noEmit` 통과. 실제 flow QA는 남음 | `30-work/work-001-english-app-copy-audit.md`, `30-work/README.md` |
| 2026-06-20 | work-change | STL-WORK-001 | Phase 1 copy audit 완료. local clone 확인 후 모바일 사용자 노출 한글 문자열 수정 대상/제외 대상 분리 | `30-work/work-001-english-app-copy-audit.md`, `30-work/README.md` |
| 2026-06-20 | work-add | STL-WORK-001 | 모바일 앱 전반 한글 알림·모달·사용자 노출 문구를 영어로 통일하는 copy audit/polish WP 추가. 30-work index를 Status Board/Spec Coverage 구조로 갱신 | `30-work/work-001-english-app-copy-audit.md`, `30-work/README.md` |
| 2026-06-08 | decision-add | STL-DEC-001~022 (003 결번) | medi_docs ADR 21건 → 10-decision 큐레이션 이관(probe). 각 결정 코드 grounding 포함, 모두 accepted | `10-decision/README.md` |
| 2026-06-09 | spec-add | STL-SPEC-001~013 (011 결번) | medi_docs spec 12건 → 20-spec 큐레이션 이관. 계약 표면만(구현 본문 제외), 각 spec 코드 grounding. 10건 implemented / 2건 in_dev(SPEC-006 period_type, SPEC-009 모바일 Apple). decision↔spec wikilink 연결, 10-decision README Spec 컬럼 승격 | `20-spec/README.md`, `10-decision/README.md` |
