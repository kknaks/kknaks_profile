# [researcher · 읽기만] 고민 0 케이스 35 의 고민 찾기 + 엑시머 레이저 개요 · 원리 (사용자 승인 11-20)

너는 procedure-hub 조사 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. **silver · gold · DB · 허브 레포 쓰기 0** · 커밋 0 · 서브에이전트 0 · 사용자 포트(18105 · 18222) 손대지 마라 · 키 출력 0. 산출은 아래 파일뿐.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model/silver`(gold 43b95e4e) · 원장 = `$P/orchestration/work/_archive/procedure-hub/phub-recommend/bronze/phub-ledger/`
조회 도구(필요할 때 · 서버 띄우지 말고 코드 직접 · 키 출력 금지): 식약처 `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-27-mfds-mcp/`(`src/mfds_mcp/tools.py` · device · drug 허가 · 사용 목적) · 약학정보원 `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-28-kpic-mcp/` · 웹 검색(제조사 공식 · 식약처 · FDA 510(k) · 논문 · 교과서).

## 원칙(사용자 11-20 — 다시 묻지 마라)
케이스 = 단위 시술. 고민은 케이스에만. **우리 데이터는 완전히 채운다** — 모든 케이스는 고민 1 이상. 원장에 없으면 외부 근거로 채우되 **출처 필수 · 지어내기 금지**. 고민은 허브 고민 사전(`$S/concern.csv` 266)에서 고르고, 사전에 없으면 새 고민 후보(이름 · 상위 고민 · 근거).

## 대상
1. `$W/concern-zero-cases.csv` — 고민 0 케이스 35(케이스 · 시술 · 부위 · 조직 · 설명 · 명동점 진료항목). 앞 리포트의 이유: 조직(표적)이 달라 같은 시술 고민을 못 옮김 15 · 시술 자체에 고민 0 20(`$W/concern-apply-report.md` §7).
   - CAS-064 근적외선 타이트닝은 사용자 BBL 조사(`$W/bbl-research-user-20261120.md` — SkinTyte 적응: 피부 처짐 · 이완 · 탄력 저하)도 근거로 쓴다.
2. 시술 「엑시머 레이저」(이번에 새로 만든 시술 · `$S/procedure.csv` 의 엑시머 행) — `overview` · `mechanism` 빈칸 · 원리 코드(`mechanism_code`) 후보. 다른 시술 overview · mechanism 문체(쉬운 한국어 2~3 문장)를 따라 쓴다.

## 산출
- `$W/concern-zero-fill.csv`(utf-8-sig): 한 줄 = (케이스 × 고민). 칸: `case_code` · `procedure` · `site` · `tissue` · `concern_code`(사전 코드 또는 「새」) · `concern_name` · `새 고민이면 상위 고민 · name_en` · `근거 종류`(원장 / 제조사 · 식약처 · 논문 · 교과서 등 외부 / 같은 시술 다른 케이스 / 사용자 제공) · `출처`(파일 포인터 또는 URL) · `근거 문장`(원문 그대로 짧게) · `확신`(확실 / 후보). 케이스마다 1 줄 이상 — 정말 근거를 못 찾으면 그 케이스를 `근거 못 찾음` 한 줄로(이유).
- `$W/excimer-overview.md`: overview · mechanism 문안 · mechanism_code 후보 · 출처.
- `$W/research-concern-zero.md`: 케이스별 결과 수 · 근거 종류별 수 · 새 고민 후보 · 근거 못 찾은 케이스 · 명동점 진료항목에 닿는 변화.

## 검증
35 케이스 전부 표에 · 출처 빈칸 0 · 사전 고민 코드 실재 · `git -C $P status --short` 에서 새 파일이 위 3 개뿐 · silver 바이트 그대로.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_d630855d-4002-4ea8-94ec-00c387f4b872 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: 고민 0 케이스 · 엑시머" --body "케이스별 / 근거 종류 / 못 찾은 것"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] researcher 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] researcher: <질문>" --enter`
