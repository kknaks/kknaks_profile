# [researcher] 영문 `name` 을 그 나라 글자로 — zh · zh-Hant · yue (DEC D-61)

너는 **interpret-pwa `researcher` 워커**다. 앞 맥락은 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/researcher/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · **read-only — 아래 두 파일만 만든다** · ⚠ PUBLIC

## 1. 왜

사용자 원칙: **그 나라 글자가 있는 언어는 그 나라 글자로 표기 · 정말 없을 때만 영어.** 지금 사전 `.8` 은 앞 조사에서 「현지 클리닉도 영문을 쓴다」 · 「근거 있는 현지 표기 없음」 으로 영문 `name` 이 된 칸이 많다. D-61 은 이 칸들을 다시 본다.

## 2. 읽을 것

- DEC **D-61**(+ D-35 · D-38 · D-46): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- **대상 칸 목록**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r4-targets.json` — 담당 언어(zh · zh-Hant · yue) 행만
- 지금 시드(읽기만 · `.8`): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back/seed/glossary.json`
- 앞 조사(사이트 · 근거 재사용): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/quality-r1-zh-report.md` · `quality-r2-en-ja-th-vi-report.md` · `quality-r3-tw-alias-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/_archive/interpret-pwa/interpret-pwa-v2/research-dispositions.md`(10-27 처분 — 「한국 전용 음역 → 영문」 은 D-61 이 다시 본다)

## 3. 방법

- 칸마다 그 나라 글자 표기를 찾는다. 근거 = 그 나라 **피부과 · 미용 클리닉 공식 사이트**(앞 조사 6곳 + 필요하면 더) · **현지 의료미용 플랫폼**(손님이 보는 표기 — 예 대륙 新氧 · 대만/홍콩 현지 플랫폼 · 태국 현지 플랫폼 · 일본 현지 예약 플랫폼 — 이 조사에서만 근거로 친다). 한국 병원의 외국어 페이지 · 한국 회사 플랫폼(강남언니 · creatrip 등)은 근거 아님
- zh · zh-Hant · yue 는 136칸(zh 42 · zh-Hant 29 · yue 65) — 중국어권은 한 플랫폼에 간체 · 번체가 같이 있으면 둘 다 쓴다(zh 간체 · zh-Hant · yue 번체)
- **지어내지 마라** — 음역을 만들지 마라. 별명(색 별명 · 「绿毒」 류)은 이름이 아니다 — 「별명」 으로 표시만
- 지금 별칭에 그 나라 글자 꼴이 있으면 그것부터 근거를 찾는다

## 4. 판정 (칸마다)

| 판정 | 뜻 |
|---|---|
| 현지 글자로 | 근거 1곳 이상 — 제안 `name`(그 나라 글자) · 영문은 별칭으로 · 출처 2+ 면 reviewed 제안 true |
| 현지 표기 없음 | 클리닉 · 플랫폼 모두 영문만(또는 0건) — 영문 그대로 |
| 일반어 | 브랜드가 아니라 일반 시술 · 성분명(PRP · PDRN · IPL 류) — 현지 일반 명칭이 있으면 「현지 글자로」 |
| 별명뿐 | 현지 글자 꼴이 별명뿐 — 영문 그대로 · 별명은 쓰지 않음 |

## 5. 산출 — 두 파일

1. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/r4a-zh-report.md` — 사이트 · 플랫폼 목록(번호 · URL) · 판정 집계 · 「현지 글자로」 표(id · ko · 언어 · 지금 name · 제안 name · 별칭 · 출처 · reviewed) · 「현지 표기 없음」 목록 · 정할 것
2. `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/r4a-zh.json` — 담당 언어 대상 칸 전부 `[{"id","lang","current","verdict","proposed_name","proposed_aliases","sources","reviewed_suggest","note"}]`

## 6. 범위

- 담당 언어(zh · zh-Hant · yue)만 · th · ja 는 다른 워커 · 사전 · 코드 · 문서 수정 금지 · 결정하지 않음

## 8. 검증

- JSON 행 수 = 대상 목록의 담당 언어 행 수 · 「현지 글자로」 행마다 출처 1개 이상

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_133d6a82-b91e-4f3d-97c0-dd0ef56a50c4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: r4a-zh" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] researcher r4a-zh 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] researcher r4a-zh: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
