# [reviewer] 7단계 고민 → 시술 전수 눈검 — 영역을 계산할 수 없는 엣지 · 추천 조합 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 읽기만. 산출 `orchestration/work/phub-recommend/review-step7-sweep.md` 하나(+ 같은 이름 .json).

## 왜(사용자 10-30)
사용자가 연결 구조 페이지에서 「이중턱 → 겨드랑이 마이크로웨이브」 · 「목주름 → 관자놀이 필러」를 직접 찾았다. 부위가 있는 고민은 R21 · R22 규칙으로 고쳤지만(`step7-siteup-report.md`), **영역을 계산할 수 없는 고민(P4 항노화 · P5 · P6 · P7 · P9 · P14 · 쁘띠시술 등)의 엣지 169 · 추천 조합 구성 117** 은 규칙이 못 거른다. 사용자가 하나씩 찾지 않도록 **전수로 보고 이상한 것만 추린다.**

## 볼 것(전수)
- `step7-concerns.json` edges(앵커 부위 없음 · R22 영역 없음) · combos 구성 — 위 셈을 파일에서 다시 세서 시작
- 고민마다: 붙은 단위 시술 목록 · 그 엣지의 원천 근거(source · basis · evidence) · 단위 시술의 부위 · 계열 · 기법 · 5단계 purposes
- **이상함 판정 기준(지금 데이터 근거로만 · 가상 문장 금지)**:
  ① 단위 시술의 부위가 고민 뜻과 어긋남(예: 색소 고민에 두피 시술 · 다한증에 얼굴 미용 보톡스)
  ② 원천 근거는 계열만 말하는데 계열 안 다른 용도 시술까지 열림(5단계 purposes 와 고민이 안 맞음)
  ③ 원천 근거 문장과 단위 시술이 다른 말(원천 「레이저토닝」 → 붙은 건 제모 레이저 등)
  ④ 같은 고민에 같은 계열 시술이 부위만 바꿔 대량으로(후보 전부 흔적)
- 판정마다 근거 칸 · 「이상함 / 확인 필요 / 정상」 · 이상함이면 추천 조치(빼기 · 계열만 · 규칙 후보)

## 산출
- 맨 위: 본 셈 · 이상함 N · 확인 필요 N · 정상 N · **원인별 묶음**(같은 원인은 규칙 하나로 고칠 수 있게)
- 사용자에게 보일 표: 이상함 · 확인 필요만 — 고민 · 단위 시술 · 왜 · 추천 조치 · 원천 근거 한 줄
- 정상은 셈과 고민별 요약만

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_a2bf6061-125c-47d8-b6c8-bb0b4fb2395c --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 7단계 고민 → 시술 전수 눈검" --body "본 엣지 N · 조합 N / 이상함 N · 확인 필요 N / 원인 묶음 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] reviewer 완료 — 7단계 고민 → 시술 전수 눈검. 상세는 인박스." --enter
```
