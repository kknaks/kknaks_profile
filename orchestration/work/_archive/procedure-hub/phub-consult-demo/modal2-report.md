# 모달 효과 · 부작용 정리 리포트 (app 워커 · 2026-11-22)

발주 `task_5a00e2a0b9dc` · `ctx_4e634df7703a` · 사용자 결정 11-22 · 허브 부작용 분류(나) 뒤. 커밋 0 · 서브에이전트 0 · 18105(pid 48013) · 18222(pid 3822) 손 안 댐.

실물 허브: 코디 답대로 **빈 포트 18106 에 새 gold `c02d3ae8…`(aux `60788233…` · 작업 사본 `silver-model/gold`)** 로 따로 띄워 썼다(앱 18294 의 `HUB_REST_URL` 만 18106). 끝나고 둘 다 껐다. 매핑 JSON 은 지금 두 경로 sha `27f37eaf…`(허브 워커가 meta 를 새 gold 로 다시 만든 것 · sites 92 그대로).

## 1. 바뀐 것

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/modal.py` | `effects()` · `sides()` · `side_groups()` — 아래 규칙 · 장부용 셈 `pm.counts{effect_rows, effect_before, effect_after, side_rows, side_before, side_after}`. `course` · `side_other`(LLM 블록 재료 — 계열 줄 포함)는 그대로 |
| `templates/partials/modal_body.html` | 효과: `이름 — 칸 · 칸`. 부작용: 분류 묶음 `div.cs-pm__sgrp--{urgent\|caution\|temporary\|none}`(`data-class` = 허브 원문) · 묶음 머리 slot `pm-side-<key>` · 「바로 병원」 경고 `div.cs-pm__alert`(머리 slot `pm-alert-head` + 원문 줄). 칸마다 `span.cs-pm__f[data-f]` + 칸 이름 slot `pm-f-<칸>`. **slot 은 모두 빈칸으로 시작**(시안에 없는 글 · `ui_text.json` 0 줄 더함) |
| `static/consult.css` | 위급 묶음 = 빨간 테두리 · 연한 빨강 바탕 · 이름 빨강(맨 위) · 경고 줄 = 왼쪽 빨간 선 · 칸 사이 ` · ` · 이름 뒤 ` — `(CSS 꾸밈 — 글자 0) · 빈 slot 숨김 |
| `tests/test_v05_modal.py` | md1 단언을 이름 합침으로 고침 · 새 시험 둘(정리 규칙 · 화면 꼴) |

### 정리 규칙(사용자 결정 1 ~ 5)

1. **계열(modality)에서 물려받은 줄은 뺀다.** 판단 = `layer.holder.holder_table == "modality"`. 케이스 자기 · 시술 물려받음 줄만 남는다. LLM 블록 · 0.4 재료 · `course` · `side_other` 는 그대로다.
2. **같은 이름은 하나로 합친다**(효과 = `effect_name` · 부작용 = `adverse_name`). 칸 값은 원문을 모아 같은 값은 한 번만 쓴다. 코드는 `data-codes` 에 모두 남긴다.
3. **부작용 묶음** = 허브 `severity_class`. 순서는 위급 → 주의 → 일시적 → 빈칸이다. 한 이름에 분류가 여럿이면 가장 무거운 것을 쓴다. 빈 묶음은 그리지 않는다.
   - 3b. **「이럴 땐 바로 병원」** = `guidance_alerts` 가 true 인 줄 원문이다. 분류와 별도로 각 부작용 아래 경고 칸에 둔다(대처 줄과 겹치면 경고에만).
4. **부작용 칸**(원문을 이음 · 값 없으면 비움): 빈도(`freq_grade_text` · `freq_value_text`) · 심한 정도(`severity_text`) · 언제(`onset_text`) · 얼마나(`duration_text`) · 대처(`guidance_texts` 가운데 **kind 「관리」 줄**).
   - **판단 한 줄(보고):** 「경고 기준」 · 「모니터링」 · 「예방」 줄은 모달 대처에서 뺐다. 실측으로 이 줄들은 관찰 기준(「예상보다 큰 부종」 · 「부종 피크 Day 2」 · 「아스피린 피하기」)이다. 대처로 이으면 「부종 — 1-2일 · 예상보다 큰 부종 · 비대칭 부종 …」 처럼 읽힌다. 경고 기준 가운데 허브가 alert 로 표지한 줄은 3b 경고로 나온다. 나머지는 LLM 재료에 그대로 있다. 바꾸려면 `modal.CARE_KINDS` 한 줄이다.
5. **효과 칸**: 언제부터(`onset_text`) · 최대(`peak_text`) · 얼마나(`duration_text`) 원문. `note` 는 모달 칸이 아니다(빼고 장부 값에만 남김).

## 2. 줄 수 전 → 후(새 gold c02d3ae8 · 허브 18106)

「전」 = 옛 모달(코드마다 한 줄 · 계열 줄 포함). 「후」 = 정리 뒤.

| 진료항목 | 효과 행 | 효과 전 → 후 | 부작용 행 | 부작용 전 → 후 | 묶음(위급 · 주의 · 일시적) | 경고 칸 |
|---|---:|---|---:|---|---|---:|
| 입꼬리보톡스 제오민 `26-JUREK-ZOMN`(CAS-006) | 13 | **11 → 5** | 63 | **41 → 19** | 3 · 4 · 12 | 0 |
| 얼굴필러 쥬비덤 `26-PPSFL-JVD-1CC`(CAS-1046) | 20 | **7 → 5** | 59 | **37 → 25** | 7 · 10 · 8 | 7 부작용(경고 줄 10) |
| 울쎄라피 프라임 300샷 `26-USPP-300SHOT`(CAS-3046) | 11 | **9 → 2** | 37 | **25 → 6** | 1 · 0 · 5 | 0 |

표본(쥬비덤 · 화면 그대로):
- 효과:
  - 「볼륨 회복 — 즉시 · 즉각적 · 6-18개월 · 6-18개월 지속」
  - 「주름 개선 — 즉시 · 6-18개월」
  - 「턱선 정리」(칸 값 없음 → 이름만)
- 위급 묶음(맨 위 · 빨간 상자): 「혈관 폐색 — 드물지만 · 응급 히알루로니다제 처치 필요」 · 시야 장애 · 아나필락시스 · 피부 괴사 · 감염 · 농양 · 실명.
- 주의 묶음: 「백색 변화」 + 경고 「** 혈관폐색 (blanching/하얗게 변함) -- 골든타임 Day 0-1 **」 · 「심한 통증 + 피부 창백/청색 변화」.
- 일시적 묶음: 「부종 — 1-2일 · 1-3일」 · 「통증 — ★★☆☆☆」 + 경고 「비정상적으로 심한 통증 (통증 스케일 7 이상)」.

## 3. 스크린숏(`$W/e2e-shots/` · 1440 × 900 · 페이지 오류 0)

| 파일 | 무엇 |
|---|---|
| `modal2-botox-xeomin-effect.png` · `modal2-botox-xeomin-side.png` | 입꼬리보톡스 제오민 — 효과 5 · 부작용 19(위급 신경 손상 · 근육 마비 · 호흡곤란 맨 위) |
| `modal2-filler-juvederm-effect.png` · `modal2-filler-juvederm-side.png` | 얼굴필러 쥬비덤 — 효과 5 · 부작용 25 · 「바로 병원」 경고 칸 7 |
| `modal2-ulthera-effect.png` · `modal2-ulthera-side.png` | 울쎄라피 프라임 — 효과 2 · 부작용 6(위급 화상) |

경고 칸 머리 · 묶음 머리 · 칸 이름은 slot 이라 지금은 빈칸이다. 위급 묶음은 빨간 상자로, 경고 줄은 빨간 선으로 보인다.

## 4. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_modal.py` | **11 passed** |
| 위 + v05 전부 + 0.4 관련(T17 포함 — 템플릿 · 코드 한글 0) | **293 passed · 1 skipped** |
| `ruff check clinic_chat/consult/` + 손댄 시험 | 통과 |

새 시험:
- `test_tidy_merge_drop_modality_classes_alerts`:
  - 계열 줄 뺌 · 멍 둘 → 하나.
  - 칸 = 빈도 · 얼마나(같은 값 한 번) · 대처(관리만).
  - 예방 줄 0 · 경고 = alert 줄.
  - 값 없는 칸 = 빔.
  - 묶음 위급 → 일시적 → 빈칸 · 빈 묶음 뺌.
- `test_tidy_markup_groups_and_alert`(가짜 허브 · 모달 조각):
  - 위급 묶음이 일시적보다 위 · 계열 줄 0.
  - slot `pm-side-urgent` · 경고 칸 꼴 · 머리 slot `pm-alert-head`.

## 5. 남은 것

| # | 무엇 |
|---|---|
| R1 | slot 문구(`pm-side-urgent` · `pm-side-caution` · `pm-side-temporary` · `pm-side-none` · `pm-alert-head` · `pm-f-freq` · `pm-f-severity` · `pm-f-onset` · `pm-f-duration` · `pm-f-care` · `pm-f-peak`)는 사용자 · 디자인 확인 대상이다. 지금은 빈칸이고, 값을 넣으면 그대로 보인다 |
| R2 | 대처로 보일 kind = 「관리」 만(§1-4 판단) — 사용자 확인 대상 |
| R3 | 원문 칸 값이 겹쳐 보이는 경우가 있다(「6-18개월 · 6-18개월 지속」 · 「즉시 · 즉각적」). 원문이 달라 둘 다 둔다. 합치려면 허브 쪽 정리가 필요하다 |
| R4 | 18105 는 아직 옛 gold(caa03560)다. 18222 를 새 gold 로 보려면 코디가 18105 를 다시 띄워야 한다(`adverse-class2-report.md` §9). 옛 gold 에서는 `severity_class` 가 없어 모든 부작용이 「빈칸」 묶음 하나로 나온다(오류 아님) |
