# 「특이사항」 = `visitor.memo` 확인 — 데모 쓰기 1건

- 시험일: 2026-10-26 (KST) · 시험자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-reception-test-report.md`(아래 `RT§`)에서 이어진다
- 허가 범위: 지시서의 쓰기 1건뿐
- 테넌트 · 키 확인은 앞 판 §0 과 같다
  - 스크립트 `assert`: 테넌트 = 데모, 공개 키 = `KOS_API_tenent_dev` ≠ 운영 키
  - 이번 실행은 허가 경로를 `visitor/v2/commands/update-visitor-management-information` **하나로 좁혔다**
- 대상: 앞 판 시험 A 일정의 고객 1명(데모 기존 고객)
- 리포트에 id · 이름 등 값은 적지 않았다

---

## 0. 결론

1. **KOS 웹 「특이사항」 = 고객 `memo` 필드다**(JS · 데모 확인)
   - 웹앱 고객 정보 창의 「특이사항」 입력칸(높이 120 textarea)은 `value = visitor.memo` · `onChange → memo` 로 묶여 있다
   - 고객 요약 · 일정 패널의 「특이사항」 칸도 `memo` 를 보인다(JS `visitorInformation.common.specificRemarks` 라벨 → `memo`)
   - 저장할 때 바뀐 칸을 고르는 표에서도 `memo` 는 관리 정보 묶음의 「특이사항」 항목이다
   - 데모에서 메모를 바꾼 뒤 내부 `get-visitor.memo` · 공개 `getScheduleDetail.visitor.memo` · 내부 일정 상세 `visitor.memo` 가 모두 시험 문구가 됐다
   - ⚠ **공개 `getVisitor` 에는 `memo` 키가 없다**(응답 키 7개). 공개로 특이사항을 읽는 곳은 **일정 응답의 `visitor.memo`** 다
2. **관리 정보 묶음을 「읽은 값 그대로 + memo 만 바꿔」 보내면 memo 와 수정 시각 말고는 아무것도 바뀌지 않는다**(키 36개를 하나씩 비교)
   - 본문에서 **빼고 보냈을 때** 다른 필드가 지워지는지는 시험하지 않았다(허가 1건) → Q-79

---

## 1. 근거 — JS(웹앱 `visitor-information_v0.0.157`)

| 위치 | 내용 |
|---|---|
| 고객 정보 수정 창 | 라벨 `basicInformation.input.specificRemarks.label` = 「특이사항」 → `<textarea value={memo} onChange={memo:e}>` |
| 저장 diff 표(관리 묶음) | `memo: {key: …specificRemarks.label}` · `visitorFunnel` · `referrer` · `visitorType` · `visitorCategories` … — **memo 는 관리 정보 묶음**이다(개인 정보 묶음이 아니다) |
| 고객 요약 · 일정 패널 | 「특이사항」 칸 = `memo` |
| 관리 정보 저장 요청 | `update-visitor-management-information` ← `{id, memo, visitorFunnel, referrer(→ visitor/account/unregistered 중 하나로 펼침), visitorType, visitorCategories[], doctor, counselor, aggrementPersonalInformation, aggrementAdvertisements, agreementInformationalNotification, customAttributes[]}` |
| JSON 인코딩 | 값이 `undefined` 인 칸은 빠진다. 빈 배열(`visitorCategories` · `customAttributes`)도 빠진다. 추천인(`referrer`)은 `$case` 에 따라 최상위 `visitor{visitorId}` · `account{accountId}` · `unregistered{name}` 중 하나로 나간다 |

---

## 2. 쓰기 1건

### 2.1 보낸 본문(모양)

내부 `visitor/v2/queries/get-visitor` 로 읽은 응답에서 관리 묶음 키를 **그대로 복사**했다. 다른 점은 `memo` 하나다.

| 키 | 보낸 값 |
|---|---|
| `id` | 고객 id |
| `memo` | **`[ccc 시험] 특이사항 확인`**(전에는 빈칸) |
| `visitorFunnel` | 읽은 값 `{funnelCategoryId, funnelId, funnelDetail}` |
| `unregistered` | 읽은 값 `{name}`(추천인 — 이 고객은 「미등록」 꼴로 들어 있었다) |
| `visitorType` | 읽은 값 `{id, name}` |
| `visitorCategories` | 읽은 값(1개, `{id, name, order, color}`) |
| `doctor` · `counselor` | 읽은 값 `{id, name}` |
| `aggrementPersonalInformation` · `aggrementAdvertisements` · `agreementInformationalNotification` | 읽은 값(bool 3개) |
| `customAttributes` | 읽은 값이 `[]` 라서 웹앱처럼 **뺐다** |

### 2.2 결과

| 순서 | 호출 | 결과 |
|---|---|---|
| W | `POST api.kos-solution.com/tenants/{tenantId}/visitor/v2/commands/update-visitor-management-information` | **200** `{}` |
| 조회 | 3초 뒤 4곳 다시 읽기 | 모두 200 · 메모 반영됨 |

---

## 3. 전후 비교 (필드마다)

| 조회 | 키 수 | 바뀐 키 | memo |
|---|---|---|---|
| 내부 `visitor/v2/queries/get-visitor` | 36 | **`memo` · `updatedDateTimeUtc`** 뿐 | 빈칸 → 시험 문구 |
| 공개 `getScheduleDetail.data.visitor` (A 일정) | 13 | **`memo`** 뿐 | 빈칸 → 시험 문구 |
| 내부 `schedule/v1/queries/get-schedule-detail.data.visitor` | 13 | **`memo`** 뿐 | 빈칸 → 시험 문구 |
| 공개 `getVisitor` | 7 | 없음 | **키 없음**(이 응답에는 memo 가 나오지 않는다) |

내부 고객 키 36개 중 바뀌지 않은 것
- 개인 정보: `name · phoneNumber · dateOfBirth · gender · nationality · language · registrationNumber · foreignRegistrationNumber · passportNumber · address · snsInfo · email`
- 관리 정보: `visitorFunnel · funnel · detailedFunnel · unregistered · recommenderName · visitorType · visitorCategories · doctor · counselor · 동의 3개 · customAttributes`
- 그 밖: `migratedMemo · chartNumber · isNew · lastVisitedDateTimeUtc · lineInformation · unniInformation · createdDateTimeUtc · deleted` 등

결론: **읽은 관리 정보를 그대로 함께 보내면 메모만 바뀐다**(확인). 앞 판 문진 제출(Q§4.2)과 달리 이 작업은 `updatedDateTimeUtc` 를 바꾼다.

---

## 4. 「메모만 바꾸려면 무엇을 같이 보내야 하나」

- **확인된 길**: 내부 `get-visitor` → 관리 묶음 키(`visitorFunnel · 추천인(visitor/account/unregistered) · visitorType · visitorCategories · doctor · counselor · 동의 3 · customAttributes`)를 읽은 그대로 → `memo` 만 바꿔 `update-visitor-management-information`. 웹앱도 같은 방식(읽고 → 고치고 → 묶음 전체)이다
- **확인 안 된 것**: 묶음 키를 빼고 `{id, memo}` 만 보내면 나머지가 지워지는지 · 그대로 남는지. 웹앱 JSON 인코딩은 빈 배열 · undefined 를 빼므로, 서버는 「안 보냄」과 「비움」을 구분하지 못할 수 있다(추정) → Q-79
- 공개 API 로 메모를 쓰는 길은 없다(U§2.3 · 스펙 쓰기 25개 grep 결과와 같다)

---

## 5. 호출 기록

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| **쓰기 · 내부** | `visitor/v2/commands/update-visitor-management-information` | **1** | 200 |
| 조회 · 내부 | `visitor/v2/queries/get-visitor` 2 · `schedule/v1/queries/get-schedule-detail` 2 | 4 | 200 |
| 조회 · 공개 | `getScheduleDetail` 3 · `getVisitor` 2 | 5 | 200 |
| 인증 | 공개 `exchange-token` 1 · 내부 sign-in 1 | 2 | 200 |

- 허가 밖 쓰기 0건, 운영 키 0건
- **되돌리지 않았다** — 이 고객의 특이사항에는 `[ccc 시험] 특이사항 확인` 이 남아 있다

---

## 6. 정할 것 (결정하지 않음)

| # | 자리 | 왜 정해야 하나 |
|---|---|---|
| Q-79 | 메모만 보낼 때(`{id, memo}`) 나머지 관리 정보가 지워지는가 | 이번에는 읽은 값을 다 보내서 안전했다. 빼고 보냈을 때의 동작은 쓰기를 한 번 더 해야 안다. ccc 는 웹앱처럼 「읽고 → 묶음 전체」로 보낼지, 시험을 한 번 더 허가할지 |
| Q-80 | 공개로 특이사항을 읽는 곳 | 공개 `getVisitor` 에는 memo 가 없다. 일정 응답의 `visitor.memo` 로 읽을지, 내부 `get-visitor` 를 쓸지 |
| Q-81 | 읽기 → 쓰기 사이의 동시 수정 | 묶음 전체를 다시 보내므로, 그 사이에 KOS 웹에서 누가 유입 · 분류 · 담당을 바꾸면 ccc 가 옛 값으로 덮어쓸 수 있다(추정). 쓰기 직전에 다시 읽을지 |
| Q-82 | **사용자 눈 확인** | KOS 웹 고객 정보 「특이사항」에 시험 문구 `[ccc 시험] 특이사항 확인` 이 보이는지 사람이 확인해야 한다(대상 = 앞 판 시험 A 일정의 고객 · 오늘 4층 · 상담 대기 · A-룸7) |
