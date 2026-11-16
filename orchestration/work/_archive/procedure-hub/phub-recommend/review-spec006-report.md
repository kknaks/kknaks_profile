# 검수 — SPEC-006 · WORK-004 (hub-evals 실험 앱)

**FAIL** · FAIL 1 · WARN 7 · **open = 13**(SPEC-006 §7-3 추천 기본값 R-1 ~ R-10 승인 대기 10 + §7-4 사용자 몫 U-1 · U-2 · U-4 3 — 모의 판 구현은 막지 않음)

- 기준: `reference/2026-10-30-hub-evals/README.md` · `jev-research.md` · `_RESUME.md` §2 10-30(원장도 MCP · hub-evals 결정 Q-1 ~ Q-8 · Claude API 키 별도 · 최종 목표 · 레포 공개 · 데이터 · 키 env · 환자 정보 금지) · `DEC-001.md` D-08 · D-11 · `SPEC-005.md` §5 · §5-12
- 대상: `SPEC-006.md`(13:58) · `WORK-004.md`(13:58)
- 허브 실물은 아직 구현 중이라 도구 계약은 SPEC-005 문서와 대조했다. 원장 파일은 `phub-stg-2026-10-26/` 실물을 읽어 확인했다. GitHub `kknaks/clinic_chat` 는 `gh repo view` 로 PUBLIC · 빈 레포임을 확인했다
- 골격은 결정과 맞는다: 세 케이스 같은 Sonnet 설정 · 같은 t0 · case1 원장 MCP · case2 골드 MCP · case3 허브 사전 → Jev → 골드 경로 → Sonnet 1회 · SDK 직접 루프 · 키 env · 공개 레포 규칙 · R 추천 기본값 분리. **FAIL 1 은 ① 정규화 규칙 한 줄이다**

---

## FAIL

### F-1 · ① 단어 검사 정규화가 인용한 정본과 다르고, 실물 원장에서 거짓 「없는 이름」을 낸다 — SPEC-006 §5-1 정규화 행 · WORK-004 Phase 5

- SPEC-006 §5-1: 「공백 제거 · **영문으로 시작하면 소문자** · 라틴 악센트 제거」(README §4 ① 2 · `semantic.md` §4 인용)
- 인용한 정본 `semantic.md` §4(지금): 「NFKC → 라틴 악센트 접기 → fold(쳐짐 → 처짐) → 공백 제거 → 괄호 지움 → **전부 소문자**」(`semantic-build.py:55-63` `norm`). `semantic.json dictionary.resolve_rules.note` 는 「영문으로 시작하면 소문자」를 3단계 lexicon 설명으로 따로 두고 「사전은 이 규칙 하나(품질 M)」라고 적는다. README 의 그 문구는 옛 3단계 규칙이다. README 자신도 「시맨틱 사전 정규화와 **같은 규칙**」이라고 했으니, 따라야 할 것은 §4 다
- 실물 영향: 원장 21 파일에서 **한글로 시작하고 영문 대문자가 섞인 문자열이 290개**다(예: 「듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG)」 · 「필러(HA/CaHA)」). 답에서 뽑은 「Nd:YAG」 는 영문으로 시작하므로 「nd:yag」 가 된다. 원장 문자열은 한글로 시작하므로 소문자로 바뀌지 않는다. 그래서 부분 일치가 안 되고 「없는 이름」으로 셈된다. ① 은 「지어낸 이름」 셈인데 영문 표기를 쓰는 답일수록 거짓 경보가 늘어, 세 케이스에 같은 잣대라는 전제(README §4 ①)가 흔들린다
- 고칠 것: §5-1 정규화를 `semantic.json dictionary.resolve_rules.normalize` 그대로로 바꾼다(문서 = 코드 · 답 · 원장 · 사전 셋 다 같은 함수). WORK-004 Phase 5 의 「정규화 표」 시험에 「한글로 시작 + 영문 대문자」 원장 문자열 하나를 넣는다

---

## WARN

| id | 곳 | 무엇 | 근거 | 고칠 것 |
|---|---|---|---|---|
| W-1 | SPEC-006 §2-4 ↔ WORK-004 Phase 1 시험 | §2-4 는 `.env.example` 에 예시 값을 적는다(`jev-1.14.0` · 모델 id · 허브 URL · `./runs` · `18210` · `12` · `0.3`). Phase 1 시험은 「`.env.example` 값 빈칸」이다. 둘 중 하나는 지켜질 수 없다 | 두 문서 문구 | 시험을 「키(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 값 빈칸 · 사용자 홈 경로 없음」으로 좁힌다 |
| W-2 | SPEC-006 §3-4 ③ 경로표 | SPEC-005 §6-1 의 의도 → 도구 대응이 빠졌다. 확인 조건 노드가 안 잡히는 I-09(「통증 민감」 꼴)은 T3 `sections=overview,ops` 로 가야 하고, I-07 자기 쌍은 같은 id 를 두 번 넣는다. case3 의 「의도별 고정 경로」가 허브 측 정본보다 좁다 | SPEC-005 §6-1 · §5-5 | ③ 에 두 줄을 더하거나 「경로 = SPEC-005 §6-1 의 의도 → 도구 그대로」로 참조한다 |
| W-3 | SPEC-006 §5-1 · §5-2 | ① 은 「채점 경로가 실험 대상 서버에 기대지 않게」 원장 로컬 파일을 직접 읽는다. 그런데 ② Opus 기준 자료는 허브 원장 MCP 로 준다(R-10). 같은 이유가 ② 에는 적용되지 않았다. 인용 확인을 로컬 파일로 하므로 판정은 지켜지지만, 기준이 둘이다 | 두 절 문구 | ② 의 원장 도구를 앱 안 로컬 구현(같은 R1 ~ R3 계약)으로 할지, 허브 MCP 로 둘지 R-10 에 적는다 |
| W-4 | SPEC-006 §8 · WORK-004 Phase 1 | `cp .env.example .env` 뒤 `uv run python -m clinic_chat.server` — `uv run` 은 `.env` 를 저절로 읽지 않는다. `config.py` 가 `.env` 를 읽는지(dotenv · pydantic-settings), 아니면 `--env-file .env` 를 쓰는지 정해 두지 않았다. 허브 쪽 절차는 `--env-file` 을 쓴다 | §8 · Phase 1 | 하나로 정해 §8 명령과 Phase 1 완료 조건에 적는다 |
| W-5 | WORK-004 Done Criteria | 실물 E2E 가 「(조건 될 때)」다. 모의 판만으로 Done 이 되면 외부 서비스(Anthropic · TypeSafe · 허브 MCP) 경로가 실물 호출 없이 끝난다 | WORK-004 Done · Phase 7-3 | status 를 둘로 나눈다(「모의 완료」 / 실물 E2E 1질문 뒤 「완료」) |
| W-6 | SPEC-006 §3-4 ② 슬롯 | D-08 이 적은 Jev 슬롯은 「고민 · 부위 · 중증도 · 조건」이다. SPEC-006 슬롯(vocab 종류 + 시술 · 제품)에 **중증도**가 없고, 없는 이유도 적혀 있지 않다(SPEC-005 T9 vocab 에도 중증도 없음) | DEC-001 D-08 · SPEC-005 §5-10 | 「중증도는 허브 vocab 에 없어 이 실험 슬롯 밖」 한 줄을 적거나, 고민 하위(중증도 → 하위 고민 · 7단계 보정 ③)로 덮인다는 근거를 적는다 |
| W-7 | SPEC-006 §3-4 ① | README · jev-research 흐름은 「허브 노드 목록(캐시) → Jev」이다. SPEC 은 질문마다 T1 resolve(`hub_resolve`)를 먼저 부른다. Q-4(255 넘는 슬롯만 사전 후보) 를 위해 필요한 단계지만, 255 이하 슬롯만 쓰는 질문에도 단계가 하나 더 생겨 case3 속도에 들어간다 | 10-30 Q-4 · Q-7 · jev-research §3 | 「T1 은 늘 부른다(시술 슬롯 판단에 필요)」를 근거와 함께 적고, `stages[]` 에 따로 남는다는 점(이미 있음)으로 비교를 분리한다 |

---

## 항목별 대조

### ① 세 케이스 같은 조건

| 항목 | case1 | case2 | case3 | 판정 |
|---|---|---|---|---|
| 답 모델 | claude-sonnet-5-5 | 같음 | 같음 | 같음(README §1) |
| thinking | `between_tools` | 같음 | 같음 | 같음(Q-3 · jev-research §4 「disabled 400」) |
| effort | high | 같음 | 같음 | 같음(R-3) |
| 공통 프롬프트 | `common.md` + 케이스 부분 | 같음 | 같음 | R-5 · 판 sha 기록 |
| 시작 | 같은 t0 · gather | 같음 | 같음 | 같음 |
| 측정 지점 | 첫 text_delta · 단계 · 왕복 · 토큰 | 같음 | 같음 | 같음 · `ttft_answer_ms` 더함 |
| 데이터 | 원장 MCP 3(§5-12) | 골드 MCP 9 | T1 → Jev → 골드 경로 → Sonnet 1 | Q-1 · 10-30 「원장도 MCP」 · README §2 그대로 |
| 폴백 · 루프 상한 | 없음 · 12 | 같음 | 해당 없음 | 같음 |

### ② SPEC-005 도구 계약

- 원장 도구 `raw_list` · `raw_get` · `raw_search` · 마운트 `/procedure-hub/raw-mcp/mcp` · 응답 머리 `raw.dir_manifest_sha16` · 헬스 manifest 21/21 — SPEC-005 §5-12 와 같다
- 골드 MCP `/procedure-hub/gold-mcp/mcp` · REST `/procedure-hub/gold` · T1 출력 `candidates` · `menu_candidates` · `unmatched` · T2 `concerns` · `site` · `cc` · T7 `menu` / `concern` · T9 kinds(intent · menu 포함) · 응답 머리 `build.build_hash` · `claude_contract`(SPEC-005 §5-0 · O-3 결정) — 같다
- 의도 12 · I-12 허브 도구 없음 — 같다. 경로표의 빠진 두 줄은 W-2

### ③ Jev · Claude 연결

- Jev: `typesafe-sdk` `AsyncTypeSafeClient` · `jev-1.14.0` 고정(Q-6) · Choice 255 한도 · 넘는 슬롯(단위 시술 162 + 제품 354 + 계열 27 = 543)만 T1 후보로 줄임(Q-4) · confidence · p_max · 1·2위 비 · 0.3 문턱(Q-5) · Noul 은 confidence 없음 · 한국어만(Q-8) · 「해당 없음」 + 짝 Noul · 순서 seed · 401 · 422 · 429/529 · 시간 초과 — jev-research §1 · §2 와 같다. 나머지 슬롯(고민 57 · 부위 53 · 확인 조건 53 · 목적 13 · 의도 12 · 메뉴 8)은 255 아래
- Claude: Anthropic Python SDK + MCP `ClientSession` 직접 루프 · Messages API MCP connector 안 씀(로컬 불가 · 공개 노출 안 함) · Agent SDK 안 씀 — Q-2 · jev-research §4 와 같다

### ④ 속도 · 기록 · 품질 공정성

- 속도 칸 · `stages[]` 이름 · 토큰 · `runs.jsonl` 한 줄 · `human_checks.jsonl` 분리 · versions(모델 · 프롬프트 판 · 골드 build_hash · 원장 manifest · app_commit) — README §3 · §6 을 덮는다
- ② 가리기(seed 섞기 · A/B/C · 흔적 · 속도 안 보임) · 실패마다 `{file, path, quote}` 를 로컬 원장으로 확인 → `invalid` · 기준 자료 B(R-10) · 사람 확인 — README §4 공정 장치를 전부 덮는다
- ① 정규화 F-1 · 기준 둘 W-3

### ⑤ 공개 레포 안전

- `.gitignore`(`.env` · `runs/` · `*.jsonl` · `.cache/`) · 원장 · 시맨틱 · 실버 · 골드 · 기록 · 캐시 · `.env` 커밋 금지 · 경로는 env · `test_repo_rules.py`(추적 목록 · 키 꼴 문자열 · 원장 파일 이름 21) · fixture 는 「fixture」 표시 문자열 · 스크린샷 레포 밖 · push 는 코디 승인 뒤 · 환자 정보 금지 안내 줄 + Jev 전송 사실 — 10-30 · D-11 · jev-research §5-1 을 덮는다
- `.env.example` 예시 값 충돌 W-1

### ⑥ 결정 · 추천 분리

- 결정됨으로 쓴 것: O-1 · O-7 · O-8(레포) · O-9 · Q-1 ~ Q-8 — 근거가 결정표에 다 있다
- 추천 기본값 R-1 ~ R-10 은 §7-3 에 분리했고 U-3 으로 승인 대기다. 본문에서 그 값을 쓰는 곳마다 「R-n」 표시가 있다
- 「정해진 것」처럼 들어간 새 결정: 없음. 폴백 없음 · 필수 슬롯 없으면 되묻기는 README §1 · D-08 근거가 있다. 포트 18210 · `ttft_answer_ms` 는 구현 세부다

### ⑦ WORK-004 Phase · 모의 · 실행 절차

- Phase 1 ~ 7 마다 완료 조건이 있다 · 관련 시험만 · 전체는 Phase 7 · 키 없으면 모의(모의 허브 MCP · 모의 Anthropic 스트림 · 모의 Jev) · 허브 실물 대조는 WORK-003 뒤 Phase 7
- §8 절차: 허브 명령은 WORK-003 과 같다(`.env.gold` 예시에 `PHUB_RAW_DIR` 있음 확인). 앱 쪽 `.env` 읽기 W-4 · Done 조건 W-5
