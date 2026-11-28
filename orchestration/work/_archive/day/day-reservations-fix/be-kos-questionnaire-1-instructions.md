# [backend · 실물 확인] KOS 문진(초진설문) 읽기 — 어떤 API · 제출 시각 · 문항이 DAY 와 1:1 인가

너는 **day `backend` 워커**다. 맥락이 없다고 생각하고 이 파일만 따른다. 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` (base `origin/dev` `65506f35`) — 레포 루트 `AGENTS.md` 먼저
- 앞 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/research-1-report.md`(코드 읽기 결과 · 파일:줄)

**이번 일은 구현이 아니다. 레포 파일을 고치거나 커밋하지 마라.** 스크립트는 레포 밖 `/private/tmp/<이 작업 폴더>/` 에만. 결과는 리포트 하나.

## 1. 왜

사용자 결정(11-27): 문진은 **고객 마지막 제출일부터 6개월** 지나면 다시 받는다(「6개월 경과」). **KOS 에서 받은 문진도 DAY 로 동기화**한다 — 사용자 「KOS 문진 항목이 DAY 와 완전히 같다」. DAY 는 지금 KOS 문진을 안 읽는다(research-1 §0 · Q12). 동기화를 SPEC 에 넣기 전에 KOS 가 무엇을 주는지 실물로 본다.

## 2. 쓸 것

- KOS 호출 = DAY `backend/day/emr/kos/client.py` `KosClient`(`internal()` · `open()`) 그대로. 새 HTTP 코드 짓지 마라.
- 데모 지점 값 = `/Users/kknaks/git/CENTURION_DAY/deploy/local.env` 의 `DAY_SEED_KOS_*` · `KOS_*_BASE` · `KOS_WEB_BASE` — 스크립트 안에서 읽기만 · 출력 금지.
- **데모 지점 확인 먼저**(`backend/day/emr/kos/demo/board_data.py` `check_open_key_is_demo` 와 같은 확인). 실패하면 멈추고 보고.
- 경로 근거 찾기: KOS 문서 `/Users/kknaks/git/ax-clinic-project`(초진설문 · questionnaire · survey grep · KOS 사용 캡처 `para/archive/inbox_archive/2026-10-01-kos-usage-capture-raw.md`) · HAR 이 있으면 그것 · cc-prototype(`git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:<path>`). 근거 없는 경로를 추측해 두드리지 마라 — 못 찾으면 「경로 근거 없음」으로 보고.
- DAY 문진: `questionnaire_history` 모델 · 공개 문진 서비스(`services/questionnaire_public.py`) · 문항 정의(문항 목록이 어디 있는지 찾아라).

## 3. 확인 (읽기만)

1. KOS 에서 고객의 문진(초진설문) 목록 · 상세를 읽는 API 경로 · 요청 모양 · 응답 키 모양.
2. **제출 시각** 칸 이름 · 형식(시간대) · 고객 단위인가 방문(일정) 단위인가 · 여러 번 낸 이력이 다 오나.
3. 문항: KOS 응답 문항 키 ↔ DAY 문항 **1:1 대조 표**(같음 / 다름 / 한쪽만). 「완전히 같다」가 맞는지 근거로.
4. 바뀐 문진만 가져올 길(목록 API 에 날짜 거르기 · 고객 상세에 마지막 제출 칸 등)이 있나 — 동기화 방식 후보(결정 아님).
5. 데모 고객 중 문진 낸 고객이 있는지(KOS 고객 id 앞 8자 · 개수만).

## 4. 하지 말 것

- **KOS 쓰기 금지**(읽기만). 레포 수정 · 커밋 금지. 로컬 스택 · docker · DB 건드리지 마라.
- `~/.config/day/` 아래 열지 마라. 데모 지점 말고 다른 병원 키 금지. 비밀값 · 토큰 · 고객 개인정보 · 문진 답 원문 출력 · 기록 금지(키 이름 · 모양 · O / X 만).

## 5. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservations-fix/orchestration/work/day-reservations-fix/be-kos-questionnaire-1-report.md` — 맨 위 표: 확인 1 ~ 5 × (경로 · 응답 코드 · 결과 · 비고) → 문항 대조 표 → 동기화 후보 · 정할 것.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_99b025fc-f3ef-403e-8162-509c41545e2e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_99b025fc-f3ef-403e-8162-509c41545e2e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
