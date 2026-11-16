# [backend] WP23 — 시드 `.7` 사전 전체 보정 (D-46 · D-51 ~ D-54 · SPEC 0.8.4 §4.2.4)

너는 WP21 · WP22 를 한 **interpret-pwa `backend` 워커**다. 맥락이 없으면 `quality-wp21-be-brief.md` · `wp21-be-report.md` · `wp22-be-report.md` 부터.
작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`(WP21 커밋 `37aafa9` 위 · WP22 스크립트 수정은 미커밋 — 그대로 두고 이어서)

## 1. SSOT

- WORK **WP23 행**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` — 이 행이 이번 일의 전부다(입력 네 파일 · 변환 스크립트 · 대조표 · 시드 검사 · §4.6 재측정 · **D-54 순서 · 멈춤 조건**)
- SPEC **0.8.4** §4.2 · §4.2.1 · **§4.2.4**(반영 규칙 · 손 처분 칸 · 읽는 법 a ~ k · ② F · 별칭 순서) · §4.6(「D-54 절차」 · 「넘는다」 = 줄이기 없는 전체 > 기준(통과 최대치 × 0.9)): 같은 폴더 `20-spec/spec-001-interpret-pwa.md`(코디 커밋 `ee23d056`)
- 처분: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` §1 ~ §8
- 입력: `quality-r1-zh-cells.json` · `quality-r2-en-ja-th-vi-cells.json` · `quality-r3-tw-alias.json`(같은 폴더) · 시드 `.6`

## 2. 선행 처분 (WP22 ㉔ — 코디)

- **울쎄라(ph-121) zh 별칭 `Ultherapy` 를 뺀다**(처분 §8 E7). zh `name` `美版超声刀` 은 그대로

## 3. 멈춤 조건 (WP23 행 그대로 — 다시 적음)

- 변환 결과 개수가 SPEC §4.2.4 개수와 다르면 멈추고 코디에게
- §4.6 v6 재측정 → 「넘는다」 언어가 있으면 D-54 순서(zh-Hant 「10-27 근거」 → ja · th 출처 1곳뿐인 새 별칭)로 빼고 다시 잰다 → **그래도 넘으면 멈추고 코디에게**(사용자 판단 — 시드는 그 상태로 두고 보고)
- 정방향이 하나라도 빠지거나 v6 가 거절하면 멈춤

## 5. allowed_paths

- `back/seed/glossary.json` · `back/scripts/`(변환 스크립트 — 입력 경로는 인자로 · 레포에 조사 파일 복사 금지) · `back/tests/`(시드 검사 · 표 대조 — 집합 비교)
- 운영 `app/` 은 시드 검사 규칙이 SPEC 과 다를 때만(모호어 목록 §4.2.1 의 `kr-014` 예외 등) — 고치면 보고에 이유

## 6. 보고

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp23-be-report.md` — 언어별 개수(SPEC 과 대조) · 대조표 경로(레포 밖이면 경로만 · 레포용은 id · 언어 · 판정 · 개수만) · v6 언어별 통과 최대치 · 기준 · 뺀 수 · D-54 로 뺀 별칭 수 · 멈췄으면 무엇 때문에
- 시드 `version` = `2026-11-14.7`

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
