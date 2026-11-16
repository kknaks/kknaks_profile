# [planner] 마감 문서 동기 — SPEC-001 0.5.0 · WORK-001 · README (D-35 ~ D-37 · 운영 장애)

너는 interpret-pwa planner 다. 역할 · 검증 · 보고는 원 브리프: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md`. allowed_paths: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/README.md`. DEC · log.md 는 건드리지 마라.

## 입력
- DEC-001 **D-35 · D-36 · D-37**(D-32 · D-13 은 뒤집힘 표시) — `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 배포된 최종 코드 main fe8475e(read-only): `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/`
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/research-tw-names-report.md` · `d35-be-report.md`(운영 장애 절 — TTS keepalive `{}` → Soniox invalid_request 'Missing stream_id' · 2026-10-27 02:07 · 고침) · `d36-fe-report.md` · `design-r7-report.md` · `d37-be-report.md` · `d37-fe-report.md` · `design-r8-report.md`
- 배포(코디): 코드 PR #5 ~ #8 · infra #29 · #30 · #32 · #33 · 최종 이미지 back · front fe8475e(image.tag 하나) · 확인: health/me {ok} · /api/glossary 404 · docs 404 · wss ready

## 고칠 것
1. SPEC 0.4.1 → **0.5.0**: §4 시드(대만명 · reviewed 규칙 · zh 구어 별칭 · 모호어 제외 · version .4) · §4.6/§4.7 **용어집 메뉴 API 삭제**(D-37) · §5.6 zh-Hant s2tw + 激光→雷射(D-35 · s2twp 폐기) · §5 오류 문구 일반 4종 · TTS keepalive 형식 `{"keep_alive": true}` 과 다른 stream_id 오류 처리(장애 근거) · §3 me/health 응답 · docs 끔 · 허용 경로 6개 · §7 누르고 말하기(D-36 · 시안 Mode-Auto-Idle · PTT-Ready · PTT-Pressed) · 메뉴 로그아웃만 · §9.5 배포 기록 갱신 · §10 OQ 정리(남은 것: 사람 목소리 E2E · 못 찾은 대만명 80 · 데모 로그인 끄기)
2. WORK-001: WP12 이후 행(D-35 · 장애 · D-36 · D-37) done · PR 번호 · 남은 것
3. README 현재 상태 · 최근 로그
4. 비밀값 · 계정값 0

## 완료 보고
원 브리프 §9(코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA').
