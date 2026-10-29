# 레코드 스키마 — `step1-products.json` (v2)

정본 파일의 `basis.fields` 를 풀어 쓴 것과 실제 행 발췌다. 칸을 새로 만들지 말고 이 칸에 넣는다.

## 파일 최상위

| 칸 | 무엇 |
|---|---|
| `version` · `generated_at` · `scope` · `basis` | 판 · 날짜 · 범위 · 입력(고정본 · 결정 · 조사 파일 · 스크립트) |
| `summary` | 수치(행 · 상태별 · 추천 · 라인 · 업체 칸 · 원천 수정 · open) — **반영 때마다 다시 센다** |
| `lines{라인 이름}` | 라인(상위) — `line_row` · `items[{license_no, name?, ledger_id?}]` · `item_undetermined_rows` · `company` · `decision` |
| `shared_license[]` | 같은 허가를 가리키는 원장 행 묶음 · `relation` |
| `open[]` | 결정에 없어 바꾸지 않은 것 `{ledger_id, name, open, decision}` |
| `items[]` | 행(아래) |

## 행 (`items[]`)

| 칸 | 무엇 | 비고 |
|---|---|---|
| `ledger_id` | 원천 taxonomy id · 새 행은 `auto-…` | 바꾸지 않는다 |
| `family` | 원천 계열 `{code, name}` | 2단계 대상 |
| `1_identity` | `kind`(제품(의료기기) · 장비 · 확인 불가 …) · `basis` · `basis_type` | |
| `2_names` | `display_name`(대표 한글 1) · `ledger_name`(원장 이름) · `search_names[{name, lang 한/영}]` · `name_basis[]`(이유) | 허가 이름은 `licenses[].official_name` 에만 |
| `4_license.status` | 6종: 정상 · 확인 불가 · 허가 대상 아님 · 허가 취소(이력) · 미허가 · 허가번호 미확인 | `rules.md` 상태 표 |
| `4_license.recommendable` | 추천 여부 | 상태에서 정해진다 |
| `4_license.reason` | 상태 판정 한 줄(규칙 · 결정 · 근거) | |
| `4_license.licenses[]` | **정상 · 내수 허가만** `{key, license_no, kind, state, item, official_name, models, holder, manufacturer, date, source}` | key = `device:<품목일련번호 또는 허가번호>` · `emedi:<허가번호>` · `drug:<ITEM_SEQ>` |
| `4_license.history[]` | 취소 · 취하 · 만료 · 재제조 | `state` 에 「취하」 · 「재제조(정품 아님)」 등 |
| `4_license.reference[]` | 수출용 · 후보 · 연결 안 함 + `why` | 수출용은 emedi 근거를 `why` 에 |
| `4_license.license_basis` · `distribution_sources[]` | 「국내 유통 확인 · 허가 대상 여부 출처 없음」 + 유통 URL | 규칙 5 |
| `4_license.approval` | 규칙 귀결로 연결한 경우 `{by, date, basis}` | 승인 기록 |
| `5_spec` | 규격(허가 포장단위 · 함량 · 시장 단위) | |
| `6_companies` | `manufacturer` · `importer` · `seller` · `license_holder` · `other` — 각 `[{name, original, basis}]` · `conflicts[]` | 근거 없으면 name 에 「근거 없음(…)」 |
| `7_site_use` | 현장 사진 id | |
| `line` | 이 행이 속한 라인 `{line_name, role, members, decision}` | 최상위 `lines` 와 맞춘다 |
| `merged_into` / `merged_from` | 합침 — 행은 남긴다 | `active: false` |
| `moved_to` · `moved_note` | 「5단계 시술 이름」으로 빠짐 — 행은 남긴다 | `active: false` |
| `gate` · `change_vs_draft` · `note` · `evidence[]` · `recheck` · `open[]` | 사람 확인 사유 · 초안 대비 변화 · 근거 · 재조사 질의 기록 · 남은 것 | |
| `active` | 합침 · 빠짐이 아닌 제품 행 | |

## 실제 행 1 — 디클래씨 (정상 + 취소 이력 · 판매 근거 없음)

```json
{
 "ledger_id": "auto-12-1774737181584",
 "family": {
  "code": "M3",
  "name": "M3 바이오스티뮬레이터/콜라겐부스터 · CaHA (칼슘하이드록시아파타이트)"
 },
 "1_identity": {
  "kind": "제품(의료기기)",
  "basis": "식약처 허가(제허11-1324호, 제허 23-60 호) · 원천 taxonomy M3 바이오스티뮬레이터/콜라겐부스터 · CaHA (칼슘하이드록시아파타이트)",
  "basis_type": "구간 A 기록"
 },
 "2_names": {
  "display_name": "디클래씨",
  "ledger_name": "디클래씨",
  "search_names": [
   {
    "name": "DCLASSY CaHA",
    "lang": "영"
   },
   {
    "name": "Facetem",
    "lang": "영"
   }
  ],
  "name_basis": [
   "대표 이름 「디클래씨」: 원장 이름(국문)",
   "「DCLASSY CaHA」: 10-27 제품 이름(정규화)",
   "「Facetem」: 같은 허가의 다른 제품명"
  ]
 },
 "4_license": {
  "status": "정상",
  "kind": "의료기기",
  "reason": "정상 허가 1건 이상 → 허가 규칙(10-27): 정상 1 연결 · 취소 1 은 history(이력)",
  "licenses": [
   {
    "key": "emedi:제허11-1324호",
    "license_no": "제허11-1324호",
    "kind": "의료기기",
    "state": "정상",
    "item": "조직수복용재료",
    "official_name": "BACF_0.8",
    "official_name_en": "Graft/prosthesis",
    "product_names": "볼라썸,VOLassom,Facetem, NUIT, Facetem S, VoLassom CaHA, DCLASSY CaHA 0.8, DCLASSY CaHA 1.5, LUMICA",
    "models": [
     "BACF_0.8",
     "FACETEM BACF08RP",
     "FACETEM BACF03RP",
     "CAFO0003",
     "CAFO0015",
     "CAFD0015"
    ],
    "holder": "(주)시지바이오",
    "holder_biz": "제조업",
    "date": "2011-12-05",
    "source": "emedi(의료기기 전자민원 품목 검색 https://emedi.mfds.go.kr/search/data/list · 제품명/품목명/모델명 전체) query2=Facetem → 허가 제허11-1324호 (품목일련번호 2011006033)"
   }
  ],
  "history": [
   {
    "key": "device:2023000474",
    "license_no": "제허 23-60 호",
    "kind": "의료기기",
    "state": "취소",
    "item": "조직수복용재료",
    "official_name": "Facetem S BACF15P외 3건",
    "models": [
     "Facetem S BACF08RP",
     "Facetem S BACF10RP",
     "Facetem S BACF15P",
     "Facetem S BACF03RP"
    ],
    "holder": "(주)디엔컴퍼니",
    "holder_biz": "제조업",
    "manufacturer": "(주)시지바이오",
    "date": "2023-01-27",
    "source": "식약처 의료기기 품목허가 API(getMdlpPrdlstPrmisnItem05) device:2023000474 · 질의 device TYPE_NAME=Facetem · emedi query2=Facetem"
   }
  ],
  "reference": [],
  "recommendable": true
 },
 "6_companies": {
  "manufacturer": [
   {
    "name": "(주)시지바이오",
    "original": null,
    "basis": "의료기기 허가 제허11-1324호(제조 허가) 업체 · emedi 업종 제조업"
   }
  ],
  "importer": [
   {
    "name": "해당 없음",
    "original": null,
    "basis": "국내 제조 허가(허가번호 「제허」 · 의약품 업종 제조) — 수입 허가 없음"
   }
  ],
  "seller": [
   {
    "name": "근거 없음(대웅제약 · 디엔컴퍼니 공동 브랜드 보도 — 판매 주체 미확인)",
    "original": null,
    "basis": "업체관계 결정 roles.seller · https://www.newsis.com/view/NISX20260612_0003666695"
   }
  ],
  "license_holder": [],
  "other": [],
  "conflicts": []
 },
 "evidence": [
  "emedi(의료기기 전자민원 품목 검색 https://emedi.mfds.go.kr/search/data/list · 제품명/품목명/모델명 전체) query2=Facetem → 허가 제허11-1324호 (품목일련번호 2011006033)",
  "식약처 의료기기 품목허가 API(getMdlpPrdlstPrmisnItem05) device:2023000474 · 질의 device TYPE_NAME=Facetem · emedi query2=Facetem",
  "web: https://www.newsis.com/view/NISX20260612_0003666695",
  "업체관계 결정 link: https://dailypharm.com/user/news/339272 · https://www.newsis.com/view/NISX20260612_0003666695"
 ],
 "open": [],
 "active": true
}
```

## 실제 행 2 — 슈링크 (내수 허가 연결 · 수출용은 reference · 발췌)

```json
{
 "ledger_id": "M9-1-3",
 "2_names": {
  "display_name": "슈링크",
  "ledger_name": "슈링크",
  "search_names": [
   {
    "name": "SHURINKs",
    "lang": "영"
   },
   {
    "name": "UF3-C300",
    "lang": "영"
   },
   {
    "name": "ULTRAFORMER-IIIs",
    "lang": "영"
   }
  ],
  "name_basis": [
   "대표 이름 「슈링크」: 제품 이름(10-27 정규화)",
   "「SHURINKs」: 식약처 모델명",
   "「UF3-C300」: 식약처 모델명",
   "「ULTRAFORMER-IIIs」: 식약처 모델명"
  ],
  "ledger_maker_texts": [
   "클래시스"
  ]
 },
 "4_license": {
  "status": "정상",
  "kind": "의료기기",
  "reason": "수출 전용 허가 대신 같은 업체 내수 허가 연결 — SHURINK · SHURINK-A 모델(규칙 A: 이름 + 업체 일치 · 수출용 재판정 10-28) · 코디 승인(검수 v3 G1 · _RESUME §2 10-28 — 정상만 연결 · 수출용 규칙의 직접 귀결 · 같은 업체 · 이름 일치)",
  "licenses": [
   {
    "key": "device:제허14-1422",
    "license_no": "제허 14-1422 호",
    "kind": "의료기기",
    "state": "정상",
    "item": "집속형초음파자극시스템",
    "official_name": "ULTRAFORMER III (REGEND)",
    "models": [
     "SHURINK",
     "SHURINK-A"
    ],
    "holder": "(주)클래시스",
    "manufacturer": null,
    "date": "2014-08-01",
    "source": "emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2014007558 · 목록 query2=SHURINK · xprtppYn 아니오(내수)"
   }
  ],
  "history": [],
  "reference": [
   {
    "license_no": "제허 15-1401 호",
    "model": "SHURINKs",
    "item": "고강도집속형초음파수술기",
    "company": "(주)클래시스",
    "state": "정상",
    "date": "2015-09-14",
    "key": "device:2015006863",
    "why": "수출용에 한함 — 국내 허가로 치지 않음(10-27 규칙) · 근거 emedi 품목 상세 POST https://emedi.mfds.go.kr/search/data/item meddevItemSeq=2015006863 xprtppYn=예 · 비고 「수출용에 한함」"
   }
  ],
  "approval": {
   "by": "코디",
   "date": "2026-10-28",
   "basis": "검수 v3 G1 승인 — 정상 · 내수 허가만 연결 · 수출용 규칙의 직접 귀결 · 같은 업체 · 이름 일치(_RESUME §2 10-28)"
  },
  "recommendable": true
 },
 "active": true
}
```

## 실제 행 3 — 리프세라 (확인 불가 → 리프테라에 합침 · 행은 남김)

```json
{
 "ledger_id": "auto-M9-1775363051791",
 "2_names": {
  "display_name": "리프세라",
  "ledger_name": "리프세라",
  "search_names": [],
  "name_basis": [
   "대표 이름 「리프세라」: 제품 이름(10-27 정규화)"
  ]
 },
 "4_license": {
  "status": "확인 불가",
  "licenses": [],
  "history": [],
  "reference": [],
  "recommendable": false
 },
 "merged_into": "M9-1-8",
 "active": false
}
```

## 발췌 — 알라딘필링 `4_license` (국내 유통 확인 표시 · 추천 유지)

```json
{
 "status": "허가 대상 아님",
 "license_basis": "국내 유통 확인 · 허가 대상 여부 출처 없음",
 "distribution_sources": [
  {
   "url": "https://tatoaay.co.kr/common/html/nonpay.html",
   "text": "타토아의원 안양범계역 가격표 「알라딘필링 1회(재생관리 포함)」 (data-anyang prices/c05_타토아의원-안양범계역.json · 2026-09-28)"
  },
  {
   "url": "http://www.toxnfill28.com/serviceInfo.php?c=703",
   "text": "톡스앤필의원 안양 가격표 「뉴알라딘 필링」 (data-anyang prices/c10_톡스앤필의원-안양.json · 2026-09-28)"
  }
 ],
 "recommendable": true
}
```

## 발췌 — 젠틀맥스 프로+ `history` (재제조 · 취하)

```json
[
 {
  "license_no": "수허 26-194 호",
  "model": "GentleMaxi Pro Plus",
  "item": "알렉산드라이트 레이저 수술기",
  "company": "주식회사 밴스로컬",
  "state": "재제조(정품 아님)",
  "date": "2026-08-21",
  "key": "device:2026005331"
 },
 {
  "key": "device:수허13-466",
  "license_no": "수허 13-466 호",
  "kind": "의료기기",
  "state": "취하",
  "item": null,
  "official_name": "GentleMax Pro",
  "models": [],
  "holder": "(주)신한씨스텍",
  "manufacturer": null,
  "date": "2019-09-17(취하)",
  "source": "step1-d09-web"
 }
]
```

## 발췌 — 엑소힐러 (시술 이름으로 빠짐)

```json
{
 "ledger_id": "auto-M4-1775360458021",
 "moved_to": "5단계 시술 이름",
 "moved_note": "병원 메뉴명 · 장비 유형 일반명 — 제품 원장에서 빼고 5단계 시술 이름으로(D24)",
 "active": false,
 "recommendable": false
}
```
