# 계약 v2 — 원내 현황 탭 (backend ↔ frontend)

결정 정본: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` **R46 ~ R53**. 시안: `.../reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` — `renderSide`(L1804) · `stageCard`(L1777) · `STAGE_CATS` · CSS `.ibc` · `.ib-st` · `.ib-pay` · `.ib-kv`(L440 ~ 475). 생김새 · 문구는 시안 정본, 동작은 결정.

## 보기 모델 (기존 V 에 추가 · 최상위 컨텍스트 이름 `inhouse`)

```
inhouse {
  chips: [ {key: "all"|"reception"|"consult"|"procedure"|"going_wait", label: 시안 문구, count: int} ]  # 순서 = 시안 STAGE_CATS
  items: [ {
    visit_id: str,
    name: str,
    cat: "reception"|"consult"|"procedure"|"going_wait",
    stage: {key: 표 카드 state 와 같은 키, label: 시안 단계 문구},
    payment_due: bool,          # R42 그대로(표의 「수납 필요」와 같은 값)
    payment_done: bool,         # R48
    reserved_label: str|null,   # 접수만 — 시안 whenOf 형식
    nationality: str|null,      # 접수만 — 표와 같은 값(R33)
    counselor_name: str|null,   # 상담 대기부터 · 없으면 null(줄 안 그림)
    amounts: {total:int, received:int, unpaid:int}|null,  # 시술 대기 · 시술 진행 · 귀가 대기만 — R49 ~ R51
    order_all: int,             # 「전체」 칩 정렬 순번(수납 필요 먼저 → 단계 → 시각)
    order_cat: int              # 다른 칩 정렬 순번(단계 → 시각)
  } ]
}
```
- 대상 = **오늘**(보는 날짜와 무관 · R47). 날짜를 바꿔도 `inhouse` 는 오늘 것.
- 판정(대상 · cat · 배지 · 금액 · 순번)은 전부 서버. 화면은 칩으로 거르고 순번으로 줄 세우기만.
- 폴링(`poll=1`) 응답에도 같은 `inhouse` 가 들어간다. 고른 탭 · 칩은 폴링 · 날짜 이동 뒤에도 유지(화면 상태).
- 금액 표시는 시안 `n0w`(「1,234 원」). 「수납 필요」 금액은 unpaid > 0 이면 빨강.
- 빈 목록 = 「해당하는 고객이 없어요」. 카드 누르기 = 동작 없음.
