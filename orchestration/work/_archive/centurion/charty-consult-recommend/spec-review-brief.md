# reviewer 브리프 — SPEC 검수 (read-only)

너는 이 작업의 맥락이 없다. **아무 파일도 고치지 않는다.** 리포트 1개만 쓴다.

## 1. 읽을 것 (절대경로)
- 정해진 것: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/orchestration/work/charty-consult-recommend/_RESUME.md` §2
- 검수 대상: 같은 폴더 `SPEC.md`
- 코드: `/Users/kknaks/orca/workspaces/kknaks_profile/shipworm/reference/2026-10-21-charty-poc/web/` · 측정 원본 `web/public/m3d/report/measure.json`
- Hub API(GET, 인증 없음): `https://stg-procedure-hub.medisolveai.com/api/taxonomy` · `/api/procedure-profiles`

## 2. 볼 것
1. `_RESUME §2` 결정과 어긋나는 곳(카드=부위명+시술명만 · 패키지/가격 X · 필터 강조/흐림 · 우측 패널 3개 큰 화면에서 제거 · 모달 · 스냅샷 · 사진 없음)
2. **SPEC 이 인용한 사실 실물 대조**: 코드 경로·줄, measure.json 점수(§2-2 · AC-1 · AC-8), Hub 노드 id(hub-refs 후보 · M8-4-1 등)와 필드 존재 여부 — 직접 grep·curl 해서 확인
3. §1-3 「빠지는 것」 전수조사 누락 — 빠지는 컴포넌트/testid 를 쓰는 곳을 grep 으로 전부 세서 SPEC 표와 대조
4. WP 순서·완료 조건이 frontend 워커 1명이 그대로 따를 수 있나. AC 가 검증 가능한 문장인가
5. 사용자가 실물에서 만날 이상한 자리(카드·선 겹침, 모달 크기, 1920×1080 안에 들어가나 등)

## 3. 쓸 것 — 같은 폴더 `spec-review-report.md`
판정 **PASS / WARN / FAIL** + 항목별 근거(경로:줄 / 명령 결과). FAIL 은 고칠 내용을 구체적으로.

## 4. 하지 마라
- 파일 수정 금지(리포트 제외) · 커밋 금지 · 포트 3417 dev 서버 건드리지 마라

## 9. 완료
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[spec reviewer 완료] orchestration/work/charty-consult-recommend/spec-review-report.md" --enter
```
