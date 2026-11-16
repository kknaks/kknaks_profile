
# [researcher] 세 참여자(D-68) — 차례 끝 · 겹친 소리 · 끼어들기 신호 조사(OQ-034 ~ 036)

너는 **interpret-pwa `researcher` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/researcher/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)


## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-68**(세 참여자 · 규칙 ① ~ ④ · 기본값) · 끝의 「열린 것 (2026-11-16)」 OQ-034 ~ 036 ← 이번 질문
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` 입력 6 · 「확인한 사실 (코디 2026-11-16)」
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.9.4 — §5.3 메시지 · §5.10 끊김 · §7.4 반이중
- 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/areas/concept/front/half-duplex-echo-suppression.md` · 같은 폴더 `push-to-talk.md`
- Soniox 공식: `https://soniox.com/docs/llms.txt` 에서 시작(실시간 STT WebSocket 응답 모양 · 토큰 필드 · endpoint · finalize · keepalive)

## 2. 배경

통키를 「고객 – 통키 – 직원」 세 번째 참여자로 바꾼다(D-68): ① 자막은 바로 · 음성은 차례 끝(말하던 사람이 다 마침)에 ② 재생 중에도 마이크 송신 ③ 재생 언어로 받아쓰인 말은 버림(자기 목소리) ④ 재생 중 반대 언어 진짜 말이 들리면 재생 멈춤. 만들기 전에 아래 셋을 사실로 닫아야 한다. **결정하지 말고 사실 · 수치 · 선택지 · 코디 추천을 낸다.**

## 3. 질문

**Q1 (OQ-034) 차례 끝을 무엇으로 아나**
- Soniox 실시간 응답이 **소리가 없을 때도** 오는가(빈 `tokens` · `total_audio_proc_ms` · `final_audio_proc_ms` 같은 진행 값). 토큰의 `start_ms` · `end_ms` 가 있는가.
- 있다면 서버에서 「마지막 말 토큰 끝 → 지금 처리된 오디오 시각」 차이로 「말이 N ms 멈춤」 을 잴 수 있는가. 비확정 토큰이 나오다 사라지는 경우(소음)는 어떻게 보이나.
- 다른 길(front 음량 · Soniox 의 다른 기능)이 있으면 비교.

**Q2 (OQ-035) 겹친 소리에서 받아쓰기 · 언어 태그**
- 재생 언어(예: 한국어 TTS)와 진짜 말(예: 중국어)이 겹친 오디오를 넣었을 때, 진짜 말의 받아쓰기가 얼마나 남고 토큰 `language` 태그가 맞는가. 반대(중국어 TTS + 한국어 말)도.
- 되울림 쪽(재생 언어) 토큰이 진짜 말 언어로 잘못 태그되는 비율.

**Q3 (OQ-036) 끼어들기 신호**
- 진짜 말이 시작된 뒤 반대 언어 비확정 토큰이 처음 나오기까지 지연(ms).
- 되울림만 있을 때 반대 언어 토큰이 잘못 나오는 경우 — 몇 개 · 얼마나 이어지나. 「반대 언어 비확정 토큰 k 개 또는 t ms」 기준의 후보값과 그 근거.

## 4. 실물 시험 — 하는 법

- 시험 스크립트 · 음성 파일은 **`/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe/`** 에만 둔다(레포 안 금지).
- 코드 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back` 의 venv · `app.service.interpret.soniox`(STT · TTS 연결 · `stt_config`)를 import 해서 쓴다(읽기만 · 코드 수정 금지). 음성은 Soniox TTS 로 만든다(기존 `back/scripts/quality_check.py` 가 TTS 로 파일 만드는 방식 참고). 겹친 소리 = 두 PCM 을 더해 만든다(음량 비 몇 가지 — 폰 스피커가 말소리보다 크거나 비슷한 경우). 실제 폰 스피커 · 방 울림과는 다르다는 한계를 리포트에 적는다.
- Soniox 키: `export SONIOX_API_KEY=$(ssh medi-me "/opt/homebrew/bin/kubectl -n interpret-pwa-prod get secret interpret-pwa-secret -o jsonpath='{.data.SONIOX_API_KEY}'" | base64 -d)` 로 **그 셸 env 에만**. 키를 출력 · 파일 · 리포트 · 로그에 남기지 않는다.
- 호출은 필요한 만큼만(언어 zh 중심 · ja 하나 정도면 충분).

## 5. allowed_paths — 이 밖은 건드리지 마라

- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-turn-taking-report.md`
- 시험 파일: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile--------/6b7f4a9c-bfce-487f-8c42-08de89fd57d4/scratchpad/probe/`

## 6. 리포트 모양

질문마다: 답(사실) · 근거(공식 문서 URL 또는 실물 수치 — 어느 쪽인지 표시) · 문서에 없는 것은 「문서에 없음」 · 선택지 · 코디 추천. 끝에 「정할 것」 목록. 기록 문장 · 키 0.

## 7. 범위 제약 — 하지 말 것

- 코드 · 문서(DEC · SPEC · WORK) 수정 금지. 결정하지 않는다.
- 운영 서버 · 사용자 포트 · 프로세스를 건드리지 않는다(키를 읽는 kubectl 한 줄 외).

## 8. 검증

```
질문마다 답 + 공식 문서 URL. 문서에 없는 것은 「문서에 없음」. 결정하지 않고 「정할 것」으로 모은다
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
  --to term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] researcher: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
