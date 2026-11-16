# [planner] 통키 품질 개선 — SPEC 0.8.2 · §4.2.4 시드 `.7` 값 채우기 (D-46 · D-51 · D-52 · 조사 처분) + 검수 N-1 ~ N-3

너는 **interpret-pwa `planner` 워커**다. 0.8.0 · 0.8.1 을 네가 썼다 — 맥락이 없으면 아래부터 읽어라.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- DEC **D-46 · D-51 · D-52**(+ D-35 · D-38 · D-40): `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- **처분(확정)**: `orchestration/work/interpreter-idea/quality-research-dispositions.md` — §1 칸 판정 → 반영 규칙 · §2 정할 것 29건 처분. **이 문서가 값의 SoT**
- 조사: `orchestration/work/interpreter-idea/quality-r1-zh-report.md` · `quality-r1-zh-cells.json`(510) · `quality-r2-en-ja-th-vi-report.md` · `quality-r2-en-ja-th-vi-cells.json`(680)
- 지금 시드(읽기만 · `.6`): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back/seed/glossary.json`
- 검수: `orchestration/work/interpreter-idea/review-quality-doc-report-2.md` N-1 ~ N-3
- 앞 선례(시드 표를 SPEC 에 어떻게 썼나): SPEC §4.2.2 · §4.2.3(0.6.0)

## 2. 할 것

1. **§4.2.4 「시드 `.7`」 을 채운다** — 「조사 뒤 채움」 자리를:
   - 반영 규칙(처분 §1 그대로) · 처분 표(§2 — 29건 · D-51 새 term 「써마지」 · D-52 토닝 zh · 리투오 새 term · 합치는 term 두 쌍(ph-105 ← ph-106 · ph-097 ← ph-127) · 확인된 값 오류)
   - **칸 전부를 표로 옮기지 마라.** 값의 원천은 `cells.json` 두 파일 + 처분 문서다. SPEC 에는 ① 규칙 ② 예외 · 수동 처분 칸 목록(처분 §2 가 손으로 정한 칸 — 이건 표로) ③ 규칙을 기계 적용했을 때 **언어별 개수**(name 바뀜 · alias 더함 · alias 뺌 · reviewed 바뀜 · 반영 안 함(vi S3 단독))를 네가 두 JSON 과 시드로 **직접 계산해** 적는다(계산 스크립트는 scratchpad · 레포에 넣지 마라)
   - 새 term id 규칙(지금 시드의 id 체계를 보고) · 합친 term 의 id 처리(통역 기록의 `terms` 에 옛 id 가 남는 것 — 기록은 고치지 않는다고 적기)
   - 시드 `version` = `2026-11-14.7`(형식은 지금 시드를 따른다)
2. **WORK WP23** 을 이에 맞춘다 — backend 가 두 JSON + 처분을 읽어 시드를 바꾸는 **변환 스크립트**(레포 `back/scripts/`)로 반영 · 결과 대조표(바뀐 칸 목록)를 보고에 · 시드 검사 · §4.6 한도 재측정(언어별 뺀 수)
3. **§10 새 OQ 하나 — 대만어(zh-Hant) 별칭 정리**: 지금 한도로 zh-Hant 역방향 별칭 33개(문안 넣으면 44)가 잘린다. 코디 제안 = 「대만 6곳 · 10-27 조사에서 쓰임이 확인된 별칭만 남기고 근거 없는 별칭은 뺀다(term 은 안 뺌)」 — 별칭마다 확인한 기록이 지금 조사에 없어서 짧은 조사가 한 번 더 필요하다. **사용자 미정 — 열린 것으로만** 쓰고, WP23 선행 조건에 「이 OQ 처분」 을 넣는다
4. 검수 N-1 ~ N-3 고침
5. SPEC `version` 0.8.2 · 변경 이력 · 부록 A(D-51 · D-52)

## 3. 범위 · 검증

- allowed_paths: `para/projects/summer-star/interpret-pwa/20-spec/` · `30-work/` 만. DEC · BASE · 처분 문서 · 시드 · 코드는 읽기만
- 처분 문서에 없는 값을 짓지 마라 — 규칙으로 안 닫히는 칸이 나오면 OQ 로 올리고 보고
- 시험 목록 문장 · 통역 기록 문장 0 · 키 · 실명 0
- 보고는 `orchestration/work/interpreter-idea/quality-spec-report.md` 끝에 「0.8.2」 절로

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_bab04d70-ca05-420e-8996-9e7d2e3a953b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
