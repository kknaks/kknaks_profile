# 조사 브리프 — 차티 · 메디킷 · 피부 리포트 (read-only)

너는 이 작업의 맥락이 없다. 이 파일만 보고 끝낼 수 있게 썼다.

## 0. 목적
M3D(미가메디) 3D 피부 스캐너 리포트 화면을 재구성해 **우리 피부과 상담용 웹 목업**을 만든다.
목업은 **메디킷 디자인 시스템**으로, **차티(CHARTY) 웹**의 화면 문법 위에 얹는다.
이번 판은 **조사만** 한다. 화면을 그리거나 코드를 쓰지 않는다. 결정하지 않는다.

## 1. 읽을 것 (전부 read-only)
| 대상 | 경로 | 기준 |
|---|---|---|
| 메디킷 DS | `/Users/kknaks/git/medikit` | `main`(55c14a2) — 체크아웃 그대로 읽는다. 먼저 `CLAUDE.md`·`README.md` |
| 차티 | `/Users/kknaks/git/harness_works/CENTURION-CHARTY` | **`origin/stg`(461a48e, v1.8.0-rc.3)**. 체크아웃은 `release/v1.3.1`(낡음) — **checkout·pull·worktree 생성 금지.** `git -C <레포> ls-tree -r --name-only origin/stg` · `git show origin/stg:<path>` · `git grep <pat> origin/stg` 로만 읽는다 |
| 원본 리포트 | `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/reference/2026-10-21-charty-poc/` | `테스트 보고서.html`(저장본) · `m3d-ai-h5.migamedi.co.kr.har`(API 응답 3개: `report/render.v3` · `measure/results/render` · `basic/analyze/results/render`) |

⚠ HAR 에 실존 인물 개인정보(이름·생년월일·회원번호)가 있다. **리포트에 값을 옮기지 마라** — 필드명·구조·예시는 가명/마스킹으로.

## 2. 질문
### A. 메디킷
1. 패키지 정체 — 이름·버전·빌드(tsup)·배포 방식, 차티가 어떻게 소비하나(npm 의존? 버전?)
2. 토큰 — 색(브랜드·시맨틱·상태)·타이포·간격·radius·shadow. 파일 위치와 실값 요약
3. 컴포넌트 목록 — 이름 · 용도 한 줄 · 파일. 특히 **카드·탭·배지/칩·점수/게이지·차트·이미지 뷰어·모달·테이블·레이아웃(사이드바·헤더)**
4. 목업을 HTML 로 만들 때 쓸 수 있는 형태가 있나(빌드 CSS, tailwind preset, 스토리북 등)

### B. 차티 (origin/stg)
1. 프론트 스택·라우팅 구조·화면 목록(라우트 → 화면 이름 → 한 줄 용도)
2. **상담·고객(환자)·차트 관련 화면**이 있나 — 있으면 레이아웃·구성 요소·데이터 필드
3. 메디킷을 실제로 어떻게 쓰나(import 예 2~3개 파일:줄) / 메디킷 밖 자체 컴포넌트가 많은가
4. 화면 공통 골격(셸·내비·헤더) — 새 「피부 상담」 화면이 들어간다면 어디에 붙는 모양인가(결정 말고 후보만)
5. 백엔드에 피부 분석·외부 스캐너 연동 흔적이 있나(grep: skin, m3d, migamedi, scan, 피부)

### C. 원본 리포트
1. 화면 섹션 순서와 각 섹션이 보여 주는 것(HTML 저장본 기준)
2. API 3개 응답 구조 — 카테고리·항목(feature)·점수/level/degree·이미지(atlas/images)·3D 의 관계를 표로
3. 상담에 쓸 만한 데이터 vs 장식에 가까운 데이터 — 의견 말고 **필드 근거**로

## 3. 산출물
**파일 1개만 생성**: `/Users/kknaks/orca/workspaces/kknaks_profile/차티-화면-구상/orchestration/work/charty-consult-mockup/research-report.md`
- 질문 번호마다 답 + 근거(`파일:줄` 또는 `origin/stg:path:줄`)
- 확인 못 한 것은 「확인 안 됨」
- 판단이 필요한 것은 끝에 **「정할 것」** 목록으로 모은다. 네가 정하지 않는다
- 그 밖의 파일·레포는 건드리지 않는다(git 상태 변경 금지, fetch 도 하지 마라 — 코디가 이미 했다)

## 9. 완료
리포트를 다 쓰면 아래 두 개를 순서대로 실행한다(task_id·dispatch_id 는 preamble 에서).
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_342408b8-2fe7-428d-be5b-332e77582853 --text "[researcher 완료] orchestration/work/charty-consult-mockup/research-report.md" --enter
```
질문이 있으면 같은 terminal send 로 `[질문] ...` 을 보내라.
