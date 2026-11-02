# [writer] Strong Hajin Tauri 래퍼 — 적용 조사에서 SPEC-006까지

너는 Claude 문서 워커다. 이전 세션 맥락은 없다. 현재 코디 워크트리에서 아래 허용 문서만 작성한다. 같은 트리의 다른 코디가 프로젝트 화면을 진행 중이므로 기존 변경과 기존 _RESUME 본문은 건드리지 않는다.
역할: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/role.md 및 같은 폴더 rules.md·skills.md·tools.md·workflow.md.
작업 워크트리: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin. 커밋·push·PR은 코디 소유.

## 1. SSOT — 먼저 읽을 것

- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/para.md · para/projects/project.md
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/10-decision/decision-005-tauri-wrapper.md — 사용자 확정 방향
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/research-task-management-tauri.md — 앞 조사. 기술적 단정은 코드·공식 문서로 재확인
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/templates/projects/20-spec/spec.md — 스펙 양식
- 참조 코드: /Users/kknaks/git/toy_pr2/task_management/AGENTS.md
- 참조 Tauri: /Users/kknaks/git/toy_pr2/task_management/app/front/src-tauri/tauri.conf.json · Cargo.toml · src/lib.rs · capabilities/default.json · Info.plist · Entitlements.plist
- 참조 프론트: /Users/kknaks/git/toy_pr2/task_management/app/front/README.md · package.json · src/lib/auth/tokenStore.ts · src/features/meetings/hooks/audioCapture.ts · useMeetingStream.ts
- 참조 문서: /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/task-management/40-architecture/system/README.md 및 관련 meeting spec
- 적용 코드: /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects/AGENTS.md · frontend/src/lib/api.ts · frontend/src/features/meetings/stream.ts · microphone.ts · backend/src/ax_workspace/entrypoints/http.py · http_auth.py · bootstrap/settings.py · delivery/
- 적용 코드가 미커밋 작업 중임을 감안하고 기준 HEAD·조회 시각을 리포트에 기록.
- 기대는 개념: 해당 없음. 제품 결정과 조사 사실을 구분.

## 2. 배경 / 사용자 승인 범위

사용자: “클로드로 발주 할거고 참고할 tauri 위치 까지 알려줘서 발주 하자. 스펙까지 한번에 갈거야”.
조사 보완 → SPEC 작성 → 별도 리뷰어 검수 → 수정까지 이번 문서 단계다. 구현 계획(WP)·제품 코드 구현은 아직 범위 밖.
이미 확정: 배포 HTTPS 웹을 Tauri 창에서 여는 래퍼, 같은 origin의 웹/API와 세션 쿠키 유지(키체인/Bearer 전환 안 함), 녹음 중 자동 절전 방지, 화면 꺼짐 허용, 수동 잠자기·덮개 닫기는 사용자 의도, OS 알림 시스템은 추후, Tauri 설치파일 빌드 구성 계승 및 지속 개발·배포 문서화.
참조의 FE 번들 동봉 방식을 그대로 복사하면 안 된다. 쿠키를 원천적으로 불가능하다고 쓰지 않는다. 서명·업데이트·CI가 이미 있다는 주장도 하지 않는다.

## 3. 계약

SPEC-006은 외부 계약: 사용자 흐름·웹/셸 인터페이스·상태·에러·권한·인수조건. 조사 파일에는 코드 변경 지점·공식 문서 근거·대안·미결을 둔다.
확정된 결정을 뒤집지 않는다. 기술적 세부는 근거를 갖고 제안하되 사용자 미정 항목을 확정이라고 쓰지 않는다. OQ-T01~06은 이미 있는 근거로 해소할 수 있는 것과 사용자 판단이 필요한 것을 가른다. OS·도메인·배포 채널·서명 신원 등은 발명하지 않는다. 미결 때문에 전체 작성을 멈추지 말고 해당 계약만 명시적으로 gate하고 나머지는 완성한다.

## 4. 핵심 확인

1. production 프로파일의 API 등록·인증 경로: development 서버를 운영 대안으로 슬쩍 승인하지 말 것.
2. 원격 HTTPS 웹 → 최소 Tauri 커맨드 연결: capability remote origin allowlist, 웹브라우저 폴백, 외부 링크·탐색·웹 갱신/앱 버전 호환 경계. 범용 shell 권한 금지.
3. 녹음 상태와 절전 방지 수명: 시작·재개 성공 시점, 일시정지·종료·실패·로그아웃·화면 이동·창 닫기·프로세스 종료, 중복 acquire/release, 수동 절전 후 복귀. 지금 제품의 상태와 맞춰라. 화면 꺼짐과 시스템 잠자기를 구분.
4. 각 OS의 idle sleep 방지와 명시적 sleep 차이는 공식 문서 근거로 검증. 실제 녹음·마이크 포맷·권한은 실측 전까지 보장이라고 쓰지 말 것.
5. 쿠키 HttpOnly/Secure/SameSite·세션 만료·WS·업로드·CSRF 경계, 로그인 유지 미결. 키체인으로 회귀하지 말 것.
6. 설치파일과 웹 서버는 별도 배포. 앱 식별자 분리, 설치/재설치/업데이트 호환, 릴리즈 검증 기준. 아직 없는 배포 URL/서명/자동업데이트는 미결로.
7. 알림은 후속 기능 경계만. 알림 이벤트·푸시·트레이 상주를 이번 구현 약속으로 확대하지 말 것. 시스템 오디오 캡처도 범위 밖.

## 5. allowed_paths

- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/20-spec/spec-006-tauri-wrapper.md (신규)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-implementation-research.md (신규 적용 조사)
- /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-projects/tauri-spec-writer-report.md (완료 리포트)
다른 파일은 전부 읽기 전용. DEC 수정 제안과 index/log 갱신안은 리포트로 코디에게 전달한다.

## 6. 작업 순서

1. 위 경로와 관련 코드 읽기. 조사 전체를 반복하지 말고 설계에 필요한 빈칸을 보완한다.
2. 공식 Tauri·Apple·Microsoft·웹 표준 문서로 플랫폼 계약 확인. 근거 URL과 확인일·로컬 파일:줄을 적용 조사에 남긴다.
3. SPEC-006 status:draft로 작성. DEC-005를 frontmatter links.decisions에 연결. works:[] 유지. 템플릿 빈칸 없이, 해당 없는 절은 이유를 적는다. 숫자·상태·명령 인터페이스가 모호하면 OQ와 구현 차단 범위를 명시.
4. 사용자 눈에 보이는 시나리오·에러/경계 matrix·수명주기·인수조건을 연결. 실제 테스트 수행 결과처럼 적지 않는다.
5. 자기 점검 후 리포트. 별도 리뷰어는 코디가 발주한다. 네가 워커를 추가 발주하지 마라.

## 7. 범위 제약

제품 코드·다른 문서 수정, 설치·빌드·테스트·서버 기동·중단·커밋·push·PR 금지. 비밀값 읽기 금지. 다른 프로젝트 워커/터미널/태스크 상태에 손대지 말 것.

## 8. 검증

인수조건에 식별자 부여. DEC-005 D-01~06 추적, 기존 계약과 차이, 미결별 차단 범위, 아직 실측하지 않은 항목을 분리한다. 보고서에 생성 문서·주요 판단·OQ·검수 포인트를 적는다. 코드 구현 완료나 배포 완료를 주장하지 않는다.

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
