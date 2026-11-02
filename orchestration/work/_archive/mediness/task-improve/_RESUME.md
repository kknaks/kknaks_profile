
# 재개 노트 — task-improve (mediness)

**지금**: **전 배포 완료 (2026-09-01).** dev(5df3ecea)·prod(494d6fec) 파드 3종 롤아웃·alembic 0138(backfill 60 포함)·health 200. spec #675→#667(main bacb9374f)·code #140→#138(main 494d6fec) 전부 머지. k8s_infra#2(task-references hostPath) 머지·볼륨 반영 실측 완료(dev·prod). main→mediness 역머지 충돌 해소(SPEC-240 doc_no 251 재발번). 스펙 3커밋(522f485ac·ae53ad84f·73414aea2, PR #675) + 코드 3커밋(5b98247a WP-129·db4bcfab WP-130·3573ecf4 모달 정정, PR #140). 검수 전 라운드 PASS. 로컬 스택 가동 중(back·mcp·worker 워크트리 + front dev :23001, DB 0138).
**다음(문서 마감만 잔여)**: WP-129/130 status done 갱신 + WP-131 환류(실기동 수리 등재) → SUMMARY 작성 → archive-work = 완료선. 공지거리: slack 미매핑 5명 요청 DM 미수신·기존 decision/incident 태스크 배경 빈 값. v2 이월: 내가 요청한 일 화면·권한/상태별 게이팅·@멘션·기존 초안 첨부·task.draft 참조자/완료예정 축.

세팅: `scripts/new-work.sh mediness task-improve` · 설정 SSOT `config/projects/mediness.json`
코디handle: `term_d5bec05e-881f-4a29-a144-fd73be7e23c4`

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec` (branch `kknaksss/task-improve-spec`, base `origin/mediness` → PR `mediness`)
- `app`: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (branch `kknaksss/task-improve`, base `origin/dev` → PR `dev`)

## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [!] **사용자: spec PR #675 → code PR #140 리뷰·머지** (병합 전 필수 2건은 PR #140 코멘트에 기재)
- [ ] 배포 전: k8s_infra_mac 차트 hostPath(`/mnt/mac/task-references`·`-dev`) PR + Pre-deploy DB 실측 3건(빈 created_by 행·slack_id 미매핑 비율·살아있는 instruction run)
- [ ] 머지·배포 후: WP-129/130 status done 갱신(P0·P8 실측 닫기) → SUMMARY 작성 → archive-work = 완료선
- [!] v2 이월 잔여(OQ-22 내가 요청한 일 화면 · OQ-23 권한/상태별 게이팅 · OQ-24 @멘션)는 다음 신규 작업 입력
- [!] 로컬 스택: canonical compose(postgres·redis·back·mcp·worker) + 워크트리 override(스크래치패드 docker-compose.task-improve-worktree.yml) + front dev :23001(nohup). 정리 시 front pid kill + compose down

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-01 | **작업 범위 = 업무 요청 도입 + 태스크 페이지 개선.** 설계 결정은 task-redesign §2 확정분을 그대로 입력으로 사용(게이트 없음·파생 구분·`assignee_member_id` 축·슬랙 DM graceful·진입점 2곳·레거시 주석처리·워크플로 웹 재배정 요청 축 이월·알림 고도화 제외) — 정본: `work/_archive/mediness/task-redesign/_RESUME.md` §2 | 사용자 지시 (2026-09-01) + 직전 작업 확정 이월 |
| 2026-09-01 | **~~요청자 자동 cc~~ 폐기 → `created_by` 파생만.** 요청자 식별·접근·「내가 요청한 일」 뷰 전부 `created_by_member_id` 로 파생(접근 자격은 이미 created_by 를 봄 — manual_surface.py:456). task_ccs 에 요청자를 자동 추가하지 않는다. 요청 판정 = 비워크플로 task_type ∧ created_by ≠ assignee (둘 다 NOT NULL). 본인 태스크 = created_by == assignee | 사용자 확정 (2026-09-01, 08-31 「요청자 자동 cc」 재정정) |
| 2026-09-01 | **샤라웃 지시 배제 = 입구만 주석 차단.** 슬랙(`/샤라웃`·봇멘션·폼)·AX 채팅 intake 양쪽에서 지시(실행 요청) 유형의 **진입점만** 주석으로 막는다. 내부 워크플로 로직·원장은 손대지 않는다 — **나중에 재활성 가능해야 함** | 사용자 확정 (2026-09-01 "나중에 다시 쓸 수도 있어서 주석만, 입구만 막으면 되잖아") |
| 2026-09-01 | **태스크 본문 통일 = 4부 구조(배경·목표·Todo·진행로그) + 출처 링크.** `background`·`goal` **컬럼 신설**(nullable text 2개 — 마크다운 한 자리 관례 폐지), Todo=`task_check_items`·로그=`task_events`+댓글 기존 축. **decision/incident 원장 라이브 렌더 폐지** — 생성 시 워크플로가 배경/목표 스냅샷 저장, 원문은 execution 사슬 출처 링크로. `description` 은 legacy fallback. migration = 컬럼 2 + 인덱스 1 | 사용자 확정 (2026-09-01 "원장을 렌더할 필요가 있을까, 컬럼 추가") |
| 2026-09-01 | **채팅 생성 = DB 필드 채움이 목표.** 현행 AX 채팅이 배경/목표를 안 채우고 넘어가는 문제 — 채팅 발 초안은 **배경(background)·목표(goal)·체크리스트(task_check_items) 세 가지를 반드시 채워 산출**한다(대화 맥락에서 AI 생성, 부족하면 되물음·초안 카드에서 사람이 검수). 채팅은 입력구이고 산출물은 채워진 DB | 사용자 확정 (2026-09-01, 체크리스트 포함 정정) |
| 2026-09-01 | **참고자료·완료 산출물 = `task_references` 테이블 1개 신설.** 축 2개: `role`(reference 참고자료 / deliverable 완료 산출물) × `kind`(link / file). 컬럼: task_id FK·url·file_path·filename·title·created_by_member_id·`deleted_at`(**soft delete** — tasks 관례 동일). 파일 저장은 부서공간 storage path-guard 패턴 재사용. ~~산출물 업로드는 완료의 조건 아님(옵션)~~ → **같은 날 정정: 완료 시 산출자료 또는 완료기록 중 최소 1 필수** (완료 모달 결정 행 참조). **출처(샤라웃/incident)는 행으로 저장하지 않음** — execution 사슬이 구조적 정본, 화면 참고자료 섹션 첫 줄에 자동 렌더만. 다른 결정·회의록 추가 참조는 link 행으로 | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **상세 최종 구조 = 배경 / 목표 / Todo / 참고자료(출처 자동 + 링크·파일) / 완료 산출물 / 진행로그(댓글).** migration 총계: 컬럼 2(background·goal) + created_by 인덱스 1 + 테이블 1(task_references) | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **완료 전이 = 완료 등록 모달 경유, 빈손 완료 불가.** 완료(→done) 시 모달에서 ① 산출자료만 ② 산출자료+완료기록 ③ 완료기록만 — 세 조합 중 하나 필수(근거 없는 완료 방지 — "업무를 완료했는지 판단할 근거"). 저장: 완료기록 → `task_completed` TaskEvent payload / 산출자료 → task_references role=deliverable. 서버도 강제(둘 다 없으면 422 — 화면만 막으면 MCP·채팅 경로가 우회). **사람 액터의 완료 전이에만 적용** — 시스템 자동 완료(워크플로 멱등 완료·incident 슬랙 [완료] 등 actor_kind=system)는 예외. 수락·검수 게이트 아님 — 타인 승인 없이 본인이 근거를 남기는 것 | 사용자 확정 (2026-09-01, 서버 강제·시스템 예외 재확인) |
| 2026-09-01 | **AX 채팅에 첨부파일 업로드 기능 신설.** 채팅에서 참고자료·산출물을 올릴 수 있어야 함 — 업로드는 초안(draft) 단계에 붙였다가 승인 시 `task_references` 로 귀속. **링크는 하이퍼링크로 렌더**(title 있으면 title 표시, 내부 URL 은 딥링크) | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **첨부 표시 = 기본 다운로드 카드 + 이미지만 인라인 미리보기.** 이미지(png/jpg/gif/webp)는 인라인, PDF·오피스·기타는 다운로드 카드(파일명·크기). 비이미지 인라인 렌더 금지(XSS)·`Content-Disposition: attachment` 서빙. PDF 뷰어 등 미리보기 확장은 후속 additive | 사용자 확정 (2026-09-01 "일단 그렇게 가자") |
| 2026-09-01 | **첨부 저장 경로 확정 — 기존 관례(부서공간·오디오) 그대로.** env `TASK_REFERENCE_STORAGE_ROOT` 기본 `/app/var/task-references`, k8s hostPath `/mnt/mac/task-references`(prod)·`-dev`(dev), 레이아웃 `{task_id}/{reference_id}_{원본파일명}`, 채팅 초안은 `drafts/{draft_id}/` 스테이징→승인 시 이동, DB 엔 상대경로만. **⚠ 배포 사전조건: k8s_infra_mac 차트(values-dev/prod) hostPath 볼륨 추가 PR 별도** (medi-me 실측 2026-09-01) | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **세부 3건 = 코디 추천 채택.** ① 파일 제한: 파일당 25MB·실행파일류 차단 목록·개수 제한 없음 ② 참고자료/산출물 권한: 접근 가능자(담당자·요청자·cc) 추가 가능, 삭제 = 올린 본인+담당자+요청자 ③ 요청자 권한: 자기가 요청한 태스크 수정(배경·목표·기한)·취소 가능, 상태 전이는 담당자만. 댓글은 기존 `comment_task` seam 재사용(신설 0) | 사용자 확정 (2026-09-01 "추천으로") |
| 2026-09-01 | **WP = 역할별 2건 분할.** WP-129(업무 요청 축 + 샤라웃 지시 입구 차단 — 시안 무관, migration 인덱스 1) / WP-130(상세 5부 통일 + 완료 근거 — background/goal·task_references·완료 모달·채팅 채움/첨부, 시안 P8 귀속, migration 컬럼 2+테이블 1 + k8s 사전조건). 분할 기준 = «background/goal·task_references 필요 여부» | 사용자 확정 (2026-09-01 "역할별로 2개 분할 발주") |
| 2026-09-01 | **페이지 시안 v1 범위 확정 — «내가 요청한 일» 화면은 v2 로 이월.** 이번엔 시안의 보드(내 할 일 단일 모수) + 상세 페이지만 만든다. WP-130 P7 의 요청 축 화면 분리는 v2 — §4.19.6-R 슬롯은 v1 계약(이 시안)으로 채우고 요청 축 배치는 OQ 로 이월 | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **시안 충돌 4건 사용자 판정.** ① 상세 섹션 배치 = 시안대로(Todo 선두·참고자료/산출물 우측 레일) — 5부 결정은 **구성 요소 목록이지 순서 계약이 아님**("디자인만 저렇게 그리는 것") ② 완료 조건 = **논의대로 산출자료/완료기록 중 최소 1** — 시안의 「요약 무조건 필수」 기각, 모달 활성 조건 = 둘 중 하나 ③ 출처 마커 = **스펙 5값 유지** — 시안 2값 기각 ④ 마감 임박 강조 = 도입, **D-3 이하(3일 아래) 강조** — 프론트 단독 파생(서버 판정 축 신설 없음) | 사용자 확정 (2026-09-01 "시안만 참고하고 우리 규칙을 정한다") |
| 2026-09-01 | **수정 권한·상태별 수정 규칙 = v2 이월.** v1 은 현행 계약 유지 — «볼 수 있으면 고칠 수 있다»(가시성=자격, 2026-08-12 정책 동형). 역할별 연필 게이팅·~~참고자료 삭제 3원칙~~(v2 이월)·**상태별 수정 매트릭스**(terminal 잠금 등) 전부 v2. v1 에 남는 강제: 전이 자격(기존 서버 판정)·요청자 취소 축(구현 완료)·완료 근거 422·terminal 재배정 금지(기존 가드) | 사용자 확정 (2026-09-01 "지금 하면 너무 복잡하니까 상태별 수정은 나중에") |
| 2026-09-01 | ~~첨부 추가 UI 인라인 통일~~ → **정정(사용자 반려): 레일 발 = 중앙 모달(시안 «참고자료 추가» 다이얼로그가 정본 — 제목·부제·X·[링크\|파일]·URL·표시 이름·취소/추가), 완료 모달 안 = 인라인 행**(모달 속 모달 금지). 같은 컴포넌트 presentation 축으로 공유. 코디가 «인라인으로 하자»로 오독했던 것 — 시안에 모달 디자인이 있었다 | 사용자 확정 (2026-09-01 실기동 반려, 코디 직접 정정) |
| 2026-09-01 | **승인 카드 공용 본문 확정(와이어프레임) — WBS 등록 발 포함.** 태스크를 만드는 모든 승인 카드(task.draft·wbs_task.create/update)는 «버전/PHASE/담당자/기한/요청자 + 배경 + 목표 + 체크리스트 + 첨부 + 요약문 + [승인][거절]» 을 싣는다. **+확장(같은 날): 정본 컬럼 세트 = 웹 Task 생성 모달과 동일** — 참조자(cc)·owner/실행 조직·시작 예정일·제품·버전까지, 승인 착지 시 태스크에 전부 기록. ~~빈 축 미적재(코디 판정)~~ → **재정정(사용자): 빈 축도 «미지정/미기재» 행으로 상시 표시** — 전 컬럼이 항상 카드에 선다. AI 가 발화·문맥에서 채우고 못 채운 자리는 «미기재» 로 노출(조용한 생략 금지). 승인 시 본문이 실제 태스크(background/goal·check_items·due)로 착지 | 사용자 확정 (2026-09-01 실기동 — 와이어프레임 승인 요구) |
| 2026-09-01 | **생성 모달에도 첨부(참고자료) 입력 포함 — 태스크 컬럼·연관 원장 전부가 생성 시점에 들어가야 «끝»이다.** Task 생성 모달에 참고자료(링크·파일) 섹션 추가: 생성 성공 후 task_references 로 순차 업로드(업로드 실패해도 태스크는 생성 + 실패 안내), 정책 동일(25MB·denylist·이미지 인라인) | 사용자 확정 (2026-09-01 "태스크 컬럼이랑 연관된 거 다 넣을 수 있어야") |
| 2026-09-01 | **댓글 = 현행 유지 (task_events event_type=comment, 수정·삭제 없음).** 로그↔댓글 구분은 event_type 으로 이미 성립. 댓글 수정·삭제가 필요해지면 task_comments 분리로 전환(additive) — 코디 해석("아 오키"), 뒤집기 가능 | 사용자 승인 (2026-09-01) |
| 2026-09-01 | **채팅 요청 발화 패턴 확정 = «태우님께 000 업무 요청 해줘».** AX 채팅에서 업무 요청은 담당자를 발화에 명시하는 형태로 간다 — planner 기본값(담당자 해소 = 발화 명시 시에만, 모호하면 요청자 본인) **사용자 확정으로 승격** | 사용자 확정 (2026-09-01) |
| 2026-09-01 | **샤라웃(의사결정 intake)의 «지시(실행 요청)» 유형 전면 배제 — 슬랙·채팅 양쪽, 주석 비활성만.** ~~ⓑ 해석(태스크 지시 자리만)~~ → 사용자 확정으로 확대: 샤라웃의 흐름 유형에서 **지시(실행 요청)를 슬랙 표면(`/샤라웃`·봇멘션·폼)과 채팅 intake(SPEC-156) 모두에서 배제**한다. 코드 삭제 아님 — 주석처리 수준 비활성. **결정 요청·공유 유형과 승인/결재 축은 유지.** 앞으로 태스크 요청(지시)은 AX 채팅 포함 전부 **태스크 생성(새 업무 요청 축)** 으로 간다. + Q3의 개인 대시보드 3자리 비활성 포함. ~~배정 부트스트랩 전면 비활성~~ → **정정(검수 V-1): 지시 흐름 발 부트스트랩만 비활성** — 생성 시점 3곳 중 결정 승인·[후속 실행] 발은 유지 축(승인/결재)에 속해 살아 있어야 함(WP-130 P3 도 그 전제). 코디 판단, 사용자 결정("지시만 배제·결재 유지")과 정합 — **Q3 닫힘** | 사용자 확정 (2026-09-01 "샤라웃에서 지시는 다 배제. 슬랙/채팅 둘 다") + 검수 V-1 정정 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner (본 라운드) | `term_c601189f-68a7-47ad-99cc-28467c3d1f79` | `task_b6eedbabdb93` | `ctx_f0325fb8ed1c` | `task-improve-spec-brief.md` | **완료** — 14파일(+439/-104)·SPEC 9건·WP-129(11ph)·lint 0 error. 코디 검증 통과 |
| planner (WP분할) | `term_cebda8f1-69e5-48e4-96d1-959d1571e3f2` | `task_e4320572ce09` | `ctx_cfc10c5dca3c` | `task-improve-wp-split-brief.md` | **완료** — work-129-task-request-axis / work-130-task-detail-unification, lint 0 error |
| reviewer_spec | `term_ee356877-f0bb-4c14-9a80-c669e7572741` | `task_1b33f63a5a30` | `ctx_09e8a61f1703` | `task-improve-review-spec-brief.md` (갱신본) | **완료 — FAIL 1건(V-1)·WARN 5** (`review-spec-report.md` 덮어씀) |
| planner (V-1 정정) | `term_e4a8e702-f8cc-4301-afc8-e3682d3ee247` | `task_8562cefc1238` | `ctx_14133525206b` | `task-improve-spec-fix-brief.md` (V-1) | **완료** — 5파일 정정·정합 grep 통과·lint 0 error |
| reviewer_spec (R2) | (종료) | `task_c346992314a3` | `ctx_a49932c2b1c3` | (인라인 targeted 스펙) | **완료 — PASS** (V-1 해소·새 모순 0). 리포트 R2 절 append |
| backend (WP-129) | `term_09a7da3b-8568-4294-a0f2-8bb785d6d2c1` | `task_b28f7175c8fd` | `ctx_63b04e39acdb` | `task-improve-be-brief.md` | **완료** — 1099 passed 0 failed·신규 49(코디 독립 재실행 49 passed)·인덱스 1건 왕복·입구 8자리(6번째 발견 — WP 환류 필요). 주의: P0 DB 실측 3건 Pre-deploy 이월·채팅 DM pre-commit 비대칭 |
| reviewer_code | `term_f46dd57c-2142-4802-82ee-6d7348c1a92c` | `task_095b7894d65c` | `ctx_8096351ebdd0` | `task-improve-review-code-brief.md` | **완료 — WARN(FAIL 0)** 계약 8항 전량 PASS·WARN 7 (`review-code-report.md`) |
| backend (W1·W2 정정) | `term_ac3b7874-a0c5-4eda-875c-ad63c2e7f319` | `task_da87a5a57baf` | `ctx_079fb6329fb8` | `task-improve-be-fix-brief.md` | **완료** — 술어 repositories/task_request 이동·RETIRED 1정본. 코디 재검증(역전 grep 0·49 passed) |
| planner (시안 v1) | `term_4750cc78-e9ac-4be2-afc4-f19b9495ebed` | `task_11ca10913e36` | `ctx_93b13db65cbb` | `task-improve-spec-design-brief.md` | **완료** — 6파일 +353/-158·㉘ 신설·OQ-22/23/24·gap 3건 서버작업 0·WP-130 BLOCKED 0·취소선 33. 코디 검증(lint 0·잔존 0) 통과 |
| reviewer_spec (시안) | `term_81c74bc8-d21d-49b5-bb66-fa7bd70fd11f` | `task_29827dd299ec` | `ctx_4f27de632204` | `task-improve-review-design-brief.md` | **완료 — FAIL 2(사이드바 224 vs SPEC-220 288·[⋯] 열거 분열)·WARN 6.** 판정 6·규율 3·gap 3 PASS (`review-design-report.md`) |
| planner (시안 정정) | `term_810cffca-5f9e-4b2f-b254-a35bf47fe872` | `task_e80524c05b7f` | `ctx_5a6b5fae4dea` | `task-improve-design-fix-brief.md` | **완료** — F/W 전건 착지·lint 0. 잔존 3건은 코디 원라이너로 닫음 |
| reviewer_spec (시안 R2) | (종료) | `task_ea89dea9de20` | `ctx_9b6614eff81d` | (인라인 targeted) | **완료 — PASS** (8건 착지·잔존 0·새 모순 0) |
| backend (WP-130) | `term_aa0d993b-5fba-46bc-a8df-97456df89d42` | `task_470494f7302b` | `ctx_851299703bb3` | `task-improve-be130-brief.md` | **완료** — 447 passed(코디 독립 43)·migration 0138 3객체·완료 422(파생 면제=OI-2 확정)·storage_guard 공용화·첨부 스테이징 A+turns seam. 미결 8: planner 환류 ⓐ(§6.1 카드 문구 착지)ⓑ(size_bytes 문서)ⓒ(WBS 모달→FE 지시) |
| frontend (연결 4건) | (같은 터미널) | — | — | (터미널 지시) | **완료** — 4건 전부(+회귀 5건·purpose 읽기 호환·첨부 칩 링크 없음·WBS 모달 completionNote). tsc 0·1826 pass. 코디 통합 검증(63 passed·tsc 0) 통과 |
| reviewer_code (130) | `term_cfeb4671-85ba-4262-a357-4ad711a1f3d1` | `task_32ed59e137dc` | `ctx_f2916fea8d96` | `task-improve-review-code130-brief.md` | **완료 — FAIL 3**(①WBS 테스트 26건 미갱신 ②다중 파일 첨부 유실 ③바인딩 오소비)·WARN 9·계약 전부 통과. 미결 ⓐⓑ = 코드 옳음·문서 환류 (`review-code130-report.md`) |
| backend (130 fix) | `term_65f9915c-f6b1-4a79-ad04-9427f15c5797` | `task_acb0f92e6e6c` | — | `task-improve-be130-fix-brief.md` | **완료** — 2파일 갱신(신규 6·선행 20 다 고침)·바인딩 3겹·수정카드 봉인·25MB 선검사. 163 passed(코디 독립 80). ⚠ 도중 전체 스위트 실행 시도 — 코디 중단·타겟 재지시 |
| reviewer_code (R2) | (종료) | `task_7ef68552b63f` | `ctx_69d14d2879fc` | (인라인 targeted) | **완료 — PASS** (FAIL 3 해소·계약 불변). 병합 전 필수: CI 전체 1회·W-2 배포 공지 |
| planner (최종 환류) | (종료) | `task_628c01383c2f` | — | `task-improve-spec-final-brief.md` | **완료** — 7항목 착지(㉙·§6.1 정정·첨부 3겹 문서화·모달 정정 반영·WP in_dev)·커밋 73414aea2·코디 검증 후 푸시 |
| frontend (130 fix) | `term_388b9379-1cd5-4134-bdc6-33f606386682` | `task_e6ea49f9bc56` | — | `task-improve-fe130-fix-brief.md` | **완료** — 직렬화 사슬(회귀 5)·fallback 서버 body 한 벌·tsc 0·1831 pass |
| frontend (WP-130) | `term_31c79c8f-b189-434a-9588-5d0826c5b894` | `task_ddd0f7fb46d4` | `ctx_46395fba91ad` | `task-improve-fe130-brief.md` | **완료** — 39파일·신규 테스트 33건·tsc 0·vitest 1821 pass(실패 6 선행 실측)·AC-4 정정 반영(WBS 원클릭·TaskWbsViewAction 한 벌). 미결 0 |
| frontend (WP-129) | `term_db69e4ab-b5cc-47a8-b9aa-49f2a74d30cb` | `task_dc584d2a1c5b` | `ctx_7cc43cfefbf9` | `task-improve-fe-brief.md` | **완료** — front/ 4파일(+139/-2)·요청자 행·회귀 5건·tsc/prettier 통과·fail-closed. 코디 diff 범위 확인. 미결: 메타 그룹 제목 라벨(SPEC 트리 «담당·요청·조직») 1건 |

(롤백 전 라운드 — planner `task_d44242109c1d` 완료 / reviewer FAIL / R2 `task_be7b3d01f252` 중단: 전부 2026-09-01 사용자 지시로 종료·롤백)

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/675 (522f485ac 요청 축 + ae53ad84f 시안 v1 + 73414aea2 최종 환류)
- code PR: https://github.com/MediSolveAIDev/mediness-app/pull/140 (5b98247a WP-129 + db4bcfab WP-130 + 3573ecf4 모달 정정 — R2 PASS)
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-09-01` **릴리스 완주**: dev 스쿼시 머지→CI→ArgoCD 검증 → main 릴리스(#667 충돌 해소·doc_no 재발번 포함, #138) → prod 롤아웃·0138·health 검증 → k8s_infra#2 hostPath 머지·마운트 실측. Pre-deploy 실측 4건 전부 안전(고아 60=설계 대상)

- `2026-09-01` 실기동 검증 라운드 종료 — 카드 결재자 축 수리(9aad87f9)·빈 축 상시 표시(9d790f5f) → PR #140 최종 코멘트. 사용자 지시로 머지 단계 진입, WP-131 환류는 머지 후. v2 이월 +1(기존 초안 첨부 추가)

- `2026-09-01` **실기동 수리 사이클(카드 본문·모달 첨부) 완주** — 3라운드(카드 BE·카드 FE·모달 첨부) → 코디 통합 검증(BE 105·MCP 45·FE 66·tsc 0) → 커밋 bf8f1bba. 이월 목록: task.draft 의 참조자·완료예정 축(초안 LLM 산출 스키마 변경 필요 — 별도 라운드, 발주 보류)

- `2026-09-01` **사이클 완결**: 최종 환류 커밋 73414aea2 푸시(PR #675 3커밋 확정) · 자료 추가 모달 정정(사용자 반려 → 코디 직접, 3573ecf4) · worker 기동(채팅 실동작) · orchestration reset·터미널 정리. 남은 것 = 사용자 머지 + 배포 사전조건

- `2026-09-01` WP-130 코드 사이클 완주: BE+FE → 검수 FAIL 3 → 정정(BE 3겹 바인딩·FE 직렬화·코디 배지 한 줄) → R2 PASS → 커밋 db4bcfab·PR #140 갱신(제목 WP-129·130 통합, 병합 전 필수 2건 코멘트). 최종 스펙 환류 발주

- `2026-09-01` 로컬 스택 기동(back·mcp 워크트리 override + front dev :23001, migration 0138 적용) → 사용자 실기동 반려 1건(헤더 배지 2줄) 코디 직접 정정(TaskDetailShell 한 줄 병합). 검수 FAIL 3건 → BE/FE fix 라운드 발주

- `2026-09-01` 시안 v1 스펙 사이클 완주: planner ㉘ → 검수 FAIL 2·WARN 6 → 정정(+코디 원라이너 3) → R2 PASS → 커밋 ae53ad84f, PR #675 갱신. 완료 워커 터미널 정리

- `2026-09-01` WP-129 코드 사이클 완주: BE(1099 passed)+FE(회귀 5) → reviewer_code WARN(FAIL 0) → W1·W2 정정 → 코디 재검증 → **code PR #140**. 병행: planner 시안 v1 스펙 개정 진행 중

- `2026-09-01` 사용자 WP 승인 → 스펙 커밋·push·spec PR #675 → WP-129 코드 발주(BE P0~P3·P5·P6 / FE P4 병렬)

- `2026-09-01` **스펙 단계 완결** — planner 본 라운드(14파일)→WP 2건 분할→검수 FAIL 1(V-1)→ⓐ안 정정→R2 PASS. 사용자 WP 리뷰 대기. 워커 터미널 정리

- `2026-09-01` **결정 재확정 + planner 재발주 (task_b6eedbabdb93)** — 롤백 후 사용자와 문답으로 §2 결정 15건 확정(파생 판정·cc 폐지·상세 5부·task_references·완료 모달·채팅 채움/첨부·샤라웃 지시 전면 배제·저장 경로 medi-me 실측·세부 3건 추천 채택). 발주 계획 사용자 승인 후 최종 브리프로 발주
- `2026-09-01` **전면 중지 + 롤백 (사용자 지시: "확인도 안 받고 작업하니까 이 모양")** — 워커 3기 종료(R2 planner·reviewer·구 planner)·orchestration reset·스펙 워크트리 clean 복원. 교훈: **스펙(설계 문서) 작업도 코드와 같다 — 발주 전에 반영 계획을 사용자에게 보여주고 승인받는다.** 런북의 "자동 발주" 원칙보다 사용자 게이트가 우선
- `2026-09-01` reviewer_spec 검수 완료 — FAIL 6건(V-1~6: 구 「담당자 본인 고정」 활성 잔존)·WARN 5·결정 SoT 위반 0 → planner R2 발주(task_be7b3d01f252)
- `2026-09-01` 사용자 지시: 샤라웃 «테스크 요청 지시» 걷어내기(주석만)·AX 채팅 요청 = 테스크 생성 축 — §2 결정 기록, 경계 확인 중

- `2026-09-01` planner 완료(8파일: 스펙 154·155·230 + runtime_task + WP-129 + 인덱스 3종 동기) → 코디 검증(diff 범위·lint exit 0·게이트 부재 grep) → reviewer_spec 발주 (task_141f321b02b2)
- `2026-09-01` 사용자 지시: 페이지 디자인은 사용자 직접 — planner Q1·Q2 를 «시안 대기» 슬롯으로 전환 지시, 데이터 계약만 확정 진행
- `2026-09-01` new-work.sh 세팅(planner·backend·frontend 브리프 + 워크트리 2벌) → planner 브리프 채움(확정 결정 8건 + 사용자 주도 디자인 절차) → planner 발주 (task_d44242109c1d)

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
