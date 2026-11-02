# [planner] SPEC-001 0.4.0 · WORK-001 — D-22 ~ D-33 동기 · 우리 용어집 시드(D-33)

너는 interpret-pwa planner 다. 역할 · allowed_paths · 검증 · 보고 방식은 원 브리프 그대로: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md`
맥락이 없으니 아래 파일만 믿어라.

## 입력 (정본)
- DEC-001 **D-22 ~ D-33**: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` (0.3.0 뒤에 추가된 것 전부)
- 지금 SPEC 0.3.0: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md`
- 실제 구현(배포된 main d0a91a7 · read-only): `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/` — 구현이 이미 D-22 ~ D-32 를 반영했다. SPEC 을 코드에 맞춰 적되, 다르면 DEC 가 이긴다
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/` 의 `wp6-*-report.md` · `fix-phone1-*` · `fix-phone2-*` · `fix-phone3-*` · `live-check-wp6-2026-10-26.json`(한도 실측 → 기본값 18832)
- 시안: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/design/` (D-22 ~ D-24 · D-29 · D-30 · D-28 반영본)

## 고칠 것
1. **D-22 ~ D-32 를 SPEC 에** — §2.4(INTERPRET_DEMO_LOGIN · GLOSSARY_CONTEXT_MAX_CHARS 18832 = 실측 근거) · §3(데모 로그인 API · config) · §5.5(lang 7개 · zh-Hant · 목록 표시 이름 · 한국어 이름 중국어/대만어) · §5.6(번체 변환 언어별: yue s2tw · zh-Hant s2twp) · §7(원 위 외국어 안내 · 원 64/88 · 원 줄 140 · 말풍선 · 자동 스크롤 · ↓ 최신 · 초기화 · 언어 목록 180° 자체 목록 · 데모 로그인 화면 · 로그인 입력 16px) · §10 OQ 정리
2. **D-33 우리 용어집 시드** — §4 를 새로 쓴다: 시드 파일 경로 · **JSON 스키마**(term · entries · 필드 이름 · 필수/선택 · 출처 · 검수 · 버전) · 기동 때 읽기 · 실패 동작(시드가 깨지면 기동 실패가 맞는지 vs 빈 용어집 — 시드는 우리 파일이니 시험으로 막고 기동 실패로 권장) · context 조립(정방향 · 역방향 · 별칭 · 한도 · 줄이기 순서) · TTS 는 현지명(괄호 없음 — D-19 괄호 제거는 시드 변환 뒤 필요 없는지 판단) · 용어집 메뉴 API 모양(현지명 · 별칭 · 검수 표시) · **첫 가져오기 스크립트**(Procedure Hub matrix → 시드 · 괄호 분해 규칙 · zh-Hant 초안 s2twp · 검수 안 됨 표시 · 한 번만 돈다) · Procedure Hub 런타임 호출 제거 · 시험 항목 · 실물 재확인(6개 + zh-Hant 한도 · 써마지 · 울쎄라 정방향/역방향)
3. **WORK-001** — WP9(backend: 시드 스키마 · 가져오기 스크립트 · 로더 · context · 메뉴 API · 시험 · 실물) · WP10(frontend: 메뉴에 현지명 · 별칭 · 검수 표시 — 필요한 만큼만) · WP11(재배포 · 폰 확인) 행 추가 · 완료 조건 · 부분 검증
4. SPEC 0.3.0 → 0.4.0 · 변경 이력. DEC 는 고치지 않는다. 비밀값 · 계정값 0

## 완료 보고
원 브리프 §9 그대로(코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration').
