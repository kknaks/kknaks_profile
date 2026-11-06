# @day-reviewer — 체크리스트

## 공통
- read-only. 리포트 1개만 쓴다. 근거 없는 지적 · 취향 지적 금지.
- allowed_paths 이탈은 무조건 FAIL.

## 문서 검수 (SPEC · WORK)
- [ ] DEC · baseline 과 SPEC · WORK 가 어긋나지 않나. 원천에 없는 정책이 SPEC 에 있으면 FAIL
- [ ] 열린 것을 닫힌 것처럼 쓴 곳, 닫힌 것을 다시 연 곳
- [ ] 인수조건이 확인 가능한가 (누가 · 무엇으로)
- [ ] 워커가 추측으로 메워야 하는 빈칸이 없나
- [ ] `python3 scripts/lint-pipeline.py --strict` 1회 — products/day/ 범위 ERROR 0. 타 제품 결과는 '무관'으로 분리

## 코드 검수
- [ ] SPEC 항목별 대조: 같음 / 다름(FAIL)
- [ ] 아카이브(origin/stg)에서 통째로 복사해 온 곳이 없나 — 있으면 출처 표기 여부
- [ ] 레포 `AGENTS.md` 계층 규칙: router 가 DB 를 안 만짐 · repository 층 없음 · 모델 감추기(`day.public` 은 DTO 만) · 같은 파일 이름
- [ ] 외부 CRM: 업무 테이블에 업체 전용 칸(`kos_id` 등) 없음 · 업체 차이는 `emr/<업체>/mapper.py` 안 · 외부 쓰기는 outbox
- [ ] 웹 화면: 인라인 스크립트 · eval · CDN · 손 CSS 0, HX 조각/전체 페이지 분기, CSRF(centurion 가이드 기준)
- [ ] 비밀값 · 가짜 계정 · 하드코딩된 주소가 없나 (env 로만)
- [ ] API 에 없는 값을 다른 필드로 추정해 채운 곳
- [ ] 빈 단언 · 폴백처럼 테스트는 초록인데 계약이 깨진 「조용히 통과하는 자리」
- [ ] DB 가 필요 없는 규칙을 `infra`(실제 DB) 테스트로만 확인하고 있지 않은지 — 도메인 규칙은 DB 없는 단위 테스트(레포 `AGENTS.md` 「테스트」 · 2026-11-06)
- [ ] 「직원이 실물에서 만날 자리」를 따로 모은다

## 리포트
```markdown
# 리뷰 리포트 — <slug> / <doc|code> (<날짜>)
## 판정: PASS | WARN | FAIL
## FAIL
## WARN
## 직원이 실물에서 만날 자리
## 참고(기존 부채)
```
