
# [planner] 업무 요청 도입 + 태스크 상세 5부 통일 — 스펙 반영 + WP 작성 (R2 전면 재발주)

너는 **mediness `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec` — **base(origin/mediness)와 동일한 깨끗한 상태다. 직전 라운드 산출물은 사용자 지시로 전부 롤백됐다** — 이 브리프가 유일한 발주다.
base 브랜치: `origin/mediness` → 최종 PR 대상 `mediness` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것

**결정의 SoT (코디 레포, read-only 절대경로 — 여기 없는 건 발명하지 마라):**

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` **§2 결정 표 전체** — 2026-09-01 사용자와 문답으로 확정한 결정 십수 건이 이번 발주의 전부다. **이 표와 어긋나는 스펙을 쓰지 마라. 확정된 결정을 다시 논의하지 마라.** 아래 §3 은 그 표의 요약이다 — 두 곳이 다르면 _RESUME §2 가 맞다.

**기존 문서의 SoT (이 워크트리):**

- `products/mediness/40-architecture/domains/runtime_task.md` — 태스크 원장 정본(5값 enum·전이표·TaskEvent 어휘). **상태 축·이벤트 어휘를 건드리지 않는다**
- `products/mediness/20-spec/spec-154-decision-workflow.md` §4.8(본문 양식·생성 surface)·§4.19(통합 상세 셸) — 개정의 주 착지점
- `products/mediness/20-spec/spec-155-ax-task-draft-workflow.md` · `spec-230-landing-agent-chat.md` — 채팅 생성 계약
- `products/mediness/20-spec/spec-111-decision-intake-slack.md` · `spec-156-decision-chat-intake-workflow.md` — 샤라웃 intake(지시 입구 차단 대상)
- `products/mediness/20-spec/spec-119-decision-notify-slack.md` — Slack DM 인프라(재사용, 신설 금지)
- `products/mediness/20-spec/spec-127-department-document-storage.md` — 파일 저장 관례 선례(path-guard·storage root)
- `products/mediness/40-architecture/erd.md` — 컬럼·테이블 신설 반영 대상
- `products/mediness/30-work/work-126-task-ledger-unification.md` — WP 문서 형식 선례

기대는 개념 — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

태스크 원장은 5값 모델로 통일됐지만(WP-126), ① 남에게 일을 시키는 통로가 무거운 샤라웃(의사결정 등록) 지시 유형뿐이고 ② 태스크 상세에 담기는 내용이 출처마다 다르며(수동=자유 텍스트 / AI 초안=마크다운 / decision·incident=원장 라이브 렌더) ③ 완료에 근거가 남지 않는다. 이번 작업이 세운다:

1. **업무 요청 축** — 게이트 없는 타인 배정(파생 판정), 진입점 2곳(모달·채팅), DM
2. **상세 5부 통일** — 배경/목표/Todo/참고자료/완료 산출물/진행로그, 원장 렌더 폐지
3. **완료 근거** — 완료 모달(산출자료 또는 완료기록 필수)
4. **샤라웃 지시 유형 입구 차단** — 주석 비활성, 재활성 가능

산출물 = **관련 스펙 개정 + WP 문서 1건**(다음 빈 번호, 현재 최대 work-128 — upstream 선점 시 코디가 재번호). 코드 발주는 사용자 WP 리뷰 뒤 별도.

## 3. 계약 (2026-09-01 사용자 확정 — 이대로 반영)

**A. 업무 요청 축**

1. 요청 판정 = **파생**: 비워크플로 task_type(`manual.*`·`ai.*`) ∧ `created_by_member_id ≠ assignee_member_id`(둘 다 NOT NULL). 새 컬럼·새 task_type·새 상태·새 TaskEvent 0
2. 게이트 없음 — 수락·검수 어떤 형태로도 금지. 거부 동선 = 재배정 요청(담당자 본인 포함)
3. **요청자 자동 cc 없음** — 식별·«내가 요청한 일» 조회 전부 `created_by` 파생. cc 는 사용자가 직접 지정할 때만
4. DM = spec-119 인프라 재사용(요청자·제목·딥링크 1개), **실패해도 태스크 생성**(graceful — incident fail-loud 와 다른 축, 혼동 금지)
5. 진입점 2곳: 생성 모달 담당자 개방 + 채팅 발화 패턴 **«태우님께 000 업무 요청 해줘»**(담당자는 발화 명시 시에만 해소, 모호하면 요청자 본인). 배정 후보 범위 = 같은 조직 활성 구성원
6. 요청자 권한: 자기가 요청한 태스크 **수정(배경·목표·기한)·취소 가능**. 상태 전이는 담당자만

**B. 상세 5부 통일**

7. 구조 = **배경 / 목표 / Todo / 참고자료(출처 자동 + 링크·파일) / 완료 산출물 / 진행로그(댓글 포함)**
8. `tasks.background`·`tasks.goal` **컬럼 신설**(nullable text) — §4.8 의 「description 마크다운 한 자리」 관례 폐지. `description` 은 legacy fallback(background/goal 비면 표시)
9. **decision·incident 원장 라이브 렌더 폐지** — 생성 시 워크플로가 배경·목표·체크리스트를 스냅샷 저장. 원문은 execution 사슬 출처 링크로. §4.19 의 출처별 조건부 블록을 이에 맞게 정리
10. 댓글·로그 = 현행 `task_events` 유지(event_type=comment 구분, 수정·삭제 없음). 신설 0

**C. `task_references` 테이블 신설**

11. `role`(reference/deliverable) × `kind`(link/file). 컬럼: task_id FK·url·file_path·filename·title·created_by_member_id·created_at·**deleted_at(soft delete)**
12. 출처는 행으로 저장하지 않음 — 화면 참고자료 첫 줄에 execution 사슬로 자동 렌더. 추가 내부 참조는 link 행
13. 링크 = 하이퍼링크 렌더(내부 URL 딥링크). 첨부 표시 = **기본 다운로드 카드 + 이미지(png/jpg/gif/webp)만 인라인**. 비이미지 인라인 금지(XSS)·`Content-Disposition: attachment`
14. 파일 제한: 파일당 25MB·실행파일류 차단 목록·개수 제한 없음. 권한: 접근 가능자(담당자·요청자·cc) 추가, 삭제 = 올린 본인+담당자+요청자
15. 저장 경로: env `TASK_REFERENCE_STORAGE_ROOT` 기본 `/app/var/task-references`, 레이아웃 `{task_id}/{reference_id}_{원본파일명}`, 부서공간 path-guard 패턴 재사용, DB 엔 상대경로만. **배포 사전조건: k8s_infra_mac 차트에 hostPath(`/mnt/mac/task-references`·`-dev`) 볼륨 추가 PR 별도** — WP 에 명시

**D. 완료 모달**

16. 완료(→done) = 모달 경유, **산출자료 / 산출자료+완료기록 / 완료기록 중 하나 필수** — 빈손 완료 불가. **서버도 강제**(둘 다 없으면 422). 저장: 완료기록 → `task_completed` 이벤트 payload / 산출자료 → task_references(role=deliverable)
17. **시스템 액터 완료는 예외**(워크플로 멱등 완료·incident 슬랙 [완료] 등). 수락·검수 게이트 아님 — 본인이 근거를 남기는 것

**E. 채팅**

18. 채팅 발 초안은 **배경·목표·체크리스트를 반드시 채워 산출** — 대화 맥락에서 AI 생성, 부족하면 되물음, 초안 카드에서 검수 후 확정. 「채팅은 입력구, 산출물은 채워진 DB」
19. 채팅 **첨부 업로드 신설** — `drafts/{draft_id}/` 스테이징 → 승인 시 task_references 귀속·태스크 경로 이동, 초안 폐기 시 정리

**F. 샤라웃**

20. 지시(실행 요청) 유형 **입구만 차단** — 슬랙(`/샤라웃`·봇멘션·폼)·채팅 intake(SPEC-156) 양쪽. **주석 비활성 수준 — 내부 워크플로 로직·원장 보존, 재활성 가능해야 함.** 결정 요청·공유·승인/결재 축 유지. + 개인 대시보드 «업무수행» 세그먼트·상세모달 배정·`/decisions/me/tasks`·배정 부트스트랩도 같은 주석 비활성
21. 앞으로 «일 시키기»는 전부 태스크 생성(A 축)으로

**G. migration 총계** — 컬럼 2(background·goal) + `created_by` 인덱스 1 + 테이블 1(task_references). 이 이상 늘리지 마라.

**H. 페이지 시안 대기** — /ax/tasks «내 할 일 / 내가 요청한 일» 화면 구조·요청 표기는 **사용자가 직접 디자인 중**. 스펙에 화면 구조를 확정으로 박지 말고 «사용자 시안 대기» 슬롯 + 시안이 지켜야 할 경계만 남겨라.

## 4. 먼저 읽을 핵심 파일

- `_RESUME.md` §2 (위 SSOT) — 전체 결정 원문
- `spec-154` §4.8·§4.19 — 본문 양식·상세 셸·생성 surface 표 (원장 렌더·마크다운 관례의 현행 서술 위치)
- `spec-155` §6·§7·§8·§9 — 채팅 초안 산출 스키마(배경/목표 마크다운 → 컬럼 전환·체크리스트 필수·담당자 개방)
- `spec-111`·`spec-156` — 지시 유형이 계약된 절(입구 차단 개정 노트 착지점)
- `spec-127` — 저장 관례(path-guard·env root) 선례 인용용

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/mediness/`
- `context/`

## 6. 구현 단계

1. `_RESUME.md` §2 정독 → 결정 → 문서 착지 지도 작성
2. 스펙 개정 — A~F 를 해당 스펙에 개정 노트 형식으로 반영. **«추가»만 하지 말고 구 서술(원장 렌더·마크다운 한 자리·본인 고정·지시 유형 활성 서술)을 grep 으로 찾아 취소선/정정하라** — 직전 두 라운드가 전부 이 잔존으로 FAIL 났다
3. ERD·도메인 문서 — background/goal·task_references 반영
4. WP 1건 작성 — BE phase 분할(생성 개방·requested 조회+인덱스·DM 훅·본문 컬럼·references CRUD+storage·완료 모달 seam·채팅 채움/첨부·샤라웃 입구 주석) + FE phase(시안 대기 표시). migration 총계·k8s_infra_mac 사전조건 명시
5. `python3 scripts/lint-pipeline.py --strict` — mediness 범위 ERROR 0 + 구 서술 grep 스윕 수치 보고

## 7. 범위 제약 — 하지 말 것

- 수락·검수 게이트 재도입 금지 / 새 상태·새 TaskEvent 발명 금지 / DM 인프라 신설 금지
- migration 을 §3-G 총계 밖으로 늘리지 마라
- 샤라웃 내부 로직·원장 재설계 금지 — 입구 차단만
- incident 워크플로(WP-127 축)·알림 고도화(OQ 로만) 금지
- 화면 구조를 사용자 시안 없이 확정하지 마라
- 열린 자리를 네가 정해야 하면 **«planner 판단 · 사용자 뒤집기 가능»** 표시를 반드시 남겨라
- 커밋·push·PR 금지 (§9)

## 8. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec && python3 scripts/lint-pipeline.py --strict
```

- 이번 제품 범위 ERROR 0 (SPEC-030 coverage WARN 1건은 선재분 — 무관 분리). 타 제품 기존 WARN/ERROR 는 "무관"으로 분리 보고.
- 구 서술 grep 스윕(`원장.*렌더|마크다운.*합침|본인 고정|## 배경`) 결과를 수치로 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] planner: <질문>" --enter`
