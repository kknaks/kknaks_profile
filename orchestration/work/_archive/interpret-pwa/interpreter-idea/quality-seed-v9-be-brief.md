# [backend] 시드 `.9` — 영문 name 을 그 나라 글자로 (D-61 · 처분 §15)

너는 WP21 ~ WP26 을 한 **interpret-pwa `backend` 워커**다. 작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`(코드 커밋 `0ec772d` 위)

## 1. SSOT

- DEC **D-61**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- **처분 §15**(+ §12 ~ §14): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` — 이 표가 값의 SoT
- 조사: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/r4a-zh.json` · `r4a-zh-report.md` · `r4b-th-ja.json` · `r4b-th-ja-report.md`
- 시드 지금 `.8`

## 2. 할 것

1. 변환 스크립트(`back/scripts/seed_v9.py` — 입력 경로는 인자 · 재실행 같은 바이트)로 `.8` → `.9`(`version` = `2026-11-15.9`):
   - r4a · r4b 의 「현지 글자로」 · 「일반어」 칸 → 처분 §15 대로 `name`(그 나라 글자) · 영문 옛 name 은 별칭 · `reviewed`
   - §15 「안 씀」 칸 · 「현지 표기 없음」 · 「별명뿐」 은 그대로
   - §15 r4a-9 · r4b-9: zh · th 근거 없는 별칭 빼기(조사 리포트 목록 그대로)
   - 틀린 꼴: 새 name 과 겹치면 그 꼴만 빼고 보고
2. 시드 검사 · `ruff` · `pytest` 1회 · 바로잡기 연기 확인(WP26 과 같은 39행 — 바뀐 name 으로 다시)
3. **㉒** 7개 언어 연결 — 거절 0 · 줄이기 0 확인. 넘는 언어가 있으면 D-54 순서(출처 약한 별칭부터)로 빼고 다시 · **그래도 넘으면 멈추고 보고**
4. 대조표(바뀐 칸: id · 언어 · 옛 name → 새 name · reviewed) — 레포용 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/seed-v9-diff.json`
5. 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/seed-v9-be-report.md` — 언어별 name 바뀐 수 · 별칭 뺀 수 · ㉒ 표 · 남은 영문 name 수(5개 언어)

## 5. allowed_paths

- `back/seed/glossary.json` · `back/scripts/` · `back/tests/`

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
