# [backend] WORK-001 WP2 — 통역 중계 WS · Soniox STT/TTS · 실물 호출 확인 4건

너는 **cc-prototype `backend` 워커**다. WP1 을 한 같은 워커라면 맥락이 있다. 없으면 역할 문서와 아래부터:
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/backend/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` · ⚠ frontend 워커가 `cc/front/` 에서 통역 모달(WP4) 작업 중 — 건드리지 마라.

## 1. SSOT

- SPEC-001 §7: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- **WS 계약(정본 — front 가 이대로 만들고 있다)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/interpret-ws-contract.md`
- Soniox 조사: 같은 폴더 `research-soniox-report.md`(엔드포인트 · 설정 메시지 · 공식 FastAPI 중계 데모) · `research-soniox-chinese-report.md`(zh · 번체 · 음색 미확인 4건)
- Soniox 공식 문서: `https://soniox.com/docs/llms.txt` 에서 필요한 페이지(실시간 STT · translation two_way · TTS websocket) — 리포트와 다르면 **공식 문서가 맞다**
- 앞 판: `wp1-be-report.md`

## 2. 할 것

1. **실물 호출 확인 먼저(SPEC §7.3)** — `cc/back/.env` 에 `SONIOX_API_KEY` 가 들어 있다(코디가 넣음, **값을 출력 · 로그 · 리포트에 쓰지 마라**). 짧은 스크립트로 1회씩: ① `zh` STT · 번역 결과가 간체/번체 ② 광둥어 발화가 `zh` 로 잡혀 two_way 번역되는지(광둥어 음성 샘플이 없으면 TTS 로 만든 음성 · 공개 샘플로 시도하고 못 하면 pending) ③ 번체를 TTS 에 넣으면 어떻게 되나 ④ tts-rt-v2 음색 목록 · 출력 형식(PCM · 샘플레이트). 결과로 SPEC §7.2 번체 변환 · 음색 · `audio_start.sampleRate` 를 정한다
2. `WS /api/interpret` — 계약 그대로. Soniox STT(stt-rt-v5, translation `two_way` ko ↔ lang) 연결 · 클라 PCM 중계 · 토큰을 발화 단위 `caption` 으로 묶기(원문 언어로 `side`) · 확정 발화의 번역문을 Soniox TTS 로 → `audio_start` · PCM 바이너리 · `audio_end`. `traditional:true` 면 자막(원문 · 번역의 중국어)만 번체로(OpenCC 류 패키지). TTS 에는 간체
3. 오류: 키 없음 → `no_api_key` · Soniox 연결 실패 → `soniox_unavailable` · 잘못된 start → `bad_request`. 클라 close · stop 때 Soniox 연결 정리(새는 연결 없게 — TTS 동시 한도 3)
4. `cc/back/README.md` 에 통역 확인 방법 한 단락

## 3. 범위 제약

- `cc/back/` 만. 계약 모양을 바꿔야 하면 `[질문]`(front 가 병렬로 쓴다)
- KOS 호출 금지. API 키 출력 금지. 실물 호출은 확인에 필요한 만큼만(짧게)
- 서버 확인은 임시 포트, 끝나면 그 프로세스만 종료. 사용자 포트(8600 · 3600) · 프로세스 금지. 커밋 · push · PR 금지

## 4. 검증

```
cc/back 에서 uv run pytest · uv run ruff check . — 각 1회. 기능 폴더 밖 import 없음. 사용자 포트·프로세스 안 건드림. 실행 못 한 검증은 사유와 함께 pending
```

- 이번 WP 항목만: 실물 호출 4건 결과 · 임시 서버에 WS 클라이언트(스크립트)로 TTS 로 만든 한국어 음성 PCM 을 보내 `caption`(final) · `audio_start`/바이너리/`audio_end` 를 실제로 받는 것 1회 · 단위 시험(발화 묶기 · side · 번체 변환 · 오류 코드)
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp2-be-report.md` — §7.3 4건 결과 표 포함

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_eb0f5374-235a-4757-bb3a-1b2768c7e255 \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] backend: <질문>" --enter`
