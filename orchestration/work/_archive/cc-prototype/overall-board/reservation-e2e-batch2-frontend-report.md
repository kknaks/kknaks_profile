# 예약 현황 E2E batch 2 — frontend 결과 보고

## 상태: done (#3 보류 — 지시대로 안 함)

기준 = `reservation-e2e-batch2-instructions.md` frontend 칸 · `reservation-e2e-feedback.md` 「# batch 2」. 코드 `1d482d8` 위 · 커밋 안 함.

## 수행 — 파일

- `procedure/front/lib/hooks.ts` — `useResvBoard` 에 `prev`(새 날짜 응답 전 앞 날짜 표)
- `procedure/front/app/(main)/reservations/live/page.tsx` — 앞 표를 흐리게 · 제목 줄 날짜는 바로 새 날짜
- `procedure/front/components/reservations/DetailModal.tsx` — #2 · #4 · #6 · #7 · #8 · #9 + Esc 고침

## 처리 여부

| # | 처리 | 내용 |
|---|---|---|
| 1 | 완료 | **원인 측정**(임시 3790/8790 가짜 모드 · headless): [›] 클릭 → `GET board?date=` 나감 **39ms** → 응답 56ms → 표 그림 146ms. front 는 날짜가 바뀌면 바로 부른다(폴링 · 디바운스 기다림 없음 — `useResvBoard` 효과가 date 바뀔 때 즉시 `load`). 늦어 보인 이유 = **새 날짜 응답이 올 때까지 표를 통째로 지우고 「불러오는 중…」만 보였던 것** + 실 back 에서 캐시 없는 날짜는 KOS 하루 조회(`ensure → fetch_day`)를 기다림. 고침: 날짜를 바꾸면 제목 줄 날짜는 바로 바뀌고 앞 날짜 표 · 패널은 흐리게(불투명도 0.45 · 누름 막음) 두었다가 응답이 오면 바꿔 끼움(`e2e-b2-1-date-stale.png` = 응답 2초 늦춘 상태). 실 back 에서도 여전히 느리면 `fetch_day`(KOS 호출) 시간이 원인 — backend 측정 필요 |
| 2 | 완료(front) | 상세 GET 이 404(코드 상관없이)면 폴링 · 표 상태 변화 다시 읽기를 멈추고 「KOS 에서 사라진 예약이에요」 + [닫기]. 404 강제 시험: 12초 동안 요청 2번(열 때 · dev 이중 마운트) → 5초 폴링 없음 확인 |
| 4 | 완료 | 상담사 고르기 = medikit Popover(portal · 모달 위 레이어 · `avoidCollisions` 로 아래 자리 모자라면 위로). 고르면 닫히고 카드에 [{이름} 실장 호출] 버튼(켜짐 = `can.callCounselor`) → 호출. 트리거 글자 = 고른 이름. 덤: 팝오버가 열린 채 Esc 를 누르면 모달까지 닫히던 것 → 팝오버만 닫게(`e2e-b2-4-counselor.png`) |
| 6 | 완료(시안 대조) | 시안 `M:1826-1832` · `M:546-560` 대조 — 아래 표 |
| 7 | 완료 | 이전 방문 = 기본 전부 펼침 · 접은 것만 기억(▾/▸ 눌러 접기) |
| 8 | 완료 | 이전 방문 Badge(결과가 `other` 일 때 원문이던 것): RESERVED 예약 · IN_PROGRESS 진행 중 · COMPLETED 방문 완료 · NO_SHOW 노쇼 · CANCELED 취소. 시술 내역 줄 상태: NOT_STARTED 시작 전 · WAITING 대기 · READY 진행 · DONE 완료 · CANCELED 취소. 모르는 값은 원문. 판정(`result`)은 back 그대로 |
| 9 | 완료 | 내원 현황 단계 카드 = 한 줄 `[점][제목][상세] …… [HH:MM][버튼]`. 접수 완료 = 「A-룸1 배정 · 데스크 X」 + 접수 시각 · 상담 = 상담사 · 호출 정보 + 시각(진행 중 = 시작 시각 · 그 밖 = 호출 시각) + [상담사 선택] · 시술 · 귀가 = 같은 꼴(응답에 상세 · 시각 값이 없어 제목만 · 귀가 정산 상자는 그 아래)(`e2e-b2-9-flow.png`) |
| 3 | 보류 | 지시대로 하지 않음 |
| 5 | — | backend 몫 |

### #6 시안 대조

| 항목 | 시안 | 지금 |
|---|---|---|
| 정렬 | `sort((a,b) => a.busy - b.busy)`(빈 방 먼저) + 목록 `flex-direction: column-reverse` → **화면에서는 사용 중 위 · 빈 방 아래** | 같음(같은 정렬 + column-reverse) |
| 열 수 | 한 열 | 한 열 |
| 사용 중 | `bg-ms-gray-100 border-ms-gray-100` · 상태 「사용 중」 `text-typo-body-400 text-ms-gray-500` · 누를 수 없음 | 같음 |
| 빈 방 · 선택됨 | `bg-ms-white border-ms-white` / `bg-primary-100 border-primary` · 「비어있음」/「선택됨」 `text-typo-body-500 text-primary` | 같음 |
| 줄 | `[이름 64 · body-600][사용자 · body-400 gray-600 flex 1][상태]` · 높이 ≥ 44 · 반경 8 | 같음. 사용자 칸은 응답에 값이 없어 비움(backend 에 「방을 쓰는 고객 이름」 있으면 채울 수 있음) · 이름이 64 를 넘으면 줄바꿈 대신 늘어나게(「A-레이저실」) |
| 머리 | 「시술실 배정」 heading-md-500 + 「{구역} · 빈 방 N개」 body-400 gray-500 | 같음 |
| 틀 | 오른쪽 20 · 아래 60 · 폭 min(420, 100% − 40) · 반경 10 · 그림자 · 목록 최대 320 스크롤 | 같음 |

## 검증

- `npx tsc --noEmit` 0 · `npm run lint` 0 · `npm run build` 성공
- 화면: 임시 front 3790 · back 8790(가짜 모드 · KOS 주소 `127.0.0.1:9` 로 막음) headless — 스크린샷 `fe-shots-reservation/e2e-b2-1-date-stale.png` · `e2e-b2-4-counselor.png` · `e2e-b2-6-rooms.png` · `e2e-b2-9-flow.png`, 콘솔 오류 0. 끝나고 두 프로세스 종료(포트 비어 있음). 사용자 포트 안 건드림
- 가짜 데이터에는 빈 방이 없어(빈 방 0개) #6 의 「빈 방 아래」는 화면으로 못 보임 — 코드는 시안 식 그대로

## 코디가 확인할 것

1. #1 이 실 back 에서도 느리면 backend 의 캐시 없는 날짜 KOS 조회(`reservation_sync.fetch_day`) 시간을 재야 한다 — front 는 즉시 요청
2. #6 사용 중 방의 고객 이름(시안 `who`)은 응답에 없다 — 넣을지
