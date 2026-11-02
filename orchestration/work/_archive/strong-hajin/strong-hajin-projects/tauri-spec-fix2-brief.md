# [writer] SPEC-006 수정 2 — R2 경계 조건 닫기

기존 역할·금지사항 유지. 새 dispatch로 보고한다. 이번은 구조 재설계가 아니라 현재 네이티브 소유 구조의 계약 정합 수정이다.

## 1. 읽을 것
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-tauri-spec-r2-report.md 전체
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-fix1-brief.md (코디 판단 A~H 유지)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-fix1-report.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md
- DEC-005 · 적용 조사 · 최초 writer 브리프의 역할/프로젝트/템플릿 규약

## 2. 목적
1차 FAIL5/WARN10은 닫혔다. 이를 다시 논의하지 않는다. R2-F1~F4, R2-W1~W7만 최소 변경으로 닫아라. TTL/renew/참조계수를 되살리지 않는다. 커맨드는 기존 넷으로 유지 가능하며 임의 기능 확대 금지.

## 3. 수정 계약 — 코디 판단
- F1: AC-T17을 '셸이 앱내 전환/same-document 사건만으로 자동 해제하지 않음'으로 수정. 실제 녹음 종료 시 웹 cleanup 해제는 L-10대로 유지. L/M/시나리오 전수 동기화.
- F2: 동일 session acquire의 멱등성은 점유 중복 방지이지 OS 재시도 금지가 아니다. 상태 degraded이거나 wake 후 재확보가 필요하면 동일 키로 재무장할 수 있다. 가시성 복귀/시스템 wake 등 사건 기반 재요청과 성공/실패 UI 갱신을 계약화. 신호가 오지 않았다고 해제하지 않는다. native가 감지하지 못하는 OS 손실을 실시간 감지한다고 보장하지 말고 확인 가능한 사건·재요청 결과로만 상태 갱신. U-3에 최신 확인 상태와 경고 해제 조건을 적어라. OS 성공을 보장하는 대신 실패 시 기존 degraded 정책을 적용. 상태도/AC와 일치.
- F3: 닫기/종료 요청이 취소되면 녹음과 점유 유지. 실제 종료가 확정/완료되는 경계에서만 정리. 차단·취소된 네비게이션과 문서 교체를 구분. 비교표의 '녹음 중 스스로 풀림 없음'은 '갱신 실패로 해제하지 않음'으로 한정. 취소된 닫기·외부 이동 AC 포함.
- F4/W1: 세션 키는 녹음 회차마다 새 값, 재사용 금지. 종료된 녹음의 늦은 acquire가 점유를 남기지 않는 계약. 마이크 획득 전에 끝난 경우뿐 아니라 IPC acquire가 진행 중에 cleanup된 경우도 포함: 취소/직렬화/보상 release 등 구현 방법은 WP 몫이나 '종료 후 늦은 완료에도 최종 잔존 0'을 요구. 과도한 영구 tombstone 구조를 SPEC에서 강제하지 않는다. 문서 교체 뒤 이전 요청이 새 문서 점유를 만들지 않는 경계도 함께 점검.
- W2: shell 없음(일반 웹)과 shell은 있으나 IPC 실패 분리. acquire/info 실패는 녹음 계속+U-3. 단 release 실패를 'degraded 녹음 계속'으로 뭉개지 말 것: 이미 종료한 녹음을 다시 켜지 않고 정리 실패·잔존 가능성을 드러내며 문서/창 lifecycle 정리는 유지. 네이티브 없는 브라우저는 기존처럼 조용히 동작.
- W3: release 응답은 잔여 점유와 실제 확인된 OS 상태를 반영(on/degraded/off). 본문/표/상태도 일치.
- W4: M-1의 IPC 의존 AC 목록 누락 보완.
- W5: QA 측정 기준은 코디 기본값으로 확정: 자동 절전 대기시간 T가 실제로 설정된 테스트 환경에서 max(3T, 30분) 이상. 제품 녹음 시간 제한이 아니라 검증 하한이다. 사용자 재승인 사항으로 만들지 말 것. 웹 스로틀 안전 배수라는 뜻도 아님.
- W6: 되묻기에는 사용자가 답한다. 웹/셸 두 확인창이 중복되지 않는 외부 계약, 실제 어느 층이 맡는지는 실측과 WP가 정함.
- W7: Safari 18.4 배포 대상에 Sonoma/Ventura도 있다는 공식 사실 반영. 'Safari 설치됨 = 해당 WKWebView 버전·정확한 MIME 지원 보장'으로 확대하지 말 것. 대상 웹뷰 실제 캡처/서버 수용은 실측 유지.

## 4. 범위
수정 허용 파일:
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-implementation-research.md (필요한 정정만)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-fix2-report.md (신규)
DEC/index/log/이전 리포트 수정 금지. 코드·빌드·설치·서버·테스트·커밋·push·PR·추가워커 금지.

## 5. 검증
F/W 조치표·상태도/인터페이스/AC/OQ 서로 대조. 정상·취소·실패·재시도·늦은 완료 시나리오를 간단히 펼쳐 스스로 확인. status draft 유지, patch 버전 증가. 새로운 제품 결정을 질문으로 늘리지 말고 범위 내 기술적 공백을 닫는다. 남는 실측/사용자 결정과 문서 오류를 분리.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --from term_21131adc-c6b5-4082-834e-305628bb9de6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
