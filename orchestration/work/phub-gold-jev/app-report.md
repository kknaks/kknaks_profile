# app 완료 보고 — WORK-002 WP-1 ~ WP-8 (clinic_chat · kknaksss/phub-gold-jev · 커밋 없음)

## 변경 파일
- 새로: `pyproject.toml` · `uv.lock` · `.python-version` · `clinic_chat/**`(41 py) · `prompts/**`(md 10) · `tests/**`(19)
- 덧붙임: `.env.example`(이름만 · 값 없음) · `README.md`(「실행 안내(e2e)」 절)
- 안 고침: `.gitignore`
- 로컬 · gitignore: `.env`(경로 env 몇 개 덧붙임 — RAW_DIR · QUESTIONS_CSV · GOLD_CSV_DIR · LEDGER_CHECK_PATH · HUB_WORKTREE · TYPESAFE_DEFAULT_MODEL. 키 값은 읽지도 출력하지도 않음) · `data/eval-set/**` · `runs/**`

## 실물 확인 E1 ~ E6
| # | 결과 | 값 |
|---|---|---|
| E1 Jev | 통과 | model `jev-1.14.0` · choice 1 + noul 2 한 요청 · probabilities 키 3 · 242 ms |
| E2 Sonnet | 통과(추론 끔은 **불가**로 결론) | `claude-sonnet-5-5` · 구독 · 2,684 ms. `claude --help` 에 추론 끔 플래그 없음(`--effort low…max` 뿐). `--settings {"alwaysThinkingEnabled":false}` + `MAX_THINKING_TOKENS=0` 은 받아들여지고 빈 프롬프트에선 thinking 없음 — **그러나 E5 의 실제 B 단계 ⑤ 입력에서 thinking 블록이 나옴** → `ANSWER_REASONING` 기본 = `lowest_effort`(`--effort low`) · `.env.example` 설명 반영. 쪽마다 `llm_pages[].thinking_seen` 으로 기록 |
| E3 Haiku | 통과 | `claude-haiku-5-5` · 같은 격리 인자 · effort 받음 · 3,029 ms |
| E4 허브 | 통과(재시작 뒤 재확인) | gold_hash `8accbb21…` · 목록 꼴 resolve total 1231 · 25 쪽 · read 1231 complete · MCP 도구 8 · 모의 ↔ 실물 꼴 차이 없음 · MCP 오류 글자 = REST 글자 |
| E5 세 열 Q22 | 통과 | A 18,439 ms(LLM 5 · 도구 16) · B 8,697 ms(근거 충족 · 허브 4 · Jev 3 · LLM 1) · B 켬 8,601 ms · C 10,667 ms(LLM 3 · 도구 4) · runs.jsonl 한 줄 §7-1 · §7-2 · §7-3 필드 빠짐 0 · C `--allowedTools` 도구 이름 7 단위 받아들여짐(WORK A-7 해소) |
| E6 합성 키 배관 | 통과 | `claude-opus-5-5` · 9,154 ms · 구조화 출력 항목 5 · 실패 근거 칸 · 「합성 키 — 배관 확인 · 채점 수치 아님」 · 결과 `runs/plumbing/` 만 |
| WP-2 실물 | 통과 | RAW_DIR JSON 21 · manifest `03e71322cdc9a3e9` |
| e2e 한 질문 · 한 열 | 돈다 | `runner --question … --columns b` → 근거 충족 11,297 ms · `runs --show --trace` · `batch --check` 전부 됨 |

## WP-6 실물(답 키)
- 37 명세(ast 리터럴만 · gold-build 실행 없음 · gold 해시 앞뒤 같음) · 37 키 · `sample_check` 36/37 · 걸린 문항 17(`data/eval-set/key-summary.md`)
- Q33 = (나) ✓ · Q12 = (다) ✓ · **Q10 = 「상태 안 맞음」(기대 (가))** — `facets package` 가 hier 기본 expand 로 상위 고민 패키지 18 행을 내 「행 0」 이 안 선다(SPEC-002 §5 (가) ↔ SPEC-001 §4-4 계층 펼침 사이 구멍 · 문항별 예외로 메우지 않음)
- **Q25 표본 3/6 안 듦** — 순서·간격 범위 고정 갈래(순서 · 간격 · 재시술 간격)에 「회피」 가 없어 gold-build 길보다 좁음(SPEC §3-2 표 구멍 후보)
- 「입구 이름 맞춤 확인」 10 문항: 「보톡스」 등이 시작 표 안에서 개념 3(계열 · 시술 · 제품)으로 겹침 — 명세는 resolve 순서 첫 개념을 골랐다 → 사용자 확인 때 볼 것
- 추가 32 문항: 질문 문장 **초안 draft** 로 세트 파일에(69 줄 검증 통과) — **사용자 확정 전**. 이름 없음 · 오타 묶음 resolve 후보 수: N01 = 2 · N05 = 1(0 아님 → 그 묶음 꼴이 아님 — 문장 고칠 것) · 나머지 0. 32 문항의 호출 명세 · 키는 확정 뒤에 뽑는다

## 검증
`uv sync` OK · `uv run ruff check .` All checks passed · `uv run pytest -q` **85 passed**(모의만 — 키 · 허브 · 구독 없이). `rg unconfirmed clinic_chat` = 거부 문구 · 셈 칸 2 줄뿐(푸는 길 없음). key_calls 에 exec · runpy · subprocess · import 없음.
git status: 커밋 후보 = `.env.example` · `README.md` · `.python-version` · `pyproject.toml` · `uv.lock` · `clinic_chat/` · `prompts/` · `tests/` / ignored = `.env` · `data/` · `runs/` · `.venv` · 캐시. 커밋 후보 grep: 홈 경로 · 키 꼴 0 · 실제 코드 · gid · LCK 꼴 0(예시 `GXX-00001` 만) · 시술 이름 0.

## 계약 · 결정 준수 / 구현에서 정한 것(보고)
- SPEC · WORK 안 고침. 커밋 · push · PR 없음. 허브 띄우기 · 내리기 없음. batch 전체 안 돌림.
- **패키지 이름 `clinic_chat/raw/` → `clinic_chat/raw_ledger/`** — `.gitignore` 의 `raw/` 규칙이 패키지를 통째로 무시해서(WORK §2-3 이름과 다름 · .gitignore 는 안 고침)
- resolve 맞춤 꼴에서 **더 긴 조각 안에 드는 짧은 조각의 후보는 뺐다**(예: 「이마 주름」 이 맞으면 「주름」 은 안 씀) — SPEC 에 없는 꼴 · 키 명세는 「조각 전체 맞춤」 이라 같은 방향
- required 는 facet 단위 초안 — 그 범위에서 그 표를 내는 조회를 안 불렀으면 「해당 없음」(예: 회피 범위의 조건 쪽 시작은 pair 미요구)
- BR1 의 `site` 필터: `concern_candidates.site` · `facets filters.site_name`(그 칸이 있는 facet 만) — 입구가 둘 이상일 때만
- 답 프롬프트 · 채점 프롬프트 · Jev instructions 10 파일 = **초안** — SPEC-002 O-9 의 확인 지점을 구현 뒤(e2e 보고)로 옮긴 것(C-1). 결과에 「프롬프트 미확정(사용자 확인 전)」 이 찍힌다
- WORK 완료 조건 「채점 입력 문자열에 gid 꼴이 없다」 는 답 부분만 가렸다 — 전체 답 키 행(실패 근거에 쓸 gid)은 채점 입력에 있다(SPEC §8-3 「실패마다 gid」 와 부딪쳐 그렇게 읽음)

## 미결 · 주의
1. 사용자: 답 키 37 확인(걸린 17) · 추가 32 문항 확정(N01 · N05 문장 고침) · 프롬프트 10 파일 확인 → `answer_key --confirm` · `prompts --confirm`
2. 코디 판단: Q10 (가) 구멍 · Q25 순서·간격 갈래 · 「추론 끔 불가 → lowest_effort」(SPEC O-23 (b))
3. 실제 채점 · 보고서는 키 확인 뒤(미확인 키 거부 확인됨)
