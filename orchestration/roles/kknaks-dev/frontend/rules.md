# @kknaks-fe — 규칙

- 기존 코드가 규약 — 새 컴포넌트 전에 인접 컴포넌트(`components/home/`·`components/shell/`) 패턴을 읽는다
- 시안 HTML(brief §1)이 시각 정본 — 마크업·토큰을 그대로 옮기되 React 관례로 변환
- spec 의 UX 문구를 임의로 바꾸지 않는다
- 폴링은 pending 동안만 — done/failed 에서 반드시 멈춘다 (cleanup 포함)
- allowed_paths 밖 수정 금지 (`app/back/`·`para/`·`orchestration/`)
- 검증: `npx tsc --noEmit` 만진 파일 0 에러. 전체 빌드 금지

## 리포트 형식

```markdown
# {WORK-ID} 결과 보고
## 상태: done / in-progress / blocked
## 수행 내용 — 파일 목록 · 라우트/컴포넌트 변경
## 검증 결과 — tsc 수치 · 수동 확인 항목
## 다른 팀 영향 — BE 계약 불일치 발견 사항
## 이슈/블로커
```
