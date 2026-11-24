# [spec] SPEC-010 고침 5 — r4 FAIL 반영 → 0.2.2 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 재검수 `$W/review-spec-010-r4.md` 의 P0-1 · P1-1 ~ P1-4 · P2-1 ~ P2-6 전부를 `$W/SPEC-010-consult-myeongdong.md` 에 반영해 0.2.2. 문서 1 개만 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0.

## 사용자 결정(11-20 — PoC)
- **P0-1:** 최저가 「다른 single」 후보에서 **0 원 혜택 옵션 · 회원권 상품(제목 「1년권」 · 「가입비」) 옵션은 뺀다.** **첫방문 옵션(「[첫방문]」 · 카테고리 「10월 첫방문 이벤트」)은 후보에 둔다**(PoC — 뜨게 함). 「[오픈]」 등 이벤트가도 둔다. 손님이 드롭다운에서 직접 고른 옵션은 무엇이든 그대로. 판별 = 원문 제목 · 카테고리 · 가격 0 규칙 표(`price.py` 상수) · 걸린 옵션 수를 WP-5 리포트에.
- **P1-1:** 같은 회차 다른 대상 옵션은 후보로 쓰지 않는다 — **상품 제목의 「남성」 · 「여성」 낱말이 고른 옵션과 같을 때만**(낱말 없는 것끼리는 비교 가능). C9 에 「남성 1 회 고름 → 여성 후보 0」 줄.

## 코디 기본값
- P1-2: group 은 **모든 구성 (진료항목, count)이 장바구니 옵션 줄에 있을 때만** 후보 · 그 줄들을 덮음 · 시험 (가) · (나) 줄.
- P1-3 · P1-4 · P2: 검수 「고칠 방향」 그대로(효과 길 = `facets?facet=outcome&node=effect:` read_all · O-8 줄임 · WP-H 안 넓힘).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.2" --body "r4 반영"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 5 완료 — <한 줄>. 상세는 인박스." --enter
```
