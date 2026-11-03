# @day-frontend — 규칙

## 서버 렌더링 + HTMX (본: centurion `docs/development/medikit-htmx-design-guide.md`)
- 화면은 서버가 Jinja2 로 그린다. 전체 페이지 = `base.html` 확장 + partial include, 부분 갱신은 `partials/*` 조각을 HTMX 로.
- HTMX 요청(`HX-Request`)이면 조각만, 아니면 전체 페이지 — 한 라우트가 둘 다 처리한다(centurion `web.py` 방식).
- JS 는 프레임워크 없이 바닐라 한 파일 — 이벤트 위임 + `data-*` 속성. **인라인 스크립트 · `eval` 금지**(CSP).
- `htmx.min.js` 는 벤더링한다(CDN 금지). 라이선스 파일을 같이 둔다.
- 스타일은 medikit 토큰 · `ui.html` 매크로의 클래스만. 손 CSS 로 흉내 내지 않는다. 빌드된 CSS 는 커밋하고 손으로 고치지 않는다.
- POST 계열은 CSRF — HTMX 는 `X-CSRF-Token` 헤더, 일반 form 은 `csrf_token` 필드.
- 시안이 정본. 「시안과 똑같이」는 배치까지 문자 그대로. 시안에 없는 자리는 리포트에 기록하고 임의로 꾸미지 않는다.
- API · 도메인에 없는 값을 다른 필드로 추정해 화면에 채우지 않는다.

## 안전
- 사용자 포트 · 프로세스를 건드리지 않는다. SPEC 이 정한 포트만 쓴다.

## 스코프
- allowed_paths 밖 수정 금지. 커밋 · push · PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <WORK> <Phase> 결과 보고
## 상태: done / in-progress / blocked
## 수행 — 템플릿 · 조각 · 정적 파일 목록
## 검증 — 명령과 결과 (화면 pytest · 인라인 스크립트/손 CSS grep)
## 계약 대조 — SPEC · 시안 항목별 같음/다름
## 이슈 · 코디가 확인할 것
```
