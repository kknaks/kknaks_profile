# [architect] 카카오톡 Mac 조회·발송 가능성 조사 (read-only)

너는 strong-hajin `architect` 워커다. **맥락이 없다** — 아래가 전부다.
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md`
- 결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 (특히 카톡 행 · 메시지함/답장 행)

## 1. 질문 (사용자 2026-10-06)
카카오톡은 **Mac 에서만** 지원한다. Strong Hajin 데스크톱 앱(Tauri·Rust)이 Mac 의 카톡을 **조회(수집)** 하고 **발송(답장)** 까지 할 수 있나? 할 수 있다면 어떤 방식으로?

## 2. 읽을 것
1. 우리 과거 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/` 전부(00-baseline·10-decision·20-spec·log). **Mac 에 해당하는 것과 Windows 전용인 것을 갈라라**(대부분 Windows 판일 수 있다). 코드 레포 canonical 경로는 Windows(`C:/Users/sc971/...`)로 낡아 이 Mac 에 없다 — 문서만 근거로
2. 외부 레포 https://github.com/silver-flight-group/kakaocli — **scratchpad 에 얕게 clone 해서 읽기만**(빌드·실행·설치 금지 · 이 레포 밖으로 아무것도 설치하지 마라). 확인할 것:
   - 조회: Mac 카톡의 로컬 DB 위치·형식·암호화, 키를 어떻게 얻나(사용자 입력? 기기 값에서 유도?), 방 목록·메시지·첨부·사진을 어디까지 읽나, 실시간 감지 방식(파일 감시? 폴링?)
   - 발송: **어떤 방식으로 보내나**(손쉬운 사용(Accessibility)·AppleScript UI 자동화? 내부 API? 그 밖?), 필요한 macOS 권한, 카톡 창이 떠 있어야 하나, 첨부 보내기 되나, 실패·오발송 위험
   - 언어·라이선스(재사용 가능 범위) · 마지막 커밋·지원하는 카톡 버전 · 이슈에 나온 깨짐 사례
3. 실제 이 Mac 은 **읽기 확인만** 허용: `ls` 로 카톡 컨테이너 경로 존재 여부 정도. **DB 열기·복호화·카톡 조작·메시지 발송 금지**

## 3. 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/kakao-survey.md` 하나:
- §1 결론 한 문단 — 조회 가능? 발송 가능? 각각 어떤 조건에서
- §2 조회 방식 (mykakao 근거 vs kakaocli 근거 비교 표)
- §3 발송 방식 · 권한 · 위험
- §4 Strong Hajin 에 붙이는 그림 — Tauri(Rust) 데스크톱이 무엇을 하고 서버가 무엇을 하나. kakaocli 를 그대로 쓰나(사이드카 실행) / 방식만 Rust 로 옮기나 — 선택지와 근거(결정은 하지 마라)
- §5 앞서 열린 질문 K-1~K-6 과의 관계(`_RESUME.md` 카톡 행) · 새로 생긴 질문
- §6 약관·안정성 위험(카카오 비공식 · 버전 업데이트로 깨짐)
- 모든 주장에 근거(파일:줄 / 레포 경로:줄 / 커밋)

## 4. 하지 말 것
- 정책·스펙 쓰지 마라 · 다른 파일 쓰지 마라(§3 파일 하나만) · 커밋 금지
- 카톡 DB 복호화·실행·발송 등 **실물 조작 금지**

## 9. 완료 보고 — 문구 변경 금지
> 핸들은 dispatch preamble 의 값을 믿어라.
```bash
orca orchestration send --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_a0ef6537-e532-4b7e-84e5-7e174161f6d8 --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "architect 완료: 카톡 조사" --body "결론 / 근거 / 미결"
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[worker_done] architect 완료 — 카톡 Mac 조회·발송 조사. 상세는 kakao-survey.md" --enter
```
- 막히면: `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] architect(kakao): <질문>" --enter`
