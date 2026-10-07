
# [reviewer] <한 줄 제목>

너는 **strong-hajin `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-inbox`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

<같은 워크트리를 다른 워커와 공유하면 여기에 경고를 적는다. 예: "BE 워커가 `back/` 에서 병렬 작업 중 — 건드리지 마라.">

## 1. SSOT — 검수 대상과 기준
**너는 read-only 리뷰어다. 코드를 고치지 않는다. 판정(PASS/WARN/FAIL)과 근거만 낸다.** 이 워크트리(코드, origin/main)는 **읽기만** 한다.
- 검수 대상: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-008-external-channels.md` (v0.2.0) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-009-mac-kakao-collector.md` (v0.2.0)
- 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` (accepted · D-01~D-50) + `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2 의 DEC-008 이후 행(2026-10-06 — 보존 없음 · 첨부 25/50MB · mykakao 방식 · SPEC OQ 처리 · 비밀값 위치) · 확정 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` + `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-1~6.md`
- 관련: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md`(I-2 개정 필요 표시) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/70-runbook/runbook-002-production-deploy.md` · 운영 차트 `/Users/kknaks/git/harness_works/k8s_infra_mac/charts/strong-hajin/`(읽기만)

## 2. 무엇을 보나
1. **결정 정합** — D-01~D-50 과 원장 후속 결정이 SPEC 에 빠짐·어긋남 없이 들어갔나(대응표만 믿지 말고 본문 계약에서 확인)
2. **코드 정합** — SPEC 이 근거로 든 파일:줄 32곳 이상이 실제와 맞나 · 계약이 지금 구조(모듈·인증/세션·워커 프로세스·schema_sync·settings env 로딩·materials 저장·프론트 라우팅·데스크톱 셸)에 **붙을 수 있나**. 붙기 어려운 곳은 구체적으로
3. **계약 완결성** — 구현 워커가 이 SPEC 만 보고 짤 수 있나: 데이터(키·제약·소프트 딜리트·중복 방지) · API(경로·요청/응답·오류) · 동기화(Socket Mode 단일 소유 · Gmail watch 갱신·pull · 백필 진행률 · 재시작 메우기) · 첨부(중계·hostPath·한도) · 답장(스레드·첨부) · 카톡 업로드·상태 · 프로필·비밀번호
4. **UX 정합** — 시안 화면·상태가 UX Contract 에 다 있나(메시지함 2/3열 · 답장 상태 · 설정 세 연동·프로필 · 네 상태)
5. **SPEC 둘 사이 계약**(SPEC-008 §4.6 ↔ SPEC-009) 일치
6. **위험** — 비밀값 노출 · 권한/소유 누수(남의 메시지) · 운영 배치(레플리카·hostPath·Secret 마운트) · SPEC-006 개정 범위
7. SPEC-009 는 DB 여는 절차를 **일부러 비웠다**(참조만) — 그걸 FAIL 로 치지 마라. 경계 입출력이 충분한지만 본다

## 3. 계약
해당 없음.

## 4. 먼저 읽을 핵심 파일
§1 순서.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-008-009.md` **하나만** 새로 쓴다. 코드·문서 수정 금지 · 커밋 금지

## 6. 구현 단계
1. 읽기 → 2. 항목별 판정 표(항목 · 판정 · 근거 파일:줄 · 고칠 것) → 3. 총평 PASS/WARN/FAIL 하나

## 7. 범위 제약
- 고치지 마라 · 새 정책 제안은 「제안」으로 따로(판정과 섞지 마라)

## 8. 검증
```
모든 FAIL·WARN 에 근거 파일:줄과 고칠 것 한 줄 · 총평 하나
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_fd936f8b-e332-4fa6-b892-ad24d3e754cd \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
