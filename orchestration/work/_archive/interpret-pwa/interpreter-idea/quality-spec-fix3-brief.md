# [planner] 통키 품질 개선 — SPEC 0.8.3 · WP23 보완 (문서 검수 F-1 · W-1 ~ W-3 · DEC D-54 · 처분 §4 ~ §6)

너는 **interpret-pwa `planner` 워커**다. 앞 맥락은 없다 — 0.8.0 ~ 0.8.2 는 다른 planner 터미널이 썼다. 아래를 읽고 이어서 고쳐라.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 앞 발주 · 보고: `orchestration/work/interpreter-idea/quality-spec-fix2-brief.md` · `quality-spec-fix2-add-1.md` · `quality-spec-report.md` 「0.8.2」 절
- **검수 리포트**: `orchestration/work/interpreter-idea/review-quality-doc-report-3.md` — F-1 · W-1 · W-2 · W-3 (재계산 수치 포함)
- **처분(SoT)**: `orchestration/work/interpreter-idea/quality-research-dispositions.md` **§4(OQ-030 — e 가 planner 기본값과 다름) · §5(한도 → D-54) · §6(r3 처분)**
- DEC 새 행 **D-54**: `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 조사 r3: `orchestration/work/interpreter-idea/quality-r3-tw-alias-report.md` · `quality-r3-tw-alias.json`(245행)
- 조사 r1 · r2 JSON · 시드 `.6` · 코드(WP21 `37aafa9`)는 앞 발주와 같다

## 2. 고칠 것

| # | 처분 |
|---|---|
| F-1 | §4.2.4 「읽는 법」 e 와 손 처분 칸을 **처분 §4-e(7개 언어 전부 — 부위 term 에 시술 이름을 name · alias 로 더하지 않음)**로 · OQ-030 은 「닫힘 — 코디 처분 §4」 로 · 언어별 개수 다시 계산(검수 재계산: name 199 · alias 214 · 바뀐 칸 343 · th 역방향 별칭 15 → 9 — 네가 다시 세서 맞춰라) |
| W-1 | ② F 에 r3 실제 판정 넷과 처리(처분 §6 표) · 필드 이름(`id` · `alias` · `verdict` · `sources` · `note`) · `.7` 에서 별칭으로 내려오는 옛 zh-Hant name 에도 D-53 적용 |
| W-2 | 「안 잘릴 것」 문구를 수치대로(뺌 77 반영 `.7` 순수 계산 — 22,471자 · 782자 초과 · `terms` 73 빠짐 · 역방향 별칭 0) + **D-54 절차**: WP23 v6 재측정 → 넘으면 zh-Hant 「10-27 근거」 23 → ja · th 새 별칭 중 출처 1곳뿐인 것 → 그래도 넘으면 멈추고 코디 · 사용자 |
| W-3 | 읽는 법 c 로 버리는 칸을 **id 목록으로**(문구에 기대지 않게) · ja 별칭 1개 차이 원인을 찾아 적는다 |
| WORK | WP23 을 D-54 · 처분 §6 에 맞춘다(입력에 r3 JSON · 멈춤 조건 · 재측정 순서) |

## 3. 범위 · 검증

- allowed_paths: `para/projects/summer-star/interpret-pwa/20-spec/` · `30-work/` 만. DEC · BASE · 처분 문서 · 시드 · 코드는 읽기만
- SPEC `version` 0.8.3 · 변경 이력 · 부록 A(D-54)
- 시험 목록 문장 · 통역 기록 문장 0 · 키 · 실명 0
- 보고는 `orchestration/work/interpreter-idea/quality-spec-report.md` 끝에 「0.8.3」 절로

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_abdfc414-5fdf-42c2-aca3-9c64b4cc071c \
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
