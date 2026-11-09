# [reviewer · 읽기 전용] 시술 현황 시안 검수 — 명동점 업무 흐름 · KOS HAR · cc-prototype 코드 · DAY 데이터 모델 대조

너는 day reviewer 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/`. **읽기 전용** — 어떤 파일도 고치지 마라 · 커밋 금지. 산출물은 리포트 1개.
**범위 = 시술 현황 화면만**(사용자 2026-11-06). 예약 · 접수 · 상담 · 채팅 · 알림 화면은 보지 않는다(경계에서 넘겨받고 넘겨주는 지점만).

## 대조할 원천

| 무엇 | 위치 | 역할 |
|---|---|---|
| **시안(검수 대상)** | `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` (약 3MB · data URI 포함 — HTML · CSS · JS 구조로 읽어라) | 생김새 정본 |
| 명동점 업무 흐름 | `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-10-12-cc-prototype/workflow-v2.md`(**시술 구간 정본** · 10-16 명동점 인터뷰) · `workflow-v1.md`(처음 생각한 흐름 — 참고) · `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-10-26-cc-reservation/workflow-v3.md`(앞 · 뒤 경계 — 수납 뒤 시술 대기로 들어오는 곳 · 귀가 대기로 나가는 곳만) | 현장이 실제로 하는 일 |
| KOS HAR | `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-12-cc-prototype/` 의 `시술현황_새로고침.har` · `시술현황_방배정.har` · `의사호출.har` · `의사호출_2.har` · `시술완료.har` · `시술완료_상태.har` · `로그인.har` (gitignore · **실제 병원 데이터일 수 있다**) | KOS 가 실제로 주는 필드 |
| KOS 공개 API 정리 | `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-10-12-cc-prototype/kos-demo-api.md` | 참고 |
| cc-prototype 코드 | `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<경로>` — `procedure/front/components/procedures/*` · `procedure/front/app/**/live*`(현황판 페이지) · `procedure/back/app/domain/rules.py` · `api/board.py` · `service/board_service.py` · `kos/sync.py` | 이미 구현된 동작 |
| cc 결정 · 계약 | workflow-v2 머리말이 가리키는 DEC-005 · SPEC-003 · SPEC-004 (`/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/`) | 동작 규칙의 근거 |
| DAY 데이터 모델 | `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-000-data-model.md` §3 03(visit · visit_flow_log) · 05(작업 · 호출 · 마취 · 카드 순서) · 06(방 · 구역) | DAY 가 저장하는 칸 |
| 앞 조사 | `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-ds-research-report.md`(시안 요소 E01 ~ E56 · DS gap) | 요소 번호를 재사용해라 |

**HAR 보안**: 필드 이름 · 타입 · 구조 · 건수만 적는다. 이름 · 전화 · 차트번호 · 테넌트 id · 토큰 · 메모 원문 등 **값은 리포트에 한 글자도 옮기지 마라.**

## 볼 것

1. **시안 → 데이터 근거**: 시안이 보여 주는 값 하나하나(카드 · 배지 · 시간 · 이름 · 메모 · 아이콘 상태)가 어디서 오는지 — KOS 응답 필드(HAR 경로) / DAY 테이블 칸 / 계산(규칙 · 근거) / **근거 없음**. 근거 없음은 「추정으로 채우면 안 되는 자리」로 따로 모은다.
2. **업무 흐름 · cc → 시안**: workflow-v2 의 단계 · 동작(시작 · 종료 · 마취 · 의사 호출 · 수락 · 방 배정 · 드래그 순서 · 귀가 대기 등)과 cc 구현의 동작 · 규칙(마취 20분 · 호출 5분 · 상태 2계층 등)이 시안에 있는지 — 있음 / 다른 모양으로 있음 / **없음**.
3. **서로 다른 것**: 시안 · workflow · cc · DEC/SPEC 이 서로 다르게 말하는 상태 이름 · 단계 순서 · 기준값 · 누가 무엇을 누르는지. 어느 쪽이 최신인지 날짜 근거와 함께.
4. **KOS 에 있는데 아무 데도 안 쓰는 것**(시술 현황 HAR 기준): 화면에 쓸지 판단할 후보.
5. **DAY 데이터 모델 빈칸**: 시안 · 흐름에 필요한데 SPEC-000 에 칸 · 테이블이 없는 것(또는 그 반대 — 모델에 있는데 화면 어디에도 안 나오는 것).
6. 시안 안의 「정하기 전 · 아직 없음」 주석과 workflow-v2 「정할 것」 중 시술 현황에 걸린 것.

## 하지 말 것

결정하지 마라 — 판단이 필요한 것은 선택지와 근거로. 가상 시나리오를 만들어 실패를 세지 마라 — 지금 원천이 말하는 것만. KOS API 를 호출하지 마라(HAR · 문서만). 시안을 브라우저로 열 수 있으면 열어도 되지만 파일을 바꾸지 마라.

## 보고

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-screen-procedure-report.md`:
- 요약(1 ~ 5 각각 건수)
- **사용자 결정이 필요한 것** 목록 — 항목마다 무엇이 부딪히나 · 선택지 · 근거(파일:줄 / HAR 경로 / 시안 요소 E번호) · 리뷰어 추천 하나
- 나머지 표(1 ~ 6)
- 확인 못 한 것
완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` **둘 다**).
