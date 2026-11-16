# 리뷰 리포트 — interpret-pwa-poc / doc (2026-10-26)

- 대상: `para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md`(이하 SPEC) · `30-work/work-001-interpret-pwa.md`(이하 WORK)
- 기준: DEC-001(accepted, D-01~D-17) · BASE-001 · 작성 브리프 `interpret-pwa-poc-spec-brief.md` §6
- 대조 자료: cc-prototype `origin/main:procedure/back/app/{api/interpret.py,service/interpret/{session,soniox,assembler,chinese}.py,service/auth.py,main.py}` · medikit README(`_archive/cc/design/_ds/medikit-*/README.md`) · Soniox 공식 문서 2026-10-26(`stt/concepts/context` · `stt/rt/error-handling` · STT/번역/TTS 지원 언어 · `tts/concepts/voices`)
- planner 리포트(`*spec*report*.md`): 폴더에 없음 — 문서 본문만으로 판정

## 판정: FAIL

FAIL 2건. 둘 다 고칠 곳이 좁다(SPEC 몇 줄). 나머지는 WARN이며 DEC 반영 · public 값 · 언어 코드는 통과.

| 브리프 §6 점검 | 결과 |
|---|---|
| ① D-01~D-17 이 SPEC 에 다 있나 | **PASS** — 부록 A(`spec:478-496`)에 17개가 모두 있고, 가리키는 절이 실제로 그 내용을 담고 있다. 빠진 번호 0 |
| ② DEC 근거 없는 정책 | **PASS(주의)** — DEC 밖 값은 모두 「기본값」으로 표시되어 있다(§0 정의 `spec:51`). 사용자 확인이 필요한 것은 OQ-005·007 로 올라가 있다. 단 FAIL-2 는 기본값끼리 D-09 와 충돌한다 |
| ③ BE↔FE 계약이 같은 모양으로 읽히나 | **WARN** — 로그인 · 용어집 · WS 메시지 · 오류 코드 모양은 한 벌이다. 재연결 · 백그라운드 복귀 동작은 비어 있다(FAIL-1 · WARN-1) |
| ④ env · 포트 · 경로 일관성 | **WARN** — 8800/3800 은 한 벌이고 지금 LISTEN 중인 것도 없다. `INTERPRET_BACK_PORT` · `NEXT_PUBLIC_API_BASE_URL` 을 누가 읽는지가 비어 있다(WARN-2) |
| ⑤ 실물 확인이 WORK 완료 조건에 들어갔나 | **PASS** — §9.3 ①~④·⑥ → WP2, §9.4 → WP7, §9.5 · 기기 → WP8, 실 matrix → WP1, 실발화 → WP4 |
| ⑥ 번체(D-17) · `yue` | **PASS** — `yue`→Soniox `zh` · 자막 `s2tw` · TTS 간체 · 용어 target `t2s` 로 닫혔다. 광둥어 품질(OQ-001)과 TW/HK 만다린(OQ-004)은 열린 것으로 명시되어 있다. Soniox 지원 언어표에서 `yue` 부재와 `zh` TTS 「Simplified only」를 확인했다 |
| ⑦ public — 키 · 비밀번호 · 실명 | **PASS(SPEC·WORK)** — grep 결과 0. 대상 밖인 DEC/BASE 에 로그인 아이디 값이 있다(참고-1) |

## FAIL

### FAIL-1 · `invalid_request` 재연결(§4.4 4번)의 시점 · 판별이 비어 있어 워커가 추측으로 메워야 한다
- 위치: `spec:207` · `spec:262`(`ready` = 「Soniox 두 연결 완료」) · `spec:427`(§9.1 시험) · `work:51`(WP2 완료 조건)
- 근거: D-05(한도를 넘으면 `terms` 를 줄인다) · rules.md 「워커가 추측으로 메워야 하는 빈칸」
- 사실:
  - 원형 `SonioxStt.open` 은 설정을 보내고 바로 반환한다(`soniox.py:78-82`). Soniox 는 설정을 받아도 응답(ack)을 보내지 않는다. 거절은 나중에 메시지 흐름 안에서 `{"error_code":400,"error_type":"invalid_request",…}` 로 오고, 그 직후 연결이 닫힌다(공식 `stt/rt/error-handling`).
  - 원형은 `open_stt` 직후 바로 `ready` 를 보낸다(`session.py:106-112`). 거절은 `_stt_reader` 안에서 `SonioxError(문자열)` 로 바뀌어 `soniox_unavailable` 로 끝난다(`session.py:131-133`, `soniox.py:52-55`). 이때 `error_type` 은 문자열 안에 묻혀 사라진다.
- 비어 있는 것: ① 거절을 언제 알아채나 — `ready` 를 보내기 전에 첫 메시지를 몇 초 기다리나, 아니면 `ready` 뒤 중계 도중에 알아채고 조용히 다시 붙나 ② 기다리는 동안 들어온 PCM 은 버리나 · 쌓나 · 재연결한 쪽으로 보내나 ③ `invalid_request` 를 무엇으로 판별하나(`error_type` 필드 · Soniox 권고는 `error_type` 분기) ④ 재연결 때 TTS 연결도 다시 여나.
- 영향: §9.1 「context 재연결」 시험의 가짜 Soniox 동작이 워커마다 달라진다. th 는 글자 수가 한도에 붙어 있어(`spec:210`) 토큰 기준으로 실제로 거절될 가능성이 있는 경로다.
- 권장: SPEC §4.4 4번에 시점(예: 설정을 보낸 뒤 N초 동안 첫 응답 또는 오류를 기다리고 나서 `ready`, 또는 `ready` 뒤 첫 오류에서 재연결하고 그 사이 PCM 은 버림), 판별 기준(`error_type == "invalid_request"`), `SonioxError` 에 `error_type` 을 싣는 것을 한 줄씩 정한다.

### FAIL-2 · 「멈춤」이 「출력 중」보다 먼저 판정되어 멈춤 직후 TTS 가 나와도 D-09 안내가 뜨지 않는다
- 위치: `spec:363`(판정은 위에서부터) · `spec:369-370`(멈춤이 출력 중보다 위) · `spec:260`(`pause` 때 back 이 `finalize` → 말하던 발화를 확정)
- 근거: D-09 「TTS 재생 중에는 그 언어 색 + 〈언어〉로 출력 중 안내」
- 사실: 원을 누르면 `pause`(`spec:378`)가 간다. back 은 `finalize` 로 그 발화를 확정하고 TTS 를 보낸다(원형 `session.py:159-162` → `_emit` → `_tts_worker`). 그래서 「멈춤 상태에서 TTS 재생」은 원을 누를 때마다 생기는 흔한 경로다. 이때 표대로 판정하면 원은 회색 「멈춤」으로 남고, 출력 언어 색과 「〈언어〉로 출력 중」은 뜨지 않는다.
- 권장: 「출력 중」을 「멈춤」보다 위로 올리거나, 멈춤 행에 「단 재생 중이면 출력 중」이라고 적는다(§9.2 단위 시험 「상태 판정 순서」에도 같이).

## WARN

### WARN-1 · 백그라운드에서 돌아왔을 때의 「멈춤」은 §7.3 의 멈춤과 다른 상태인데 같은 이름이다
- 위치: `spec:417` vs `spec:369` · `spec:378`
- 근거: D-07 · 브리프 §6 ③(FE 가 같은 모양으로 읽히나)
- §7.3 의 멈춤은 WS 가 열린 채로 `pause` 한 상태이고, 원을 누르면 `resume` 을 보낸다. §8 의 복귀 「멈춤」은 WS 가 이미 닫힌 상태이고, 원을 누르면 새 WS 와 새 `start` 가 필요하다. 상태 하나에 원 누름 동작이 둘이다. 표에 행을 나누거나(예: 「닫힘 · 원을 눌러 다시 연결」) 판정 조건을 적어야 한다.

### WARN-2 · `INTERPRET_BACK_PORT` · `NEXT_PUBLIC_API_BASE_URL` 을 누가 읽는지 비어 있다
- 위치: `spec:97` · `spec:103` · `spec:118` · `spec:121` · `spec:108`
- 근거: D-11 · 브리프 §6 ④
- 개발 실행은 `uvicorn … --port 8800` 처럼 CLI 에 포트가 박혀 있다(`spec:103`). uvicorn CLI 는 `config.py` 를 읽지 않으므로 `INTERPRET_BACK_PORT` 를 바꿔도 효과가 없다. compose 포트 매핑과 Dockerfile CMD 가 이 값을 쓰는지도 정해져 있지 않다.
- `NEXT_PUBLIC_API_BASE_URL` 은 레포 루트 `.env.example` 에 둔다(`spec:108`). 하지만 `cd front && npm run dev` 는 `front/.env*` 만 읽는다. compose `build.args` 도 `env_file` 이 아니라 `${…}` 치환으로 받아야 한다.
- 권장: 「이 env 를 읽는 곳 = Dockerfile CMD · compose `ports`/`build.args` 치환 · dev 명령」을 한 줄로 고정한다. 아니면 `INTERPRET_BACK_PORT` 를 env 목록에서 빼고 포트는 8800 으로 고정한다.

### WARN-3 · medikit 에 없는 컴포넌트 이름(`Select` · `Drawer`)이 계약에 적혀 있다
- 위치: `spec:359` · `spec:404` · `work:52`
- 근거: D-10 · 개념 design-system(「실재를 대조한다」)
- medikit README 컴포넌트 목록에는 `Select` · `Drawer` 가 없다. 실재하는 것은 `ComboBox` · `Menu` · `Modal` · `Dialog` 이다. SPEC 이 「또는 실재하는 것」으로 열어 두었지만, 실재 이름으로 확정하는 편이 워커 간 편차를 줄인다. 색 · 글자 클래스(`bg-primary` · `bg-purple` · `bg-red` · `bg-ms-gray-300/400` · `text-ms-gray-500/800` · `text-typo-headline-md-600`)는 README 규칙에 맞는다.

### WARN-4 · §7.3 표와 본문의 외국어 영역 「오류」 문구가 다르다
- 위치: `spec:367`(외국어 영역 열 「—」) vs `spec:377`(4개 상태에 「오류 머리말」 포함)
- 근거: D-09 · rules.md 「추측으로 메워야 하는 빈칸」 — front 가 오류 때 외국어 영역에 무엇을 띄울지 둘 중 하나를 골라야 한다.

### WARN-5 · WP 결과로 닫아야 하는 열린 것의 자리가 WORK 에 없다
- 위치: `work:82-88` · `spec:466` · `spec:469` · `spec:472`
- 근거: rules.md 「인수조건이 확인 가능한가(누가 · 무엇으로)」
- OQ-003(역방향 용어 — §9.3 ② 결과로 결정)과 OQ-009(괄호 병기 — §9.3 ⑤ 결과로 사용자 결정)는 WP2 산출물을 보고 닫는다. 그런데 WORK 열린 것 표에도, WP 완료 조건에도 들어가 있지 않다.
- OQ-006 은 「WORK 리뷰에서 본다」(`spec:377`)고 했는데, WP5 리뷰 항목(`work:54`)에는 없다.

### WARN-6 · iOS 에서 새로고침으로 통역 화면에 바로 들어오면 `AudioContext` 를 깨울 사용자 동작이 없다
- 위치: `spec:382` · `spec:386`
- 근거: D-03(TTS 재생) · §7.4
- 깨우는 자리는 「로그인 단추 · 원 누름」뿐이다. 토큰이 살아 있어 로그인 화면을 건너뛰면(`spec:312`) 자동으로 시작한 세션의 TTS 가 첫 원 누름 전까지 소리 없이 재생될 수 있다. 원 누름은 `pause` 를 겸하므로 깨우려고 누르면 멈춘다. 기기 확인(§9.5)에서 처음 드러날 자리라 기본 동작(예: 첫 탭 오버레이)을 지금 적어 두는 것을 권장한다.

## 고객이 실물에서 만날 자리

- **th(태국어) context 한도**: 글자 수는 약 9,945자로 10,000에 붙어 있다(`spec:210`). 토큰 기준으로 넘으면 FAIL-1 경로로 간다. `terms` 를 빼도 넘으면 th 는 통역 자체가 안 된다(OQ-002).
- **`yue` 선택 = 만다린 음성 + 표준 문어 번체 자막**(OQ-001): 「廣東話」라고 고른 환자가 만다린을 듣는다. 안내 문구도 「광둥어로 출력 중」이 된다(`spec:298` · `spec:370`).
- **Origin 정확 일치**: `INTERPRET_FRONT_ORIGIN` 기본값은 `http://localhost:3800` 이다(`spec:117`). `127.0.0.1:3800` 으로 열면 CORS가 막히고 WS 가 1008 로 닫힌다. FE 는 `/me` 가 200 이라 401 처리를 하지 않고 「오류」만 보인다.
- **잠금 단위가 back 전체**(`spec:132`): 배포 뒤 누구든 5회 틀리면 사용자도 1분 동안 못 들어온다. 기본값 표시는 되어 있다.
- **Soniox 세션 최대 시간(413 `max_duration_reached`) · 503 조기 종료**(공식 error-handling): 원형대로면 `soniox_unavailable` → 「오류 + 다시 연결」로 간다. 자동 재연결 없음(`spec:417`)과 맞는 동작이다. 긴 상담 중에 한 번은 만날 수 있다.

## 참고(기존 부채 · 대상 밖)

- **참고-1 (public 값)**: DEC `decision-001-interpret-pwa.md:50`(「사용자 지정 계정(admin)」 · 「admin / …」)과 BASE `baseline-001-interpret-pwa.md:46` 에 로그인 아이디 값이 적혀 있다. D-06 자체가 「코드 · 문서에 값을 적지 않는다」고 하고, SPEC 도 아이디 값을 문서에 쓰지 않는다고 한다(`spec:123`). 검수 대상 밖이라 처분은 코디에게 넘긴다.
- **참고-2**: 용어집 주소 `stg-procedure-hub.medisolveai.com`(`spec:33` · `spec:119`)은 인증 없는 공개 주소다. DEC/BASE 에도 이미 있다. 비밀값은 아니다.
- **참고-3**: `_RESUME.md` §3 의 planner 행이 「진행」으로 남아 있다. 검수와는 무관하다.
- Soniox 대조 결과(통과): `context` 칸 이름 · `{key,value}` · `{source,target}` · 8,000토큰(~10,000자) · `invalid_request` 모두 공식 문서와 같다. `en·ja·zh·th·vi` 는 STT · 번역 · TTS 모두 지원하고, 음색은 모든 언어에서 쓸 수 있다(Jiwoo 유지 가능). 원형과 다른 자리(`lang` 6개 · `traditional`/`scheduleId` 제거 · `context` 추가 · 잠금 단위 · 로그인 응답 축소)는 모두 이유가 적혀 있다.
