
# [planner] SPEC-001 0.2.1 — reviewer WARN W-1 · W-2 반영 (작은 개정)

너는 consult-analysis `planner` 워커다(SPEC-001 을 쓴 그 워커). 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/상담데이터분석`.

## 입력
- 리뷰 리포트 `orchestration/work/consult-layer1/review-layer1-report.md` §WARN W-1 · W-2
- `para/projects/summer-star/consult-analysis/20-spec/spec-001-layer1-schema.md` 0.2.0

## 코디 결정 (이대로 반영)
1. **W-1** — 보관함 바로 아래에 폴더도 `*.json` 도 아닌 보통 파일(숨김 아님)이 있으면 **멈춘다**. G-12 의 조건에 이 꼴을 더한다(§1 · §4.1 · §5.4). 숨김 파일 무시는 그대로
2. **W-2** — 새 멈춤 **G-13 「원본 파일 읽기 실패」**(JSON 깨짐 · 비 ASCII 바이트 · 읽기 오류). 멈출 때 §5.4 끝줄대로 채널 · 보관함 · 몇 번째 방 · 규칙 번호를 찍는다. §5.1 의 ASCII 전제 문장에 G-13 연결
3. 변경 이력 0.2.1 행 · `20-spec/README.md` 버전 칸 0.2.1 · status 는 accepted 유지(계약 확장 아님 · 멈춤 강화)
4. WORK-001 WP3 행 아래에 「WP4 — reviewer WARN W-1 ~ W-3 반영(etl)」 한 줄 추가 · 상태 todo

## allowed_paths
- `para/projects/summer-star/consult-analysis/20-spec/`
- `para/projects/summer-star/consult-analysis/30-work/`

## 검증
- G-12 · G-13 이 §5.4 표에 있고 근거 절을 가리킨다 · 다른 절은 안 바뀜(`git diff` 로 범위 확인) · 고객 정보 0

## 완료 보고 — 문구 변경 금지
> preamble 의 코디네이터 핸들이 아래와 다르면 preamble 이 맞다.
- 커밋 · push · PR 금지. 끝나면 두 명령 모두:
```bash
orca orchestration send --to term_1e2044b5-cf36-479a-9750-9d7adba63b4c --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC 0.2.1" --body "변경 / 검증 / 미결"
orca terminal send --terminal term_1e2044b5-cf36-479a-9750-9d7adba63b4c --text "[worker_done] planner 완료 — SPEC 0.2.1(W-1 · W-2). 상세는 인박스." --enter
```
