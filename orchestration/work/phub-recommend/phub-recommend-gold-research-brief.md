# [researcher] 골드 설계 조사 — 규칙 적용 그래프 · 허브 도구 · 의도별 탐색 · 패널 응답 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 작업 폴더 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`.
**읽기만**. 산출 `gold-research.json` · `gold-research.md`.

## 목표 · 아키텍처(사용자 10-30 · `_RESUME.md` §2 「목표 · 아키텍처」 행)
- 상담 앱에서 유저 질문에 **빠르고 정확하게** 답한다. 화면 = 채팅 + 왼쪽 얼굴 지도 패널에 그 부위 추천 시술 · 설명(· 병원 상품 — 이건 별도 연결 층 · 이번 범위 아님). 디자인 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-chatry-sample/`(S3p-Scenario.dc.html 11단계 대화 — 읽어서 질문 · 패널 갱신 흐름 뽑기)
- 흐름: 상담 앱 Jev(빠름 · 질문 → 의도 · 슬롯) → **허브 도구(결정론 · LLM 없음)** → Claude(답 문장). **허브에는 LLM 없음**(10-26). Jev 는 슬롯만 · 허브 호출은 앱 서버가(추천 — 판단 표에)
- **골드 = 카드 묶음이 아니라 「규칙을 다 적용한 그래프」** — 실버 1,145 노드 · 5천 엣지 규모라 요청 때 탐색해도 ms. 허브 도구가 골드 그래프를 탐색한다. 자주 오는 의도는 정해 둔 탐색 경로 · 여러 홉 질문도 같은 그래프로
- **허브는 병원과 무관 · 고정**. 병원 상품은 연결 층(별도 조사 `kos-link-research` 진행 중)이 단위 시술 id 에 붙임 — 골드는 단위 시술 · 제품 id 를 안정 키로 내기만

## 입력
- 시맨틱 정본 `semantic.json` · `.md`(노드 13 · 엣지 21 · 표시 12 · gate 3값 · 상속 규칙 9 · 사전 · id 대응) · 실버 `step1` ~ `step8` json · 결정표 `_RESUME.md` §2 전부(특히 10-26 경계 · 10-27 W-1 기본 응답 · 10-29 reading_contract · 피함 · by_sub_condition · 10-30 R21 ~ R27)
- 옛 SPEC-004(대체될 것 · 참고만)

## 만들 것(추천안 · 근거 · 셈)
1. **골드 그래프 규칙**: 상속 펼치기(계열 → 단위 시술 · 하위 · 기법 · 부위 — 시맨틱 상속 9 그대로 계산) · 부작용 덮어쓰기(계열 → 제품 · 단위) · 기본 응답 거르기(gate · 표시별 — 안전 정보는 늘 냄) · 충돌 · 조건부 · by_sub_condition 처리 · 결과 셈(펼친 뒤 엣지 수 등 — 실제로 계산해 보기)
2. **의도 목록**: 샘플 11단계 + 상담 질문 종류(고민 → 추천 · 시술 설명 · 비교 · 같이 · 순서 · 간격 · 나한테 해도 되나(확인 조건) · 부작용 · 회복 · 가격은 연결 층) — 의도마다 슬롯 · 예시 질문(샘플 근거)
3. **허브 도구 목록**(REST · MCP 같은 것): 사전 검색(말 → 후보 노드 id) · 의도별 탐색 · 범용 이웃 탐색 — 입력 · 출력 스키마 초안 · 결정론 · 후보 여럿이면 후보 전부(10-27)
4. **의도별 탐색 경로**: 골드 그래프 위 경로(예: 고민 × 부위 → 추천 단위 시술 → 관계 · 피함 · 확인 조건 · 합병증 · 부작용 · 근거)
5. **패널 응답 모양**: 왼쪽 얼굴 지도 영역(3단계 부위 노드 대응) · 카드 칸 · Claude 에 줄 뼈대(근거 id · 표시 · 「카드 밖 말 금지」용)
6. **속도 · 정확성 장치**: 응답 크기 · 홉 제한 · 근거 인용 · 표시 전달
7. 결정 묶음 + **사용자 최종 판단 한 표**(진짜 사용자 몫만)
- 지금 데이터로 계산 · 추정 금지 · 가상 문장 시험 금지 · 실버 · 시맨틱 수정 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_b0dd9333-4a56-452d-8ebb-b1e5c228c17a --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "researcher 완료: 골드 설계 조사" --body "골드 규칙 N · 의도 N · 도구 N · 탐색 경로 N / 펼친 뒤 엣지 N / 결정 묶음 N · 사용자 판단 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — 골드 설계 조사. 상세는 인박스." --enter
```
