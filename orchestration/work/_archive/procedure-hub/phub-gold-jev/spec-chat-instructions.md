# SPEC-004 0.1 — 상담 채팅 1판(CLI 기억 · htmx 화면 · 얼굴 점 · 시술 리스트)

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · 제약(외부 API 호출 · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-004-consult-chat.md` 새 파일 1개만.** 11-17 사용자 결정: Procedure Hub 데이터(원장 · silver · gold)는 공개 정보 — 「회사 데이터 본문 0」 은 이 데이터에 걸지 않는다(비밀값 · 키 · 내부 URL 금지 그대로).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · 공개 레포 · 구현은 여기에 이어서) · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만) · `SM=$W/../_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

1. `$W/_RESUME.md` §2 — 11-17 행 전부(특히 맨 위 「CLI 실행기 = 앱이 직접」 · 「채팅 조사 뒤 사용자 결정」 · 「이번 세션 목표 = 상담 채팅」) ← 정본
2. `$W/research-chat.md` 전체 ← 조사 근거(여기 없는 사실을 지어내지 마라 · 「확인 안 됨」 은 그대로 열린 것으로)
3. `$W/SPEC-001-hub-gold-mcp.md`(도구 9 계약 · `concern_candidates`) · `$W/SPEC-002-chat-eval.md` §3-2a · §3-7
4. 앱: `$A/clinic_chat/{runner.py,walk/,clients/,llm/,web/,runs.py,progress.py,prompts.py}` · `$A/prompts/` · `$A/README.md` · `$A/pyproject.toml`
5. CLI 옵션 정리: `/Users/kknaks/git/library/claude_code_pty/open_kknaks/docs/legacy/CLAUDE_CODE_ANALYSIS.md` §2 · §4 · `…/open_kknaks/worker/executor.py:150-190`(꼴 참고만 — 쓰지 않는다)
6. 얼굴 밑그림(참고용 · 레포에 안 둠): `/Users/kknaks/Downloads/미니멀 인체 해부학 삼면도.png` 왼쪽 패널 · silver `$SM/silver/{site,concern_site,procedure_case,concern}.csv`

## 정해진 것(다시 묻지 마라)

- 화면 = 서버사이드 렌더링 + **htmx** · 왼쪽 위 얼굴 SVG + 부위 점 · 왼쪽 아래 시술 리스트 · 오른쪽 채팅창 · 새 화면(18220 시험 화면은 그대로) · 포트 18222 · Jinja2 의존 추가 · htmx 는 로컬 파일 고정.
- LLM = **CLI 먼저**(SDK 모듈은 배포 전 — 이 판 범위 밖, 갈아 끼울 자리만) · **앱이 CLI 를 직접 띄운다**(open_kknaks 안 씀) · Sonnet. 옵션은 `_RESUME` §2 「CLI 실행기」 행 그대로(`--session-id` 첫 턴 → `--resume` · `--no-session-persistence` 뺌 · `--system-prompt-file` · `--fallback-model haiku` · `--effort low` · `--max-turns 1` · 도구 막음 · stream-json).
- 대화 장부 = 앱 메모리 + 파일 한 줄씩(`runs.jsonl` 꼴) — 턴 · session_id · 고른 대상 · 읽은 재료 id · 답 · 시간.
- 재료 = B 흐름(gold + Jev 가 맨 앞에서 판단 · 허브 폭 · LLM 에는 필요한 칸만) · 턴마다 새로 읽은 것만 그 턴 메시지에(덧붙이기).
- **시술 리스트는 앱이 허브 행으로 결정론적으로 짓는다**(LLM 답 문장 아님 · 계열 묶음 · 층 표시) · 채팅 답은 짧게 · 리스트를 다시 읊지 않음.
- 얼굴 = **손 SVG(새로 그림 · 벡터)** · 좌표는 코드(표)에 · 부위 코드(SITE-xxx)마다 0~1 비율 좌표 · 좌우 짝은 점 둘 · 얼굴 밖 · 넓은 부위(얼굴 전체 · 전신 · 등 · 허벅지 …)는 **얼굴 아래 라벨**. 점 기준 = **고민 부위**(`concern_site`). 원본 PNG 는 레포에 안 둠.
- 근거 꼬리(답 줄 ↔ 재료 줄) 유지 · **화면에서만 숨김**.
- 화면 문구는 짓지 않는다(빈 자리 표시 · 사용자 몫).
- **상담 플로우(짧게 → 깊게의 단계 · 시술을 눌렀을 때 · 상세 턴 목록 자리)는 사용자가 따로 준다** — 이번 판은 「한 턴 = 고민 → 리스트 + 점 + 짧은 답」 과 「이어 묻기(장부 맥락)」 의 뼈대까지. 플로우 자리는 0.2 로 열어 둔다(U-5 · U-10 그대로 열린 것).
- 허브가 고민 → 부위를 응답에 안 내는 것은 **SPEC-001 0.7(별도 문서)** 이 닫는다 — 여기서는 「`concern_candidates` 응답 머리에 고민 부위 코드 목록」 을 쓴다고 가정하고 그 계약 필요만 적는다.

## 할 것

1. 구조: 모듈 자리(새 패키지/모듈) · 시험 앱과 함께 쓰는 것(walk · clients · progress) / 새로 짓는 것.
2. CLI 기억: 명령 꼴 전부 · session_id 수명 · 실패 · 시간 초과 · 프로세스 동시 한도 · 임시 cwd 처리(세션 파일 위치가 cwd 에 매이는지 — 조사 근거로) · SDK 로 갈아 끼울 경계(인터페이스).
3. 한 턴 흐름: 입력 → Jev → 허브 → 리스트 · 부위 → LLM → 화면 조각 셋(htmx `hx-swap-oob` · SSE 스트리밍) — 단계별 이벤트 · 무엇을 먼저 그리나(리스트 · 점은 LLM 전에).
4. 이어 묻기: 장부의 앞 턴 대상을 Jev 후보에 넣는 법 · 재료 덧붙이기.
5. 상담 프롬프트 기반: 시험 프롬프트에서 남길 것 / 뺄 것(조사 §2) · 파일 자리 · 문구 확정은 사용자(C-1 그대로 초안).
6. 얼굴 SVG · 좌표표: 파일 자리 · 표 꼴 · 부위 60 의 분류(점 · 짝 · 영역 · 선 · 안 보임 → 라벨) · 누가 찍고 누가 확인(초안 워커 · 사용자 눈).
7. 시험 · 실물 확인: 단위 시험 · CLI 3턴 실측(기억 이어짐 · 첫 글자 · 캐시 기록) · 화면 e2e 꼴(코디가 18222 띄움 · 사용자 확인).
8. version 0.1.0 · 열린 것(상담 플로우 · U-5 · U-10 · SDK · `--bare`) · **WORK 전 사용자 결정**(최소 · 추천 붙임 · 위 「정해진 것」 은 올리지 마라).

## 검증

- 결정 행 → 문서:줄 표 · 조사 근거 인용 경로 실재 · 공개 grep(비밀값 · 키 0).
