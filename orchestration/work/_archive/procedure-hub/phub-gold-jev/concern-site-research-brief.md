# [researcher] concern_site 보강 — 원장 근거 확인(읽기만)

너는 **procedure-hub `researcher` 워커**다(read-only). 앞 판 맥락이 없다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/researcher/role.md`(+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`).

작업 워크트리(코디 · 공유): `P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` — **리포트 1개 외에는 만들거나 고치지 마라.** 같은 폴더에서 다른 writer 둘이 다른 파일을 쓰는 중이다.

경로: `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(silver · gold · notes — 읽기만) · 원장 `L=$P/orchestration/work/phub-recommend/bronze/phub-ledger/`(JSON 21 — 읽기만)

## 배경 · 정해진 것

- 사용자 결정(11-17): silver `concern_site`(고민 ↔ 부위)를 **원장에 부위가 분명한 고민만** 보강한다. 원장에 있는 것만 넣고 지어내지 않는다 · 없으면 목록으로만 남긴다. 묶음 고민(주름 · 처짐 · 윤곽 · 체형 등 — 하위가 부위를 가짐)과 원래 부위가 없는 고민(기미 · 탄력 저하 · 노화 · 혈관종 등)은 보강하지 않는다.
- **이번은 조사만.** silver 반영 · gold 재빌드 · DB 재적재는 지금 구현이 끝난 뒤 한 번에 한다(코디 몫).
- 코디 어림 후보(silver 이름 · 설명 기준 — 원장 문장으로 확정 필요): CON-025 불독살 → 턱선(볼) · CON-162 저작근 비대증 → 사각턱 · CON-166 사다리꼴근 비대증 → 승모근 · CON-190 러브핸들 → 복부(옆구리) · CON-200 탈모 · CON-277 두피/탈모 · CON-209 비듬 · CON-122 모공 막힘 → 두피(탈모는 정수리도) · CON-156 튼살 → 배 · 허벅지 · CON-260 손톱 약화 → 손톱.

## 할 것

1. 후보마다: silver `concern` 행 · 지금 `concern_site` 행 · silver `site` 에 맞는 부위 코드가 있나(없으면 「부위 코드 없음」) · **원장 근거 문장**(파일 · JSON 경로 · 문장 그대로 — 고민이 그 부위에 있다고 원장이 말하는가) · silver `source_ref` 로 그 고민이 원장 어디서 왔나.
2. 판정: 넣음(근거 있음 · 부위 코드 있음) / 안 넣음(근거 없음 · 묶음 고민 · 원래 부위 없음) / 부위 코드 없음(silver site 에 없는 자리 — 사전 보강이 따로 필요) — 각각 이유.
3. **후보 밖도 한 번 훑는다**: 부위 연결 없는 고민(자기 기준 175 · 하위 포함 160 — SPEC-001 0.7.1 §5-11 SP 재셈) 가운데 원장 문장에 자리가 분명한 것이 더 있나(이름에 부위 낱말 · 원장 indication 문장의 부위). 추가 후보만 같은 꼴로.
4. 넣음으로 판정된 것의 **silver `concern_site` 행 초안**(id 는 빈칸 · concern_code · site_code · 근거 경로) 표 — 파일로 쓰지 말고 리포트 안 표로.
5. 넣었을 때 영향 어림: 그 고민의 「고민 + 부위」 질문이 HG3(거름) 쪽으로 바뀌는 것(SPEC-001 0.7.1 SP → HG3) · 얼굴 점 생기는 고민 수 · 37 답 키 문항 가운데 닿는 것(questions.csv · 키 명세 — 앱 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev/data/eval-set/` 읽기만).

리포트 머리에 요약 + 「넣음 / 안 넣음 / 부위 코드 없음」 표 + 「정할 것」(있으면 · 추천 붙임).

## allowed_paths

- **쓰기: `$W/research-concern-site.md` 1개만.** 임시 파일은 네 scratchpad.

## 하지 말 것

결정 · silver/gold 수정 금지 · 외부 호출 · `.env` 금지 · 서버 · DB 건드리지 마라 · 큰 파일 금지.

## 완료 보고 — 문구 변경 금지

> 핸들은 dispatch preamble 값을 믿어라.

```bash
orca orchestration send \
  --to term_a88e896b-403c-4d2d-9bcc-4388724b3418 --from <네 터미널 핸들> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "researcher(concern_site) 완료: <한 줄>" \
  --body "변경 파일 / 넣음 · 안 넣음 · 부위 코드 없음 수 / 정할 것 / 주의점"

orca terminal send --terminal term_a88e896b-403c-4d2d-9bcc-4388724b3418 \
  --text "[worker_done] researcher(concern_site) 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
