# WORK-001 WP4 결과 보고 — front 통역

## 상태: done (실발화 1회 · 실기기는 pending — 레포 루트 `.env` 에 `SONIOX_API_KEY` 없음)

워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` · 커밋 없음(변경만). WP3 리포트 `wp3-fe-report.md` 에 이어서.

## 수행 — 파일 · 화면 목록

- `front/lib/interpret.ts` — 원형 `cc-prototype origin/main:_archive/cc/front/lib/interpret.ts` **복사** 뒤 SPEC 자리만 고침(import 없음)
  - 그대로: AudioWorklet `Pcm16kWriter`(16 kHz · 640샘플 · s16le) · 24 kHz PCM 이어 붙여 재생 · 홀수 바이트 이월 · 재생 큐 비우기 · `stop` 뒤 정리 · 오류면 닫고 자동 재연결 없음
  - 고침: `start{lang}` 만(§5.1 — `traditional` · `scheduleId` 없음) · **AudioContext 를 `start()` 동기 구간(사용자 동작 안)에서 만들고 `resume()`** → 마이크 → worklet → WS(§7.4 순서 · 원형은 마이크 뒤) · **`ready` 전 PCM 송신 없음**(§4.4.1) · `AnalyserNode` RMS(`level()`) · `pause()` / `resume()` 분리(원 누름 · `pause` 때 지금 재생 멈춤 · 멈춤 중 `audio_start` 는 재생) · 원 누름 때 `suspended` 면 다시 깨움(iOS) · caption `id` → `side` 로 재생 중 발화의 출력 언어 알림 · ready 전 끊김을 `beforeReady` 로 알림
  - 원형의 비 PCM(`format`) 디코드 분기는 뺐다 — §5.3 은 PCM s16le 만
- `front/lib/halfDuplex.ts` — 반이중 문(원형 `mute` · `maybeUnmute` · `stopPlayback` 규칙 그대로 떼어 냄 · 400 ms)
- `front/components/interpret/InterpretScreen.tsx` — 세션 수명: 오버레이 탭 · [다시 연결] · 언어 고르기(사용자 동작 안)에서만 새 세션 · 언어 바꿈 = `stop` → 새 `start` · 자막 지움 · 원 누름 `pause`/`resume`(열린 4 ~ 8 만) · 백그라운드(`visibilitychange` hidden) → `stop` · 「시작 전」 · 로그아웃 → `stop` · 토큰 지움 · `/login` · ready 전 끊김 → `GET /api/auth/me`(401 이면 로그인으로) · 음량 반응(rAF · 듣는 중 1.0 ~ 1.5 · 대기 1.0 ~ 1.2 · 출력 · 멈춤 중 끔)
- `front/lib/view.ts` · `lib/phrases.ts` — 영역 배치(§7.5) · 상태 판정(§7.3 — **출력 중이 멈춤보다 위**) · 문구

## 검증 — 명령과 결과 (각 1회 · 최종 코드)

| 명령 | 결과 |
|---|---|
| `npx tsc --noEmit` | 통과 |
| `npm run lint` | 통과(경고 0) |
| `npm run build` | 통과(Next 16.4.3 — WP3 리포트 이슈 1) |
| `npx vitest run` | 2 파일 · **15 시험 통과** — 영역 배치 4 · 상태 판정 4 · 문구 3 · 반이중 4(재생 끝 + 400 ms · 재개 대기 중 새 `audio_start` 취소 · reset · **멈춤 중 `audio_start` → 출력 중 → 재생 끝 + 400 ms → 멈춤**) · 백그라운드 복귀 → 시작 전 · 오류 때 외국어 문구 |
| `node scripts/check-classes.mjs` | 쓴 클래스 78 · 빌드 CSS 에 없는 것 **0** |

브라우저 확인 — **가짜 back**(scratchpad 스크립트 · `:8800` · SPEC §5.3 메시지 모양만 맞춘 WS · Origin · `?token=` 검사) + front dev `:3800` + 헤드리스 Chrome(가짜 마이크 장치 · 맥). 스크린샷 `wp4-fe-shots/`.

| # | 확인 | 결과 |
|---|---|---|
| 1 | 새로고침 진입 → 「시작 전」 오버레이 · 탭 전 WS 0개 | 같음 |
| 2 | 오버레이 탭 → `{"type":"start","lang":"en"}`(그 밖 필드 없음) | 같음 |
| 3 | **`ready` 전 송신 0 B** · 「연결 중…」 `bg-ms-gray-300` | 0 B |
| 4 | `ready` 뒤 송신 시작 · 「말씀하세요」 `bg-ms-gray-400` · 음량 반응 | 1.2 초에 38,400 B(= 16 kHz × 2 B × 1.2 s) |
| 5 | caption `side=me` non-final → 한국어 영역에만 흐림 · 「한국어 듣는 중」 `bg-primary` | 같음 |
| 6 | final → 외국어 영역에 번역 · 진하게 | 같음 |
| 7 | `audio_start`(u1 · `side=me`) → 「영어로 출력 중」 `bg-purple` 맥박 · 외국어 영역 「Speaking in English」 | 같음 |
| 8 | **재생 중 송신 0 B**(1.5 초 음성 · `audio_start` + 100 ms ~ 재생 끝 + 300 ms) · 재생 끝 + 400 ms 뒤 송신 재개 · 「말씀하세요」 | **0 B** · 재개 확인 |
| 9 | caption `side=them` → 외국어 영역에 원문 · 「영어 듣는 중」 `bg-purple` · 외국어 「Listening」 | 같음 |
| 10 | `audio_start`(u2 · `side=them`) → 「한국어로 출력 중」 `bg-primary` | 같음 |
| 11 | 원 누름 → `{"type":"pause"}` · 「멈춤 · 원을 눌러 다시 듣기」 · 멈춤 중 송신 0 B | 같음 · 0 B |
| 12 | **멈춤 중 `audio_start`** → 「영어로 출력 중」 → 재생 끝 + 400 ms → 「멈춤」 | 같음 |
| 13 | 원 누름 → `{"type":"resume"}` → 「말씀하세요」 | 같음 |
| 14 | 출력 중 원 누름 → 재생 멈춤 + `pause` → 「멈춤」 | 같음 |
| 15 | 언어 바꿈(日本語) → 옛 WS `stop` · 새 WS `start{lang:"ja"}` · 자막 지움 · 「연결 중…」 → `ready` → 「말씀하세요」 | 같음 |
| 16 | 백그라운드 → `stop` · 복귀 → 「시작 전」 오버레이 | 같음 |
| 17 | `error` 수신 → `bg-red` · 서버 문구 · [다시 연결] · 외국어 영역 「接続エラー」 + `ErrorIcon` | 같음 |
| 18 | [다시 연결] → 새 WS · `start{lang:"ja"}` | 같음 |
| 19 | 핸드셰이크 거절 + `/api/auth/me` 401 → 토큰 지움 · `/login` | 같음 |

실 back(WP1 코드 · 가짜 로그인 값)으로 한 것(WP3 때): 로그인 → 오버레이 탭 → WS 인증 · `start` 통과 → back `error no_api_key` → 오류 상태 · 「SONIOX_API_KEY 가 .env 에 없어요」 — front ↔ back WS 경로 · 오류 표시는 실물로 확인.

PWA(운영 빌드 `next start -p 3800`): manifest 응답 · `apple-touch-icon` 링크 · `/sw.js` `Cache-Control: no-cache` · 서비스 워커 등록 · 캐시 `interpret-shell-v1` 생성 확인.

띄운 프로세스(가짜 back · 실 back · front dev · front start)는 모두 내렸다(8800 · 3800 비어 있음). 사용자 포트 3700 · 8700(docker)은 건드리지 않았다. 가짜 로그인 값은 실행 때만 쓰고 지웠다.

## 계약 대조 — SPEC 항목별

| SPEC | 같음 / 다름 |
|---|---|
| §4.4.1 클라 쪽 — `ready` 전 PCM 없음 · 같은 WS 유지(연결 중이 길어질 뿐) | 같음 |
| §5.2 `WS /api/interpret?token=` · 주소 = `NEXT_PUBLIC_API_BASE_URL` http→ws · 거절 → `/api/auth/me` 401 처리 | 같음 |
| §5.3 메시지 · 오디오 형식(16k 640샘플 송신 · `sampleRate` 재생 · `audio_end` = 보내기 끝) · `side` → 출력 언어 | 같음 |
| §7.3 상태 8개 · 판정 순서 · 색 · 문구 · 원 누름 / 오버레이 탭 분리 | 같음 |
| §7.4 오버레이 탭 안에서 AudioContext → 마이크 → WS · 반이중 400 ms · 깨우는 곳 셋 + 원 누름 | 같음 |
| §7.5 영역 배치 · 흐림/진하게 · 빈 문자열 줄 없음 · 끝으로 따라감 | 같음 |
| §8 자동 재연결 없음 · 백그라운드 → stop → 시작 전 · wake lock | 같음 |

## 이슈 · 코디가 확인할 것

1. **pending — 실발화 1회**(맥 브라우저 `localhost:3800` + 실 back WP2 · 한국어 · 외국어 각 1문장 · 재생 중 송신 0 B): 레포 루트 `.env` 에 `SONIOX_API_KEY` 가 없어 못 했다. 가짜 back 으로 같은 항목(자막 영역 · 출력 중 · 재생 중 0 B)은 확인했다. 키를 넣고 back WP2 를 띄운 뒤 `cd front && npm run dev` 로 돌리면 된다(`front/.env.local` 에 `NEXT_PUBLIC_API_BASE_URL=http://localhost:8800` — gitignore · 이 워크트리에 만들어 둠).
2. **pending — 실기기**: 휴대폰 마이크 · iOS AudioContext · PWA 설치 · 화면 꺼짐 방지 · 맥 Safari. 서비스 워커의 오프라인 화면(`offline.html`)은 헤드리스 Chrome 오프라인 흉내가 워커의 fetch 에 걸리지 않아 확인하지 못했다(등록 · 캐시 생성까지만).
3. 출력 언어 표시는 **마지막 `audio_start` 의 발화** 기준이다. back 이 다음 발화의 `audio_start` 를 앞 발화 재생이 끝나기 전에 보내면(TTS 가 실시간보다 빨리 올 때) 「〈언어〉로 출력 중」 이 앞 발화 재생 중에 다음 발화 언어로 바뀔 수 있다. 반이중(송신 0)에는 영향 없음 — 실발화 때 보고 필요하면 조각 단위로 고친다.
4. 「한국어 듣는 중」 · 「외국어 듣는 중」 은 **가장 최근 non-final caption 의 `side`** 로 정한다(§7.3 「열린 caption」).
5. 음량 배율(RMS × 6 → 최대 1.5배)은 기본값 — 가짜 마이크로는 1.03 정도. 실발화에서 너무 작거나 크면 숫자 하나만 고치면 된다(OQ-010).
6. 원형 front 의 비 PCM `format` 디코드 분기는 뺐다(§5.3 PCM 만).
7. 단위 시험 도구로 `vitest`(devDependency)를 넣었다 — `npm test`. Docker 이미지에는 안 들어간다(`.dockerignore`).
