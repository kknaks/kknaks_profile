# 리뷰 리포트 — day-chart-photo / code 검수 4 (2루프 · e2e 1회차 피드백 E3 · C28 ~ C31) (2026-11-24)

- 대상: 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-chart-photo` 미커밋 변경(be-loop2 · fe-loop2 · fe-loop2-fix-1 반영 뒤)
- 근거: `e2e-1-feedback.md` · 결정 C25 ~ C32 · SPEC mediness #960 `7c5820d5`(규칙 39 ⑪ · 사진 API `tick`) · 레포 `AGENTS.md`
- read-only. 파일 수정 없음.

## 판정: FAIL (1건 — 서버 배포에서만 드러남) · WARN 7

코드 안의 계약은 결정대로 섰다: E3 캐시 어댑터 · C28 장마다 실패 · C29 글자 · C30 멈춤 · 겹침 · C31 목록 실패 = 판정 안 함 · C25 와 안 겹침. 관문 3개 모두 통과.
**F1**: dev · prod 앞단 Caddy 가 요청 본문을 **6MiB** 로 막는다. 그래서 여러 장 올리기(C28 「장 수 한도 없음」)가 서버 배포에서는 6MiB 를 넘으면 통째로 실패한다. 로컬 e2e 는 Caddy 를 거치지 않아 통과한다.

## 관문 명령(1회씩)

| 명령 | 결과 |
|---|---|
| `scripts/test.sh -q backend/tests/architecture backend/tests/day` | **2190 passed** (256s · exit 0) — fix-1 로 `test_day_js_는_innerHTML_로_글자를_넣지_않는다` 도 통과 |
| `cd backend && uv run ruff check day tests` | All checks passed |
| `cd scripts/frontend && npm run -s check` | 122 pass · 0 fail |

## FAIL

### F1 C28 여러 장 올리기 — 서버 앞단 본문 상한 6MiB 때문에 사진 2장(5MB 씩)부터 Caddy 가 413 으로 막는다
- 위치: `deploy/caddy/Caddyfile:4` · `:7-9`(`(day_proxy)` `request_body { max_size 6MiB }` — dev · prod 두 사이트 공통 · 주석 「업로드 경로가 생기면 경로별로 늘린다」). 이번 diff 에서 `deploy/` 는 바뀌지 않았다.
- 서버 쪽은 상한을 없앴다: `routers/board_photos.py:49-50` `MAX_FILES = 1000` · 장당 5MB 만 서비스가 본다(be-loop2 보고 「전체 본문 크기 한도를 없앴다」).
- 결과: 서버 배포에서 고른 장의 합이 6MiB 를 넘으면 요청이 API 에 닿지 않는다. 이때 Caddy 413 에는 `X-Day-Error` 가 없다 → htmx `responseError` → 413 토스트 템플릿이 없으면 화면에 아무것도 안 뜬다. 한 장도 저장되지 않는다.
- 근거: C28 「장 수 한도 없음 · 장당 5MB」 · e2e 1회차 사용자 「여러장 올린다니까」.
- 조용히 통과하는 자리: 로컬 `start.sh` 는 Caddy 를 거치지 않는다. 테스트도 ASGI 직접 호출이다. e2e 2회차를 로컬에서만 돌리면 보이지 않는다.
- 고칠 방향(결정 필요 — 배포 설정): `/board/visits/*/photos` 경로만 `request_body max_size` 를 크게 하는 블록(예: 100MiB 등 운영 상한)을 둔다. 아니면 화면이 여러 장을 장마다 따로 보낸다(C28 「KOS 등록은 묶어서」와 부딪힘). 「장 수 한도 없음」에도 운영 상한 하나는 필요하다(임시 디스크 — W3).

## WARN

### W1 (높음) C31 — KOS 목록 응답에서 **매핑에 실패한 항목은 조용히 빠진다**. 그래서 그 사진은 「KOS 에서 지워짐」으로 판정돼 DAY 에서 지워진다
- 위치: `backend/day/emr/kos/photos.py:68-81` `visit_photos` — `map_all(live, visit_photo)` 의 실패 목록(`_`)을 버린다 · `emr/kos/mapper_photo.py:19-23`(`id` · `fileName` 이 문자열이 아니면 `MappingError`) → `services/visit_photo_import.py:365-410` `_remove_gone` 이 `present` 에 없는 살아 있는 ref 행을 소프트 삭제.
- 지금 HAR 모양(`id` · `fileName` = 문자열)에서는 일어나지 않는다. 다만 KOS 가 어느 날 `id` 를 숫자로 주거나 `fileName` 이 빈 항목을 섞으면, 그 사진들이 탭을 여는 10초마다 DAY 에서 사라진다. 소프트 삭제 · 기록 `kosRemoved` 는 남는다.
- 같은 갈래 — **목록이 「정상 응답 · 빈 배열」일 때도** 그 방문의 반영된 사진이 전부 지워진다. 예: 그 직원 토큰에 사진 보기 권한이 없음, 방문 · 고객 외부 id 가 다른 KOS 일정에 다시 이어짐(예약 병합 · 재연결), KOS 쪽 일시 장애로 빈 목록. 브리프가 「가장 위험」으로 든 「목록 조회 실패」는 막혀 있다(`test_C31_DAY_가_먼저_지운_행은_C25_재삭제만_목록_실패면_판정_안_함`). 그러나 「성공했지만 비었거나 모자란 목록」은 아무것도 막지 않는다.
- 근거: C31 「KOS 에서 지운 사진은 DAY 에서도 지운다」 · AGENTS.md 외부 CRM 「외부 응답에 없는 값을 다른 칸으로 추정해 채우지 않는다」(없음 = 지움으로 추정).
- 제안: ⓐ `map_all` 실패가 하나라도 있으면 그 회차는 C31 판정을 하지 않는다(가져오기만). ⓑ 한 번에 지울 수 있는 비율 · 장 수에 상한을 둔다(예: 목록이 비었는데 반영된 행이 있으면 판정 안 함). 아니면 「두 회차 연속 없음」일 때만 지운다. 결정 필요.

### W2 (중간) C30 — 사진 탭을 연 채 파일 고르기 창을 10초 넘게 열어 두면, 고른 파일이 **말없이 올라가지 않는다**
- 위치: `backend/day/static/day.js:1617-1632` `photosTick` — 10초마다 `htmx.ajax(… target: box)` 가 그 자리를 innerHTML 로 바꾼다. `photosBusy`(`:1611-1616`)는 `.htmx-request` · 삭제 확인 창만 본다. **OS 파일 고르기 창이 열려 있는지는 모른다.** 바뀐 뒤 고른 파일은 떨어져 나간 옛 `<input type=file>` 의 `change` 로 가서 요청이 나가지 않는다(`board_photos.html` 의 `trigger='change'` form 이 새로 그려짐).
- 실물에서 여러 장을 고르다 보면 10초는 쉽게 넘는다(C28).
- 제안: 파일 칸이 포커스 · 클릭된 뒤 `change`/`cancel` 이 올 때까지 tick 을 건너뛴다(`input` 에 `click` → 표시 · `change` · `cancel` · `focus` 복귀 → 해제). 아니면 목록 영역만 바꾸고 올리기 form 은 바꾸지 않는다.

### W3 (중간) C28 — 형식 · 크기에 걸린 장, 저장소 실패로 멈춘 뒤의 장이 **말없이 빠진다**
- 위치: `services/visit_photos.py:373-375`(`rejected` 는 전부 걸렸을 때만 첫 오류로 쓴다 · 일부만 걸리면 버림) · `:383-389`(저장소 실패 = `break` — 남은 장 저장 안 함 · 토스트 없음) · 응답 토스트는 KOS 실패(C27)뿐.
- 예: 4장 중 1장이 HEIC · 1장이 6MB → 2장만 올라가고 200 · 아무 안내 없음. 직원은 4장이 다 올라갔다고 안다.
- 근거: C28 「한 장 실패해도 나머지는 남음 · 실패 장 = 「KOS 미반영」 + [다시 시도]」 — 검사에 걸린 장의 표시는 결정에 없다. 그래서 **사용자 확인 필요**(글자 · 예 「N장은 올리지 못했습니다(JPEG · PNG · 5MB 까지)」).
- 같은 곳: 본문 상한이 없어 한 요청이 임시 디스크에 무제한 쌓인다(Starlette 가 파일을 임시 파일로 흘림 · 장당 5MB 검사는 다 받은 뒤). 서버 배포에서는 F1 의 Caddy 상한이 막아 주지만, F1 을 풀 때 같이 운영 상한을 정해야 한다.

### W4 (중간) C30 부하 — 브라우저 탭이 숨겨져도(다른 창 · 화면 잠금) 10초 확인이 계속된다 · 한 번마다 판 전체 읽기 + KOS 호출
- 위치: `day.js:1607-1610` `photosShown` = 창 열림 · 패널 보임만 본다. `document.hidden` 은 보지 않는다(판 새로고침은 `document.hidden` 이면 미룬다 — `day.js` `refreshDeferred`).
- 셈(탭 하나 · 10초마다):
  - API: `GET …/photos?tick=1` 1회. `chartable` 이 `load_world`(그 병원 판 전체)를 읽는다(`services/visit_photos.py` `chartable`). 이어서 Redis 표시와 `kiq` 1회.
  - worker: 작업 1회 = KOS `get-visitor-images` **1회**(늘) + C25 재삭제 대상마다 `delete-visitor-images` 1회 + 새 사진이 있으면 서명 1회 + 장마다 GET. 같은 방문이 도는 중이면 넣지 않는다(`request_import` · 잠금).
  - 결과: 열린 탭 1개 = KOS 6회/분 이상 · 직원 10명이 탭을 열어 두면 60회/분. 직원이 모달을 닫지 않고 자리를 떠도 계속된다.
- 제안: `document.hidden` 이면 그 회차를 건너뛴다. 탭이 다시 보이면(`visibilitychange`) 바로 한 번 읽는다. 결정 C30 「탭을 닫거나 다른 탭이면 멈춤」의 취지와 맞다.

### W5 (낮음) C25 재삭제 — KOS 에 이미 없는 사진을 매 회차 다시 지우려 한다(10초마다)
- 위치: `services/visit_photo_import.py:413-450` `_redelete` — 지운 행 · 살아 있는 ref 마다 `delete-visitor-images` 를 부르고, 실패하면 `continue`(ref 남김). 그 사진이 KOS 목록(`listed`)에 이미 없으면(KOS 웹에서 따로 지움) KOS 가 404/4xx 를 주는 경우 ref 가 끝내 풀리지 않는다. 그러면 C30 10초 확인마다 실패 호출이 쌓인다.
- 제안: `listed` 에 없는 KOS id 는 부르지 않고 ref 만 소프트 삭제한다(이미 같은 회차에 목록을 읽었다).

### W6 (낮음) E3 — 캐시 어댑터의 교체 · 동시 첫 생성
- `emr/factory.py:93-103` `adapter_for` — ⓐ 연결 설정(fingerprint)이 바뀌면 옛 어댑터를 `aclose()` 한다. 이때 다른 요청이 그 어댑터로 `fetch_visit_tasks` 중이면 닫힌 httpx 클라이언트가 `RuntimeError` 를 낸다. `_kos_now`(`services/board_charts.py:109-114`)는 `EmrError` 만 잡으므로 그 차트 저장은 500 이 된다(드묾 — 설정 바꾼 순간). ⓑ 잠금이 없어 동시 첫 호출 둘이 각각 만들면 하나는 덮이고 닫히지 않는다(sign-in 1회 더 · 클라이언트 1개 샘). worker 에서만 쓰던 함수를 API 동시 요청에서 쓰게 되면서 생긴 틈이다.
- 토큰 만료 · 재로그인 = 동기화와 같은 `KosClient.internal_token`(만료 10분 전 갱신 · 401 이면 다시 · 「기기 5개 한도」면 가장 오래된 같은 표시 세션 해제 · `emr/kos/client.py:322-350` · `_token_lock`). **같은 방식이다 — PASS.**
- 프로세스 종료: `runtime/main.py:41` lifespan `close_adapters()` — **PASS.**
- 실물 확인: API(`--workers 1`) · worker 가 이제 각각 시스템 계정 세션을 하나씩 오래 쥔다. 로컬 · dev · prod 가 **같은 KOS 시스템 계정**을 쓰면 세션이 5개를 넘을 수 있다. 그러면 서로 가장 오래된 세션을 해제하며 번갈아 sign-in 한다. e2e 2회차 ⑤ 에서 api.log 를 보면 된다.

### W7 (낮음) C30 — 삭제 응답과 10초 확인 응답이 엇갈리면 지운 사진이 다음 10초까지 다시 보인다
- 위치: tick 은 `photosBusy` 가 거짓일 때만 나간다. 그러나 tick 이 나간 **뒤** 직원이 삭제를 누르면, 두 응답이 같은 자리를 바꾼다(삭제 버튼은 자리의 자식이라 `hx-sync="this:replace"` 대상이 아님). tick 응답이 늦게 오면 지운 사진이 잠깐 되살아난다. 다음 10초에 바로잡히므로 표시만의 문제다.

## 항목별 PASS

### E3 — `build_adapter` 호출처 전수
| 호출처 | 토큰 | 판정 |
|---|---|---|
| `emr/factory.py:101` (`adapter_for` 안 — 캐시가 만드는 자리) | — | PASS |
| `services/board_charts.py:109`(`_kos_now`) → `adapter_for` · 요청마다 닫지 않음 | 시스템 계정 | PASS(E3 원인 고침) · 테스트 `test_board_loop2.py:48` `test_E3_연속_저장_2회_KOS_클라이언트는_병원별_1개` |
| `services/ext_sync.py:88` · `:140` → `adapter_for` | 시스템 계정 | 그대로 |
| `services/visit_photo_kos.py:229` `(factory or build_adapter)` — 사진 · 직원 토큰 · 요청마다 닫음 | 직원(sign-in 없음) | PASS(그대로 두라는 지시) |
| `services/reservation_notice.py:216` — 공지 저장 · 직원 토큰 · 닫음 | 직원 | PASS(시스템 sign-in 없음) |
- 참고: 브리프의 `grep build_adapter(` 는 `(factory or build_adapter)(` 꼴을 못 잡는다. `grep build_adapter` 로 다시 확인했고 위 다섯 곳이 전부다.

### C28 — 장마다 실패 · 묶은 register
- 장마다 저장소 + 행 + `photo.upload` 커밋(`visit_photos.py:304-350`) · 바이트는 업로드 임시 파일에서 장마다 다시 읽음(메모리엔 한 장) · 행 잠금(`_kos_lock`) 장마다.
- KOS(`visit_photo_kos.py:266-345` `register_many`): 코드 1번 → 장마다 presigned + PUT(**실패하면 그 장만** 「KOS 미반영」) → 남은 장 `register-visitor-images` **1회** → 목록 1회에서 uuid 자리로 id.
- 묶은 register 가 일부만 실패할 때: KOS 가 일부만 등록하고 오류를 주면 남은 장 **전부** 「KOS 미반영」이 된다. 그다음 [다시 시도]와 C23 가져오기가 uuid 자리로 먼저 찾으므로 **두 번 등록되지 않는다.** 200 인데 일부만 등록되면 못 찾은 장만 「KOS 미반영」이다. **PASS.**
- 테스트 `test_C28_*` 4개(`test_board_loop2.py:104-162`).
- 메모리 · 크기: 장당 5MB · 메모리 한 장 — PASS. 전체 상한 → F1 · W3.

### C29 — 토스트 글자
| 코드 | 결정 글자 | 코드 위치 | 판정 |
|---|---|---|---|
| `chart_staff_required` | 담당자를 선택해 주세요 | `routers/board_messages.py:26` | 같음 |
| `chart_conflict` | 다른 곳에서 먼저 수정된 내용이 있습니다. 확인 후 다시 저장해 주세요 | `:25` · 탭 저장 409 `message`(`routers/board.py:512`) | 같음 |
| `staff_not_listed` | 선택할 수 없는 담당자입니다 | `:27` | 같음 |
| 차트 저장 `doctor_not_listed` | 선택할 수 없는 담당자입니다 | `:29` `chart_staff_not_listed` · `errors.py:140-148` `ChartStaffRejected.message_key` | 같음 · 호출 · 수락 글자(`:11`)는 그대로 |
- 화면 경로: 409 충돌 = `board_chart_tab.html` `message` → `ui.toast_oob`. 그 밖 = 오류 토스트 조각 + `X-Day-Error` → `day.js` 4xx 끼우기. 테스트 `test_C29_*`(`test_board_loop2.py:77` · `:91`) · `test_board_page_charts.py`(렌더). **PASS** — 실물 클릭은 e2e ①.

### C30 — 멈춤 · 겹침 · 잠금
- 다른 탭 = `runtime.cancel(box, "photos-tick")`(`day.js:1633-1639`) · 모달 닫힘 · 패널 숨김 · 자리 사라짐 = 다음 회차에서 끝(`photosShown`) — PASS(document.hidden 은 W4).
- 올리기 · 삭제 · 다시 시도 · 읽기 진행 중 · 삭제 확인 창 열림 = 그 회차 건너뜀(`photosBusy`) — PASS(파일 고르기 창은 W2).
- 화면 요청: `tick=1` = 작업만 넣고 기다리지 않음 · `poll=1` = 넣지 않음 · 없음 = 넣고 3초(`routers/board_photos.py` GET · SPEC `7c5820d5` 표 그대로) · 테스트 `test_C30_tick_은_작업만_넣고_기다리지_않음_poll_은_넣지_않음`.
- 같은 방문 작업 겹침 = 도는 중이면 넣지 않음 · 작업 잠금 `try_lock` — 앞 판 그대로 PASS.

### C31 — C25 와의 충돌 · 목록 실패
- DAY 가 먼저 지운 행 = `_remove_gone` 이 `VisitPhoto.deleted_at IS NULL` 만 본다 → C25 `_redelete`(지운 행 · 살아 있는 ref) 몫과 겹치지 않음 — PASS.
- ref 없는 「KOS 미반영」 행 = 안 건드림 · 목록을 읽은 **뒤** 생긴 ref = 안 지움(`ExternalRef.created_at <= listed_at`) — PASS. 다만 `listed_at` 은 앱 시계(`d.now()`)이고 `created_at` 은 DB 시계(`server_default now()`)다. 두 시계가 어긋나면 경계가 흐려진다. 같은 VM 이라 작다(참고).
- **목록 조회 실패**(네트워크 · 5xx · 모양 오류 · 토큰) = 예외로 `_remove_gone` 에 오지 않음 — **전부 지우지 않는다. PASS.** 「성공한 빈 · 모자란 목록」은 W1.
- 테스트 `test_C31_*` 3개(`test_board_loop2.py:195-260`).

## 조용히 통과하는 자리
1. **F1** — 테스트 · 로컬 e2e 모두 Caddy 를 거치지 않는다.
2. **W1** — FakeKos 목록은 늘 「모양이 맞는 전부」다. 매핑 실패 · 빈 성공 응답을 흉내 내는 테스트가 없다.
3. **W2** — 파일 고르기 창은 node · pytest 로 흉내 낼 수 없다. 실물 클릭으로만 보인다.
4. **E3** — 테스트는 「클라이언트 생성 수」를 센다. 실물 KOS 의 「기기 5개 한도」 세션 수(로컬 · dev · prod · worker · API 가 계정을 같이 쓰는지)는 못 본다.
5. **C28 묶은 register 의 실제 부분 성공** — KOS 가 일부만 등록하고 오류를 주는지, 전부 아니면 전무인지는 HAR 에 없다(가짜는 전부 실패만 흉내).
6. **C30** — 10초 타이머는 node 가짜 시계로만 확인했다. 백그라운드 탭에서 브라우저가 타이머를 늦추는 정도(W4)는 실물로만 보인다.

## e2e 2회차 체크리스트(이번 고침 중심 · 로컬 + **dev 서버 1회**)
1. (C29) 담당자 비우고 [저장] → 「담당자를 선택해 주세요」 · 목록 밖 담당자 → 「선택할 수 없는 담당자입니다」 · KOS 웹에서 같은 줄 고친 뒤 [저장] → 「다른 곳에서 먼저 수정된 내용이 있습니다. 확인 후 다시 저장해 주세요」 · 호출 · 수락의 원장 목록 밖 글자는 그대로
2. (E3) 차트 [저장]을 연속 3번 → `api.log` 에 KOS sign-in 이 한 번만(또는 0번 — 이미 토큰 있음) · 「기기 5개 한도」 해제 줄 없음
3. (C28) 「시술 전」에 JPEG 2 + PNG 1 한 번에 고르기 → 3장 · KOS 사진 탭에 3장(분류 · 메모) · KOS register 요청 1번(KOS 웹 HAR 과 같은 꼴)
4. (C28 · W3) HEIC 1장 + JPEG 1장 · 6MB 1장 + JPEG 1장 → 올라간 장 수와 안내(지금은 안내 없음 — 기록)
5. (**F1 · dev 서버**) 5MB 가까운 사진 2장 이상 한 번에 → 지금은 Caddy 413 · 화면 표시 없음 · 저장 0 — 고친 뒤 다시
6. (C30 · E4) 사진 탭을 연 채 KOS 웹에서 그 일정에 사진 1장 올리기 → 모달을 닫지 않고 10 ~ 20초 안에 보임 · 다른 차트 탭으로 옮기면 DevTools 에 `tick` 요청이 멈춤 · 모달 닫으면 멈춤
7. (W2) 사진 탭에서 [+] → 파일 고르기 창을 15초 열어 둔 뒤 고름 → 올라가는지(지금은 안 올라갈 수 있음)
8. (W4) 사진 탭을 연 채 브라우저를 다른 창 뒤로 1분 → `tick` 요청이 계속 나가는지 · KOS 호출 수(worker 로그)
9. (C31) KOS 웹에서 DAY 가 올린 사진 1장 · KOS 웹이 올린 사진 1장을 지움 → 10 ~ 20초 안에 DAY 에서도 빠짐 · `photo.import` 기록 `kosRemoved` 2
10. (C25 + C31) DAY 에서 지운 사진의 KOS 삭제를 실패하게 함 → 다음 회차에 KOS 에서 지워짐 · DAY 의 다른 사진은 그대로
11. (W1 · 확인만) 그 방문 KOS 사진이 있는 상태에서 사진 보기 권한이 없는 직원으로 사진 탭 열기 → DAY 사진이 지워지지 않는지

## 사용자 확인 필요(결정 문제 — 기록만)
- F1: 사진 올리기 경로의 본문 상한(운영 값) — 「장 수 한도 없음」과 함께 정할 것
- W1: C31 의 안전장치(매핑 실패 · 빈 목록이면 판정 안 함 · 연속 두 번 없음 등)
- W3: 검사에 걸린 장 · 저장 못 한 장의 안내 글자
- W4: 보이지 않는 탭(`document.hidden`)에서 10초 확인을 멈출지(C30 취지)

## 참고(무관 · 기존)
- E5 → C32 그대로 · E6 = 로컬 env(코드 무관).
- review-code-2 N1(의사 동기화 이력 집도의) · N2(README 테스트 파일 이름)는 이번 범위 밖이다. 열려 있는지 확인하지 않았다.
