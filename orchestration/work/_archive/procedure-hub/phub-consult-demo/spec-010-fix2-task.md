# [spec] SPEC-010 고침 2 — r2 FAIL(새 P1 3 · P2 6) → 0.1.2 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 재검수 `$W/review-spec-010-r2.md` 의 **N1 ~ N3 · P2-N1 ~ N6 전부**를 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.1.2(변경 기록 한 줄씩). 문서 1 개만 · 코드 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0.

## 코디 결정
- **N1: (ㄴ)** — 허브 케이스 profile 행에 `method_codes`(`·` 로 이은 문자열 · 순서 = case_method 행 순서) · `method_texts`(같은 순서 · silver method description 원문) 두 칸을 더한다. `g_profile` 에 method 자기 행은 **더하지 않는다**(`node=method:` 기존 속성 조회 응답 그대로). 손대는 파일 · 회귀 조건은 검수 「고칠 방향」 3 · 4 그대로(작업 사본 gold-build · gold-check + 허브 headers · facets · medallion(DB 판) · g_profile 밖 gold 바이트 같음 · `node=method:` 기존 응답 같음 · 0.4 관련 시험 통과). 방법 그림 코드는 `method_codes` 로.
- N2 · N3 · P2 는 검수 「고칠 방향」 대로.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.1.2" --body "N1~N3 · P2 반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 2 완료 — <한 줄>. 상세는 인박스." --enter
```
