# [researcher] HAR 분석 — 방 이동 · 차트 작성 (다음 기능 논의 준비)

너는 day **researcher** 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/researcher/role.md`(+ 같은 폴더). **read-only** — 레포 수정 · 커밋 · KOS 호출 · DB 접속 금지. 산출물 = 리포트 1개.

## 원천
- HAR(KOS 데모 지점 · 사용자 2026-11-10): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/reference/2026-11-09-cc-day/har/방이동.har` · `차트작성.har` · `차트작성2.har` (+ 같은 폴더 앞선 HAR 들 참고 가능)
- 기획안(명동점 · read-only): `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` §2-1 관리실 이동 · §4-2 의사 차트 · 간호관리차트 · §6-1 관리실 기록 · `cc-개요.md`(KOS 읽기 · 쓰기 표 · 원칙 K-*)
- 사용자 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/_RESUME.md` §2 「차트(④) 사용자 확인 · 결정」 행(작성자 1명 · 간호관리차트 담당자 필수 · 의사차트 집도의 필수 · 탭 · 표 디자인 · 로그인 직무별 먼저 보이는 탭)
- DAY 코드(read-only): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(PR #238 브랜치) — 지금 차트(읽기 전용 · `assigneeMemo` · `doctorMemo`) · 방(`visit.room_id` · `change-tasks-room` · 방 배정 작업) · `backend/day/emr/kos/` · 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/spec-002-procedure-board.md`

## 할 것
1. **HAR 마다 쓰기 요청(commands)을 순서대로**: 경로 · 요청 칸 이름 · 값 모양(타입 · enum) · 응답 상태 · 앞뒤 조회(queries)로 확인되는 결과 칸. **값(고객 이름 · 전화 · 메모 글 · 직원 실명 · 토큰)은 옮기지 마라** — 칸 이름 · 타입 · 건수만
2. **방 이동**: 무엇을 바꾸나(방 배정 작업 · 시술 작업 · 방문) · 시술 대기/진행 중 차이(HAR 에 있는 만큼) · 침대 · 정원 개념이 요청 · 응답에 있나 · KOS 가 방 이동 기록(들어온 · 나간 시각)을 주는 조회가 HAR 에 있나 · 기획 2-1(점유 이동 · 다른 관리실로 이동 · 복귀) · 6-1(관리실 기록)과 대조해 **KOS 로 되는 것 / DAY 자체로 가져야 하는 것 / 안 되는 것** 표
3. **차트 작성**: 간호(담당자 메모) · 의사(원장 메모) 쓰는 요청 · 칸 · 작성자(1명) · 담당자/집도의가 요청에 어떻게 실리나 · 필수 조건이 요청에서 드러나나 · 고쳐 쓰기(이력 · 덮어쓰기) · 지난 방문 차트 읽는 조회 · 기획 4-2(의사 차트 · 간호관리차트 · 전체 시술에 내용 적용 · 작성자 추가 · 저장 · 이력 보존 10년/5년)와 대조 표
4. DAY 지금 코드 · 스펙과의 차이(무엇을 새로 만들어야 하나 · 이미 있는 것)
5. **결정하지 마라** — 「정할 것」 목록으로(사용자 결정과 HAR 이 부딪히면 그것도)

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-har-room-chart-report.md` — 질문마다 답 + 근거(HAR 파일 · 항목 순번 · 파일:줄). 확인 못 한 것은 「확인 안 됨」.

## 완료 보고 (두 명령 모두)
```bash
orca orchestration send --to term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 방 이동 · 차트 HAR" --body "<요약 · 정할 것 수>"
orca terminal send --terminal term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd --text "[worker_done] researcher 완료 — <한 줄>" --enter
```
