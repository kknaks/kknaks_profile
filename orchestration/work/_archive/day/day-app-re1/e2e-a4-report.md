# e2e A4 — 로컬 BE(43ba40a3) + KOS 데모 지점 실물 호출 (코디 · 2026-11-25)

스택: 코드 워크트리 `./start.sh --kos-demo --scheduler`(:11040 · migration head 0028 · seed-demo 데모 연결) · 앱 로그인 `POST /api/auth/login client=app` → Bearer(테스트 계정 · 간호 · board edit)
대상 방문: 판 카드 `3cc93bd6…`(A-룸4 · 시술 2줄)

| # | 호출 | 결과 |
|---|---|---|
| 1 | GET /api/visits/{id}/chart | 200 · tasks 2 · base.body null(처음 쓰는 줄) |
| 2 | POST …/chart assignee(baseLogId null · baseBody "") | 200 · saved 1 · 새 logId · author · savedAt · outbox `sent: 1`(worker 로그) |
| 2′ | 같은 요청에 baseBody **null** | 400 invalid_request field rows.0.baseBody — 계약 C2(문자열) 그대로. 앱은 `chart_controller.dart:156` 에서 null → "" 로 보냄 → 문제 없음 |
| 3 | 옛 기준으로 다시 저장 | 409 chart_conflict · details.conflicts[0].body = 「저장 1\n옛 기준 저장」(서버가 이어 붙임) |
| 4 | POST …/photos before + JPEG 2 | 200 · kosSynced true ×2 · kosError null · rejected [] |
| 5 | GET …/photos · ?poll=1 · ?tick=1 | 200 · 두 묶음(시술 전 2 · 시술 후 0) |
| 6 | GET …/photos/{id}/file (Bearer) | 200 · image/jpeg · no-store · inline · nosniff |
| 7 | POST …/delete | 200 · 1장 남음 · kosError null |
| 8 | POST …/kos-retry(이미 반영된 장) | 200 · kosSynced true |
| + | staffId null | 409 chart_staff_required(계약대로) · 칸 생략 = 400 invalid_request |

판정: **PASS**. 확인 못 한 것: KOS 웹 화면에서 사진 · 메모 눈 확인(로그 · 응답의 kosSynced 로 대신) · Caddy 100MiB(로컬엔 Caddy 없음 — 배포 때).
데모 지점에 남은 것: 메모 「[e2e 앱 경로] 저장 1」 · 사진 1장(단색 테스트 이미지).
