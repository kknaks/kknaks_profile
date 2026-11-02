# [backend] 실물 e2e 1호 — `meeting_notes.json` 이 OpenAI 구조화 출력에서 400 · 저장소 바인드 마운트 · 회의 8 `/finalize` 실측

너는 **task-management `backend` 워커**다. 오늘 아침 사용자가 실제 회의(회의 id 8 · 12.4MB 녹음)를 앱에서 돌렸고 **AI 요약이 한 번도 안 나왔다.** 원인은 코디가 찾았다 — 네가 고치고 실물로 닫는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `5c72c25` = WORK-014). 도커 스택이 **떠 있다**(`make ps` — db · redis · api · worker · mcp 전부 healthy). api 는 `--reload` 라 `.py` 를 고치면 바로 재시작된다 — 지금은 회의가 끝났으니 괜찮다.

문서(읽기 전용) — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`
- `20-spec/spec-008-meeting-close.md §4` 「② 출력」 예시(payload 키) · 「② 검증」 표 ④(페이로드 참조 틀리면 그 키만 null) · ⑤(status done/cancelled 키 제거)
- `20-spec/spec-007-meeting-live.md §4` 「배치 출력」 · 검증 순서 4행(회의 중 payload 버림)
- `30-work/work-011-meeting-live.md` §Internal Interface(스키마 소유 = 011) · `work-012-meeting-close.md`(`_parse_output(fill_final=True)` · `_final_payload`)
- 실물 증거 예시 — `orchestration/work/docs-v1/work009-phase4-evidence.md`(워커 컨테이너에서 codex 를 직접 부른 방법)

## 1. 원인 (코디가 확인한 것)

워커 컨테이너의 codex 세션(`/root/.codex/sessions/2026/09/08/rollout-…01a07e57….jsonl`)에 배치 두 번 다 이 오류가 있다:

```
invalid_json_schema — Invalid schema for response_format 'codex_output_schema':
In context=('properties','agendas','items','properties','lines','items','properties','payload','type','0'),
'additionalProperties' is required to be supplied and to be false.
```

`app/back/ai_schemas/meeting_notes.json` 의 줄 `payload` 가 `{"type": ["object","null"]}` 뿐이다. OpenAI 구조화 출력(strict)은 **모든 object 에 `additionalProperties: false` 와 `properties` · 그 키 전부가 `required`** 여야 한다. 스키마의 다른 object 다섯은 이미 그렇다(코디가 훑었다) — `payload` 만 비어 있다. 웜스타트(스키마 없음)는 성공했고 resume 도 됐다. 그 뒤 모델 호출이 400 이라 codex 가 exit 1 · 빈 출력 → back 은 「워커 오류」로 `failed` 처리. **WORK-011 · 012 검수가 못 잡은 이유 = 밤새 실물 codex 호출이 없었다.**

## 2. 고칠 것 셋

### 2-1. `meeting_notes.json` — `payload` 를 strict 규격의 object 로 (스키마 한 벌은 그대로)
```
payload: {"type": ["object","null"], "additionalProperties": false, "properties": {…}, "required": [키 전부]}
키 = 액션 payload 일곱(ActionLinePayload: title · workTypeId · projectId · startDate · dueDate · description · todos)
   ∪ 업무 payload 일곱(TaskLinePayload/_TaskChange: dueDate · status · note · todos · relatedTaskIds · projectId · completionResult)
   = 11 키 · 전부 nullable(type: [X, "null"]) · strict 라 required 에 11 개 다 적는다
status enum ["todo","in_progress"] + null · todos/relatedTaskIds 는 array · 날짜는 string(format date 는 strict 에서 허용되면 쓰고 안 되면 pattern 없이 string)
```
- 회의 중(`fill_final=False`)은 지금처럼 **읽고 버린다** — 변화 없음.
- 최종(`_final_payload`)은 지금 규칙을 유지하되 **모양이 11키 union 이 됐으니 그 줄 kind 에 없는 키와 null 은 뗀다**(SPEC-008 ② 검증 표 ④ 「틀리면 그 키만 null」의 연장 — 새 결정 아님). 액션 줄에 `title` 이 null 이면 payload 자체를 null 로(액션 payload 는 title 필수).
- `_validator`(jsonschema) · 테스트 픽스처 · `static` needle 을 따라 고친다. **스키마 파일은 하나 · 둘째 파일 금지.**
- **strict 규격 전수 확인** — 파일 안 모든 object 가 `additionalProperties:false` + 전 키 required 인지 스크립트로 세고 테스트로 잠근다(다음 사람이 키 하나 더할 때 또 400 나지 않게).

### 2-2. 저장소 바인드 마운트 (사용자 요청 — 녹음 원본을 로컬에서 바로 보게)
```
docker-compose.local.yml api:   - storage:/data  →  - ${STORAGE_HOST_DIR:-storage}:/data
  (값이 경로면 바인드 · 비면 지금의 명명 볼륨 — volumes: storage 선언은 남긴다)
.env.example                    STORAGE_HOST_DIR 주석 한 줄(기본 비움 = 명명 볼륨)
로컬 .env                       STORAGE_HOST_DIR=/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-08-real-summit
```
그 폴더에 코디가 `recordings/8.bin`(회의 8 녹음 · webm)을 이미 넣어 두었다. `docker compose -f docker-compose.local.yml up -d --no-deps api` 로 api 만 재생성하고 `exec api ls /data/recordings` 에 `8.bin` 이 보이는지 확인. 볼륨의 옛 파일(1.bin · 3.bin)은 옮기지 않는다.

### 2-3. 회의 8 `/finalize` 실측 — **AI 요약이 실제로 나오는 것까지가 완료다**
```
회의 8 은 지금 generating · running(옛 job). api 재시작으로 그 job 은 죽고 기동 스윕(BE §5-3)이 failed 로 닫아 ended+failed 가 되거나, 옛 job 이 ② 3회 실패로 스스로 ended+failed 가 된다 — 어느 쪽이든 그 뒤 POST /api/meetings/8/finalize(세션 토큰은 앱이 쓰는 계정으로 — /api/auth 로 받아라)
① Soniox async 재전사(12.4MB · 실비) → ② codex 최종(스키마 고친 것) → merged 안건·줄 · ai_headline · term_corrections
증거 파일 — orchestration/work/docs-v1/e2e-01-real-summit-evidence.md: job 흐름(progress.phase 전환 · attempt) · 워커 로그(task.start/done · exit 0) · codex 세션의 task_complete(error 없음) · DB 결과(merged 안건 수 · 줄 수 · headline 원문 · termCorrections) · 회의 중 배치가 왜 0건이었는지 한 줄
② 가 또 실패하면 그 오류 원문을 증거 파일에 적고 §9 (2) 로 즉시 보고 — 스키마 밖 원인(모델 출력이 검증 ①~⑤ 에 걸림 등)은 결정이 필요할 수 있다
```

## 3. 하지 마라
- 스키마 밖으로 범위 넓히지 마라(프롬프트 문구 · 검증 규칙 변경 0). 프론트 금지.
- `except Exception` · 임의 재시도 0. 워커 컨테이너의 codex 세션 파일을 지우지 마라.
- 회의 8 의 사람 줄 · 안건 · 전사 행을 건드리지 마라.

## 4. allowed_paths
```
app/back/   docker-compose.local.yml   .env.example   .env(STORAGE_HOST_DIR 한 줄)
```

## 5. 검증
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1 && make test          # Errors 0
# strict 전수: 모든 object 에 additionalProperties=false + 전 키 required (테스트로도)
# 실물: 워커 컨테이너에서 codex 를 output_schema=meeting_notes.json 으로 한 번 직접 불러 400 이 사라진 것(work009-phase4-evidence.md 방식) → 그 다음 회의 8 /finalize
```

막히면 30분 넘기지 말고 §9 (2) 로 물어라.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 스키마 400 수정 · 바인드 마운트 · 회의 8 finalize 실측" \
  --body "고친 파일 / make test 수치 / codex 직접 호출 결과 / 회의 8 finalize 결과(merged 안건·줄 수 · headline) / 증거 파일 경로 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — 스키마 400 수정 · 회의 8 finalize. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
