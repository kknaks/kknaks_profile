# 실물 e2e 1호 — `meeting_notes.json` 이 OpenAI 구조화 출력에서 400 나던 것

**결론: 고쳤고, 실물로 닫혔다.** 합성 호출이 아니라 **사용자가 지금 돌리는 회의(id 9)의 배치가 성공**했다.

## 1. 원인 — 줄 `payload` 한 자리

```
invalid_json_schema — In context=('properties','agendas','items','properties','lines','items',
'properties','payload','type','0'), 'additionalProperties' is required to be supplied and to be false.
```

`payload` 가 `{"type": ["object","null"]}` 뿐이었다. OpenAI 구조화 출력(strict)은 **모든 object 에
`additionalProperties: false` + `properties` 의 키가 전부 `required`** 여야 한다. 스키마의 다른 object 다섯은
이미 그랬고 `payload` 만 비어 있었다. 400 이면 codex 는 **빈 출력으로 exit 1** 하고, back 에는 「워커 오류」로만 보인다.

## 2. 고친 것

- `payload` 를 strict 규격 object 로 — **열한 키**(액션 생성분 일곱 ∪ 업무 변경분 일곱) · 전부 nullable · `required` 에 열하나 다.
  strict 는 「선택 키」를 허용하지 않는다 → **선택은 `required` 에서 빼는 대신 nullable 로 두고 null 을 보낸다**.
- `status` enum 은 **넷 + null**(`todo`·`in_progress`·`done`·`cancelled`). 코디 결정(B) — SPEC-008 §4 ② 검증 ⑤
  「`done`·`cancelled` 면 그 키만 뗀다 · 줄도 시도도 산다」가 정본이고, 좁히면 모델이 종결 상태를 낼 때 배치 전체가
  폐기돼 `final_failed` 가 된다. 사람 표면의 422(MF-59)는 `schemas/meeting.py` 의 `PayloadStatus` 그대로다.
- `_final_payload` — 스키마가 합집합이 됐으니 **그 줄 종류의 키만** 남긴다(저장 모양은 여전히 둘 · M-14-a).
  액션은 `title` 이 null 이면 payload 자체가 null · `todos` 는 `null → []`. 업무는 값이 있는 키만(빈 배열도 뺀다).
- 테스트 둘로 잠갔다 — 파일 전체를 훑어 **모든 object 의 strict 규격**을 세는 것(object 6개), 그리고
  **열한 키 = 프론트 계약 두 벌의 합집합**인지 대조하는 것. 다음 사람이 키를 더할 때 또 400 나지 않게.

## 3. 실물 확인 — 워커 로그가 갈린다

같은 스택 · 같은 워커 컨테이너에서 **고치기 전후**가 이렇게 나뉜다.

```
# 고치기 전 (회의 8 — 배치 · 최종 전부)
00:13:26 task.failed  error='Process exited with code 1 (empty output)' exit_code=1
00:13:33 task.failed  error='Process exited with code 1 (empty output)' exit_code=1
00:15:29 task.failed  ...  (최종 회의록 ② — 3회 시도 전부)
00:15:38 task.failed  ...

# 고친 뒤 (회의 9 — 사용자가 지금 돌리는 실물)
00:26:28 task.start   (웜스타트)      → 00:26:35 task.done exit_code=0
00:29:11 task.start   (회의 중 배치)  → 00:29:49 task.done exit_code=0   ← 400 이 사라졌다
00:30:04 task.start   (다음 배치)     → 진행 중
```

DB 도 같은 말을 한다(읽기 전용 조회).

```
 id | status    | integration_state | ai 안건 | ai 줄 | 성공 배치 | 실패 배치
  8 | ended     | failed            |   0    |   0   |    0     |   16     ← 고치기 전 회의(손대지 않았다)
  9 | recording | not_started       |   1    |   3   |    1     |    0     ← 고친 뒤 · AI 요약이 실제로 쌓인다
```

**워커 컨테이너가 보는 파일**(`/app/ai_schemas/meeting_notes.json`, ro 마운트)로도 확인했다 —
object 6개 전부 strict 통과 · `payload.additionalProperties=false` · 키 11 · `status` enum 넷+null.

> 브리프 §5 의 「워커에서 codex 직접 호출」은 **하지 않았다** — 확인하려던 그 경로를 사용자의 실제 회의가
> 지금 지나고 있고(위 exit 0), 같은 컨테이너에서 codex 를 하나 더 띄우면 실물 회의에 끼어든다.
> 합성 호출보다 이쪽이 강한 증거다.

## 4. 회의 중 배치가 왜 0건이었나 (회의 8)

배치는 **돌았다**(16회). 매번 codex 가 400 으로 exit 1 → 빈 출력 → 검증 전에 실패 → `meeting_batch_run` 이
실패로만 쌓이고 `track='ai'` 행은 하나도 안 생겼다(M-7 — 검증을 통과해야 지우고 넣는다). 그래서 화면에 AI 요약이
한 번도 안 떴고, 종료 뒤 ② 도 같은 이유로 3회 실패해 `ended`+`failed` 가 됐다.

## 5. 저장소 바인드 마운트 — 코드는 됐고 **아직 반영 전이다**

- `docker-compose.local.yml` api: `- ${STORAGE_HOST_DIR:-storage}:/data` (값이 비면 지금까지의 명명 볼륨 · `volumes: storage` 선언 유지)
- `.env.example` 에 주석 한 줄 · 로컬 `.env` 에 `STORAGE_HOST_DIR=…/reference/2026-09-08-real-summit`
- **api 재생성은 하지 않았다**(실물 회의 중 · 코디 지시). 지금 `/data` 는 여전히 명명 볼륨이다.

> ⚠ **재생성 순서 주의.** 회의 9 의 녹음은 **명명 볼륨**의 `/data/recordings/9.bin` 에 쌓이고 있다.
> 회의 9 를 `/finalize`(① 재전사가 그 파일을 읽는다) 하기 **전에** api 를 바인드 마운트로 재생성하면
> 그 파일이 안 보여 `transcription_failed` 가 난다. 재생성은 **회의 9 종료 파이프라인이 끝난 뒤**에 하거나,
> 먼저 볼륨의 `9.bin`(과 필요하면 `8.bin`)을 호스트 폴더로 복사한 뒤에 해야 한다.

## 6. 남는 것

- **회의 8 `/finalize` 실측** — 코디 지시로 하지 않았다(사용자가 앱에서 직접 돌린다). 회의 8 의 줄·안건·전사·상태는 건드리지 않았다.
- 이 문서의 §3 은 회의 9 가 도는 도중의 값이다 — 종료 파이프라인(① 재전사 → ② 최종)까지 지난 결과는 그 뒤에 덧붙이면 된다.
