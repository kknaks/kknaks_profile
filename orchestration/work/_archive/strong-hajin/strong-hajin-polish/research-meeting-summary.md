# 조사: 운영 회의 요약(종료 합성) 실패 — 2026-10-01

조사자: backend 워커(read-only). 운영 `strong-hajin-prod` 조회만 했고 쓰기·재시도·재시작은 하지 않았다.

## 0. 한 줄 원인

**회의 중 Codex 세션은 `back` 파드에서 열리고(웜스타트·배치), 종료 합성은 `worker-meeting` 파드에서 그 세션을 `codex exec resume <id>` 로 이어 가려 한다. 그런데 Codex 세션 파일(rollout)이 저장되는 `CODEX_HOME`(`/app/.scax/codex-runtime`)이 파드마다 따로인 컨테이너 로컬 디렉터리라서, worker-meeting 에는 그 세션이 없다. 그래서 codex 가 약 200ms 만에 0이 아닌 코드로 끝나고, 세 번의 시도가 모두 실패한다.**

STT(Soniox), 재전사, 녹음 파일, codex 인증, 바이너리, 네트워크는 원인이 아니다(§1-4).

## 1. 증거

### 1-1. worker-meeting 로그 (`kubectl logs deploy/worker-meeting --timestamps`)

```
2026-10-01T09:02:43.98+09:00 회의 ac0e419b-… 합성 시도 1/3 실패
2026-10-01T09:02:44.18+09:00 회의 ac0e419b-… 합성 시도 2/3 실패
2026-10-01T09:02:44.39+09:00 회의 ac0e419b-… 합성 시도 3/3 실패
2026-10-01T09:02:44.39+09:00 회의 ac0e419b-… 합성 실패: 회의록을 만들지 못했습니다 — 잠시 뒤 다시 시도해 주세요
2026-10-01T14:59:17.95+09:00 회의 df661b31-… 합성 시도 1/3 실패   (2/3, 3/3 도 각각 약 200ms 간격)
2026-10-01T15:27:38.97+09:00 회의 df661b31-… 합성 시도 1/3 실패   ← 사용자가 [다시 시도]를 눌렀고, 같은 방식으로 실패
```
매 시도의 traceback은 똑같다.
```
finalize_service.py:222 _attempt → self._agent.run_final(...)
bootstrap/application.py:491 run_final → provider.converse(...)
platform/codex_cli.py:233 converse → raise ProviderRequestFailed("Codex CLI conversation failed", provenance)
```
codex 프로세스의 returncode 가 0이 아니었다는 뜻이다(`codex_cli.py:232`). 시도 하나가 **약 200ms** 걸렸다. 모델 API까지 가지도 못하고 로컬에서 거부된 시간이다. codex stderr는 앱이 로그로 남기지 않아 정확한 문구는 볼 수 없다(§4).

### 1-2. DB 조회 (SELECT만)

| meeting | status | transcript_source | meeting_transcripts | batch_runs | meeting_ai_sessions.opened_at |
|---|---|---|---|---|---|
| ac0e419b (09:02, 36초 회의) | failed | **final** | 2 | 0 | 00:02:15Z |
| df661b31 (14:15) | failed | **final** | 450 | **24회 모두 succeeded** (05:17Z~05:58Z) | 05:15:28Z |
| 6ab04166 (14:00 Ax KPI 설정 회의) | cancelled | – | – | – | – (예약만 있던 회의, 06:26Z 취소. 이 장애와는 관계없다) |

- `transcript_source = final` 이다. **재전사(Soniox 재청취)는 성공했다.** 실패했다면 `retranscribe.py:48-53` 의 다른 사유가 남았을 것이다.
- 배치 24회가 성공했다. **같은 codex·같은 인증·같은 세션이 back 파드에서는 동작했다.**
- `failure_reason` 이 `FAILURE_UNFINISHED` 다. 일반 예외에서 나오는 사유다(`finalize_service.py:74`).

### 1-3. 파드 안 Codex 런타임 홈 (`ls`/`find` 조회만)

```
== back            cwd=/app
.scax/codex-runtime/sessions/2026/10/01/rollout-2026-10-01T00-02-08-<ac0e419b의 세션 id>.jsonl
.scax/codex-runtime/sessions/2026/10/01/rollout-2026-10-01T05-15-22-<df661b31의 세션 id>.jsonl
models_cache.json 있음
== worker-meeting  cwd=/app
find: '.scax/codex-runtime/sessions': No such file or directory
models_cache.json 없음 (codex 가 모델 API에 한 번도 닿지 않았다)
```
DB의 `meeting_ai_sessions.provider_session_ref` 두 개가 back 파드의 rollout 파일 이름과 정확히 같다.

### 1-4. 배포 구성 (`kubectl get deploy -o json`, 값은 출력하지 않음)

- back, worker-meeting, worker-conversation 이 모두 PVC `codex-home` 을 **`/root/.codex`** 에 마운트한다. 인증(`auth.json`)은 이 공유 볼륨에서 온다. 그래서 인증은 정상이다.
- 앱의 실제 `CODEX_HOME` 은 `/root/.codex` 가 아니다. 상대경로 **`.scax/codex-runtime` → `/app/.scax/codex-runtime`** 이고, 어떤 볼륨에도 마운트되어 있지 않다. 즉 파드마다 따로이고, 파드를 재시작하면 사라진다.
- configmap에는 이 경로를 바꾸는 키가 없다. 코드에도 설정으로 받는 자리가 없다(아래 2).

## 2. 실패 경로

1. `/start` → `bootstrap/application.py:1688`/`1722`/`3672`/`3778` `launch_warm_start` → `MeetingBatchService.warm_start` (`modules/meetings/batch_service.py:159-172`). **API 프로세스(back 파드)** 의 스레드에서 codex 새 세션을 열고 `meeting_ai_sessions` 에 기록한다(`modules/meetings/application.py:1440-1441`).
2. 회의 중 배치 `meeting_batch.schedule` (`application.py:639`, `1833`, `3872`)도 back 파드에서 `codex exec resume` 을 한다. 같은 파드의 rollout 이 있으니 성공한다.
3. 종료 → `_enqueue_finalize` (`application.py:2015`) → durable job → **worker-meeting 파드** `bootstrap/meeting_worker.py:100` `finalize_meeting` → `MeetingFinalizeService._run_once` (`finalize_service.py:135`).
4. ① 재전사는 성공한다(`transcript_source=final`).
5. ② `_attempt` (`finalize_service.py:202-222`): DB의 `session_ref`(`application.py:1476`)가 있으니 콜드 스타트가 아니다. `run_final` → `codex_cli.py:267-312` `_conversation_arguments` 가 `exec resume <session_ref>` 를 만든다.
6. `CODEX_HOME` 이 `prepare_isolated_codex_home(self._profile.runtime_home)` (`codex_cli.py:771`) 즉 `CodexCliProfile.runtime_home = Path(".scax/codex-runtime")` (`codex_cli.py:89`)이다. worker-meeting 의 이 디렉터리에는 그 세션 rollout 이 없다 → codex 가 즉시 비정상 종료한다 → `ProviderRequestFailed` (`codex_cli.py:233`).
7. `_run_once` 가 3회까지 다시 시도한다(`FINAL_ATTEMPTS = 3`, `finalize.py`). 세션이 계속 없으니 결과도 매번 같다. 그 뒤 `commit_failure(FAILURE_UNFINISHED)` (`finalize_service.py:169`) → 화면에 「실패」가 뜬다.
8. resume이 실패했을 때 콜드 스타트로 넘어가는 경로가 없다. 그래서 [다시 시도]도 같은 이유로 실패한다(15:27 로그).

**로컬(`make local-stack`)에서 드러나지 않은 이유(추정):** API와 meeting worker 가 같은 머신의 같은 cwd 에서 돌아 `.scax/codex-runtime` 을 함께 쓴다. 파드가 갈리는 k8s 에서만 깨진다.

## 3. 고칠 자리 후보 (위치만)

**인프라·배포**
- `deploy/back`·`deploy/worker-meeting`(그리고 같은 패턴인 worker-conversation, worker-report)의 볼륨: `/app/.scax/codex-runtime` 을 파드 사이에 공유하는 영속 볼륨이 없다. 이 런타임 홈은 `/root/.codex` PVC와 별개다.

**코드**
- `backend/src/ax_workspace/platform/codex_cli.py:89` `CodexCliProfile.runtime_home`: 상대경로로 고정되어 있고 설정(`Settings`/환경변수)으로 받는 자리가 없다. 프로파일을 조립하는 곳(`bootstrap/application.py` `_AI_PROVIDER_FACTORIES`, 약 `:4554`)도 같다.
- `backend/src/ax_workspace/modules/meetings/finalize_service.py:202-222` `_attempt`: resume 실패를 콜드 스타트로 되받는 경로가 없다.
- `backend/src/ax_workspace/platform/codex_cli.py:232-233`: returncode 가 0이 아닐 때 codex stderr 를 버린다. 운영에서 원인 문구가 남지 않는다(이번 조사의 한계와 같은 자리).
- 세션을 여는 프로세스(back, `batch_service.py:159-172`)와 이어 쓰는 프로세스(worker-meeting, `meeting_worker.py:100`)가 다르다는 전제 자체도 위치 후보다.

**운영 조치(사람 결정)**
- 실패한 두 회의(ac0e419b, df661b31)는 원문(재전사본)이 DB에 남아 있다. 위 문제가 고쳐지기 전에는 [다시 시도]를 눌러도 같은 이유로 실패한다.
- 같은 위험: back 파드가 재시작하면 back 쪽 rollout 도 사라진다. 진행 중인 회의의 배치 resume 도 같은 방식으로 깨질 수 있다.

## 4. 조사 한계

- codex의 실제 stderr 문구(예: "no saved session" 계열)는 확인하지 못했다. 앱이 stderr 를 남기지 않고, worker-meeting 의 codex `logs_2.sqlite` 는 비어 있다(0행). 운영에서 codex 를 직접 실행하는 것은 금지 범위라 재현하지 않았다. 원인 판정은 ① 세션 파일이 없음 ② 약 200ms 의 즉시 실패 ③ 같은 세션이 back 에서는 성공 ④ `models_cache.json` 이 없음(API 미도달), 이 네 정황으로 했다.
- 노드 codex 버전은 `/opt/codex/bin/codex` 에 있다(runbook §6: 0.146). 버전 차이(`exec resume` 인자 호환)가 함께 작용했을 가능성은 배제하지 못했다. 다만 같은 바이너리와 같은 인자로 back 의 배치 resume 이 24회 성공했으므로 주원인은 아니다.
- worker-report, worker-conversation 이 같은 구조 때문에 실패한 적이 있는지는 보지 않았다.
- 배포된 이미지의 커밋과 이 워크트리 코드가 같다는 것은 traceback 줄 번호(`codex_cli.py:233`, `finalize_service.py:154/222`, `application.py:491`)가 일치하는 것으로만 확인했다.
