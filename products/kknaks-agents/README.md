# kknaks-agents

## 목적

특정 agent 제품에 종속되지 않고 LLM을 **교체 가능한 추론 모듈**로 쓰는 최소 Python runtime 라이브러리의 SSOT다. tool 등록·검증·실행, model 호출 반복과 종료 조건, session 원본 상태, context 구성과 compaction, skill 선택은 전부 라이브러리와 호스트 애플리케이션이 소유하고, provider는 한 번의 공통 요청을 한 번의 공통 응답으로 바꾸는 adapter로만 남긴다.

규칙: `rules/product-doc-pipeline.md`

> ID prefix: frontmatter `id`는 전역 유일성을 위해 `KAG-` prefix를 쓴다 (`KAG-BL-001`, 이후 `KAG-DEC-001` 등). MRT/CFO/AXKG 컨벤션과 동일하다.

> 현재는 **baseline 수집 단계**다. decision·spec·work는 아직 없고, 코드 저장소도 첫 커밋 전이다. 다음 단계는 decision이다.

## 코드 레포

코드는 이 레포가 아니라 별도 저장소에서 관리한다. 아래 값은 오케스트레이션 설정(`config/projects/kknaks-agents.json`) 기준이며, 이 제품은 아직 `context/studio/projects.md`에 등록돼 있지 않다.

| 항목 | 경로 |
|---|---|
| Remote | `https://github.com/kknaks/kknaks_agents.git` (첫 커밋 전) |
| Local clone | `/Users/kknaks/git/library/kknaks_agents` |
| 문서 SoT | `/Users/kknaks/git/toy_pr2/kknaks_profile/products/kknaks-agents` |

> 저장소 이름과 배포 package 이름은 아직 확정되지 않았다. 설계 노트의 `llm_runtime`은 가칭이다.

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | KAG-BL-001 raw | 사용자 리뷰 후 decision으로 승격 |
| Decision | 없음 | 첫 decision 작성 (**다음 단계**) |
| Spec | 없음 | decision 확정 후 |
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
