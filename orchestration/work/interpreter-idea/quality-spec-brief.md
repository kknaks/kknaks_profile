# [planner] 통키 품질 개선 — SPEC 0.8.0 · WORK WP21 ~ (DEC D-43 ~ D-48)

너는 **interpret-pwa `planner` 워커**다. 앞 맥락은 없다. 먼저 역할 문서를 읽어라 (절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` (코디 워크트리 탑승 — 코디와 같은 트리. `reference/` · `orchestration/work/` 의 다른 파일은 건드리지 마라)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다) · ⚠ **PUBLIC 레포** — 키 · 계정값 · 실명 · **통역 기록 문장** 0

## 1. SSOT — 먼저 읽을 것

- `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` — **D-43 ~ D-48** 과 그 아래 「열린 것 (2026-11-14 · 품질 개선)」 OQ-021 ~ 023(셋 다 기본값으로 닫힘). 계약의 SoT. **여기 없는 건 발명하지 마라.** 앞 규칙 D-33 · D-35 · D-38 · D-40 도 같이 본다
- `para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` — **입력 5** · **확인한 사실 (코디 2026-11-14)** (기록 분석 · 카톡 지적 원인 · 사전 점검 · Soniox v6)
- `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` (지금 **0.7.0**) — 고칠 문서. 관련 절: §2.4 env · §4.2 ~ §4.2.3 시드 · §4.5 context 조립 · §4.6 한도 · §5.1 · §5.5 · §9.1 · §9.3 실물 · §10 · 부록 A
- `para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` — WP20 까지. 이번 WP 를 더한다
- 코드(읽기만 · 운영 main `e0fbda8` 과 같음): `/Users/kknaks/orca/workspaces/interpret-pwa/interpreter-idea`
  - `back/app/service/interpret/soniox.py` — `STT_MODEL`(27) · `stt_config`(42 ~ 56 · `max_endpoint_delay_ms` 1000)
  - `back/app/service/glossary.py` — `GENERAL`(33 ~ 37) · `ContextParts` · `build_context`(232 ~) · `to_soniox`(222) · 줄이기 순서 `TRIM_ORDER`
  - `back/app/service/interpret/langs.py` — `CONTEXT_MAX_CHARS`(31 ~ 39 · 언어별 한도)
  - `back/app/service/interpret/assembler.py` — 발화 조립 · `side` 판정(138)
  - `back/app/service/interpret/session.py` — 확정 발화 → 자막 · TTS · 기록
- 시험 목록(로컬 전용 · git 제외 — **문장을 SPEC 에 옮기지 마라**): `reference/2026-11-12-interpreter-idea/test-sentences.md` — T01 ~ T33 · 다섯 분류 · 「나오면 FAIL」 기준. OQ-021 대로 SPEC 에는 **번호 · 분류 · 판정 방식 · 파일 위치**만 쓴다
- Soniox 공식: <https://soniox.com/docs/stt/models.mdx>(v6 · 2026-11-03) · <https://soniox.com/docs/stt/concepts/context> · <https://soniox.com/docs/stt/rt/endpoint-detection>

**기대는 개념**: 해당 없음.

## 2. 배경

베타에서 실장 · 중국 코디가 「토닝 번역 어색 · 울쎄라 · 써마지가 영어로 · 시술이 수술 뉘앙스」를 지적했다. 기록 분석 결과 원인은 사전 값 · 역할(직원 → 손님)을 모르는 번역 · 잘게 끊긴 발화 · 원문 없는 번역 · STT 인식이 섞여 있다(BASE-001 확인한 사실). 이번 판은 **코드(D-43 · D-45 · D-47 · D-48)와 사전(D-46)** 두 갈래다. 사전 갈래의 **값**은 지금 다른 researcher 워커 둘이 조사 중이다 — 너는 **절차 · 규칙 · 자리**만 쓰고 값은 비워 둔다.

## 3. 계약 — DEC 에서 SPEC 으로

| DEC | SPEC 에 쓸 것 |
|---|---|
| D-43 | `STT_MODEL` = `stt-rt-v6`. 다른 STT 설정은 그대로(v5 와 API 호환 — 공식 문서 인용) |
| D-44 · OQ-021 · OQ-022 · OQ-023 | §9.3 에 **품질 시험** 절: 시험 목록 위치(로컬 전용 파일) · 분류 5개와 번호 범위 · **전후 비교 절차**(① 고치기 전 = 지금 운영 조합(v5 · 사전 `.6` · 지금 context) ② 고친 뒤) · 입력 = **Soniox TTS 로 만든 음성 파일 재생**(3절 「쉼」 문장은 쉼을 넣은 파일) · 판정 = 「나오면 FAIL」 문구는 기계 · 뜻 · 자연스러움은 사람(중국어는 중국 코디 확인 권장) · **손님 쪽(외→한) 문장 언어마다 3개 추가**(사전 보정 결과의 시술명 포함 — 문장 작성은 WP 에서, SPEC 은 조건만) · 울쎄라 원인 가르기(단독 · 나란히 · zh 별칭 `Ultherapy` 역방향 짝 유무) · 결과는 수치 · 번호만 레포에(문장 0) |
| D-45 | §4.5 context 에 **서술 칸 `text`** — 역할(한국어 쪽 = 클리닉 직원 · 상대 = 손님) · 방향(한→외 = 손님이 듣는 말 · 높임 / 외→한 = 손님이 한 말). **문안 초안을 SPEC 에 쓴다**(영어 · 언어 무관 한 벌인지 언어별인지는 근거가 없으면 OQ). `general` 도 필요하면 고친다. **일반 낱말 짝(접수 → 登记 류)은 `translation_terms` 에 넣지 않는다**(D-45). §4.6 한도: `text` 는 줄이지 않는 칸(`general` 과 같은 취급) — 지금 언어별 크기 대비 한도 여유(zh-Hant 는 거의 0)를 BASE · 코드에서 다시 세어 **언어마다 몇 개가 줄이기로 빠질지 계산 방법**을 쓴다(값은 시드 `.7` 확정 뒤 실측) |
| D-46 | §4.2.x 에 **시드 `.7` 보정 절 — 자리만**: 근거(현지 클리닉 공식 사이트 · 나라 매핑 en = 미국 · ja = 일본 · zh = 대륙 · zh-Hant = 대만 · th = 태국 · vi = 베트남 · yue = 홍콩) · 규칙(현지어 우선 · 현지에 없으면 영어 · 독립 출처 2+ 만 `reviewed: true` — D-35 그대로) · 처분 절차(조사 리포트 → 코디 처분 → 표) · 이름 겹침 원칙(앞 처분의 의도된 겹침 — 보툴렉스 = 레티보 = 乐提葆 — 는 유지) · 확인된 오류 목록(BASE 그대로). **바꿀 값 표는 비워 두고 「조사 뒤 채움」으로 표시** |
| D-47 | §5 STT 설정: 1루프는 `max_endpoint_delay_ms` 1000 그대로 · 시험 3절이 v6 에서도 조각나면 올린다(후보 값 · 지연과 맞바꿈은 사용자가 실물에서 판단 — 정하지 마라) · v6 끊김 감도 값(`endpoint_sensitivity` 등)은 공식 문서에 있는 이름 · 범위만 인용 |
| D-48 | §5 에 **빈 원문 막기**: 원문이 비었거나 문장부호 · 공백뿐인 확정 발화는 자막 · TTS 로 내보내지 않는다. 판정 규칙(어떤 글자를 문장부호로 보나)을 쓴다. **그런 발화를 통역 기록에 남길지는 DEC 에 없다 → §10 OQ 로** |

## 4. 먼저 확인할 것 (전수)

- `grep -n "stt-rt-v5\|max_endpoint\|GENERAL\|general\|translation_terms\|CONTEXT_MAX" spec-001-interpret-pwa.md` — v5 · context 설명이 나오는 자리 전부를 스스로 세고 보고에 줄 번호 목록을 붙여라
- 부록 A(결정 대응표)에 D-43 ~ D-48 행

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 구현 단계

1. **SPEC 0.8.0** — 머리 `version` · `updated_at` · 변경 이력 행 · 근거 목록 「D-01 ~ D-42」 → 「D-01 ~ D-48」
2. §3 표대로 각 절 고침 · §10 에 새 OQ(근거 없어 못 정한 것만) · 부록 A
3. **WORK** — WP21 ~ 를 더한다. 제안 순서(근거 있으면 바꿔도 된다 — 바꾸면 이유를 보고):
   - **WP21 back 코드** — v6 · `text` · 빈 원문 막기 · 시험(§9.1) · 시드는 건드리지 않음
   - **WP22 품질 시험 「전」** — 지금 운영 조합으로 시험 목록 실행(로컬 · 키는 사용자 `.env`) · 결과 JSON(번호 · 판정 · 수치만)
   - **WP23 시드 `.7`** — 조사 리포트 · 코디 처분 뒤 표대로 · 시드 검사 · context 크기 재측정(줄이기로 빠지는 수)
   - **WP24 품질 시험 「후」** — WP21 + WP23 조합으로 같은 목록 + 손님 쪽 문장 · 전후 비교 표 · 시험 3절 결과로 D-47 끊김 값 조정 여부를 코디 · 사용자에게 올림
   - **WP25 배포 · 실물** — main → Actions → infra 태그 PR → 수동 sync → §9.6 · 운영에서 대표 문장 확인
   - 「병렬」에 WP21 ↔ WP23 관계(둘 다 back 레포 · 같은 워크트리)를 적는다
4. 문서 README · `log.md` 갱신이 규칙(role 문서)에 있으면 따른다 — 없으면 하지 마라

## 7. 범위 제약 — 하지 말 것

- DEC 문서는 고치지 마라(코디 소유)
- 코드 · infra 레포 · 시드 파일은 읽기만
- **사전 값(현지명)을 짓지 마라** — 조사 리포트가 아직 없다. 표는 자리만
- 시험 목록 문장 · 통역 기록 문장을 SPEC · WORK 에 넣지 마라(번호 · 분류 · 수치만)
- `text` 문안 말고는 계약 밖 정책(끊김 기본값 확정 · 모델 비교 · LLM 번역 전환 등)을 짓지 마라 — 필요해 보이면 §10 OQ 로 올리고 보고

## 8. 검증

```
SPEC 의 모든 절이 DEC · 확정 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 계정값 · 실명 0(grep)
```

- 추가: `grep` 으로 SPEC · WORK 에 시험 목록 문장이 0 인지(파일을 열어 T 번호 문장 몇 개를 골라 SPEC 에서 검색) 확인해 보고에 적는다
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고서는 `orchestration/work/interpreter-idea/quality-spec-report.md` 에도 같은 내용으로 남긴다(워커가 죽어도 남게).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d181fbae-29f2-43bb-9a41-6bc888ca07de --from term_5fb24b1c-5649-42e7-bcfe-dd33ee95ddc7 \
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
