# 시나리오 파일 형식 — researcher(만듦) ↔ backend WP7b(읽음) (코디 결정 2026-10-13)

위치: `cc/back/data/scenario/` (gitignore — 실데이터 원문이 섞인다). 필드 이름은 **KOS 응답 이름을 그대로** 쓴다(있는 것만).

## seed.json — 「아침에 KOS 에서 받아 온 것」

```json
{
  "date": "2026-10-09",
  "schedules": [
    { "id": "<scheduleId>",
      "reservation": { "startDateTime": "...Z", "status": "RESERVED", "reservationMemo": "...", "reservationGroupId": "...", "funnel": {...}|null },
      "visitor": { "id": "...", "name": "<가짜>", "isNew": true, "nationality": "TW", "gender": "FEMALE", "dateOfBirth": "YYYY-MM-DD", "memo": "" },
      "scenario": "S1", "scriptFrom": "<대본 10-09 scheduleId>" }
  ],
  "ticketBundles": { "<visitorId>": [ /* getTicketBundlesQuery.data[] 모양 그대로 — AVAILABLE 장 포함 */ ] },
  "pastSchedules": { "<visitorId>": [ { "date": "YYYY-MM-DD", "consultations": [ {"counselors":[{"id","name"}], "content":{"text":"..."}} ], "orderMemo": "...", "procedures": [ {"title":"..."} ] } ] }
}
```

## events/<scheduleId>.json — 「진행하다 KOS 에서 들어오는 것」

```json
{
  "consultationDone": {
    "consultation": { "counselors": [{"id","name"}], "content": {"text": "..."} },
    "orderMemo": "...",
    "tasks": [ /* 상담사가 넣은 시술 — getScheduleDetail.data.tasks[] 모양(PROCEDURE · ETCETERA 원장 상담), sequence · title · procedureConfiguration(시술권 전이면 ticketConfiguration {}) · paymentRequired:true */ ],
    "payment": { "totalAmount": 1280000, "items": [ /* getPurchaseItemStatistics.data[] 에서 productTitle · productOptionTitle · cost */ ] }
  },
  "paymentDone": { "ticketIdsBySequence": { "2": "<ticketId>", "3": "<ticketId>" } },
  "taskDone": { "<sequence>": { "assigneeMemo": "..." } }
}
```

- 이름 치환은 D-09(고객 · 동행인 이름만 가짜, 메모 본문 포함). 직원 id · 이름은 `kos-staff.json` 실제 값
- 시드에 없는 장면(재내원 · 남은 시술권 · 지난 상담)은 같은 모양으로 만든다 — 만든 값은 `"synthetic": true` 표시

## 추가 (2026-10-13) — 오늘 근무 직원 `staffIds`

seed.json 최상위에 `"staffIds": ["<kos-staff id>", ...]` — **오늘 근무 직원(더미 스케줄)**. 로그인 목록 · 배정 후보 = 이 목록 + 데스크.
- 인원(사용자 지정): **의사 2 · 코디 3 · 간호사 4 · 피부관리사 2** + 상담사는 이벤트에 나오는 상담사(2~3명)
- 실제 `kos-staff.json` 직원 중에서 직군 태그가 맞는 사람을 고른다(10-09 에 나온 사람 우선). 「마취용」 제외
- 이벤트(`consultationDone.consultation.counselors`)의 상담사는 이 목록 안에 있어야 한다. 이벤트 `tasks[].doctors` · `assignees` 는 **비워 둔다**(배정은 데스크 몫 — 사후 값 금지)
- `staffIds` 가 없으면 back 은 이벤트 등장 직원 + COORDINATOR 활성 직원으로 대체(백업 규칙)
