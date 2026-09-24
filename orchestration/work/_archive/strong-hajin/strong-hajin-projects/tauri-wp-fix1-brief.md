# [writer] WORK-006 검수 수정 1

기존 writer 역할·규약 유지. 맥락이 없으면 tauri-wp-writer-brief.md부터 읽어라. 이번 지시가 수정 범위의 정본이다. 작업 루트 /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin.

## 1. 입력
- orchestration/work/strong-hajin-projects/review-tauri-wp-report.md (F1~3, W1~8, R6 보강)
- tauri-wp-writer-report.md 및 tauri-deployment-decisions.md (같은 work 디렉토리)
- para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md
- DEC-005 D01~09, SPEC-006 v0.2.3, orchestration/runbook.md

## 2. 목적
계약 I1~8·AC43·실측15·DEC9와 계측 우선 구조 유지. 검수의 경계·소유·순서 오류만 닫는다. 계획 문서만 수정하고 실제 코드·실측·배포는 하지 않는다.

## 3. 코디 수정 판단
- F1 수용. 기존 코드 워크트리 /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects 와 그 브랜치를 이어 쓴다. 새로운 WORK 번호를 이유로 새 워크트리 만들지 않는다. App.tsx·labels.ts 접점 명시, 현재 HEAD/미머지 사실은 읽기 전용 재확인하되 미래에도 그 상태라고 고정하지 않는다.
- F2 권장(a) 수용. Phase6을 결정/구성 설계와 실제 구현/배포 실행으로 분리. 차트·Application·values·ARM 이미지·FE 서빙·운영 프로파일 구현·배포 실행의 주체/파일/선행/검증/rollback을 계획 안에 둔다. 외부 레포 코딩은 워커, 코디는 발주·검증. 사용자에게 직접 명령 실행을 떠넘기지 않는다. 실제 운영 변경은 구체 산출물이 준비된 뒤 세션의 승인 범위에 따라 진행하는 경계를 명시. 이번 문서 워커의 실행 금지를 미래 구현 Phase 전체 금지로 복사하지 않는다.
- F3 수용. 개발 fixture 설치검증과 운영 origin을 넣은 최종 빌드·설치검증·Release 발행을 구분. 운영 origin 설정→최종 빌드→그 아티팩트 검증→발행 순서. Phase8이 발행판 설정을 사후 수정하지 않게 의존을 재정리. 번호 유지/하위 단계/재번호는 최소 명확한 방식으로 선택. 추적표/게이트/Done Criteria 함께 갱신.
- W1·W2·W4·W7·W8 수용. HTTPS IPC fixture 명시. 회의 라이브 고정 MIME과 브라우저 후보 경로를 나눠 서버 수용까지 각각 검증. 클러스터10/레포9 구분.
- W3 취지는 수용하되 'fixture 기록 인용만으로 제품 AC 완료'를 일반화하지 않는다. 통합 배선에 영향받는 쿠키·만료·닫기 확인도 제품판 검증이 필요한지 판단해 명시. 실측 ID는 15개 그대로, 제품 재측정은 같은 ID의 증거 단계로 구분.
- W5: Windows 장비 없으면 그 축 보류. 사용자 승인 없이 macOS 단독 출시를 기본 행동으로 쓰지 않는다. D07 양쪽 지원 유지.
- W6: FE 서빙은 코디 기본안 ingress 경로 분기(정적 FE 컨테이너+/api·WS)로 선택하고 사용자 gate 해제. 사용자가 지정한 인프라 저장소 활용을 기본 제안으로 적되 회사 org에 새 제품 구성을 발행하는 범위 확인은 실제 변경 전 쟁점으로 남겨라. 계획 작성·로컬 준비 전체를 막지 않는다.
- 검수가 구현 선택을 과하게 사용자 결정으로 분류한 부분은 그대로 복사하지 마라. ARM64 이미지 작성 자체는 운영 목표에 필요한 구현 선택이다. 보호 수준을 낮추는 결정은 별개이므로 현재 보호 요구 여부/호환성 확인 뒤 기존 보호 요구를 훼손하지 않는 안을 기본으로 계획한다. '이미지 하나 늘어 비용'만으로 사용자 gate를 만들지 않는다.
- 운영 프로파일의 내부 구현 수단과 인증 정책 변경을 분리. 쿠키 유지·기존 권한 유지·HTTPS 운영을 달성하는 내부 정리는 계획 가능하다. 권한 완화나 인증 방식 도입 등 새 계약은 별도 결정으로 gate하되, development 프로파일로 운영하는 우회는 금지. 기술 선택마다 사용자 확인을 강요하지 않는다.
- R6 데이터 rollback 보강: PVC/녹음원본/자료/DB 파괴를 rollback 절차로 두지 말고 보존·백업·복구 증거 구분.

## 4. allowed_paths
- para/projects/summer-star/strong-hajin/30-work/work-006-tauri-wrapper.md 수정
- orchestration/work/strong-hajin-projects/tauri-wp-fix1-report.md 신규
기존 리포트·SPEC·DEC·index·log·코드·인프라는 읽기 전용. 커밋/push/PR/설치/빌드/실측/테스트/서버변경/추가발주 금지.

## 5. 완료 기준
F1~3·W1~8 항목별 처분표(다르게 처리한 것은 이유), R6, AC43/실측15/DEC9 전수, 실행 선행 공백·순환0, 최종 아티팩트와 검증 대상 일치, YAML/형식/미수행 상태 검증. 각 Phase 주체·입출력·파일·증거·차단 범위 갱신. 추가 사용자 질문을 줄인 근거와 진짜 남은 결정만 리포트에 정리. 독립 재검수는 코디가 발주한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe --from term_3905b395-8c86-4e2f-82d0-cfa590d8a74f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1f3a40c9-5b3d-4196-a44d-bb65907d59fe --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
