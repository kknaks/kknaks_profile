# [reviewer] SPEC-006 v0.2.1 최종 문서 재검수 — R2 수정 범위

Claude 독립 read-only 검수. 기존 reviewer 역할·템플릿·프로젝트 규약 유지. 이전 판단을 반복하거나 검수마다 선호 기능을 추가하지 않는다.

## 1. 읽을 것
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-tauri-spec-r2-report.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-fix2-brief.md (코디 판단)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-fix2-report.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md v0.2.1
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-implementation-research.md 정정 부분
- DEC-005 및 최초 검수 브리프 규약

## 2. 검수 목적
R2-F1~F4/W1~W7 처분을 확인하고 수정으로 생긴 직접 회귀만 본다. 이미 통과한 전체 조사/사실/구조 검증을 다시 수행하지 않는다. 실측/미정 OS/배포주소/사용자 선택은 문서 오류와 구분한다.

## 3. 집중 기준
- AC-T17과 L-10 일치. native가 직접 해제하지 않음과 웹이 녹음 끝내며 해제함 분리.
- degraded 재무장, UI 최신 확인 상태, 실제 실패 시 계속 녹음+경고. OS 성공을 무조건 보장하지 않을 것.
- 창 닫기 취소·막힌 이동에서 점유 유지, 실제 문서 교체/종료 정리. 동일 문서 URL변경 구분.
- 늦은 acquire에 대한 최종 잔존0, 문서 세대경계, 키 유일성/재사용 금지. release IPC 실패의 잔존 가능성 예외와 정상 완료 AC가 혼동되지 않음.
- E-14a/b/c 구분, 종료한 녹음이 되살아나지 않음, native 없음 브라우저 폴백.
- 관찰 하한 max(3T,30분), WebKit 배포OS 사실과 실제 WKWebView 지원 실측 구분.
- 과도한 FAIL은 금지: 구현 내부 기법이 미선택이거나 실측이 남아 있음 자체는 FAIL 아님. 모순·도달 불가능 AC·명시 요구 위반일 때만 FAIL. 사소한 표 목록 중복/표현은 WARN으로 위치와 교체 문장을 제시.

## 4. 산출물과 권한
/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/review-tauri-spec-r3-report.md 하나만 작성. 제품·이전 보고서 0줄 수정. 코드/빌드/서버/테스트/프로토타입/커밋/push/PR/추가워커 금지.

## 5. 완료 기준
첫 줄 PASS/WARN/FAIL 및 건수. R2 각 항목 닫힘 여부와 근거, 새 직접 회귀가 있으면 정확한 문장·최소 수정안. 문서 품질 통과와 후속 사용자 결정/구현 실측 목록을 분리. 요약에서 구조는 닫혔는지 명확히 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --from term_d3ba7d04-3add-4968-b1bc-eaebc7692737 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2ae8654e-00e2-4649-ab7c-cb3b5e02b995 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
