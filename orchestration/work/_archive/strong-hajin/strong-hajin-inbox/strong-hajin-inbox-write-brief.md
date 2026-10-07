# [writer] BASE-006 · DEC-008 — 외부 채널(메일·슬랙·카톡) 연동 · 메시지함 · 프로필 설정

너는 strong-hajin `writer` 워커다. **맥락이 없다** — 아래가 전부다. 먼저 역할 문서를 읽어라:
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/roles/strong-hajin/planner/role.md` (+ 같은 폴더 rules·skills·tools·workflow — writer 는 planner 역할을 쓴다)
- 문서 규칙 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/project.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진` — **코디네이터 워크트리다. 코디가 같은 곳에서 일한다. §5 의 파일만 쓴다.**

## 1. SSOT — 먼저 읽을 것
- **결정 원장 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/_RESUME.md` §2** ← 이 문서들의 **유일한 결정 근거**. 2026-10-05~06 행 전부. **취소선 행은 뒤집힌 결정** — 뒤집힌 것으로 기록하라. **여기 없는 결정은 발명하지 마라**(열린 것은 Open Questions 로)
- 조사·실측 리포트(baseline 의 관측 근거): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-survey.md`(원래 시안 조사) · `kakao-survey.md` · `kakao-attach-survey.md` · `kakao-db-fields.md`
- 시안 변경 기록(확정 시안 = 정본): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/design-change-1.md` ~ `design-change-6.md` · 로컬 사본 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/reference/2026-09-10-sc-meeting/package 2/` (`Inbox.html`=메시지함 · `Settings.html`)
- 실물 시험 결과(_RESUME §2 2026-10-06 행): Gmail API 동의 1회 readonly+send · Slack 사용자 토큰 10권한·방 목록 실측
- 형식 본보기: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/00-baseline/baseline-005-task-detail.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-006-task-detail.md` (frontmatter · 절 구성 · 표 · 결정 번호 D-n · OQ 번호)
- 관련 기존 문서(링크·어긋남 기록용): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/20-spec/spec-001-work-management.md`(기존 업무 > 수신함) · `decision-001-work-page.md` · `decision-005-tauri-wrapper.md` · `decision-007-production-deploy.md`(hostPath 바인드 마운트) · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/mykakao/`

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 쓰나
slug `strong-hajin-inbox` 에서 시안 → 정책을 사용자와 닫았다. 이제 그걸 문서 파이프라인 첫 두 칸으로 올린다:
- **BASE-006** (raw) — 들어온 것과 관측: 사용자 원문 요구 · 원래 시안(설정·수신함)이 그린 것 · 기존 「업무 > 수신함」 · 메일/슬랙 실물 시험 결과 · 카톡 조사 3건(조회 가능·발송은 UI 자동화·첨부 CDN 만료·DB 필드·kakaocli 이 기기 실패) · 시안 변경 6판
- **DEC-008** (proposed) — 결정: `_RESUME.md` §2 를 **주제별로 묶어** D-n 으로. 권장 묶음: 범위·단계 / 화면 역할(메시지함 vs 업무>수신함) / 메일 / 슬랙 / 카톡 / 실시간·백필 / 저장·소유·삭제·첨부 / 답장 / 프로필 설정 / 시안과 달라진 점(한 줄 목록). 각 결정에 날짜·근거(사용자 지시/결정/코디 기본값). 뒤집힌 것은 취소선 + 뒤집은 결정 번호
- **2단계(AX 판단 — 생성/업데이트/패스 → 업무>수신함)** 는 「다음 단계로 미룬 것」 절로. 이벤트 단위 등은 미결로

## 3. 계약
해당 없음 (문서만). spec·work 는 쓰지 마라 — 다음 판이다.

## 4. 먼저 읽을 핵심 파일
§1 순서대로. `_RESUME.md` §2 가 길다 — 행을 빠짐없이 DEC-008 어딘가에 대응시켜라(대응표를 DEC-008 끝 부록으로).

## 5. allowed_paths — 이 밖은 건드리지 마라
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/00-baseline/baseline-006-external-channels.md` (새로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/decision-008-external-channels.md` (새로)
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/00-baseline/README.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/para/projects/summer-star/strong-hajin/10-decision/README.md` — **표에 한 줄씩만 추가**(기존 행 고치지 마라)
- 그 밖 금지 · 커밋·push 금지

## 6. 구현 단계
1. §1 을 읽는다
2. BASE-006 작성 — 관측과 입력만, 결정 문장 금지
3. DEC-008 작성 — 결정 D-n · Open Questions(OQ-801~ — 아래 §6-4) · 다음 단계로 미룬 것 · 부록 대응표(_RESUME §2 행 → D-n)
4. 열린 것으로 남길 것(결정 원장이 「미결」로 둔 것 + 시안 변경 기록의 미결 중 정책인 것): 운영 GCP 프로젝트 이전 시점(이직·상용) · 카톡 DB 를 못 읽는 경우 표시 · 상태 카드에 앱이 올릴 수 있는 정보 · 좁은 화면 3열 · 그 밖 원장에서 「미결」인 것. **구현 세부(테이블 이름·API 경로)는 결정이 아니다 — 쓰지 마라**
5. README 표 두 줄

## 7. 범위 제약 — 하지 말 것
- 결정을 새로 만들지 마라 · 원장과 다르게 고쳐 쓰지 마라 · 코디 기본값은 「코디 기본값(사용자 이의 없음)」으로 표시
- 실명·실제 URL·토큰을 쓰지 마라(시험 결과는 숫자·권한 이름만)
- spec/work/로그/회고 금지

## 8. 검증
```
_RESUME §2 의 모든 행이 DEC-008 부록 대응표에 있다 · 뒤집힌 결정 3건(삭제→소프트 딜리트 · 사용자 테이블→별도 테이블 · 서버 키·방ID→로컬) 이 취소선으로 남아 있다 · BASE 에 결정 문장 없음 · frontmatter 가 본보기와 같은 키
```
- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --from term_3fb95c1b-5d7d-4bcd-8409-b1dba0fbfdea \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4c7ad25d-d490-4978-9a1b-cd710c3fac2b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
