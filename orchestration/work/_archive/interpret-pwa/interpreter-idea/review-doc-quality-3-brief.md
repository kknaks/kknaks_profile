# [reviewer_doc] 통키 품질 개선 — SPEC 0.8.2 · WORK WP23 검수 (§4.2.4 시드 `.7` 값)

너는 **interpret-pwa `reviewer_doc` 워커**다. 0.8.0 · 0.8.1 을 네가 검수했다 — 맥락이 없으면 아래부터. **read-only** — 리포트 1개만.
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 변경: `git diff -- para/projects/summer-star/interpret-pwa/20-spec para/projects/summer-star/interpret-pwa/30-work` (커밋 `b0892cbb` = 0.8.1 이후 · 0.8.2)
- 발주: `orchestration/work/interpreter-idea/quality-spec-fix2-brief.md` · 추가 지시 `quality-spec-fix2-add-1.md`(D-53 은 OQ 아님)
- planner 보고: `orchestration/work/interpreter-idea/quality-spec-report.md` 끝 「0.8.2」 절
- **값의 SoT**: `orchestration/work/interpreter-idea/quality-research-dispositions.md`(§1 · §2 · **§4 OQ-030 처분 — e 는 planner 기본값과 다름** · §5 열린 것) · `quality-r1-zh-cells.json` · `quality-r2-en-ja-th-vi-cells.json` · DEC D-46 · D-51 · D-52 · D-53
- 시드(읽기만 · `.6`): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea/back/seed/glossary.json` · 코드(읽기만 · WP21 커밋 `37aafa9`): 같은 워크트리 `back/app/service/glossary.py`

## 2. 볼 것

1. **§4.2.4 가 처분 문서 · DEC 와 한 칸씩 맞나** — 손 처분 칸(kr-014 써마지 · kr-015 리투오 · 합침 두 쌍 · D-52 토닝 zh · yue 음역 17 · 장비 영문 · 빗금 31)
2. **언어별 개수**(name 201 · alias 220 · reviewed ✗→✓ 66 · ✓→✗ 56 · 바뀐 칸 349)를 두 JSON + 시드 + 처분으로 **다시 계산해** 맞나(스크립트는 scratchpad · 레포 무수정). 코디 처분 §4-e(부위 term 에 시술 이름 안 넣음 · 7개 언어)를 적용하면 개수가 얼마나 바뀌나 — SPEC 이 아직 planner 기본값으로 적혀 있으면 「코디 처분과 다름」 으로 지적
3. **§4.6 「시드 `.7` 추정」**(ja `terms` 138 · th `terms` 전부 + 역방향 별칭 15 · zh-Hant 44 → 53)을 코드로 다시 세어 맞나 · 처분 §5(ja · th 열린 것)가 SPEC 에 열린 것으로만 있나
4. **WP23** — 변환 스크립트 입력(세 파일 + r3 JSON) · 선행(r3 · OQ-030 · ㉔) · 대조표 · 시드 검사 · 재측정 · 멈춤 조건이 backend 가 바로 짤 수 있게 정해졌나 · 합친 term 의 옛 id 처리(통역 기록 안 고침)
5. D-53 이 OQ 가 아니라 결정으로 들어갔나(추가 지시 1)
6. 근거 없는 값 0 · public(키 · 실명 · 시험 목록 · 기록 문장 0)

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report-3.md` — 판정 PASS / WARN / FAIL · 지적마다 `파일:줄` + 근거

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_9bf4f5be-03de-42ff-81a7-d3e96f2e238d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d181fbae-29f2-43bb-9a41-6bc888ca07de --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
