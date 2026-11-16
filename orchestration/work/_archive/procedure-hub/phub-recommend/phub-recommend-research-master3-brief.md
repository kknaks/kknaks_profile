# [researcher] 제품 원장 초안 3차 — 현장 기기 사진 · Hub 영문명 · 웹 확인

너는 `product-master-draft.json` 을 만든 researcher 다. 같은 스크립트 · 캐시(`/tmp/phub-master/`) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지를 쓴다.

## 사용자 지시(2026-10-27)

1. **현장 기기 사진으로 모델 확인** — `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-reference-image/device-photos/시술기기_이미지_정리/` (`1_더데이랩스_사용중` 76장 = 실제 병원에서 지금 쓰는 기기 · `2_샘플_우스킨_사용중지` 33장). 목록 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-reference-image/device-inventory.csv`. **사진을 직접 열어(Read)** 로고 · 모델명 · 제조사 표기를 읽는다. 파일명은 후보일 뿐 — 사진에서 읽은 글자를 근거로 적는다(읽히지 않으면 「사진 판독 불가」)
2. **Hub 자체 영문명** — stg `GET /procedure-hub/api/v1/terminology/matrix` · `/glossary/matrix` 를 각 1회 받아(`/tmp/phub-master/` 에 저장) 원장 이름 ↔ 영문명 쌍을 쓴다. 이 영문명은 **원천 근거가 있는 검색어**(guessed: false)
3. 1 · 2 로 얻은 제조사 · 모델 · 영문명으로 **식약처 재조회** — 이번 호출 300회 이내(오늘 누적 상한 1000, KST)
4. 그래도 못 찾은 것은 **웹 검색**(WebSearch · WebFetch)으로 제조사 · 국내 수입사 · 정식 영문명을 찾는다 — 제조사 공식 사이트 · 국내 수입사 사이트 우선, **출처 URL 필수**. 웹에서 얻은 이름으로 식약처를 다시 조회한다(같은 호출 상한 안에서)
5. **원장에 없는 현장 기기**(사용중 76 중 원장 제품과 안 이어지는 것 — 코디 셈 43, 「써마지 ↔ 써마지FLX」 같은 이름 차이는 이어 준다)는 「원장 신규 후보」로 따로 모은다

## 규칙

- 사진 판독 · 웹 · 추측으로 찾은 식약처 허가는 **auto 금지 — 전부 candidate**. 근거 종류를 후보마다 표시(`via`: photo · hub_en · web · guess · company_list) + 사진 경로 · URL
- 자동 확정 규칙 A(`_RESUME` §2: 추측 아닌 이름 포함 제품 그룹 하나 + 업체 일치)는 hub_en 근거에도 적용해도 된다(hub_en 은 원천 근거)
- 같은 성분 · 함량만 다른 허가는 한 제품(+ 규격) — `_RESUME` §2
- 키 · 캐시 원문 · 사진 파일 자체를 산출물에 넣지 않는다(경로만). 다른 파일 수정 금지

## 산출물

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.json` **v3**(summary 에 2차 → 3차 변화 · via 별 수 · 호출 수) · 각 product 에 `in_use_at_clinic`(사진 photo_id) 표시
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-master-draft.md` 갱신 — 맨 위: ① 현장 사용 76대 표(사진 판독 결과 · 원장 제품 · 식약처 허가) ② 원장 신규 후보 표 ③ 시술군별 원장 → 식약처 표. 사람이 바로 읽게, 기술 용어는 아래로

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 제품 원장 초안 3차" \
  --body "사진 판독 수 / 찾은 수 변화(via 별) / 신규 후보 수 / 호출 수 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 제품 원장 초안 3차. 상세는 인박스." --enter
```
