# planner 브리프 — 큰 화면 부위별 추천 시술 카드 스펙

너는 이 작업의 맥락이 없다. 아래 「읽을 것」을 먼저 읽어라. **코드를 쓰지 않는다. 스펙만 쓴다.**

## 1. 읽을 것 (절대경로, read-only)
- `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/orchestration/work/charty-consult-recommend/_RESUME.md` — 정해진 것 (§2 는 다시 논의하지 마라)
- 직전 스펙: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/orchestration/work/_archive/centurion/charty-consult-mockup/SPEC.md`
- 목업 코드: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/reference/2026-10-21-charty-poc/web/` — **쓰는 곳을 전부 grep 으로 세라**. 시작점: `src/components/screen/screen-view.tsx`, `src/components/viewer/face-canvas.tsx`(3D→화면 투영 `:147`), `src/domain/filters.ts`, `src/data/recommend-rules.ts`, `src/data/mock/taxonomy-subset.json`, `src/domain/skin-report.ts`, `src/sync/*`, `e2e/`, 테스트
- 측정 원본: `.../web/public/m3d/report/measure.json`(gitignore, 로컬에 있음)
- Procedure Hub API(인증 없음, GET): `https://stg-procedure-hub.medisolveai.com/api/taxonomy` · `/api/procedure-profiles` · `/api/problem-packages` · `/api/contraindications` · `/api/products`. 구조는 직접 받아 확인

## 2. 쓸 것 — `orchestration/work/charty-consult-recommend/SPEC.md` 1개
1. 화면 ① 1920×1080 새 배치 — 얼굴 가운데 · 좌3/우3 부위 카드 · 지시선 · 점. ASCII 와이어. 빠지는 패널과 그 컴포넌트·테스트 처리
2. 부위 카드 6개 정의 — `_RESUME §2-1` 초안을 확정(측정값 → 부위 → Hub 고민 항목 → 시술명). 강조/흐림 규칙(필터·등급·측정값 없음)
3. 3D 앵커 — 부위별 메시 표면 좌표 정하는 방법(개발용 찍기 도구 or 계산), 매 프레임 투영·가림 판정·카드 쪽 끝점, 회전·리셋 시 동작
4. 모달 — 시술명 클릭 → 표시 항목(원리·주의사항·금기·효과 시작/지속·사후관리 등)과 Hub 필드 연결. 시술명 단위와 Hub modality 단위가 어긋나는 문제의 처리안
5. Hub 스냅샷 — 받을 범위, 파일 위치·형식, 받는 스크립트(또는 수동 절차), 출처·받은 날짜 표기
6. 기존 `recommend-rules.ts`·태블릿 추천 패널과의 관계(대체/공존) — 태블릿 화면은 이번에 안 바꾼다
7. **WP 분할**(frontend 워커 1명 순서대로) + WP 별 완료 조건
8. **수용 기준(AC)** 번호 매겨서, 검증 가능한 문장으로. 「필터 모공 선택 시 모공/피부결 카드만 진함」「얼굴 회전 시 점이 피부에 붙어 이동」「보톡스 클릭 시 모달에 원리·주의사항」 등
9. 정할 것 — 네가 못 정한 것만, 기본값 제안과 함께

## 3. 하지 마라
- 코드·`web/` 수정 금지. 커밋·push 금지. `_RESUME.md` 수정 금지
- 사용자 dev 서버(포트 3417) 끄거나 재시작 금지

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[planner 완료] orchestration/work/charty-consult-recommend/SPEC.md" --enter
```
