# [reviewer] procedure/ 코드 리뷰 — WP1~WP5 (back · front)

너는 **cc-prototype `reviewer` 워커**다. 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/roles/cc-prototype/reviewer/role.md` (+ 같은 폴더)

리뷰 대상 워크트리(read-only): `/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2` 의 **`procedure/`**(커밋 전 · 미추적 파일). `cc/` 는 대상 아님.

## 1. SSOT

- 계약: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/20-spec/spec-003-procedure-board.md`(§5 상태 전이표 · 버튼 활성표 · §7 API/SSE · §8 KOS 반영 · §4 덮어쓰기 기준)
- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md` D-01~D-34
- 작업: `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/para/projects/summer-star/cc-prototype/30-work/work-003-procedure-board.md` WP1~WP5 완료 조건
- 워커 보고: backend(인박스 요약은 아래 §2) · frontend `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/wp5-frontend-report.md` · 스크린샷 `wp5-shots/`
- 결정 표의 사실 줄(HAR · 실호출): `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/_RESUME.md` §2

## 2. 워커가 이미 밝힌 것(재확인만)

- 시스템 계정 id = 내부 `get-user-account` data.id(sign-in id 아님) — SPEC §4.1 정정 후보
- `change-flow-step` 같은 단계로 보내면 400 → 같은 단계로 안 보냄 — SPEC 정정 후보
- `call-tasks-doctors` 400(귀가 대기 일정에서) — 미결, E2E 재확인 예정
- compose 에 front 서비스 없음(NEXT_PUBLIC_* build.args 필요) — **로컬 한 번에 띄우기가 막혀 있음**
- 호출 기준 5분이 front 상수 · `PROC_FAKE_BOARD` 계약 밖 env · 760px 미만 카드만 · 국적 코드 그대로

## 3. 볼 것 — 판정 FAIL · WARN · PASS, 각 지적에 `파일:줄` + 근거(SPEC 절 · D-번호)

1. **규칙 정확성**: 유효 호출(D-25 가장 최근 호출) · 수락 범위(D-27 그 호출의 미수락 시술만) · [시작] 조건(D-30 새 호출 뒤 꺼짐) · [종료](D-31) · 첫 [시작] = PROCEDURE(D-32) · 귀가 대기(D-33 방 빼기, 시술 완료로 방 안 비움) · 마취 별개(D-23) · 카드 조건(D-21 · 22) · 진행/완료 시술 호출 불가(D-26)
2. **KOS 연동**: 덮어쓰기 기준(D-09 — KOS 기준 필드 / ccc 기준 필드 / 반영 대기 보호) · 토큰 갱신 · 조회 시간 09~21 · 4층 · 1시간 직원/방 · 원장 목록 제외(D-11) · 반영 대기열 순서 · 실패 처리
3. **front 가 규칙을 다시 계산하지 않는가**(스냅샷 값만 쓰는가) · SSE 재연결 · version 순서
4. **보안 · public**: 키 · 토큰 · 비밀번호 · 이메일 · 실명 · KOS id 값이 코드 · 시험 · 고정값 · 로그에 0 · `.env` gitignore · 관리자 로그인 토큰 · `?token` SSE 노출 범위 · CORS
5. **로컬 실행**: `procedure/README.md` 대로 사용자가 한 번에 back + front 를 띄울 수 있는가(지금 막힌 곳 목록)
6. **조용히 통과하는 자리**: 시험이 가짜로 통과하는 곳 · 예외를 삼키는 곳 · KOS 실패를 성공으로 보는 곳
7. 기능 독립(`procedure` 밖 import 0) · 계층(api → service → repository, ORM 이 repository 밖으로 안 나감)

## 4. 산출물 — 이것만

- `/Users/kknaks/orca/workspaces/kknaks_profile/명동-POC-v2/orchestration/work/myeongdong-poc-v2/review-wp1-5-report.md` — 맨 위 판정 요약(FAIL n · WARN n) → 지적 표(번호 · 판정 · 파일:줄 · 내용 · 근거 · 고칠 방향) → 「SPEC 쪽을 고쳐야 하는 것」 따로

## 5. 하지 말 것

- 리포 파일 수정 · 실행 중인 프로세스 종료 · 데모 지점 KOS 쓰기(조회 · 코드 읽기만). 테스트 실행은 해도 된다(쓰기 0 · 사용자 포트 금지)
- 커밋 · push · PR

## 8. 검증

```
각 지적에 파일:줄 + 근거(SPEC 절 · D-번호). 판정 FAIL · WARN · PASS. 기능 독립 위반은 FAIL. 「조용히 통과하는 자리」를 따로 본다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6cc6a0d0-7bc9-484c-bd1a-0015e5c4f9de --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
