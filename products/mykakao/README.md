# mykakao

## 목적

mykakao 제품을 운영하기 위한 SSOT다.

규칙: `rules/product-doc-pipeline.md`

> 아직 초안(draft) 단계. 제품 정의는 baseline부터 채워나간다.
> 코드는 별도 레포 `mykakao`에 있고, 이 디렉토리는 제품 문서 SoT다.

## 코드 레포

| 항목 | 경로 |
|---|---|
| Remote | `github.com/kknaksss/mykakao` |
| Local clone | `/Users/kknaks/git/toy_pr2/mykakao` |
| 문서 SoT | `/Users/kknaks/git/toy_pr2/kknaks_profile/products/mykakao` |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | BASE-001 accepted | — |
| Decision | DEC-001 accepted | — |
| Spec | SPEC-001 draft | 일정 파싱 단계 진입 시 보강 |
| Work | WORK-001 done | (다음) 일정 파싱 spec/work |

> 현재 범위: **메시지 추출까지만**(웹 데모 + 실시간 SSE 포함). 일정 파싱/캘린더 출력은 다음 단계에서 별도 decision/spec.

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |

> 40-architecture / 60-release / 70-runbook 은 필요해질 때 생성한다 (optional).

## 최근 로그

전체 이력은 `log.md`.

- 2026-06-12 BASE-001 / DEC-001 / SPEC-001 작성 — 메시지 추출 방식 확정 + 라이브 검증
- 2026-06-12 WORK-001 — 웹 데모(백+프론트) + 실시간 SSE 완성, 라이브 검증
