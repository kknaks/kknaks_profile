---
type: spec
id: SPEC-002
title: "2층 판정 · 분석 — 언어 · 예약 단계 · 국적 · LLM 라벨 · 통계 · 산출물"
version: 0.3.0
status: accepted
product: consult-analysis
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/consult-analysis
  - doc/spec
  - status/accepted
links:
  baselines:
    - "[[baseline-002-conversion-language|BASE-002]]"
  decisions:
    - "[[decision-002-layer2-analysis|DEC-002]]"
    - "[[decision-001-two-layers|DEC-001]]"
  specs:
    - "[[spec-001-layer1-schema|SPEC-001]]"
  works:
    - "[[work-002-layer2-analysis|WORK-002]]"
  releases: []
  related: []
sources:
  - para/projects/summer-star/consult-analysis/10-decision/decision-002-layer2-analysis.md (D-01 ~ D-13 · accepted)
  - para/projects/summer-star/consult-analysis/data/layer1.sqlite (1층 DB · gitignore — 2026-11-16 planner 가 읽기 전용으로 규칙을 돌려 봄. 이 문서의 「실측」은 전부 이 값이다)
---

# 2층 판정 · 분석 — 계약

> etl 워커가 그대로 구현하는 계약이다. 1층(SPEC-001)은 고치지 않는다. 2층은 같은 SQLite 파일에 `l2_` 테이블로 붙는다(D-01).
> `D-NN` 은 DEC-002, `DEC-001 D-NN` 은 따로 적는다. IG = `instagram` · FB = `facebook`.
> 이 레포는 PUBLIC 이다 — 이 문서 · 스크립트 · 보고서 · 집계 JSON 에는 건수 · 비율 · 우리 계정 상용 문구의 머리 몇 글자만 있다.
> 고객 본문 · 이름 · 계정명은 DB 와 `data/`(gitignore) 밖으로 나가지 않는다.

## 변경 이력

| 버전 | 날짜 | 내용 |
|---|---|---|
| 0.1.0 | 2026-11-16 | 처음 씀 — 2층 테이블 6 · 예약 단계 규칙(실측 성공 92방 · 사람 확인 21건) · 언어 규칙 · LLM 라벨 계약 · 통계 정의 · 산출물 · 열린 것 OQ-201 ~ 205 |
| 0.3.0 | 2026-11-16 | §5 LLM 입력에서 **예약표 메시지를 뺀다** — 우리 예약표 발송(`form_labels ≥ 3`) · 고객 예약표 회신(`form_filled ≥ 2`). 예약표의 통역 · 날짜 칸이 `interpreter` · `schedule` 주제로 읽혀 성공 방 주제가 부풀었다(etl 점검: 성공 방 통역 89 · 일정 93 · 위치 75 · 부작용 36 전부 근거에 예약표). `topics` 는 **고객이 묻거나 말한 것만**. 프롬프트 `llm-0.3.0` · 전체 다시(`--reset`) |
| 0.2.2 | 2026-11-16 | §6 이모지에서 **예약표 칸이 든 고객 메시지(`form_labels ≥ 1`)를 뺀다** · 사진은 예약표 회신 앞 · 뒤로 나눠서도 낸다 — 회신한 예약표의 ★ · 📝 양식 기호가 이모지로 세여 성공 방 이모지가 94.6% 로 부풀었다(빼면 50.5%) · 코디 검증 |
| 0.2.1 | 2026-11-16 | OQ-206 닫음(B · D-22) — `fat_dissolving`(消脂針) · `tune`(Tune) 을 목록 · 별칭 표에 더함. 재시험은 이 목록으로 한 번 · 코디 |
| 0.2.0 | 2026-11-16 | DEC-002 D-14 · D-19 ~ D-21 반영 — §5 시술 목록에 다섯 값(`rejuran` · `mole_wart_removal` · `acne_scar` · `pore_texture` · `eye_area`) · 별칭 표(우리 메시지 출처 48개) · 새 칸 `procedures_other`(§1 · §5 · DB 만) · 모델 haiku · 표본 재시험 뒤 전체 · §2.3 · §2.4 에 etl 실측(큐 15)과 사람 판정(성공 93) · §2.5 `handoff_mentioned` 낱말 경계 규칙(IG 12 · FB 17) · §8 OQ-201 ~ 205 닫힘 표시 · OQ-206 |

## 1. 테이블 — D-01 · D-02

공통 칸(모든 `l2_` 테이블): `judge` TEXT NOT NULL(`rule` \| `llm` \| `human` · CHECK) · `evidence_message_id` INTEGER NULL FK → `message`(근거가 여러 건이면 대표 1건 · 근거 메시지가 없는 판정만 NULL — §1 각 표에 적음) · `version` TEXT NOT NULL(판정 버전 — 규칙은 `rule-0.1.0` · LLM 은 `llm-<프롬프트 버전>`).

| 테이블 | 행 단위 | 행 수(실측 기준) | 칸(공통 칸 외) |
|---|---|---|---|
| `l2_message` | 메시지 1건 | 28,706 = `message` | `message_id` PK FK · `lang`(§3 · 우리 메시지도 채움) · `n_letters` · `han_trad` · `han_simp` · `n_emoji` · `auto_kind`(§2.1 · 우리 메시지만 · 아니면 NULL) · `form_labels` · `form_filled`(§2.3 — 그 메시지에 나온 칸 수 · 채운 칸 수) |
| `l2_conversation_lang` | 방 1개 | 1,916 | `conversation_id` PK FK · `lang` · `top_share`(REAL) · `is_mixed` · `n_letters` |
| `l2_booking_stage` | 방 1개 | 1,916 | `conversation_id` PK FK · `stage`(`inquiry` \| `form_sent` \| `form_filled`) · `rule_stage`(사람이 덮어도 규칙 값은 남김) · `form_source`(`staff` \| `flow` \| `auto` \| `none`) · `sent_message_id` · `filled_message_id` · `filled_fields`(채운 칸 수 최대) · `got_auto_reply`(0/1) · `handoff_mentioned`(0/1 · §2.5) |
| `l2_nationality` | 방 1개 | 1,916 | `conversation_id` PK FK · `nationality`(코드 · 모르면 NULL) · `source`(`form` \| `self` \| `lang` \| `none`) · `raw_value`(예약표에 적힌 그대로 · DB 안에만) · `llm_confidence` NULL |
| `l2_llm_label` | 방 1개(고객 본문이 있는 방만) | 1,883 (IG 505 · FB 1,378) | `conversation_id` PK FK · `topics`(JSON 배열) · `procedures`(JSON 배열) · `procedures_other`(JSON 배열 · 목록 밖 시술의 원래 이름 · DB 만 — §5) · `nationality_mention` · `staff_confirmed`(0/1) · `confidence`(REAL) · `model` · `evidence_message_ids`(JSON 배열) · `input_truncated`(0/1) |
| `l2_review_queue` | 사람 확인 1건 | 50 안쪽(실측 21) | `queue_id` PK · `conversation_id` FK · `reason`(§2.4 의 E-1 ~ E-3) · `rule_stage` · `human_stage` NULL · `decided_at` NULL |

- `evidence_message_id`: `l2_message` 는 자기 `message_id` · `l2_conversation_lang` 은 그 언어 글자가 가장 많은 고객 메시지 · `l2_booking_stage` 는 `filled_message_id` → 없으면 `sent_message_id` → 둘 다 없으면(`inquiry`) 방의 첫 메시지 · `l2_nationality` 는 값이 나온 메시지(`source = 'lang'` · `'none'` 은 `l2_conversation_lang` 의 근거와 같게 · 고객 메시지가 없는 방만 NULL).
- 1층 테이블에는 칸을 더하지 않는다. `l2_` 테이블은 1층 id 만 가리킨다.

## 2. 예약 단계 — D-03 · D-04 · D-05 · DEC-001 D-06 · D-07

### 2.1 자동응답 — `l2_message.auto_kind` (우리 메시지 · 실측)

| 값 | 규칙(복원된 `content`) | 메시지 IG / FB | 방 IG / FB |
|---|---|---|---|
| `off_hours_form` | 「非營業時間」이 들어 있음 — 영업시간 외 안내 + **빈 예약표** | 179 / 150 | 150 / 125 |
| `away` | 「感謝您的訊息，我目前不在線」으로 시작 | 188 / 350 | 148 / 268 |
| `off_hours_prefix` | 「您好，小編將於工作日」로 시작 — 영업시간 외 머리말이 붙은 상용 답 | 22 / 165 | 20 / 111 |
| `system` | 「잠재 고객 단계를」 · 「거의 완료되었습니다」 · 「請點按我們提供的其中一個選項」 · 「Customer님이」 로 시작 — 플랫폼이 넣은 알림 | 0 / 456 | 0 / 354 |
| `flow` | 위가 아니고 · 같은 채널에서 **같은 본문이 10번 이상** 나오고 · 바로 앞 메시지와의 간격이 **3초 이하** — 즉시응답 흐름(단추 · 키워드) | etl 이 셈 | — |

- 위에서 아래 순서로 처음 맞는 값 하나. 어느 것도 아니면 NULL(사람이 보낸 것으로 본다).
- 자동응답을 하나라도 받은 방(`system` · `flow` 제외): IG 300 · FB 는 etl 이 셈 → `l2_booking_stage.got_auto_reply`.
- 근거: 반복 문구별 응답 간격 실측 — `flow` 꼴 문구는 건수의 90% 이상이 3초 안, 사람이 고른 상용 답은 중앙값 4초 이상.

### 2.2 예약표 칸 사전 — D-04 (실측 · 우리 예약표 문구에서 뽑음)

칸 이름은 **긴 것부터** 찾는다. 판(版)이 달라도 칸은 같다 — 판마다 사전을 따로 두지 않는다.

| 칸 | 칸 이름(부분 일치) |
|---|---|
| `date` | 希望預約日期與時間 · 預約日期與時間 · 來院日期時間 · 預約日期 · 來院日期 |
| `name` | 護照英文姓名 · 姓名 · Name · 이름 |
| `birth` | 西元出生年月日 · 西元生日年月日 · 出生年月日 · 生日年月日 · 生日 · Birth · 생년월일 |
| `nationality` | 國籍 · 国籍 · Nationality · 국적 |
| `gender` | 性別 · 性别 · Gender · 성별 |
| `procedure` | 希望施作項目 · 施作項目 · 預算 |
| `interpreter` | 是否需要翻譯人員 · 是否需要翻譯 · 是否需要口譯員 · 翻譯 · 口譯 |
| `director` | 是否需要院長商談 · 院長商談 |
| `phone` | 聯絡電話 · 聯繫電話 · 聯絡方式 · 聯繫方式 · 電話 |
| `email` | Email · email · E-mail |
| `medical` | 施作經歷 · 過敏 · 蟹足腫 · 藥物 · 懷孕 · 相關施作 · 相關施術 |

상담사 예약표의 판 — 머리 문구(실측 · 공백을 하나로 줄인 머리 8글자 기준 · 메시지 수):

| 머리 | IG | FB |
|---|---|---|
| 「★ 預約資訊 希…」 | 39 | 60 |
| 「為了提供更精準的…」 | 0 | 100 |
| 「沒問題！為了能更…」 | 7 | 29 |
| 「★ 預約資訊 姓…」 | 2 | 21 |
| 「📝 預約表格 預…」 | 4 | 9 |
| 「預約表格 ★ 來…」 | 5 | 4 |
| 「★ 來院日期時間…」 · 「★ 到院預約資料…」 | 3 | 6 |

FB 예약표는 IG 와 문구가 같은 판을 쓰고, 「為了提供…」(의료 이력 칸이 붙은 판)만 FB 에만 있다.

### 2.3 판정 규칙

1. **칸 세기**(메시지 1건): 사전의 칸 이름이 나온 자리를 전부 찾는다. 칸 값 = 그 이름 끝에서 **다음 칸 이름 시작**(마지막 칸은 그 줄 끝)까지.
   값에서 괄호 안내문(`（…）` · `(…)` 40자 이내) · 구역 머리(`★ …` · `📝 …`) · 앞의 쌍점과 공백을 지운 뒤 글자(숫자 · 라틴 · 한자 · 가나 · 한글)가 하나라도 남으면 **채운 칸**. `form_labels` = 나온 칸 종류 수 · `form_filled` = 채운 칸 종류 수.
2. **예약표 발송**(우리 메시지): `form_labels ≥ 3` 인 메시지.
   - `auto_kind` 가 `off_hours_form` · `off_hours_prefix` → 자동응답의 빈 표. **`form_sent` 로 세지 않는다**(DEC-001 D-07). `form_source = 'auto'` 후보일 뿐.
   - `auto_kind = 'flow'` → `form_source = 'flow'`(OQ-205 — 권장대로면 `form_sent` 로 센다).
   - 그 밖 → `form_source = 'staff'`.
   - 방의 `form_source` 는 `staff` > `flow` > `auto` > `none` 순으로 가장 앞의 것. `sent_message_id` = 그 종류의 첫 메시지.
3. **`form_filled`**(= 예약 성공 · D-04): 방의 **고객 메시지 중 `form_filled ≥ 2` 인 것이 하나라도** 있음. `filled_message_id` = 그중 채운 칸이 가장 많은 것(같으면 먼저 온 것). 어떤 표를 받았는지는 따지지 않는다(자동응답의 표를 채워도 성공).
4. **`form_sent`**: 3 이 아니고 · 방에 `staff` 또는 `flow` 예약표 발송이 있음.
5. **`inquiry`**: 그 밖 전부(고객 메시지가 없는 방 포함).

실측(2026-11-16 · planner 가 위 규칙을 1층 DB 에 돌린 값 · `flow` 포함):

| | IG | FB | 합 |
|---|---|---|---|
| 방 | 511 | 1,405 | 1,916 |
| `form_filled` | 40 | 52 | **92** |
| `form_sent` | 24 | 134 | 158 |
| `inquiry` | 447 | 1,219 | 1,666 |
| 예약표 발송 방 — `staff` / `flow` 만 | 60 / 0 | 152 / 27 | 212 / 27 |
| 자동응답 빈 표를 받은 방 | 150 | 136 | 286 |
| `form_filled` 의 표 출처 — `staff` · `flow` / `auto` 만 / 표 없음 | 36 / 4 / 0 | 45 / 5 / 2 | 81 / 9 / 2 |
| `form_filled` 중 `nationality` 칸을 채운 방 | 39 | 49 | 88 |
| 고객 메시지의 채운 칸 수 최대 — 0 / 1 / 2 ~ 3 / 4 이상 | 460 / 11 / 0 / 40 | 1,330 / 23 / 2 / 50 | 1,790 / 34 / 2 / 90 |

채운 칸 수는 0 ~ 1 과 4 이상으로 갈린다(2 ~ 3 은 2방) — 「2개 이상」 문턱이 실측과 맞는다.
etl 구현의 수가 이 표와 다르면 **규칙을 비틀어 맞추지 않는다** — 차이 나는 방 수와 이유(값 정리 방식)를 보고한다.

### 2.4 사람 확인 큐 — D-05 · D-19 (planner 실측 21건 · etl 실측 15건 · 50 안쪽)

| 사유 | 조건 | IG | FB |
|---|---|---|---|
| E-1 | 채운 칸 수 최대가 **1** 이고 · 방에 예약표가 있었다(`form_source ≠ 'none'`) | 3 | 12 |
| E-2 | 칸 이름 없이 예약표 뒤에 온 고객 메시지가 자료 꼴 — (생년월일 꼴 + 대문자 영문 이름) 또는 (날짜 꼴 + 대문자 영문 이름) 또는 (날짜 꼴 + 생년월일 꼴 · 200자 미만) · 채운 칸 최대 < 2 | 1 | 3 |
| E-3 | 채운 칸 수 최대가 **2 ~ 3**(규칙은 `form_filled` · 확인만) | 0 | 2 |

- **etl 실측(WP1 · WP2) = 15건** — E-1 12 · E-2 1 · E-3 2. 위 표(21)와의 차이 6건: 칸 값 정리(괄호 안내문 · 구역 머리 지우기) 해석이 달라 E-1 에서 FB 3방 · 자료 꼴 판정이 달라 E-2 에서 FB 3방이 빠졌다. 단계 · 자동응답 건수(§2.1 · §2.3 표)는 etl 실측과 같다. **기준은 etl 실측 15건**이다.
- **사람 판정(D-19)**: 15건 중 **3건이 `form_filled`** — 2건은 규칙도 `form_filled` 였고(E-3), 1건은 칸 이름 없이 자료를 보낸 방이라 규칙 `form_sent` 를 사람이 덮었다. 나머지 12건은 규칙 값 그대로. 판정 뒤 **`form_filled` 93**(규칙 92 + 1) · `form_sent` 157(158 − 1) · `inquiry` 1,666. 판정 파일은 `data/review_decisions.csv`(로컬).
- 큐가 **50건을 넘으면 멈추고 코디네이터에게 보고**한다(사유별 건수만). 조건을 스스로 좁히지 않는다.
- 채운 칸 1개인데 예약표가 없던 방(19)은 큐에 넣지 않는다 — 문장 속에 칸 낱말이 나온 것이다(`inquiry`).
- 사람 판정은 `l2_review_queue.human_stage` 에 적고 `l2_booking_stage.stage` 를 덮는다(`judge = 'human'` · `rule_stage` 는 그대로).
- 큐 파일(본문이 보여야 판정한다)은 `data/review_queue.csv` 에만 낸다 — gitignore · 레포 · 보고에 싣지 않는다.

### 2.5 다른 경로 · 확정 안내 — D-15 · D-16 · D-21 (실측)

- `handoff_mentioned = 1`: 예약표 회신이 없는 방 중 **우리 메시지가 다른 메신저(LINE · WhatsApp · WeChat · 카카오)를 언급한 방**. 규칙은 **낱말 경계 일치**(D-21) — 대소문자 무시 · 메신저 이름의 **앞뒤 글자가 라틴 글자가 아닐 때만** 센다(다른 낱말 속에 든 것 · 주소 속 글자는 세지 않는다). 실측(etl) **IG 12 · FB 17 = 29방**. 0.1.0 의 21 · 73 은 부분 일치 대략치였다. 단계는 바꾸지 않는다(D-15).
- 확정 안내 꼴(「預約完成」 류)은 규칙으로 잡으면 자동응답 문구 · 일반 안내와 섞인다(낱말 일치로 회신 없는 방의 20% 넘게 걸림 — 쓸 수 없다). → LLM 라벨의 `staff_confirmed` 로만 받는다.

## 3. 언어 — D-06 · D-13

**메시지**(`l2_message.lang` · URL 을 지운 `content` · 글자 = 유니코드 문자 종류로 셈):

| 순서 | 조건 | 값 |
|---|---|---|
| 1 | 글자가 없다(`content` NULL · 이모지 · 숫자뿐) | `none` |
| 2 | 한글이 가장 많다 | `ko` |
| 3 | 가나가 1자 이상이고 한자 + 가나가 가장 많다 | `ja` |
| 4 | 한자가 가장 많다 → OpenCC 로 가른다: `han_trad` = `t2s` 변환에서 바뀌는 글자 수 · `han_simp` = `s2t` 에서 바뀌는 글자 수 | `han_trad > han_simp` → `zh-Hant` · 반대 → `zh-Hans` · 같으면(공통 글자뿐) → `zh`(OQ-204) |
| 5 | 라틴 글자가 가장 많다 → 영어 기능어 목록(the · is · are · you · and · to · for · can · how · what · please · thanks · hi · hello 등 30개 안쪽 · 스크립트에 상수로)이 낱말로 1개 이상 | 있으면 `en` · 없으면 `other` |
| 6 | 그 밖(태국 문자 등) | `other` |

- 의존성: `opencc-python-reimplemented`(순수 파이썬) — `scripts/requirements-layer2.txt` 에 버전 고정(D-13).
- **방**(`l2_conversation_lang`): 고객 메시지의 `n_letters` 를 언어별로 더해 **가장 많은 언어**. `zh` 인 메시지의 글자는 그 방의 `zh-Hant` · `zh-Hans` 중 `han_trad` · `han_simp` 합이 큰 쪽에 붙인다(둘 다 0 이면 방도 `zh`).
  `top_share` = 그 언어 글자 수 ÷ 전체 글자 수 · `is_mixed` = `top_share < 0.8`. 고객 글자가 없는 방은 `none`.
- 실측(문자 종류만 · 번간 구분 전): 고객 글자가 가장 많은 문자 — 한자 IG 438 · FB 1,285 / 라틴 39 · 55 / 한글 17 · 26 / 가나 2 · 1 / 그 밖 2 · 8 / 글자 없음 13 · 30.
  라틴 방 94 중 영어 기능어가 잡히는 방 60 · 안 잡히는 방 34(→ `other`). 문자 종류 기준 섞인 방(`top_share < 0.8`) IG 105 · FB 92.
  번체 · 간체 건수는 OpenCC 가 planner 환경에 없어 세지 못했다 — etl 이 WP1 에서 센다.

## 4. 국적 — D-09 · DEC-001 D-08

| 순서 | `source` | 규칙 | `judge` |
|---|---|---|---|
| ① | `form` | `filled_message_id` 메시지의 `nationality` 칸 값(§2.3 의 칸 값) → `raw_value`. 대응표(스크립트 상수 — 台灣 · 臺灣 · Taiwan → `TW` · 香港 → `HK` 등 · 값 종류가 88건 안쪽이라 etl 이 distinct 를 보고 만든다 · 대응 못 하면 `other`)로 `nationality` | `rule` |
| ② | `self` | ① 이 없고 `l2_llm_label.nationality_mention` 이 있음 | `llm` |
| ③ | `lang` | ① ② 가 없음 — 방 언어로 추정: `zh-Hant` → `TW/HK` · `zh-Hans` → `CN` · `ko` → `KR` · `ja` → `JP` · 그 밖 → NULL(`source = 'none'`) | `rule` |

통계에서는 `source` 를 늘 같이 낸다 — ③ 은 국적이 아니라 언어권이다.

## 5. LLM 라벨 — D-07 · D-08

- **입력**(방 1개 = 호출 1번): 방의 메시지를 시간순으로 `[C]`(고객) · `[S]`(우리) 머리표와 본문만. 이름 · 계정명 · 시각 · 첨부 경로는 넣지 않는다. `auto_kind` 가 NULL 이 아닌 우리 메시지는 뺀다. 본문 합이 **6,000자**를 넘으면 앞 3,000자 + 뒤 3,000자(`input_truncated = 1`). 고객 본문이 없는 방은 부르지 않는다. **예약표 메시지도 뺀다**(0.3.0): 우리 메시지 중 `form_labels ≥ 3`(예약표 발송) · 고객 메시지 중 `form_filled ≥ 2`(예약표 회신). 지시문에 「`topics` 는 고객이 묻거나 말한 주제만 — 우리 안내 · 양식의 칸 이름은 주제가 아니다」를 넣는다.
- **출력**(JSON 하나 · 다른 글 없음):

```json
{"topics": ["procedure", "price"], "procedures": ["ulthera", "other"], "procedures_other": ["<시술 이름>"], "nationality_mention": null,
 "staff_confirmed": false, "confidence": 0.8, "evidence": [3, 7]}
```

| 칸 | 값 |
|---|---|
| `topics` | 0개 이상 — `procedure`(시술 문의) · `price`(가격 · 예산) · `schedule`(예약 · 일정) · `location`(위치 · 교통) · `interpreter`(통역 · 언어) · `result`(효과 · 후기 · 전후) · `safety`(부작용 · 회복 · 금기) · `promo`(이벤트 · 할인) · `other` |
| `procedures` | 0개 이상 — `ulthera` · `thermage` · `sofwave` · `onda` · `titanium` · `rf_microneedle` · `juvelook` · `botox` · `filler` · `skinbooster` · `laser` · `rejuran` · `mole_wart_removal` · `acne_scar` · `pore_texture` · `eye_area` · `fat_dissolving` · `tune` · `lifting_unspecified` · `other` — 20개(D-20 · D-22 · 표본에서 `other` 가 방 기준 57% 라 다섯 값을 더함). 별칭은 아래 표 |
| `procedures_other` | 0개 이상 — `procedures` 에 `other` 가 있을 때만 · 목록 밖 시술의 원래 이름(짧게). 없으면 `[]` |
| `nationality_mention` | 고객이 스스로 밝힌 국적 · 사는 곳의 코드(`TW` · `HK` · `CN` · `US` …) 또는 `null`. 추측 금지 |
| `staff_confirmed` | 우리가 날짜 · 시간을 넣어 예약을 확정해 준 말이 있으면 `true` |
| `confidence` | 0 ~ 1 |
| `evidence` | 판단 근거가 된 메시지의 입력 내 순번(1부터) → 스크립트가 `message_id` 로 바꿔 `evidence_message_ids` 에 |

시술 별칭 — 지시문에 넣는다(D-20). 전부 **우리 메시지**(1층 DB `is_owner = 1`)에 나오는 말이고, 괄호는 그 말이 나온 방 수다(2026-11-16 실측).

| 값 | 별칭 |
|---|---|
| `ulthera` | 美國音波(159) · 音波(527) · Ulthera(178) · Ultherapy(173) |
| `thermage` | 鳳凰電波(373) · 鳳凰(455) · 電波(390) · Thermage(143) · 熱瑪吉(7) |
| `ulthera` + `thermage` | 電音波(232) — 두 시술을 묶어 부르는 말이라 둘 다 낸다 |
| `sofwave` | 索夫波(425) · Sofwave(135) |
| `onda` | Onda(341) |
| `titanium` | 鈦提升(208) · 鈦(209) · Titanium(123) · Titan(123) |
| `rf_microneedle` | 黃金微針(263) · 微針(270) · Potenza(28) |
| `juvelook` | 喬雅露(222) · Juvelook(145) · 藍瓶(176) |
| `rejuran` | 麗珠蘭(167) · Rejuran(26) |
| `skinbooster` | 水光針(278) · 水光(385) · 光針(353) · Skinvive(114) |
| `botox` | 肉毒(495) · Xeomin(17) · Botox(1) |
| `filler` | 玻尿酸(239) · Belotero(2) · Restylane(1) · 瑞絲朗(1) |
| `laser` | 雷射(299) · 皮秒(9) |
| `acne_scar` | 痘疤(103) · 凹洞(86) |
| `pore_texture` | 毛孔(499) |
| `eye_area` | 眼周(138) · 眼下(13) · 黑眼圈(12) · 淚溝(12) · 眼袋(10) |
| `mole_wart_removal` | 痣(9) · 疣(2) |
| `fat_dissolving` | 消脂針(83방 · D-22) |
| `tune` | Tune(66방 · 기기 이름 그대로 · D-22) |

- 별칭 48개(묶음 말 1개 포함) · 값 17개. 별칭이 없는 값: `lifting_unspecified`(시술 이름 없이 리프팅 · 拉提만 물음) · `other`.
- 목록에 없는 시술은 `other` 를 내고 **원래 이름을 `procedures_other` 에 짧게**(시술 · 기기 이름만 · 20자 이내 · 문장 금지) 적는다. `procedures_other` 는 DB 에만 둔다 — 통계 · 집계 JSON · 보고서에는 내지 않는다(D-20).
- 우리 메시지에 자주 나오지만 목록에 대응 값이 없는 말(→ `other`): 消脂針(83) · Tune(66) · LDM(29) · 超聲刀(19) · 海芙(14) · 舒顏萃(14) · 除毛(13). 목록에 넣을지는 재시험의 `other` 비율을 보고 정한다(§8 OQ-206).

- JSON 이 깨지거나 목록 밖 값이면 1번 다시 부르고, 또 실패하면 그 방은 행을 만들지 않고 건수로 보고한다(조용히 `other` 로 채우지 않는다).
- **호출**: 로컬 CLI 를 `subprocess` 로 · 프롬프트는 표준 입력으로 · 도구 사용 끔 · 방 본문을 파일로 쓰지 않는다. 결과는 DB 에만(D-08). CLI = `claude -p` · 모델 = **haiku**(D-14 · 모델 비교는 하지 않는다). 표본 30방 실측: 실패 0 · 방당 약 $0.0007.
- 순서: 표본 30방(단계 3종 × 채널 고르게 · 끝남 — `other` 방 기준 57%) → **표본 재시험**(넓힌 목록 · 별칭 표 · `procedures_other` 로 **같은 30방**을 `--reset` 뒤 다시 · `other` 가 든 방의 비율과 `procedures_other` 값 종류 수를 보고) → 코디 확인 → 전체 1,883방. 이미 행이 있는 방은 건너뛴다(이어 하기). 지시문이 바뀌었으니 `version` 의 프롬프트 버전을 올린다.

## 6. 통계 정의 — D-10 · D-11

분모는 **방**이다. 축 3개: 방 언어(`l2_conversation_lang.lang`) · 예약 결과(`form_filled` = 성공 / 그 밖 = 실패 · `form_sent` 는 따로도 냄) · 채널. 고객 메시지가 없는 방(IG 3 · FB 17)은 전환율 분모에서 빼고 건수만 적는다.

| 항목 | 계산 |
|---|---|
| 방 수 · 전환율 | 전환율 = `form_filled` 방 ÷ 고객 메시지가 있는 방. `form_sent` 이상 비율 · `form_sent → form_filled` 비율도 |
| 예약까지 턴 수 | 턴 = 발신자가 바뀔 때까지 이어진 메시지 묶음(`auto_kind` 가 있는 메시지는 뺌). 방의 첫 메시지 ~ `filled_message_id` 까지의 턴 수. 성공 방만 · 중앙값 · 사분위 |
| 예약까지 시간 | `filled_message_id` 의 `sent_at_ms` − 방의 첫 고객 메시지 `sent_at_ms`. 시간 단위 · 중앙값 · 사분위 |
| 방 전체 턴 · 메시지 수 | 고객 메시지 수 · 우리 메시지 수(자동응답 뺌) · 턴 수 — 중앙값 |
| 고객 메시지 길이 | 고객 메시지 `n_letters` 의 방별 중앙값 → 그 값의 중앙값. 예약표 회신 메시지(`form_filled ≥ 2`)는 뺀다 |
| 첫 메시지 형태 | 방의 첫 고객 메시지를 하나로: `photo`(사진 첨부) · `share`(공유) · `sticker_or_none`(글자 없음) · `short`(글자 10자 이하) · `question`(`?` · `？` · `嗎` · `呢` · 「請問」 포함) · `statement`(그 밖) — 위에서부터 처음 맞는 것 |
| 우리 첫 응답까지 시간 | 첫 고객 메시지 뒤 처음 나오는 **자동응답이 아닌** 우리 메시지까지. 분 단위 중앙값 · 「1시간 안」 비율 · 응답 없음 건수 |
| 문의 시각 | 첫 고객 메시지의 KST(`sent_at_ms` + 9시간) 시(0 ~ 23) · 요일 · 영업시간(평일 10 ~ 19시 KST — 자동응답 문구에 적힌 시간) 안 / 밖 |
| 이모지 | **예약표 칸이 든 고객 메시지(`form_labels ≥ 1`)는 뺀다**(0.2.2 — 양식 기호 ★ · 📝 가 섞인다). `n_emoji` = 유니코드 Emoji_Presentation · 확장 그림 문자 범위(U+1F300 ~ U+1FAFF · U+2600 ~ U+27BF) 글자 수. 고객 메시지에 1개 이상 쓴 방의 비율 · 메시지당 평균 |
| 사진 사용 | 고객 메시지에 `attachment.kind = 'photos'` 가 있는 방의 비율. 예약표 회신 뒤의 사진(여권 등일 수 있음)과 앞의 사진을 **나눠서도** 낸다(0.2.2) |
| 자동응답 받음 | `got_auto_reply = 1` 방의 비율 · 받은 방 / 안 받은 방의 전환율 |
| 문의 주제 · 시술 | `topics` · `procedures` 값별 방 수(한 방이 여러 값 — 합이 100% 를 넘는다고 적는다) · 값별 전환율. 분모는 라벨이 있는 방 |
| 국적 | `nationality` × `source` 별 방 수 |

- 모든 비율은 `{"n": 분자, "d": 분모, "pct": 소수 1자리}` 로 낸다. **분모가 10 미만이면 `"small": true`** — 보고서 · 차트에서 표시하고 비율로 말하지 않는다(D-11).
- 중앙값 · 사분위는 방 수 `n` 을 같이 낸다. 인과로 쓰지 않는다 — 「차이」로만.

## 7. 산출물 · 실행 — D-12 · D-13

| 스크립트(`scripts/`) | 일 | 인자 |
|---|---|---|
| `judge_layer2.py` | `l2_message` · `l2_conversation_lang` · `l2_booking_stage` · `l2_nationality` · `l2_review_queue` | `--db`(필수) · `--queue-out data/review_queue.csv` · `--decisions data/review_decisions.csv`(사람 판정 · 있으면 덮음) |
| `label_layer2_llm.py` | `l2_llm_label` | `--db` · `--cli` · `--model` · `--sample N` · `--reset`(있던 라벨을 지움 — 없으면 이어 하기) |
| `stats_layer2.py` | 집계 JSON | `--db` · `--out` |

- **다시 돌리면 2층만 새로**: `judge_layer2.py` 는 규칙 테이블 다섯을 지우고 다시 만든다(한 트랜잭션). 1층 테이블 · `l2_llm_label` 은 건드리지 않는다. `l2_llm_label` 이 있으면 `l2_nationality` ② 까지 채운다(없으면 ① ③ 만 — LLM 뒤에 한 번 더 돌린다).
- 표준 출력에는 건수만. 본문 · 이름 · `thread_path` 를 찍지 않는다.
- **집계 JSON** `para/projects/summer-star/consult-analysis/50-report/stats-001.json`(커밋함 · 건수 · 비율만 · 차트 페이지 입력):
  최상위 `meta`(생성 시각 · 판정 버전 · 방 수 · 라벨 방 수) · `stage`(채널별) · `by_lang` · `by_outcome` · `by_channel` · `lang_x_outcome` — 각 묶음 안에 §6 항목 이름을 키로.
  JSON 에는 언어 · 단계 · 주제 같은 **분류 값과 수**만 들어간다. `raw_value` · 본문 · 이름 · id 는 넣지 않는다.
- **보고서** `para/projects/summer-star/consult-analysis/50-report/report-001-conversion-language.md`(새 폴더 `50-report/` · `README.md` 인덱스 포함) — 절 구성:
  ① 요약(숫자 5개 안쪽) ② 데이터 · 판정 방법 · 한계(표본 크기 · 규칙 판정 · 언어권 ≠ 국적) ③ 예약 단계 깔때기(채널별) ④ 예약까지 가는 대화 — 성공 / 실패 비교 ⑤ 언어별 특징 ⑥ 문의 주제 · 시술 ⑦ 문의 시각 · 응답 시간 · 자동응답 ⑧ 다음에 볼 것.
  수치는 전부 `stats-001.json` 에서 온다 — 보고서에만 있는 수는 없다.

## 8. 열린 것 — 옵션 + 권장

OQ-201 ~ 205 는 **닫혔다** — 전부 권장 A 대로: OQ-201 → D-14(`claude -p` · haiku) · OQ-202 → D-15 · OQ-203 → D-16 · OQ-204 → D-17 · OQ-205 → D-18. 아래 표의 그 줄들은 기록이다. 열린 것은 OQ-206 하나다.

| ID | 무엇 | 옵션 | 권장 · 근거 |
|---|---|---|---|
| ~~OQ-206~~ (닫힘 · D-22 · B) | 별칭 표에 대응 값이 없는 시술(消脂針 83방 · Tune 66방 등 — §5)을 목록에 더할지 | **A** 재시험의 `other` 비율을 보고 정한다 · **B** 지금 값을 더한다 | **A** — D-20 이 정한 목록은 표본 30방 기준이다. 재시험에서 `other` 가 여전히 20% 를 넘으면 `procedures_other` 상위 값을 근거로 더한다 |
| OQ-201 | LLM CLI · 모델 | **A** `claude -p` · **B** `codex exec` | **A** — 로컬에 둘 다 깔려 있다(확인함). 번체 중국어 대화를 읽고 정해진 JSON 을 내는 일이고 1,883번 부른다. 모델은 표본 30방을 작은 모델 · 큰 모델 둘로 돌려 주제 · 시술 일치율을 보고 정한다(일치율이 높으면 작은 모델). 시험은 WORK-002 WP3 |
| OQ-202 | 예약표 없이 다른 경로로 넘긴 예약을 `form_filled` 로 볼지 | **A** 보지 않는다 · 표시만(`handoff_mentioned`) · **B** 성공으로 본다 | **A** — 다른 메신저 언급 방이 94(IG 21 · FB 73)인데 거기서 예약이 됐는지는 이 데이터에 없다. 성공 정의(예약표 회신)를 지키고, 보고서 한계 절에 「다른 경로 언급 94방」을 적는다 |
| OQ-203 | `confirmed` 단계 | **A** 두지 않는다 · LLM 의 `staff_confirmed` 를 참고 값으로만 · **B** 단계로 둔다 | **A** — 확정 문구는 규칙으로 못 가른다(§2.5). LLM 값이 나온 뒤 `form_filled` 와 얼마나 겹치는지 보고 다음 판에서 정한다 |
| OQ-204 | 번체 · 간체를 가를 글자가 없는 한자 메시지 · 방의 값 — D-06 값 목록에 없다 | **A** 값 `zh`(번간 미상)를 더한다 · **B** 그 방 · 채널의 다수 쪽으로 넣는다 | **A** — 짧은 메시지는 공통 글자뿐일 수 있고, 다수 쪽으로 넣는 것은 추정이다. 메시지는 방의 번간으로 흡수되고(§3) 방까지 `zh` 로 남는 것은 적을 것이다(건수는 WP1 에서) |
| OQ-205 | 즉시응답 흐름(`flow`)이 보낸 예약표를 `form_sent` 로 셀지 | **A** 센다(`form_source = 'flow'` 로 구분) · **B** 자동응답처럼 뺀다 | **A** — 영업시간 외 빈 표는 누구나 받지만(DEC-001 D-07) 흐름의 표는 고객이 예약 단추 · 말을 눌러서 받는다. `flow` 만 받은 방은 FB 27 · IG 0. B 면 `form_sent` 가 158 → 131 |
