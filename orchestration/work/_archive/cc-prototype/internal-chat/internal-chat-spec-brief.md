# [planner] 직원 앱 내부 채팅 — SPEC-007 · WORK-011 작성

너는 **cc-prototype `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅` (코디 워크트리)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

## 1. SSOT — 먼저 읽을 것 (이기는 순)

1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` ← **결정 정본 D-01 ~ D-37 · OQ-901 · 902. 여기 없는 정책은 발명하지 마라**
2. 확정 시안 = 화면 정본(D-35): `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design/Ceramique 의료진 앱 — 채팅.dc.html` (sha `7148eb3fc0e0` · 장면 24) + `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design-chat-report.md` (r2 절이 위 · r1 의 S1 ~ S13 대조표 · 「확인할 것」 1 ~ 10)
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/research-mattermost-report.md`: §2 모델 · §3 흐름 · **§4 우리 코드에 붙일 자리(파일:줄)** · §5 매핑 초안
4. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md`: 사용자 입력
5. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md`: 지금 앱 계약(§3 계정 · §5-1 ~ §5-4 푸시 · 알림 · §6.8 공통 틀 · §7.1 SSE · §7.3 경로 수 · §7.4 표 · §8 검증 꼴)
6. 지금 구현(읽기만 · canonical · pull/checkout 금지): `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/ios/Runner/`

근거 표기 예: `D9-nn` = DEC-009 · `R§` = research 리포트 · `DS:Sn` = 시안 장면 · `S4§` = SPEC-004 · `코드` = 지금 구현(파일:줄).

**기대는 개념**: 해당 없음

## 2. 배경

직원 앱(procedure/app · Flutter iOS)에 직원끼리 쓰는 메신저(1:1 + 그룹 · 텍스트 · 사진 · 푸시)를 넣는다. 결정(DEC-009)과 화면 시안이 사용자 확정까지 끝났다. 이제 계약(SPEC)과 작업 순서(WORK)를 쓴다. 웹 화면은 없다(D9-01).

## 3. 쓸 것

### 3.1 SPEC-007 (새) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` · 0.1.0 · draft

SPEC-006 의 머리 · 근거 표기 · public 경고 꼴을 따른다. 담을 절(이름은 바꿔도 되지만 빠지면 안 된다):

- 범위 In / Out(D9-03 의 「없음」 목록 그대로)
- **표**: 방 · 멤버 · 메시지 · 사진(R§5 초안을 출발점으로 · 이름은 우리 말로 · D9-07). 만드는 방식은 지금 `db.py` 의 `CREATE TABLE IF NOT EXISTS` + `MIGRATIONS` 꼴. `push_log.kind` 에 채팅 값 추가
- **API**: 상대 목록(D9-05 · 로그인 필요 · `{id, name, role}`) · 방 목록(안 읽음 · 마지막 메시지) · 1:1 열기(재사용 D9-08) · 그룹 만들기 · 참여자 추가 · 나가기 · 1:1 숨기기 · 알림 끄기 · 메시지 목록(`before` · `since` · 50 · D9-19) · 보내기(`clientId` · D9-16) · 삭제(내 것만 · D9-17) · 읽음 · 사진 올리기 · 사진 열기(방 멤버만 · Bearer · D9-23). 각 API 의 요청 · 응답 · 오류 코드 · 권한. 경로 수 시험(`S4§7.3`)을 새 수로
- **SSE 이벤트**: 이름 · 페이로드 · 받는 계정(방 멤버) · 같은 계정 다른 기기(읽음). 웹이 안 깨지는 근거(D9-25)
- **푸시**: 대상(D9-26) · 내용(D9-27 · D9-36 제목 규칙) · 만료 1일(D9-31 · 호출 푸시는 0 그대로) · `thread-id`(D9-32) · 앱 앞 배너 거르기(D9-28) · 알림 목록 · 종 배지에 안 들어감(D9-30)
- **사진**: `PROC_PHOTO_DIR/chat/` · 앱에서 2048px 로 줄이기 · 5MB · 썸네일 없음 · 캐시 · 사진첩 저장 안 함(D9-21 ~ D9-24). 앱 패키지 · `Info.plist` 사진 보관함 문구(R§4.3)
- **앱 화면**: 시안 장면 24장을 화면 절로 옮긴다. 장면마다 `DS:Sn` 근거. 5탭(D9-33) · 탭 배지 · 숨김 규칙(D9-34) · D9-36 모양 값. 시안과 구현 사이 갈 수 없는 곳은 「시안과 다른 곳」 표로
- **앱 생명주기**: 백그라운드 = SSE 닫힘 → 앞으로 오면 `since` 로 메우기(R§4.1)
- **바뀌는 지금 코드 자리**: R§4 의 「바뀔 곳」 전부를 파일:줄과 함께(SSE 파서 허용 이름 · `push.dart` 모르는 kind · `apns.py` 만료 고정 · `AppTab` · `shell.dart` · 멀티파트 전역 한도 등). **R§4 를 다시 grep 해서 빠진 자리가 없는지 전수로 확인**하고, 리포트에 그 grep 명령과 결과 수를 적는다
- **검증**: back 단위 시험 목록(권한 · 1:1 재사용 · 중복 방지 · 삭제 · 안 읽음 · 나간 사람 · 사진 권한 · 푸시 대상 · 만료) · 앱 시험 · **실기기 iOS E2E**(두 계정 두 기기 · 백그라운드 푸시 · 사진 · 그룹 · 나가기 — 완료 조건 · 사용자 표면)
- **법적 검토 주석 자리**(OQ-902) · 열린 것(OQ-901 · 902 + 이 문서가 고른 기본값을 OQ-9xx 로)
- 부록: DEC-009 D-01 ~ D-37 → SPEC 절 대조표(빠짐 0) · 시안 장면 24 → 화면 절 대조표(빠짐 0)

### 3.2 WORK-011 (새) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md`

WORK-009 · WORK-010 꼴. WP 나눔: back(표 · API · SSE · 푸시 · 사진) → app(탭 · 방 목록 · 대화 · 사진 · 방 정보 · 푸시 · 생명주기) → REVIEW → 실기기 E2E. BE ∥ APP 병렬은 계약(API · SSE 페이로드)이 SPEC 에 다 있으면 허용. WP 마다 대상 파일 · 완료 조건 · 검증 명령(WP 범위만 · 전체는 마지막 한 번). infra 변경이 있는지(사진 폴더는 기존 PVC 하위라 없을 것으로 보임 — 확인해서 적어라).

### 3.3 함께 고칠 것 (최소)

- SPEC-004: frontmatter links 에 SPEC-007 한 줄 · §6.8 「4탭」에 「채팅 탭은 SPEC-007」 가리킴 한 줄 · §5-4 「종류는 둘뿐」 옆에 「채팅 푸시는 목록에 안 들어감(SPEC-007)」 한 줄. 그 밖은 고치지 않는다
- `20-spec/README.md` · `30-work/README.md` 행 추가 · `log.md` 한 줄 · DEC-009 는 고치지 않는다(코디 몫)

## 4. 먼저 볼 곳

- research 리포트 §4 (파일:줄이 전부 있다)
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/service/stream.py` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/push/apns.py` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/service/push.py` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/repository/db.py` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/back/app/api/photos.py`
- `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/sse/board_stream.dart` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/push/push.dart` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/app_state.dart` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/lib/screens/shell.dart` · `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app/ios/Runner/AppDelegate.swift`

## 5. allowed_paths: 이 밖은 건드리지 마라

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/` (SPEC-007 새 파일 · SPEC-004 위 3줄 · README)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/` (WORK-011 새 파일 · README)
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/log.md` 한 줄
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-report.md`

## 6. 단계

1. §1 을 다 읽는다(시안은 장면 24장 전부)
2. SPEC-007 → WORK-011 → §3.3 순서로 쓴다
3. 리포트(rules.md 형식 + 대조표 수치 + 전수 grep 결과 + 이 문서가 고른 기본값 목록)
4. §9 두 채널로 보고한다

## 7. 하지 말 것

- 코드 수정 · 커밋 · push · PR 금지. procedure 서버 · 앱 · docker 실행 금지
- DEC-009 에 없는 기능 금지(반응 · 답장 · 수정 · 검색 · 사진 여러 장 · 웹 화면 …)
- 결정이 필요한데 DEC 에 없으면 기본값을 골라 「기본값」으로 표시하고 OQ 와 리포트에 올린다. 혼자 확정하지 않는다
- public 레포 — 키 · 토큰 · 비밀번호 · 실명 · 연락처 · KOS id · Apple 팀 id 금지

## 8. 검증

```
SPEC 의 모든 절이 DEC · workflow · 시안 중 하나를 근거로 가리킨다. 근거 없는 정책 0 · 열린 것은 열린 것으로. 링크 · 인덱스 갱신. public — 키 · 실명 0(grep)
```

- DEC-009 D-01 ~ D-37 → SPEC 절 대조 빠짐 0 (수치)
- 시안 장면 24 → 화면 절 대조 빠짐 0 (수치)
- R§4 「바뀔 곳」 → SPEC 「바뀌는 코드 자리」 빠짐 0 + 다시 grep 한 결과
- 실명 · 키 grep 0 · 리포트 끝에 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short`

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_61179808-14b1-431b-a85f-619d2c232e8e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
