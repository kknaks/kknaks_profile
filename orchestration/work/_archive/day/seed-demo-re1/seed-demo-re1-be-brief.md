
# [backend] 데모 지점 테스트 데이터 시드 — 「방 배정」 기본 · 한국어 이름 · 상담 양식 오더 메모 · 시술 4개 이상

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/seed-demo-re1`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

혼자 쓰는 워크트리다.

## 1. SSOT — 먼저 읽을 것

- 사용자 기준(2026-11-12 · 그대로): 「생성할 때 방 배정 기본으로 넣어라 · 시술 기타에 있잖아」 · 「오더 메모 넣고 환자 이름 한국어 제대로 채워서」 · 「시술도 4개 이상씩 랜덤으로」 · 오더 메모 형식 = 아래 2절 양식
- 코디가 오늘 레포 밖에서 돌린 임시 사본(참고 · 그대로 옮기지 말고 레포 규약에 맞게): `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-fix-web-app/aaec6ef4-e755-4791-a846-42b6a5a0baa8/scratchpad/seedrun/scripts/seed_demo_board.py`(이름 · 메모 · 국적 바꿈) · `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile-day-fix-web-app/aaec6ef4-e755-4791-a846-42b6a5a0baa8/scratchpad/seedrun/scripts/enrich_demo.py`(시술 더하기 · 양식 메모)

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

해당 없음.

## 2. 배경 / 무엇을 바꾸나

`scripts/seed_demo_board.py` 는 KOS **데모 지점**에 시술 대기 방문을 만든다. 지금은 ① 기타 작업을 목록에서 돌려 골라 「방 배정」이 일부에만 걸리고 ② 이름이 `[TEST] 한국 …` ③ 오더 메모가 `테스트 오더 메모 N` ④ 시술 1개 ⑤ 국적이 나라별 순환이다. 사용자 기준으로 바꾼다:

1. **기타 작업 = 「방 배정」 기본** — 병원 연결 설정의 「방 배정」 기타 작업 id(env `DAY_SEED_KOS_ROOM_ASSIGN_ETC_TASK_ID` · 이미 local.env 이름 있음 · 없으면 지금처럼 목록에서 「방 배정」 제목으로 찾고 그래도 없으면 멈춤)로 모든 방문에 넣고 방을 붙인다.
2. **이름 = 한국어 가짜 이름**(성 + 이름 목록에서 무작위 조합 · 실제 인물 · 유명인 이름 피함 · `[TEST]` 없음) · 국적 KR 기본(옵션으로 지금 국적 순환 유지 가능).
3. **오더 메모 = 상담 양식**(줄 그대로):
```
[상담내용]
N) <니즈>
H) <시술 이력>
----------------------------------
이름 :  <고객 이름>         ROOM NO. <배정 방 — 「A-룸N」이면 N, 아니면 방 이름>
실장 :  <가짜 실장 이름>       Dr:
[진단기] O

OUT TIME : <퇴실 메모>
0. 자가세안 O
- 마취크림
1. <KOS 에 실제로 들어간 시술 이름>
2. …

[특이사항] x
[임플란트 여부] x
```
니즈 · 이력 · 퇴실 메모 · 실장 이름은 스크립트 안 가짜 목록에서 무작위. 시술 줄은 **KOS 에 실제로 들어간 시술 제목**(상세 조회로 읽어 — 반영 지연 있음 · 기다렸다 다시 읽기).
4. **시술 4개 이상 무작위**(기본 4 ~ 6 · `--procedures` 로 조절) — 상품 옵션마다 지금 수납 흐름(init → add items → register → tx → accept → ticket → add-flow-tasks) 그대로 반복. 데모 지점 상품이 3개라 겹쳐도 된다.
5. 마지막 확인(`missing_parts`)이 새 메모 · 시술 수 · 「방 배정」 유무를 본다(옛 「테스트 오더 메모」 비교 없앰).

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

해당 없음 — 개발용 스크립트. 제품 코드 · API · DB 변경 없음.

## 4. 먼저 읽을 핵심 파일

- `scripts/seed_demo_board.py` 전체 — 데모 테넌트 가드 · 출력에 이름/전화/생년월일 안 냄 규약 유지
- `backend/tests/` 에서 이 스크립트 시험(`grep -rn seed_demo_board backend/tests`) — 있으면 맞춘다
- `deploy/local.env.example` — env 이름

## 5. allowed_paths — 이 밖은 건드리지 마라

- `scripts/seed_demo_board.py`
- 이 스크립트 시험 파일(`backend/tests/` 아래 · 있으면 고침 · 없으면 새로)
- `deploy/local.env.example`(env 이름 설명 한 줄이 필요할 때만)

## 6. 구현 단계

1. 위 2절 1 ~ 5 구현 · `--dry-run` 이 그대로 동작(KOS 쓰기 0)
2. 시험: 이름 한국어 · 메모 양식 줄 순서 · 「방 배정」 id 선택 · 시술 수 범위 · 가드(데모 아니면 0 요청)
3. 실물은 하지 마라(코디가 데모 지점에 1회 돌린다)

## 7. 범위 제약 — 하지 말 것

- KOS 데모 지점 · dev · prod 서버에 쓰지 마라(dry-run 만). 실제 고객 · 직원 이름 넣지 마라.
- 제품 코드(`backend/day/`) · migration 변경 금지.
- 사용자 포트 · 프로세스 · 로컬 스택 건드리지 마라.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
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
  --to term_e62e850f-aae8-4092-a945-6f9406c2af07 --from term_3aae8b41-becd-44cb-ac22-b88605bfdfbb \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_e62e850f-aae8-4092-a945-6f9406c2af07 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
