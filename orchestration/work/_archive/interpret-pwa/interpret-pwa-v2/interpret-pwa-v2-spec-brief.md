# [planner] SPEC-001 0.6.0 · WORK-001 — 사전 확장(D-39 · D-40) · 통역 기록(D-41)

너는 interpret-pwa planner 다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/planner/role.md` (+ rules · skills · tools · workflow). allowed_paths: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/README.md`. DEC · log.md 는 코디 몫. 커밋 금지.

## 입력
- DEC-001 **D-39 · D-40 · D-41**: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md`
- 지금 SPEC 0.5.0 · WORK-001
- 조사 3개 + 처분: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-r1-zh-report.md` · `research-r2-ja-en-tw-report.md` · `research-r3-th-vi-yue-report.md` · **`research-dispositions.md`(코디 처분 — 이게 기준)**
- 코드(배포본 main 2a9d5a5 · read-only): `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:<경로>` (canonical 은 낡음 — checkout · pull 금지)

## 고칠 것
1. §4 사전: 새 term 13개(N01 ~ N12 · N14 — id 규칙 정하기 · 예 `kr-001`(Procedure Hub 밖)) · source 값(web-research YYYY-MM-DD) · 처분의 기존 표기 변경 · 대륙 공식명 규칙 · 「현지에 없음 = 영문」 규칙을 언어 공통 규칙으로 · 홍콩(yue)은 대만과 독립 · version .6 · 한도(20,251)를 넘는 언어가 생기면 줄이기 순서대로(실측 재확인 항목 §9.3)
2. **§ 신설 통역 기록(D-41)**: 저장 위치(back PVC · 경로 env) · 형식(날짜별 JSONL · 한 줄 = 한 확정 발화: session id · 시각 · lang · side · 원문 · 번역 · 걸린 term id 목록 · 세션 시작/끝 줄) · 걸린 term 판정 방법(발화 · 번역에 그 term 의 name/alias 가 나타났는지 — 정의를 문장으로) · 음성 · 토큰 · IP · 계정값 없음 · 7일 지난 파일 삭제(기동 때 + 하루 한 번) · 쓰기 실패는 통역을 끊지 않음(경고 로그) · **화면 · API 없음**(§3.5 허용 경로 6개 그대로) · 꺼내기 = kubectl cp(배포 문서) · 시험 항목
3. 배포: back PVC(차트 · 크기 · local-path 노드 제약 선례 cc-prototype) · env
4. WORK-001: WP16(back: 시드 · 기록) · WP17(infra: PVC · env) · WP18(배포 · 실물: 새 시술 3개 언어 1회 · 기록 파일 생김 · 7일 삭제 시험) 행
5. SPEC 0.6.0 · 변경 이력 · 비밀값 0

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC 0.6.0" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] planner SPEC 0.6.0 완료 — <한 줄>" --enter`
