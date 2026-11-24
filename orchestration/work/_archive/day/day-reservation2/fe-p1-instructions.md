
# [frontend · 1판] 예약 — 예약 등록 창 · 예약 상세 모달 틀 · 우클릭 · 동행 · 예약 현황 SSE 화면

너는 **day `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **backend 워커가 같은 워크트리에서 동시에** `emr/` · `dtos/` · `services/` · `routers/api/` · 스트림 라우트 · migrations · 그 테스트를 만든다 — 건드리지 마라. **너는 앞 맥락이 없다.**

## 1판 범위 (Delivery CENTURION_DAY#275 · 승인됨 · 이것만)

예약 등록 창(새 고객 W1 → W2 → W3 · duplicate_token · get-visitor) · 예약 상세 모달 **틀**(머리 · 고객 정보 · 예약 정보 · 이전 방문 · 의사 지정 · 동행 — **오른쪽 시술 목록 · 수납은 3판**, 신분확인 · 문진 · 건강정보 줄은 빈 값 · [문진 QR] · [여권 스캔] 비활성 자리) · 예약 상태 버튼 [예약 취소] · [예약 변경] 창 · 우클릭 옮기기 / 취소 / 동행 추가 · 동행 저장 · **끌어 놓아 묶기 제거** · **예약 현황 SSE**(10초 폴링 제거) · **쓰기 바닥 + D53 즉시 확인**(보낸 즉시 `get-schedule-detail` 1초 간격 다시 읽어 expect · 짧은 상한 넘으면 다음 회차) · 권한 `reservation.detail`.
KOS 쓰기 새로 엶: reserve · update-reservation · create-visitor · 공개 cancel-reservation (+ 같은 고객 찾기 읽기). 2 ~ 4판(접수 · 상담 · 시술 · 귀가) 은 **하지 마라**.

## SSOT

- Issue #275 본문(Target Delta · Acceptance · Non-Goals) — `gh issue view 275 --repo MediSolveAIDev/CENTURION_DAY`
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/delivery-1-report.md` — BE ↔ FE **계약 W · S · V**(이게 둘 사이 계약)
- SPEC-007 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec/products/day/20-spec/spec-007-reservation-detail.md`(PR #961 · `54bbeb14`) · SPEC-006 ⑫ · 002 ㉘ · 000 ②
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D56 · D53 = 이번 판)
- 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-23-reservation/20261124_예약현황_시연.html`(생김새 · 문구 정본 · base64 빼고 grep)
- KOS 실물 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-1 ~ 4-report.md`

**질문하지 말고 기준으로 정해라**: KOS 에 있는 값 = KOS 를 따른다 · 화면 = 시안을 따른다 · 데이터 없는 칸 = 빈 값 · 다음 판 동작 = 비활성 / 없음. 이 기준으로도 안 정해지는 것만 코디에게.

## frontend 몫

예약 등록 창 · 예약 상세 모달 틀(1판 칸) · 확인 창(시안 문구만) · 우클릭 메뉴 · 옮기기 모드(점선 · 끌어 놓기) · 동행 체크 · 카드 위 끌어 묶기 **제거**(day.js) · 예약 현황 SSE 연결(계약 S · `board.html` · `day.js` 방식 · 10초 폴링 제거) · 결과 전 버튼 잠금 · `write_confirmed` 성공 알림 · `kos_failed` 공용 토스트 + 「다시 시도」 · 화면 테스트. 계약 V 의 화면 값 이름대로(없으면 backend 와 `contract-v1.md`(같은 폴더)에 먼저 적어 맞춤 · backend 가 늦으면 계약 모양 가짜 값으로 화면 테스트).

## allowed_paths
`backend/day/routers/`(api/ · 스트림 라우트 제외) · `templates/` · `static/` · `styles/` · `backend/tests/day/web/` · `contract-v1.md`.

## 하지 말 것
화면 문구 짓기(시안 · 결정에 있는 글자만) · 인라인 스크립트 · 손 CSS · backend 몫 파일 · 커밋 · push · 로컬 스택 · 사용자 포트 · 2 ~ 4판.

## 8. 검증

```
uv run pytest -q <네가 만든 화면 테스트만>(TestClient 로 전체 페이지 · HX 조각 렌더 확인) — 1회. CSS 를 다시 빌드했다면 빌드 명령 1회. 인라인 스크립트 0 · 손 CSS 0(grep). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_a0519d50-d55f-45ae-b9cd-0e5d8682ac98 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
