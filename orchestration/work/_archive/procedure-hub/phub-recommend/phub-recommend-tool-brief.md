
# [tool_dev] 식약처 MCP 구현 — 공유용 독립 폴더 (SPEC-002 v0.2.0)

너는 **procedure-hub `tool_dev` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디네이터 워크트리에 함께 탄다. `reference/2026-10-27-mfds-mcp/` 밖은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-002-mfds-mcp.md` (v0.2.0) ← **계약. 여기 없는 건 발명하지 마라** — 단 아래 §3 이 SPEC 보다 우선
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-002-003-report.md` ← 검수(특히 W-13 키 누출)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/NOTES.md` ← **실호출 기록 정본**(대소문자 파라미터 · 필드 · 의약품 08)
- 키: 같은 폴더 `.env` 의 `MFDS_API_KEY` — 값을 출력 · 로그 · 파일에 쓰지 마라

## 2. 배경

사용자가 이 MCP 를 **완성해서 코드를 첨부 파일로 공유**한다(`_RESUME.md` §2). 받는 사람이 폴더 하나만으로 설치 · 실행할 수 있어야 한다.

## 3. 계약 — SPEC 보다 우선하는 지시

1. **의약품 API 는 `DrugPrdtPrmsnInfoService08`** 이다(07 은 폐기 · NOTES 마지막 절). 오퍼레이션 `getDrugPrdtPrmsnInq08` · `getDrugPrdtPrmsnDtlInq08` · `getDrugPrdtMcpnDtlInq08`. SPEC 의 「응답 미확인」 칸은 **실호출로 채워서** 구현한다(필드 · 필터 확인 몇 번). 출력에 원어명(ENTP_ENG_NAME · ITEM_ENG_NAME) · 규격(MATERIAL_NAME · PACK_UNIT) · 취소 상태를 싣는다
2. **DUR 은 아직 활용신청 안 됨**(`DURPrdlstInfoService03` 미등록). tool 은 만들되 미등록이면 `key_not_registered` 를 구분해 돌려주고, README 에 「DUR 활용신청 필요」를 적는다
3. **공유용 폴더 요건**: README(한국어 — 무엇 · 공공데이터포털 키 발급과 활용신청할 API 4개 링크 · 설치(`uv sync`) · Claude Code(`claude mcp add`) / Claude Desktop 설정 예 · tool 표와 예시 · 한도 · 캐시 위치 · 문제 해결) · `.env.example` · `pyproject.toml` + `uv.lock` · LICENSE 없음(사용자 결정 전) · **Procedure Hub · 이 프로젝트 경로에 기대지 않는다**(절대경로 금지)
4. 키 · 캐시(`cache/`) · `.venv` 는 git 에 안 들어간다(`.gitignore` 이미 있음 — 유지 · 보강)

## 4. 먼저 읽을 핵심 파일

- SPEC-002 §4 Interface Contract(tool 입출력) · §5 Implementation Rules · §6 Verification

## 5. allowed_paths

- `reference/2026-10-27-mfds-mcp/` 안만(`.env` 는 읽기만 — 수정 금지)

## 6. 구현 단계

1. 뼈대: pyproject(공식 MCP SDK · httpx) · 패키지 · stdio 진입점
2. API 클라이언트(키 주입 · 키 마스킹 · 에러 구분 · 캐시 · 일일 상한) → tool 들 → `mfds_status`
3. 테스트(실호출 없는 고정 응답) · 실호출 확인 스크립트(`scripts/smoke.py` 같은 것 — 의료기기 · 업체 · 의약품 각 1~2회, DUR 은 미등록 확인)
4. README · `.env.example`
5. 마지막에 MCP 를 stdio 로 한 번 띄워 `tools/list` · tool 하나 호출까지 확인

## 7. 범위 제약 — 하지 말 것

- 커밋 · push 금지. 폴더 밖 수정 금지. 키 값 노출 금지(테스트 · 로그 · 예외 메시지 포함)
- 대량 호출 금지(확인용 몇 번)

## 8. 검증

```
폴더 안에서 uv sync · uv run pytest(실호출 없음) · uv run ruff check . — 각 1회. 실호출 확인 스크립트는 키가 있을 때 엔드포인트당 몇 번만. 키 · 캐시 · 개인 경로가 git 에 안 들어가는지 git status 로 확인
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
  --to <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> \
  --text "[worker_done] tool_dev 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal <코디handle — stale 이라 미치환. 직접 확인해 채울 것> --text "[질문] tool_dev: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
