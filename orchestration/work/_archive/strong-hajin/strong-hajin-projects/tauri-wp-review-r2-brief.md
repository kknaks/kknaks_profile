# [reviewer] WORK-006 수정1 재검수

기존 tauri-wp-review-brief.md의 역할·읽기전용·보고 규약 유지. 작업 루트 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin. 기존 검수와 수정으로 인한 직접 회귀만 확인한다. 새 기능/취향을 요구하지 않는다.

## 1. 입력
- orchestration/work/strong-hajin-projects/review-tauri-wp-report.md
- 같은 디렉토리 tauri-wp-fix1-brief.md (코디 판단 우선), tauri-wp-fix1-report.md
- para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md 수정본
- SPEC-006 v0.2.3, DEC-005 D01~09, orchestration/runbook.md

## 2. 확인
1. F1~3·W1~8·R6 전건 처분. 기존 워크트리 유지, 운영 구현 실행 주체/파일/완료 기준, origin→최종빌드→검증→해시 동일판 발행의 도달 가능성과 의존 공백/순환0.
2. Phase6a·6b와 8·9 책임 일치. 6b 서버 이미지와 8/9 데스크톱 설치파일을 '같은 아티팩트'라고 뭉개지 않았는지 — 서버/웹 버전과 셸 호환 조합을 기록해야 하는 곳과 설치파일 해시 일치가 필요한 곳 구분.
3. W3: fixture 인용보다 제품판 재측정을 강화한 이유 타당성. AC-T27 하나 인용하는 가정(서버·웹 변경 없음)이 6b 운영 프로파일 정리 후에도 유효한가. 최종판에서 달라진 부분을 재검증하는 규칙인지.
4. W8 두 녹음 경로 각각 포맷/서버 수용. 브라우저 경로만 실패한 경우도 지원 요구에 맞게 보완/gate되는지, 회의 MIME만 성공하면 무조건 진행하는 틈 없는지.
5. 사용자 gate 축소는 코디 지시다. FE 서빙/ARM 이미지의 내부 구현 선택을 다시 사용자 결정으로 올리지 않는다. 인증 권한 완화·보호 수준 하향만 조건부 결정. 기존 보호와 권한 의미를 보존하는 계획인지.
6. Windows 장비 없음은 해당 축 보류. '설계·구현·로컬 검증 어느 미결에도 안 막힌다' 같은 요약이 Windows 실측 필요성과 충돌하면 한정. Phase 수는 실제10(1~5,6a,6b,7,8,9), 번호9와 혼동은 경미 문구로 취급.
7. P5 인프라 워커 설정을 구현 전에 준비하는 담당/위치가 계획에 있는지. 이번 문서 단계에서 실제 config 변경이 없어도 FAIL 아님.
8. AC43/실측15/DEC9·I1~8 보존 및 수정으로 생긴 회귀만 검증. 미수행 상태 유지.

## 3. 산출물 / 제한
orchestration/work/strong-hajin-projects/review-tauri-wp-r2-report.md 하나만 신규. 다른 파일 전부 read-only. 코드/테스트/빌드/실측/원격변경/서버/커밋/push/PR/추가워커 금지. 문서 자체 정합 검증 가능. 비밀값 미열람.

## 4. 완료
PASS/WARN/FAIL 및 건수, 기존 지적 전건 닫힘 여부/근거, 직접 회귀는 정확한 위치·최소 수정, 승인저지 구분. 기존 코디 판단과 다르면 이유를 적되 이미 결정된 구현 선택을 이유 없이 재개방하지 않는다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe --from term_6f15ca95-9228-48e3-974d-4a867a426d6b \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
