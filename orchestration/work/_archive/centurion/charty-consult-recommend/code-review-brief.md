# reviewer 브리프 — 코드 검수 (read-only)

너는 이 작업의 맥락이 없다. **코드·문서를 고치지 않는다.** 리포트 1개만 쓴다.

## 1. 읽을 것 (절대경로)
- 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/orchestration/work/charty-consult-recommend/` 의 `SPEC.md` + `fe-brief.md` §2(검수 보정) + **`layout-fix-brief.md`(SPEC §0·§1 덮어씀 — 우선)** + `_RESUME.md` §2
- 워커 보고: 같은 폴더 `fe-report.md` · `screens/`
- 코드: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/reference/2026-10-21-charty-poc/web/` — 변경분은 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/shipworm diff HEAD -- reference/` + untracked

## 2. 볼 것
1. R-1~R-25 를 fe-report 표만 믿지 말고 코드·테스트로 대조. 테스트가 실제로 그 조건을 단언하는지(빈 단언·skip 남용)
2. layout-fix 정정이 지켜졌나 — 오른쪽 열 3패널·관련 파일·e2e 가 HEAD 와 같은 동작인지, 지운 것은 focus-card 전용만인지(grep 전수)
3. 3D 투영·가림·`__faceViewer` 덮어쓰기·메모리/리렌더(useFrame 안 setState 등) 문제
4. Hub 스냅샷: 출처·받은 날짜 표기, 한자·불필요 필드, 개인정보 없음. 커밋 대상에 얼굴 에셋(`public/m3d`)·스크린샷 0건
5. 「목업 · 의학적 근거 아님」 유지 · 태블릿 동작 회귀 없음(가격 토글 포함)
6. **사용자가 실물에서 만날 어색한 자리**(겹침·잘림·흐린 선 가독성·모달 크기·스크롤) — 코드로 짚어라

## 3. 검증 명령은 돌려도 된다
`npm run lint` · `npm run test` · e2e 는 3417 기존 서버 재사용으로만. **3417 서버를 끄거나 재시작하지 마라.** `npm run build` 는 돌리지 마라(dev 서버와 충돌 위험)

## 4. 쓸 것 — 같은 폴더 `code-review-report.md`
판정 **PASS / WARN / FAIL** + 항목별 근거(경로:줄 / 명령 결과). FAIL 은 고칠 내용을 구체적으로.

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[code reviewer 완료] orchestration/work/charty-consult-recommend/code-review-report.md" --enter
```
