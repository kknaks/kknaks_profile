# [writer] WORK002 검수 최소정정 한회
## 1. 역할/입력
기존 strong-hajin-work-v2-wp-brief.md 역할/규칙/SSOT 유지. review-v2-work-report.md F1~5/N1~6만 수정. SPEC/코드변경 없음. 오늘 구현목표, 전수재조사 금지.
## 2. 지시
F1 derived 생성/전투영/타입/검증 추가. SPEC 실제 Data contract의 reply/status_note 등 누락하지 않고 생산단계 명시.
F2 open→done 명시구현+양쪽경로회귀, 요청직접완료거부 보존. A9 우회/사용자판정요청 제거.
F3 내부 COMPLETION_SUBMITTED 보존, 외부 state done/derived awaiting_review 투영. '승인판단행 존재'는 아무 과거승인 하나면 충분하다는 뜻이 아님: 현재 완료회차 및 재개/보완 후 유효성 포함하여 승인없음을 확실히 판정. FE소비동시정합. 투영타입묶음만 읽어 권한/완결 추론금지.
F4 현재 SPEC 명시범위로 WORK 정렬(회의 일정은 기술가능 기록, SPEC환류 없는 조용한 구현추가금지). 원문디자인 요구는 후속계약으로 남겨 전체완료라고 숨기지 않음.
F5 재현가능 migration 파일/중복조회/기존인덱스결손격리재현/재적용/INVALID회복. 리뷰제안의 concurrent/nonconcurrent DDL을 하나파일에서 무조건 둘다실행하는 함정은 피할 것: 명확한 분리파일이나 안전한 실행모드로 단일기술안. 실제운영적용과 격리검증 구분. 새 migration이 이미 있다고 쓰지 않음.
N1~6 함께정정. SPEC U번호 자체변경금지, WP에서 SPEC UX-U1과 BASE U1을 구분라벨로 참조. N7 index는 코디.
OQ203 사용자답대기이므로 기존 submit허용은 '새선택확정'이 아닌 현행보존. 조건별검증계획 남기고 답전 정책확정표시 금지. OQ206 명확한 좁은 의존, seed를 없애는 방식으로 실제경로결함 숨기지 말 것: 미답경로/미검증 명시. 미정외 독립범위 계획완성.
코디 baseline82파일 sha 일치확인. W1검증증거재사용으로 Phase0 전량4종 반복제거, 환경/PG관측 필요검증만. v2검증은 반드시 새실행.
## 3. allowed_paths
para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md
orchestration/work/strong-hajin-work/v2-work-fix1-report.md
## 4. 보고
F1~5/N1~6 변경전후 짧게, 전부TODO유지. 불필요보고장문없음. 완료후 코디최소검증→검수자 최종diff확인으로 바로 구현발주 예정.
## 5. 금지
코드/DB/테스트/빌드/커밋/push/PR/index/log/원문/디자인/SPEC변경 없음.
## 6. 검증
문구/phase/추적정합만. 실행0.
## 7. 범위
오직 지적수정. 새기능제안/재조사없음.
## 8. 완료
2채널 완료후 idle. 현재 코디 term9de live.
## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_9de388d5-58b1-4bbe-8864-5e930def648b --from term_0ca0ef16-4e59-4fc9-8799-1fb4bf84b25a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_9de388d5-58b1-4bbe-8864-5e930def648b --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
