# [frontend] WORK-001 WP4 — 통역 모달

너는 **cc-prototype `frontend` 워커**다. WP3 를 한 같은 워커라면 맥락이 있다. 없으면 역할 문서와 아래부터:
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/roles/cc-prototype/frontend/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype` · ⚠ backend 워커가 `cc/back/` 에서 작업 중 — 건드리지 마라.

## 1. SSOT

- SPEC-001 §7 · §2: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/para/projects/summer-star/cc-prototype/20-spec/spec-001-cc-poc.md`
- **WS 계약(정본)**: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/interpret-ws-contract.md` — back(WP2)이 이대로 만든다
- 시안: claude design `dda9a931-…` 의 `Ceramique 직원 - 의사`(모달) · `Ceramique 직원 - 통역 모달 상태`(연결 중 · 듣는 중 · 멈춤 · 오류) — DesignSync
- 앞 판: `wp3-fe-report.md` (같은 work 폴더)

## 2. 할 것

1. 환자 상세 [통역] → 통역 모달(폰 = 아래에서 올라오는 시트 · 넓은 화면 = 가운데 창, 시안대로). KR 국적이면 [통역] 숨김(이미 돼 있으면 그대로)
2. 언어: 환자 국적 → SPEC §7.2 표로 기본값, 모달 상단에서 8개 중 변경 → WS 다시 연결. TW · HK 는 `traditional:true`
3. 마이크: `getUserMedia` → AudioWorklet 으로 16kHz mono PCM s16le 로 바꿔 바이너리 전송. 모달 열기 = 연결 · 듣기 시작, [멈춤]/[다시] = `pause`/`resume` + 마이크 트랙 멈춤, [닫기] = `stop` + 정리(트랙 · AudioContext · WS 모두)
4. 자막: `caption` 을 `id` 로 갱신 — 메신저형(`them` 왼쪽 · `me` 오른쪽, 원문 크게 + 번역 작게, 미확정은 흐리게). 새 말풍선이 오면 아래로 스크롤
5. 음성: `audio_start` → 바이너리 PCM 조각을 이어서 재생(Web Audio, 끊김 없이 큐) → `audio_end`. 재생 중엔 자기 소리가 다시 들어가지 않게 `echoCancellation: true`
6. 상태 4종(시안): 연결 중 · 듣는 중 · 멈춤 · 오류(마이크 거부 · `error` 메시지 · WS 끊김)
7. back 주소: WS 는 `NEXT_PUBLIC_API_BASE_URL` 에서 `http→ws` 로

## 3. 범위 제약

- `cc/front/` 만. 계약 모양을 바꾸지 마라(이상하면 `[질문]`)
- back WS 가 아직 없을 수 있다 — 계약대로 응답하는 **임시 목업 WS 서버**(임시 포트, 확인 후 종료)로 자막 · 음성 재생 흐름을 확인. 목업 파일은 남기지 마라(또는 `cc/front/scripts/` 아래 dev 전용으로 남기고 README 에 적기)
- 사용자 포트(3600 · 8600) · 프로세스 금지. 커밋 · push · PR 금지

## 4. 검증

```
cc/front 에서 npx tsc --noEmit · npm run lint · npm run build — 각 1회. 기능 폴더 밖 import 없음. 사용자 포트·프로세스 안 건드림. 실행 못 한 검증은 사유와 함께 pending
```

- 이번 WP 항목만(실제 Soniox · 마이크 통합은 WP5). 목업 WS 로 caption 갱신 · audio 재생 · 상태 전환 확인
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-prototype/orchestration/work/sts-prototype/wp4-fe-report.md`

## 5. 완료 보고 — **문구 변경 금지**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --from term_1bd4c892-2253-4670-9a5f-c6412cf15a9d \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_57b54cef-8b6c-44fe-ad1f-d2cf875755dc --text "[질문] frontend: <질문>" --enter`
