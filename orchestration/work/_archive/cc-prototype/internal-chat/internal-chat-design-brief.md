# [designer] 직원 앱 내부 채팅 시안 — 방 목록 · 대화 · 새 방 · 방 정보 (폰 · 아이패드)

너는 **cc-prototype `designer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/roles/cc-prototype/designer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅` (코디 워크트리)
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 코디네이터 워크트리다. `orchestration/work/internal-chat/design/` 과 리포트 1개 말고는 아무것도 만들거나 고치지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` ← **화면에 그릴 기능의 정본. D-01 ~ D-34 에 없는 기능은 그리지 마라**
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md`: 사용자 입력 원문
- `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md`: §6.0 공통 원칙 · §6.8 공통 틀(탭바 · 레일 · 헤더 · 숨김 규칙) · §6.9 · §6.13 알림 목록 · §6.14 설정 · §6.6 테마
- 기준 시안(읽기만): Claude Design 프로젝트 `dda9a931` 의 「Ceramique 의료진 앱 (구현 v3)」 · 「Ceramique 간호사 모바일 (구현 v3)」 · 「Ceramique 시술실 태블릿 (구현 v3)」(.dc.html). **실제 앱 화면을 다시 그린 것이라 이것이 모양 기준이다**

**기대는 개념**: 해당 없음

## 2. 배경

직원 앱(Flutter · iOS · 폰 + 아이패드)에 직원끼리 쓰는 메신저를 넣는다. 사용자 말로는 「텔레그램처럼 그냥 메신저, 사진, 이런 것만」. 사용자가 시안을 먼저 보고 확정한 뒤에 SPEC 을 쓴다(DEC-009 D-06). 확정된 시안이 화면 정본이 된다.

## 3. 그릴 것 — 화면 · 상태 목록 (정본 = DEC-009)

**새 파일 하나**: 프로젝트 `dda9a931` 안에 「Ceramique 의료진 앱 — 채팅.dc.html」. 폰 장면과 아이패드 장면을 같이 둔다. 기존 파일은 열어서 읽기만 한다.

공통 틀: 기준 시안의 헤더 · 폰 아래 탭바 · 아이패드 왼쪽 레일을 그대로 쓰고, **「채팅」 탭을 설정 앞 5번째 칸**에 더한다. 탭에는 안 읽은 방 수 배지가 붙는다(D-20 · D-33).

| # | 화면 · 상태 | 꼭 보여야 할 것 | DEC |
|---|---|---|---|
| S1 | 방 목록 | 1:1 · 그룹 섞임 · 방 이름(그룹 이름 없으면 참여자 나열) · 마지막 메시지 미리보기(사진이면 「사진」 · 지운 메시지면 「삭제된 메시지예요」) · 시각 · 안 읽음 배지 · 알림 끈 방 표시 · [새 대화] 버튼 | D-09 · D-17 · D-20 · D-29 |
| S2 | 방 목록 비어 있음 | 첫 사용 안내 + [새 대화] | — |
| S3 | 새 대화 — 상대 고르기 | 계정 목록(이름 · 역할 칩) · 검색 · 한 명 = 1:1, 여러 명 = 그룹 · 그룹이면 이름 입력(선택) · 인원 한도 2~20 | D-05 · D-08 ~ D-10 |
| S4 | 대화 — 1:1 | 말풍선(내 것 / 상대) · 날짜 구분선 · 시각 · 텍스트 · 사진 1장 메시지 · 「삭제된 메시지예요」 자리 · 아래 입력창 + [사진](카메라 · 앨범) + [보내기] | D-03 · D-15 · D-17 |
| S5 | 대화 — 그룹 | S4 + 보낸 사람 이름 · 시스템 메시지 한 줄(「A 님이 B 님을 초대했어요」 · 「A 님이 나갔어요」) · 비활성 계정 「(비활성)」 | D-11 · D-14 |
| S6 | 보내는 중 · 보내기 실패 | 보내는 중 표시 · 실패하면 [다시 보내기] | D-16 |
| S7 | 사진 고르기 | 카메라 / 앨범 고르는 시트 · 올리는 중 | D-03 · D-22 |
| S8 | 사진 크게 보기 | 전체 화면 · 닫기. **저장 버튼 없음** | D-24 |
| S9 | 내 메시지 길게 누르기 | [삭제] 하나(내 메시지만 · 남의 메시지엔 메뉴 없음) · 삭제 확인 | D-17 |
| S10 | 방 정보 | 참여자 목록 · [참여자 추가](그룹만) · 알림 끄기 토글 · [나가기](그룹) / [목록에서 숨기기](1:1) · 그룹 이름 | D-10 · D-12 · D-13 · D-29 |
| S11 | 앱이 앞에 있을 때 다른 방 새 메시지 배너 | 기존 시안의 배너 모양 · 보고 있는 방이면 안 뜬다(설명 주석으로) | D-28 |
| S12 | 잠금 화면 푸시 | 보낸 사람 + 본문 앞부분 · 사진이면 「사진」 · 같은 방 묶음 | D-27 · D-32 |
| S13 | 아이패드 | 왼쪽 레일 + 방 목록 + 오른쪽 대화(두 칸) | D-33 |

샘플 데이터: 가짜 이름 · 병원 업무 같은 가짜 대화(예: 「3번 방 마취 들어갔어요」). 실명 · 실제 고객 정보 0.

## 4. 먼저 볼 곳

- 기준 시안 3개 파일 전체(헤더 · 탭바 · 레일 · 카드 · 칩 · 시트 · 배너 · 입력창 모양)
- SPEC-004 §6.8 (탭 · 숨김) · §6.13 (알림 목록 모양)

## 5. allowed_paths — 이 밖은 건드리지 마라

- Claude Design 프로젝트 `dda9a931` 의 **새 파일 「Ceramique 의료진 앱 — 채팅.dc.html」 하나만** 만들고 고친다 (DesignSync). 기존 파일은 읽기만
- 로컬 사본: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design/` (새 파일 사본 + 짧은 README)
- 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/design-chat-report.md`

## 6. 단계

1. §1 을 다 읽는다
2. §3 S1 ~ S13 을 새 파일에 그린다
3. 로컬 사본을 `design/` 에 둔다
4. 리포트를 쓴다(rules.md 형식 · S1 ~ S13 대조표 · DEC 와 다르게 그린 곳 · 제안)
5. §9 두 채널로 보고한다

## 7. 하지 말 것

- 기존 Claude Design 파일 수정 · 삭제 금지 · 다른 프로젝트 금지
- DEC-009 에 없는 기능 금지 — 반응 · 답장 · 스레드 · 수정 · 파일 · 음성 · 타이핑 표시 · 상대 읽음 숫자 · 사진 저장 · 강퇴. 넣고 싶으면 리포트 「제안」으로만
- 새 색 · 새 폰트 · 새 컴포넌트 언어 금지 — 기준 시안 그대로
- 코드 · para 문서 수정 · 커밋 · push · PR 금지
- 실명 · 키 · 계정값 금지(public 레포)

## 8. 검증

```
브리프의 화면 · 상태 목록이 시안에 전부 있다(화면별 이름 표) · 로컬 사본이 프로젝트와 같다 · 기존 시안의 테마 · 컴포넌트만 쓴다 · 가짜 값만(실명 · 키 0) · 기존 파일 무수정
```

- 리포트에 S1 ~ S13 각각 「있음 · 장면 이름」. 없으면 이유
- 리포트 끝에 `git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short` 결과

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
  --subject "designer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e \
  --text "[worker_done] designer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_61179808-14b1-431b-a85f-619d2c232e8e --text "[질문] designer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
