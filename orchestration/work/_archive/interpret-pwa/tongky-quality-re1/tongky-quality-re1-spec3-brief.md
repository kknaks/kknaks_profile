
# [planner] SPEC 0.9.5 · WORK — 세 참여자(D-68 · D-69)

너는 **interpret-pwa `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/roles/interpret-pwa/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

코디 워크트리를 그대로 쓴다. 코디가 `10-decision/` 에 D-67 ~ D-69 · BASE-001 입력 6 을 이미 적었다 — 그 파일은 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` **D-68 · D-69**(+ D-03 반이중 · D-09 원 표시 · D-36 누르고 말하기 · D-67) · 끝의 「열린 것 (2026-11-16)」 ← 근거. **여기 없는 정책은 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md` 입력 6 · 확인한 사실(2026-11-16)
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/orchestration/work/tongky-quality-re1/research-turn-taking-report.md` ← 사실 · 수치 · Soniox 문서 URL(agent text · manual finalization) — SPEC 이 인용할 근거
- `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` 0.9.4 전체 중 §5(통역 WS) · §7(화면 · §7.3 원 상태 · §7.4 반이중) · §8 · §9
- 지금 코드(읽기만): `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/back/app/service/interpret/{session,assembler,soniox}.py` · `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/front/lib/{interpret,halfDuplex,ptt}.ts` · `/Users/kknaks/orca/workspaces/interpret-pwa/tongky-quality-re1/front/components/interpret/InterpretScreen.tsx`

기대는 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/통키-품질개선/para/areas/concept/front/half-duplex-echo-suppression.md` — 이번에 이 개념을 **대체**한다(개념 문서는 고치지 마라 · 코디 몫).

## 2. 배경

통키를 통로가 아니라 「고객 – 통키 – 직원」 세 번째 참여자로 바꾼다. D-68 규칙: ① 자막은 확정되는 대로 바로 · **음성은 차례 끝에** 그 차례 번역을 이어 읽는다 ② 재생 중에도 마이크 송신(반이중 걷음) ③ 자기 목소리는 통역하지 않는다 ④ 끼어들면 재생 바로 멈춤 · 멈춘 번역은 다시 읽지 않고 자막으로만. D-69 만드는 법: 차례 끝 = back 서버 시계 1초(말하던 사람 언어 원문 토큰의 마지막 새 도착부터) · 끼어들기 = 재생 시작 뒤 반대 언어 토큰 2개 · **Soniox agent text 입력 사용**(재생할 번역문을 STT 에 보냄) + 언어 걸러내기는 뒷받침.

## 3. 계약 — SPEC 이 정해야 할 것(backend · frontend 가 이대로 만든다)

- **WS 메시지**: 끼어들기로 back 이 재생을 멈출 때 front 에 무엇을 보내나(새 메시지면 이름 · 모양 · 이미 받은 PCM 처리). front → back 으로 재생 상태(시작 · 끝 · 멈춤)를 알려야 하는지 — agent text 시점(문서: 재생 0.5 ~ 1 s 앞 · 서버 보낸 시각 어림 허용)과 ③ 의 「재생 중 + 끝난 뒤 여유」 창을 무엇으로 잴지에 따라. 기존 메시지(§5.3)는 바뀌는 것만.
- **agent text**: 보내는 메시지 모양 · 시점 · 끼어들기 때 끝내는 법(조사 리포트 · 공식 문서 인용) · STT 설정 키가 필요하면 그 키(§5.10 「그 밖의 STT 설정」 · `enable_agent_text_input` 은 지금 「쓰지 않는다」 로 묶여 있다 — D-69 로 푼다).
- **차례 상태**: 누가 말하는 중 · 통키 차례 · 대기 — back 이 갖는 상태와 전이. 재생 언어 토큰은 차례 끝 계산 · 끼어들기 셈에서 뺀다. 차례 중에 상대 언어 말이 시작되면(상대가 대답) 어떻게 되나.
- **누르고 말하기(D-36)** 와의 관계: 그대로 두되 반이중 게이트를 같이 쓰던 부분(개념 문서 「같은 송신 게이트」)이 어떻게 바뀌는지.
- **원 표시(§7.3 · D-09)**: 「출력 중」 표시는 재생 동안 그대로 · 송신 판정(`outputting`)과 묶인 부분은 D-68 로 고친다. 새 화면 문구는 만들지 않는다(시안 · DEC 에 없는 문구 금지).
- 기록(§5.9): 버린 되울림 토큰 · 멈춘 재생을 기록에 남기는지 — DEC 에 없으면 「그대로(caption 만 기록)」.

## 4. 먼저 볼 것

- SPEC 에서 `grep -n -E "반이중|TTS|audio_start|audio_end|outputting|재생|송신|half-duplex"` 결과 전부 — 반이중을 전제한 문장을 하나도 빼지 말고 센다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `para/projects/summer-star/interpret-pwa/20-spec/`
- `para/projects/summer-star/interpret-pwa/30-work/`

## 6. 할 것

1. SPEC **0.9.5**(front matter · 변경 이력 맨 위 · §1 범위 한 줄). 새 절(예 §5.13 「세 참여자 — 차례 · 끼어들기 · agent text」)과 §5.3 · §5.10 · §7.3 · §7.4 · §8 고침. 숫자(1초 · 2개)는 코드 상수 한 곳 · env 아님(§2.4 원칙을 따름).
2. §9.1 시험(가짜 Soniox): 차례 끝 전엔 TTS 없음 · 차례 끝에 그 차례 번역을 순서대로 · 재생 중 반대 언어 토큰 2개 → 멈춤 메시지 · 남은 큐 버림 · 재생 언어 토큰은 차례 끝 · 끼어들기 셈에서 빠짐 · agent text 가 재생 전에 나감 · 반이중 없이 재생 중 PCM 이 나감(front).
3. §9.6 「배포 뒤 확인 0.9.5」: 사용자 실기기 zh(손님이 이어 말한 뒤말이 기록에 남는가 · 직원 쪽도 · 끼어들면 재생 멈춤 · 되울림이 손님 자막으로 뜨는 수 · 말 끝 → 음성 시작 체감) — OQ-035 를 닫는 측정(재생 대 목소리 크기 체감 · 되울림 오발)도 여기. 기록은 수치만.
4. 부록 A · 제목 D 목록 · §10(OQ-034 ~ 036 상태 · 새로 열린 것만).
5. WORK: **WP30**(back) · **WP31**(front) · **WP32**(배포 · 실기기 — WP29 절차) 행. 병렬 절(back · front 병렬 가능한지 · 계약 고정 뒤). WP29 상태 칸: 2026-11-16 배포 끝(코드 #13 `fe375ad` · infra #56) · 실기기 결과 = 문장 경계 확정 뒤 재생 중 뒷말 버려짐 → D-68.

## 7. 범위 제약 — 하지 말 것

- DEC · 코드 · 개념 · `orchestration/` 수정 금지. DEC 에 없는 정책 · 화면 문구를 만들지 않는다 — 막히면 「정할 것」 으로 보고.
- 실기기 기록 문장 · 키를 옮기지 않는다(PUBLIC).

## 8. 검증

```
SPEC 의 모든 절이 DEC · 확정 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 계정값 · 실명 0(grep)
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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_0cdc063d-4b42-4e5f-bc41-65528f81e60f --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
