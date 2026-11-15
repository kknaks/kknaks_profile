# [backend] WP27 — 7차 나라별 시험 · 최종 버전 · 결과 페이지(언어별 탭) (D-57 · D-59 · D-61 · D-62)

너는 WP21 ~ 시드 `.9` 를 한 **interpret-pwa `backend` 워커**다. 작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`

## 1. 먼저 (D-62)

- 시드 `.9` 그대로 받는다(ja · th `terms` 줄이기 OK — 짝 손실 0) · **reviewed 6칸**(보고서 「확인 부탁」 — zh-Hant ph-080 · yue ph-132 · yue ph-157 · zh kr-008 · th ph-007 · th ph-088)을 `true` 로 한 줄 바꿈 · 시드 검사 · pytest 1회

## 2. WP27 (WORK 행 그대로 — 단 시드는 `.8` 이 아니라 **`.9`**)

- SSOT: WORK **WP27 행** · SPEC 0.9.1 §9.3 「7차」 ㉗ · §5.12 — `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/`
- ① 목록(로컬 전용 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/test7-sentences.md`) — 직원 쪽 S01 ~ S10(6차 음성 그대로 · 해시) · S11 ~ S19(시술 9개 한국어 문장 · 음성 새로) · 손님 쪽 G01 ~ G09(언어마다 · **시드 `.9` 의 그 언어 name 으로**). **S11 ~ S19 · G01 ~ G09 초안을 쓰고 음성을 만든 뒤 멈춘다 → 코디 확인 → 실행**
- ② 규칙 = 스크립트가 시드 `.9` 에서 만든다(로컬 `test7-rules.json`)
- ③ 196행 실행(최종 버전 · 조합 인자 없음)
- ④ **결과 페이지 HTML 하나**(로컬 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/quality-run/test7-result.html` · 언어별 탭 7 · 탭마다 직원 쪽 표 · 손님 쪽 표 — 번호 · 시술 · 원문 · 번역 · 기계 판정 · 바로잡기 표시(바꾸기 전 글 같이) · 사람 판정 칸 · **현지 표기 없음 표시**(그 언어 name 이 영문인 term) · 탭 머리에 수치 · 외부 요청 0 · 사람 판정은 코디가 넣을 수 있게 JSON 하나를 읽어 그리는 구조)
- ⑤ 레포용 JSON(번호 · 판정 · 수치만) `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/test7-*.json`
- 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp27-be-report.md`

## 5. allowed_paths

- `back/seed/glossary.json`(reviewed 6칸만) · `back/scripts/` · `back/tests/` · 위 로컬 경로(git 제외 폴더)

## 8. 검증

```
back 에서 uv run pytest · uv run ruff check . — Phase 범위에 맞게 1회씩, 통과하면 반복하지 마라. Soniox · Procedure Hub 경로는 실물 호출 1회(키 없으면 pending). 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_1408924f-69e8-469c-b6b1-8e4fe8ed9c6b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
