#!/usr/bin/env python3
"""bronze-ledger-column-scan.json → bronze-ledger-column-report.md 렌더.
표·수치는 전부 JSON 에서 읽고, 한 줄 설명·관찰 문장·질문만 이 파일에 손으로 적는다."""
import json
import os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "bronze-ledger-column-scan.json")
OUT = "/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/bronze-ledger-column-report.md"

R = json.load(open(SCAN, encoding="utf-8"))
F = R["files"]
CC = R["cross_checks"]
EX = R["extra_checks"]


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def ex_join(l):
    return " · ".join(f"`{esc(x)}`" for x in l) if l else ""


# ---------- 손으로 적는 부분 ----------
DESC = OrderedDict([
    ("anatomy-danger-zones.json", "얼굴 11개 부위(zone)별 혈관·신경·조직 수치·보톡스/필러 주의사항. 계열 코드 없음"),
    ("combo-recipes.json", "목적(goal)별 시술 조합 레시피 7개. 시술은 M 코드 배열, 후속 프로토콜(week/action) 포함"),
    ("complications.json", "계열 10개(M1·M2·M3·M7·M8·M9·M11·M14·M15·M16)별 합병증 65건: 중증도·발생률·기전·관리·예방"),
    ("consent-checklist.json", "계열 17개별 필수 고지·금기·응급 징후 문자열 배열"),
    ("contraindications.json", "계열 쌍(from→to) 27개의 병행 금기/주의/간격 규칙"),
    ("extracted.json", "계열 17개의 교과서 추출 요약(개요·기전·적응증·안전성·금기·관리). 최상위 키가 M 코드"),
    ("literature-evidence.json", "계열 17개별 문헌 근거 문장 119개(moa/adverse_effects/effects) + 인용(PMID/DOI) + 환자용 4개 국어 문장"),
    ("market-pricing.json", "계열 17개별 시장 가격 항목 122개(low/mid/high, KRW, 단위 문자열)"),
    ("patient-education.json", "계열 17개별 환자 설명(쉬운 설명·원리·지속·통증·다운타임) + Q&A 51개"),
    ("pih-risk.json", "에너지/필링 계열 세부 시술 26개의 PIH 위험도·발생률·위험인자·예방. procedure_ref 로 taxonomy 하위 id 참조"),
    ("post-procedure-timeline.json", "시술 10종의 시술 후 경과(phases: Day 구간별 정상/이상/주의/응급 증상 배열)"),
    ("pre-procedure-checklist.json", "공통 체크 12개 + 계열 17개별 시술 전 확인 항목 123개(label/type)"),
    ("problem-combos.json", "고민(P) 8개별 상담용 패키지 24개: tier·제품·가격대·세일즈 멘트·임상 근거"),
    ("problem-packages.json", "고민 14개 × 주호소(cc) 115개별 시술(제품 포함)·조합·대안. description 에 「taxonomy P1~P14 기반 자동 생성」"),
    ("procedure-comparison.json", "비교 주제 9개(lifting 등)별 시술 39개의 기전·통증·다운타임·비용·적합/한계·PIH"),
    ("procedure-profiles.json", "계열 17개의 플로어 운영 프로파일(phase 순서·마취·준비시간·소요시간·위험 점수·주의·관리)"),
    ("products.json", "제품-제조사 매핑 8개 섹션 59개 제품(name/name_en/제조사/국가/mfds). 섹션 키가 영문 슬러그"),
    ("synergy.json", "시술 노드 쌍 115개의 시너지 링크(함께/다음에/대신). 노드는 `M코드-이름` 합성 문자열"),
    ("taxonomy.json", "계열(modality) 17 → 하위 74 → 항목 521 + 계열별 extracted/products, 고민(problem) 14 → 하위 53 → 항목 117(modality_ref). 가장 큼(660KB)"),
    ("treatment-optimization.json", "고민 8개 × 중증도 3단계의 최적 조합·순서·근거, 연령대 4개 권장, 조합 규칙 8개, 연간 플랜 3개"),
    ("treatment-sequence.json", "동일 세션 시술 순서 11단계, 당일 병행 금기 9쌍, 대표 조합 8개, 최소 간격 9개. 시술명 대부분 자유 텍스트"),
])

# 주 레코드 경로(요약 표의 「레코드 수」)
MAIN_RECORDS = OrderedDict([
    ("anatomy-danger-zones.json", ["zones"]),
    ("combo-recipes.json", ["recipes"]),
    ("complications.json", ["categories", "categories[].complications"]),
    ("consent-checklist.json", ["categories"]),
    ("contraindications.json", ["rules"]),
    ("extracted.json", ["(최상위 {code})"]),
    ("literature-evidence.json", ["(categories.{code})", "categories.{code}.moa", "categories.{code}.adverse_effects", "categories.{code}.effects"]),
    ("market-pricing.json", ["categories", "categories[].items"]),
    ("patient-education.json", ["categories", "categories[].common_concerns"]),
    ("pih-risk.json", ["procedures"]),
    ("post-procedure-timeline.json", ["timelines", "timelines[].phases"]),
    ("pre-procedure-checklist.json", ["universal_checks", "category_specific", "category_specific[].checks"]),
    ("problem-combos.json", ["combos", "combos[].packages"]),
    ("problem-packages.json", ["problems", "problems[].complaints", "problems[].complaints[].procedures", "problems[].complaints[].combos"]),
    ("procedure-comparison.json", ["comparisons", "comparisons[].procedures"]),
    ("procedure-profiles.json", ["profiles"]),
    ("products.json", ["(섹션 8)", "*.products"]),
    ("synergy.json", ["links"]),
    ("taxonomy.json", ["modality", "modality[].subcategories", "modality[].subcategories[].items", "modality[].products", "problem", "problem[].subcategories", "problem[].subcategories[].items"]),
    ("treatment-optimization.json", ["by_concern", "by_concern[].severity_levels", "by_age_group", "combination_rules", "annual_plans"]),
    ("treatment-sequence.json", ["principles", "sequence_order", "incompatible_same_day", "common_combos", "minimum_intervals"]),
])

# 파일별 손 관찰 (스크립트 결과를 읽고 적음; 판정 아님)
OBS = OrderedDict([
    ("anatomy-danger-zones.json", [
        "`zones[].tissue_data` 는 부위마다 키가 전부 다르다(11개 zone 에 `notes` 만 공통, 나머지 31개 잎 경로는 각각 zone 1개에만). 고정 스키마가 아니라 부위별 자유 구조.",
        "`vessels[].depth_mm` 는 24건 중 22건, 대신 `depth_range_mm[]` 가 5건 — 깊이가 단일값/범위 두 형태로 섞여 있다.",
        "`danger_level`(2~5 정수)과 `danger_color`(green/yellow/orange/red), `filler_specific.risk_level` 이 zone 마다 같은 값으로 셋 다 들어 있다.",
        "`botox_specific.diffusion_range_cm` 은 문자열 `1.5-3.0`(1건), `filler_specific.emergency_protocol` 은 3건에만 있다.",
        "혈관·신경 이름은 `한글 (영문)` 합성 문자열. 같은 혈관이 여러 zone 에 반복(활차상동맥, 안면동맥 등 4종 중복).",
        "M/P 코드 참조가 하나도 없다. 부위 id 는 영문 슬러그(forehead, glabella …)이고 taxonomy 의 부위 라벨(코, 이마/관자놀이 …)과는 표기가 다르다.",
    ]),
    ("combo-recipes.json", [
        "`goal` 은 영문 슬러그(lifting, regeneration, tightening, texture, anti-aging, tone), `intensity` 는 한글(기본/풀패키지/표준/적극) — 한 레코드 안에 영/한 코드가 섞여 있다.",
        "`procedures[]` 는 M 코드 배열(9종). 레시피 id 는 `R1~R7` 로 이 파일에만 있는 체계.",
        "키 이름이 camelCase(expectedResults, patientExplanation, repeatCycle, followUp) — 대부분의 파일(snake_case)과 다르다.",
        "`followUp[].week` 는 정수(2~52), `action` 은 자유 텍스트. `repeatCycle` 도 자유 텍스트(`3~6개월 간격 반복`).",
    ]),
    ("complications.json", [
        "`version`/`updated` 메타가 없다(21개 중 taxonomy·extracted 와 함께 3개).",
        "계열 10개만 다룬다(M4·M5·M6·M10·M12·M13·M17 없음).",
        "`risk_factors` 가 65건 중 46건은 빈 배열 `[]`, 19건만 채워짐(총 92개 문자열).",
        "`evidence`(38/65)·`duration`(19/65)은 일부 레코드에만 있다. `evidence` 는 URL 문자열이고 `;` 로 여러 개를 이어 붙인 경우가 있다.",
        "`incidence`·`onset` 은 자유 텍스트(`대부분 (일시적)`, `약 11-25% (부위·기법에 따라)`).",
        "합병증 `name` 이 계열 사이에서 중복된다(`감염`, `PIH (시술 후 과색소침착)`). 같은 개념이 `홍반 (Erythema)` / `홍반 (Erythema / Redness)` / `홍반 (시술 직후 빨개짐)` 처럼 세 표기로도 나온다.",
    ]),
    ("consent-checklist.json", [
        "레코드당 문자열 배열 3개뿐이라 구조가 단순하다. 잎 키 8개.",
        "`contraindications[]` 105개 중 distinct 70 — `임신 및 수유 중` 15회, `켈로이드 체질` 6회 등 같은 문자열이 계열마다 반복된다. `시술 부위 활동성 감염` 과 `시술 부위 활동성 감염 또는 염증` 처럼 비슷한 문장이 따로 있다.",
        "`mandatory_disclosures[]` 109개는 전부 distinct.",
    ]),
    ("contraindications.json", [
        "`from`/`to` 코드와 `from_name`/`to_name` 이름이 레코드마다 같이 들어 있다(코드-이름 중복 보관). 이름은 taxonomy 의 category 와 같다.",
        "`level` 은 caution 14 / safe 8 / warning 5 의 3값, `interval` 은 자유 텍스트 12종(`같은 날 가능`, `2주 간격 권장`).",
        "쌍은 27개이며 한 방향만 있다(M1→M2 는 있고 M2→M1 은 없음). M10·M13~M17 은 등장하지 않는다.",
    ]),
    ("extracted.json", [
        "최상위가 M 코드 키 17개인 객체이고, 키 순서가 M10…M17, M1…M9 (문자열 정렬 순).",
        "같은 내용이 `taxonomy.json` 의 `modality[].extracted` 에도 들어 있다. 17개 중 9개(M1·M4·M6·M7·M9·M11·M14·M15·M16)는 본문이 완전히 같고, 8개(M2·M3·M5·M8·M10·M12·M13·M17)는 일부 키 본문이 다르다(§3.9).",
        "`safety.serious` 가 M10·M13 은 `null`, 나머지 15개는 배열 — 같은 키에 타입이 섞인다. `safety.emergency` 는 2개에만 있다.",
        "`procedure_id` 는 `M1-BOTOX` 같은 영문 대문자 슬러그로 다른 파일 어디에도 안 나오는 식별자.",
        "`source` 는 교과서 장 번호 문자열(`임상적 피부관리 36장`) 또는 `일반 의학 지식`(5건). `source_type` 은 kr 11 / general 5 / us 1. `updated` 는 M3 하나에만 있다.",
        "`name` 표기가 taxonomy 의 category 와 다른 것: M3 `바이오스티뮬레이터`(taxonomy `바이오스티뮬레이터/콜라겐부스터`), M5 `PRP 피부재생술`(`PRP/자가혈`), M9 `기기리프팅`(`기기 리프팅`), M12 `MTS (마이크로니들 치료)`(`마이크로니들링(MTS)`).",
    ]),
    ("literature-evidence.json", [
        "`categories` 는 M 코드 키 객체(17개)이지만 섹션이 비어 있는 계열이 많다 — moa 빈 곳 6(M6·M10·M11·M13·M14·M17), adverse_effects 빈 곳 6(M6·M9·M10·M11·M13·M14), effects 빈 곳 8(M3·M6·M10·M11·M13·M14·M15·M17). M6·M10·M11·M13·M14 는 세 섹션 전부 빈 배열.",
        "`accuracy_score`/`accuracy_note` 는 119개 문장 중 17개에만 있다(moa 6, ae 8, effects 3). `added_at` 은 102개에 있고 값은 전부 `2026-04-19` 하나.",
        "`citations[]` 는 문장마다 정확히 1개이고, 같은 논문(PMID 33714246 등)이 여러 문장에 반복된다 — 인용 20종이 119회. `doi`(113/119)·`pmc`(114)·`oa_url`(114)은 일부 빠짐.",
        "`patient_ko` 41개에 `[1][2]` 같은 각주 번호가 본문에 남아 있다. `patient_ja` 5건과 `patient_en` 1건에 한글 글자가 섞여 있다(예: `局所の伝달を`, `ボツ리ヌス`, `狙い通리의`).",
        "`name` 은 영문 학술 명칭(`Botulinum toxin type A (aesthetic)`)으로, 다른 파일의 한글 계열명과 다르다.",
        "`accuracy_summary.by_category_average` 는 7개 계열만 있고, `patient_translations_coverage` 는 `119/119` 문자열.",
    ]),
    ("market-pricing.json", [
        "`unit` 이 17종 자유 문자열(`1회` 87, `1cc`, `2cc`, `1바이알`, `900샷`, `10줄`, `양쪽`, `부위/1회` …).",
        "`items[].name` 에 제품·부위·국산/수입 구분이 괄호로 들어간다(`이마 주름 (수입)`, `울쎄라 (풀페이스)`, `리쥬란 힐러 (2cc)`). 122개 전부 distinct 이고 taxonomy 항목과 직접 연결되는 코드는 없다.",
        "low ≤ mid ≤ high 위반 0건. 값은 KRW 정수.",
        "M9 의 `name` 이 `에너지기기(HIFU/RF)` 로 taxonomy `기기 리프팅` 과 다르다(procedure-profiles 도 같은 표기). M5 는 `PRP/엑소좀`(taxonomy `PRP/자가혈`).",
    ]),
    ("patient-education.json", [
        "계열 17개 전부 있고 잎 키 12개. 모든 값이 자유 텍스트 문장.",
        "`patient_name` 은 환자용 별칭(`주름 보톡스`, `볼륨 필러`, `실 리프팅 (얼굴 당김 시술)`) — 계열명의 또 다른 표기.",
        "`duration_simple`·`downtime` 은 17건 중 distinct 16 (같은 문장이 두 계열에).",
    ]),
    ("pih-risk.json", [
        "`procedure_ref` 가 taxonomy 하위 id 를 가리키는데 깊이가 섞여 있다 — 항목(M8-1-1 등) 16건, 하위분류(M8-5, M9-1, M9-2, M11-1, M15-1) 7건, 계열(M12, M13) 3건. 22 distinct / 26 — `M8-1-1`, `M8-5`, `M11-1`, `M13` 이 각각 2건에 쓰였다.",
        "`procedure_ref` 가 taxonomy 항목과 이름이 어긋나는 것: `M8-5-3` 은 pih 에서 `알렉산드라이트 제모 (755nm LP)`, taxonomy 에서는 `젠틀맥스프로+`.",
        "`notes` 객체의 키가 `M1_to_M7`, `M10`, `M16`, `M17` — 범위 표기 키와 단일 코드 키가 섞여 있다.",
        "`pih_risk` 5값은 `risk_levels` 정의 키와 정확히 일치. `pih_rate` 는 `~5%` 같은 자유 텍스트.",
        "`subcategory` 는 한글 라벨(`색소/토닝`, `프락셔널`) 12종으로 taxonomy subcategory label 과 같은지 코드로는 확인되지 않는다(코드 없음).",
    ]),
    ("post-procedure-timeline.json", [
        "`timelines[].id` 는 영문 슬러그(botox, ha-filler, hifu-rf …), `category` 는 M 코드 — 단 `dca-injection` 의 category 는 `M16-DCA` 로 코드+하위 라벨 합성값.",
        "`name` 이 계열명이 아니라 시술명(`HA 필러`, `HIFU/RF 리프팅`, `프락셔널 CO2 레이저`, `케미컬 필링 (중간 깊이)`)이다.",
        "`phases[].period` 는 `Day 0`, `Day 1-3`, `Day 7-30` 등 12종 문자열이고 구간이 시술마다 다르다. `label` 24종(`시술 당일`, `부종 피크기` …).",
        "phase 의 증상 키 4개(normal/abnormal/caution/emergency)는 `reaction_levels` 정의와 일치.",
    ]),
    ("pre-procedure-checklist.json", [
        "`universal_checks[]` 에는 `id`(영문)가 있지만 `category_specific[].checks[]` 에는 id 가 없고 `label`+`type` 뿐이다.",
        "`type` 은 두 곳 합쳐 6종(must_check, absolute_contraindication, relative_contraindication, counseling, inform, safety_protocol). universal 과 category_specific 이 쓰는 집합이 다르다.",
        "`checks[].label` 123개 중 distinct 112 — `켈로이드 체질 확인`, `항응고제/항혈소판제 복용 여부` 등이 여러 계열에 반복. `자가면역질환 여부` / `자가면역질환 여부 (육아종 위험)` / `(이물반응 위험)` 처럼 괄호 보충으로 갈라진 표기.",
    ]),
    ("problem-combos.json", [
        "고민 8개만 있다(P6·P8·P10·P12·P13·P14 없음). P3 이름이 `처짐/탄력`, P4 가 `피부결/톤/항노화` 로 taxonomy(`쳐짐`, `항노화`)와 다르다.",
        "`packages[].id` 가 `P1-1`, `P1-2` … 형식인데 taxonomy 의 problem 하위분류 id(`P1-1`=코, `P1-2`=이마/관자놀이)와 같은 문자열을 다른 뜻으로 쓴다.",
        "`procedures[]` 는 M 코드이지만 `products[]` 는 `나보타 or 보툴렉스`, `울쎄라(HIFU) 또는 올리지오(모노폴라 RF) + 보톡스 + 쥬비덤` 같은 자유 조합 문장 1개씩이다.",
        "`priceRange` 는 `5~8만`, `15~30만/회` 식 자유 텍스트(단위 `/회` 가 일부에만).",
        "`tier`(entry/recommended/premium/vip) 와 `tierLabel`(기본/표준/확장/종합)이 쌍으로 들어 있고, `productTier` 는 7종(`국산`, `수입`, `국산+수입 혼합`, `수입+국산`, `국산/수입`, `혼합`, `수입 프리미엄`).",
        "키 이름이 camelCase(salesPitch, upsellHook, clinicalRationale …).",
    ]),
    ("problem-packages.json", [
        "`complaints[].cc` 115개가 taxonomy problem 항목 117개와 이름으로 대응한다 — taxonomy 에만 있는 것 2개(`P4:줄기세포치료`, `P8:경화요법`), packages 에만 있는 것 0. 단 cc 쪽엔 taxonomy 항목 id(`auto-63-…`)가 없다.",
        "`cc_group` 이 taxonomy 하위분류 label 과 다른 곳 2건(P9 `니들RF`: cc_group `여드름흉터` vs taxonomy `튼살`; P9 `프락셔널레이저`: `수술흉터/화상흉터` vs `튼살`). cc 이름이 P9 안에서 중복되어 생긴 대응.",
        "`procedures[].name` 29종이 M 코드 15개에 매핑되는데 한 코드에 여러 이름(M8: 레이저/프락셔널/서브시전/혈관레이저/제모레이저/피코레이저, M15: 반영구화장/메디컬스킨케어/약물치료/병변내 스테로이드주사/모발이식, M9: 리프팅기기/인모드/미라드라이, M14: 크라이오/지방분해, M16: 수액/미백주사). `리프팅기기` 는 taxonomy `기기 리프팅` 과 표기가 다르다.",
        "`procedures[].products` 가 254건 중 47건 빈 배열. `combos` 가 1건 빈 배열.",
        "`products[]` 34종 중 products.json 에 없는 것 4: `헤어맥스(LLLT)`, `트리암시놀론(±5-FU)`, `PDL(V빔)`, `CO2레이저`. `리쥬란 힐러`·`셀피아`·`프락셀`·`시크릿` 등 10여 종은 products.json 엔 있으나 taxonomy 항목(items) 이름으로는 없음(§3.5).",
        "`combos[].combo[]` 멤버 이름에 `MTS`, `바이오스티뮬레이터`, `필링` 처럼 `procedures[].name` 에 없는 표기가 섞여 있다.",
        "`cc` 115 중 distinct 107 — `아그네스`, `스킨보톡스`, `프락셔널레이저`, `니들RF`, `서브시전`, `브이올렛` 이 다른 고민에 중복(taxonomy 도 같음).",
    ]),
    ("procedure-comparison.json", [
        "`comparisons[].id` 는 영문 슬러그 9개(lifting, wrinkle, volume, skin_texture, pigment, hair_removal, body_contouring, acne, rejuvenation) — treatment-optimization 의 `icon`(wrinkle, lifting, volume, texture, pigment, acne, laser, body)과 비슷하나 다른 집합.",
        "`procedures[].name` 은 브랜드+괄호 설명(`울쎄라 (HIFU)`, `써마지FLX (RF)`), `category` 는 M 코드. `히알루론산 필러` 가 두 비교에 중복.",
        "`pain` 은 `★★★☆☆` 별 문자열 4종, `pih_risk` 는 very_low/none/low/moderate/high 5종(pih-risk.json 의 5단계와 달리 `none` 이 있고 `very_high` 가 없음).",
        "`cost_range`·`downtime`·`onset`·`duration` 모두 자유 텍스트(`100-400만원`, `즉시 + 3개월 점진`).",
        "`evidence_notes[]` 는 9개 중 3개에만, `asian_skin_note` 는 39개 중 2개에만.",
        "M10 자리에 `리포셀 (HIFU 지방)`, M9 에 `IPL (광선치료)`·`IPL 제모`·`바넬라 (고주파 바디)`, M17 에 `엑소좀 (줄기세포 유래)` 가 들어 있다(코드-이름 대응을 그대로 적음).",
    ]),
    ("procedure-profiles.json", [
        "17개 계열 전부. 불리언 5개(hasProtein/hasHA/usesGel/createsWound/createsChannel)·정수 점수 3개(thermalLoad·bleedingRisk·swellingRisk, 0~3)·정수 시간 3개(prepTime, durationMin, durationMax).",
        "`phase` 9종 + `phaseOrder` 정수인데 phaseOrder 가 중복된다(95: M6·M15, 90: M7·M16, 85: M9·M14).",
        "`mechanism[]` 12종 중 `regenerative`(M3·M4·M5·M6) 와 `regeneration`(M17) 이 따로 있다.",
        "`needsAnesthesia` 6종(none, topical, topical_or_block, topical_or_none, block, block_or_sedation), `position` 2종.",
        "`name` 표기: M5 `PRP/엑소좀`, M9 `에너지기기(HIFU/RF)` (market-pricing 과 같고 taxonomy 와 다름).",
        "키 이름 camelCase 16개로 가장 많다.",
    ]),
    ("products.json", [
        "섹션 키 8개가 영문 슬러그(botulinum_toxin, filler_ha, …)이고 안에 `category_id` 가 있다. `energy_device.category_id` 만 배열 `[M8, M9, M11]`, 나머지는 문자열 — 같은 키에 타입이 다르다.",
        "섹션마다 제품 키가 다르다: `mfds` 가 energy_device 18개엔 아예 없음, `ingredient`(biostimulator 6·skin_booster 3), `material`(thread_lift), `type`(energy_device·prp_exosome·stem_cell), `note`/`legal_warning`/`regulatory_status`(일부).",
        "자리표시자 `-` 가 있다: skin_booster `스킨보톡스` 의 manufacturer·country 가 `-`(note: `보톡스 희석 피내주사법 (별도 제품 아님)`).",
        "`mfds: false` 6건(스킨보톡스, 벨피엔, ASCEplus, EXOSOME SKIN, 큐어스킨, 에스에프).",
        "taxonomy `modality[].products` 와 비교: M1 에 products.json 은 `티엠버스`, taxonomy 는 `타임버스`(같은 제품의 다른 표기로 보이는 쌍, 판정 아님); M2 taxonomy 에만 `신펄`; energy_device 의 `볼뉴머` 는 products.json 에만(§3.5).",
        "제조사 `클래시스` 와 `클래시스(Classys)` 두 표기.",
    ]),
    ("synergy.json", [
        "`from`/`to` 가 `M1-보톡스`, `M9-울쎄라`, `M4-쥬베룩` 처럼 코드+이름 합성 문자열이고, 별도로 `from_category`/`to_category` 에 코드가 또 있다. 합성 문자열의 코드 접두와 category 가 어긋난 건 0.",
        "노드 이름 52종은 계열명·제품명·부위 변형이 섞여 있다(`M1-보톡스` / `M1-사각턱보톡스` / `M1-보톡스(코끝)`, `M9-인모드` / `M9-인모드(바디)`, `M12-MTS` / `M12-MTS(두피)`).",
        "`type` 3종(함께 50 / 다음에 49 / 대신 16). `target` 17종에 `안티에이징`/`안티에이징 패키지`, `흉터`/`흉터/재생`, `색소`/`색소/미백`, `여드름`/`여드름/모공` 처럼 비슷한 값이 따로 있다.",
        "링크는 방향이 있고(from→to) 115개 전부 `reason` distinct. `timing` 53종 자유 텍스트.",
    ]),
    ("taxonomy.json", [
        "`version`/`updated` 메타 없음. 잎 키 87개로 가장 많다.",
        "`modality[]` 에 `category` 와 `name` 이 둘 다 있고 17개 전부 같은 값.",
        "항목 id 체계가 세 가지: `M1-2-1` 형(128개), `auto-M4-1775362490962` 형(322개), `auto-63-1774737181584` 형(62개), `auto-M16-DCA-<timestamp>` 형 9개(M3 hADM 1, M16 DCA 8). 하위분류 id 도 `M1-2` 형 56개 외에 `M3-new-1774324237649`, `auto-new-M4-1775360442`, `M9-SIG`, `M15-도포`, `M16-DCA`, `auto-1775361777` 등 18개. problem 항목 id 는 117개 전부 `auto-#-timestamp` 형.",
        "항목 `extracted` 의 하위 키 표기가 갈린다: `safety.common`(521) 외에 `safety.common_adverse_effects`(2), `safety.serious_adverse_effects`(2), `safety.contraindications`(4), `safety.long_term`(1), `safety.note`(4); `onset_duration.peak`(7) 와 `peak_effect`(8), `maintenance`(1); `indications.extended`(4) 와 `secondary`(9). products[].extracted 에는 `safety.common_side_effects`(4), `onset_duration.diffusion`(1)도 있다.",
        "`modality[].products` 는 M6·M10·M12·M13·M14·M15·M16 7개 계열에서 빈 배열. `products[].mfds` 는 59개 중 17개 null(M8·M9·M11 기기 전부).",
        "항목 `detail` 빈 문자열 20개(PDO, PCL, PLCL, 알라딘필링, 셀레늄 …). `subcategories[].items` 빈 배열 2개(`M15-도포`, `M15-팩`). `subcategories[].label` 중복 `기타`, `추가`.",
        "항목 이름 중복: `볼뉴머` 가 M4(auto-M4-…, `classification_issue` 플래그) 와 M9-2-3 두 곳. 원장 안에 이미 교정 메모 키가 있다 — `classification_issue`(2), `reclassified_to`(1: 소프라노 티타늄 → M8), `correction_note`(1: 리팟), `verification_needed`(1: 톡스온), `is_marketing_name`+`canonical_category`+`naming_caveat`(6: 꿀광주사·아기주사·벨벳주사·백옥주사·마늘주사·신데렐라주사).",
        "`modality[].extracted` 는 extracted.json 과 본문이 같거나(9) 일부 다르며(8), extracted.json 의 메타 키(name_en, source, procedure_id 등)는 없다.",
        "`problem[].subcategories[].items[].modality_ref` 는 117개 중 26개가 빈 배열(반영구·약물치료·서브시전·윤곽주사·지방분해주사·미녹시딜·FUE/FUT·미라드라이 등). 참조 코드는 전부 M1~M17 안에 있다.",
        "problem 항목 이름 중복 6건(아그네스, 스킨보톡스 → P6·P7 / 프락셔널레이저, 니들RF → P7·P9(2곳) / 서브시전 → P7·P9 / 브이올렛 → P11·P12).",
        "P3 의 category 가 `쳐짐`(다른 파일은 `처짐/탄력`, `처짐`).",
    ]),
    ("treatment-optimization.json", [
        "M/P 코드가 전혀 없다. `concern` 8개(주름 개선, 처짐/탄력, 볼륨 손실, 피부결/모공, 색소/기미, 여드름/흉터, 제모, 바디컨투어링)는 taxonomy 고민 14개와 이름이 다르고 1:1 대응이 아니다.",
        "`optimal_combo[]` 57종이 전부 자유 텍스트(`스킨부스터(리쥬란)`, `HIFU(슈링크/울쎄라)`, `HIFU(울쎄라/슈링크)`, `실리프팅(PDO/PCL)`/`실리프팅(PCL/PDO)`, `다이오드 레이저(810nm)`/`다이오드(810nm)` 처럼 순서·괄호만 다른 쌍 다수).",
        "`severity_levels[].level` 은 `경미 (fine lines)` 처럼 등급+설명 합성 문자열 24종. `evidence_level` 2종(high 13 / moderate 11). `total_duration` 9종 문자열(`12-18개월 + 유지` 포함).",
        "`contraindicated_combos` 11건 빈 배열, `caveats` 1건만.",
        "`combination_rules[].priority` 4종(critical/important/moderate/caution), `consensus` 3종(`3/3 AI 합의`, `2/3 AI 합의 (제한적 근거)`, `근거 기반 임상 권고`).",
        "`annual_plans[].schedule[].procedures[]` 는 `토닝 4회`, `IPL(가을 색소 관리)` 같은 횟수·계절 섞인 문장.",
        "`by_age_group[].upgrade`(3/4)·`note`(1/4) 일부에만.",
    ]),
    ("treatment-sequence.json", [
        "`sequence_order[].categories[]` 19개가 `M15-클렌징`, `M9-HIFU`, `M8-토닝`(코드+라벨 합성), `M11`·`M2`(코드만), `국소마취`·`연고마취`(코드 없음) 세 형식이 섞여 있다. `M15-클렌징`·`M15-도포`·`M15-LED`·`M15-팩` 중 taxonomy 하위 id 로 실존하는 건 `M15-도포`·`M15-팩` 뿐.",
        "`incompatible_same_day[].pair[]` 는 길이 1~2 배열(1건은 `HA 필러 주입 후 RF/HIFU` 한 문장). 이름은 자유 텍스트(`CO2 프락셔널`, `심부 필링(페놀)`, `이소트레티노인 복용 중`).",
        "`minimum_intervals` 의 기간 단위가 `min_days`(7건) 와 `min_months`(2건) 로 갈린다. `from`/`to` 는 자유 텍스트(`필러 (별도 세션)`, `필러 (동일 부위 재시술)`).",
        "`common_combos[].sequence[]` 는 `슈링크 HIFU`, `보톡스 이마/미간`, `ALA 도포·배양` 처럼 제품·부위·단계가 섞인 문장.",
        "`principles[]` 13개 문장과 treatment-optimization `combination_rules` 가 같은 주제(열시술→주사 순서, 필러→RF 14일)를 다른 문장으로 담고 있다.",
    ]),
])

QUESTIONS = [
    # 식별자·정본
    "계열(M1~M17)·고민(P1~P14) 코드와 이름의 정본은 `taxonomy.json` 인가? 다른 파일의 다른 표기(`기기 리프팅`/`기기리프팅`/`리프팅기기`/`에너지기기(HIFU/RF)`, `처짐/탄력`/`쳐짐`/`처짐`, `PRP/자가혈`/`PRP/엑소좀`/`PRP 피부재생술`)는 taxonomy 쪽으로 맞추는 것으로 보면 되는가, 아니면 파일별 표기에 의미 차이가 있는가?",
    "`extracted.json` 과 `taxonomy.json › modality[].extracted` 가 8개 계열에서 본문이 다르다(M2·M3·M5·M8·M10·M12·M13·M17). 어느 쪽이 최신/정본인가? `extracted.json` 에만 있는 메타(`source`, `source_type`, `procedure_id`, `extracted_at`)는 필요한가?",
    "`products.json` 과 `taxonomy.json › modality[].products` 가 59개로 같은 수이지만 `티엠버스`/`타임버스`, `신펄`, `볼뉴머` 에서 다르다. 제품 목록의 정본은 어느 쪽인가? taxonomy 쪽에는 `extracted` 본문이 붙어 있고 products.json 쪽에는 `mfds`·`type` 등이 더 있는데 둘을 합칠 것인가?",
    "taxonomy 항목 id 가 `M1-2-1` 형(128) / `auto-M4-<timestamp>` 형(322) / `auto-63-<timestamp>` 형(62) / 기타(9) 로 섞여 있고, problem 항목은 전부 `auto-#-<timestamp>` 다. 이 id 들은 외부(앱·DB)에서 이미 참조되고 있어 그대로 보존해야 하는가, 실버에서 새 키를 발급해도 되는가?",
    "`pih-risk.json › procedure_ref` 가 항목(M8-1-1)·하위분류(M8-5)·계열(M12) 세 깊이를 섞어 가리키고, 2건에 같은 ref 가 중복된다. 이 참조의 단위를 하나로 맞출 것인가, 아니면 「가장 구체적인 수준」을 그대로 두는가?",
    "`problem-combos.json › packages[].id`(P1-1, P1-2 …) 가 taxonomy 의 problem 하위분류 id 와 같은 문자열을 다른 뜻으로 쓴다. 이 패키지 id 를 외부에서 쓰고 있는가? 바꿔도 되는가?",
    "`post-procedure-timeline.json` 의 `category` 값 `M16-DCA` 와, `treatment-sequence.json` 의 `M15-클렌징`·`M9-HIFU`·`M8-토닝` 같은 코드+라벨 합성값은 taxonomy 하위분류를 가리키려는 의도인가? (`M15-도포`·`M15-팩`·`M16-DCA` 는 taxonomy 하위분류 id 로 실존하지만 나머지는 없다.)",
    "`synergy.json` 의 노드(`M1-보톡스`, `M1-사각턱보톡스`, `M9-울쎄라`, `M4-쥬베룩`)는 계열·시술·제품 어느 단위인가? 실버에서 노드를 taxonomy 항목/제품에 연결해야 하는가, 아니면 계열 코드(from_category/to_category)까지만 쓰는가?",
    "`problem-packages.json` 의 `complaints[].cc` 는 taxonomy problem 항목 이름과 113/115 가 일치하지만 id 가 없다. 이름으로 붙여도 되는가? 이름이 중복되는 6개(아그네스, 스킨보톡스, 프락셔널레이저, 니들RF, 서브시전, 브이올렛)와 P9 의 `cc_group` 불일치 2건은 어느 쪽이 맞는가?",
    "`problem-packages.json › procedures[].name` 29종(레이저/프락셔널/서브시전/혈관레이저 … → 전부 M8)은 계열보다 세밀한 「시술 종류」 층으로 보인다. 이 층을 실버에 별도 엔티티로 둘 것인가, taxonomy 하위분류에 대응시킬 것인가? 대응표는 누가 주는가?",
    # 자유 텍스트 시술명
    "`treatment-optimization.json`(optimal_combo 57종)·`treatment-sequence.json`(pair/sequence/from/to)·`procedure-comparison.json`(name 39)·`market-pricing.json`(items.name 122)·`problem-combos.json`(products 문장)의 시술/제품명은 전부 자유 텍스트다. 실버에서 이들을 코드로 연결해야 하는가? 연결한다면 대응표를 사람이 주는가, 아니면 연결하지 않고 문장으로 둔 채 쓰는가?",
    "`treatment-optimization.json › by_concern[].concern` 8개와 `procedure-comparison.json › comparisons[].id` 9개는 taxonomy 고민 14개와 1:1 이 아니다(주름 개선 ↔ P2 는 되지만 바디컨투어링·볼륨 손실·rejuvenation 등은 어디로?). 고민 축의 정본을 taxonomy P 로 볼 것인가, 아니면 이 파일들의 분류를 별개 축으로 두는가?",
    # 비어 있는 것
    "`literature-evidence.json` 에서 M6·M10·M11·M13·M14 는 세 섹션 전부 비어 있고, `complications.json` 은 10개 계열, `post-procedure-timeline.json` 은 10개 시술, `contraindications.json` 은 11개 계열, `problem-combos.json` 은 8개 고민만 다룬다. 빠진 계열/고민은 「없음」으로 둘 것인가, 채워질 예정인가?",
    "`taxonomy.json › problem[].…items[].modality_ref` 가 26개 항목에서 빈 배열(반영구화장, 약물치료, 미녹시딜, FUE/FUT, 미라드라이 등)이다. 이 항목들은 M 계열 밖의 시술로 두는가, 새 계열이 필요한가?",
    "`complications.json › risk_factors` 46/65 빈 배열, `problem-packages.json › procedures[].products` 47/254 빈 배열, `treatment-optimization.json › contraindicated_combos` 11/24 빈 배열, taxonomy `products` 7개 계열 빈 배열. 빈 배열은 「해당 없음」인가 「미입력」인가? 구분이 필요하면 원장 쪽에서 표시해 줄 수 있는가?",
    "`taxonomy.json › modality[].products[].mfds` 가 기기 17개에서 null 이고, `products.json` 의 energy_device 18개에는 `mfds` 키 자체가 없다. 기기는 mfds 허가 개념을 쓰지 않는 것인가(=null 유지), 아니면 미입력인가?",
    # 타입·표기
    "`extracted.json › safety.serious` 가 M10·M13 에서 null, 나머지는 배열이다. null 은 「심각 부작용 없음」인가 「미입력」인가?",
    "`products.json` 의 `스킨보톡스` 는 manufacturer/country 가 `-` 이고 note 에 「별도 제품 아님」이라고 되어 있다. 제품 목록에 유지하는가?",
    "`literature-evidence.json › patient_ko` 41개에 `[1][2]` 각주 번호가 남아 있고 `patient_ja` 5건·`patient_en` 1건에 한글이 섞여 있다. 실버에서 이 문자열을 정제해도 되는가(원문 보존이 필요한가)?",
    "taxonomy 항목 `extracted` 하위 키가 갈려 있다(`safety.common` vs `common_adverse_effects` vs `common_side_effects`, `onset_duration.peak` vs `peak_effect`, `indications.extended` vs `secondary`). 같은 뜻으로 합쳐도 되는가? `secondary` 와 `extended` 는 다른 뜻인가?",
    "`procedure-profiles.json › mechanism[]` 의 `regenerative`(M3·M4·M5·M6) 와 `regeneration`(M17), `phaseOrder` 중복(95: M6·M15 / 90: M7·M16 / 85: M9·M14)은 의도인가?",
    "`treatment-sequence.json › minimum_intervals` 의 `min_days`/`min_months` 두 단위, `market-pricing.json › unit` 17종, `problem-combos.json › priceRange` 의 `/회` 유무 — 단위를 정규화해도 되는가, 원문 단위를 보존해야 하는가?",
    "taxonomy 안에 이미 교정 메모 키가 있다(`classification_issue` 2, `reclassified_to` 1, `correction_note` 1, `verification_needed` 1, `is_marketing_name` 6). 실버는 이 메모대로 재분류된 결과를 담는가(예: 소프라노 티타늄 → M8, 볼뉴머 M4 항목 제거), 아니면 원장 위치를 그대로 두고 메모만 옮기는가?",
    "`anatomy-danger-zones.json` 의 부위 11개(forehead, glabella …)와 taxonomy problem 하위분류 라벨(코, 이마/관자놀이, 턱/턱선 …), `problem-packages.json › cc_group` 52종은 서로 다른 부위 어휘다. 부위를 실버의 축으로 둘 것인가? 둔다면 정본 어휘는 무엇인가?",
    "`version`/`updated` 가 파일마다 다르고(1.0~6.2, 2026-04-04~2026-09-03) taxonomy·extracted·complications 에는 없다. 실버가 원장 버전을 기록해야 하는가? 어느 날짜 스냅샷(`phub-stg-2026-10-26`)을 브론즈의 기준으로 보는가?",
]

# ---------- 렌더 ----------
L = []
P = L.append


def table(headers, rows):
    P("| " + " | ".join(headers) + " |")
    P("|" + "|".join("---" for _ in headers) + "|")
    for r in rows:
        P("| " + " | ".join(str(c) for c in r) + " |")
    P("")


P("# 원장 JSON 21개 컬럼(키) 구조 분석 리포트 — 브론즈")
P("")
P("- 작성일: 2026-11-03")
P("- 입력(읽기 전용): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/*.json` 21개")
P(f"- 방법: `bronze-ledger-column-scan.py` 로 21개 파일을 기계적으로 훑고, 결과 `bronze-ledger-column-scan.json` 에서 이 문서를 렌더(`bronze-ledger-column-report-render.py`). 셋 다 스크래치 디렉토리 `scratchpad/` 에 있다.")
P("- 표기 규약: 배열은 `[]`, 코드형 동적 키(M1, P1-2, M1-2-1, auto-63-…, M1_to_M7)는 `{code}` 로 접었다. 「잎 키」= 스칼라 또는 빈 배열/빈 객체가 놓이는 경로.")
P("- 이 문서는 **관찰만** 적는다. 어느 쪽이 맞다는 판정, 어떻게 고칠지의 설계는 하지 않는다. 기존 작업물(source-map, step*, DATA-001, `_archive/`)은 읽지 않았다.")
P(f"- 합계: 파일 21 · 잎 키 경로 {R['total_leaf_paths']} · 바이트 {sum(f['bytes'] for f in F.values()):,}")
P("")

# ===== 1. 요약 표 =====
P("## 1. 요약 표")
P("")
rows = []
for fn, d in F.items():
    tl = d["top_level"]
    if tl["kind"] == "object":
        if tl.get("dynamic_code_keys"):
            shape = "객체(최상위 키 = M 코드)"
        else:
            shape = f"객체(메타 {len(tl['meta'])} + 데이터 키 {len(tl['data'])})"
    else:
        shape = "배열"
    recs = []
    for p in MAIN_RECORDS[fn]:
        if p.startswith("("):
            if fn == "extracted.json":
                recs.append(f"{p} {len(d['dynamic_key_dicts'][''] ['keys'])}")
            elif fn == "literature-evidence.json":
                recs.append(f"{p} {d['dynamic_key_dicts']['categories']['n_keys']}")
            elif fn == "products.json":
                recs.append("섹션 8")
        elif p == "*.products":
            recs.append("products " + str(sum(v["records"] for k, v in d["record_sets"].items() if k.endswith(".products"))))
        else:
            rs = d["record_sets"].get(p)
            if rs:
                recs.append(f"{p.split('.')[-1].split('[]')[-1] or p} {rs['records']}")
            elif p in d["arrays"]:
                recs.append(f"{p} {d['arrays'][p]['total']}")
    rows.append([f"`{fn}`", f"{d['bytes']:,}", shape, " / ".join(recs), d["leaf_count"], DESC[fn]])
table(["파일", "바이트", "최상위 형태", "레코드 수", "잎 키", "한 줄 설명"], rows)

P("메타 키 현황(`version`/`updated`):")
P("")
table(["파일", "version", "updated"], [[f"`{fn}`", v["version"] or "—", v["updated"] or "—"] for fn, v in CC["version_updated"].items()])
P("키 표기 스타일(camelCase 키가 있는 파일):")
P("")
table(["파일", "키 수", "camelCase 키"], [[f"`{fn}`", v["n_keys"], ", ".join(f"`{k}`" for k in v["camelCase"])] for fn, v in CC["key_casing"].items() if v["camelCase"]])

# ===== 2. 파일별 절 =====
P("## 2. 파일별 절")
P("")
for i, (fn, d) in enumerate(F.items(), 1):
    P(f"### 2.{i} `{fn}` — {d['bytes']:,}B · 잎 키 {d['leaf_count']}")
    P("")
    P(DESC[fn])
    P("")
    P("**최상위 구조**")
    P("")
    tl = d["top_level"]
    if tl["kind"] == "object":
        if tl.get("dynamic_code_keys"):
            P(f"- 객체. 최상위 키가 전부 코드: {', '.join(d['dynamic_key_dicts']['']['keys'])}")
        else:
            if tl["meta"]:
                P("- 메타 키: " + ", ".join(f"`{m['key']}`=`{esc(m['value'])}`" for m in tl["meta"]))
            P("- 데이터 키: " + ", ".join(f"`{x['key']}` ({x['kind']}, {x['size']})" for x in tl["data"]))
    dyn = {k: v for k, v in d["dynamic_key_dicts"].items() if k != ""}
    if dyn:
        for k, v in dyn.items():
            P(f"- 동적 코드 키 객체 `{k}`: {v['n_keys']}개 — {', '.join(v['keys'][:20])}")
    if d["arrays"]:
        arr = [f"`{p}`×{v['n_arrays']}(len {v['min']}~{v['max']}, 합 {v['total']})" for p, v in d["arrays"].items()]
        P("- 배열: " + ", ".join(arr))
    P("")
    P("**잎 키 표**")
    P("")
    rows = []
    for p, s in d["leaf_paths"].items():
        types = ",".join(f"{t}" for t in s["types"])
        rows.append([f"`{p}`", types, s["count"], s["null"], s["empty"], s["distinct_n"], ex_join(s["examples"])])
    table(["경로", "타입", "횟수", "null", "빈값", "distinct", "예시"], rows)
    enums = [(p, s) for p, s in d["leaf_paths"].items() if s.get("enum_like")]
    P("**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)")
    P("")
    if enums:
        table(["경로", "distinct 값 (횟수)"], [[f"`{p}`", ", ".join(f"`{esc(v['v'])}`({v['n']})" for v in s["enum_values"])] for p, s in enums])
    else:
        P("- 없음")
        P("")
    P("**식별자 후보** (레코드 배열별)")
    P("")
    rows = []
    for p, rs in d["record_sets"].items():
        for c in rs["candidates"]:
            dup = ", ".join(f"`{esc(x)}`" for x in c["duplicates"][:6]) if c["duplicates"] else ""
            rows.append([f"`{p}`", rs["records"], f"`{c['key']}`", c["present"], c["distinct"], "○" if c["unique"] else "✗", dup])
    if rows:
        table(["레코드 배열", "건수", "키", "존재", "distinct", "유일", "중복 예"], rows)
    else:
        P("- 없음(식별자 키 없음)")
        P("")
    sparse = [(p, rs) for p, rs in d["record_sets"].items() if rs["sparse_keys"]]
    if sparse:
        P("**일부 레코드에만 있는 키**")
        P("")
        table(["레코드 배열", "건수", "키=존재수"], [[f"`{p}`", rs["records"], ", ".join(f"`{k}`={v}" for k, v in rs["sparse_keys"].items())] for p, rs in sparse])
    P("**관찰** (원장 자체에서 보이는 것. 판정 아님)")
    P("")
    auto = [o for o in d["observations"] if not o.startswith("일부 레코드에만")]
    for o in auto:
        P(f"- (기계) {o}")
    for o in OBS[fn]:
        P(f"- {o}")
    P("")

# ===== 3. 교차 식별자 =====
P("## 3. 교차 식별자 표")
P("")
P("### 3.1 계열 코드 M1~M17 × 파일 (코드가 값·키·접두로 등장하면 ○)")
P("")
files = list(F.keys())
short = {fn: fn.replace(".json", "") for fn in files}
hdr = ["코드", "taxonomy 이름"] + [short[f] for f in files if f not in ("anatomy-danger-zones.json", "treatment-optimization.json")]
rows = []
for code, per in CC["modality_file_matrix"].items():
    rows.append([code, EX["canonical_modality_names"][code]["ko"]] + [("○" if per[f] else "") for f in files if f not in ("anatomy-danger-zones.json", "treatment-optimization.json")])
table(hdr, rows)
P("`anatomy-danger-zones.json`·`treatment-optimization.json` 에는 M/P 코드가 전혀 없다. `pih-risk.json` 의 `notes.M1_to_M7` 은 범위 키라 M1~M7 열에 세지 않았다(위 표의 pih-risk 열은 `procedures[].category`·`procedure_ref` 기준).")
P("")

P("### 3.2 고민 코드 P1~P14 × 파일")
P("")
pfiles = ["taxonomy.json", "problem-packages.json", "problem-combos.json"]
rows = []
for code, nm in EX["canonical_problem_names"].items():
    cov = CC["code_coverage_by_file"].get(code, [])
    rows.append([code, nm["ko"]] + [("○" if f in cov else "") for f in pfiles])
table(["코드", "taxonomy 이름"] + [short[f] for f in pfiles], rows)

P("### 3.3 코드가 쓰인 키 경로 (파일별)")
P("")
rows = []
for fn in files:
    paths = OrderedDict()
    for code, v in R["cross_codes"].items():
        if fn in v["files"]:
            for p in v["files"][fn]:
                paths[p] = paths.get(p, 0) + v["files"][fn][p]
    if paths:
        rows.append([f"`{fn}`", "<br>".join(f"`{p}` ({n})" for p, n in paths.items())])
table(["파일", "코드가 나오는 경로 (등장 횟수)"], rows)

P("### 3.4 계열 코드 → 이름 표기 (파일별로 코드 옆에 붙은 이름을 그대로)")
P("")
rows = []
for code, per in CC["modality_names_by_file"].items():
    cells = []
    for fn, names in per.items():
        cells.append(f"{short[fn]}: " + " / ".join(f"`{esc(n)}`" for n in names))
    rows.append([code, EX["canonical_modality_names"][code]["ko"], "<br>".join(cells)])
table(["코드", "taxonomy", "파일별 표기"], rows)

P("### 3.5 제품명 교차")
P("")
P("`products.json` 섹션 vs `taxonomy.json › modality[].products`:")
P("")
table(["섹션", "category_id", "공통", "products.json 에만", "taxonomy 에만"],
      [[k, v["category_id"], v["common"], ", ".join(v["products_json_only"]) or "—", ", ".join(v["taxonomy_only"]) or "—"] for k, v in CC["products_json_vs_taxonomy_products"]["by_section"].items()])
P("`problem-packages.json › procedures[].products[]` 34종의 소재:")
P("")
table(["제품명", "횟수", "products.json", "taxonomy products", "taxonomy items"],
      [[esc(x["name"]), x["n"], "○" if x["in_products_json"] else "", "○" if x["in_taxonomy_products"] else "", "○" if x["in_taxonomy_items"] else ""] for x in CC["problem_packages_products"]])
P("`problem-combos.json › packages[].products[]` 는 조합 문장 1개씩(24건)으로 제품명 단위가 아니다:")
P("")
for x in CC["problem_combos_products_values"]:
    P(f"- `{esc(x['v'])}`" + (f" ×{x['n']}" if x["n"] > 1 else ""))
P("")

P("### 3.6 하위 코드 참조")
P("")
P("`pih-risk.json › procedure_ref` → taxonomy:")
P("")
table(["procedure_ref", "pih name", "taxonomy 항목?", "taxonomy 하위분류?", "taxonomy 항목 이름"],
      [[x["procedure_ref"], esc(x["name"]), "○" if x["in_taxonomy_items"] else "", "○" if x["in_taxonomy_subcategories"] else "", x["taxonomy_item_name"] or "—"] for x in CC["pih_procedure_ref_check"]])
P("중복 ref: " + ", ".join(f"`{k}`×{v}" for k, v in CC["pih_procedure_ref_duplicates"].items()))
P("")
P("`problem-combos.json › packages[].id` 와 같은 문자열의 taxonomy problem 하위분류:")
P("")
table(["package id", "package name", "taxonomy 하위분류 label(같은 id)"], [[x["package_id"], esc(x["package_name"]), x["taxonomy_subcategory_label"] or "(없음)"] for x in EX["problem_combos_package_id_vs_taxonomy_subcategory_id"]])
P("`treatment-sequence.json › sequence_order[].categories[]` 값: " + ", ".join(f"`{x}`" for x in CC["treatment_sequence_names"]["sequence_categories"]))
P("")
P("`post-procedure-timeline.json › timelines[]` (category:name):" )
P("")
for x in CC["timeline_categories"]:
    P(f"- {x}")
P("")

P("### 3.7 `extracted.json` vs `taxonomy.json › modality[].extracted`")
P("")
table(["코드", "본문 동일", "다른 키", "extracted.json 에만 있는 키"],
      [[c, "○" if v["identical_core"] else "✗", ", ".join(v["differing_keys"]) or "—", ", ".join(v["extracted_only_keys"])] for c, v in CC["extracted_vs_taxonomy_extracted"].items()])

P("### 3.8 `problem-packages.json › cc` vs `taxonomy.json › problem 항목`")
P("")
v = CC["problem_packages_cc_vs_taxonomy_items"]
P(f"- taxonomy 항목 {v['taxonomy_items']} / packages cc {v['packages_cc']} (problem_id+이름 쌍 기준)")
P(f"- taxonomy 에만: {', '.join(v['only_in_taxonomy'])}")
P(f"- packages 에만: {', '.join(v['only_in_packages']) or '없음'}")
for m in v["cc_group_vs_subcategory_label_mismatch"]:
    P(f"- cc_group ≠ taxonomy label: {m['problem_id']} `{m['cc']}` — packages `{m['cc_group']}` / taxonomy `{m['taxonomy_label']}`")
P(f"- problem-combos 가 다루는 고민: {', '.join(x['problem_id'] + ' ' + x['problem'] + ('(taxonomy: ' + x['taxonomy_category'] + ')' if x['taxonomy_category'] != x['problem'] else '') for x in CC['problem_combos_problems'])}; 없는 고민: {', '.join(CC['problem_combos_missing_problems'])}")
P("")
P("`problem-packages.json › procedures[].name` → category 코드 (한 코드에 여러 이름):")
P("")
table(["name", "횟수", "category", "taxonomy category 이름"], [[esc(x["name"]), x["n"], ", ".join(x["categories"]), ", ".join(str(v) for v in x["taxonomy_category_of_code"].values())] for x in CC["problem_packages_procedure_names"]])

P("### 3.9 시술명이 자유 텍스트인 자리")
P("")
P("- `synergy.json` 노드 52종: " + ", ".join(f"`{x['v']}`" for x in CC["synergy_node_names"]))
P("- `treatment-optimization.json › optimal_combo[]` 57종: " + ", ".join(f"`{esc(x['v'])}`" for x in CC["treatment_optimization_optimal_combo_values"]))
P("- `treatment-optimization.json › by_age_group[].recommended_base[]`: " + ", ".join(f"`{x}`" for x in CC["treatment_optimization_age_values"]["recommended_base"]))
P("- `treatment-sequence.json › incompatible_same_day[].pair[]`: " + ", ".join("`" + " ↔ ".join(p) + "`" for p in CC["treatment_sequence_names"]["incompatible_pairs"]))
P("- `treatment-sequence.json › minimum_intervals[]` from→to: " + ", ".join(f"`{x['from']}` → `{x['to']}`" for x in CC["treatment_sequence_names"]["minimum_intervals"]))
P("- `procedure-comparison.json › procedures[].name` 39종 (category): " + ", ".join(f"`{esc(x['name'])}`({x['category']})" for x in CC["procedure_comparison_procedures"]))
P("")

P("### 3.10 표기 변형 목록 (띄어쓰기·괄호·영/한·대소문자만 다른 것; 이름류 키의 24자 이하 값)")
P("")
P("정규화(소문자·괄호 제거·공백/구분자 제거)가 같은데 표면형이 2개 이상인 것. **같은 것이라는 판정이 아니다** — 괄호 안이 부위·용량·제품을 구분하는 경우도 함께 섞여 있다.")
P("")
rows = []
for n, forms in R["surface_variants"].items():
    cells = []
    for f, per in forms.items():
        fl = sorted({fn.replace(".json", "") for fn in per})
        cells.append(f"`{esc(f)}` [{', '.join(fl)}]")
    rows.append([esc(n), "<br>".join(cells)])
table(["정규화 키", "표면형 [파일]"], rows)

# ===== 4. 다국어 =====
P("## 4. 다국어 필드 표")
P("")
rows = []
for fn, paths in R["lang_paths"].items():
    for p in paths:
        s = F[fn]["leaf_paths"][p]
        rows.append([f"`{fn}`", f"`{p}`", s["count"], ex_join(s["examples"][:2])])
table(["파일", "경로", "횟수", "예시"], rows)
P("- 4개 국어(ko/en/zh/ja)가 모두 있는 곳은 `literature-evidence.json` 의 `patient_*` 뿐(문장 119개 × 4). 나머지는 `name_en`/`category_en`/`concern_en`/`name_ko` 처럼 한글 본문 + 영문 라벨 1개.")
P(f"- `literature-evidence.json` patient_* 안의 각주 잔재 `[n]`: ko {EX['literature_patient_text_citation_remnants'].get('ko', 0)}건. 다른 언어 본문에 한글 섞임: " + ", ".join(f"{k} {v}건" for k, v in EX["literature_patient_text_hangul_in_other_lang"].items()) + " (예: " + ", ".join(f"`{esc(x)}`" for x in EX["literature_samples"].get("hangul_in_ja", [])[:2]) + ")")
P("- 영문 라벨끼리도 표기가 다르다: taxonomy `Botulinum Toxin` / procedure-profiles `Botulinum Toxin` / products `Botox` / extracted `Botulinum Toxin Type A` / literature `Botulinum toxin type A (aesthetic)`; M9 는 `Energy Based Device Lifting`(taxonomy) / `Non-invasive skin tightening: HIFU and radiofrequency`(literature) / extracted `name_en` 별도.")
P("")

# ===== 5. 질문 =====
P("## 5. 원장만 보고 드는 질문 (실버 설계 전에 물을 것)")
P("")
for i, q in enumerate(QUESTIONS, 1):
    P(f"{i}. {q}")
P("")

P("## 부록 A. 계열·고민 정준 이름 (taxonomy.json 기준)")
P("")
table(["코드", "category", "category_en", "group", "하위", "항목", "products"],
      [[c["id"], c["category"], EX["canonical_modality_names"][c["id"]]["en"], c["group"], c["subcategories"], c["items"], c["products"]] for c in CC["taxonomy_modality_counts"]])
table(["코드", "category", "category_en", "하위", "항목"],
      [[c["id"], c["category"], EX["canonical_problem_names"][c["id"]]["en"], c["subcategories"], c["items"]] for c in CC["taxonomy_problem_counts"]])
P("## 부록 B. taxonomy id 패턴")
P("")
table(["계열", "항목 id 패턴 (개수)"], [[m, ", ".join(f"`{k}`={v}" for k, v in c.items())] for m, c in CC["taxonomy_modality_item_id_patterns"].items()])
P("- 하위분류 id: " + ", ".join(f"`{k}`={v}" for k, v in CC["taxonomy_modality_subcategory_id_patterns"].items()))
P("- problem 항목 id: " + ", ".join(f"`{k}`={v}" for k, v in CC["taxonomy_problem_item_id_patterns"].items()) + " / products id: " + ", ".join(f"`{k}`={v}" for k, v in CC["taxonomy_product_id_patterns"].items()))
P("- 교정 메모 키가 붙은 항목: " + "; ".join(f"{x['modality']} `{x['name']}`({x['id']}: {', '.join(x['flags'])})" for x in EX["taxonomy_items_with_flags"]))
P("")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(OUT, len(L), "lines;", len(QUESTIONS), "questions")
