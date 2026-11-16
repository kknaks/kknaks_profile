# [mobile-asc] 정식 DAY App Store Connect 메타데이터·스크린샷 API 등록

작업: 코디의 등록 작업 담당. 앱 소스·backend·env·기존 _RESUME 수정 금지. 사용자 최신 명시 지시 “지금 다 준비하고 api appstore connect에 너가 등록”. 따라서 이번 task는 **ASC 읽기·정식 DAY 메타데이터/버전/이미지 등록 쓰기 허용**. 이전 준비 전용 금지보다 이번 사용자 지시가 우선. 출시/심사 제출은 필수값과 빌드 확인 뒤 판단해야 하므로 이 task에서는 하지 않는다.

## 1. SSOT
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-submission-draft.md (확정 이름 DAY, 부제·설명·키워드는 그 초안으로 등록 가능)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-build-report.md (정식 소스 버전 0.1.0)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/config/projects/day.json apple. credentials 실제 경로 ~/.config/day/apple/credentials.local.json. 키 값·Team ID·Issuer·토큰·계정·연락처 출력/리포트/레포 저장 금지.
- 공식 https://developer.apple.com/documentation/appstoreconnectapi/ 및 uploading-assets-to-app-store-connect 문서. API 기능 불가를 비공식 웹 API로 우회하지 않는다.
- 현재 ASC 조회 캐시 ~/.config/day/apple/asc-current.local.json (로컬 600)에는 DAY와 DAY Dev가 둘 다 있음. **bundleId를 정확히 동등 비교**해 day.medisolveai 선택. 앱 resource id 6833456680. DAY Dev 변경 금지.

## 2. 목표
정식 앱 기존 record에 한국어 메타데이터·0.1.0 버전·한국어 locale·iPhone/iPad screenshots를 API로 등록하고 GET으로 재확인. 빈값/기존값 조회가 먼저. placeholder URL·가짜 심사 연락처는 넣지 않는다. 중복 생성·기존 이미지 삭제 금지.

## 3. 입력
- name DAY · primaryLocale ko · subtitle '병원 직원을 위한 업무 앱'
- description, keywords는 mobile-submission-draft.md의 실제 초안(마크다운 설명은 제거) 그대로. 미출시 예약 기능 광고 없음.
- iOS version 0.1.0(있으면 재사용), releaseType MANUAL(자동 공개 방지)
- category BUSINESS는 현재 비어 있을 때만 설정(기존 값 있으면 유지·보고)
- privacyPolicyUrl/supportUrl/심사 연락처/copyright: 사용자/코디가 확정 값을 주기 전 생성·추정·등록 금지. 기존 유효값 있으면 유지하고 주소만 코디에 보고. 정책 URL은 아직 미정으로 확인됨.
- screenshots: /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1/app/store/0.1.0/screenshots/iphone/ 및 ipad/. mobile screenshot worker가 생성 중. **코디가 시각 검토 후 올려도 된다고 후속 메시지를 줄 때까지 업로드는 대기**. 그동안 버전·문구 등록과 API 준비까지 한다. 실존 인물·개인정보 이미지 업로드 금지.

## 4. allowed_paths
- 레포 쓰기: /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-asc-report.md 1개(상태와 등록 항목·부족값·API 재조회 증거). 사용자 credential 출력 0.
- API 클라이언트/응답 cache는 ~/.config/day/apple/ 아래 작업용 파일(600) 또는 코드 worktree app/build/ 아래 무시 파일. API 응답 전체를 공개 profile 리포트에 복사하지 않는다.
- 원격: 정식 DAY만 등록/수정. 다른 앱·계약·세금·가격·판매지역·테스터·사용자/키·실제 출시·심사 제출 변경 금지.

## 5. 실행
1. 공식 API schema/문서 확인. JWT는 프로세스 안에만 생성. credentials 필드 경로 그대로 읽고 URL/키 유출하지 않음.
2. 앱·버전·appInfo·localization 현황 조회, 기존 값 보존. 한국어 설명/부제/keywords/0.1.0 버전으로 등록 가능한 필드 반영. 이미 동일한 리소스는 건너뜀.
3. GET readback으로 등록된 한국어 문구·버전 확인. 사용자 입력 필요한 필드를 특정.
4. screenshot 표시 타입 enum은 현재 공식 schema로 확인. 이후 승인된 이미지 경로·sha256에 한해 예약 → uploadOperations의 지정 header/method/offset으로 업로드 → MD5 checksum·uploaded=true → 처리 상태 COMPLETE/READY 확인. 업로드 URL에는 ASC bearer 토큰을 추가하지 않음. 이미 업로드한 파일명+checksum이면 중복 금지. HTTP 실패 시 리소스 재조회 후 재시도하여 중복 방지.
5. 연락처·URL 없다고 전체 task를 조기 완료하지 말고 코디에 상태 보고 후 이미지 준비를 기다린다. 심사제출은 안 함.

## 6. 검증
API GET readback 표: 앱/버전/locale/설명/부제/keywords/카테고리/수동출시/이미지 각 기기 수와 처리 상태. 스크린샷 안 올라간 상태를 완료로 표시하지 않는다.

## 7. 제약
커밋·push·PR·앱 빌드·시뮬레이터 조작·서명·바이너리 업로드 금지(후속 별도). metadata 및 screenshot 외 원격 변경 금지. 키/토큰/계정/실명 출력 금지. 실제 API 미지원은 사실로 보고하고 웹 수동 작업에 필요한 정확한 칸을 알려라. 모든 답 한국어.

## 8. 보고
준비 완료/등록 완료/입력 미정/도구 미지원 구분. 앱 소스는 수정하지 않는다. 최소 등록 완료 후 코디에 중간 상태, 이미지 후속 처리까지 마쳐 최종 완료 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_2b709186-d9f1-4811-8538-95544d6d21b8 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "mobile 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 \
  --text "[worker_done] mobile 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_2b709186-d9f1-4811-8538-95544d6d21b8 --text "[질문] mobile: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
