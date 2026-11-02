# 앱 계약 후속 — 구현 중 정해진 빈칸 (코디 · 2026-10-27) · 다음 planner 판에 SPEC-004 로

| # | 자리 | 정한 것 | 근거 |
|---|---|---|---|
| 1 | §5-3 띄우기 pending · claim 응답 | 항목 = `{requestId, kind, reservationId, customerId, deviceId, status, expiresAt}` · `GET pending` = `{items:[항목]}`(그 기기 pending + 이미 opened · 오래된 것 먼저 · 돌려주며 opened) · `POST claim` = 항목 하나 | backend 질문 · 코디 OK |
| 2 | §6.15 문진 prefill | `prefill.dateOfBirth` = `yyyyMMdd`(KOS 양식 그대로) | backend BE4 보고 |
| 3 | §5-4 알림 읽음 | `POST /api/notifications/read` 본문 `ids?` · `callId?` · `reservationId?` · 응답 `{ok:true, read:N}` | backend BE1 보고 |
| 4 | §5-4 알림 목록 | `items[].target` = `{visitId?, callId?, reservationId?}`(`callId` 더함) | backend BE1 보고 |
| 5 | §6.15 문진 prefill | `prefill.phone` = `{countryCode, phoneNumber}` | backend BE4 보고 |
| 6 | §6.16 스캔 응답 | `PROC_PHOTO_DIR` 비면 `photo = {ccc:"disabled", kos:"skipped"}` · `photoId: null` — enum 에 `skipped` 더함 | backend BE5 보고 |
| 7 | §6.17 · 상세 응답 | `customer.identity.photoKos`: `ok` \| `failed` \| `skipped` \| null(`id_photo.kos_status`) — 웹 「KOS 사진 실패」 표시 | frontend 질문 · 코디 OK |
