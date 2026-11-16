# 리뷰 리포트 — llm-codex-hotfix / planner 리뷰 (SPEC 4건 + WP-133) (2026-11-13)

## 판정: **WARN** (FAIL 사유 없음 — 아래 경미 6건은 코디네이터 판단으로 수정 재발주 또는 진행)

## 검수 범위
- 워크트리 `llm-codex-hotfix-spec` (HEAD = origin/mediness `8180696a`, 미커밋): 수정 6 + untracked 1
  - `products/mediness/30-work/work-133-server-llm-codex-hotfix.md` (신규)
  - `20-spec/spec-070-briefing.md` · `spec-111-decision-intake-slack.md` · `spec-116-okknaks-v2-migration.md` · `spec-130-weekly-report.md`
  - `30-work.md` · `log.md`
- allowed_paths(`products/mediness/`·`context/`) 이탈: **0**
- 실행한 검사:
  - `python3 scripts/lint-pipeline.py --strict` → **0 error / 263 warning, exit 0**. 이번 변경 파일(WP-133·SPEC-070/111/116/130·30-work.md)에 걸린 WARN **0**. 263 WARN 은 전부 기존 것이라 무관 (예: `products/selly/30-work.md:1 YAML frontmatter 없음`).
  - 코드 대조: mediness-app `origin/main` = `67b6a7dc` (survey 의 prod 배포본과 동일). `git show` 로 decision_gate.py · decision_gate_tools.py · decision_gate_stream.py · pipeline_ingest_consumer.py · brief/synthesizer.py · weekly_report_pipeline.py · meeting_v2_submission.py · meeting_v2_extractor.py · meeting_extractor_client.py · landing_chat/submission.py · config.py · worker-entrypoint.sh 를 읽었다.
  - 전수 grep: `git grep -nE 'provider=|"claude"|claude-|meeting_llm_batch|AgentClient\(' origin/main -- back/app`, `_default_ai_call` 호출처 grep, back/tests 의 claude 인자 단정 grep.
  - ID 충돌 점검: 최근 갱신 remote 브랜치 40개에서 `MEDINESS-WP-133`·`MEDINESS-DOC-255`·`work-133` 를 찾았다 → 0건. 현행 doc_no 최댓값은 254 이고 255 는 유일하다.

## 위반 (FAIL 사유)
- 없음.

## 경미 (WARN)

1. **`work-133-server-llm-codex-hotfix.md:102`·`:173` (Open ③) — C 의 lint 동작을 잘못 적었다.** `lint_markdown`(`synthesizer.py:398-420`)은 H1·9절·금지 토큰을 **부분 문자열 포함(`in`)** 으로만 본다. 그래서 codex 가 본문을 ```` ```markdown ```` 펜스로 감싸거나 머리말 산문을 붙여도 **lint 는 통과한다.** 그 결과 FAILED 가 나는 대신, 펜스와 산문이 섞인 본문이 조용히 `markdown_body` 에 저장·발행된다. 위험의 방향이 WP 서술과 반대다. 예외는 머리말에 금지 토큰(`내가 `·`본인이` 등)이 들어가는 경우뿐이다.
   - 근거: 사실 정확성(검수 항목 1). 코드 `synthesizer.py:398-420`.
   - 권장 수정: Open ③ 과 결과 파싱 표 C 행을 «lint 는 통과하고 오염 본문이 발행될 수 있다» 로 고친다. Phase 3 C 수용 조건에 «`markdown_body` 가 `# 📋 메디솔브 브리핑` 으로 시작하고 펜스·머리말이 없다» 를 넣는다.

2. **`spec-070-briefing.md:414` (§5 Acceptance Criteria) — 개정 본문과 모순되는 잔존 문구.** `- [ ] LLM submit 1회 (`max_turns=25`, mediness MCP 4 read-only tool 노출)` 가 그대로 남았다. 같은 SPEC 의 개정된 `:363` 은 «codex 에는 turn 제한 키가 없다, max_turns=25 는 claude 경로에만» 이라고 쓴다.
   - 근거: SPEC 정합(검수 항목 7). 같은 문서 안의 모순.
   - 권장 수정: `:414` 를 «LLM submit 1회 (codex · 시간 상한 600s · mediness MCP 4 read-only tool 노출)» 로 고친다.

3. **WP-133 Phase 2 (`:131-138`) — 깨질 기존 테스트를 짚지 않았다.** provider 기본값이 `codex` 로 바뀌면, claude 인자를 기본 설정에서 단정하는 기존 테스트가 실패한다.
   - `back/tests/services/test_brief_synthesizer.py:541-549` (`provider == "claude"`, `max_turns == 25`, `mcp_config`, 접두 `allowed_tools`)
   - `back/tests/services/test_decision_gate_ai.py:300-311`·`:318-370` (`allowed_tools`/`disallowed_tools`/`mcp_config`/`max_turns` in provider_options — B′ partial 검증 포함)
   - `back/tests/services/test_decision_gate_redesign.py:120` (`meeting_llm_batch == "claude-sonnet-4-6"` — 값은 안 바뀌어 통과하겠지만 의미가 낡는다)

   WP 는 «만들거나 고친 테스트 파일만 1회» 라고만 써서, 코드 워커가 회귀를 발견하고 나서야 판단하게 된다.
   - 근거: 구현 가능성(검수 항목 4).
   - 권장 수정: Phase 2 작업에 «위 기존 테스트는 claude 설정을 명시(settings override)해 claude 분기 회귀 테스트로 보존하고, codex 단정은 신규로 둔다» 한 줄과 파일 목록을 넣는다.

4. **WP-133 Phase 3 (`:147-149`) — 수용 실행 수단이 막연하다.** 무엇을 확인할지는 명확하다. 그러나 «수동 1회 실행»(C), «실제 버전 1행으로 콜 1회»(D), «back 파드에서 `_default_ai_call` 을 실제 게이트 프롬프트로 1회 호출»(B)의 **구체 명령·스크립트가 없다.** B 는 user prompt 를 `recommend_with_ai` 가 조립하므로, `_default_ai_call` 을 직접 부르면 운영과 같은 프롬프트가 아니다.
   - 레포에 이미 있는 후보: `back/scripts/eval_decision_gate.py`(B), `back/scripts/brief_backfill.py`(C).
   - 근거: 수용 기준(검수 항목 6) «운영 같은 조건에서 검증 가능하게».
   - 권장 수정: B 는 «`recommend_with_ai` 경유(eval 스크립트 1건 또는 Slack 멘션 1회)», C 는 «다음 06:00 정기 run 우선, 수동은 기존 스크립트명 명시», D 는 «`weekly_report_pipeline._default_ai_call` 을 W47 실데이터 1버전 프롬프트로 파드 내 1회 호출 — admin 재생성은 W47 draft archive 위험» 처럼 수단을 못박는다.

5. **WP-133 Open ② (`:172`) — C 의 argv 한계 위험을 실측 전에 볼 수단이 없다.** 현 코드는 **본문(serialized)만** 바이트를 로그하고 100KB 에서 경고한다(`synthesizer.py:533-539`). codex 로 실제로 나가는 것은 system + 템플릿 + 본문을 합친 프롬프트이고, 단일 argv 한계(회의록 v2 는 147KB 에서 `E2BIG`)는 그보다 낮을 수 있다. 첫 prod run 이 E2BIG 로 FAILED 가 될 수 있는데, 합본 크기 로그가 없으면 사후 판별이 어렵다.
   - 근거: 구현 가능성 / 수용 기준.
   - 권장 수정: Phase 1 작업에 «compose 후 최종 프롬프트 바이트를 로그»(B·C·D 공통, 한 줄)를 넣는다. 그러면 Open ② 를 첫 실호출 로그로 닫을 수 있다.

6. **`spec-070-briefing.md:366` — 문장이 끊기지 않았다.** «…합본 크기가 실패 축이다 초과 cap 분은 …» 에 마침표나 구분자가 없어 두 문장이 붙었다.
   - 근거: 문서 품질. 사소함.
   - 권장 수정: «실패 축이다.» 뒤에 끊는다.

참고(판정 무관):
- SPEC-070 의 `ClaudeClient → AgentClient`, `open_kknaks_queue → brief_queue` 치환은 같은 bullet 안의 사실 정정이고 코드와 일치한다(`synthesizer.py:547`·`:555`). «관련 없는 절 수정» 으로 보지 않았다.
- SPEC-130·SPEC-070 은 개정 노트를 상단 블록이 아니라 본문 bullet 에 날짜와 근거로 인라인했다. SPEC-130 의 기존 관례는 상단 `> 변경 노트` 블록이지만, 날짜·근거·불변 범위가 모두 적혀 있어 WARN 으로 올리지 않았다.

## Open Issues 5건 판정표

| # | 내용 | 구현을 막나? | 판정 |
|---|---|---|---|
| ① 설정 키 배치 | provider/모델/MCP 키 이름(공용·경로별·회의 키 재사용) | **안 막음** | 값(codex · 빈 값 → landing 모델 · MCP url 동일)은 정해져 있고 키 이름만 남았다. 개발 내부 결정이라 WP Open 이 맞는 자리다. 권장 ⓐ 로 진행 가능. |
| ② C 프롬프트 vs argv 한계 | 합본이 E2BIG 에 근접할 수 있음 | **안 막음 — 실측으로 닫음** | 단 WARN-5 대로 합본 바이트 로그를 Phase 1 에 넣어야 첫 run 에서 닫힌다. 한계를 넘으면 cap 조정은 SPEC-070 개정 사안이고, 이 경우 C 수용이 지연될 수 있다(위험 실재). |
| ③ C 출력 펜스/머리말 | codex 출력 형식 | **안 막음 — 실측으로 닫음** | 단 위험 서술이 틀렸다(WARN-1): lint FAILED 가 아니라 조용한 오염 발행이다. 수용 조건에 본문 형태 확인을 넣어야 실측이 이 위험을 잡는다. |
| ④ B 계측 `collect_stream_stats` | codex 스트림에서 0/누락 | **안 막음** | 코드상 실패하면 `{}` 를 돌려주고(`decision_gate_stream.py:133-137`) 추천에는 영향이 없다. 후속으로 두는 것이 타당하다. |
| ⑤ SPEC-111 실측 수치 재측정 | codex 에서 속도·품질 변화 | **안 막음** | 핫픽스 범위 밖이라는 판단이 타당하다. OQ-17 이 이미 열려 있다. |

## 사용자에게 물어야 할 것
- 없음. D1~D4 는 지켜졌고 되묻는 서술도 없다. WP Pre-deploy 의 «W47 draft 편집 여부 확인 후 재생성 여부를 사용자에게 확인» 은 운영 데이터 보호 절차이지 결정을 되묻는 것이 아니다. WARN-4 대로 D 수용을 파드 내 직접 호출로 정하면 이 질문 자체가 필요 없어진다.

## 기존 부채 (이번 판정 제외)
- `back/scripts/brief_synthesize_smoke.py:313`·`back/scripts/warmup_local_check.py:77` 의 `provider="claude"` — 수동 스모크 스크립트라 서버 경로가 아니다. WP 범위 밖으로 둔 것이 맞다(survey §6-7).
- lint 기존 WARN 263건(타 제품 포함) — 무관.

## 확인한 것 (PASS 근거)
1. **사실 정확성 — 일치.** WP 인용 파일:줄을 전부 대조했다.
   - B: `decision_gate.py:651-736` (submit `:697-718`, `provider="claude"` 기본 `:655`, `model=settings.meeting_llm_batch` `:701`, provider_options `system_prompt`·`max_turns`·`effort:"low"`·`mcp_config`·`allowed_tools`·`disallowed_tools`, options `timeout_sec`)
   - `_extract_json :439-455`, stream `:729`
   - B′: `pipeline_ingest_consumer.py:159-169`(partial `pipeline_gate_max_turns=25`), `:184 loads_json_robust`
   - C: `synthesizer.py:553-572` (`provider="claude"`, `max_turns 25`, `effort medium`, 접두 4종, `timeout 600`), `:600-612`
   - D: `weekly_report_pipeline.py:498-525` (submit `:512-519`, `max_turns 1`, `effort low`, `timeout 300`), `parse_4week_summary :124-146`
   - config: `meeting_llm_batch="claude-sonnet-4-6" :183`, `meeting_llm_provider="codex" :264`, `meeting_codex_model="" :267`, mcp key/url `:269-270`, resolved `:294-296`, `landing_chat_model="gpt-5.6-terra" :125`
   - 상태 판정 `"done"` 은 open_kknaks 의 원 status 값이다(`meeting_extractor_client.py:340-344` 가 done → ok 로 정규화하는 것으로 확인). codex 에서도 불변.
2. **선례 일치 — 일치, 발명 없음.** 대응표의 모양(`sandbox="read-only"`, `skip_git_repo_check=True`, `config` `-c` 리스트, `model_reasoning_effort`, `approval_policy="never"`, `mcp_servers.<key>.url/http_headers{X-Internal-Auth}/enabled_tools`, 툴별 `approval_mode="approve"`, 표면 축소 4줄, model `or None`, `compose_prompt` 구분선, `redact_config_overrides`)이 `meeting_v2_submission.py:72-175` 와 글자 단위로 같다.
   - MCP 인증은 X-Internal-Auth 이고, 현 claude 경로의 worker `/tmp/mcp-config.json` 도 같은 헤더다(`worker-entrypoint.sh:14-24`). 권한 동일 주장이 사실이다.
   - effort `low`·`medium` 은 landing 실측 허용값 목록에 있다(`landing_chat/submission.py:24-26`).
   - provider 를 설정값으로 두고 claude 분기를 보존하는 것은 `meeting_v2_extractor.py:449-471`·`:511-535` 와 같은 방식이다.
3. **전수성 — 누락 없음.** back/app 의 grep 결과에서 B·C·D 에 닿는 claude 의존은 decision_gate `:655`·`:701`, synthesizer `:556-557`, weekly `:515-516`, 그리고 각 provider_options 뿐이고 전부 WP 대응표에 있다. `_default_ai_call` 호출처는 `recommend_with_ai :801`(provider 미지정)·B′ partial·weekly scheduler 뿐이다. 파싱(B/B′/C/D)과 계측(B stream)도 결과 파싱 표에 있다. 남는 것은 테스트(WARN-3)뿐이다.
4. **구현 가능성** — 조립·분기·설정 지시가 서로 충돌하지 않는다. Open 5건은 모두 비차단이다. 보강 필요 사항은 WARN-3·4·5.
5. **결정 준수(D1~D4) — 준수.** 범위는 B·B′·C·D 이고, A·`DEPLOY.md §4-4`·`agent/` 는 「제외 — 후속」(`:45-50`, `:180`)이다. 구현 대상은 mediness-app `main` 핫픽스 → main→dev(`:18`)로 명시됐다. 결정을 되묻는 서술은 없다.
6. **수용 기준** — B·C·D 각 1회, prod 워커, `status=done` + 파서/lint 통과 + worker `exit_code=0` 이 명시됐고 «단위 테스트만으로 done 아님» 도 적혀 있다. 실행 수단의 구체성은 WARN-4.
7. **SPEC 정합** — SPEC-111 상단 2026-11-13 개정 노트(날짜·근거·바뀌는 3행·불변 범위)와 §3.2 표 3행이 WP 와 일치한다. SPEC-070·130 인라인 개정은 날짜·근거·WP 링크를 갖췄다. SPEC-116 은 현황 주석 1줄뿐이다. 모순은 SPEC-070:414 1건(WARN-2).
8. **문서 규칙** — 확인한 항목:
   - WP frontmatter(id·doc_no 255 유일·type·status proposed·owner TBD·last_updated·covers 3·depends_on [])
   - 파일명 NNN 일치
   - 30-work.md 반영: Status Board(11열, proposed/TBD/0.5~1d/2026-11-14), WP List(proposed/TBD/covers 일치), Spec Coverage 3행
   - SPEC-070 구현 상태 done → in_dev: WP-063 done + WP-133 proposed 의 derive 규칙상 맞다
   - log.md 행(spec-change, wp-add / 영향 ID 5개 / PR `—` 은 머지 후 backfill 관례)
   - Harness v1 예외 사유 명시(`:26`)
   - SPEC frontmatter `version` 은 올리지 않았다(규칙 준수). 3자 status 일치는 lint 0 error 로 확인했다.
