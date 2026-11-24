# [data] 허브 데이터 구멍 3 — 입꼬리주름 · 팔자주름 필러 · 타이트닝 효과 (사용자 승인 11-23 「응 추천대로해」)

너는 procedure-hub 데이터 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · **18105 · 18222 손대지 마라**(허브 18105 는 GET 만 · 새 gold 로 재기동은 코디) · 키 출력 0. 막히면 질문.

`P=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇` · `W=$P/orchestration/work/phub-consult-demo` · 작업 사본 `S=$W/silver-model`(`silver/*.csv` · `gold/`) · 앞 방식(그대로 따라라) `$W/concern-apply-task.md` · `$W/concern-apply-report.md` · `$W/case-fill-task.md` · 매핑 JSON(읽기만) `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo/data/kos/myeongdong-mapping-20261120-v3.json` · 측정 정답표 `$W/quality/answers.md`(#1 · #7 · #12).

## 원칙(다시 묻지 마라)
- 케이스 = 단위 시술(부위 · 방법 필수) · **고민 · 제품은 케이스에만** · 우리 데이터는 완전히 채운다(원장 누락은 근거 종류 「보충」 + 근거 글) · **지어내기 금지**(근거 없는 효과 · 고민 연결 0) · 케이스 코드 바꾸지 않음 · 원칙은 바꾸지 않는다.

## 구멍(품질 측정에서 나옴)
1. **입꼬리주름(CON-015) @입꼬리 → 명동점 0 묶음** — 명동점에 입꼬리보톡스(CAS-006 · 입꼬리) · 필러 진료항목이 있는데 고민 입꼬리주름과 안 이어짐. 손님 「입꼬리 주름이 고민」 → 「짚어 드리기 어려워요」 원인.
2. **팔자주름(CON-009) @팔자 → 필러 없음** — 목록이 기기 · 볼뉴머 · 스킨부스터만. 명동점 필러 진료항목(풀페이스필러 등 매핑 JSON 에서 확인) 케이스 ↔ 팔자주름 연결 · 부위 확인.
3. **효과 피부 타이트닝(EFF-021) → 볼뉴머 · 써마지FLX · 아이써마지 3 개뿐** — 소프웨이브 · 울쎄라피 프라임(그리고 같은 성격 기기 — 슈링크 · 온다 · 티타늄 등 명동점 매핑 케이스) outcome 에 타이트닝이 없음.

## 할 일
1. 세 구멍마다 **까닭**(연결이 원장에 없음 / 있는데 silver 에서 빠짐 / 다른 이름 고민 · 효과에 붙음 등)을 원천(bronze · 원장 문장 · silver 줄)으로 밝힌다.
2. 같은 꼴 **전수**: 셋만 고치지 마라 — 명동점 매핑 케이스 전부에 대해 (a) 그 케이스 부위에 맞는 부위 고민(주름 · 처짐 · 볼륨 계열)이 비었나 (b) 같은 시술 계열끼리 outcome(타이트닝 · 리프팅 · 주름 개선 등)이 들쭉날쭉한가 를 표로 센다. 근거로 채울 수 있는 것과 사람 판단(50 줄 안쪽 · 추천 붙여)을 나눈다.
3. 근거 있는 것은 silver 에 반영(앞 방식 그대로 · source_ref · 근거 종류) → gold 빌드 → gold-check PASS. 사람 판단 줄은 반영하지 말고 리포트에.
4. 바뀐 뒤 셋의 명동점 묶음 목록 전 → 후(허브 관계 기준 · 매핑 JSON 으로 묶음 이름).

## 산출
`$W/data-gap3-report.md`: 까닭 표 · 전수 표(꼴 × 수) · 반영 줄 수 · 사람 판단 표(추천) · gold_hash · aux_hash 전 → 후 · gold-check 결과 · 셋 전 → 후 목록 · 코디가 할 것(18105 새 gold 재기동 · 매핑 JSON 다시 만들 필요 여부).

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_442687ca-246d-497c-a2a6-1cd227251952 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "data 완료: 허브 구멍 3" --body "까닭 / 전수 꼴 수 · 반영 줄 / 사람 판단 수 / gold_hash"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] 허브 구멍 3 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] data-gap3: <질문>" --enter`
