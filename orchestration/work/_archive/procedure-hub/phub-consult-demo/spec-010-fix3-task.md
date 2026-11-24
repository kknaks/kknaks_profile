# [spec] SPEC-010 고침 3 — 사용자 결정 반영 → 0.2.0 (11-20)

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · `$W/SPEC-010-consult-myeongdong.md` 0.1.2(PASS) 를 아래 사용자 결정으로 고쳐 0.2.0. 문서 1 개만 · 코드 · 데이터 수정 0 · 커밋 0 · 서브에이전트 0. 검수 r3 의 P2 2(옛 「방법 profile」 글 · WP-H alembic)도 같이.

## 사용자 결정(11-20 — 다시 묻지 마라)
1. **상담 = 조건 누적으로 좁히기.** 손님이 막연한 바람에서 시작해 대화로 조건(시술 · 부위 · 고민 · 효과 · 제품(브랜드 · 국산/수입 — 허브 제품 국가 칸))을 하나씩 정하며 받을 진료항목까지 좁힌다. U-13 「이번 턴으로 바꿈」 폐기 → **조건 칸 누적 · 바꾸면 그 칸만 교체 · 목록 = 모든 조건을 만족하는 진료항목 · 0 이면 앞 목록 유지 + 어느 조건 때문인지 봇이 말함**. 0.4 `carry.py`(조건 이어받기) 위에 얹는다.
2. **봇의 다음 질문 고르기:** 지금 목록을 가장 잘 가르는 축(부위 / 고민 / 효과 / 제품)을 고른다(규칙 · 시험 가능한 꼴로).
3. **장바구니:** 담는 단위 = **진료항목**(상품 · 옵션은 담을 때 고르지 않음). 목록과 별개로 쌓이고 서버가 대화마다 든다. 봇은 장바구니를 보고 「같이 받기」(허브 pair) 질문에 답한다.
4. **최저가 = 장바구니 진료항목 전부를 덮는 KOS 상품 옵션 조합 중 합계 최소**(single 옵션 + group(묶음) 옵션 · 집합 덮기). **가격 기준 = 이벤트가(`additional_prices[].visitor_type == 「이벤트가」`)가 있으면 이벤트가, 없으면 정가**(U-2 폐기 · 정가도 같이 보임). group 의 이벤트가는 **옵션 단위** 값이다(구성 줄의 additional_prices 는 옵션 합계가 반복돼 있음 — 실측 「[11월 이벤트] 온다50kj+티타늄30kj」 정가 1,100,000 / 이벤트가 590,000 · 구성 두 줄 모두 590000 → 구성 이벤트가는 쓰지 않음). 장바구니 밖 진료항목을 품은 group 은 **후보에서 뺀다**(U-4 추천 (가)). 카드 2 장 = 최저 · 두 번째 최저 조합(상품명 + 옵션명 + 가격).
5. 「+ 다른 시술 포함 묶음이 같은 값이면 추가 추천」(예 써마지 + 쥬베룩 = 써마지 + 쥬베룩 + 울쎄라 값)은 **다음 단계** — 범위 밖에 한 줄.
6. 나머지 §11-1 결정은 **추천대로**(U-3 은 4 의 집합 덮기에 맞게 다시 씀 · U-9 · U-12 · U-26 등 추천 그대로).
7. **그림 서빙은 앱이 한다** — 허브 서버(18105)는 그림을 읽지도 내보내지도 않는다(`$W/image-register-report.md` §4). 그림 시드 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/images/`(원리 54+1 · 방법 49+17 — 명동점 빠짐 0) 를 env 경로로 읽어 앱이 서빙(경로 · 캐시 · 없을 때 처리 계약).
8. **매핑 JSON 에 상품 표가 들어간다**(다른 데이터 워커가 v3 를 만드는 중 · `$W/mapping-json-v3-task.md` 의 꼴) — 스펙은 그 꼴(products[] · product_categories[] · items[].option_refs)을 쓴다.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "spec 완료: SPEC-010 0.2.0" --body "결정 1~8 반영 / WP 변화"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] spec 고침 3 완료 — <한 줄>. 상세는 인박스." --enter
```
