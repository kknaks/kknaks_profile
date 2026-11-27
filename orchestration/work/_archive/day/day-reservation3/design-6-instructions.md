# [designer] 시안 v15 — 버전 배지는 제목 옆 · 액션 버튼은 메모 아래 (6차)

너는 day `designer` 워커다. 맥락이 없으면 먼저 읽어라:
- 브리프 `orchestration/work/day-reservation3/day-reservation3-design-brief.md` (규칙 §5 ~ §9 그대로)
- 5차 지시 `design-5-instructions.md` · 5차 리포트 `design-5-report.md`

## 할 것

`design/20261126_예약현황_시연_v14.html` → `design/20261126_예약현황_시연_v15.html` 로 복사해 고친다. **v14 는 고치지 않는다.** 머리 주석에 `v15(11-26): …` 한 줄. 바꾸는 곳 = 1열 예약 정보 덩어리뿐.

### 사용자 피드백

19. **버전 종류 배지(신규 · 수정 · 취소)를 「예약 정보」 제목 바로 옆으로.** 내원 일시 줄에서 배지를 빼서 그 줄도 라벨 + 값(다른 줄과 같은 모양).
20. **액션 버튼([예약 생성] · [예약 수정] · [예약 취소])을 예약 메모 입력칸 아래 오른쪽으로.** 제목 줄 오른쪽에서 뺀다. 답할 버전이 없으면(확정 · 취소됨 · 닫힘) 버튼 줄을 비워 두되 **높이는 유지**(초진 / 재진 · 상태와 상관없이 1열 높이 같음).

```text
──────────────────────────────────────────
예약 정보 [신규]
 내원 일시        10.29(목) 15:00 · 영미권
 희망 시술        쥬베룩
 원장/상담사      없음 / 최다은
 통역             영어 통역 필요
 예약 메모
 [textarea]
                                [예약 생성]
```

- 1열 높이 같음 · 스크롤 없음 유지 — 버튼 줄만큼 textarea 를 줄인다(최소 3줄).

## 스크린샷

`design/v15-first.png` · `design/v15-return.png` · 확정 상태(버튼 없음) `design/v15-done.png`.

## allowed_paths

- `orchestration/work/day-reservation3/design/20261126_예약현황_시연_v15.html` (새 파일) · `design/v15-*.png`
- `orchestration/work/day-reservation3/design-6-report.md`

## 리포트 (`design-6-report.md`)

① 피드백 19 · 20 반영 ② 세 장면 1열 높이 ③ 새 CSS · 삭제 ④ 질문. 검증: 새 색 0(v14 와 diff) · JS 오류 0 · v14 이전 · reference 무수정.

## 완료 보고

1차 브리프 §9 와 같은 두 명령. subject 는 `designer 완료: 시안 v15 — 배지 · 버튼 위치`.
