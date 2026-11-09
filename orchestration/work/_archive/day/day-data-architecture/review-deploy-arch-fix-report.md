# 리뷰 리포트 — deployment.md W1 ~ W4 재확인 (2026-11-08)

대상: mediness `products/day/40-architecture/deployment.md`(미커밋) · `log.md` · 작성 리포트 `planner-deploy-arch-fix-report.md`. 앞 리포트 `review-deploy-arch-report.md` W1 ~ W4.
lint `--strict` → 0 error.

## 판정: PASS (가벼운 남은 것 3)

| W | 지금 | 판정 |
|---|---|---|
| W1 prod 같은 SHA | 흐름 표 「시작」 prod = **fast-forward 로만**(`git push origin <sha>:prod` 또는 승격 워크플로 · merge · squash 금지 — 「새 commit 이면 같은 이미지가 깨진다」) · sequence 「같은 commit · merge · squash 아님」 · 준비 목록 「브랜치 규칙 — prod fast-forward 만 · 누가 push · 강제 여부는 사용자」 | 닫힘 |
| W2 롤백 시작 | 롤백 = **수동 실행 워크플로(환경 · 이전 성공 SHA)** → 그 이미지로 재배포 · 새 줄 「migration 되돌리기 = 안 함(forward-only) · 이전 이미지가 새 스키마에서 돌게 migration 을 쓴다」 | 닫힘 |
| W3 prod 순서 | sequence · 표 모두 **① prod migration**(수동 · 승인 · 「dev 에 같은 revision 적용됨」 확인 · `upgrade head`) → **② prod 배포**(head 확인만 · 다르면 중지) · 미결 「승인 수단」은 세부(승인 문자열 등)만 | 닫힘 |
| W4 GitHub 준비 | 준비 목록에 4줄 — GitHub Environments(dev · prod) · 브랜치별 OIDC federated credential · Actions 변수(비밀값은 Key Vault 만) · 브랜치 규칙 | 닫힘 |

새 모순은 없다. 순서 ① → ② 와 fast-forward · 수동 롤백이 서로 맞는다. 사용자 결정(브랜치 push → 배포 · prod = dev 에서 확인한 같은 이미지)도 그대로다.

## 남은 것 (가벼움 · 막지 않음)

1. **① prod migration 이 쓰는 이미지.** 「같은 SHA 이미지로 migration 을 돌린다」는 말이 없다. prod 브랜치를 올리기 전에 실행하므로, 입력이 dev 에서 확인한 SHA 라는 것을 한 마디 적으면 구현자가 헷갈리지 않는다.
2. **수동 롤백 뒤 브랜치 머리 ≠ 돌고 있는 이미지.** 롤백하면 브랜치를 되돌리지 않고 VM 만 이전 이미지가 된다. 다음 `prod` push 가 다시 최신을 올린다는 사실을 롤백 줄에 반 줄 적으면 좋다(앞 리포트 W2 의 덧붙임).
3. **준비 목록에 두 줄이 없다.** 앞 W4 가 짚은 것 중 아래 둘이 빠졌다.
   - 「`v2-dev` → `dev` 이름 바꾸기 · `prod` 새로 만들기」. 결정 요약 L23 에만 있다.
   - 「배포 workflow · 배포 compose · Caddyfile 구현 발주」. L16 「아직 없다」에만 있다.
   이번 코디 지시가 W4 를 Environments · OIDC · 변수 · 규칙 4줄로 정했으니 지적은 아니다. 다만 사용자가 실제로 할 일과 다음 발주 한 줄로 남겨 두면 체크리스트로 쓰기 쉽다.
