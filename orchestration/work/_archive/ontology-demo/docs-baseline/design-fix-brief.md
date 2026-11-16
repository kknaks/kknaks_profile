
# [design-fix] 디자인 패키지 조정 — 정정 20건 + 신규 설계 3건 + 데이터 재키잉

너는 **디자인 조정 워커**다. 이번 태스크에 한해 쓰기 허용 범위는 **오직**:
`/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/design/` (하위 전부)
그 밖(리포 파일·reference 의 design 밖·orchestration)은 읽기만. **원천 데이터(bronze/·silver/ 등)는 열지도 마라 (PII).**

## 1. 입력 (read-only)

- `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/DESIGN_FEEDBACK.md` ← 조정 요구 전문
- `/Users/kknaks/orca/workspaces/kknaks_profile/docs-baseline/para/projects/summer-star/ontology-demo/20-spec/` ← 값의 SoT (정정본 v0.0.3). 특히 SPEC-001 §4(테이블·행수·enum·마스킹 표기·**node_id 25종 표**), SPEC-003 §4(엔드포인트·채팅 폴링·상태·에러), SPEC-004(화면 계약 — §7.2 디자인 조정 대기 표가 이번 체크리스트), SPEC-005 §4(답변 객체)
- 디자인 패키지 자체(`design/` 안 01~08·data/·design/*.dc.html) — 기존 토큰·컴포넌트 체계를 벗어나지 마라. 새 색·새 컴포넌트 패턴 발명 금지.

## 2. 할 일

### A. 값 정정 (기계적 — SPEC-001 v0.0.3 값 그대로)

- `data/tables.json`: 행수 8건(75,479 · 6,198 · 73 · 9,689 · 11 · 235 · 34 · 57) · `noshow_rate = 부도÷(내원+부도)` · `visit_status` enum 내원·취소·부도 · gold_promo_calendar 그레인(프로모션 1건=1행) · 골드 표 컬럼 보강(foreign 계열 4컬럼)
- 마스킹 표기: 생년월일 `1990-**-**`(연도 노출) — 08·02·06 전수
- 실버·골드 중립바 카피: 「실명·전화·생년월일은 이 계층으로 올라오지 않습니다(차트번호는 추적용 유지)」
- 기준일 배지·「그 외 KPI」 카운트: 하드코딩 값 대신 「데이터 파생」 명시(08 §7 원칙 그대로)

### B. 그래프 데이터 재키잉 (`data/nodes.json`·`edges.json`)

- node_id 를 SPEC-001 §4 노드 표의 snake_case 25종으로 전면 재키잉 (camelCase 폐기)
- 신규 3노드 **좌표 배정**: `visits`·`new_patients_domestic`·`sales_foreign_est` (viewBox 0 0 1130 560 안, 기존 배치 문법에 맞게. 배정값을 보고에 명시 — spec 표의 '미배정' 을 채울 입력이다)
- 삭제된 3노드(review_campaign·organic_new·review_positive_rate) 제거
- edges 27건을 정본 판정(채택/자동 확정/선언/보류/기각)·부호·lag(원형 — `2w` 포함)·신뢰도·근거로 정정. 없는 엣지 제거(noshowRate→churn, cancelRate→churn 등), 합성 노드(reviews) 해소
- node_type 은 영문(kpi/intervention/…), 화면 한글 라벨은 SPEC-004 매핑표 기준

### C. 예문 정정 (05-screen-chat)

- 패턴 A·B 예문을 **SPEC-001 노드 표·SPEC 에 실린 실재 확정 엣지**로 교체 (예: cancel_rate→reservations 채택, weekday→noshow_rate 기각은 excluded 로). 패턴 C 는 정량 추정 문구 제거(관계 방향·r·n 까지만)
- 채팅 우측 520px 근거 그래프 패널 **제거** — used_edges 는 답변 칩 + 칩 클릭 → 모니터링 `?edge=` 점프. 05·07·Chat.dc.html 동기

### D. 신규 설계 3건 (기존 토큰·컴포넌트 안에서)

1. **채팅 진행 상태 5종**: pending(부분 텍스트+도구 단계)·failed+재시도·타임아웃(180초)·대화 잠금(BUSY, 컴포저 비활성)·1,000자 초과 문구 — 05 문서 + Chat.dc.html 프로토타입에 반영. 계약은 2초 폴링(SPEC-003 §4)
2. **접속 게이트 화면**: 비밀번호 1칸 입력·오류·성공 후 복귀 (SPEC-003 U-1 문구) — 02 컴포넌트 + 신규 절
3. **채팅 레이아웃 재구성**: 패널 제거 후 스레드 폭·정렬 재정의

### E. 구조·기타

- 06·tables.json: 브론즈 = 원천 3칩 + nexus 선택 시 2단 칩 14개, 계층 카운트 「브론즈 16」 파생
- 07: 라우팅 표 `/ontology/{monitoring,chat,data}` · 채팅 상태 절을 conversation/message 모델로 교체 · `min-width:1280px` 는 데모 컨테이너 스코프로
- 02: 컬럼 분포 바 제거(범위 밖 확정)
- `design/README.md` 에 개정 이력 절 추가(오늘 날짜·조정 요약)

## 3. 하지 말 것

- 새 색·폰트·컴포넌트 패턴 발명 금지(01·02 체계 안에서). spec 값과 다른 값 창작 금지 — 비면 보고.
- design/ 밖 쓰기 금지. git 조작 금지(이 폴더는 gitignore — 상관없지만 리포 쪽은 건드리지 마라).

## 4. 완료 보고 — 2채널 모두 (preamble 의 taskId·dispatchId 사용)

```bash
orca orchestration send --to term_45e793be-0adb-44c7-9d9a-eb35c4f48320 --from <네 워커handle> \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "design-fix 완료" --body "파일별 변경 요약 / 신규 3노드 좌표값 / A~E 체크리스트 결과 / 못 정한 것"
orca terminal send --terminal term_45e793be-0adb-44c7-9d9a-eb35c4f48320 \
  --text "[worker_done] design-fix 완료 — 조정 20건·신규 3건·재키잉. 상세는 인박스." --enter
```
