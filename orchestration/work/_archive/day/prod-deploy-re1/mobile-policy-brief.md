# [planner] DAY App Store 자료·스크린샷 기준과 링크 페이지 문안 초안

작업 spec 워크트리 /Users/kknaks/orca/workspaces/mediness-mediness/prod-deploy-re1-spec. 다른 planner가 기존 SPEC 파일 수정 중일 수 있으므로 아래 새 문서 1개만 쓴다. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/roles/day/planner/role.md 및 같은 폴더 규칙 읽기.

## 1. SSOT
- spec 레포 AGENTS.md 및 products/day/ 문서 구조·템플릿
- products/day/40-architecture/mobile-deployment.md · 20-spec/spec-003-mobile-app.md · spec-004-chat.md (읽기만)
- /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-submission-draft.md · mobile-build-report.md(읽기만)
- 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/prod-deploy-re1/app/README.md, app/ios/Runner/Info.plist, backend/day/services/interpret/, chat_storage.py (읽기만)
기대는 개념 없음.

## 2. 사용자 지시
시뮬레이터 재빌드·제출 이미지 제작·App Store Connect API 등록을 지금 실행. 정책/자료 원천은 mediness products/day/, 실제 이미지·가짜 fixture는 비공개 CENTURION_DAY app/store/0.1.0/.
최종 배포 Unlisted. 실제 음성에 개인정보가 포함된다고 단정한 앞 분석은 사용자 지적에 따라 정정. 단순 통역이라는 실제 기능을 설명하고 별도 동의 팝업을 필수로 확정하거나 추가 지시하지 않는다. 개인정보 공유가 실제 있다면 Apple 5.1.2(i) 조건을 확인해야 한다고 조건부로만 기록.

## 3. 확정 경로·현재 상태
서버 코디 확인: /privacy · /support 로그인 없는 공개 GET 라우트 생성 가능. https://day.medisolveai.com/privacy 및 /support. prod는 아직 서버 미배포(502), 페이지 생성은 서버 코디 소유. 앱 담당이 backend 수정 안 함.
연락처는 사용자 질문 대기, 공식 지원 이메일·전화·개인정보 책임자·보관기간/파기 정책·공급자 계약은 미정. 추측 금지. 공개 본문과 검토용 미정 목록을 분리한다.

## 4. allowed_paths
- 새 문서 products/day/60-release/app-store-preparation.md (레포 기존 규약상 다른 stage 경로여야 하면 먼저 확인하고 동일 역할 새 문서 1개만)
- 리포트 /Users/kknaks/orca/workspaces/kknaks_profile/day-fix-web-app/orchestration/work/prod-deploy-re1/mobile-policy-report.md 1개
기존 SPEC, index, log, deployment 문서 수정 금지. 새 issue/Delivery 생성·수정·승인·close 금지. 커밋/push/PR 금지.

## 5. 결과
새 준비 문서 1개에:
1. 제출물 원천/산출물 경로, 버전 묶음, iPhone/iPad 실제 simulator 캡처 기준(가짜 직원/고객만·개인정보 금지·실제 기능·필수 규격·한국어·파일명·hash·앱 버전·승인된 이미지 업로드).
2. 실제 UI+촬영전용 fixture는 허용하되 출시 main에 fixture 삽입 금지, 서버 통합 증거와 구분. 프리뷰와 미출시 기능을 광고하지 않음.
3. 현재 권한 문구 한국어 3개를 원문 그대로 기록. 마이크/갤러리 문구 바꾸지 않음.
4. 앱스토어 설명·부제·키워드·심사 노트/Unlisted 신청 사유 초안. 사실과 미정 구분. 서명·버전은 현재 0.1.0(1), 이후 업로드 build number는 ASC 조회 후 정함.
5. /privacy 공개 페이지 문안 초안: 서비스 목적·직원 계정·세션 Keychain·푸시·채팅/첨부·실시간 음성 통역의 실제 처리 흐름, 광고/분석 SDK 없는 확인 결과. DAY가 기록하지 않는 것과 Soniox 공급자 보관을 혼동하지 말 것. 법적 완성된 정책이라고 단정하지 말고 운영자/보관/파기/위탁 정보의 확정 필요 항목을 별도 표로 둔다. 근거 없는 무보관/무학습/즉시파기/안전보장 약속 금지.
6. /support 공개 페이지 문안 초안: DAY 직원용 앱 안내, 로그인·병원 권한·알림 허용·마이크/사진 권한 안내, 문의에 비밀번호·환자정보 보내지 않기. 실제 연락처는 미정 표 별도. 가짜 이메일/폼 금지.
7. 공개 전 반드시 확정할 누락 값 표와 담당(사용자/서버코디/앱코디). URL이 아직 502인 상태를 제출완료로 적지 않음.

## 6. 검증
스펙과 코드 근거 파일:줄로 문안 대조. 공식 Apple 링크만 필요시 확인. 기존 문서 미변경 확인, 간결한 한국어 초안과 리포트로 마무리. 실무 문안 작성을 위해 법률/공급자 정책을 발명하지 않는다.

## 7. 제약
키/토큰/실명/계정 출력 금지. 다른 코드/문서 수정 금지. 대규모 조사/위원회/추가 워커 금지.

## 8. 완료
완료 리포트에 새 문서 경로, 확정·미정, 공개 페이지를 곧바로 발행할 수 있는지 여부를 명시. 사용자만 정할 값을 질문하기 위해 작업을 중단하지 말고 초안을 완성하여 보고.

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
