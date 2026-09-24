# [reviewer] WORK-006 독립 계획 검수

너는 Claude read-only 리뷰어다. 이전 맥락은 없다. 작업 루트는 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin. 상대경로는 여기 기준.

## 1. 읽을 것
- AGENTS.md, orchestration/runbook.md, para/para.md, para/projects/project.md, orchestration/roles/strong-hajin/reviewer/ 역할 파일
- para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md (검수 대상)
- para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md v0.2.3 및 10-decision/decision-005-tauri-wrapper.md D-01~09
- orchestration/work/strong-hajin-projects/tauri-wp-writer-brief.md, tauri-wp-writer-report.md (R-1~7), tauri-deployment-decisions.md, tauri-spec-finalization.md
- templates/projects/30-work/work.md
- 필요 시 적용 코드 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects (AGENTS.md부터, read-only), 참조 /Users/kknaks/git/toy_pr2/task_management/app/front/src-tauri/, 인프라 /Users/kknaks/git/harness_works/k8s_infra_mac (비밀 제외).

## 2. 검수 목적
실측→구현→Mac Studio 운영→macOS·Windows 설치파일 Release까지 실행 가능한 WP인지 본다. 문서만 검수하며 실측은 미수행 상태가 맞다. SPEC 구조 자체는 이미 검수 완료; 새 기능·취향을 요구하지 않는다.

## 3. 집중 기준
- AC43·실측15·DEC9 실제 전수 추적 및 Phase 배정의 타당성. 행 수만 맞고 검증이 불가능한 것은 아닌지.
- fixture가 제품 셸 구현 전에 측정을 가능하게 하는가. Phase2 진행/보완/중단의 정의·필수 증거·Windows 장비 부재 시 분기. 최소 OS 미정의 개발기기 실측과 최종 지원판 인증 구분.
- TTL/renew 폐기·네이티브 수명·완료 사건·경합·실패/재무장 기존 계약 보존. M-2b 세션 만료 계측이 실제 코드/저장소에서 가능한가.
- 운영 프로파일·ARM64 이미지·정적 서빙·same-origin WS·서명/공증·빌드 러너·GitHub Releases·프로필 60-release 연결·rollback까지 빠진 실행 책임은 없는가.
- 확정 요구를 다시 사용자 질문으로 돌리지 않는가. 사용자는 기존 Mac Studio 인프라 경로까지 지정했다. 배포레포 선택 등 재확인이 꼭 필요한 이유가 있는지, 구현 수단(이미지/서빙)이 불필요한 사용자 gate로 부풀었는지 판단. 사용자 미정 도메인·지원버전·서명 신원은 발명 금지.
- 코디 우려1: Meta의 '같은 코드 레포이므로 워크트리를 따로 잡는다'는 런북의 동일 작업 동일 워크트리 규칙과 충돌 가능. 실제 파일 충돌 근거 없이 새 워크트리 요구 금지. WORK-005와 코드가 안 겹친다는 말도 App.tsx 접점과 비교.
- 코디 우려2: 보고서는 Phase6를 문서 구성안만으로 설명한다. Phase8 운영 최종 전에 실제 차트/이미지/서빙/프로파일 구현·배포 실행 Phase가 존재하는지. 계획이 필요한 일을 '후속 별도'로 밀어 공백을 만드는지.
- 코디 우려3: Windows 지원은 확정. 장비 없을 때 검증 보류는 가능하지만 'macOS만 낸다'는 출시 범위 변경을 임의로 승인한 것은 아닌지.
- 기술적 모순·계약 위반·누락·도달 불가만 FAIL. 증거와 정확한 위치, 최소 수정안. 단순 문구는 WARN. 실측 미수행/미선택 구현 수단 자체는 FAIL 아님.

## 4. 산출물 / allowed_paths
orchestration/work/strong-hajin-projects/review-tauri-wp-report.md 하나만 신규 작성. 나머지 파일 전부 read-only. 제품·SPEC·WP·index·log·기존 보고서 수정 금지.

## 5. 범위 제약
코드/빌드/테스트/서버/실측/설치/원격변경/커밋/push/PR/추가워커 금지. 필요한 파일 읽기·문서 정합 스크립트 가능. 비밀값 미열람.

## 6. 완료 기준
첫 줄 PASS/WARN/FAIL 및 건수. 각 지적은 위치·근거·영향·최소 수정. 승인저지/비저지 구분. 원 작성자 R1~7과 코디 우려1~3에 답. 남은 사용자 결정은 진짜 결정만, 구현 선택과 구분. 코드 기준 HEAD 확인. 실제 검증을 수행한 것으로 쓰지 않는다.

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
