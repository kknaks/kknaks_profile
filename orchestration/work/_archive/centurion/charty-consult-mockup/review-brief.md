# reviewer 브리프 — 피부 상담 목업 검수 (read-only)

너는 맥락이 없다. **판정만 한다. 코드를 고치지 않는다.**

## 1. 읽을 것
- 정본 `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/orchestration/work/charty-consult-mockup/SPEC.md` (특히 §9 WP · §10 AC 1~25 · §11)
- 같은 폴더 `_RESUME.md`(코디 결정) · `fe-brief.md` · `fe-report.md`(구현 워커 자기 보고 — **그대로 믿지 마라**)
- 코드 `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/reference/2026-10-21-charty-poc/web/`
- 스크린샷 `…/charty-consult-mockup/screens/` (Read 로 이미지 직접 본다)

## 2. 볼 것
1. **AC 1~25** — fe-report 의 PASS 근거가 실제 테스트·코드로 뒷받침되나. 테스트가 AC 문장을 정말 검증하나(느슨한 단언·skip·하드코딩된 기대값 없나)
2. fe-report 「스펙과 다르게 한 것」 10건 — 각각 타당/부당 판정
3. 스펙에 있는데 빠진 것 · 스펙에 없는데 들어간 것(범위 밖)
4. 개인정보 — 커밋될 파일(`git -C <레포> status --porcelain --untracked-files=all reference/2026-10-21-charty-poc/web`) 에 HAR 개인값·S3 URL·얼굴 이미지 없나
5. 동기화·가격 계산 로직의 경계 버그(seq·sessionId·할인 반올림·VAT)
6. 화면 문구 — 「진단·질환·치료·환자」, 한자, `-1`

## 3. 제약
- **서버·브라우저를 띄우지 마라**(e2e·dev·start 금지 — 코디가 3417 로 직접 돌린다). `npx vitest run` · `npm run lint` · `npx tsc --noEmit` 은 돌려도 된다
- 파일 생성은 리포트 1개만: `…/charty-consult-mockup/review-report.md`
- 판정: 항목별 PASS / WARN / FAIL + 근거(`파일:줄`). FAIL 은 고칠 방향 한 줄. 마지막에 총평 PASS/FAIL

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_210dc6eb-3363-4f0c-9c78-b2b05f193d94 --text "[reviewer 완료] orchestration/work/charty-consult-mockup/review-report.md" --enter
```
