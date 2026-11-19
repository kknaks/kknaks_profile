# @centurion-reviewer — 체크리스트

## 공통
- read-only. 리포트 1개만 쓴다. 근거 없는 지적 · 취향 지적 금지.
- allowed_paths 이탈은 무조건 FAIL.

## 문서 검수
- [ ] 계약 문서와 브리프가 어긋나지 않나
- [ ] 인수조건이 확인 가능한가 (누가 · 무엇으로)
- [ ] 워커가 추측으로 메워야 하는 빈칸이 없나

## 코드 검수
- [ ] **모듈 경계**: 밖에서 `crm.public` 외 import · `crm` 이 `linky`/`sso`/`admin` import · ORM 모델 노출 · 스키마 간 FK
- [ ] 계약 항목별 대조: 같음 / 다름(FAIL)
- [ ] AGENTS.md 백엔드 안전: 불변식 최종 방어선 · `AsyncSession` 공유 · event loop 블로킹 · transaction 안 외부 I/O · N+1
- [ ] 비밀값 · 가짜 계정 · 하드코딩 주소 · 실제 env 커밋이 없나
- [ ] migration: 서비스 chain(`migrations/crm`)에만, downgrade/rollback 전략
- [ ] 빈 단언 · 폴백처럼 테스트는 초록인데 계약이 깨진 「조용히 통과하는 자리」
- [ ] 다른 서비스(SSO · Linky · admin) 계약에 설명되지 않은 회귀

## 리포트
```markdown
# 리뷰 리포트 — <slug> / <doc|code> (<날짜>)
## 판정: PASS | WARN | FAIL
## FAIL
## WARN
## 운영에서 만날 자리
## 참고(기존 부채)
```
