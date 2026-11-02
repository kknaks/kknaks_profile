# 리뷰 리포트 — strong-hajin-polish / Phase 4 회의 요약 실패 (backend + infra) (2026-10-01)

## 판정: WARN

**FAIL 0 · WARN 4 · 참고 3.**
- 코드 계약 1~3과 인프라 계약은 모두 섰다. 콜드스타트는 「같은 결과물」이고, 재시도를 낭비하지 않는다. 콜드스타트까지 실패하면 이전과 같은 실패 상태로 끝난다.
- 공유 홈은 **방향이 맞다.**
  - 다섯 파드가 같은 VM 커널(lima-worker-1) 위에서 돌고, codex는 원래 한 `CODEX_HOME`을 여러 프로세스가 함께 쓰는 도구다.
  - 다만 세 가지는 보고 들어가야 한다. ① virtiofs 위 sqlite WAL은 증명되지 않았다. ② 「재시작이 고쳐 주던」 상태 오염이 이제 영속된다. ③ 세션 파일과 sqlite 로그에 정리 정책이 없다.
  - 권장: 이번에는 이대로 반영한다. 운영 반영 직후 sqlite 오류를 로그에서 보고, 대안 B(아래 §2-4)를 다음 단계로 준비해 둔다.

## 검수 범위
- 코드: `strong-hajin-polish` HEAD `8700bd0` 위 미커밋 10파일(backend 9 + `delivery/README.md`). 다른 경로의 변경은 0이다.
- 인프라: `strong-hajin-polish-infra`(base `7ba1050`) 미커밋 4파일. 모두 `charts/strong-hajin/` 안이다.
- 기준: WP Phase 4 · `research-meeting-summary.md` · `_RESUME.md` §2(10-01 「뒤집음」 결정) · `strong-hajin-polish-be-p4-brief.md` · `strong-hajin-polish-infra-brief.md`
- 실행한 검사
  - diff 정독
  - 호출 경로 추적: `finalize_service` → `_CodexFinalizeAgent` → `codex_cli.converse`
  - `helm lint`(prod): 0 failed
  - `helm template`(prod): 다섯 deployment를 Python으로 발췌(§3)
  - `make test-unit`: **392 passed**
  - `make test-contract`: 1135 + 128 passed(§6)
  - codex가 `CODEX_HOME`에 쓰는 것: 이 Mac의 `~/.codex`에서 **이름만** 나열해 확인(codex-cli 0.159.3). 운영 노드는 0.146이다
- 하지 않은 것: 클러스터 · 서버 접근, codex 실행, dev 차트 렌더(`values-dev`는 registry가 비어 있어 차트가 일부러 렌더를 거부한다)

## 1. 계약 대조

| 계약 | 결과 | 근거 |
|---|---|---|
| 1 resume 실패 → 콜드스타트 | PASS | `codex_cli.py:240-245` returncode≠0 **이고** 런타임 홈에 그 세션 rollout이 없으면 `ProviderSessionUnavailable`(`ai.py:176`, `ProviderRequestFailed`의 하위 클래스라 다른 호출자의 동작은 그대로다) → `application.py:508-511` `FinalizeSessionLost` → `finalize_service.py:217-227` **같은 시도 안에서** `_compose(session_ref=None)` |
| 「같은 결과물」 | PASS | 콜드스타트는 원래 있던 경로를 그대로 쓴다(`_compose` · `build_final_prompt(transcript=…)`, `finalize.py:384-386` 「확정 발화 전량」). `finalize_input`은 세션 유무와 상관없이 언제나 `transcript` 전량(재전사 뒤 원문)을 싣는다(`meetings/application.py:830-833`). 출력 스키마(`FINAL_OUTPUT_SCHEMA`) · 검증(`finalize_notes`) · 적재(`commit_success`)도 같다 |
| 재시도 낭비 없음 | PASS | 세션이 없는 것은 시도를 쓰지 않는다. `source["session_ref"] = None`(`:226`)이라 남은 시도도 콜드로 간다. 테스트 `test_a_lost_session_does_not_spend_retries_on_the_same_resume` |
| 콜드도 실패 → 기존 상태 | PASS | 콜드 실패는 일반 예외라 `_run_once`의 3회 루프를 탄다. 그 뒤 `commit_failure(last_reason or FAILURE_UNFINISHED)`로 지금과 같은 사유가 남는다. 테스트 `test_cold_start_that_also_fails_settles_the_same_failure_as_before` |
| 「세션 있음 + 다른 실패」는 일반 실패 | PASS | `_session_on_disk`가 참이면 `ProviderRequestFailed` 그대로다. 테스트 `test_a_resume_that_fails_with_the_session_present_is_an_ordinary_failure` |
| 2 런타임 홈 env | PASS | `settings.py` `SCAX_CODEX_RUNTIME_HOME` → `codex_runtime_home`(기본 `.scax/codex-runtime`, 지금과 같다) → `create_codex_cli_provider`(`application.py:4543`). 빈 문자열이면 기본값(`or`). 테스트 `test_runtime_home_comes_from_settings_and_defaults_to_the_old_path` |
| 3 stderr 요약 로그 | PASS(남는 위험은 WARN-3) | `cli_process.py:74-103` `summarize_stderr`(마스킹 → 600자 꼬리 자르기 순서) · `codex_cli.py:784-791` `_log_failure`. generation과 conversation 두 실패 자리 모두에 붙었다 |
| 4 resume 쓰는 곳 전수 | PASS(보고) | §4 |
| WP 문면 | **WARN-4** | §5 |

## 2. 공유 홈의 동시성 (핵심)

### 2-1. codex가 `CODEX_HOME`에 쓰는 것 (근거)
- 이 Mac `~/.codex`(0.159.3)의 이름 나열
  - `sessions/YYYY/MM/DD/rollout-*.jsonl`
  - **`state_5.sqlite` + `-wal` + `-shm`**(WAL 모드)
  - **`logs_2.sqlite`**(로컬 147MB)
  - `goals_1` · `memories_1` · `queue_1` · `thread_history_1.sqlite`
  - `session_index.jsonl` · `history.jsonl` · `models_cache.json` · `installation_id` · `shell_snapshots/` · `.tmp/` · `log/` · `cache/` · `skills/` 등
- 운영 런타임 홈에서도 같은 계열을 봤다: `logs_2.sqlite` · `models_cache.json` · `sessions/`(조사 §1-3 · §4)
- 0.146에 정확히 어떤 sqlite가 생기는지는 운영에서 보지 않았다. 버전마다 파일 번호가 갈린다.
- 앱의 격리 검사(`prepare_isolated_codex_home`)는 `AGENTS.md` · `config.toml` · `skills/.system` 밖의 skills만 막는다. 위 파일들은 정상 산출물이다.

### 2-2. 여러 파드가 같은 디렉터리를 동시에 쓸 때
| 자리 | 판단 | 근거 |
|---|---|---|
| rollout(세션당 파일 하나) | **안전** — 단, 같은 세션을 동시에 이어 쓰는 경우는 예외(아래 WARN-2) | 세션마다 파일이 갈리고, 이어 쓰는 쪽만 덧붙인다 |
| sqlite(state · logs 등) 동시 쓰기 | **같은 커널 안이라 원리상 성립한다. 다만 virtiofs 위에서 증명되지 않았다(WARN-1)** | 다섯 파드는 모두 `lima-worker-1` 한 VM 커널 위에 있다(렌더 §3 nodeSelector). 그래서 「네트워크 FS 위 여러 호스트」라는 SQLite의 금기 조건과는 다르다. fcntl 잠금과 `-shm` mmap은 같은 게스트 커널의 페이지 캐시 · 잠금 테이블에서 조정된다. 그리고 codex는 원래 한 `CODEX_HOME`에서 여러 프로세스(터미널 여럿)가 함께 쓰는 도구다. 지금까지도 back 파드 하나 안에서 배치 · 웜스타트 스레드가 동시에 codex를 띄웠다. **새 변수는 「여러 프로세스」가 아니라 「virtiofs」다.** `/mnt/mac`은 `vmType: vz`이고 mountType을 지정하지 않았다(`lima/worker-1.yaml:4,35-38`). Lima 기본값으로는 virtiofs(Apple Virtualization)다. 이 FS가 FUSE 잠금을 넘기는지, 게스트 커널 로컬 잠금으로 떨어지는지는 이 저장소에서 확인할 수 없다 |
| `auth.json` symlink 경합 | **닫혔다** | `codex_cli.py:825-831`: 동시 `symlink_to`가 `FileExistsError`를 내면 대상이 같은지만 보고 넘어간다. 대상 `/root/.codex/auth.json`은 다섯 파드가 같은 PVC `codex-home`을 같은 경로에 마운트한 것이다(렌더 §3). 그래서 공유 디렉터리의 symlink 하나가 모든 파드에서 같은 파일로 풀린다. 테스트 `test_a_shared_runtime_home_tolerates_another_process_linking_auth_first` |
| `mkdir(mode=0o700)` | 안전 | `exist_ok=True`. hostPath는 type `Directory`라 노드에 디렉터리가 미리 있어야 한다(§7) |

### 2-3. 공유 · 영속이 새로 만든 위험
- **WARN-1 virtiofs 위 sqlite WAL — 증명되지 않음**
  - 위 근거대로 원리상은 성립한다. 하지만 macOS 호스트 공유(virtiofs) 위의 SQLite WAL은 잠금 · mmap 일관성 문제가 보고되는 영역이다.
  - 깨지면 이렇게 보인다
    - codex가 `database is locked` 또는 `disk I/O error`로 종료한다. stderr가 이제 로그에 남으므로(계약 3) 바로 보인다.
    - 최악은 `state_5.sqlite`가 깨져 모든 파드의 codex가 실패하는 것이다.
  - 이 저장소에서 검증할 길은 없다(클러스터 · codex 실행 금지). **운영 반영 직후 확인 항목**으로 둔다(§7).
- **WARN-2 같은 세션을 두 파드가 동시에 이어 쓸 수 있다(새로 열린 경로)**
  - 배치와 합성의 상호 배제는 **프로세스 안 `threading.Lock`**(`batch_service.py:132` `_lock_for`, `application.py:970`이 합성에 넘김)뿐이다.
  - back의 마지막 배치가 아직 도는 중에 worker-meeting 합성이 같은 세션을 `exec resume`하면, 두 codex가 같은 rollout에 덧붙인다.
  - 예전에는 홈이 갈라져 있어 이 경로가 불가능했다(합성이 그냥 실패했다).
  - 실제 확률은 낮다. 합성 앞에 재전사(음원 전체 재청취)가 있어 보통 그 사이에 배치가 끝난다. 합성은 자기 메모리의 이력으로 답하므로 결과물은 성립한다. 그 뒤로 그 세션을 이어 쓰는 일도 없다.
  - 그래도 「배치가 도는 중이면 기다린다」(`finalize_service.py:135` docstring)는 이제 파드를 넘어서는 지켜지지 않는다. 고친다면 DB 수준 표식이 필요하다(코디 판단).
- **참고 R-1 재시작이 고쳐 주던 오염이 이제 영속된다**
  - 예전에는 런타임 홈이 파드 로컬이라 재시작하면 깨끗해졌다.
  - 이제는 다음 일이 한 번 생기면 **다섯 파드가 재시작해도 계속 막힌다.** 사람이 노드 디렉터리에서 그 파일을 지워야 한다.
    - 금지 파일(`config.toml` · 모르는 `skills/*`)이 생기는 경우: 예를 들어 codex 버전을 올렸는데 새 버전이 skills 아래에 다른 것을 만들면 `prepare_isolated_codex_home`이 `ProviderUnavailable`을 낸다.
    - `auth.json` symlink가 일반 파일로 바뀌는 경우: codex가 rename으로 저장하는 버전이면 그렇다.
  - 런북에 「AX 전부 실패 + `isolated Codex runtime …` 로그 → 공유 홈 점검」 한 줄을 권한다.
- **WARN-3 (공유 홈 · stderr 공통) 정리 정책이 없다**
  - 세션 rollout · `logs_2.sqlite`가 Mac 디스크에 무기한 쌓인다(로컬 개인 사용만으로 `logs_2.sqlite`가 147MB였다).
  - 대화 · 회의 · 보고서 세션이 다섯 파드에서 모두 쌓인다. 보존 기간(예: 회의 종료 N일 뒤, 대화 마지막 turn N일 뒤)이나 주기 정리가 필요하다. **이번 범위 밖으로 기록만** 한다.

### 2-4. 대안 (근거와 함께)
| 안 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **A(지금)** 홈 전체 공유 | `/app/.scax/codex-runtime` = hostPath | 단순하다. 세션 · 인덱스 · state가 한 벌이라 resume 조회 경로가 무엇이든 성립한다 | WARN-1 · R-1 · WARN-3 |
| **B** 파드별 홈 + `sessions/`만 공유 | 홈은 파드 로컬(또는 파드별 하위 디렉터리)로 두고, `…/codex-runtime/sessions`만 hostPath subPath로 공유 | sqlite를 공유하지 않아 WARN-1이 사라진다. 오염도 파드 로컬이라 R-1이 줄어든다 | codex resume이 **id → rollout 경로**를 `sessions/` 스캔으로 찾는지, `state_*.sqlite` · `session_index.jsonl` 인덱스에 기대는지 **0.146에서 확인해야 한다.** 인덱스에만 기댄다면 B는 resume을 되살리지 못한다. 앱의 `_session_on_disk`는 파일 스캔이라 「있음」으로 보는데 codex는 「없음」으로 실패하고, 이 경우 콜드스타트도 일어나지 않는다(일반 실패 3회) |
| C 현 상태 + 콜드스타트만 | 공유 없음 | 동시성 위험 0 | 회의 배치 · 대화 turn은 재시작 · 배포 때마다 세션을 잃는다(§4). 사용자 결정(10-01)과 어긋난다 |

**결론**: A로 반영한다. 반영 직후 §7의 sqlite 오류 확인에서 문제가 보이면 B로 옮긴다. B로 가기 전에 「0.146 `exec resume <id>`가 인덱스 없이 rollout 스캔으로 찾는가」를 운영 밖(로컬 0.146)에서 먼저 확인한다. 이 결론은 코디 · 사용자 판단으로 넘긴다.

## 3. 인프라

`helm template … -f values-prod.yaml -n strong-hajin-prod` 발췌:

| deployment | nodeSelector | codex-runtime mount | volume | codex-home |
|---|---|---|---|---|
| back | `lima-worker-1` | `/app/.scax/codex-runtime` | hostPath `/mnt/mac/strong-hajin/codex-runtime`, type `Directory` | PVC `codex-home` → `/root/.codex`(불변) |
| worker-conversation | 〃 | 〃 | 〃 | 〃 |
| worker-material | 〃 | 〃 | 〃 | 〃 |
| worker-meeting | 〃 | 〃 | 〃 | 〃 |
| worker-report | 〃 | 〃 | 〃 | 〃 |
| front | 없음 | 없음 | 없음 | 없음(맞다 — codex를 쓰지 않는다) |

- **다섯 deployment 전부**: PASS. `aiMounts` · `aiVolumes`는 `back.yaml:77,87`과 `worker.yaml:56,64`(kinds 루프)에서만 불리고, 두 템플릿 모두 이 둘을 include한다. 빠진 곳이 없다.
- **lima-worker-1 고정**: PASS(`back.yaml:36-37` · `worker.yaml:28-29`). replicas는 모두 1이고, back · worker 모두 `strategy: Recreate`다.
- **`codex-home` PVC 불변**: PASS. diff는 `codex-runtime` 추가뿐이다. `ai-pvc.yaml`은 변경 0.
- **hostPath type `Directory`**: PASS. 녹음 · 자료와 같은 관례다(`back.yaml:84,86`). 마운트가 빠졌을 때 VM 디스크에 조용히 쓰지 않고 시작을 거부한다 — 옳은 선택이다. 발주서의 「`DirectoryOrCreate` 등」보다 기존 관례를 따랐다.
- **노드 디렉터리가 먼저 있어야 한다**: `values-prod.yaml` 주석에 적혀 있다. 명령은 §7.
- **dev 경로 분리**: PASS. `values-dev.yaml` → `/mnt/mac/strong-hajin-dev/codex-runtime`. Argo에 strong-hajin dev app은 없다(`argocd/applications`에는 `strong-hajin-prod` · `-datastores`뿐). dev를 처음 띄울 때 이 디렉터리도 먼저 만들어야 한다.
- **env 없음**: 발주서는 env `SCAX_CODEX_RUNTIME_HOME`을 요구했다. 하지만 뒤의 결정(`_RESUME.md` §2 10-01 「env 불필요 — 앱 기본 경로에 그대로 마운트」)을 따랐다. 결정과 맞으므로 PASS다.
  - 이 방식은 컨테이너의 cwd가 `/app`이라는 데 기댄다. 상대경로이기 때문이다. 렌더된 `workingDir`은 없으므로 이미지 `WORKDIR`에 기댄다. 조사 §1-3에서 back · worker-meeting 모두 `cwd=/app`임을 확인했다.
  - 이미지 WORKDIR이 바뀌면 조용히 파드 로컬로 돌아간다. 차트 주석에 이 의존을 한 줄 적어 두면 좋다(참고).

## 4. resume을 쓰는 다른 자리

| 자리 | 세션을 여는 곳 → 이어 쓰는 곳 | 공유 홈으로 | 남는 위험 |
|---|---|---|---|
| 회의 배치 `application.py:603-617`(`meeting-batch`) | back → back | **나아진다.** 회의 중 back이 재시작 · 배포돼도 세션이 남는다(조사 §3 「같은 위험」) | 홈을 잃으면(디렉터리 삭제 등) 배치는 콜드 폴백이 없다. 그 회의의 배치는 끝까지 실패하고, 합성은 콜드로 산다. `ProviderSessionUnavailable`이 하위 클래스라 지금과 같은 실패로 처리된다 |
| 대화 turn `platform/conversations.py:277 · :489`(`latest_session`) | worker-conversation → worker-conversation | **크게 나아진다.** 예전에는 worker-conversation이 재시작할 때마다(**배포마다**) 기존 대화의 다음 turn이 모두 resume 실패였을 것이다. 이번 조사 범위 밖이라 운영 사례는 확인하지 않았다 | 홈을 잃으면 대화도 콜드 폴백이 없다. 해당 대화가 계속 실패한다 |
| 종료 합성 | back → worker-meeting | 고쳐진다(공유) + 안전장치(콜드) | WARN-2 |
| 보고서 · 자료 | `reports.py:881 · 900`은 결과의 session ref를 기록만 한다. resume 호출은 grep에서 찾지 못했다 | 영향 없음 | — |

## 5. 그 밖의 지적

- **WARN-4 WP Phase 4 문면이 결정과 어긋난다(문서 drift)**
  - WP `work-008-polish.md:268`은 「인프라 변경 없이 코드로 닫는다」, `:274`는 「범위 밖: 인프라 공유 볼륨」이라고 적고 있다.
  - 10-01 결정은 「뒤집음 — hostPath 공유」다(`_RESUME.md` §2). 코드 · 인프라는 결정을 따랐고 WP만 남아 있다.
  - 커밋 전에 planner(또는 코디)가 WP 계약 · 범위 줄을 고쳐야 한다. 그렇지 않으면 인프라 PR이 WP 「범위 밖」 위반으로 읽힌다.
- **WARN-3(stderr 쪽) 마스킹의 남는 틈** — `cli_process.py:78-90`
  - 막는 것
    - `Bearer/Basic <tok>`
    - `*api_key|token|secret|password|authorization|cookie|credential* [:=] 값`(JSON의 `"access_token":"…"` · `x-api-key:` · `OPENAI_API_KEY=` 포함)
    - JWT(`eyJ…`)
    - `sk-/pk-/rk-/sess-` 키
    - URL userinfo(`scheme://user:pass@`)
  - 마스킹을 먼저 하고 자르므로, 잘린 조각에 비밀이 남지 않는다.
  - 틈 1: **키 이름 없는 긴 hex · base64 토큰**은 지나간다.
  - 틈 2: `Cookie: a=b; c=d`에서 첫 값만 가려지고 `; ` 뒤 쿠키는 남는다.
  - 틈 3: **회의 원문 · 프롬프트가 stderr에 실리면** 600자까지 로그에 간다(개인정보). `exec --json`에서 codex가 stderr에 프롬프트를 되풀어 쓰는지는 확인하지 못했다. 코드 주석도 「길면 프롬프트 조각이 따라 나온다」를 의식하고 있다.
  - 실패 때만 남는 한 줄이라 위험은 낮다. 운영 첫 실패 로그를 한 번 눈으로 보는 것을 권한다.
- **참고 R-2** `delivery/README.md:59`
  - 「맞추지 않아도 … 콜드 스타트」는 종료 합성에만 해당한다. 배치 · 대화는 콜드 폴백이 없다(§4). 문장을 「종료 합성은」으로 좁혀 두면 오해가 없다.
- **참고 R-3** `_session_on_disk`(`codex_cli.py:794-799`)는 실패 때만 `sessions/` 전체를 rglob한다. 공유 홈이 커지면(WARN-3) 느려진다. 실패 경로라 영향은 작다.

## 6. 테스트

- 새 테스트 9개
  - contract 6(`test_codex_cli.py`): 세션 없음 → Unavailable · 세션 있음 → 일반 실패 · 마스킹 로그 · `summarize_stderr` · settings 기본값과 env · symlink 경합
  - unit 3(`test_meeting_finalize_service.py`): 콜드 폴백 · 시도 미소모 · 콜드 실패 → 같은 사유
- `make test-unit`: **392 passed, 1 deselected**
- `make test-contract`: **병렬 1135 passed + 직렬(serial) 128 passed, 실패 0** (rc=0)

## 7. 운영 반영 체크리스트

1. **노드 디렉터리 선행**(sync 전, 사람이 실행): `limactl shell worker-1 -- sudo mkdir -p /mnt/mac/strong-hajin/codex-runtime`
   - hostPath type `Directory`라 이 디렉터리가 없으면 다섯 파드가 모두 `ContainerCreating`에서 멈춘다.
   - Mac 쪽 실경로는 `~/mediness-data/strong-hajin/codex-runtime`이다(`lima/worker-1.yaml:36-38`).
   - 권한은 녹음 디렉터리와 같은 방식으로 맞춘다.
2. **한 PR로 반영**: 백엔드 이미지 태그(이 코드)와 차트 변경을 같은 infra PR에 싣는다(`_RESUME.md` 「image.tag와 한 PR」) → Argo 수동 sync.
   - 순서가 갈려도 둘 다 안전하다. 차트만 먼저 나가면 공유만 되고 콜드 폴백이 없다. 코드만 먼저 나가면 콜드 폴백만 있다.
3. **sync 직후 확인**
   - 다섯 파드가 `Running`인가
   - `kubectl exec deploy/worker-meeting -- ls /app/.scax/codex-runtime`에 `auth.json` symlink와 back이 연 `sessions/`가 보이는가
4. **sqlite 확인(WARN-1)**: 첫 대화 · 회의 몇 번 뒤 다섯 파드 로그를 본다. `Codex CLI … 실패했습니다: …database is locked|disk I/O error|malformed`가 0인지 확인한다. 보이면 대안 B를 검토한다.
5. **기존 실패 회의 [다시 시도]**: ac0e419b(36초) · df661b31(14:15 회의)
   - 공유 홈은 **새로 비어 있다.** 그래서 예전 back 로컬 세션은 없다(배포로 back이 재시작되면 이미 사라졌다).
   - 따라서 [다시 시도]는 **콜드스타트 경로**를 탄다. 로그 「회의 … 합성이 이전 세션을 이어 가지 못합니다 — 콜드 스타트로 돕니다」 → 「합성 완료 (콜드 스타트)」를 확인한다.
   - 회의록 형식이 보통 회의와 같은지 사용자 E2E로 본다.
6. **새 회의 하나 E2E**: 시작 → 배치 몇 번 → 종료 → **콜드스타트 로그 없이**(세션 resume) 회의록이 서는지 본다. 이게 공유 홈의 본 검증이다.
7. **대화 이어 쓰기**: 배포 전에 있던 대화에 한 마디 더 하면 실패할 수 있다(옛 세션은 파드 로컬이었다). 새 대화는 이후 배포를 넘겨도 이어지는지 다음 배포 때 본다.
8. **런북 한 줄(R-1)**: 「AX 전부 실패 + `isolated Codex runtime …` 로그 → 공유 홈의 금지 파일 · auth symlink 점검」
9. **정리 정책(WARN-3)**: 후속 과제로 등록한다.

## 확인한 것
- 계약 1~3 · 콜드 = 같은 결과물 · 재시도 미소모 · 콜드 실패 = 기존 상태 ✔
- 공유 홈 동시성: symlink 경합 닫힘 ✔ / sqlite on virtiofs 미증명(WARN-1) / 동시 resume(WARN-2) / 영속 오염(R-1) / 정리 없음(WARN-3)
- 인프라 다섯 deployment · 노드 고정 · PVC 불변 · Directory · dev 분리 ✔(helm lint 0 failed)
- resume 전수: 배치 · 대화 · 합성(+ 보고서는 기록만) ✔
- allowed_paths: 코드 diff는 backend 9 + README, 인프라 diff는 `charts/strong-hajin/`만 ✔
