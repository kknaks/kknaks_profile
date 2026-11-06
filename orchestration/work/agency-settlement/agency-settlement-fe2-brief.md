# [frontend] WP-FE2 — 시안 v2 적용 · 헤더 메뉴 · 에이전시 탭 · 엑셀 버튼 (SPEC-001 0.3.1)

너는 **agency-settlement `frontend` 워커**다. 맥락이 없으면 먼저 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md` (+ 같은 폴더) 를 읽어라. (시안 v2 를 만든 그 워커라면 그 맥락을 써라.)

⚠ **backend 워커가 같은 워크트리 `back/` 에서 병렬 작업 중 — `back/` · 레포 루트 README 를 건드리지 마라.** 계약은 SPEC §4.2 · §4.7 그대로 — back 이 아직 없으니 가짜 응답으로 먼저.

- 계약 SoT: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.3.1** · 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` **2판**(네 WP 행 = 완료 조건 · 검증)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` D-01 ~ **D-17** · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2
- 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r4-report.md`(마지막 · WARN) · `review-doc-r3-report.md`
- 시안 v2(채택): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v2-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — 1판 코드가 커밋 안 된 채 있다(이어서 고친다). ⚠ **코디가 띄운 로컬 서버 8800(back) · 3800(front)이 떠 있다 — 그 포트 · 프로세스를 건드리지 마라.** 띄워 볼 때는 다른 포트 · 끝나면 내린다. `back/.env` 에 운영 키가 있다 — **읽지도 쓰지도 · 운영 KOS 를 부르지도 마라**(가짜 transport · 가짜 응답만).

## 할 것
WORK-001 2판 **WP-FE2** 행 전부: **시안 v2 를 그대로 코드로**(헤더 「월별 조회 | 에이전트별 조회」 · 폭 제한 없음 · 수납 머리 + 들여 쓴 품목 줄 · 0원 구성품 흐리게 · 배지 · 상태 화면 · 「받은 시점 기준」 · 마지막으로 받은 시각 · 이번 달 [새 결제 받기] / 지난 달 「✓ 확정 · 저장됨」 + 작은 [전체 다시 받기](확인 1번) · 「새로 받음」 배지 · 0건 문구) · 에이전트별 = 탭 「에이전시 전체」 + 그 달 에이전시 탭(「(에이전시)」 뗀 이름) · 손님 수 · 결제 손님 수 · 「수수료 — 다음 판」 · 툴바 오른쪽 [엑셀 내보내기](지금 화면 범위 · §4.7). 디자인 토큰 · 컴포넌트는 지금처럼 cc-prototype `procedure/front` 복사본.
가짜 응답(가짜 이름 · 에이전시A/B/C · 가짜 금액)으로 시안 장면마다 스크린샷을 찍어 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/shots-fe2/` 에 두고 보고한다(시안 장면 이름과 같게).

## 하지 말 것
- `back/` · 실제 고객 · 에이전시 이름 · `localStorage` · cc-prototype import · 커밋 · push

## 검증
```
cd front && npx tsc --noEmit && npm run lint && npm run build
```
보고에 WP-FE2 완료 조건 한 줄씩 + 시안과 다른 곳 목록.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_b19a3776-0bcd-4f25-992e-ba7af21fc8b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WP-FE2" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] frontend: <질문>" --enter`
