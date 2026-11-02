# [planner] SPEC-001 0.3.0 · WORK-001 — 시안 정본 · Soniox 실물 결과 · D-18~D-21 반영

너는 앞서 SPEC-001 · WORK-001 을 쓴 interpret-pwa planner 다. 역할 · allowed_paths · 검증 · 보고 방식은 원 브리프 그대로:
`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md`

## 입력 (정본)

- DEC-001 **D-18 ~ D-21** (새로 추가됨): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- **확정 시안** — 코드 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/design/` (README · `project/*.dc.html` 17화면). designer 가 D-21(헤더 「Tongky」 · 로그인 「통키」 · final:false gray-600)을 지금 반영 중 — 그 세 가지는 DEC 로 적으면 된다
- 시안 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/design-report.md` (특히 「제안」 1~8 — D-21 이 1 · 2 · 3 · 4 · 5 를 채택. 6 은 구현 메모, 7 원 크기는 시안 값, 8 은 시안 없음 → 기존 SPEC 문구 유지)
- **Soniox 실물 결과**: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/live-check-2026-10-26.json` (① ~ ⑦ 모두 통과 · 6개 언어 거절 0 · th 9,900자 최대 · ⑦ 거절 0.458초 · 오디오 전)
- 코드 리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/review-code-report.md` (FAIL-1 · WARN 1~6) · 피드백 묶음: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/e2e-feedback-batch-1.md`

## 고칠 것

1. **§6 · §7 을 시안에 맞춘다(D-20 · D-21)** — `data-product="ceramique"` + `ceramique-theme.css`(primary `#2498bd`) · 외국어 = purple · 회전 화살표 아이콘 · 앱 이름 · 시안에서 더한 요소 · 원 크기(시안 값) · final:false gray-600 · 오버레이가 헤더를 덮는지(시안 기준 — 리뷰 WARN-3 닫기). 화면마다 시안 파일명을 근거로 단다
2. **§4.3 · §4.4 역방향 용어(D-18)** — 고른 언어 표기 → ko 짝을 `translation_terms` 에 더하는 규칙 · 중복 · yue 처리(t2s) · 한도(`GLOSSARY_CONTEXT_MAX_CHARS` 10000 유지)를 넘을 때 `terms` 부터 줄이는 순서 · 실물 재확인 항목을 §9.3 에 추가(6개 언어 거절 0 + 역방향 적중)
3. **§5 TTS 괄호 제거(D-19)** — TTS 입력에서만 괄호 부분(전각 · 반각) 제거 규칙 · 자막은 그대로 · 시험 항목
4. **§9.3 실물 결과 기록** — ① ~ ⑦ 결과를 표로, `STT_CONFIG_CHECK_SEC` 2초 · `GLOSSARY_CONTEXT_MAX_CHARS` 10000 확정. §10 OQ-002 · OQ-003 · OQ-009 닫기(D-18 · D-19)
5. **리뷰 WARN 반영 자리** — WARN-1(용어집 URL 오류면 기동 실패 → 빈 용어집) · WARN-2(ASCII 아닌 토큰 500 → 401) · WARN-4(출력 중 언어 표시 시점) · WARN-5(로그인 env 비었을 때 기동 경고 로그 · 응답은 같은 401) · WARN-6(용어집 10초는 전체 시간) 을 계약 문장으로. FAIL-1(멈춤 뒤 남은 TTS 조각 버림)도 §7.4 에
6. **WORK-001** — WP6 행을 이 묶음으로 구체화(backend: D-18 · D-19 · WARN-1·2·5·6 · 실물 재확인 / frontend: 시안 맞춤 · 테마 · 아이콘 · 이름 · FAIL-1 · WARN-4 · PWA manifest 이름) · 완료 조건 · 부분 검증
7. SPEC version 0.2.0 → 0.3.0 · 변경 이력. DEC 는 고치지 않는다

## 완료 보고

원 브리프 §9 그대로(코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration' 으로 확인).
