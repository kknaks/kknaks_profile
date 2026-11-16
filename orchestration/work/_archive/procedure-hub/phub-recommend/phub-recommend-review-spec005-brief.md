# [reviewer] SPEC-005 · WORK-003 검수 — 실물 · 결정표 전수 대조 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `orchestration/work/phub-recommend/`. 산출 `review-spec005-report.md` 하나 · 맨 위 PASS/FAIL + 「open = N」.

## 볼 것(전수 · 지금 데이터만)
1. **입력 계약 §2**: 적힌 파일 · 칸 경로 · 해시를 실버 `step1` ~ `step8` · `semantic.json` 실물에 하나씩 대조(없는 칸 · 이름 다름 · 셈 다름). SPEC-004 가 검수에서 「입력 계약이 실물과 다름」으로 떨어진 전례 — 그 꼴 0 이어야
2. **결정 반영**: `_RESUME.md` §2 의 10-26 경계 · 10-27 W-1 · 10-29 reading_contract · 10-30 행 전부(골드 = 규칙 적용 그래프 · 허브 고정 · 연결 층 앱 · 충돌 하나로 resolved · 품질 목표 · 골드 판단 ①~⑤ · D-01~D-14(D-08 정정) · 메뉴 라벨 8 · U-2 · U-3 앱 몫 · KOS 기록만)가 SPEC 에 빠짐 · 어긋남 없이 들어갔나. 결정에 없는 새 결정이 「정해진 것」처럼 들어갔나(있으면 FAIL · 열린 것으로)
3. **골드 규칙 §3**: gold-research G1~G17 정정 3곳 · G18 · 셈이 지금 실버로 맞나(펼친 뒤 행 수 등 가능한 건 직접 계산)
4. **도구 §5**: 9 도구 입력 · 출력 스키마가 의도 12 · 품질 문항 111 을 덮나(문항마다 어느 도구로 답하나 표) · ①②③ 경로
5. **E2E §6 · WORK-003 완료 조건**: 품질 6/6 + Q106 · Q108~110 · 의료진 5문항 제외 · 실물 호출 · 속도 — 측정 가능하게 적혔나
6. **WORK-003 Phase**: 순서 · Phase 마다 완료 조건 · 관련 시험만(전체 검증은 끝에 한 번) · 코드 레포 로컬 전용 · push 금지 · v1 뼈대만 재사용 · 키 · 실명
7. SPEC-004 · WORK-002 「대체됨」 한 줄만인지
- 가상 문장 · 미래 원천 시험 금지 · 지적은 지금 데이터 · 결정표 근거로만

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_985b2783-a884-4f3f-8c78-49992113369e --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: SPEC-005 검수" --body "PASS|FAIL · FAIL N · WARN N · open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] reviewer 완료 — SPEC-005 검수. 상세는 인박스." --enter
```
