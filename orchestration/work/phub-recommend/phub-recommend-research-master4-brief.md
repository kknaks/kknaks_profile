# [researcher] 제품 원장 4차 — 허가 미확인 148 · 웹 미조사 25 · 신규 현장 기기 끝까지

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
사용자 지시(10-27): **오늘 골드까지 간다. 한도 때문에 멈추지 않는다.**

## 입력
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json`(v3) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.md` · 3차 스크립트/캐시 `/tmp/phub-master/`(있으면 재사용)
- 게이트 페이지 분류 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-match-build.py` + `_RESUME.md` §2 「제품 게이트 축소」 행 — 이 기준으로 「허가 미확인」이 된 148(1차·2차·3차에서 이름 든 허가 없음 + 못 찾음)이 대상
- 웹 미조사 22 + 신규 3(3차 보고 미결) · 신규 현장 기기 35 중 식약처 후보 없는 17
- 도구: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지(`uv run python`). 키는 `.env`(값 출력 금지). **MFDS_DAILY_LIMIT 를 4000 으로 올려 두었다** — 이번 회차 2,500회 이내

## 방법
1. 대상마다 **웹 검색으로 정식 브랜드명 · 영문명 · 제조사 · 국내 수입사**를 찾는다(제조사 · 수입사 공식 사이트 우선, 출처 URL 필수). 이 세션의 웹 검색 한도에 닿으면 그때까지의 결과로 진행하고 남은 목록을 보고한다
2. 찾은 이름 · 업체로 식약처 재조회(의료기기 TYPE_NAME/ENTRPS · 의약품 item_name/entp_name)
3. 판정은 3차와 같은 규칙: 근거가 웹이어도 **공식명에 이름이 들고 업체가 같으면 auto**(게이트 축소 규칙) · 이름 든 제품 여럿 = 라인 · 이름 맞고 업체 다름 = candidate(직접 확인) · 없으면 unknown 유지
4. 웹으로도 정체를 못 찾은 것은 「무엇인지 한 줄」 + 「병원 자체 메뉴명/화장품/단종 추정」 등 이유를 남긴다

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json` **v4**(summary 에 3차 → 4차 변화 · 호출 수 · 웹 검색 수) · `.md` 갱신(맨 위 사람이 읽는 표: 4차에서 새로 찾은 것 · 끝까지 못 찾은 것과 이유)
- 키 · 캐시 원문 · 업체 주소 금지. 다른 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 제품 원장 4차" \
  --body "결과 수치 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 제품 원장 4차. 상세는 인박스." --enter
```
