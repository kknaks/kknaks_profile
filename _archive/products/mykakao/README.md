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
| Baseline | BASE-001 accepted / BASE-002 accepted | — |
| Decision | DEC-001 accepted / DEC-002 accepted (OQ 4건 closed) | — |
| Spec | SPEC-001 draft / SPEC-002 draft | SPEC-002 → WORK-002 |
| Work | WORK-001 done / WORK-002 todo | WORK-002 구현(BE 호스트 / FE / docker redis+codex worker) |

> 현재 범위: **메시지 추출**(웹 데모 + 실시간 SSE)은 완료. **AI 요약 체인**은 BASE-002/DEC-002/SPEC-002/WORK-002까지 문서 확정. 코드 구현(WORK-002)은 별도 BE/FE 워커 소관. 일정 파싱/캘린더 출력은 그 이후.

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
- 2026-06-15 BASE-002 / DEC-002 — AI 요약 체인 개시. open_kknaks(codex) + 단일 방·날짜 + SSE + 2뷰 결정 확정(구현 OQ 4건은 spec 단계)
- 2026-06-15 SPEC-002 — AI 요약 기능 계약(2뷰/SSE/codex gpt-5.5/조립템플릿/cap). DEC-002 OQ 4건 closed + links 승격. → WORK-002
- 2026-06-15 WORK-002 — AI 요약 작업 지시서(W-1 BE 엔드포인트 2 / W-2 FE 2뷰 / W-3 redis+codex 워커 기동) + acceptance. status todo, 코드는 BE/FE 워커 소관
- 2026-06-15 WORK-002 인프라 개정 — W-3을 docker(redis `7-alpine` + codex worker, examples 미러) + backend 호스트 스크립트(`redis://localhost:6379`)로 교체. 결과 저장(DB) 명시적 제외. DEC/SPEC 불변
