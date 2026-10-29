# 식약처 API 실호출 기록 (2026-10-27)

키: `.env` 의 `MFDS_API_KEY` (공공데이터포털 일반 인증키 · Decoding). 값은 커밋하지 않는다.

## 의료기기 품목허가 정보 — `MdlpPrdlstPrmisnInfoService06` (data.go.kr 15057456) · 사용 가능

| 오퍼레이션 | 필터(대문자 · 확인됨) | 주요 필드 |
|---|---|---|
| `getMdlpPrdlstPrmisnList05` 목록 | **소문자** `prduct`(품목명=일반명칭) · `entrps`(업체) — 대문자는 무시됨(writer 재호출로 정정) | ENTRPS · PRDUCT · PRDUCT_PRMISN_NO · PRMISN_DT · RTRCN_DSCTN_DIVS_CD/DT(취소·취하) · MDEQ_PRDLST_SN · MNFT_CLNT_NM · **MANUF_NM(제조원 원어명)** |
| `getMdlpPrdlstPrmisnItem05` 상세 | **대문자** `TYPE_NAME`(모델명 · 부분 일치 · 대소문자 구분) · `ENTRPS`(부분 일치) — 소문자는 무시됨 | 위 + GRADE · USE_PURPS(사용목적) · MEA_CLASS_NO · **TYPE_NAME(모델명)** · BRNO |

- 전체 214,377건. `PRDUCT` 는 「조직수복용생체재료」 같은 **일반명칭**이라 브랜드(써마지)로는 안 걸린다 — 브랜드는 `TYPE_NAME`(모델명)에 있을 때만 걸린다
- 예: `TYPE_NAME=Thermage` → 3건(대리점 수입분). 솔타메디칼코리아 제품은 모델 코드(TF-3-60 등)로 등록 → 브랜드 ↔ 허가 매칭은 업체 + 모델 + 사용목적으로 해야 한다
- `MANUF_NM` 예: 「Solta Medical Inc.」 · 「Collagen Corporation」 → **회사 원어명 원천으로 쓸 수 있다**
- 취소·취하된 허가가 섞여 있다(RTRCN_DSCTN_*) — 유효 허가만 골라야 한다

## 의약품 제품 허가정보 — `DrugPrdtPrmsnInfoService07` (data.go.kr 15095677) · 미등록

- `SERVICE_KEY_IS_NOT_REGISTERED_ERROR` — 이 키로 활용신청이 안 됐거나 승인 반영 전(반영까지 1시간 안팎 걸릴 수 있음)

## 의료기기 수입 및 제조허가 상세 — `MdeqMnftPrmsnDtlService01` (data.go.kr 15073895) · 사용 가능

- `getMdeqMnftPrmsnDtlInq01` · 전체 15,893 업체 · 필드 예: BSSH_NM(업체명) · COB_FLAG_CODE_NAME(제조업/수입업) · PERMIT_STATE_CODE_NAME(허가 상태) · PRMSN_YMD

## 정정 · 추가 (SPEC-002 작성 중 writer 재호출 9회)

- 목록과 상세가 파라미터 대소문자 규칙이 반대다(위 표). 0건이면 응답에 `items` 키가 없다
- `MANUF_NM` 표기가 갈린다(「Inc.」 / 「, Inc.」) — 원어명 정규화 필요
- 업체 API `BSSH_NM` 부분 일치 · `COB_FLAG_CODE_NAME`(제조업/수입업)
- 의약품 · DUR: SERVICE_KEY_IS_NOT_REGISTERED (10-27 기준)

## 의약품 제품 허가정보 — **`DrugPrdtPrmsnInfoService08`** · 사용 가능 (10-27 확인)

- 07 은 「등록되지 않은 서비스키」 — 현재 버전은 **08**. 활용신청은 승인돼 있었다(07 호출이 틀렸던 것)
- `getDrugPrdtPrmsnInq08`(목록) · `getDrugPrdtPrmsnDtlInq08`(상세) · `getDrugPrdtMcpnDtlInq08`(주성분 상세). 필터 `item_name`(소문자)
- 목록 필드: ITEM_SEQ · ITEM_NAME · **ITEM_ENG_NAME** · ENTP_NAME · **ENTP_ENG_NAME(회사 원어명)** · ITEM_PERMIT_DATE · PRDLST_STDR_CODE · PRDUCT_PRMISN_NO · ITEM_INGR_NAME · CANCEL_DATE/CANCEL_NAME(정상/취소) · BIZRNO
- 상세 필드: CNSGN_MANUF(위탁 제조원) · ETC_OTC_CODE(전문/일반) · **MATERIAL_NAME(총량·성분·분량·단위 — 예 「1바이알 · 100 유니트」)** · **PACK_UNIT(포장 단위 — 규격 원천)** · EE/UD/NB_DOC_DATA(효능 · 용법 · 주의) · MAIN_ITEM_INGR · ATC_CODE · MAIN_INGR_ENG · STORAGE_METHOD · VALID_TERM
- 예: 나보타 → 「나보타주(클로스트리디움보툴리눔독소A형)」 / Nabota Inj / (주)대웅제약 / Daewoong Pharmaceuticals / 1바이알(100유니트) / 전문의약품 / 정상

## DUR 품목정보 — `DURPrdlstInfoService03` · 사용 가능 (10-27 사용자 신청 직후 확인)

- 오퍼레이션 9개: getUsjntTabooInfoList03(병용금기) · getPwnmTabooInfoList03(임부금기) · getSpcifyAgrdeTabooInfoList03(특정연령대금기) · getOdsnAtentInfoList03(노인주의) · getCpctyAtentInfoList03(용량주의) · getMdctnPdAtentInfoList03(투여기간주의) · getEfcyDplctInfoList03(효능군중복) · getSeobangjeongPartitnAtentInfoList03(서방정분할주의) · getDurPrdlstInfoList03(DUR 품목 목록)
- 필터 `itemName`. 나보타 병용금기 0건(톡신은 DUR 대상 거의 없음) · 이소트레티노인 임부금기는 아래 실호출 참고

## 구현 중 확인 (tool_dev 실호출 · 10-27 — 키 값은 기록하지 않음)

의약품 08 · DUR 03 의 「응답 미확인」 칸을 채운 기록. 필터가 먹었는지는 `totalCount` 로 판단했다(무시되면 전체 건수가 나온다).

| 오퍼레이션 | 보낸 필터 | total | 알게 된 것 |
|---|---|---|---|
| `getDrugPrdtPrmsnInq08` | `item_name=나보타` | 4 | 소문자 `item_name` · 부분 일치. items 는 **평평한 dict 목록** |
| 같음 | `ITEM_NAME=나보타`(대문자) | 42,704 | 대문자는 무시된다(전체) |
| 같음 | `entp_name=대웅제약` | 363 | 소문자 `entp_name` · 부분 일치 |
| 같음 | `item_name` + `entp_name` | 4 | AND |
| 같음 | `item_seq=<ITEM_SEQ>` | 42,704 | **목록은 `item_seq` 를 무시한다** |
| 같음 | `item_ingr_name=<성분>` | 0 | 받는지 판단 불가(0건) → tool 에 성분 입력을 두지 않았다 |
| 같음 | `item_name=포도당` | 50 | 취소 예: `CANCEL_NAME` 「취하」 · `CANCEL_DATE` 「20241213」. 정상은 `CANCEL_NAME` 「정상」 · `CANCEL_DATE` null |
| `getDrugPrdtPrmsnDtlInq08` | `item_seq=<ITEM_SEQ>` | 1 | 상세는 `item_seq` 를 받는다(한 건 조회 키). 없는 값이면 0 |
| 같음 | `item_name=나보타` | 4 | 상세도 `item_name` 을 받는다 |
| `getDrugPrdtMcpnDtlInq08` | `item_seq` · `ITEM_SEQ` · `prduct`(소문자) | 125,614 | 모두 무시된다 |
| 같음 | `Prduct=나보타` | 0 | `Prduct`(첫 글자 대문자)는 받지만 **완전 일치**다 |
| 같음 | `Prduct=<상세의 ITEM_NAME 전체>` | 1 | 필드: ENTRPS_PRMISN_NO · ENTRPS · PRDUCT · MTRAL_SN · MTRAL_CODE · MTRAL_NM · QNT · INGD_UNIT_CD · ITEM_SEQ · MAIN_INGR_ENG · BIZRNO · CPNT_CTNT_CONT · TAMT_SEQ |
| `DURPrdlstInfoService03/getPwnmTabooInfoList03` | `itemName=이소트레티노인` | 41 | items 평평. 필드: TYPE_NAME · MIX_TYPE · INGR_CODE · INGR_ENG_NAME · INGR_NAME · MIX_INGR · FORM_NAME · ITEM_SEQ · ITEM_NAME · ITEM_PERMIT_DATE · ENTP_NAME · CHART · CLASS_CODE · CLASS_NAME · ETC_OTC_NAME · MAIN_INGR · NOTIFICATION_DATE · PROHBT_CONTENT · REMARK · INGR_ENG_NAME_FULL · CHANGE_DATE |
| 같음 | `ITEM_NAME=이소트레티노인` | 16,063 | 대문자는 무시된다 |
| 같음 | `itemSeq=<ITEM_SEQ>` | 1 | `itemSeq` 를 받는다 |
| `getUsjntTabooInfoList03` | `itemName=이소트레티노인` | 1,189 | 병용 상대는 `MIXTURE_*` 필드(MIXTURE_ITEM_NAME · MIXTURE_INGR_KOR_NAME …) · PROHBT_CONTENT |
| `getDurPrdlstInfoList03` | `itemName=이소트레티노인` | 41 | 필드에 CANCEL_DATE/CANCEL_NAME 이 있다. 키 하나가 `'TYPE_NAME  '`(뒤 공백 둘)로 온다 — 원본 그대로 낸다 |

- 의약품 상세의 `EE_DOC_DATA` · `UD_DOC_DATA` · `NB_DOC_DATA` 는 `<DOC title="효능효과" …>` XML 문자열이다
- **틀린 키(가짜 값)로 부르면 HTTP 403 `SERVICE_KEY_IS_NOT_REGISTERED_ERROR`** 가 온다 — 미등록과 구분되지 않는다(stdio 누출 시험 중 확인)
- (검수 W-2 확인, 10-27) DUR 6종(특정연령대 · 노인 · 용량 · 투여기간 · 효능군중복 · 서방정분할) 모두 `itemName` 필터가 먹는다 — 없는 이름 0건, 아세트아미노펜 48 · 0 · 204 · 0 · 139 · 24(필터 없을 때 2,672 · 1,974 · 6,600 · 648 · 7,055 · 2,195)
