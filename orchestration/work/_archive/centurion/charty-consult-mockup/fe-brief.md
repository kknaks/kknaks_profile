# frontend 브리프 — 피부 상담 목업 구현 (WP1~WP8)

너는 이 작업의 맥락이 없다. 아래를 먼저 읽어라.

## 1. 읽을 것
- **정본: `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/orchestration/work/charty-consult-mockup/SPEC.md`** — 전부. 여기 없는 것은 만들지 않는다
- 같은 폴더 `_RESUME.md` · `research-report.md` · `assets-report.md` (배경·근거)
- 차티 stg 참고는 `git -C /Users/kknaks/git/harness_works/CENTURION-CHARTY show origin/stg:<path>` 로만(체크아웃·fetch 금지)

## 2. SPEC §11 정할 것 — 코디 확정 (전부 기본값)
1 태블릿 좌우 분할 · 2 「피부 분석」 탭 맨 앞 추가 · 3 금액 직접 수정 없음 · 4 굵은주름 좌/우 id 기준 + 태블릿 ⓘ, 화면 ① 미표시 · 5 추천 규칙 표대로 + 파일 머리 「목업용 · 의학적 근거 아님」

## 3. 범위
- 쓰는 곳: `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/reference/2026-10-21-charty-poc/web/` 전부(신규) + 리포트·스크린샷용 `orchestration/work/charty-consult-mockup/` 아래 `fe-report.md`·`screens/`
- 읽기만: `reference/2026-10-21-charty-poc/m3d-assets/`·HAR. **수정·삭제 금지**
- `.gitignore` 는 코디가 이미 처리했다(`web/node_modules`·`web/.next`·`web/public/m3d`·`*.har`·`m3d-assets`·`screens/`). 더 필요하면 리포트에 적어라 — 직접 고치지 마라
- **git commit·push 금지.** 코디가 검증 후 커밋한다
- **포트**: dev/e2e 는 **3417** 만 쓴다(`next dev -p 3417`). 사용자 포트·프로세스(3000 등) 건드리지 마라. 끝나면 네가 띄운 서버는 내린다
- 얼굴 이미지·HAR 개인값(hash·생년월일·회원번호·S3 URL)이 커밋 대상 파일에 들어가면 안 된다(AC-4)

## 4. 진행
- SPEC §9 순서대로 WP1→WP8. **WP 마다 그 WP 완료 조건만** 확인하고, 전체 `npm run verify` 는 WP8 에서 한 번
- WP 하나 끝날 때마다 `fe-report.md` 에 한 줄 진행 기록(워커가 죽어도 이어지게)
- 막히면 우회로를 만들지 말고 `[질문]` 으로 물어라. 스펙과 다르게 해야 하면 이유를 리포트에 적는다

## 5. 산출
- `web/` 앱
- `fe-report.md`: WP별 결과 · **AC 1~25 확인 표**(AC 번호 · 결과 PASS/FAIL/미확인 · 근거 — 명령 출력·테스트명·스크린샷 경로) · 스펙과 다르게 한 것 · 남은 것
- `screens/` 스크린샷 4장 + 오버레이 확인 스크린샷

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_210dc6eb-3363-4f0c-9c78-b2b05f193d94 --text "[frontend 완료] orchestration/work/charty-consult-mockup/fe-report.md" --enter
```
질문은 같은 terminal send 로 `[질문] ...`. 코디 핸들이 안 닿으면 `orca terminal list --json` 에서 제목 「차티 피부과 상담 웹 목업」 터미널을 찾아라.
