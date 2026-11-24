# [spec] SPEC-010 고침 1 — 검수 FAIL(P0 1 · P1 6 · P2 11) 반영 → 0.1.1 (11-20 · 자동 고침)

너는 SPEC-010 을 쓴 스펙 워커다. `W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 검수 `$W/review-spec-010.md` 를 읽고 **P0 · P1 전부 · P2 전부**를 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.1.1 로 올린다(변경 기록에 지적 번호별 한 줄). 문서 1 개만 고친다 · 코드 · 데이터 · 허브 수정 0 · 커밋 0 · 서브에이전트 0.

## 코디 결정(검수가 코디에게 넘긴 것)
- **P0-1:** 고민 → 진료항목은 `concern-candidates` 의 `reach` 에 「케이스 직접」 이 든 것만(행 단위 `rows[].reach == 케이스 직접`). 「제품 경유」 · `unreached` · `descended` 는 진료항목 경로에서 뺀다(LLM 재료로는 0.4 그대로 가능). 쪽 넘김은 `read_all`. WP-3 완료 조건에 실물 허브 표본(팔자주름 · 턱살 · 기미 — 진료항목 수 · 엉뚱한 부위 0) 추가. 근거 = `_RESUME` §2 11-20 「고민의 정본 = 케이스 · 제품 층 고민은 제품에 둠」.
- **P1-1: (가) 허브 WP(WP-H)를 WP-4 앞에 둔다** — 케이스 profile 에 `method_codes`(case_method 행 순서) · 방법 profile 행(silver method description 원문 · 그림 코드)을 더한다. 허브 · 앱은 함께 배포(D-6). §1-3 「허브 수정 범위 밖」 을 이 한 칸만큼 고친다. U-21 은 이 길로 고친다. 명동점 화면 기준 그림 빠짐 수(원리 0 · 방법 10)를 적는다.
- P1-2 ~ P1-6 · P2 는 검수 「고칠 방향」 대로. 기계가 정할 수 있는 것은 규칙으로 닫고, 정말 사용자 몫만 §11 에 남긴다(P1-4 조상 부위 「얼굴 전체」 포함은 추천 「넣는다」 로 §11 한 줄). 검수 §「결정 정리 제안」 대로 §11 을 **사용자(추천대로 한 번에 묻기)** / **코디 기본값(통보만)** / **사용자 문구(빈 slot)** 셋으로 나눠 적는다.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.1.1" --body "지적별 반영 / §11 셋 나눔 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 1 완료 — <한 줄>. 상세는 인박스." --enter
```
