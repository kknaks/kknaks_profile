# [backend] 2루프 — e2e 1회차 피드백 (C28 · C29 · C30 · C31 · E3)

**읽을 것** (이 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/시술현황-차트/orchestration/work/day-chart-photo/`)
- `e2e-1-feedback.md`
- 결정 파일 C28 ~ C32
- SPEC 고침 `planner-fix-10-report.md` — mediness #960 최신 커밋 · 계약은 SPEC 이 SoT

## 할 것

**E3 — 저장마다 KOS sign-in 하지 않기**
- `services/board_charts.py` 의 `_kos_now` 가 `build_adapter` 를 쓴다 → `emr/factory.py` 의 `adapter_for`(병원별 캐시)로 바꾼다.
- API 프로세스 종료 때 닫히는지(`close_adapters`) 확인한다.
- 같은 이유로 새 클라이언트를 만드는 경로가 있으면 전부 찾아서 같이 바꾼다. grep 으로 전수 확인: `build_adapter(` 호출처.
- 사진의 직원 토큰 경로는 그대로 둔다.
- 테스트: 연속 저장 2회 → sign-in 1회.

**C28 — 여러 장 올리기**
- `POST …/photos` 가 `file` 여러 개를 받는다.
- 장마다 저장소 + 행을 만든다.
- KOS 는 presigned 를 장마다 받고, register 는 한 번에 묶는다(`사진등록다수.har` 모양 — 값 옮기지 않음).
- 실패한 장 = 「KOS 미반영」 · 나머지는 그대로 남는다.
- 장당 5MB · 장 수 한도 없음.
- 테스트 포함.

**C29 — 토스트 글자**
- `board_messages.py` 에서 `chart_staff_required` · `chart_conflict` · `staff_not_listed` · `doctor_not_listed` 를 UNSET 에서 빼고 결정 글자를 넣는다.
- 탭 저장 409 충돌 응답의 `message` 도 채운다.

**C30 — 사진 탭 다시 읽기 · 열려 있는 동안 동기화**
- 사진 탭 GET(그리고 `poll`)마다 가져오기 작업을 넣는다(잠금 · 중복 방지 그대로).
- 10초 확인 요청 입구를 SPEC 대로 둔다(화면 요청은 작업 넣기만).

**C31 — KOS 에서 지운 사진 정리**
- 가져오기 작업이 KOS 목록에 없는 ref 있는 DAY 행을 소프트 삭제한다.
- C25(KOS 재삭제)와 충돌하지 않게 한다 — DAY 가 먼저 지운 행은 제외.

## 하지 마라
- 템플릿 · JS(frontend 몫)
- 커밋

## 검증 · 보고
- 검증: `scripts/test.sh -q backend/tests/day/board` · ruff
- 보고: `be-loop2-report.md` + preamble worker_done 두 채널
