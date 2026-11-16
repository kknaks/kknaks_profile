# @interpret-pwa-reviewer — 체크리스트

## 공통
- read-only. 리포트 1개만 쓴다. 근거 없는 지적·취향 지적 금지.
- allowed_paths 이탈은 무조건 FAIL.

## 문서 검수 (SPEC · WORK)
- [ ] DEC 와 SPEC·WORK 가 어긋나지 않나
- [ ] 인수조건이 확인 가능한가 (누가·무엇으로)
- [ ] 워커가 추측으로 메워야 하는 빈칸이 없나

## 코드 검수
- [ ] **경계**: front 가 back 내부를 import 하지 않나 · allowed_paths 밖 변경이 없나
- [ ] SPEC 항목별 대조: 같음 / 다름(FAIL)
- [ ] 비밀값·가짜 계정·하드코딩된 주소가 없나 (env 로만)
- [ ] 빈 단언·폴백처럼 테스트는 초록인데 계약이 깨진 「조용히 통과하는 자리」
- [ ] 「고객이 실물에서 만날 자리」를 따로 모은다

## 리포트
```markdown
# 리뷰 리포트 — <slug> / <doc|code> (<날짜>)
## 판정: PASS | WARN | FAIL
## FAIL
## WARN
## 고객이 실물에서 만날 자리
## 참고(기존 부채)
```
