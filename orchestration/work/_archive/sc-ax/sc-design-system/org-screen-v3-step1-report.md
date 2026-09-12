# 조직 화면 v3 1단계(읽기 전용) 결과 보고 — frontend

- 작업일: 2026-09-07 · 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-design-system` (HEAD `ceecbe9`, 커밋 없음)
- 계약: `reference/2026-09-09-sc-ax-design/org-chart-template/HANDOFF.md` + 코디 결정(브리프 §3)

## 상태: done

---

## 1. 그린 것 / 안 그린 것 (브리프 §3 항목별)

| 핸드오프 요소 | 이번에 | 근거 |
|---|---|---|
| 3분할 그리드 (392 · 1fr · 600, gap 24, `calc(100vh - 300px)`/min 560) | **그림** | 1920 에서 정확히 392·600·600 = 1640 (§4 화면표) |
| 패널 외곽 `--border-strong` · `--radius-panel` · 내부 스크롤 · 헤더 고정 | **그림** | `.org-panel` / `.org-panel-scroll` |
| 헤드 배지 — 관리자 `badge ai`「조직 관리 권한 있음」 / 직원 `badge outline`「읽기 전용」 | **그림** | `me` 의 capability 에 `organization.manage` 가 있는가 |
| 패널 ① tree — chevron 펼침 ≠ 선택, 직접/전체 카운트, 노드 종류, 리더 `avatar xs` | **그림** | `tree` 응답의 `direct_member_count`·`member_count`·`unit_type`·`leaders` |
| 패널 ① 이름 검색 → 트리 필터 (클라이언트) | **그림** | 루트 unit 의 `units/{root}/members` 를 한 번 받아 이름 색인으로 쓴다 (기존 엔드포인트, 새 API 아님) |
| 패널 ② 행 68 · 사번 · `avatar sm` · 이름 · 소속 요약 「(주)·(겸직)」 · 직급 | **그림** | 사번 자리 = `member.member_id` (임시 사번 key) |
| 패널 ② 선택 행 `--surface-selected-row` · hover `--surface-sunken` · 로딩 Skeleton · 실패 `Empty error` | **그림** | |
| 패널 ③ 헤더 `avatar lg` · 이름 20 · 사번 · 「재직」 배지 + 「재직과 계정은 다른 축입니다」 | **그림** | |
| 패널 ③ 축 5행(계층·소속·직책·직급·직무) + 권한 강조 박스 + 축별 원칙 문구 6개 | **그림** | 문구는 전부 `labels.ts` |
| 「이력」 버튼 (6개) | **그림 · `disabled` + `title="이력 조회는 준비 중"`** | 축별 이력 API 없음 (브리프 §3) |
| 권한 축 「변경」 → `Drawer label="권한 변경"` | **그림** | `POST /api/access/grants` · `/grants/{id}/revoke` 는 이미 있다 |
| 회수 → Drawer 닫은 뒤 `ConfirmModal`(destructive, 사유 필수) → `Toast` | **그림** | Drawer 위에 모달을 겹치지 않는다 (DS 규칙) |
| 하단 변경 기록 (관리자만) — 헤더 + `Empty variant="filter"` | **그림 (테이블 없음)** | 조회 API 없음 |
| **소속·직책 「변경」 버튼** | **안 그림** | 소속·직책 command 가 BE 에 없다 (SPEC-005 §5) |
| **행 메뉴 `⋯`** | **안 그림** | 가능한 행동 envelope 가 없다 |
| **「로그인 계정 있음」 배지** | **안 그림** | 응답에 계정 유무가 없다 — 「재직」만 |
| **변경 기록 테이블 마크업** | **안 그림** | 위와 같음 |
| **「회수된 권한」 절 / 「N건 더 보기」** | **안 그림 (절 자체 생략)** | §2 참조 — 응답에 회수분이 없다 |
| **소속 변경 Drawer (핸드오프 §3 화면)** | **안 그림** | command·preview API 없음 |
| 프로토타입 전용 좁은 창 CSS | **안 옮김** | 핸드오프 지시 |

## 2. 회수된 권한 — 어느 쪽이었나

**응답에 회수분이 없다 → 절 자체를 생략했다.**

근거(BE 코드, 읽기만 함): `platform/organization_access.py:78` 의 `profile_for` 가 grant 를 고를 때
`AccessGrantRecord.revoked_at.is_(None)` 로 거른다. `modules/organization_access/administration.py:84` 의
`member_access` 는 그 `profile["grants"]` 를 그대로 내보낸다. 즉 `GET /api/access/members/{id}` 는
**구조적으로 회수된 grant 를 담지 않는다** — 데이터가 없어서가 아니라 쿼리가 거른다.
회수 이력을 보이려면 BE 응답 확장이 필요하다(조사 리포트 D9).

## 3. 권한 축의 세 관점 (403 버그 수정 포함)

| 보는 사람 | 대상 | 결과 |
|---|---|---|
| 관리자(`organization.manage`) | 누구나 | `GET /api/access/members/{id}` 의 grants + 「변경」 |
| 직원 | **자기 자신** | `me.grants` 로 채운다 (호출 없음) |
| 직원 | 남 | 값 자리 `EmptyValue` + 「관리 권한이 있는 사람에게만 보입니다」 |
| 관리자인데 호출 실패(403·5xx) | — | **`Empty variant="error"`** — 예전엔 스켈레톤이 영원히 남았다 |

권한을 못 읽은 자리에는 「변경」도 열어 주지 않는다(`access.status === "ready"` 일 때만 렌더).

## 4. 화면표 — 세 폭 × 두 관점 (Playwright, 5176 실측)

| 계정 | 폭 | 가로 오버플로 | 헤드 배지 | 변경 기록 | 「변경」 | 「이력」 | 행 메뉴 | 패널 폭 (↕=내부 스크롤) |
|---|---|---|---|---|---|---|---|---|
| 1001 (대표·관리) | 1920 | **0** | 조직 관리 권한 있음 | 있음 | 1 | 6 전부 disabled | 0 | 392 · 600 · 600 |
| 1001 | 1440 | **0** | 조직 관리 권한 있음 | 있음 | 1 | 6 전부 disabled | 0 | 259 · 373 · 400 |
| 1001 | 1280 | **0** | 조직 관리 권한 있음 | 있음 | 1 | 6 전부 disabled | 0 | 308 · 380 · 448 |
| 1141 (팀장·직원) | 1920 | **0** | 읽기 전용 | 없음 | **0** | 6 전부 disabled | 0 | 392↕ · 600 · 600 |
| 1141 | 1440 | **0** | 읽기 전용 | 없음 | **0** | 6 전부 disabled | 0 | 259↕ · 373 · 400 |
| 1141 | 1280 | **0** | 읽기 전용 | 없음 | **0** | 6 전부 disabled | 0 | 308↕ · 380 · 448 |

세 패널 모두 `overflow-y: auto` — 내용이 길면 패널 안에서만 스크롤한다(위 ↕).

> 브리프의 팀원 `1107`·부서장 `1106` 은 **로그인이 401** 이다(`/api/auth/providers` 에는 계정이 있는데
> `scax-demo-1234` 가 통하지 않는다). 직원 관점은 로그인이 되는 팀장 `1141`(`organization.manage` 없음)로
> 확인했다. 관점 차이를 보는 데는 같은 조건이다.

## 5. 핸드오프 ↔ DS 충돌 1건 (새로 발견 — 판정 필요)

**1281~1440 에서 핸드오프의 최소폭이 셸에 들어가지 않는다.**

- DS 셸: 사이드바 200 + `.canvas` 여백 80(`styles.css` `@media (max-width:1440px)`) → 1440 에서 본문 **1080**
- 핸드오프 최소폭 합: 300 + 380 + 440 + gap 48 = **1168**
- 그대로 두면 1440 에서 가로 8px 오버플로가 났다(실측).

처리: 1281~1440 구간에서만 세 열을 **1920 과 같은 비율**(24% · 1fr · 37%)로 줄였다.
1920 에서는 핸드오프 값 그대로(392·600·600), 1280 에서는 사이드바가 빠지고 여백이 48 이 되어
본문 1184 — 핸드오프 최소폭이 그대로 들어가므로 원래 선언을 쓴다.
조사 리포트 §v2↔v3 충돌(X1~X4)에 없던 4번째 충돌이다.

## 6. 변경 파일

| 파일 | 성격 |
|---|---|
| `frontend/src/OrgPage.tsx` | 전면 교체 (414 → 320줄). 상태·fetch 흐름·관리자 판정은 재사용 |
| `frontend/src/org/OrgTreePanel.tsx` | 신규 — 패널 ① |
| `frontend/src/org/MemberListPanel.tsx` | 신규 — 패널 ② |
| `frontend/src/org/MemberAxesPanel.tsx` | 신규 — 패널 ③ + `AccessView`·`grantText` |
| `frontend/src/org/AccessDrawer.tsx` | 신규 — 권한 변경 Drawer |
| `frontend/src/OrgPage.test.tsx` | 신규 — 10 케이스 |
| `frontend/src/labels.ts` | `orgScreen` 카피 묶음 + `membershipSummary()` 추가 (기존 export 불변) |
| `frontend/src/styles.css` | **+15줄** — `.tabular` · `.org-screen-grid`(+1440 미디어쿼리) · `.org-panel` · `.org-panel-scroll` · hover 1줄. hex 0 |

`api.ts` · `viewModels.ts` · `idempotency.ts` · `App.tsx` · `ds-entry.tsx` · `.design-sync/` · `backend/` · `package.json` — **변경 0**.
`styles.css` 의 기존 `.org-grid`(2열, 484줄)와 이름이 겹쳐 새 클래스는 `.org-screen-grid` 로 두었다. 옛 조직 CSS 는 지우지 않았다.

## 7. 검증 결과

```
npx tsc --noEmit                       → 0 에러
npx vitest run src/OrgPage.test.tsx    → 10 passed / 10
grep -oE '#[0-9a-fA-F]{3,6}\b' src/OrgPage.tsx src/org/*.tsx  → 0
grep -n 'fetch(' src/OrgPage.tsx src/org/*.tsx                → 0
git diff --stat -- frontend/src/api.ts                        → (빈 출력) 새 request 호출 0
styles.css diff 에 추가된 hex                                  → 0
세 폭 × 두 관점 가로 오버플로                                    → 전부 0
```

전체 빌드·acceptance-e2e 는 돌리지 않았다(사용자 방침). 다른 테스트 파일은 조직 화면을 건드리지 않는다
(`grep '"조직"' src/*.test.tsx` → `OrgPage.test.tsx` 뿐).

테스트 10 케이스: 관리자 렌더 · 직원 렌더 · 직원의 자기 권한(me.grants) · 소속·직책에 「변경」 없음 + 「이력」 6개 disabled ·
tree 펼침≠선택(양방향) · 이름 검색 필터 · 403 → `Empty error` · Drawer 열림 → 사유 없으면 회수 막힘 → Drawer 닫힌 뒤 ConfirmModal →
revoke 페이로드·Toast · 부여 페이로드·Toast·Drawer 닫힘 · 사번 자리와 행 메뉴 없음.

## 8. 다른 팀 영향 / 미결

- **BE 에 필요한 것**(조사 리포트 BE-1~BE-8 그대로): 축별 이력 API · 변경 기록 조회 API · 소속/직책 command + preview ·
  행 메뉴 envelope · `MemberResponse` 에 사번·계정 유무·직무 kind · `access/members` 에 회수분(§2).
  이것들이 오면 이번에 잠가 둔 자리(「이력」 disabled, 「변경」 미렌더, 변경 기록 Empty)가 그대로 열린다.
- **planner 보고 필요**: §5 의 1440 폭 충돌 — 핸드오프 최소폭을 낮출지, DS 의 1440 여백 80 을 줄일지는 디자인 판단이다.
- 조직 유형 라벨은 API 의 `unit_type` 그대로 뒀다(「본부」로 나오는 곳 포함) — 카탈로그 소유.
- 데모 계정 `1106`·`1107` 로그인 401 (§4 주). BE/시드 쪽 확인이 필요하다.
- 직무 축은 SC 데이터가 0행이라 전원 `EmptyValue` 다 — 예상대로다.
