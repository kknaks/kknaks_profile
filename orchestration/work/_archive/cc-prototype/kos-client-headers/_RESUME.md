# 재개 노트 — kos-client-headers (cc-prototype)

**지금**: 운영 배포 완료(back 77173cf) · 403 0 · 사용자 화면 확인 대기
**다음**: 사용자 고객 검색 확인 → deploy.md 이력 행 · 마감(archive-work.sh)

세팅: `scripts/new-work.sh cc-prototype kos-client-headers` · 설정 SSOT `config/projects/cc-prototype.json`
코디handle: `term_2d7ec4cc-e726-4453-a485-d88d4284f1ec` · run `run_d8d7e35e00fe`

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/cc-prototype/kos-client-headers` (branch `kknaksss/kos-client-headers`, base `origin/main` → PR `main`)

## 1. 지금

- [ ] 사용자 화면 확인 — 고객 검색 · KOS 쓰기(예약 등록)
- [ ] deploy.md 이력 행 추가 · 마감

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-04 | 원인 = KOS 내부 API 가 11-03 18:23 KST 부터 비브라우저 UA 를 `403 Unsupported client.` 로 막음 | 운영 pod 재현 — sign-in · get-rooms 가 브라우저 UA 만 붙이면 200, Origin · Referer · kos-client-uri 만으론 403 |
| 2026-11-04 | 내부 API 요청에 UA + Origin + kos-client-uri 를 같이 넣는다. 공개 API · presigned PUT 은 그대로 | 사용자 지시(「오리진이랑 uri 도 같이」) |
| 2026-11-04 | 핫픽스 — SPEC 개정 없이 브리프가 계약 | 사용자(「핫픽스로 나가야 하니까 발주」) |

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| (없음 — backend `ctx_3170eacf5471` 완료 · release) | | | | | |

## 4. 산출물

- code PR: kknaksss/cc-prototype#20 (스쿼시 `77173cf`)
- infra PR: MediSolveAIDev/k8s_infra_mac#47 (`5ebc4dc`, back.imageTag) · infra 워크트리 `orca/workspaces/k8s_infra_mac/kos-client-headers`

## 5. 이력 (최신이 위)

- `2026-11-04` 배포 — ArgoCD Synced Healthy · back 새 pod 403 0 · health kos open/internal true · 내부 토큰 · 직원 80 · 방 28
- `2026-11-04` 운영 pod httpx 실호출 — 헤더 넣으면 sign-in · user-account · rooms · schedules · visitors 200(기본 UA 403)
- `2026-11-04` 운영 고객 검색 「요청을 처리하지 못했어요」 → 원인 확인 · 발주
