# kknaks-agents

## 목적

특정 agent 제품에 종속되지 않고 LLM을 **교체 가능한 추론 모듈**로 쓰는 최소 Python runtime 라이브러리의 SSOT다. tool 등록·검증·실행, model 호출 반복과 종료 조건, session 원본 상태, context 구성과 compaction, skill 선택은 전부 라이브러리와 호스트 애플리케이션이 소유하고, provider는 한 번의 공통 요청을 한 번의 공통 응답으로 바꾸는 adapter로만 남긴다.

규칙: `rules/product-doc-pipeline.md`

> ID prefix: frontmatter `id`는 전역 유일성을 위해 `KAG-` prefix를 쓴다 (`KAG-BL-001`, 이후 `KAG-DEC-001` 등). MRT/CFO/AXKG 컨벤션과 동일하다.

> 현재는 **decision 단계**다. 첫 decision(KAG-DEC-001 — 디렉터리 구조와 의존 경계)과 두 번째 decision(KAG-DEC-002 — 최소 headless turn runtime 동작 구조)이 모두 2026-08-08 사용자 확정으로 `accepted`가 됐다. 세 번째 decision(KAG-DEC-003 — core package 계약 경계), 네 번째 decision(KAG-DEC-004 — process package 실행 격리 경계), 다섯 번째 decision(KAG-DEC-005 — providers package 변환 경계), 여섯 번째 decision(KAG-DEC-006 — tools package 등록·허용·검증·실행 경계)은 2026-08-09 `proposed`로 **사용자 리뷰 대기** 중이다. 공개 계약은 디렉터리 하나씩 의존 그래프 아래에서 위로 내려가며, 지금까지 제안된 것은 `core/`(L0)·`process/`(L1)·`providers/`(L2)·`tools/`(L2)다. spec·work는 아직 없고 코드 저장소도 첫 커밋 전이다.

## 코드 레포

코드는 이 레포가 아니라 별도 저장소에서 관리한다. 아래 값은 오케스트레이션 설정(`config/projects/kknaks-agents.json`) 기준이며, 이 제품은 아직 `context/studio/projects.md`에 등록돼 있지 않다.

| 항목 | 경로 |
|---|---|
| Remote | `https://github.com/kknaks/kknaks_agents.git` (첫 커밋 전) |
| Local clone | `/Users/kknaks/git/library/kknaks_agents` |
| 문서 SoT | `/Users/kknaks/git/toy_pr2/kknaks_profile/products/kknaks-agents` |

> Python import package 이름은 KAG-DEC-001에서 `kknaks_agents`로 **확정**됐다(설계 노트의 `llm_runtime`은 가칭이었다). PyPI 배포명과 public import 표면의 안정성 약속은 여전히 미결이다 (KAG-DEC-001 OQ-1·OQ-2). OQ-2 중 `core/__init__.py` 재수출 범위는 KAG-DEC-003이 권고안으로 다루는 중이고, package-root 재수출과 안정 API 약속은 계속 미결이다.

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | KAG-BL-001 accepted | 남은 Possible Direction·Open Questions를 이후 decision으로 |
| Decision | KAG-DEC-001 accepted · KAG-DEC-002 accepted · **KAG-DEC-003 proposed** · **KAG-DEC-004 proposed** · **KAG-DEC-005 proposed** · **KAG-DEC-006 proposed** | **KAG-DEC-003(core 계약 경계)·KAG-DEC-004(process 실행 격리 경계)·KAG-DEC-005(providers 변환 경계)·KAG-DEC-006(tools 등록·허용·검증·실행 경계) 사용자 리뷰** (현재 게이트). 이후 raw 작성 순서는 `sessions` → `skills` → `context` → `runtime` |
| Spec | 없음 | package별 계약 decision이 정리된 후 |
| Work | 없음 | spec 확정 + 사용자 리뷰 후 |
| Architecture | 없음 | 여러 spec/work가 공유할 구조가 생기면 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |

> `60-release` / `70-runbook` / `showcase`는 필요해질 때 생성한다 (optional).

## Reference 경계

이 제품의 설계 입력에는 **수정하지 않고 읽기만 하는** 외부 자료가 있다. 경계를 문서에도 그대로 유지한다.

| 자료 | 성격 | 경계 |
|---|---|---|
| 설계 노트 (`REF-0007`, 오케스트레이션 설정 레포) | 목적·구조·동작·사용법의 현재 기준 | 여기 없는 제품 결정을 발명하지 않는다. 노트의 코드 예시는 **가안**이며 확정 public API가 아니다 |
| 사내 운영 서비스의 server-owned tool loop 구현 | read-only 관찰 사례 | 코드를 수정하지 않는다. 조직·업무·데이터가 드러나는 본문은 옮기지 않고, 구조 패턴만 일반화한다 |
| 개인 clean-room 연구 아카이브 | 개념 관찰 전용 | 실행하지 않는다. 코드·문자열·식별자를 복사하지 않고, 파생 문서에서 출처로 인용하지 않는다. 개념은 이 제품 고유 언어로 다시 명명한다 |

관련 제품: `products/open-kknaks/` — LLM 호출을 감싸는 별도 제품이다. 두 제품의 관계는 아직 결정되지 않았으며 decision 단계에서 다룬다.

## 최근 로그

전체 이력은 `log.md`.

- 2026-08-07 제품 문서 스캐폴딩 생성 (README, log, 00~40 index) 및 `products/README.md` 등록
- 2026-08-07 KAG-BL-001 작성 — provider-neutral LLM runtime 라이브러리 baseline
- 2026-08-08 KAG-DEC-001 작성(proposed) — runtime 디렉터리 구조와 의존 경계. KAG-BL-001은 `reviewing`으로 전환
- 2026-08-08 사용자 확정 — KAG-DEC-001 `accepted`(Option B 책임별 package), KAG-BL-001 `accepted`
- 2026-08-08 KAG-DEC-002 작성(proposed) — 최소 headless turn runtime 동작 구조. 사용자 리뷰 대기
- 2026-08-08 사용자 확정 — KAG-DEC-002 `accepted`(Option B deterministic turn loop). Open Questions 9건은 미결 유지
- 2026-08-09 KAG-DEC-003 작성(proposed) — core package 계약 경계(파일·타입 범주·공개 표면). 사용자 리뷰 대기
- 2026-08-09 KAG-DEC-004 작성(proposed) — process package 실행 격리 경계(보안 경계 13항목·파일 배치·실행 lifecycle·fail-closed). 사용자 리뷰 대기
- 2026-08-09 KAG-DEC-005 작성(proposed) — providers package 변환 경계(공용/전용 판정·adapter 파일 배치·호출 lifecycle 6국면·실패 소유권·capability 계약). 사용자 리뷰 대기
- 2026-08-09 KAG-DEC-006 작성(proposed) — tools package 등록·허용·검증·실행 경계(등록/허용/공개 표면 세 값 분리·파일 배치·tool call 국면 8개·거부 5계열·handler 주입 표면). 사용자 리뷰 대기
