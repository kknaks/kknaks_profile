# [researcher] 통역 서버를 DAY 에 옮기려면 — 원천 두 곳 조사 (read-only)

너는 **day `researcher` 워커**다. **너는 앞 판의 맥락이 없다.**

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 문서)
- 배경: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/e2e-feedback.md` 「버그 기록」 5번 · 그림 `e2e-shots/05-app-interpret-not-connected.png`

**read-only.** 어떤 레포도 고치지 않는다. 산출물은 리포트 1개뿐.

## 배경

DAY 직원 앱(TestFlight)의 통역이 안 된다. 코디가 확인한 것: **DAY 서버에 통역 기능이 없다** — `backend/` 에 interpret · soniox 코드 0건, dev 로그 `WebSocket /api/interpret` 403(없는 경로). 앱 쪽(WS 클라이언트 · 마이크 · 재생 · 드로어)은 구현돼 있다.

사용자(2026-11-11): 「토큰만 넣으면 되는지 통역 로직 구현해야 하는지」 · 「번역 플로우는 cc-prototype · interpret-pwa 에 있어. 사전도 따로 등록해야 해 interpret-pwa 처럼」.

조사 목적 = **DAY 서버에 통역을 옮기는 스펙을 쓰기 전에, 무엇을 그대로 가져오고 무엇을 정해야 하는지**를 근거와 함께 뽑는다. 결정하지 않는다 — 「정할 것」으로 모은다.

## 읽을 곳

| 무엇 | 어디 |
|---|---|
| 통역 원형(서버) | `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/api/interpret.py` · `service/interpret/`(session · soniox · chinese · assembler) · `config.py` · `container.py` |
| 통역 원형 문서 | `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/para/projects/summer-star/cc-prototype/` (spec · decision 중 통역 · sts) |
| 통역 최신(사전 포함) | 코드 `/Users/kknaks/git/toy_pr2/interpret-pwa/back/`(특히 `seed/glossary.json` · 통역 세션 · Soniox 호출 · 통역 기록) · 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/para/projects/summer-star/interpret-pwa/`(baseline · decision · spec — D-33 · D-36 · D-37 · D-41 등) |
| DAY 앱 클라이언트 | `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/app/lib/interpret/` · `app/lib/state/`(통역) · `app/lib/ui/interpret_widgets.dart` · `app/README.md` 「통역 WS 핸드셰이크」 · 「서버 의존 D-3」 |
| DAY 계약 | `/Users/kknaks/orca/workspaces/mediness-mediness/fix-spec/products/day/20-spec/spec-003-mobile-app.md` U-15(통역) · 표 「통역 — 사전은 서버 통역 컨텍스트로」 · 관련 OQ |
| DAY 서버 구조 | `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix/AGENTS.md` · `backend/day/routers/api/` · `backend/common/config.py` · `scripts/deploy/day_vm.py`(선택 비밀 방식) · `deploy/`(Caddy · compose — WebSocket 통과 설정) |

canonical 체크아웃(`/Users/kknaks/git/...`)은 사용자 것이다 — 읽기만 하고 pull · checkout 하지 않는다. 최신 원격을 봐야 하면 `git fetch` 뒤 `git show origin/<branch>:<path>`.

## 답할 것

1. **원형 서버 흐름**(cc-prototype): WS 경로 · 인증 · 클라이언트 ↔ 서버 메시지 종류 전부 · 오디오 형식 · Soniox 를 어떻게 부르나(모델 · 옵션 · 언어 쌍 · 번역 방식) · 음성 합성(TTS)을 누가 하나 · 세션 수명 · 끊김 · 오류 코드 · 중국어 처리(`chinese.py`)가 무엇인가 · 설정 env 이름.
2. **interpret-pwa 가 원형에서 바꾼 것**: 사전(용어집)의 구조(칸 · 언어 · 건수) · 서버가 사전을 통역에 싣는 방법 · 모드(자동 듣기 / 누르고 말하기) · 통역 기록 · 언어별 줄이기 한도 등. 원형과 나란히 표로. **어느 쪽을 DAY 의 바탕으로 삼는 게 맞는지** 근거(판단은 「정할 것」).
3. **DAY 앱이 기대하는 계약**: 앱 클라이언트가 보내고 받는 메시지 · 헤더 · 닫힘 코드 · 오류 처리를 코드에서 **전부** 세고, 원형 서버 · interpret-pwa 서버와 필드 단위로 대조한다. 앱을 안 고치고 서버만 지으면 되는지, 앱도 고쳐야 하는 차이가 있는지.
   - 덧: 지금 앱이 「없는 경로 403」을 「통역 서버가 로그인을 받지 않았어요」로 보인다 — 어느 코드가 그렇게 하는지.
4. **DAY 서버에 놓을 자리**: AGENTS.md 계층에 맞추면 어느 폴더에 무엇이 가는지 · 인증(앱 Bearer 세션)을 WS 에 어떻게 붙이는지(기존 SSE 스트림 방식 참고) · 새 의존성 · 프로세스 수 / 동시 세션 상한 / 메모리(B2s VM)에서 걸릴 것 · Caddy · compose 가 WebSocket 을 통과시키는지.
5. **비밀 · 설정**: Soniox 키를 어디에 두나 — 기존 선택 비밀 방식(`day_vm.py` `OPTIONAL_SECRETS` · Key Vault `day-<env>-…`)에 맞추면 무엇이 추가되는지. 그 밖 설정 칸.
6. **사전 등록**: interpret-pwa 방식(레포 시드 파일 → 재배포)을 DAY 에 그대로 쓸 때와 DB 에 둘 때의 차이. DAY 데이터 규칙(`day.json` `data_rules`)과 부딪히는 곳. 병원마다 다른 사전이 필요한지는 사용자가 정한 적이 있는지(문서 근거가 있으면 인용 · 없으면 「정한 적 없음」).
7. **규모**: 가져올 파일 · 대략 줄 수 · 새로 써야 하는 것 · 시험 방법(실제 Soniox 호출 1회가 완료 조건이 되어야 하는 자리).
8. **정할 것**: 사용자가 정해야 하는 것만, 후보와 함께.

## 규칙

- 질문마다 답 + 근거(`파일:줄` · git ref · 문서 절). 확인 못 한 것은 「확인 안 됨」.
- **실제 Soniox · KOS · 서버 호출 금지.** 키 · 토큰 · 고객 값 · 통역 기록 원문을 리포트에 옮기지 않는다(env 이름 · 칸 이름만). profile 레포는 PUBLIC.
- 사용자 포트(11040) · 프로세스 금지. 다른 워커(planner — mediness `fix-spec`)가 스펙을 고치는 중이다 — 그 워크트리는 읽기만.

## 보고

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-r3/orchestration/work/fix/research-interpret-report.md`
머리에 **세 줄 결론**(토큰만으로 되나 · 무엇을 바탕으로 · 앱을 고쳐야 하나), 이어서 1 ~ 8.

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 다르면 preamble 이 맞다.

끝나면 **두 명령 모두**:

```bash
orca orchestration send \
  --to term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --from term_7b626c58-91d9-4ad3-8429-de5dca2aad2e \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher 완료: <한 줄>" \
  --body "세 줄 결론 / 정할 것 N건 / 확인 안 됨 목록"

orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 \
  --text "[worker_done] researcher 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

막히면: `orca terminal send --terminal term_284b2ffb-0602-4a35-b76f-0f005373d1e2 --text "[질문] researcher: <질문>" --enter`
