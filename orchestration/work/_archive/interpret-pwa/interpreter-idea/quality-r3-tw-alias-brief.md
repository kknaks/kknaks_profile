# [researcher] 대만어(zh-Hant) 별칭 245개 — 쓰임 확인 (DEC D-53)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · **read-only — 아래 두 파일만 만든다** · ⚠ PUBLIC

## 1. 왜

사전 `.6` 대만어 별칭이 245개(중국어 76)라 Soniox context 한도를 넘어 한국어 이름 목록 · 역방향 별칭이 잘린다. D-53: **대만 현지 클리닉에서 쓰임이 확인된 별칭만 남기고 근거 없는 별칭은 뺀다**(term · name 은 안 뺀다). 별칭마다 확인 기록이 지금 조사에 없어서 이 일을 한다.

## 2. 읽을 것

- DEC **D-53** · D-35 · D-38: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 사전(읽기만 · `.6`): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back/seed/glossary.json` — `entries["zh-Hant"].aliases`
- 대만 사이트 6곳(이번 조사 표 S · URL): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r1-zh-report.md`
- 10-27 대만 조사(별칭의 원래 근거): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-seed-tw/research-tresure-report.md` · `research-kr-brands-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-r2-ja-en-tw-report.md`(zh-Hant 부분) · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-dispositions.md`
- 이번 처분(뺄 값 · 바뀔 name): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-research-dispositions.md` — §2 의 zh-Hant 관련 처분과 어긋나지 않게

## 3. 판정 (별칭 하나마다)

| 판정 | 뜻 |
|---|---|
| 유지 — 이번 6곳 | 이번 대만 6곳 본문에 글자 그대로 있다(사이트 번호) |
| 유지 — 10-27 근거 | 이번 6곳엔 없지만 10-27 조사 리포트에 대만 현지 출처 URL 이 있다 |
| 뺌 | 둘 다 없다(대륙 표기 · 홍콩 표기 · 영문 표기를 대만 근거 없이 넣은 것 등) |
| 다른 term 과 겹침 | 같은 별칭이 다른 term 에도 있다 — 근거 있는 쪽만 |

- 영문 브랜드명 별칭(예 `Ultherapy`)도 같은 기준(대만 사이트에 있으면 유지)
- **지어내지 마라** — 새 별칭을 더하지 않는다(이 일은 빼기 확인만)

## 4. 산출 — 두 파일

1. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r3-tw-alias-report.md` — 사이트(재사용 · 새로 읽은 곳) · 판정 집계 · 「뺌」 목록(term id · ko · 별칭 · 이유) · **빼고 나면 대만어 context 가 얼마나 줄어드는지**(아래 계산) · 정할 것
2. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r3-tw-alias.json` — 245행 전부 `[{"id","alias","verdict","sources","note"}]`

계산(코드 실행 허용 · 파일 수정 없이): 작업 워크트리 코드 `back/app/service/glossary.py` 의 `build_context` 로 지금 시드와 「뺌」 을 반영한 시드(메모리에서만)의 zh-Hant context 글자 수를 한도 없이 재서 비교(`cd /Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back && uv run python …`). 한도 기준 21,689자 · 문안 포함.

## 6. 범위

- 담당 언어 zh-Hant 만 · 사전 · 코드 · 문서 수정 금지 · 결정하지 않음

## 8. 검증

- JSON 이 245행인지(시드 zh-Hant 별칭 수와 같은지) · 「유지」 행마다 출처 1개 이상

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_db3667db-6cfe-4684-aa18-85104b414f88 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: quality-r3-tw-alias" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] researcher quality-r3-tw-alias 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] researcher quality-r3-tw-alias: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
