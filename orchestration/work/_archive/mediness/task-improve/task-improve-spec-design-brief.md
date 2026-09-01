
# [planner] 시안 v1 스펙 확정 — §4.19.6-R 채움 + v2 이월 정리 + 검수 환류

너는 **mediness `planner` 워커**다. 사용자 페이지 시안이 도착해 확정 판정까지 끝났다 — 이를 스펙 계약으로 박는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec`
**현재 브랜치에 직전 라운드 커밋(522f485ac)이 이미 있고 spec PR #675 이 열려 있다** — 그 위에 작업한다(커밋은 코디 몫).
base: `origin/mediness` → PR `mediness`

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/design-analysis.md` — **시안 분석 + 사용자 판정 + 규율 교정 + 코디 기본값. 이 발주의 정본.**
- 시안 원본: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/reference/2026-09-01-mediness-task-improve/` (README·SPEC_screens·SPEC_state·screens/*.dc.html — HTML 은 소스로 읽어라. 치수·색·문구·인터랙션의 정본)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2 — 결정 표(v2 이월 결정 포함)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-code-report.md` — 환류 2건의 근거(SPEC-155 필드명 W · 6번째 입구)
- 이 워크트리: `20-spec/spec-154-decision-workflow.md` §4.19(현행 상세·보드 계약·§4.19.6-R 슬롯) · `30-work/work-130-task-detail-unification.md` · `work-129-task-request-axis.md`

기대는 개념 — 해당 없음.

## 2. 해야 할 일

### A. §4.19.6-R v1 확정 (spec-154 §4.19 계열)

시안 계약을 개정 노트 + 본문으로 박는다. design-analysis.md 의 네 절(사용자 판정·규율 교정·코디 기본값·gap)을 전부 반영:

1. **상세 2단 레이아웃** — 본문(할일→배경→목표→댓글·로그 탭) + 우측 레일 320px(일정·참고자료·제출자료). 기존 «본문 존 6블록» 서술을 이 배치로 개정 — 5부 결정은 **구성 요소 목록**으로 재서술(순서 계약 아님, 사용자 확정). §4.19.1 셸과의 관계 정리
2. **완료 모달** — 620px 3분할, **활성 조건 = 한 줄 요약 또는 제출자료 1건 이상**(서버 422 계약과 동형 — 시안의 «요약 필수» 는 계약이 아님을 명시). 미체크 경고 = 경고일 뿐 차단 아님. 중단/취소 사유 모달 480px·사유 상주 배너·제출자료 done 강조·일정 미니 타임라인·D-N 표기·체크리스트 인터랙션·디자인 토큰(README 실값 참조)
3. **보드** — 완료 컬럼 월 필터(기준 = completed_at, 코디 기본값·뒤집기 가능 표기), 상태 칩 드롭다운의 시각형은 채택하되 **항목 소스 = 서버 allowed_transitions·사유 필수 전이 2단계**(시안 코드의 5값 고정 나열은 프로토 한정임을 명시), 마커 5값 유지, D-3 이하 강조(프론트 파생 — 서버 축 신설 없음), 0차 숨김·빈 그룹 미렌더 불변 확인
4. **태그 → 배지 5슬롯 매핑** · **goal 렌더 = 개행→불릿**(컬럼 1개 불변)

### B. v2 이월 OQ 등재

- «내 할 일 / 내가 요청한 일» 화면 축 — §4.19.6-R 의 본래 질문을 **v2 OQ** 로 명시 이월(v1 보드 = 단일 모수)
- 역할별·상태별 수정 게이팅 — v1 = «볼 수 있으면 고칠 수 있다» 유지 명시. **직전 라운드가 박은 «참고자료 삭제 = 올린 본인+담당+요청자» 3원칙을 v2 이월로 개정**(취소선 + 이월 표기 — WP-130 해당 작업·검증 항목도 동기)
- @멘션 = v2 OQ (v1 문구 제거)

### C. 검수 환류 2건

- **SPEC-155 §6.1 필드명 정합** — 스펙이 `assignee_member_id` 를 말하는데 구현(WP-129 P3)은 모델이 **이름만** 내고(`assignee_name`) 서버가 해소한다. 구현이 계약 의도(오배정 방어·서버 해소)에 더 충실하므로 **스펙을 구현 쪽으로 정정**하고 개정 노트에 근거를 남겨라
- **WP-129 문서에 6번째 입구 등재** — 버전 WBS 태스크 발(version_wbs.py:1730, 프로덕션 호출자 0 휴면 seam) 이 입구 목록에 없었다. P5 입구 목록에 추가(구현은 이미 차단됨 — 사실 기재)

### D. WP-130 갱신

- **P7 을 v1 시안 계약으로 재정의**(요청 축 화면 제외 — v2) → **BLOCKED 해제**, 시안 참조 경로 기재
- 완료 모달 조건·레이아웃 변경을 관련 phase 에 반영, 참고자료 삭제 3원칙 이월 반영
- gap 2건 실측 판단: ① 일정 카드 planned_start_at·expected_completion projection 유무(코드 실측 — 없으면 additive projection 을 P 작업에 추가) ② 완료 컬럼 월 필터 API 파라미터 필요 여부(R-7 전량 로드 기준으로 판단) ③ 체크리스트 position seam 유무 → 드래그 재정렬 채택/제외 확정

### 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec && python3 scripts/lint-pipeline.py --strict
```
mediness 범위 ERROR 0. **구 서술 스윕 잊지 마라** — «6블록»·«요약 필수»·«삭제 3원칙(v1 문맥)» 등 이번 개정으로 낡는 문장을 grep 으로 찾아 취소선/정정 (추가만 하는 개정이 지난 FAIL 패턴이다). 코드 실측(gap 3건)은 read-only — `/Users/kknaks/orca/workspaces/mediness-app/task-improve` 를 읽되 고치지 마라.

**하지 말 것**: 커밋·push·PR 금지 / 요청 축 화면 구조 확정 금지(v2) / migration 총계 변경 금지 / 코드 레포 수정 금지.

## 3. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 값과 아래가 다르면 preamble 이 맞다.

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner 시안 v1 확정 완료: <한 줄>" \
  --body "변경 파일 / A~D 별 결과 / gap 실측 3건 판단 / 구 서술 스윕 수치 / lint 결과"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] planner 시안 v1 확정 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] planner: <질문>" --enter`
