# [frontend · 시안] 매출 시안 v2 — 에이전트별 조회 탭 (claude design · 코드 금지)

너는 **agency-settlement `frontend` 워커**(시안 담당). **맥락이 없다고 가정하고** 읽어라:
- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/frontend/role.md`
- 앞 판 브리프 · 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/agency-settlement-design-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-report.md`(업로드 절 포함) · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload-instructions.md`
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` **D-10 · D-11 · D-12 · D-13**

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — `front/` · `back/` 건드리지 마라. 산출물 = 로컬 사본 + claude design 새 파일 1개 + 리포트.

## 사용자 결정 (2026-10-29)
- v1 시안 **채택**(「이 디자인으로 가자」). v1 은 고치지 않는다
- **에이전트별 조회 = 탭 「에이전시 전체」 + 에이전시마다 탭 하나**. 「에이전시 전체」 탭은 에이전시 손님 수납 전부를 같은 묶음 모양으로(유입 채널 칸으로 어느 에이전시인지 보임) + 에이전시별 손님 수 · 결제 손님 수 요약. 에이전시 탭은 그 에이전시만. 수수료는 자리만(「수수료 — 다음 판」)
- 데이터가 SQLite 에 저장된다(D-12): 「다시 불러오기」 → **이번 달은 「새 결제 받기」(마지막 이후만), 지난 달은 「확정 · 저장됨」 표시 + [전체 다시 받기]**(작게). 안내 문구 「상태는 지금 기준」 → **「받은 시점 기준」**(D-13) · 「마지막으로 받은 시각」 표시

## 만들 것
- **`Ceramique 월별 매출 v2.dc.html`** — v1 을 바탕으로. 로컬 사본 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/` · claude design `dda9a931-097f-4780-9301-972d5ac1fc23` 에 **새 파일 1개 추가**(사용자 업로드 허락 — 이 프로젝트 시안 파일 추가에 한함 · 기존 75개 수정 · 삭제 금지 · 같은 이름 있으면 멈추고 묻기)
- 장면: v1 장면 + `agency-all` · `agency-one` · `monthly-closed`(지난 달 · 확정) · `monthly-current`(이번 달 · 새 결제 받기)
- 이름 · 에이전시 이름은 전부 가짜(에이전시A/B/C)

## 검증 · 리포트
- list_files 75 → 76 · 다시 받아 바이트 대조 · node 로 장면 값 · 가짜 이름 grep
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v2-report.md`

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_b19a3776-0bcd-4f25-992e-ba7af21fc8b5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 시안 v2 업로드" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] frontend: <질문>" --enter`
