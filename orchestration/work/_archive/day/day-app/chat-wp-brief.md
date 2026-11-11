# [planner] DAY 채팅 Delivery235 v7 입력

이번은 SPEC 최종 독립리뷰 PASS 확인 뒤 발주할 WP 단계. 먼저 현재 spec tree /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec AGENTS.md 및 rules/delivery-workflow.md/document-pipeline.md, profile orchestration/roles/day/planner/ 지침, work/day-app/chat-decisions-20261110.md, chat-spec-report.md, chat-spec-review.md 및 후속 정정·재검수 보고, 최종 SPEC004·SPEC000 device·SPEC003 연결을 읽는다. 코디가 커밋한 현재 HEAD를 읽어 exact 결속. 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app HEAD b6c034bf 및 AGENTS·기존세션/모델/실시간은 read-only.

이 단계 편집 허용: profile /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/delivery-request-v7.json 와 chat-wp-report.md 뿐. SPEC/코드/기존JSON·GitHub·DB·commit/push/merge 수정0, 하위위임0. 작업 원장은 GitHub Delivery235이며 새WPmd/새이슈 없음.

기존 delivery-request-v6.json + delivery-v6-approved-result.json 을 근거로 같은 idempotency day/day-app, issue235, contract_version7(L3), 코드PR237/dev 하나·스펙PR921/main·머지는 사용자 마지막, iOS우선·실키/서명사용자 유지. 제목/사람용요약은 최종 기능 위주 간결하게. v6이전사항은 회귀대상으로 보존하되 이번차이=내부채팅 전기능 원형 + DAY병원/활성직원/세션/UUID/seq + 서버HTTP20/SSE/첨부디스크+AzureBlob + 최소기기등록/채팅APNs + 배너·탭배지·채팅진입. 기존 SPEC003 채팅자리만이라는 non-goals/범위와 D2채팅부분 미구현 문장이 v7과 모순되지 않게 기존JSON복사만 하지말고 대조. 알림센터 전체/Android신설/의사상담사호출정책 확장·실서버설정/배포/머지 없음.

target_specs는 변경영향을 정직하게(기존001/003, 신규004, device개정000 포함여부 actual schema/contract 검토), baseline은 fetch된 latest origin/main exactobject, canonical003/004 missing이면 pending 유지. 미머지PR921 reviewedHEAD를 implementation 근거로 결속하되 mainready로 위조 안함/선머지 요구 없음(사용자 지시 우선). 실제사용자승인 원문=「응 일단 채팅 기능 스펙부터 앱 구현 까지 진행하자」「아 백엔드 저쪽은 일단 끝나서 우리가 가면 돼!」「채팅 상대는 같은 병원 활성 직원」. 코디 해석/구현상세와 사용자결정 구분. plan_digest는 harness결과가 계산, 임의생성0.

실행계획은 구체화: backend/API+DTO/schema/service/query/models+증분migration+Redis/SSE+blob/APNs/device/task+설정예시/compose전달/의존성·검증문서의 꼭필요한 경계, app/UI+data/state+native/pickers/video+기존shell/push/session격리+tests 및 manifest/pods 필수변경. frontend웹/원장호출상태/EMR/KOS/다른패키지 변경 금지. backend와mobile 분담은 review된같은WP 뒤 disjointpaths 병렬가능, 검수각각후통합. 프로토원형시각증거 phone/iPad 필수. 새로선택SDK/외부API는 공식최신문서검증, 버전은실제lock.

review surface/AC: 같은병원 활성직원/다른병원정보유출0, 탈퇴·재초대 from_seq·기존/새첨부열람경계, room/seq/clientId 동시성·삭제뒤멱등성·전달부분실패, tombstone 포함 since복구·SSE 세션중간무효·다중process/기기·stale응답, 선택/카메라/사진/동영상/Range·MIME/용량·본문유출/임시파일정리, 읽음/음소거/숨기기/배지·배너중복, 세션환경·병원교체메모리/캐시·device oldPUT/DELETE races, APNs tokennamespace/암호화/idempotency/전송재시도·실키없음정직표기, 기존시술현황198/세션/native 회귀. 모든 단위mock로만 완료말고 로컬스크래치PG·Redis/API E2E 필요(사용자 업무DB/실계정 상태변경X). 기존 key/settings미설정은코드완료와실기기pending 명확구분, 로컬채팅API 통합 pending을무조건완료로우회0.

코드전기준 chat-code-baseline.md 참조: 앱tree migrationhead0005, 옆 종료tree migration0006_event_log_visit_type 존재/미머지. 전체옆branch 강제merge나dev선머지0. 최소 의존안은 옆migration0006 파일만 동일byte/hash로 의존 source명시하여 가져오고 신규0007을잇는것(모델호환검토/독립리뷰/관련검증), 또는 동등하게 한head보장하는 검토된대안. 원천0006수정·미확인down_revision·두head상태방치금지. rollback은새기능/설정만 안전하게끄는방법, schema데이터삭제나demoemail비우기같은prod fail-open0.

JSON schema validator/모델 validation 각1회, 오류0. 실제 CLI apply/issue쓰기/승인receipt는 코디 몫. 보고서에 code_surface phases verification rollback open_questions + 인수조건·spec매핑과schema수치, 기본값구현확인vs사용자필수결정구분. 사용자의새정책없는기술선택 때문에무의미한재승인 만들지않음. 최신preable exactID/handle, checkpoint/completion전check+ack, worker_done단한번 outcome/reportpath, 후idle.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_3333de45-6039-44ec-b7af-76bbd3afdb0c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
