# [planner] 통키 품질 개선 — SPEC 0.8.1 · WORK 보완 (문서 검수 WARN 6 + D-49 · D-50)

너는 **interpret-pwa `planner` 워커**다. 앞 판(SPEC 0.8.0 · WORK WP21 ~ WP25)을 네가 썼다 — 맥락이 남아 있으면 이어서, 없으면 아래 파일부터 읽어라.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토/orchestration/roles/interpret-pwa/planner/` · 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/아이디어-검토` · ⚠ PUBLIC

## 1. 읽을 것

- 앞 발주: `orchestration/work/interpreter-idea/quality-spec-brief.md` (§3 계약 · §7 제약 그대로 유효)
- 앞 보고: `orchestration/work/interpreter-idea/quality-spec-report.md`
- **검수 리포트**: `orchestration/work/interpreter-idea/review-quality-doc-report.md` — W-1 ~ W-6
- DEC 새 행 **D-49 · D-50** 과 고친 **D-47**(방향 — `endpoint_sensitivity` 는 덜 끊으려면 낮춘다): `para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`

## 2. 고칠 것 (코디 처분)

| # | 처분 |
|---|---|
| D-49 (OQ-025 닫힘) | §4.5 문안을 **S1 ~ S4 네 문장**으로(S4 후보 문안을 본문 코드블록에) · 상수 · §9.1 시험 · §4.6 글자 수 · 한도 영향(zh-Hant · th) 다시 계산 · OQ-025 를 「닫힘 — D-49」로 · 부록 A |
| D-50 (OQ-029 닫힘) | §9.3 손님 쪽 문장 = **7개 언어 × 3 = 21** · OQ-029 닫힘 · 부록 A |
| W-1 | **조합 A · B 는 조립 · 세션 함수의 선택 인자로만 끈다** — 운영 기본값 = 켬(문안 넣기 · 빈 원문 막기), env · WS 로는 못 끔. 모델 이름 · 시드 파일 · 역방향 짝 하나 빼기도 같은 길(스크립트가 인자로). §9.3 「조합」 에 그 길을 적고, A · B 확인 항목에 「막힌 빈 원문 수 = 0(막기 꺼짐)」 추가 · §9.1 에 「기본값 = 켬」 시험 한 줄 |
| W-2 | 3절 정의를 「쉼이 있어도 **기대한 수의** 발화로 나오는가」로 · 규칙 파일에 문장마다 **기대 확정 발화 수** · 조각 수 = 실제 − 기대 (§9.3 · WORK WP22 ①) |
| W-3 | 기계 판정 규칙 종류를 못 박는다: ① 글자 그대로 ② 정규식(라틴 글자열 등) ③ 발화 수(W-2) ④ **기계로 못 옮기는 조건 = 기계 판정 없음 → 사람 판정**. WP22 ① 완료 조건에 「규칙 파일은 코디가 확인한 뒤 조합 A 실행」 |
| W-4 | 합성 언어 = **말할 문장의 언어**(한 → 외 = `ko` · 외 → 한 = 목록의 언어) · 세션 `start` 의 `lang` = 목록의 언어 |
| W-5 | D-49 로 4문장 확정 — WORK WP21 의 「OQ-025 처분이 넣는다면」 조건문 지우고 4문장으로 |
| W-6 | `progress` 셈 근거와 값 맞추기 |
| D-47 방향 | §5.10 · OQ-027 의 `endpoint_sensitivity` 서술을 공식 문구대로 단정(「Higher values make endpoints more likely」 → 덜 끊으려면 낮춤) |

## 3. 범위 · 검증

- allowed_paths: `para/projects/summer-star/interpret-pwa/20-spec/` · `30-work/` 만. DEC · BASE 는 고치지 마라(코디 소유)
- SPEC `version` 0.8.1 · 변경 이력 행
- 시험 목록 문장 · 통역 기록 문장 0(검색) · 키 · 실명 0
- 보고는 `orchestration/work/interpreter-idea/quality-spec-report.md` 끝에 「0.8.1 보완」 절로 덧붙인다

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
