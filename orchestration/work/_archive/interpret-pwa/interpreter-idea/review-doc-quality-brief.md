# [reviewer_doc] 통키 품질 개선 — SPEC 0.8.0 · WORK WP21 ~ WP25 문서 검수

너는 **interpret-pwa `reviewer_doc` 워커**다. 앞 맥락은 없다. **read-only** — 리포트 파일 1개만 만든다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/reviewer/` (`role.md` 외)
작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승 · 커밋 전 변경을 `git diff` 로 본다) · ⚠ PUBLIC 레포

## 1. 무엇을 검수하나

- 변경: `git diff -- para/projects/summer-star/interpret-pwa/20-spec para/projects/summer-star/interpret-pwa/30-work` (SPEC 0.7.0 → 0.8.0 · WORK WP21 ~ WP25 · README 인덱스)
- 기준(SoT): DEC-001 **D-43 ~ D-48** · OQ-021 ~ 023(닫힘) — `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` 끝 / BASE-001 입력 5 · 「확인한 사실 (코디 2026-11-14)」. **DEC · BASE 의 diff 는 코디가 쓴 것 — 검수 대상이 아니라 기준이다**
- 발주 계약: `orchestration/work/interpreter-idea/quality-spec-brief.md` §3 표 · §6 · §7
- planner 보고: `orchestration/work/interpreter-idea/quality-spec-report.md`
- 코드(읽기만 · 운영 main 과 같음): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` — `back/app/service/interpret/{soniox,langs,assembler,session}.py` · `back/app/service/glossary.py`
- 시험 목록(로컬 전용 · git 제외): `reference/2026-11-12-interpreter-idea/test-sentences.md`

## 2. 볼 것

1. **D-43 ~ D-48 · 브리프 §3 과 SPEC 이 맞나** — v6 는 모델 이름만 · 끊김 값 1루프 그대로 · `text` 는 역할 · 방향(D-45) · 일반 낱말 짝 금지 · 빈 원문 막기 판정 규칙 · 시드 `.7` 은 자리만(값 0) · 품질 시험 절차(전 · 후 · TTS 파일 · 판정 방식)
2. **근거 없는 정책 0** — 특히 §4.5 `text` 문안 S1 ~ S3 이 D-45 밖 내용을 담지 않았나 · planner 가 더한 「조합 B(v6 단독)」 · WP 순서 변경(WP22 를 WP21 뒤로)이 DEC(D-43 「v6 단독 효과를 먼저」 · D-44) 근거로 서나
3. **한도 계산(§4.6)** — `text` 를 줄이지 않는 칸으로 둔 계산 방법 · zh-Hant · th 수치가 코드(`langs.py` `CONTEXT_MAX_CHARS` · `glossary.py` `build_context`)와 맞나. 의심 가면 코드로 다시 세어 봐도 된다(파일 수정 없이)
4. **§5.11 빈 원문 막기** — 판정 규칙(「글자 · 숫자 0」)이 실제 `assembler.py` / `session.py` 흐름에서 어디에 걸리는지 SPEC 이 backend 가 바로 짤 수 있을 만큼 구체적인가 · TTS · 자막 · 기록 세 갈래가 다 정해졌나(기록은 OQ-026)
5. **§9.3 품질 시험** — 시험 목록 33개 · 다섯 분류 · 「나오면 FAIL」 기계 판정이 실행 가능하게 정의됐나 · 결과 레포 반영이 번호 · 수치만인가 · 조합 A(v5)가 v5 제거일(2026-12-15) 전 제약을 적었나
6. **WORK WP21 ~ WP25** — SPEC 절을 가리키고 입력 · 산출 · 검증 명령 · 완료 조건이 WP19 · WP20 형식과 같나 · 의존(WP23 은 조사 · 처분 뒤)이 맞나
7. **OQ-024 ~ 029** — 열린 것은 열린 것으로만 남았나(본문에서 이미 정한 것처럼 쓰인 곳 없나)
8. **public** — 키 · 계정값 · 실명 · **시험 목록 문장 · 통역 기록 문장 0**(시험 목록에서 몇 문장을 골라 SPEC · WORK 에서 검색)

## 3. 산출

- 리포트: `orchestration/work/interpreter-idea/review-quality-doc-report.md` — 판정 **PASS / WARN / FAIL** · 지적마다 `파일:줄` + 근거(D-번호 · 계약 행)
- 다른 파일 수정 금지

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
