# [researcher] 데모 연결 ↔ 운영 연결이 다르게 동작하는 자리 전수조사

너는 **day `researcher` 워커**다. 먼저 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/roles/day/researcher/role.md` (+ 같은 폴더 문서).

**read-only.** 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md`. 레포 수정 · 커밋 · KOS 호출 · DB 접속 금지.

## 배경
KOS 데모 지점과 실제 병원은 **같은 API 에 테넌트만 다르다**(사용자 2026-11-09). 그런데 DAY 코드에는 「데모 연결이면 A · 운영 연결이면 B」로 갈리는 자리가 있다(예: `backend/day/emr/kos/writes.py` `TRIAL_STEPS` · 설정 `KOS_TRIAL_WRITES_ON_LIVE`). 사용자는 이 차이를 없애려 한다. 그 전에 **갈리는 자리를 전부** 찾는다.

## 대상
- 코드: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` (origin/dev 와 같음 · backend · deploy · scripts · tests)
- 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/` (SPEC-000~002 · 40-architecture · 10-decision)

## 찾는 법 — 목록이 아니라 전수조사
`is_demo` · `demo` · `trial` · `TRIAL` · `ON_LIVE` · `live` · `APP_ENV` · `not_supported` · `WriteNotSupported` 를 **grep 으로 전부** 세고, 걸린 자리마다 호출하는 쪽까지 따라간다. 키워드에 안 걸리는 갈림(예: 연결 종류로 분기하는 조건 · 설정 기본값)도 찾아라.

## 각 자리마다 적을 것(표)
| # | 파일:줄 | 무엇이 갈리나(데모일 때 / 운영일 때) | 갈리는 이유(코드 주석 · SPEC 절 · 결정 D/W 번호) | 성격 |
성격은 셋 중 하나:
- **(가) 확인 안 된 KOS 쓰기를 막는 안전장치** — API 차이 아님, 우리 정책
- **(나) 환경 격리** — 예: `APP_ENV=dev` 서버는 데모 연결만 동기화 · 로그인 후보(dev 가 실제 병원을 건드리지 않게). 데모/운영 연결 차이가 아니라 dev/prod 서버 차이
- **(다) 그 밖** — 설명

(가) 는 HAR 로 확인됐는지 · 데모 실물로 확인됐는지(근거 있으면 적고, 없으면 「확인 안 됨」)도 적는다. 이미 아는 것: 시작 취소 `PROCEDURE_WAITING` 은 사용자가 2026-11-09 데모에서 정상 동작 확인.

## 정리
- 끝에 (가) 만 모은 표: 동작 · KOS 경로 · 확인 상태
- 테스트 중 데모/운영 갈림을 단언하는 테스트 파일:줄 목록(없애면 같이 바뀔 것)
- 스펙에서 데모/운영을 나눠 적은 절 목록
- 결정하지 마라. 「정할 것」으로 모은다

## 완료 보고
끝나면 두 명령을 모두:
```bash
orca orchestration send --to term_b915fb18-742f-4779-962c-79848020b8d5 --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: <한 줄>" --body "<요약 · 자리 수 · (가)/(나)/(다) 수>"
orca terminal send --terminal term_b915fb18-742f-4779-962c-79848020b8d5 --text "[worker_done] researcher 완료 — <한 줄>. 상세는 인박스." --enter
```
핸들은 dispatch preamble 값이 맞다. 다르면 preamble 쪽으로만.
