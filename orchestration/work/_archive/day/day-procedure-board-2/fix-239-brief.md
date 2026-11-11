# [backend + frontend] #239 리뷰 반영 — 점유 이동 순서 · 조용한 거절

같은 워크트리 · 같은 규칙(`code-239-brief.md` — 커밋 · push · KOS 호출 · 앱 · 사용자 포트 금지). 리뷰: 같은 폴더 `review-239-report.md`.

## 고칠 것 (사용자 결정 2026-11-11)
- **W1 점유 이동 순서**: 「방 배정」이 없는 고객의 점유 이동은 **「방 배정」을 먼저 만들어 원래 방에 두고(확인 뒤) → 그 「방 배정」만 빼고 나머지를 새 방으로** 옮긴다(지금은 나머지 먼저 → 방 배정 나중이라 카드가 원래 방으로 돌아감). **그리고 카드 방 계산(mapper `card_room` 등)에서 「방 배정」 작업은 뺀다**(KOS 웹에서 방 배정을 다시 배정해도 카드가 안 흔들리게). 방 배정이 이미 있는 고객 · 이동 · 복귀 경로도 이 규칙으로 맞는지 확인
- **W2 설정이 비었을 때**: 「점유 이동」 버튼을 **꺼서**(스냅샷 `canHoldMove` 등) 누를 수 없게 — 새 글자 · 새 오류 코드(`room_assign_unset`)는 만들지 않는다(서버는 기존 거절 코드로 막기만)
- **W3 「방 배정」 이름을 못 구하면**: 조용히 「이동」으로 바꾸지 말고 **거절**(기존 409 관례 · 새 글자 없이 공용 토스트)
- W4(완료 시술 집도의)는 해소(사용자 확인 — KOS 상태 안 바뀜) · 고칠 것 없음
- 스펙 문구가 바뀌어야 하면 고치지 말고 보고(코디가 스펙에 반영)

## 검증
관련 테스트 + `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q` 1회 · ruff · build-css(화면 바뀌면). 로컬 DB 에 room_assign_etc_task_id 는 코디가 이미 넣음.

## 완료 보고
코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd` — worker_done(새 task 면 그 id · 아니면 `orca orchestration send --type status`) + terminal send · subject "#239 리뷰 반영".
