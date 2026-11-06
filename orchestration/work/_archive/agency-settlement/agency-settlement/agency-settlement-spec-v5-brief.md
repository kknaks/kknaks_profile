# [planner] SPEC-001 0.5.0 (백엔드 몫) · WORK 4판 — 유입 채널 · 수수료율 · KOS 상품 · PostgreSQL

너는 **agency-settlement `planner` 워커**다. **맥락이 없다고 가정하고** 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/planner/role.md` (+ 같은 폴더)
- 결정 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2 — **2026-11-02 줄 4개**(이기는 순서 1번) · 피드백 SoT `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/feedback-2026-11-02.md`
- 지금 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` 0.4.3 · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` · 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md`
- 지금 코드(정본 · 코드 PR kknaksss/agency-settlement#1): `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/back/` — 읽기만
- KOS 공식 스펙 `https://developers.kos-solution.com/openapi.yaml` — 상품 작업(`getProducts` · `getProduct` · `getCategories` · `getProductOptions` · `searchProductOptionSummaries`)과 ② 품목 통계의 상품 키(어느 필드로 품목 → 상품을 잇나)
- 시안 v3 는 다른 워커가 병렬로 만든다 — **화면은 이번 판에 쓰지 마라**(「시안 v3 대로 — 다음 판」 자리만). 계약(API · 저장 · 계산)에 집중

작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` · allowed_paths: `para/projects/summer-star/agency-settlement/20-spec/` · `30-work/` 만.

## 할 것 — SPEC-001 0.5.0
1. **유입 채널 일반화** — 「에이전시」 판정 → **모든 최초 유입 채널**(값 그대로 · 「(에이전시)」 꼬리 뗀 이름 · 빈 값 = 「(없음)」). 응답 필드 이름(agency → channel) 바꾸는 계약 · 채널별 결산(손님 · 결제 손님 · 실결제 · 수수료 · 미설정 품목 수 · 합계)
2. **⚠ 결제≠품목 비교에서 앞 달 결제의 이 달 취소를 뺀다**(9월 Ⓐ 꼴 — `review-code-r3-report.md` §2 · OQ-106)
3. **KOS 상품 목록 받기** — 조회 전용(허용 경로에 더함 · `/queries/` 만) · 상품 · 옵션 · 카테고리 저장 · 품목 → 상품 잇는 키 확인(못 이으면 OQ) · 다시 받기 API
4. **수수료율** — 상품 단위(옵션은 상품 따름) · **달별 스냅샷 표**(month · product · rate) · 새 달 = 앞 달 복사 · 확정 달 잠금(고칠 땐 확인 · 기록) · 미설정 = 수수료 0 · 품목 수수료 = 품목 실결제 × 그 품목이 보이는 달의 비율 · 「앞 달 결제 취소」 음수의 수수료 규칙(OQ · 기본값) · 설정 읽기 · 쓰기 API(로컬 · 로그인 없음 — 쓰기 API 가 생기는 것에 주의)
5. **PostgreSQL** — SQLite → PG(접속 = env `DATABASE_URL` · 로컬 시험은 docker PG 또는 testcontainers) · 마이그레이션 도구(alembic 등) · **SQLite 저장본을 PG 로 옮기는 한 번짜리 명령**(확정 달을 KOS 로 다시 받지 않게) · 잠금(달 잠금 · 쓰기)을 PG 로 · 파일 권한 대신 DB 계정 · 개인정보 칸 그대로(이름 · 방문일)
6. PDF 거래 명세서 — 생성 경로 · zip · 라이브러리만 계약(모양은 시안 v3 → 다음 판)
7. WORK 4판: WP-BE4(1 ~ 6) · WP-MIG(PG 옮기기 · 실물 대조 — 9 · 10월 수 · 금액 같음) · WP-FE4 는 시안 뒤
8. 판 0.5.0 · public grep · 정해야 할 것은 OQ(사용자/코디 표시)

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_01b390d8-5b8c-49e8-b581-8c37628253fd \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: SPEC-001 0.5.0 (백엔드)" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] planner: <질문>" --enter`
