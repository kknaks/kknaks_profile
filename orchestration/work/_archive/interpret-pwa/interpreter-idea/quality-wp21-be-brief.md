# [backend] WP21 — 품질 개선 코드: v6 · context 문안 · 빈 원문 막기 · 품질 시험 스크립트 (D-43 · D-45 · D-48 · D-49 · SPEC 0.8.1)

너는 **interpret-pwa `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea` (origin/main `e0fbda8` 에서 시작 · 깨끗함)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다. 이 워크트리는 너 혼자 쓴다(front 변경 없음).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` (**0.8.1** · 코디 커밋 `b0892cbb`) ← 계약의 SoT. **여기 없는 건 발명하지 마라.** 볼 절: §4.5(문안 S1 ~ S4 · `text`) · §4.6(한도 · 계산 방법) · §5.1 · **§5.10**(STT v6) · **§5.11**(빈 원문 막기) · §9.1(「STT 설정」 · 「context `text`」 · 「빈 원문」 · 「기본값 = 켬」) · **§9.3 「6차」**(품질 시험 · 조합을 바꾸는 길 · 규칙 종류 · 결과 · ㉒)
- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP21 행** — 할 일 ① ~ ⑥ · 산출 파일 · 완료 조건 · 검증 명령. **이 행이 이번 일의 전부다**
- DEC-001 **D-43 · D-45 · D-47 · D-48 · D-49**: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 문서 검수 리포트(참고 — SPEC 이 왜 이렇게 됐나): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/review-quality-doc-report.md` · `-2.md`
- 코드 레포 `AGENTS.md`(있으면)

**기대는 개념**: 해당 없음.

## 2. 배경

베타에서 「토닝 · 울쎄라 · 써마지 · 시술 → 수술 뉘앙스」 오역 지적이 나왔다. 원인 중 코드 쪽(모델 · 역할 모름 · 원문 없는 번역)을 이번 WP 가 고친다. 사전(시드) 보정은 **WP23** 이다 — **시드 파일은 건드리지 마라.**
품질 시험 스크립트(⑤)는 다음 WP22 에서 **고치기 전 조합(v5 · 시드 `.6` · 문안 없음 · 막기 끔)**을 돌리는 데 쓰인다. 그래서 조합을 바꾸는 길이 SPEC §9.3 표대로 **운영 함수의 선택 인자로만** 있어야 하고, 기본값(인자 없음)이 곧 운영 동작이어야 한다.

## 3. 시험 목록 · 키

- 시험 목록(로컬 전용 · git 제외 · **문장을 레포 · 시험 · 보고에 옮기지 마라**): `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/reference/2026-11-12-interpreter-idea/test-sentences.md` — 스크립트는 이 경로를 **인자로** 받는다. 규칙 파일은 WP22 에서 만든다 — WP21 은 규칙 파일 **형식**(SPEC §9.3)을 읽을 수 있는 스크립트까지
- Soniox 키: 사용자 파일 `/Users/kknaks/git/toy_pr2/interpret-pwa/.env` 에 있다. **워크트리로 복사하지 말고**, 실물 ㉒ 를 돌릴 때 그 파일을 읽어 프로세스 env 로만 넘겨라(값 출력 · 로그 · 보고 금지). 다른 프로세스 · 포트는 건드리지 마라
- 실물 ㉒ 는 Soniox 연결만 확인한다(7개 언어 × v6 · 문안 포함 · 거절 0 · 글자 수 · 뺀 수). **품질 시험 전체 실행은 WP22 — 이번에 돌리지 마라**(합성 음성 몇 개로 스크립트가 끝까지 도는지 연기 시험 1회는 해도 된다 · 결과 문장은 보고에 넣지 마라)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/` (단 `back/seed/` 는 읽기만)

## 6. 구현 단계

1. WORK **WP21 ① ~ ⑥** 그대로
2. 멈춤 조건: ㉒ 에서 **정방향이 빠지거나 거절이 나면 멈추고 코디에게 질문**(OQ-028)
3. 보고서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/work/interpreter-idea/wp21-be-report.md` (역할 rules 의 리포트 형식 · 문장 0 · 수치만)

## 7. 범위 제약 — 하지 말 것

- 시드 · front · infra 변경 금지 · `GENERAL` · `TRIM_ORDER` · `CONTEXT_MAX_CHARS` 변경 금지
- 끊김 값(`max_endpoint_delay_ms` 등) 변경 금지 — 스크립트의 조합 인자로만
- 조합 · 막기 · 문안을 env · `config.py` · WS `start` 로 바꾸는 길을 만들지 마라
- SPEC 에 없는 일반 낱말 짝을 `translation_terms` 에 넣지 마라

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
