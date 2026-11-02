# 조직 화면 v3 2단계(읽기 API 소비) 결과 보고 — frontend

- 작업일: 2026-09-08 · 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `5f8b608`, 커밋 없음)
- 계약: 브리프 §3(코디 결정 2026-09-08) + `backend/tests/contract/test_organization_member_axes.py` + HANDOFF.md

## 상태: done

---

## 1. 한 일

| # | 항목 | 결과 |
|---|---|---|
| 1 | `api.ts` 에 request 3개 + 타입 3개 | `getOrganizationMemberAxes` · `getOrganizationMemberHistory` · `getOrganizationActivity`. **95줄 추가 · 0줄 삭제**(추가만) |
| 2 | 패널 ③ 데이터 소스 교체 | `GET /api/organization/members/{id}` **한 번**으로 6축·재직·계정·권한·회수분. 1단계의 「목록 응답 + `access/members` 조합」을 걷어냈다 — 테스트가 `/api/access/members/` 호출 0 을 지킨다 |
| 3 | 「이력」 활성 | 5개 축(소속·직책·직급·직무·권한)이 `history?axis=` 를 불러 Popover 로 편다. 계층만 disabled |
| 4 | 회수된 권한 절 | `revoked_grants` 1건 이상일 때만. 11px Bold 헤더 · 12px 행 · 우측 기간 tabular · `--ai-border` 구분선 · 3건 초과면 「n건 더 보기」 토글 |
| 5 | 계정 배지 | `has_account` → 「로그인 계정 있음」 / 「계정 없음」(`badge neutral`) |
| 6 | 변경 기록 테이블 | `.plain-table` 120/280/80/가변/120 · 축 배지(권한=`badge ai`, 그 밖=`badge neutral`) · 「더 보기」 · 선택 조직 연동 · 0건이면 `Empty variant="filter"` |
| — | 안 그리는 것 유지 | 소속·직책 「변경」 · 행 메뉴 `⋯` — command·envelope 가 여전히 없다 (SPEC-005 §5) |

## 2. 판단이 필요했던 세 곳 (브리프와 다르게 한 것 포함)

### 2-1. 「이력」을 그릴지 말지의 사전 판단 — **브리프의 heuristic 을 쓰지 않았다**

브리프: 「응답의 민감 필드가 null 이면 자격 없음으로 간주」.
**쓸 수 없었다.** 서버가 가리는 필드는 `phone`·`birth_date`(→ null)와 `grants`·`revoked_grants`(→ [])인데,
- SC 데이터는 **전화 열을 반입하지 않았다** — 165명 전원 `phone === null`. 이 heuristic 이면 대표에게도 「이력」이 안 그려진다.
- `grants: []` 는 「볼 자격이 없다」와 「권한이 하나도 없다」를 구별하지 못한다. 응답의 모양이 누구에게나 같게 설계된 것이 그 이유다(계약 테스트가 그걸 못박는다).

그래서 **서버와 같은 술어를 화면에도 세웠다**: `canReadSensitive = 본인이거나 organization.manage 를 가졌는가`
(`application.py:_may_read_sensitive` 와 같은 기준). 관리 범위가 조직 일부인 사람은 여기서 참이어도 서버가 403 을 줄 수 있고, **그때는 Toast error** 로 말한다 — 브리프의 「호출 후 403 이면 Toast error」는 그대로 지켰다.

### 2-2. 계층 축의 「이력」 — **그리되 눌리지 않게 두었다**

`MEMBER_HISTORY_AXES` 는 `membership · appointment · grade · job · grant` 다섯이다. 계층은 없다 — 계층은 소속이 지나온 길을 다시 그린 것이라 스스로의 이력을 갖지 않는다. 없는 축을 소속 이력으로 몰래 바꿔치기하면 「계층 이력」이라 적힌 팝오버에 팀 이름 목록이 나온다. 그래서 `disabled` + `title="계층은 소속 축의 이력이 말합니다"` 로 두었다(행 정렬도 유지된다).

### 2-3. 날짜 문법 — **핸드오프의 마침표 대신 제품의 슬래시**

핸드오프는 `2025.03.02 – 2026.01.14` 이지만, `labels.ts:formatDate` 는 「읽기 전용 날짜는 **어느 화면에서나** `YYYY/MM/DD`」라고 못박고 있고 캘린더·업무·보고가 모두 그 문법이다. 한 제품에 날짜 문법을 둘 두지 않기로 하고 `formatPeriod` 를 `2025/03/02 – 2026/01/14` 로 만들었다(끝나지 않은 기간은 「현재」).
변경 기록의 시각은 컬럼이 120px 이라 새로 만들었다 — `formatActivityTime`: 오늘은 「오늘 12:15」, 올해는 「08/27 10:05」, 그 밖은 「2025/08/27 10:05」. 핸드오프의 「오늘 09:12」·「08.27 10:05」과 같은 규칙이고 구분자만 제품 문법이다.

## 3. 고친 결함 1건 — 이력 팝오버가 패널 밖으로 나가 잘렸다

첫 브라우저 확인에서 **폭 400 팝오버가 오른쪽으로 249~289px 삐져나갔다.** 원인 둘:

1. `.popover { left: 0 }` — 트리거의 왼쪽에서 오른쪽으로 자란다. 「이력」은 패널 **오른쪽 끝**에 서 있어서 자랄 자리가 없다.
2. `.org-panel { overflow: hidden }` — 패널이 팝오버를 그대로 자른다. 문서 가로 스크롤은 0 이라 **삐져나간 줄도 모르고 잘린다.**

수정(둘 다 allowed_paths 안):
- `styles.css` **+1 규칙**: `.org-panel .popover { left: auto; right: 0 }` — 이 패널 안에서만 오른쪽에 맞춰 왼쪽으로 편다.
- 팝오버 폭 **400 → 320**. 1440 에서 상세 패널이 400px 로 줄어(v3 그리드) 좌우 패딩 48 을 빼면 352 다. 400 은 그 폭에서 반드시 잘린다. 320 은 v2 `14` 의 **200–400 범위 안**이다.

수정 후 네 조합(대표·팀장 × 1920·1440) 전부 **아래/위/오른쪽 삐져나감 0**.

> `Popover.tsx` 는 allowed_paths 밖이라 손대지 않았다. 다만 이력은 팝오버가 열린 **뒤에** 도착하므로, 도착 시점에 `window.dispatchEvent(new Event("resize"))` 를 한 번 보내 Popover 가 남은 자리를 다시 재게 했다(§6 주의점).

## 4. 검증

```
npx tsc --noEmit                                                   → 0 에러
npx vitest run OrgPage · Popover · DatePicker · MyWorkPage         → 4 파일 54 passed / 54
  ㄴ OrgPage.test.tsx 19개 (1단계 10개 → 재작성·확장)
grep -oE '#[0-9a-fA-F]{3,6}' src/OrgPage.tsx src/org/*.tsx          → 0
grep 'fetch(' src/OrgPage.tsx src/org/*.tsx src/labels.ts           → 0
styles.css diff 에 추가된 hex                                        → 0
git diff --numstat frontend/src/api.ts                              → 95 추가 / 0 삭제 (추가만)
viewModels.ts · idempotency.ts · App.tsx · ds-entry.tsx · backend/ · package.json → diff 없음
```

신규·개정 테스트 19개: 배지 두 관점 · 직원이 남을 볼 때(권한 restricted + 「이력」 0개) · 자기 자신 · **members/{id} 한 번으로 읽고 access/members 를 부르지 않는다** · 「변경」 1개 & 계층 이력만 disabled · **계정 배지 두 값** · 이력 팝오버 열림/기간 「현재」/사유 없음 · **빈 이력** · **403 → 팝오버 + Toast** · **회수된 권한 0 / 1 / 4건(더 보기·접기)** · **변경 기록 0건 / n건+축 배지 / 더 보기 이어붙이기 / 조직 연동** · tree 펼침≠선택 · 회수 순서(Drawer 닫고 ConfirmModal) · 부여 payload.

### 화면표 — 5176 실측 (높이 900)

| 계정 | 폭 | 가로 오버플로 | 헤더 배지 | 「이력」 | 「변경」 | 변경 기록 | 이력 팝오버 (폭 · 화면밖 아래/위/오른쪽) |
|---|---|---|---|---|---|---|---|
| 1001 대표 | 1920 | 0 | 재직 · 로그인 계정 있음 | 6 (계층 1 disabled) | 1 | 표/빈 상태 | 소속 이력 · 320 · **0 / 0 / 0** |
| 1001 대표 | 1440 | 0 | 재직 · 로그인 계정 있음 | 6 (1 disabled) | 1 | 표/빈 상태 | 소속 이력 · 320 · **0 / 0 / 0** |
| 1141 팀장(자기) | 1920 | 0 | 재직 · 로그인 계정 있음 | 6 (1 disabled) | **0** | **없음** | 소속 이력 · 320 · **0 / 0 / 0** |
| 1141 팀장(자기) | 1440 | 0 | 재직 · 로그인 계정 있음 | 6 (1 disabled) | **0** | **없음** | 소속 이력 · 320 · **0 / 0 / 0** |
| 1141 팀장(**남**) | 1440 | 0 | — | **0** | **0** | **없음** | (버튼 자체가 없다) + 「관리 권한이 있는 사람에게만 보입니다」 |

### 변경 기록 표는 실제로 사건을 만들어 확인했다

시드에는 조직 축 사건이 0건이라 처음엔 빈 상태만 보였다. 그래서 **대표(1001)로 화면에서 권한을 한 번 부여했다가 회수**해 실제 사건 2건을 만들고 확인했다:

- 컬럼 폭: `시각:120px · 변경:280px · 축:80px · 사유:가변 · 기록자:120px` — 핸드오프 그대로
- 첫 행: 「오늘 12:15 / role:executive 권한을 the-sc 범위로 부여 / **권한(`badge ai`)** / 2단계 화면 확인용 임시 부여 / 양승철」
- 회수 뒤: 표 2행(둘 다 권한·ai), 상세에 **회수된 권한** 절 등장 — 「대표 · 더에쓰씨 · 2026/09/08 – 2026/09/08」

> **주의**: 이 확인 때문에 로컬 데모 DB 에 `access.grant_added`·`access.grant_revoked` **2건**과 양승철의 **회수된 grant 1건**이 남아 있다(부여한 권한은 곧바로 회수했으므로 유효 권한은 원래대로다). 깨끗한 상태가 필요하면 `make reset-demo` 로 지우면 된다.

## 5. 변경 파일

| 파일 | 변경 |
|---|---|
| `frontend/src/api.ts` | **+95 / -0** — request 3개 + `OrganizationMemberAxes`·`MemberHistoryEntry`·`OrganizationActivityEvent`·`MemberHistoryAxis` 타입 |
| `frontend/src/OrgPage.tsx` | 상세 fetch 를 `members/{id}` 로 교체 · `canReadSensitive` · 변경 기록 조회/페이징/조직 연동 · 이력 403 Toast |
| `frontend/src/org/MemberAxesPanel.tsx` | 축 데이터 소스 교체 · 계정 배지 · 축별 이력 버튼 · 회수된 권한 절 |
| `frontend/src/org/AxisHistoryPopover.tsx` | **신규** — 축별 이력 Popover(헤더 고정 · 빈/403 상태) |
| `frontend/src/org/ChangeLogPanel.tsx` | **신규** — 변경 기록 `.plain-table` · 축 배지 · 더 보기 |
| `frontend/src/org/AccessDrawer.tsx` | `member` prop 을 상세 응답 타입으로(그 외 동작 동일) |
| `frontend/src/labels.ts` | `orgScreen` 카피 확장 + `employmentStateText`·`formatPeriod`·`formatActivityTime` |
| `frontend/src/styles.css` | **+3줄** — `.org-panel .popover { left: auto; right: 0 }` 와 그 이유 주석. hex 0 |
| `frontend/src/OrgPage.test.tsx` | 10 → 19 케이스로 재작성 |

## 6. 미결 · 주의점

1. **`Popover` 는 내용이 뒤늦게 커지는 것을 스스로 모른다.** 이력은 열린 뒤에 도착하므로 `AxisHistoryPopover` 가 `resize` 이벤트를 한 번 쏴서 다시 재게 했다. 제대로 된 자리는 `Popover.tsx` 안의 `ResizeObserver` 인데 allowed_paths 밖이라 두었다 — 다음에 Popover 를 만질 때 한 줄이면 된다.
2. **팝오버가 패널 밖으로 못 나간다.** `.org-panel { overflow: hidden }` 이라 팝오버는 패널 안에서만 산다. 지금은 폭 320 으로 들어가지만, 앞으로 더 넓은 팝오버가 필요하면 `Popover` 를 portal 로 띄우는 편이 낫다.
3. `api.ts` 의 `getMemberAccess` 는 이제 부르는 곳이 없다(브리프가 「추가만」이라 지우지 않았다). 권한 변경 Drawer 의 부여/회수는 브리프대로 `/api/access/*` 를 그대로 쓴다.
4. 이력의 `reason` 은 축마다 성격이 다르다 — 권한 축은 사람이 쓴 사유가 오지만, 소속·직책은 `change_reason_ref`(참조 문자열), 직급·직무는 늘 `null` 이라 「사유 없음」으로 보인다. 서버가 주는 그대로 그렸다.
5. 부서장 `1106`·팀원 `1107` 은 이번에도 `scax-demo-1234` 로 로그인이 401 이라(1단계 보고와 동일) 직원 관점은 팀장 `1141` 로 확인했다 — 자기 자신과 남을 각각 봤다.
