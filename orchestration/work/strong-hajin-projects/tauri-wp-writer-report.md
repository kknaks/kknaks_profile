# tauri-wp-writer 결과 보고 — WORK-006 계획

## 상태: done

산출물은 두 파일이다. **제품 코드·인프라·index·log·DEC·SPEC 을 한 줄도 고치지 않았다.**
커밋·push·PR 을 하지 않았고, 빌드·테스트·실측·서버 기동·배포를 하나도 실행하지 않았다.

---

## 1. 수행 내용

### 변경 파일 (2건, 둘 다 신규)

| 경로 | 무엇 |
|---|---|
| `para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md` | **WORK-006** — `status: todo` · `progress: 0` · `links.decisions=[DEC-005]` · `links.specs=[SPEC-006]` |
| `orchestration/work/strong-hajin-projects/tauri-wp-writer-report.md` | 이 보고서 |

### 계획의 뼈대 — 8 Phase

```text
1 계측기반(탐침 셸+fixture) → 2 1차 실측 10건 ══판정══> 3 제품 셸 → 4 웹 배선 → 5 통합 재측정 4건
                                                             ├→ 6 운영 준비(병행) → 7 설치·릴리즈 → 8 운영 최종
```

**순환을 만들지 않은 방법**을 문서에 명시했다 — Phase 1 의 탐침 셸은 **계측 수단이지 제품 셸이 아니고**,
폐기해도 되고 Phase 3 이 흡수해도 된다. 그래서 「제품 셸이 서야 잴 수 있다 ↔ 재야 만들 수 있다」가 생기지 않는다.
실측 열다섯 중 **열**은 Phase 2(fixture), **넷**은 Phase 5(제품 통합 재측정), **하나**(M-10)는 Phase 7(설치 두 판)이다.
`M-1`·`M-5` 는 Phase 8 에서 **최종 확인만** 다시 한다(새 항목이 아니다).

**Phase 2 끝에 진행 / 보완 / 중단 판정 게이트**를 두었다. 중단 조건은 둘 —
① M-1 커맨드 왕복 불성립 ② M-2 포맷이 대상 OS 에서 안 열림. 후자면 **포맷 후보 도입이 선행 work 로 승격**한다(OQ-T07).

### 계약 불변식 I-1 ~ I-8

브리프 §3 의 여덟(네이티브 소유 · 커맨드 넷 · TTL/renew 없음 · 완료 사건 해제 · 취소된 닫기 보존 ·
degraded 재무장 · 늦은 acquire 잔존 0 · 웹 hang 한계 유지)을 **표로 못박고**, Phase 3·4 의 「하지 말 것」에
「구현이 어려우면 바꾸지 말고 코디에게 올린다」로 다시 걸었다. **SPEC 을 직접 고치지 않았다.**

---

## 2. 검증 (브리프 §8)

| 항목 | 기준 | 결과 |
|---|---|---|
| AC 전수 | SPEC-006 의 `AC-T01`~`AC-T43` | SPEC 유니크 **43** / WORK 유니크 **43** · **누락 0 · 초과 0** |
| AC Phase 배정 | 중복·누락 0 | 추적표 행 **43 · 유니크 43 · 중복 0**. Phase 3=**15** · 4=**5** · 5=**21** · 7=**1** · 8=**1** (합 43) |
| 실측 전수 | M-1~M-14 + M-2b = 15 | 실측표 행 **15**, `M-1 M-2 M-2b M-3 M-4 M-5 M-6 M-7 M-8 M-9 M-10 M-11 M-12 M-13 M-14` |
| DEC 추적 | D-01~D-09 | **9건 전수**, 각각 받은 자리·상태(받음/부분/경계만) |
| 선행조건 순환 | 0 | 의존이 `1→2→3→4→5`, `6`(미결만·3·4와 병행), `7←5`, `8←5·6·7` — **단조 증가, 역참조 0** |
| YAML | frontmatter 파싱 | `yaml.safe_load` **OK** · `type/id/title/status/product/work_type/owner/roles/progress/created_at/updated_at/tags/links` 전부 존재 |
| 양식 | `templates/projects/30-work/work.md` | Meta · Work Summary · Role Assignment · Scope · Code Surface · Domain/Schema · Dependency · Internal Interface Contract · Execution · Pre-deploy Check · Rollback · Done Criteria · Open Issues · Related **전부 있음** |
| 링크·식별자 | wikilink 해석 | `[[decision-005-tauri-wrapper\|DEC-005]]` · `[[spec-006-tauri-wrapper\|SPEC-006]]` 둘 다 **실재 파일** |
| 체크 상태 | 검증 완료 체크 금지 | `[x]` **0건** · Phase Status 라인 **8개 전부 `TODO`** · `progress: 0` · `status: todo` |
| 린트 | `scripts/lint-pipeline.py` | **레포에 없다**(`scripts/` 디렉토리 자체 부재) → 실행하지 않고 위 항목을 직접 검증 |

### 코드 HEAD · 조회 시각 · dirty

| 대상 | 경로 | branch | HEAD | dirty | 조회 |
|---|---|---|---|---|---|
| 문서(작업 워크트리) | `…/kknaks_profile/strong_hajin` | `kknaksss/strong_hajin` | `613cc78e6d64f5e8baeaf4723183b25713c29def` | 작업 중(내 신규 2건 포함) | 2026-09-22 17:28 KST |
| 적용 코드 | `…/Strong_hajin/strong-hajin-projects` | `kknaksss/strong-hajin-projects` | `a1f67915aa8eeb551327b858428c5d4c1519e1b4` | **0건 (clean)** | 2026-09-22 17:33 KST |
| 참조 Tauri | `/Users/kknaks/git/toy_pr2/task_management` | `main` | `a720b6ef` | 0건 | 2026-09-22 17:31 KST |
| 인프라 | `/Users/kknaks/git/harness_works/k8s_infra_mac` | — | 읽기 전용 조회만 | — | 2026-09-22 17:32 KST |

> ⚠ **조사 문서와 기준이 다르다.** `tauri-implementation-research.md` 는 `e46ce39c`(dirty 69~72)를 읽었는데
> 지금은 **`a1f6791` 이 깨끗하다.** WORK-006 이 인용한 좌표 **12개를 전부 `a1f6791` 에서 다시 확인**했다:
> `stream.ts:251·258·322`(+`317-319`·`327-331`) · `MeetingDetailPage.tsx:932` · `labels.ts:772` ·
> `BrowserRecordingPage.tsx:13` · `App.tsx:684·401` · `http.py:606·2530` · `http_auth.py:106` · `delivery/Dockerfile:63`.
> **전부 일치.** 데코레이터 분포도 다시 셌다 — `@app.` **160** = 들여쓰기 4칸 **1**(`/health`) + 8칸 **158** + 12칸 **1**
> → **159 개가 `developer_auth_enabled` 블록 안**. 조사 §6-1 의 수와 같다.

### 확인한 사실 중 계획에 새로 들어간 것

- **코드 레포에 Tauri 가 0 건**이다(`frontend/` 아래 `src-tauri` 없음). 참조와 같은 자리(`frontend/src-tauri/`)에 새로 만든다.
- **`frontend` 워커의 `allowed_paths` 가 `frontend/` 라 `src-tauri/` 를 이미 덮는다** → **새 워커 유형이 필요 없다.**
  다만 `verify` 에 Rust 검증 명령이 없다(제안 P-4).
- **`BrowserRecordingPage.tsx:13` 의 `captureId = crypto.randomUUID()` 가 이미 회차마다 새 값**이다 →
  AC-T42 의 절반은 그대로 만족한다. 새로 만들 세션 키는 **회의 라이브 쪽 하나**뿐이다.
- **`delivery/Dockerfile:63` 이 `@openai/codex-linux-x64` / `x86_64-unknown-linux-musl` 을 하드코딩**한다.
  `Makefile:25` 도 `PROTECTED_PLATFORM ?= linux/amd64`. **노드는 전부 arm64** →
  납품 이미지를 그대로 arm64 로 굽지 못한다(OQ-W03).
- **mediness ingress 는 front·api 가 다른 호스트**라 같은 origin 을 대신하지 못한다 →
  Strong Hajin 은 **한 호스트 + 경로 분기**가 필요하고, `/api/meetings/{id}/stream` 이 `/api` 아래라
  **WS 도 같은 규칙에 실린다**(`proxy-read-timeout: 3600` 필요).
- **ArgoCD Application 열 개가 전부 `targetRevision: main`** → 새 앱도 `main` 추적을 기본안으로 적었다.
  **README 의 `k8s-test` 설명은 실물과 다르므로 인용하지 않았다.**

---

## 3. 계약 준수

- **범위**: 허용된 두 파일만 썼다. 제품 코드·인프라·`10-decision`·`20-spec`·index·`log.md` **diff 0줄**.
- **실행 금지**: 빌드·테스트·실측·설치·배포·Release·서버 기동/중단 **0회**. 비밀값 파일 **미열람**
  (접속은 `mediness.json` 의 `environments` 를 **참조**만 하고 값을 복제하지 않았다).
- **추가 발주 없음**: 서브에이전트·워커를 띄우지 않았다.
- **SPEC 불변**: 새 사용자 계약이 필요한 것은 **변경 제안 P-1~P-4** 로 올렸고 SPEC 을 고치지 않았다.
- **추측 금지**: 미정(최소 OS·아키텍처·형식·운영 도메인·배포 대상·서명·공증·업데이트)은 전부
  **제안 또는 옵션+권장**으로 표시했고 **사용자 확정으로 쓰지 않았다.** 12h 세션·열린 WS 만료 동작을 바꾸지 않았다.
- **대체 검증 금지**: Windows 실기가 없으면 **「검증 불가(장비 없음)」로 남기고 macOS 결과로 대신하지 않는다**를
  Phase 2·5·7 의 측정 규칙과 Pre-deploy Check 에 각각 박았다.
- **테스트 제외 규칙 미계승**: WORK-005 의 `material_*` 특수 제외 같은 규칙을 **가져오지 않았다**(형식만 참고).

---

## 4. 검수 포인트 — 리뷰어가 볼 자리

| # | 무엇을 봐야 하나 | 왜 |
|---|---|---|
| **R-1** | **Phase 2 판정 게이트의 세 갈래가 실행 가능한가** — 「보완」의 경계가 모호하지 않은가 | 여기서 모호하면 중단해야 할 것이 조용히 진행된다 |
| **R-2** | **AC Phase 배정의 타당성** — 특히 `AC-T17`(훅을 잰다, 점유가 아니다) · `AC-T24`(Phase 3 잠정 / Phase 8 최종) · `AC-T32`·`AC-T38`(구현 층을 M-6 이 정한다) | R2 검수에서 한 번 모순이 났던 자리들이다 |
| **R-3** | **계약 불변식 I-1 ~ I-8 이 Phase 3·4 의 「하지 말 것」으로 실제로 닫히는가** | 구현 편의로 TTL 이 되살아나는 것이 이 SPEC 의 최대 회귀 위험 |
| **R-4** | **M-2b 측정 수단**(개발 DB 의 `expires_at` 직접 조정)이 제품 변경 없이 성립하는가 | TTL 이 코드 상수라 env 로 못 연다. 다른 수단이 있으면 그쪽이 낫다 |
| **R-5** | **Phase 6 의 「사실 / 제안」 분리가 지켜졌는가** — 권장안이 확정처럼 읽히는 칸이 없는가 | 운영 프로파일·이미지·서빙 방식은 전부 사용자 결정이다 |
| **R-6** | **Rollback 의 「되돌릴 수 없는 것」이 충분한가** — 식별자·발행된 Release 외에 더 있는가 | 데이터 손실 경로를 빠뜨리면 늦게 발견된다 |
| **R-7** | **Phase 6 이 Phase 3·4 와 병행 가능하다는 판단** | 코드가 안 겹치는 것은 맞으나 사람이 하나다 — 코디 판단 |

---

## 5. 남은 사용자 결정과 차단 Phase

### 이 work 가 새로 여는 것 — 여섯

| ID | 결정할 것 | 차단 Phase | 차단되지 **않는** 것 |
|---|---|---|---|
| **OQ-W01** | **Windows 실기를 갖고 있는가** | 2·5·7 의 **Windows 축** | macOS 축 전부 |
| **OQ-W02** | 배포 구성이 들어갈 레포 — 회사 `k8s_infra_mac` 인가 별도인가 | **6** | 1~5·7 |
| **OQ-W03** | 운영 서버 이미지 — 새 arm64 비보호 이미지(권장) vs 보호 이미지 arm64 확장 | **6** | 1~5·7 |
| **OQ-W04** | FE 정적 서빙 — ingress 경로 분기(권장) vs 백엔드 `StaticFiles` | **6** | 1~5·7 |
| **OQ-W05** | **운영 프로파일 해소** — 라우트 등록 / 새 프로파일 / `cookie_secure` 분리 | **6 · 8** | 1~5·7 |
| **OQ-W06** | Windows 설치파일 빌드 환경 — 실기 / 러너 / 없음 | **7 의 Windows 축** | macOS 설치파일 |

### 이어받은 것 — 차단 범위만 다시 적는다

| ID | 차단 Phase | 비고 |
|---|---|---|
| **OQ-T01** 최소 OS·아키텍처·형식 | **7** | 1~5 는 개발자 자기 기기로 잰다 |
| **OQ-T02** 운영 도메인·프로파일·인증 | **6 · 8** | 나머지는 개발 fixture 로 진행 |
| **OQ-T03** 배포 대상·서명·공증·업데이트 | **7 후단 · 8** | 앱이 도는 것 자체는 안 막는다 |
| **OQ-T07** 녹음 포맷 실측 | **Phase 2 판정** | **중단 사유가 될 수 있는 유일한 미결** |
| **OQ-T04 · T05 · T08 · T09 · T10 · T11** | **없음** | 현재 값·현재 동작으로 계획했다 |
| **OQ-T06** 커맨드 origin 값 | **8**(값만) | 모양은 Phase 3 에서 확정 |

### 변경 제안 — 사용자·코디 판단 필요

- **P-1 운영 프로파일 해소** — `PRODUCTION` 에 로그인·API 가 없고 `Secure` 쿠키는 그 프로파일에서만 붙는다.
  **새 사용자 계약이라 별도 decision 이 맞다.** WORK-006 은 Phase 6·8 을 그 결정 뒤로 gate 했다.
- **P-2 운영용 arm64 서버 이미지 신설** — 납품 보호 이미지(amd64·Nuitka·codex x64 고정)와 목적이 다르다.
- **P-3 M-2b 측정 수단** — 제품 변경 없이 개발 DB 의 `expires_at` 을 당겨 잰다. TTL 을 env 로 여는 것은 제안하지 않았다.
- **P-4 워커 설정 갱신** — `frontend` 워커 `verify` 에 Rust 검증(`cargo check`·`clippy`·tauri 빌드) 추가.
  `allowed_paths` 는 그대로 두면 된다.

### index 갱신안 — 이 워커가 고치지 않았다 (코디 몫)

- `30-work/README.md` **Status Board**:
  `| 1–8 | [WORK-006 데스크톱 래퍼](work-006-tauri-wrapper.md) | SPEC-006 전절 | todo | kknaks | 미산정 | 미정 | - | 없음 | Phase 1 발주 |`
- `30-work/README.md` **Work List**:
  `| WORK-006 | 데스크톱 래퍼 | new-feature | kknaks | todo | 0% | [본문](work-006-tauri-wrapper.md) | SPEC-006 |`
- `30-work/README.md` **Spec Coverage**: `| SPEC-006 | WORK-006 | todo |`
- `30-work/README.md` 「최종 수정」 → `2026-09-22`
- `log.md`: `| 2026-09-22 | WORK-006 계획 작성: 실측 15건·인수조건 43건을 8 Phase 에 배정. Phase 2 끝에 진행/보완/중단 판정. 운영 프로파일·배포 레포·이미지 아키텍처·Windows 실기 등 미결 6건 신설. 구현·실측·빌드·배포 미착수 | [작업](30-work/work-006-tauri-wrapper.md) |`
- `20-spec/README.md` 의 SPEC-006 행은 **`draft` 그대로 둔다** — 구현·실측이 남았다.

---

## 6. 미결·주의점

- **Phase 기간·목표일을 산정하지 않았다.** 실측 하나가 `max(3T, 30분)` 이상이고 `T` 가 기기 설정에 달렸다.
- **절전 방지 구현 수단을 정하지 않았다.** 공식 Tauri 플러그인이 **없다**는 사실만 확정이고, 직접 구현이냐
  커뮤니티 크레이트냐는 Phase 3 이 고른다.
- **`AC-T32`·`AC-T38` 의 구현 층**(웹의 `beforeunload` 냐 셸의 닫기 훅이냐)은 M-6 이 정한다 —
  계획에서 미리 정하지 않았다.
- **Windows 는 실기·빌드 환경 둘 다 미확인**이다. 계획은 「없으면 macOS 만 내고, Windows 지원을 했다고 쓰지 않는다」로 닫았다.
- **Phase 6 의 구성안은 문서다.** 실제 차트·Application 작성과 배포는 사용자 결정 뒤 별도 발주가 맞다 —
  이 계획은 그 자리를 열어 두기만 했다.
