# @interpret-pwa-designer — 규칙

- 새 디자인 언어를 만들지 않는다 — medikit + `data-product="ceramique"` · `ceramique-theme.css`(primary `#2498bd`) · ccc 「Ceramique 의사 모바일」 스타일을 그대로 쓴다.
- 화면 · 상태 목록은 SPEC-001 §7 이 정본. 없는 화면을 발명하지 않는다. 시안에서 새로 제안할 것은 리포트에 「제안」으로 따로 적는다.
- 샘플 값은 가짜(실명 · 키 · 계정값 0).
- 코드(`front/` · `back/`)는 수정하지 않는다. 커밋 · push · PR 금지.

## 리포트 형식 (브리프가 지정한 경로)
```markdown
# <slug> 시안 결과 보고
## 상태: done / in-progress / blocked
## Claude Design 프로젝트 — id · 이름 · 화면(파일) 목록
## 화면 대조 — SPEC-001 §7 항목별 있음/없음
## 제안 · 코디가 확인할 것
```
