---
type: work
id: WORK-001
title: "cc PoC 구현 — 시드 · 상태 · 화면 3종 · 통역"
status: in-progress
product: cc-prototype
feature: cc
work_type: new-feature
owner: kknaks
progress: 95
created_at: 2026-10-13
updated_at: 2026-10-13
tags:
  - product/cc-prototype
  - feature/cc
  - doc/work
  - status/in-progress
links:
  baselines: []
  decisions:
    - "[[decision-002-cc-poc|DEC-002]]"
  specs:
    - "[[spec-001-cc-poc|SPEC-001]]"
  works: []
  releases: []
  related: []
---

# cc PoC 구현 — 시드 · 상태 · 화면 3종 · 통역

SPEC-001 을 2026-10-16(금) 지점 시연 전까지 로컬에서 돌게 만든다.

> 1 파일 = 1 work = **빌드 계획**. 계약은 SPEC-001 을 참조만 한다.

## Meta

- Covers spec: SPEC-001
- 코드 레포: `kknaksss/cc-prototype` — 범위는 `cc/back` · `cc/front` · 레포 루트 `sts/` 삭제
- 외부 의존: KOS 캡처(로컬 `CC_CAPTURE_DIR`) · Soniox 키(사용자가 `cc/back/.env` 에 — WP2 전에)
- 워커: backend · frontend (config `cc-prototype.json`). frontend 는 DesignSync 로 시안을 받는다

## Work Packages

| WP | 담당 | 내용 | SPEC | 선행 | 완료 조건 |
|---|---|---|---|---|---|
| **WP1** | backend | `cc/back` 뼈대(FastAPI · uv · SQLite) · `sts/` 삭제 · 시드 build/save · 상태 모델 · 읽기/조작 API · SSE · reset · 로그인 | §3~§6 · §8 | — | SPEC §9-1 · §9-5 · API 단위 시험 · 이름 대조 시험 |
| **WP3** | frontend | `cc/front` 뼈대(Next.js · medikit) · 시안 4+1 개 import(DesignSync) · 로그인 · 데스크 · 직원 첫 화면 · 환자 상세 · `lib/api.ts` · SSE 구독 | §2 · §5 · §6 | WP1 과 **병렬**(SPEC §5 계약 기준, back 없을 땐 계약 모양 목업) | tsc · lint · build · 시안 대조 |
| **WP2** | backend | 통역 중계 WS `/api/interpret` · Soniox STT/TTS · 번체 변환 · **실물 호출 확인 4건(§7.3)** | §7 | WP1 · **사용자 Soniox 키** | 실물 호출 결과 리포트 · 시험 |
| **WP4** | frontend | 통역 모달 — AudioWorklet PCM 송신 · 자막 말풍선 · 오디오 재생 · 상태 4종 · 언어 선택 | §7 · §2 | WP3 · WP2 | tsc · lint · build |
| **WP5** | 코디 + 사용자 | 로컬 E2E — §9 1~6 을 실제로(통역은 실제 Soniox) · 사용자가 움직여 시드 지정 | §9 | WP1~4 | 사용자 표면(노트북 브라우저)에서 확인 |

순서: WP1 ∥ WP3 → WP2 → WP4 → WP5. **2026-10-13: WP1~WP4 완료(코드 `kknaksss/sts-prototype` 470b3f7) — WP4 는 WS 계약(`interpret-ws-contract.md`)을 먼저 정해 WP2 와 병렬로 했다. WP5(사용자 E2E) 대기.** 각 WP 끝마다 그 WP 관련 시험만, 전체 검증은 WP5 에서 한 번.

## 2차 — SPEC 0.2.0 반영 (2026-10-13 E2E 1차 뒤)

| WP | 담당 | 내용 | 선행 | 완료 조건 |
|---|---|---|---|---|
| **WP6** | frontend(시안) | claude design r4 — 방 패널 고객 중심(단계별 배정 · 시술 추가 · 순서 바꾸기 · 수면시술실 · 귀가) · 접수 모달(단계 고르기) · 순회형 손 필요 표시 · 범례 5직군 · 접수대기실/수면시술실 이름 | SPEC 0.2.0 | 사용자 눈 확인 |
| **WP7** | backend | SPEC 0.2.0 §4~§6 · §9 — 단계 모델 · 조작 API · 5직군 · 시드 개원 전 · 메모 공개 시점 · KOS 주석 | SPEC 0.2.0(WP6 과 병렬) | pytest · ruff · 이름 대조 |
| **WP8** | frontend | SPEC 0.2.0 §3 화면 — r4 시안대로 | WP6 · WP7 | tsc · lint · build |
| ~~WP6 · WP7 · WP7b · WP7c · WP8~~ 완료 2026-10-13(코드 `9f8f712`) | | | | |
| ~~WP10 · WP11 · WP12 · 배포~~ 완료 2026-10-13 — https://ccc.medisolveai.xyz (코드 `2abe704` · infra PR #16 #17) | | | | |
| **WP9** | 코디 → 사용자 | 코디가 §11 수락 기준을 실제 화면으로 끝까지 → 사용자 E2E | WP7 · WP8 | 사용자 표면 |

## 검수

- WP1 · WP3 끝나면 reviewer 1회(계약 대조 · 기능 독립 · 실데이터 노출)
- FAIL 지적은 원 워커에게 재발주

## Risks

| 위험 | 대응 |
|---|---|
| 시드 재구성이 근사라 현황판이 어색함 | 사용자가 움직여 고친 뒤 `seed save`(SPEC §4.3) |
| 메모 이름 치환 누락 | WP1 시험에 캡처 `visitor.name` · 메모 「이름 :」 값 전수 대조 |
| Soniox 번체 · 광둥어 · 음색 미확인 | WP2 첫 단계 실물 호출(§7.3) |
| 금요일까지 4일 | WP1 ∥ WP3 병렬 · E2E 피드백은 모아서 한 번에 재발주 |
