# [reviewer_doc] DAY 앱 UI 교정 스펙 독립 검수

너는 독립 문서 리뷰어다. 앞 맥락이 없다고 보고 이 브리프를 따른다. 역할 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/reviewer/의 role.md·rules.md·skills.md·tools.md·workflow.md 및 mediness AGENTS.md/라우팅을 읽는다.

## 1. SSOT
스펙 트리 /Users/kknaks/orca/workspaces/mediness-mediness/day-app-spec, 기존 PR921 미머지. 제품 products/day/README.md·20-spec.md·30-work.md·SPEC003·SPEC002. 사용자 교정 계약 전체는 /Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/ui-spec-brief.md §3의 13항목과 같은 폴더 _RESUME.md §2 최신 사용자 지시. planner-ui-spec-report.md도 읽되 독립적으로 diff/원천을 대조한다. 프로토 /Users/kknaks/git/toy_pr2/cc-prototype/procedure/app, DAY 코드 /Users/kknaks/orca/workspaces/CENTURION_DAY/day-app 및 /Users/kknaks/git/CENTURION_DAY는 read-only. research-prototype-toasts.md 참조.

## 2. 이번 범위
사용자 「백엔드/웹프론트 작업 중이라 일단 스펙까지만」에 따른 SPEC 교정만 검수. WP/이슈/코드/merge 단계로 넘어가지 않는다. 개념 해당없음. 구현완료/서버완료를 추정하지 않는다.

## 3. 계약 검수
13항목 전부를 표로 검수. 특히 원본디자인+DAY색, 하단4메뉴/기존인박스 구분, 미정채팅·설정 상세를 범위확대하지 않음, 각탭알림/실제배지의 서버의존, 카드4행, 마취20분초과서버기준, 목록/상세/호출탭원장직접수락·간호대리, 서버권한보존, 시술진행강조/완료아래회색/세로더보기·확인없는취소, 상세→호출시트(안에서체크+원장)·재호출A22불변, 전부완료귀가강조, 기존통역드로어/라운드음성칩, TW zh-Hant·중국어(번체)·고객별초기화/전역덮어쓰기없음, 원천없는번역없음, 성공토스트2.6초/원문/자기조작만/토스트되돌리기없음/실패DAY문구를 확인.
본문·범위제외·표·와이어프레임·시나리오·인수조건·OQ의 옛내용 모순이 남지 않았는지 확인. 데이터/API 없는 칸을 가짜로 채우거나 신규API 발명/서버 규칙 재계산/권한 확대가 없는지. 기존 D1~D3 환경·보안·세션·푸시 계약은 무관변경 없어야 한다. 정책미정은 실제 새 미정만, 사용자확정 TW를 미정으로 돌리지 않음. 다른 국적 매핑을 승인없이 새정책으로 확정하지 않음.

## 4. 산출물
/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-app/review-ui-spec-report.md 한 개만 생성. 스펙/코드 수정금지. PASS/WARN/FAIL, 각지적 파일:줄+원천근거+수정방향, 13개반영표, 남은실제의존. 사소한 표현선호를 결함으로 과장하지 않음.

## 5. 검증
git diff --check, python3 scripts/lint-pipeline.py --strict 한번 실행, products/day ERROR0(타제품무관분리). 수치는 실결과로 보고. 코드테스트/빌드/서버실행 없음.

## 6. 금지
하위워커/내부서브에이전트 금지. 파일수정은 보고서1개뿐. 커밋/push/PR/merge/이슈변경금지. 새의사결정/문구/번역/API 발명금지.

## 7. 완료
live preamble id/핸들/outcome이 옛예시보다 우선. 마지막메일확인후 worker_done 한 번, idle. 리뷰결과는 검수판정이며 수정은 planner에게 돌린다.

## 8. 수락
사용자지시와diff를 독립대조하고 근거있는 결과를 남긴다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_745f364a-e2a0-4b43-982c-820a16e3ab75 --from term_4fc8346e-2c4e-4f56-a8a4-96120c073f8c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_745f364a-e2a0-4b43-982c-820a16e3ab75 --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
