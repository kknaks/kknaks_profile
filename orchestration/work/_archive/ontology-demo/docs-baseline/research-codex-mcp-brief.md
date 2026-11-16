
# [research] mediness-app 조사 — codex 워커 연결·MCP 사용 패턴

너는 **조사 워커**다 (read-only — 리포 파일 수정·생성 금지, 산출물은 §4 리포트 1개뿐).

## 1. 조사 대상 (read-only, 절대경로)

`/Users/kknaks/git/harness_works/mediness-app`

여기에 **codex(gpt-5.6 계열)를 open-kknaks 워커로 붙이고 MCP 를 쓰는 실물 구성**이 있다.
우리(ontology-demo)가 같은 구조를 `app/ontology-agent/` 에 재현해야 한다(참고 대조:
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/app/back/service/chat/` — 우리 레포의 기존 open-kknaks 패턴,
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/app/mcp/` — 우리 FastMCP 패턴).

## 2. 조사 질문 — 전부 파일:줄 근거로 답하라

1. **codex 워커 기동**: compose(또는 실행 스크립트)에서 codex 워커 서비스가 어떻게 정의되나 —
   이미지/커맨드·env·볼륨(codex CLI 마운트?)·redis 연결·queue 이름 규약. 모델(gpt-5.6-terra 등)은
   어디서 지정하나.
2. **open-kknaks 결선**: AgentClient/RedisBroker 설정(제출 큐·응답 스트림·세션/turn 관리),
   제출 페이로드에 무엇이 실리나(시스템 프롬프트·도구 목록·컨텍스트).
3. **MCP 연동**: codex 가 MCP 서버를 어떻게 아나 — 설정 파일(config.toml 등)? 제출 시 동적 전달?
   Streamable HTTP URL 은 어떻게 주입되나. 도구 호출 결과가 응답 스트림에 어떻게 나타나나.
4. **소비·폴링**: 백엔드가 워커 응답을 어떻게 소비해 DB/API 상태로 접는가(consumer·폴딩),
   타임아웃·실패·재시도 처리.
5. **우리 적용 체크리스트**: 위를 `app/ontology-agent` 에 재현할 때 필요한 것 목록 —
   compose 추가분(queue=ontology 분리), env 키, MCP 서버 기동 방식, 코드로 가져올 패턴 vs
   우리 상황에서 달라져야 할 것.

## 3. 주의

- **사내 레포다** — 리포트에는 **패턴·구조·설정 키**만 옮겨라. 사내 도메인 지식·비밀값·
  프롬프트 본문·데이터는 옮기지 마라. 파일:줄 참조로 충분하다.
- 조사 대상 레포를 수정하지 마라. 코드 실행 불필요.

## 4. 산출물 — 이 파일 1개만 생성

`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/orchestration/work/docs-baseline/research-codex-mcp-report.md`

구조: §1 codex 워커 기동 / §2 open-kknaks 결선 / §3 MCP 연동 / §4 소비·폴링 / §5 ontology-agent 적용 체크리스트 (각 절 파일:줄 근거).

## 5. 완료 보고 — 2채널 모두 (preamble 의 taskId·dispatchId 사용)

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "research 완료: codex·MCP 패턴" --body "핵심 발견 5줄 / 적용 체크리스트 요약"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] research 완료 — codex·MCP 패턴. 상세는 리포트." --enter
```
