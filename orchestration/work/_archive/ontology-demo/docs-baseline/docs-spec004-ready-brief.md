
# [docs] 소수정 — 디자인 조정 완료 반영: SPEC-001 좌표 3건 · SPEC-004 §7.2 정리 · ready 승격

너는 **ontology-demo `docs` 워커**다. 같은 워크트리, 같은 규칙. design-fix 가 끝났다 — 조정된
디자인 패키지(read-only): `/Users/kknaks/orca/workspaces/kknaks_profile/ontology-demo/reference/ontology_demo/design/`

## 할 일 (코디 확정값)

1. **SPEC-001**(v0.0.4→0.0.5): 노드 표 '미배정' 좌표 3건 채움 — visits (355,460) · new_patients_domestic (355,210) · sales_foreign_est (895,490). (design-fix 배정, 코디 JSON 검증 완료)
2. **SPEC-004**(v0.0.2→0.1.0, **status: draft → ready**):
   - §7.2 「디자인 조정 대기 20건」 표 → 전건 해소 표기(2026-09-02 design-fix). 프로토타입 4종(Monitoring·Data·Frames·DesignSystem)의 옛 데이터는 「참조 시 문서·data/*.json 우선」 경고로 갈음 — 미해소 아님, 비고로 남김.
   - 데이터 화면 골드 계층 칩 = **5개**(gold_kpi_monthly 포함 — 테이블 목록 파생 원칙) 명시.
   - 채팅 예문 소재 확정 반영: 패턴 A = R-2 전제 교정, 패턴 B = 기각 엣지 new_patients→sales_total 배제 + payment_visits 경유 대체 경로, C 정량 추정 없음.
   - edge_id 규약 `<from>__<to>` (design-fix data 와 SPEC-003 동기 — SPEC-003 에 규약이 이미 다르게 적혀 있으면 그쪽도 맞춰 patch).
3. 20-spec/README(Spec List 버전·SPEC-004 ready·OQ 표 정리 — SPEC-004 OQ 중 디자인 대기 건 닫기) · 제품 README 현재 상태 · log.md 1줄.

## 하지 말 것 — 위 외 수정 금지. 30-work·decision 무변경. 커밋·push 금지.

완료 보고: 동일 2채널 (preamble 값, 코디 term_45e793be-0adb-44c7-9d9a-eb35c4f48320), subject "docs 완료: SPEC-004 ready".
