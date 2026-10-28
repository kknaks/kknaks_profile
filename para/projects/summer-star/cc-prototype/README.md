---
sot: here
status: active
---

# CC Prototype

고객에게 보여줄 **기능별 실험** 모음. 기능 하나가 `<기능>/front` + `<기능>/back` 한 쌍이고,
기능끼리는 아무것도 공유하지 않는다. 첫 기능은 `cc`(병원 현황판, BASE-003) · `sts`(실시간 음성 통역, BASE-002) — 사용자는 sts 가 cc 로 통합될 것으로 본다.

## 코드 위치

| 항목 | 경로 |
|---|---|
| 코드 레포 | `https://github.com/kknaksss/cc-prototype` · 로컬 `/Users/kknaks/git/toy_pr2/cc-prototype` (DEC-001 D-01) |

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | raw 5건 (BASE-002 sts · 003 현황판 · 004 예약 · 005 협찬) | 열린 질문 정리 |
| Decision | DEC-001 proposed | 사용자 승인 |
| Spec | — | 레포 뼈대 SPEC |
| Work | — | — |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | [입력](00-baseline/README.md) |
| 10-decision | [결정](10-decision/README.md) |
| 20-spec | [스펙](20-spec/README.md) |
| 30-work | [구현 계획](30-work/README.md) |
| 배포 | [배포 · TestFlight 업로드](deploy.md) — 경로 · 웹 배포 순서 · 앱 업로드 명령 |

## 최근 로그

- 2026-10-28: 고객 문진 웹 — 문진을 고객 자기 폰의 ccc 웹 페이지로(DEC-008 · SPEC-006 · WORK-010) · 앱은 QR 만 보여 줌
- 2026-10-12: DEC-001 개정(D-06) — sts 는 별도 기능이 아니라 cc 직원용 화면 안의 통역 기능
- 2026-10-10: 협찬 아이디어 노트 BASE-005 — Casty 로 찾고 Linky 에서 대화 생성
- 2026-10-10: 예약 아이디어 노트 BASE-004 — Linky → cc → KOS. 카톡·스크린샷 구간을 cc 로
- 2026-10-10: cc 아이디어 노트 BASE-003 — 병원 현황판(도면 위 실시간 위치). sts 는 cc 로 통합될 듯
- 2026-10-10: sts 아이디어 노트 BASE-002 — Soniox STT(번역 내장)+TTS 로 된다(문서 조사). 결정 전
- 2026-10-10: 제품 착수. 레포 구조·스택·기능 독립을 DEC-001(proposed)로. 배포 대상은 미정. [전체 이력](log.md)
