# Studio Workflow

## 목적

여름별컴퍼니의 개인 프로젝트 작업 흐름을 정의한다.

모든 제품 작업은 이 흐름을 기준으로 baseline, decision, spec, work 중 어디에서 시작할지 결정한다.

## 작업 종류

| Type | 의미 | 시작 위치 |
|---|---|---|
| new-feature | 새 기능 구현 | `00-baseline/` 또는 `10-decision/` |
| spec-up | 기존 기능의 요구사항/정책/UX 확장 | `10-decision/` 또는 `20-spec/` |
| refactor | 사용자 기능 변화 없이 내부 구조 개선 | `30-work/` |
| bugfix | 의도와 다른 동작 수정 | `00-baseline/` 또는 `30-work/` |
| release | 출시 준비, 배포, 앱스토어, 운영 체크 | `30-work/` |
| ops | 지표, 비용, CS, 운영 자동화 | `00-baseline/` 또는 `30-work/` |

## 기본 흐름

```text
요청/아이디어 발생
→ 작업 종류 판단
→ baseline / decision / spec / work 중 시작점 선택
→ 필요한 단계만 순서대로 구체화
→ work에서 실제 작업 추적
→ product log 갱신
→ AI hook으로 정합성 검증
```

## 시작점 판단

| 상황 | 시작점 |
|---|---|
| 아직 날것의 아이디어, 불편, 레퍼런스 수준 | `00-baseline/` |
| 무엇을 할지 선택해야 함 | `10-decision/` |
| 기능 계약을 바로 쓸 수 있음 | `20-spec/` |
| 사용자-facing 변화가 없는 구현 작업 | `30-work/` |
| 기존 spec을 구현하는 작업 | `30-work/` |

## 작업 상태

| Status | 의미 |
|---|---|
| todo | 아직 시작하지 않음 |
| in_progress | 작업 중 |
| blocked | 막힘 |
| review | 검토 중 |
| done | 완료 |

## 역할

1인 조직이라도 역할은 분리해서 적는다.

| Role | 책임 |
|---|---|
| Owner | 최종 결정과 우선순위 |
| PM | 범위, 요구사항, 일정 |
| Design | UX/UI 판단 |
| FE | 프론트엔드 구현 |
| BE | 백엔드/API/데이터 구현 |
| QA | 검증과 완료 판단 |
| Ops | 배포, 운영, 지표, 비용 |

## 운영 원칙

- 모든 실제 구현 작업은 `30-work/work-*.md`에서 추적한다.
- 작업자가 나 혼자여도 role을 비워두지 않는다.
- work에는 담당, 상태, 진행률, blocker, 다음 액션이 보여야 한다.
- spec 없이 구현 가능한 refactor/ops 작업은 work에서 시작할 수 있다.
- 사용자에게 보이는 동작이 바뀌면 spec으로 환류한다.
- 제품 방향이나 범위가 바뀌면 decision으로 환류한다.
