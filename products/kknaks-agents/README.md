# kknaks-agents

## 목적

특정 agent 제품에 종속되지 않고 LLM을 **교체 가능한 추론 모듈**로 쓰는 최소 Python runtime 라이브러리의 SSOT다. tool 등록·검증·실행, model 호출 반복과 종료 조건, session 원본 상태, context 구성과 compaction, skill 선택은 전부 라이브러리와 호스트 애플리케이션이 소유하고, provider는 한 번의 공통 요청을 한 번의 공통 응답으로 바꾸는 adapter로만 남긴다.

규칙: `rules/product-doc-pipeline.md`

> ID prefix: frontmatter `id`는 전역 유일성을 위해 `KAG-` prefix를 쓴다 (`KAG-BL-001`, 이후 `KAG-DEC-001` 등). MRT/CFO/AXKG 컨벤션과 동일하다.

> 현재는 **decision 단계**다. 첫 decision(KAG-DEC-001 — 디렉터리 구조와 의존 경계)과 두 번째 decision(KAG-DEC-002 — 최소 headless turn runtime 동작 구조)이 모두 2026-08-08 사용자 확정으로 `accepted`가 됐다. 세 번째 decision(KAG-DEC-003 — core package 계약 경계), 네 번째 decision(KAG-DEC-004 — process package 실행 격리 경계), 다섯 번째 decision(KAG-DEC-005 — providers package 변환 경계), 여섯 번째 decision(KAG-DEC-006 — tools package 등록·허용·검증·실행 경계), 일곱 번째 decision(KAG-DEC-007 — sessions package event 저장·조회 경계), 여덟 번째 decision(KAG-DEC-008 — skills package 등록·선택·prompt 투영 경계)은 2026-08-09 `proposed`로 **사용자 리뷰 대기** 중이다. 공개 계약은 디렉터리 하나씩 의존 그래프 아래에서 위로 내려가며, 지금까지 제안된 것은 `core/`(L0)·`process/`(L1)·`providers/`(L2)·`tools/`(L2)·`sessions/`(L2)·`skills/`(L2)다. KAG-DEC-008은 skills를 최소 tool loop의 필수 요소로 바꾸지 않고 **추후 조립 가능한 독립 확장 모듈**이라는 분류를 유지한다. spec·work는 아직 없고 코드 저장소도 첫 커밋 전이다.

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
| Decision | KAG-DEC-001 accepted · KAG-DEC-002 accepted · **KAG-DEC-003 proposed** · **KAG-DEC-004 proposed** · **KAG-DEC-005 proposed** · **KAG-DEC-006 proposed** · **KAG-DEC-007 proposed** · **KAG-DEC-008 proposed** | **KAG-DEC-003(core 계약 경계)·KAG-DEC-004(process 실행 격리 경계)·KAG-DEC-005(providers 변환 경계)·KAG-DEC-006(tools 등록·허용·검증·실행 경계)·KAG-DEC-007(sessions event 저장·조회 경계)·KAG-DEC-008(skills 등록·선택·prompt 투영 경계) 사용자 리뷰** (현재 게이트). 이후 raw 작성 순서는 `context` → `runtime` |
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
- 2026-08-09 KAG-DEC-007 작성(proposed) — sessions package event 저장·조회 경계(store 계약과 구현의 파일 분리·순서/원자성/중복/read-your-write 불변식·거부 6계열·memory와 durable 확장 seam·되읽기와 재생의 구분). KAG-DEC-003 OQ-2에 대한 답을 함께 제안. 사용자 리뷰 대기
- 2026-08-09 KAG-DEC-007 검수 보정(상태 `proposed` 유지) — 표현 복원(허용)과 의미·정책 분기(금지)의 경계를 §6.3에 표로 신설하고 구조 검사 기준을 “종류 이름 부재”에서 “종류를 보는 코드의 국소화”로 교정, SR3를 SR3′·SR3″로 갈라 canonical event 무손실 저장을 KAG-DEC-002 I1과 맞춤, 불변식에 SI10 추가(10개)
- 2026-08-09 KAG-DEC-008 작성(proposed) — skills package 등록·선택·prompt 투영 경계(확장 모듈 규칙 5개·세 값 분리·loader 부재·국면 6개와 불변식 9개·투영 경계와 prompt injection 판정·자산 거처 비교). skills를 최소 runtime의 필수 요소로 바꾸지 않고 독립 확장 모듈 분류를 유지. 사용자 리뷰 대기
- 2026-08-09 KAG-DEC-008 검수 보정 1(상태 `proposed` 유지) — 선택·투영의 호출 소유권을 **고정 순서 2단계(facade 미채택)**로 하나로 정하고 SKC1·SKC2 신설·방향 규칙 5개로 확장·SKI1을 단계별 결과로 정정, `registry ⊇ 선택 set ⊇ 투영`을 타입에 맞는 관계 3종(상한 ⊆ / 변환 / 출처 추적)으로 교체, §8.2를 **“권고 구조는 (가)를 전제한다”**로 고쳐 (나)/(다) 선택 시 supersede해야 할 항목을 명시(dynamic discovery 완전 제외는 유지)
- 2026-08-09 KAG-DEC-008 검수 보정 2(상태 `proposed` 유지) — 보정 1이 남긴 lifecycle 모순 해소. **실행 조건의 비대칭**을 명시(선택은 turn당 항상 한 번 · 투영은 **선택 set을 받았을 때만** 한 번 · **선택 거부는 투영을 부르지 않고 그 자리가 terminal** — SKC1상 거부는 선택 set이 아니라 넘길 값이 없다), **terminal result 셋**(투영 · 선택 거부 · 투영 거부) 신설로 lifecycle이 정확히 하나로 끝남을 고정, 다이어그램을 성공/거부 분기로 재작성하고 sequence에 `alt` 갈래 추가, SKI1을 “실행된 각 단계가 결과 하나 + lifecycle은 terminal 하나”로·SKI8을 “빈 선택 set은 성공값이라 경계를 넘어 빈 투영이 된다(SKG6은 유지)”로 재작성, seam “단계 실행 조건” 신설(6→7종)
