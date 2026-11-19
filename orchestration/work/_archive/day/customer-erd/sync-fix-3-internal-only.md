# 공개 API 빼기 — 내부 API 만 (사용자 2026-11-19 「공개 api 비싸」)

`sync-fix-2.md` 를 진행하는 중에 아래가 **우선한다**. 커밋 · push · PR 은 금지다.

## 정한 것

1. 이번 작업의 새 동기화 코드에서 **공개 API(open) 호출은 0** 이다.
   - 기존 운영 코드(`get-zones` 등)는 범위 밖이라 그대로 둔다.
2. **메뉴의 진료항목 · 약품 · 기기**
   - 공개 `get-medical-services` · `get-machines` · `get-medicines` 를 빼고, 내부 `get-products` 응답에서 모은다.
   - 모으는 곳: 옵션 · 구성의 `medicalService`(+ `configuration.medicines[]` · `machines[]` · `procedure`). id 로 중복을 뺀다.
   - 어떤 옵션에도 쓰이지 않는 진료항목 · 약품 · 기기는 받지 못한다.
     - 그래서 「응답에서 사라짐 → 소프트 딜리트」를 이 세 테이블에는 **적용하지 않는다**. 옵션에서 빠졌다고 지우지 않는다.
     - 대신 `external_ref.is_present_in_source` 만 갱신할지는 backend 가 관례를 보고 정한다. 정한 것은 리포트에 적는다.
   - 시술(`treatment`)은 내부 `procedure-menu/v2/queries/get-procedures` 를 그대로 쓴다.
3. **5분 회차를 뺀다.**
   - 공개 통계로 「오늘 밖 고객의 변경」을 잡던 루프 · 스케줄 · Redis 표시 · 코드를 지운다.
   - 이 결정으로 `sync-fix-2.md` 의 WARN-3 · WARN-4 는 없던 것이 된다.
   - 오늘 밖 고객의 변경은 OQ 로 둔다. 결제 · 환불 · 카드 사용은 대부분 방문 중이라 오늘 10초 루프가 잡는다. 나중 후보는 내부 `visitor/v2/queries/get-visitors` 하루 한 번 훑기다.
4. `sync-fix-2.md` 의 나머지(FAIL-1 못 푼 티켓 · WARN-1 별도 태스크 · WARN-2 예외 범위 · 테스트)는 **그대로 한다.**

## backend

- 위 반영 + 테스트를 갱신한다.
  - 새 코드에 `"open"` 호출이 0 인지 grep 으로 확인하고, 결과를 리포트에 붙인다.
  - 메뉴 세 테이블이 「사라짐 소프트 딜리트 안 함」인지 테스트한다.
- DEMO 실물을 다시 확인한다(같은 방식). 진료항목 · 약품 · 기기 건수는 줄어든다(쓰이는 것만). 그 건수를 적는다.
- `be-2-report.md` 「검수 3 반영」 절에 함께 적는다.

## planner (SPEC-002 ㉔ · SPEC-000)

- ㉔ 원천 표: 진료항목 · 약품 · 기기 = 내부 `get-products` 안에서 모음 · 공개 API 0 · 「옵션에서 빠짐 ≠ 삭제」.
- 루프 표: 5분 회차를 지운다. 오늘 밖 고객의 변경은 OQ 로 두고, 후보는 내부 고객 목록 하루 훑기다.
- 공개 통계 관련 결정 · 문구(결정 2 · 9 · 「구매 항목 통계」 등)를 「2026-11-19 뒤집음 — 공개 API 비용」으로 정리한다. 이전 문구는 취소선으로 남긴다.
- SPEC-000 OQ-00-4(오늘 밖 변경 — 닫았던 것)를 다시 연다.
- lint 를 돌리고 `spec-sync-report.md` 에 한 줄 남긴다.

## 완료 알림

```bash
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[worker_done] <backend|planner> 내부 API 만 반영 완료 — <한 줄>" --enter
```

## 추가 — 기존 운영 코드도 내부 API 만 (사용자 2026-11-19 「지금 우리 코드에서도 공개 안 쓰고 내부로만」)

코디가 dev 전수 grep 으로 확인했다. 운영 루프의 공개 호출은 **구역 목록 하나**다.

- 위치: `emr/kos/__init__.py` `fetch_master` 의 `_list("open", PATH_ZONES)` · `fetch_schedules` 의 캐시가 빌 때 `_list("open", PATH_ZONES)`.
- 공개 토큰 `exchange-token` 은 이 호출 때문에만 생긴다.

**backend**:
1. `PATH_ZONES` 를 내부 `schedule/zone/v1/queries/get-zones` 로 바꾼다. 경로 출처는 조사 리포트 §0 이다(데모에서 공개 id 와 2/2 일치).
   - 응답 모양이 다르면 `mapper.zone` 을 맞춘다. 기존 칸 · 결과(구역 id · 방 조회)는 같아야 한다.
2. 그러면 운영 루프에서 공개 토큰을 발급하는 일이 없어야 한다. `open_token()` 이 운영 경로에서 불리지 않음을 테스트로 확인한다.
3. 바꾸지 않는 것:
   - `open_api_key` 는 연결 설정에서 **필수 그대로**다. 계약 변경은 후속이다. 읽기만 하고 쓰지 않는다.
   - `client.call("open", …)` 기능 자체는 남긴다. 데모 시드 도구(`emr/kos/demo/`)가 쓴다.
4. 확인할 것:
   - `backend/day/emr` 의 운영 경로(demo 제외)에서 `"open"` 호출이 0 인지 grep 결과를 리포트에 붙인다.
   - 기존 동기화 테스트가 통과한다.
   - DEMO 실물에서 구역 · 방 · 일정이 이전과 같다(판 해시가 같다).

**planner**:
- SPEC-002(또는 SPEC-000 01 · `system.md`)에서 구역을 공개 API 로 받는다고 쓴 곳을 내부 경로로 고친다.
- 「DAY 운영 동기화는 공개 API 를 쓰지 않는다(비용 · 2026-11-19)」를 원칙 한 줄로 넣는다. `open_api_key` 필수는 그대로 두고 OQ 로 남긴다.
