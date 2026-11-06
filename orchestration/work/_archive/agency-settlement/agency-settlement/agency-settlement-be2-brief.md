# [backend] WP-BE2 — SQLite 저장 · 증분 · 에이전시 · 엑셀 (SPEC-001 0.3.1)

너는 **agency-settlement `backend` 워커**다. 맥락이 없으면 먼저 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/backend/role.md` (+ 같은 폴더) 를 읽어라.

⚠ **frontend 워커가 같은 워크트리 `front/` 에서 병렬 작업 중 — `front/` 를 건드리지 마라.**

- 계약 SoT: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md` **0.3.1** · 작업 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/30-work/work-001-monthly-sales-list.md` **2판**(네 WP 행 = 완료 조건 · 검증)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/10-decision/decision-001-monthly-sales-list.md` D-01 ~ **D-17** · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/_RESUME.md` §2
- 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/review-doc-r4-report.md`(마지막 · WARN) · `review-doc-r3-report.md`
- 시안 v2(채택): `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-upload/Ceramique 월별 매출 v2.dc.html` · `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/work/agency-settlement/design-v2-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement` — 1판 코드가 커밋 안 된 채 있다(이어서 고친다). ⚠ **코디가 띄운 로컬 서버 8800(back) · 3800(front)이 떠 있다 — 그 포트 · 프로세스를 건드리지 마라.** 띄워 볼 때는 다른 포트 · 끝나면 내린다. `back/.env` 에 운영 키가 있다 — **읽지도 쓰지도 · 운영 KOS 를 부르지도 마라**(가짜 transport · 가짜 응답만).

## 할 것
WORK-001 2판 **WP-BE2** 행 전부: §4.4 SQLite(표 · 줄인 필드만 · 원본 JSON 0 · 파일 권한 + WAL/SHM · gitignore) · §4.5 판단표(확정 달 KOS 0 · 저장 없음 = 전체 · 이번 달 증분 — ① 달 전체 1회 · 묶음 키 수 비교 · 비싼 조회는 새 것만) · §4.6 · 동시 요청 잠금 · 응답은 늘 저장본 · 메모리 캐시 없앰 · 에이전시 필드(§4.2 · §6.8 — 손님 = `visitorId` D-15 · 결제 손님 D-16) · `GET /api/sales.xlsx`(§4.7 · openpyxl · 수식 셀 막기 · 이름 그대로 D-17) · SPEC §9 시험 전부(#25 ~ 이후 포함).
r4 남은 것: **W-2**(① 행이 그 자리에서 금액 · 수단이 바뀌면 missing+new 로 두 번 — 수납 단위 「바뀜」으로 다루고 시험 하나) · W-3 은 문서 몫이라 무시.

## 하지 말 것
- 운영 · 데모 KOS 호출 · `/commands/` · 로그에 이름 · 금액 · id · 키 · cc-prototype import · 커밋 · push

## 검증
```
cd back && uv run ruff check . && uv run pytest -q
grep -rn "commands/" back/app   # 토큰 교환 1줄
git status --ignored            # back/.env · back/data/*.sqlite3* 미추적
```
보고에 WP-BE2 완료 조건을 한 줄씩 「충족 / 미충족(사유)」.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_6e1f25e3-1764-4c52-94ea-b26f010363f2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP-BE2" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] backend: <질문>" --enter`
