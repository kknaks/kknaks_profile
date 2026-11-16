# [planner] SPEC-005 · WORK-003 — 허브 골드 그래프 · 도구 (새로 · SPEC-004 · WORK-002 대체)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/planner/role.md`(rules · workflow · skills 같이). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`. 산출 `SPEC-005.md` · `WORK-003.md` + SPEC-004 · WORK-002 맨 위에 「SPEC-005 · WORK-003 으로 대체됨(2026-10-30)」 한 줄만.

## 정본(이것만 근거 · 결정 다시 논의 금지)
- 결정표 `_RESUME.md` §2 전부 — 특히 10-26 경계(허브 = 데이터 그래프 + 범용 조회 도구 · LLM 없음 · 안전 엣지 늘 동봉) · 10-27 W-1 · 10-29 reading_contract · 10-30 행 전부(골드 = 규칙 적용 그래프 · 허브 고정 · 병원 연결 층은 앱 · 충돌 하나로(D-13b 바꿈) · 품질 목표 · **골드 규칙 판단 추천대로 ①~⑤ · D-01~D-14**)
- 시맨틱 정본 `semantic.json` · `.md`(노드 13 · 엣지 21 · 사전 · resolve_rules · id 대응 · 상속 9 · 표시 12 · gate 3값)
- 실버 `step1` ~ `step8` json(입력 계약 = 이 파일 · 칸 경로 — 실물과 대조해 적을 것 · 10-27 SPEC-004 검수 FAIL 「입력 계약이 실물과 다름」 되풀이 금지)
- 골드 조사 `gold-research.md` · `.json`(골드 규칙 G1~G17 · 의도 12 · 도구 9 · 탐색 경로 11 · 패널 응답 · 속도 장치) — 단 G14 · D-08 은 「충돌 = resolved 하나」로 바뀜 · G9 부작용 값 · G17 조합 구성은 이미 실버에 있음
- 품질 측정 `quality-report.md` · `quality-eval.py` · `quality-eval-set.json` — **골드 E2E 의 정답 세트로 재사용**(목표 6/6 유지가 완료 조건)
- 코드 레포(로컬 전용 · push 금지) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` — v1 그래프(app/graph_main.py · MCP 18005 · DB 55434)에서 **뼈대만 재사용**(진입점 · MCP 마운트 · DB 연결) · 나머지 새로

## SPEC-005 에 담을 것
1. 범위 · 경계(허브 = 골드 그래프 + 결정론 도구 · LLM 없음 · 병원 상품 · 연결 층 · Jev · 앱은 밖)
2. 입력 계약: 실버 · 시맨틱 파일 · 칸 경로(실물 대조)
3. 골드 빌드: G1~G17(정정 반영) · 펼치기 · 거르기 · 안전 동봉 · resolved · by_sub_condition · by_direction · gap 3상태 · 결정론(빌드 해시)
4. 저장: 스키마(노드 · 엣지 · 속성 · 표시 · 근거) · 적재 방식
5. 도구(REST · MCP 같은 코어): 사전 검색(resolve_rules) · 의도별 경로(① CC 슬롯 · ② 메뉴 → 조합 · ③ 조합 기본 응답 범위) · 범용 이웃 탐색 · 입력 · 출력 스키마 · 후보 여럿 처리 · 응답 크기
6. 품질 · E2E: quality-eval 을 골드 도구 위에서 돌려 6/6 · 실물 호출(로컬 서버) · 속도 측정
7. 열린 것(사용자 몫만 · 추측 금지)
## WORK-003: Phase 나눔(적재 → 골드 빌드 → 도구 → E2E) · Phase 마다 완료 조건 · 관련 시험만(전체는 끝에 한 번)

- 실명 · 키 금지 · 가상 문장 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d604db9d-e1da-4569-bef7-73441af2e8d8 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC-005 · WORK-003" --body "SPEC 절 N · 도구 N · Phase N / 열린 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] planner 완료 — SPEC-005 · WORK-003. 상세는 인박스." --enter
```

## 추가(코디 10-30) — E2E 완료 조건 강화
- quality-eval 목표 6/6 유지 **+ 지금 남은 틀림 4문항(Q106 메뉴 → 조합 · Q108 · Q109 · Q110 조합 기본 응답 범위)이 골드 도구에서 맞음** — 판단 ② · ③ 이 도구 규칙으로 구현돼야 함. 의료진 질문 5문항(Q042 · Q075 · Q083 · Q084 · Q102)만 계산 밖
