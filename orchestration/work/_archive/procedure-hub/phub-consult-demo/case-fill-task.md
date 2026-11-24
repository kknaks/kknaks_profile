# [data] 케이스 보충 — 모든 케이스의 부위 · 방법 · 조직 · 재료를 빈칸 없이 (사용자 승인 11-20)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 수정 0 · 사용자 포트(18105 · 18222) 손대지 마라 · 키 출력 0.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · `S=$W/silver-model`(silver 작업 사본 · gold 7b8669b7 · 앞 작업 `$W/case-unit-report.md`) · `R=$P/reference/2026-11-19-myeongdong-kos`
원장 = `$P/orchestration/work/_archive/procedure-hub/phub-recommend/bronze/phub-ledger/`(source_ref 포인터로 연다). 식약처 조회(필요할 때만 · 서버 띄우지 말고 코드 직접): `/Users/kknaks/git/toy_pr2/kknaks_profile/reference/2026-10-27-mfds-mcp/`(`src/mfds_mcp/tools.py` · `.env` 키 준비됨 · 출력 금지).

## 원칙(사용자 11-20 — 다시 묻지 마라)
- **케이스 = 단위 시술** = 시술 + 부위 + 방법 + 조직 + 재료 (+ 고민 · 제품 연결). 단위 시술이면 **부위와 방법은 반드시 있다**(입꼬리 보톡스 = 입꼬리 × 근육 주사).
- **원장은 정규화 누락이 많다. 우리 데이터는 완전히 채운다.** 11-14 규칙 「원장이 말하지 않은 칸은 비운다」를 이번에 **폐기**한다. 원장이 안 적은 당연한 값(보톡스 = 근육 주사)은 채우고 근거 종류를 「보충」으로 남긴다.
- 지어내기는 금지 — 채운 값마다 근거가 있어야 한다. 근거 우선순위: ① 원장 케이스 문장 ② 원장 시술 · 계열 문장(「보톡스는 근육에 주사」) ③ 식약처 허가 자료(용법 · 투여 경로) ④ 같은 시술의 다른 케이스 원장 값 ⑤ 표준 의학 지식(보충 — 근거 글에 한 줄로 이유).
- 케이스 코드는 바꾸지 않는다(명동점 매핑 JSON 이 가리킴). 케이스를 쪼개거나 합치지 않는다 — 넓은 값으로 채운다.

## 지금(코디 셈 · 다시 세어 확인)
케이스 344 · 칸 채움: 부위만 119 · **전부 빈 109** · 방법만 69 · 방법+재료 24 · 재료만 14 · 부위+재료 5 · 부위+방법 4. 방법 있는 케이스 97(보톡스 29 중 2). 케이스 없는 시술 7. 시술 단위 방법 표 없음(procedure_material 은 있음).

## 할 일
1. **시술 기본 방법:** 시술 139 각각의 기본 방법(투여 경로 · 시술 방식)을 정한다(`method.csv` 사전 · 없으면 사전에 새 방법 추가 + 근거). 표 `$W/procedure-default-method.csv`(시술 · 기본 방법 · 근거 종류 · 근거).
2. **케이스 칸 채우기**(344 + 새 케이스):
   - 방법(`case_method`): 빈 케이스에 그 시술 기본 방법. 원장이 따로 말한 케이스(스킨보톡스 등)는 그대로.
   - 부위(`site_code`): 빈 케이스는 원장 문장 · 시술 성질로 — 얼굴 전체 = SITE-007 얼굴 · 몸 = 몸 코드 · 얼굴 + 몸 / 전신 작용(수액 · 주사 전신 투여) = SITE-001 전신. 방법 · 재료로 갈린 케이스(레이저토닝 등)도 부위를 채운다(원장 · 시술 성질로 얼굴이면 얼굴).
   - 조직(`tissue_code`) · 해부(`anatomy_code`) · 재료(`material_code`): 빈 칸을 같은 근거 순서로. 재료는 시술 재료가 하나면 그것 · 여럿이면 원장 · 제품으로 · 정말 정할 수 없으면 「사람 판단」 목록.
   - 케이스 없는 시술 7 → 케이스를 만들어 위 칸을 채움.
   - 근거: 각 새 값마다 source_ref(로컬 근거 파일 꼴은 앞 묶음과 같음 — `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>` · 근거 글 「케이스 보충 2026-11-20 · <근거 종류> · <이유>」). 공개 silver 에 병원 이름 · 진료항목 코드 0.
3. 스크립트 `drafts/clinic-supplement/clinic-a-20261119/build_batch4.py`(재현 가능) · 기준 사본 `archive/silver-before-clinic-a-20261119-b4/` · silver-check → gold-build → gold-check(작업 사본 스크립트 · 앞 묶음과 같은 방식 · 검사 고치면 diff 리포트). 그 밖 FAIL 은 멈추고 질문.
4. 매핑 JSON 두 경로 다시 만듦(앞 작업 스크립트 · meta 해시 새로 · 케이스 코드 그대로인지 확인).
5. 리포트 `$W/case-fill-report.md`: 칸별 전 → 후(빈칸 수) · 근거 종류별 수 · 새 방법 사전 항목 · 새 케이스 · **사람 판단 목록**(50 안쪽 · 묶어서 · 묶음마다 추천) · 확인 예(CAS-006 입꼬리 보톡스 · CAS-016 스킨보톡스 · 레이저토닝 · 수액 1 · 면포압출) · 검사 · 해시.

## 검증
케이스 전부 부위 · 방법 빈칸 0(사람 판단 목록에 든 것 제외 · 그 수 = 목록 수) · 조직 · 재료 빈칸 수와 이유 · 새 값 전부 source_ref 있음 · silver-check · gold-check PASS · 케이스 코드 바뀜 0 · JSON 324 두 경로 같은 해시 · 병원 이름 grep 0.

※ 동시에 다른 워커(term 은 아래 리포트로 안내)가 **읽기만** 하며 「고민 → 케이스 연결 방식」을 설계한다. 너는 silver 를 고치는 유일한 워커다. 끝나면 리포트 경로를 그 워커가 읽는다.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_c3f59148-8ca7-4a86-8c2b-1ea060538176 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 케이스 보충" --body "빈칸 전후 / 사람 판단 / 검사 / 해시"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] data 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data: <질문>" --enter`
