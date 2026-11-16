# [tool_dev] 실버 연결 구조 페이지 — 실버 1~8단계 json 을 그대로 읽어 노드 · 엣지를 보여 주기

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
만들 것: `silver-graph.html` 하나(코디가 아티팩트로 게시 · 16MB 이하 · 백엔드 없음) + 페이지 데이터 생성 스크립트 `silver-graph-build.py`(결정론 · 두 번 실행 cmp 같음 · 실버 json 이 바뀌면 다시 돌려 페이지 갱신).
스타일 · 테마 토큰 · 폰트는 `silver-questions.html` 과 같게(라이트 · 다크 · 모바일 폭 16px 여백 · 외부 스크립트는 cdnjs · jsdelivr 만).

## 왜(사용자 10-29)
REST · MCP · 스펙 전에 **실버 데이터가 실제로 어떻게 이어지는지 눈으로** 본다. 스펙 · 골드 규칙의 기준이 된다. 읽기 전용(저장 없음).

## 입력 (지금 판 · 고치지 말 것)
`step1-products.json` · `step2-families.json` · `step3-sites.json` · `step4-techniques.json` · `step5-units.json` · `step6-packages.json` · `step7-concerns.json` · `step8-relations.json` — 각 단계 md · 기록(`para/projects/company/procedure-hub/log/2026-10-2*-silver-step*.md`)으로 칸 뜻 확인. **노드 · 엣지 종류는 파일에서 세라**(목록을 지어내지 말 것 · 파일에 있는 엣지는 전부)

## 화면
1. **구조 지도**(맨 위): 노드 종류(제품 · 계열 · 부위 · 기법 · 단위 시술 · 패키지 · 고민 · 목적 · 확인 조건 · 합병증 · 근거 …)를 상자로, 엣지 종류를 화살표로 · 각각 셈 · 어느 단계 파일에서 왔는지. 상자 누르면 그 종류 목록으로
2. **따라가 보기**: 검색(이름 · 동의어 · id)으로 노드 하나 고르면 이어진 것을 엣지 종류별로 펼침 · 펼친 노드를 눌러 다시 따라감(빵 부스러기 경로 표시) · 양방향(들어오는 · 나가는 엣지). 예시 시작점 버튼: 고민 「기미」 · 「처짐」 · 「피부결」 / 단위 시술 「얼굴 전체 토닝」 / 계열 「성형용 필러」
   - 고민 → 추천 단위 시술 → 기법 · 부위 · 제품 · 패키지 / 시술 ↔ 시술 관계(종류 · 먼저 · 간격 days · 같은 날 · 하위 조건별 값 · 원문 접기) / 피함 / 확인 조건(금기 · 주의 · 확인만) / 합병증 · 위험지대 주의 / 근거
   - **계열 단위 엣지는 「계열에서 상속」으로 따로 보여 줌**(단위 시술에 펼쳐 붙이지 말 것 — 펼치기는 골드 일)
3. **표시 색**: 충돌 · 조건부(scope) · 근거 약 · 원천 질문 걸림 · 추천 제외 · gap(no_complication 등) · 사람 확인 상태 — 범례 · 「표시 붙은 것만」 필터
- 쉬운 말 · 항목 한 줄 · 원문 · 근거는 접기 · 큰 목록은 접고 개수

## 지킬 것
- 데이터는 페이지에 내장(필요 칸만 뽑아 json · 6.6MB 원본보다 작게) · U+FFFD 0 · node 구문 검사 · jsdom 스모크(예시 시작점 5개 펼침 · 검색 · 필터 · 오류 0)
- 실명 · 키 · 병원 원본 사진 금지. 실버 json · 원천 수정 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_2b987ac1-9134-4fe8-9507-b79fb361deef --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "tool_dev 완료: 실버 연결 구조 페이지" --body "노드 종류 N · 엣지 종류 N · 노드 N · 엣지 N / 파일 크기 / 검사 결과"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] tool_dev 완료 — 실버 연결 구조 페이지. 상세는 인박스." --enter
```

## 추가(사용자 10-29) — 이웃 그래프 그림
- 「따라가 보기」에 **고른 노드 주변 1~2홉을 점 · 선 그림**으로(목록과 같이 · 탭이나 나란히). 라이브러리는 cdnjs 의 cytoscape(또는 동급) — 다른 CDN 금지
- 점 색 = 노드 종류(구조 지도와 같은 색) · 선 = 엣지 종류(라벨 · 화살표) · 표시 색(충돌 · 조건부 · 근거 약 …)은 선 스타일(점선 · 색)로
- 점 누르면 그 노드로 이동(그림 · 목록 · 경로 같이 바뀜) · 1홉 / 2홉 전환 · 엣지 종류 켜고 끄기
- 이웃이 많으면(예: 50 넘음) 종류별로 묶음 점(「단위 시술 34」)으로 접고 눌러 펼침 — 엉키지 않게
- 계열 상속 엣지는 계열 점에 이어서(단위 시술에 펼치지 않음)
- jsdom 스모크에 그림 컨테이너 생성 확인 추가(렌더 자체는 브라우저)
