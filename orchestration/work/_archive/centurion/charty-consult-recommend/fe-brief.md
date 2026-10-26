# frontend 브리프 — 큰 화면 부위별 추천 시술 카드 구현 (WP1~WP6)

너는 이 작업의 맥락이 없다. 아래를 먼저 읽어라.

## 1. 읽을 것
- **정본: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/orchestration/work/charty-consult-recommend/SPEC.md`** — 전부. 여기 없는 것은 만들지 않는다
- 같은 폴더 `spec-review-report.md` — 검수 권고 W-1~W-13. **아래 §2 가 SPEC 을 덮어쓴다**
- 같은 폴더 `_RESUME.md` (배경)

## 2. SPEC 보정 — 코디 확정 (SPEC 보다 우선)
- **§6 정할 것 1~7 은 전부 기본값**
- **(8) A2 「지금 보는 것」(focus-card) 제거 — SPEC 대로 뺀다**(범례 한 줄로 대체)
- W-1: `report-missing` testid 를 측정값 없음 표시 요소에 **유지**(`viewer.spec.ts:116` 이 계속 통과해야 함)
- W-3: 새 AC 는 **`R-1`~`R-25`** 로 부른다(SPEC §8 의 1~25). 기존 테스트의 AC 는 「구 AC-n」. 새 e2e 테스트 이름도 `R-n`
- W-4: 찍기 도구에 `__faceViewer.pickAt(cx, cy)`(캔버스 px raycast → `{p, n}`) 를 둔다. 정면 스크린샷 → 좌표 지정 → `pickAt` → 결과 스크린샷 확인 순으로 6점을 찍는다
- W-5: 편집 모드 판정은 순수 함수 `anchorEditEnabled(nodeEnv, search)` + 단위 테스트, `next build` 산출물(`.next/static`)에 편집 패널 문구가 없음을 grep 으로 확인
- W-6: 프레임 확인은 `__faceViewer.anchorMs()`(AnchorProjector useFrame 1회 평균 ms) 로 노출, 평균 2ms 미만 확인. 눈 확인은 코디가 한다
- W-7: 지시선 무릎은 **얼굴 쪽으로 32px**(왼쪽 카드 +32, 오른쪽 −32) · `data-visible` = 목표 opacity > 0 · `__faceViewer.anchors().opacity` = SVG 에 실제 적용한 최종값(가림은 별도 `occlusion` 필드)
- W-8: `fetch-hub.mjs` 에 `--refs <path>` 를 둔다. 실패 시험은 임시 refs 파일로
- W-9: `gradeSentence` 는 쓰는 곳이 없어지면 지운다. copy.ts 근거 문구는 리뷰 대로
- W-10: `__faceViewer` 는 `Object.assign` 으로 덧붙이고, Controls effect 도 기존 키를 보존하게 고친다
- W-11: 흐림 opacity 는 카드 **내용**에만, match 테두리(ring)는 100%
- W-12: 칩은 `flex-wrap`, 칩 안 줄바꿈 허용. WP2 스크린샷에서 6장 모두 잘림 없음을 완료 조건에 추가
- W-13: 지시선 교차가 나면 §1-2 칸 순서 안에서 **점 자리를 옮겨 다시 찍는다**(카드 칸 바꾸기 금지)

## 3. 범위
- 쓰는 곳: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/reference/2026-10-21-charty-poc/web/` + `orchestration/work/charty-consult-recommend/` 아래 `fe-report.md`·`screens/`
- 그 밖(`para/`·`_RESUME.md`·`SPEC.md`·`.gitignore` 등) 수정 금지. 필요하면 리포트에 적어라
- **git commit·push 금지.** 코디가 검증 후 커밋한다
- **포트 3417 에 코디가 띄운 dev 서버가 있다 — 끄거나 재시작하지 마라.** e2e 는 그 서버를 재사용한다(`reuseExistingServer`). 다른 사용자 포트·프로세스도 건드리지 마라
- `web/public/m3d/`(얼굴 에셋)는 읽기만. 얼굴 이미지가 커밋 대상 파일에 들어가면 안 된다. `screens/` 는 gitignore 처리됨

## 4. 진행
- SPEC §7 순서 WP1→WP6. **WP 마다 그 WP 완료 조건만** 확인, 전체 `npm run verify` 는 WP6 에서 한 번
- WP 하나 끝날 때마다 `fe-report.md` 에 한 줄 진행 기록
- 막히면 우회로를 만들지 말고 `[질문]` 으로 물어라. 스펙과 다르게 해야 하면 이유를 리포트에 적는다

## 5. 산출
- `web/` 변경
- `fe-report.md`: WP별 결과 · **R-1~R-25 확인 표**(번호 · PASS/FAIL/미확인 · 근거) · 스펙과 다르게 한 것 · 남은 것 · **사용자가 실물에서 만날 만한 어색한 자리**
- `screens/`: 자연광 · 모공 필터 · 30° 회전 · 모달 2장(V빔·프락셔널레이저) · 앵커 정면

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[frontend 완료] orchestration/work/charty-consult-recommend/fe-report.md" --enter
```
