# [planner] SPEC-001 0.6.0 · WORK 5판

너는 **agency-settlement `planner` 워커**다. 맥락이 없다고 가정하고 먼저 읽어라:
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/orchestration/roles/agency-settlement/planner/role.md` (+ 같은 폴더)
- 지금 계약 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터/para/projects/summer-star/agency-settlement/20-spec/spec-001-monthly-sales-list.md`(0.5.2) · WORK-001 · DEC-001 D-01 ~ D-23
- 지금 코드(정본) `/Users/kknaks/orca/workspaces/agency-settlement/agency-settlement/back` · `front` — 읽기만
- 작업 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/kos-병원데이터` · allowed_paths: `para/projects/summer-star/agency-settlement/20-spec/` · `30-work/` 만


결정 원천: `_RESUME.md` §2 **2026-11-02 「code r4 F-1」 줄 · 2026-11-03 줄** · 사용자 수정 `feedback-2026-11-02-b.md` **7 ~ 21**(11 ~ 18 화면 · 19 ~ 21 구조).
지금 코드(정본 · 코드 PR kknaksss/agency-settlement#1 커밋 8089f72) — SPEC 0.5.2 와 다른 곳(code r4 수정 · FE6)도 이번 판에 맞춰라(0.5.3 몫 포함).

## 할 것
1. **[이 달 확정] · lock/unlock 없앰** — 수수료율은 언제든 고칠 수 있음(기록은 남김) · 잠금으로 막던 것(전체 다시 받기 · 상품 키 다시 잇기)은 아래 2 의 「달 상품 스냅샷 고정」으로 대신
2. **상품 정보 달별 · 일별 스냅샷** — 매일(21시) 상품 받기 = 그 달 스냅샷에 **늘어난 것만 더함** · KOS 에서 사라진 상품 · 옵션은 지우지 않고 `deletedInKos`(「KOS 삭제됨」) · 다음 달 1일 실행 때 앞 달 스냅샷 **고정**(그 뒤 키 다시 잇기 없음) · 품목 → 상품 id 는 그 품목 달 스냅샷으로
3. **스케줄** — 앱 안 · 환경 변수로 켬(로컬 기본 끔) · 매일 **21:00 KST**: 상품 받기 → 이번 달 결제 증분 · 달 1일엔 앞 달 마감(마지막 증분 · 상품 스냅샷 고정 · 매출 closed) · 실패 · 겹침 · 서버 재시작 때 놓친 실행(다음 실행에서 따라잡기) · 로그 수만
4. **수동 연결** — 상품 id 로 못 이은 품목(option · name 키) 목록 · 사람이 그 달 스냅샷 상품을 골라 연결(키 → 상품 id) · 기록 · 한 번 연결하면 같은 옵션/이름 키는 다음에도 · 수동이 자동보다 이김 · 화면 자리(설정 탭 「연결 안 된 품목 n」)
5. **화면 수정 11 ~ 18**(문구 4 곳 지움 · 일괄 대상 = 필터 이름 · 월별 기본 펼침 · 옵션 칸 왼쪽 · 넓게) — FE 몫 줄로
6. 운영 기준 11월부터(9 · 10월 테스트) — 마이그레이션은 더하기만 · 9 · 10월 데이터는 지우지 않음
7. WORK 5판(WP-BE6 · WP-FE7 병렬 · 계약 고정점) · 판 0.6.0 · public grep · 정할 것은 OQ


## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.** 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_d291ae3b-f96b-492e-8274-6c3e14da473f --from term_3a786cf2-d7ff-4b51-b5b0-7cd93003031b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: SPEC-001 0.6.0" \
  --body "변경 파일 목록 / 요약 / 검증 결과(수치) / 미결·주의점"

orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d291ae3b-f96b-492e-8274-6c3e14da473f --text "[질문] planner: <질문>" --enter`
