# [조사 · 읽기 전용] 공지 「수정하기」 + KOS 동기화 — cc-prototype 동작 · KOS 명령 · DAY 쓰기 경로

너는 맥락이 없다고 생각하고 이 파일만 따른다. **고치지 · 커밋하지 마라.** 결과는 리포트 하나.
배경: DAY 예약 현황 오른쪽 패널 공지 날짜 오른쪽에 파란 「수정하기」를 넣고, 고친 공지를 KOS 에도 반영한다(사용자 「공지사항 수정 동기화도 구현하자 · cc prototype 에 있지?」).

물음(근거 file:line · 「그대로 / 가공 / 없음」):
1. cc-prototype 동작 — `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>`: `procedure/back/app/api/reservations.py`(L230 ~ 260 `PUT /api/reservations/notice`) · `service/reservations.py`(L1016 `notice` · `PATH_NOTICE_CHANGE/CREATE/DELETE`) · `schemas/reservations.py`(L746 ~) · 화면 `procedure/front/components/reservations/ResvAside.tsx` 등. 편집 UI(모달 · 인라인 · 문구 · 버튼) · 대상 공지 고르기 · 만들기 / 고치기 / 지우기 분기 · 과거 날짜 409 · 길이 상한 · 실패 처리 · 기록(event_log)을 표로.
2. KOS 명령 — `meta/notice/v1/commands/change-content` · `create-notice` · `delete-notice` · 조회 `meta/notice/v1/queries/get-notices` 의 요청 · 응답 모양(cc 코드 · `/Users/kknaks/git/ax-clinic-project` KOS 문서 · openapi). 공지가 날짜당 몇 개인지 · released 시각 의미.
3. DAY 쓰기 경로 — DAY 는 KOS 쓰기를 어떻게 하나(`backend/day/services/outbox_kick.py` · `board_chart_writes.py` · `external_outbox` 모델 · 시술 현황 쓰기). 공지 쓰기를 같은 길(쓰기 큐 → 확인)로 태울 수 있나, 직접 호출이 맞나 — 기존 결정 · SPEC(mediness `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec/products/day/`) 근거.
4. DAY 공지 저장 · 동기화 — `models/notification.py` `notice` 테이블 · 공지 동기화 코드(어디서 KOS get-notices 를 받나 · 주기) · 예약 현황이 공지를 읽는 곳(`queries/reservations.py`). 고친 뒤 화면에 언제 보이나.
5. 시안 — `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/20261113_예약현황_시연 (1).html` 공지 부분(renderSide `nt-in`) · 「수정하기」 관련 문구가 있나. 사용자 요청 = 날짜 오른쪽 파란 「수정하기」.
6. 권한 — cc 는 누가 고칠 수 있었나 · DAY 권한 키 후보.
7. 코디가 정할 것(추천 포함): 편집 UI · 쓰기 방식 · 실패 표시 · 권한 · 과거 날짜.

금지: 코드 · 문서 고치기 · 커밋 · KOS 직접 호출 · deploy/*.env 읽기 · 스택 건드리기. 고객 정보 출력 금지.
워크트리(코드 읽기): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation`
리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/research-notice-1-report.md` — 맨 위 물음 1 ~ 7 표. preamble 의 worker_done.
