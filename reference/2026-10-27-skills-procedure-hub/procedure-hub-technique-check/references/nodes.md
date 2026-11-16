# 기법 노드 24 — 큰 기법 12 · 세부 12 (2층)

출처: `orchestration/work/phub-recommend/step4-decisions.json` `nodes[]` · 산출 `step4-techniques.json` `nodes[]`(판 v1 · 2026-10-28 · open 0) — 이 표는 그 값을 그대로 옮긴 것이다. 값이 바뀌면 결정 파일이 이긴다.
결정: `_RESUME.md` §2 10-28 「4단계 기법 조사 반영 — 전부 추천대로」 S1 · S2 · S3 · **J1 안 1**(노드 24 · 층 · 근육 · 펄스는 속성).

## 1. 표

「원천 표현」 = 이 노드로 간 표현 행 수(`bucket` 노드로). 「계열 기본(보조)」 = `family_defaults[]` 에서 이 노드를 기본 · 보조로 쓰는 계열. 「초안」 = `procedure-master-v3.json techniques` 중 유지 · 합침으로 이 노드에 온 것.

| id | 이름(상담 용어) | 상위 | 의학 용어(`medical_name`) | 계열 기본(보조) | 원천 표현(행) | 초안 유지 · 합침 | 근거(`basis`) |
|---|---|---|---|---|---|---|---|
| K01 | 주입 | — | injection | M1 · M2 · M3 · M5 · M6 · M17 · N1 | 7 | T01 근육축소 · T57 피하 주사 · T58 국소 주사 · T59 병변내 주사 · T61 주입 | mechanism injection(M1~M6 · M17) · group 주사/주입 · 계열 정의 「주사」「주입」(M1~M6 · M17 · N1) · DEC-002 D-02 예시 「근육 내 주입」「피하 주입」 |
| K01a | 메조테라피 | 주입 | mesotherapy — 진피 내 미세 다점 주입 | M4 | 6 | T02 스킨보톡스 · T33 멀티니들 · T55 메조테라피 · T56 진피 주입 | 문헌 M4 이름 「Skinboosters and mesotherapy」 · M4 정의 「진피에 소량씩 여러 점 주입」 · related_techniques 「메조보톡스 — 보톡스를 진피층에 소량 주사」「히알루론산 메조테라피(물광주사)」「메조리프트」「메조페시아」「메조테라피 — 피부에 직접 영양 성분 주입」 · D-02 예시 「진피 내 미세 주입(스킨보톡스)」 |
| K01b | 정맥 주사 | 주입 | intravenous | M16 | 1 | T60 정맥 주사 | mechanism intravenous(M16) · M16 정의 「정맥으로 투여」 · DEC-003 D-05 「수액 = 기법 「정맥 주사」」 |
| K01c | 무바늘 제트 주입 | 주입 | needle-free jet injection | (M4) | 1 | T34 니들리스 · T35 분사 | M4 정의 「(또는 무바늘 제트 주입)」(39544509 Delivery Methods) · step2 M4 deferred 「주입 기기 → 4단계」 |
| K02 | 삽입 | — | thread insertion | M7 | 1 | — | mechanism mechanical(M7) · M7 정의 「실을 피하에 넣어」 · 문헌 33469333 「inserted subcutaneously along a planned course」 |
| K02a | 코그실 삽입 | 삽입 | barbed (cog) thread | — | 0 | T18 코그 | 문헌 33469333 「Absorbable barbed threads … mechanically reposition」 · 원천 M7-2 하위 항목 「코그(Cog)」 |
| K02b | 모노실 삽입 | 삽입 | mono (smooth) thread | — | 0 | T19 모노 | 원천 M7-2 하위 항목 「모노」 · 문헌 33469333 「Thread insertion stimulates … collagen」(당김 없음) |
| K02c | 볼륨실 삽입 | 삽입 | volume thread | — | 0 | T20 볼륨실 | 원천 M7-2 하위 항목 「볼륨실」 |
| K03 | 미세침 천공 | — | microneedling (percutaneous) | M11 · M12 | 5 | — | mechanism mechanical(M12) · thermal+mechanical(M11) · createsChannel · M11/M12 정의 「미세침 … 찔러 / 미세 천공」 · 문헌 27559496 「micro-punctures」 |
| K04 | 조사 | — | irradiation (laser · IPL · LED) | M8 | 1 | — | mechanism thermal · ablative(M8) · M8 정의 「피부에 조사해」 |
| K04a | 토닝 | 조사 | laser toning (low-fluence multi-pass) | — | 3 | T04 토닝 | treatment-sequence 「M8-토닝」(레이저 단계 안에서 따로 부름) · 원천 항목 레이저토닝 · 피코토닝 · 알렉스토닝 · 제네시스토닝 |
| K04b | 프락셔널 | 조사 | fractional photothermolysis | — | 5 | T05 박피성 프락셔널 · T06 비박피성 프락셔널 · T07 프락셔널 | treatment-sequence 「M8-프락셔널」 · related_techniques 「프랙셔널 레이저」 · 문헌 32273965 「Fractional ablative / Non-ablative fractional lasers」 |
| K04c | 광역학 | 조사 | photodynamic therapy (PDT) | — | 1 | T50 광역학치료 | related_techniques 「PDT (광역학요법) — 광감작제 약물 + 레이저」 · 원천 항목 ALA-PDT |
| K05 | 에너지 가열 | — | non-invasive energy heating (HIFU · RF · microwave) | M9 | 1 | — | mechanism thermal(M9) · M9 정의 「피부를 뚫지 않고 … 가열」 · 문헌 37753689 HIFU · RF |
| K06 | 전자기 자극 | — | electromagnetic / electrical muscle stimulation | M10 | 1 | — | mechanism electromagnetic_stimulation(M10) · M10 정의 |
| K07 | 플라즈마 전달 | — | plasma energy delivery | M13 | 1 | — | mechanism plasma_energy(M13) · M13 정의 「피부 표면에 직접 전달」 |
| K08 | 냉각 | — | cooling (cryo) | M14 | 1 | T17 냉각 | mechanism cooling(M14) · M14 정의 「냉각해」 |
| K09 | 도포 | — | topical application | M15 · (M5) · (M17) | 2 | T41 중간~심층 · T42 심부필링 · T43 CROSS 기법 · T44 도포 | mechanism topical(M15) · treatment-sequence 「M15-도포」 · M5 · M17 정의 「주입·도포」 · source-map U5 |
| K10 | 침투 | — | transdermal delivery assist (iontophoresis · electroporation · sonophoresis) | (M15) | 2 | T36 초음파 주입 · T37 이온도입 · T38 전기천공 | mechanism infusion(M15) · treatment-sequence phase 「약물 도포/침투」 · 2단계 M15 하위 「흡수 보조 기기」 · related 「MTS + 약물 투입 — 경피 흡수 촉진」 |
| K11 | 박리·흡인 | — | mechanical exfoliation · suction | (M15) | 0 | T39 워터제트 · T40 미세박피 | 2단계 M15 하위 「기계적 박리·클렌징」 · treatment-sequence 「M15-클렌징」 |
| K12 | 소수술 | — | minor dermatologic procedure | — | 0 | — | 2단계 M15 deferred 「서브시전 · 면포압출 · 펀치 → 5단계 시술」 — 단위 시술이 되려면 기법 칸이 있어야 함 |
| K12a | 서브시전 | 소수술 | subcision | — | 2 | T46 섬유 밴드 절단 | 원천 항목 서브시전 detail 「섬유 밴드 절단」 · related 「진피절제주입법(서브시전 + 필러)」 |
| K12b | 펀치 | 소수술 | punch technique | — | 0 | T48 펀치이식 | 원천 항목 펀치시술 「펀치이식」 |
| K12c | 압출 | 소수술 | comedone extraction | — | 0 | T49 압출 | 원천 항목 면포압출 「압출」 |

## 2. 노드로 간 원천 표현(41행)

| 노드 | 파일#키 | 원문 | 판정 |
|---|---|---|---|
| K01 주입 | `profiles[M1].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M2].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M3].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M4].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M5].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M6].mechanism` | injection | 기법 노드 |
| K01 주입 | `profiles[M17].mechanism` | injection | 기법 노드 |
| K01a 메조테라피 | `modality[M1].extracted.related_techniques` | 메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과 | 기법 노드 근거 |
| K01a 메조테라피 | `modality[M2].extracted.related_techniques` | 히알루론산 메조테라피 (물광주사) — 피부 속 수분·탄력 개선 | 기법 노드 근거 |
| K01a 메조테라피 | `modality[M4].extracted.related_techniques` | 메조리프트 (Mesolift) -- 비타민과 히알루론산 주사로 리프팅 효과 | 기법 노드 근거 |
| K01a 메조테라피 | `modality[M4].extracted.related_techniques` | 메조보톡스 -- 보톡스를 진피층에 소량 주사해 모공/탄력 개선 | 기법 노드 근거 |
| K01a 메조테라피 | `modality[M4].extracted.related_techniques` | 메조페시아 (Mesopecia) -- 두피에 약물 주사해 탈모 치료 | 기법 노드 근거 |
| K01a 메조테라피 | `modality[M16].extracted.related_techniques` | 메조테라피 -- 피부에 직접 영양 성분 주입 | 기법 노드 근거 |
| K01b 정맥 주사 | `profiles[M16].mechanism` | intravenous | 기법 노드 |
| K01c 무바늘 제트 주입 | `modality[M1].extracted.related_techniques` | 에어보톡스 — 여드름 흉터 치료에 활용 | 기법 노드 근거 |
| K02 삽입 | `profiles[M7].mechanism` | mechanical | 기법 노드 |
| K03 미세침 천공 | `profiles[M11].mechanism` | thermal | 기법 노드 |
| K03 미세침 천공 | `profiles[M11].mechanism` | mechanical | 기법 노드 |
| K03 미세침 천공 | `profiles[M12].mechanism` | mechanical | 기법 노드 |
| K03 미세침 천공 | `modality[M5].extracted.related_techniques` | MTS + PRP — MTS로 미세 구멍을 낸 후 PRP를 도포해 흡수 촉진 | 기법 노드 근거 |
| K03 미세침 천공 | `modality[M12].extracted.related_techniques` | MTS + PRP — 미세 구멍 후 PRP 도포로 피부 재생 효과 극대화 | 기법 노드 근거 |
| K04 조사 | `profiles[M8].mechanism` | thermal | 기법 노드 |
| K04a 토닝 | `modality[M13].extracted.related_techniques` | 레이저 토닝 -- 색소 치료와 병합 | 기법 노드 근거 |
| K04a 토닝 | `modality[M15].extracted.related_techniques` | 레이저토닝 -- 기미/색소 치료에 병합 | 기법 노드 근거 |
| K04a 토닝 | `sequence_order[4].categories` | M8-토닝 | 기법 노드 |
| K04b 프락셔널 | `modality[M5].extracted.related_techniques` | 프랙셔널 레이저 + PRP — 레이저 시술 후 PRP를 도포해 재생 효과 증대 | 기법 노드 근거 |
| K04b 프락셔널 | `modality[M8].extracted.related_techniques` | 프랙셔널 레이저 — 기존 박피 레이저의 다운타임을 줄인 최신 기술 | 기법 노드 근거 |
| K04b 프락셔널 | `modality[M11].extracted.related_techniques` | 프랙셔널 레이저 -- 비슷한 피부 재생 원리이나 표피 손상이 더 큼 | 기법 노드 근거 |
| K04b 프락셔널 | `modality[M12].extracted.related_techniques` | 프랙셔널 레이저 — 비슷한 원리(미세 열손상 → 재생)이지만 레이저 에너지 사용 | 기법 노드 근거 |
| K04b 프락셔널 | `sequence_order[4].categories` | M8-프락셔널 | 기법 노드 |
| K04c 광역학 | `modality[M8].extracted.related_techniques` | PDT (광역학요법) — 광감작제 약물 + 레이저를 병합한 여드름/피부암 치료 | 기법 노드 근거 |
| K05 에너지 가열 | `profiles[M9].mechanism` | thermal | 기법 노드 |
| K06 전자기 자극 | `profiles[M10].mechanism` | electromagnetic_stimulation | 기법 노드 |
| K07 플라즈마 전달 | `profiles[M13].mechanism` | plasma_energy | 기법 노드 |
| K08 냉각 | `profiles[M14].mechanism` | cooling | 기법 노드 |
| K09 도포 | `profiles[M15].mechanism` | topical | 기법 노드 |
| K09 도포 | `sequence_order[10].categories` | M15-도포 | 기법 노드 |
| K10 침투 | `profiles[M15].mechanism` | infusion | 기법 노드 |
| K10 침투 | `modality[M12].extracted.related_techniques` | MTS + 약물 투입 — 비타민C, 히알루론산 등 유효 성분 경피 흡수 촉진 | 기법 노드 근거 |
| K12a 서브시전 | `modality[M2].extracted.related_techniques` | 진피절제주입법 (서브시전 + 필러) — 흉터 치료에 병합 활용 | 기법 노드 근거 |
| K12a 서브시전 | `modality[M5].extracted.related_techniques` | 진피절제주입법 + PRP — 여드름흉터에 서브시전 후 PRP 주입 | 기법 노드 근거 |

## 3. 노드를 세우는 규칙(요약 — 상세는 SKILL.md §2-2 · mistakes.md)

- **큰 기법** = 2단계 계열 정의(문헌 기준)의 전달 동사 + procedure-profiles `mechanism` 전달 태그. taxonomy `group` 은 기준이 아니다(X3 — M7 group 「시술/기기」 ↔ mechanism mechanical). `regenerative` · `ablative` 는 기법이 아니다
- **세부 기법** = DEC-002 D-05 부위 쪼개기 규칙을 축만 바꿔: ① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다. 둘 다 아니면 안 쪼갠다
  - K04a 토닝 · K04b 프락셔널 — treatment-sequence 가 「M8-토닝」「M8-프락셔널」을 따로 부름(①)
  - K01c 무바늘 제트 — M4 정의 「(또는 무바늘 제트 주입)」 · 초안 T34 니들리스 + T35 분사 합침. 크리스탈필 「분사」는 같은 글자 다른 뜻 → K11 박리·흡인
  - K02a~c 코그 · 모노 · 볼륨 — 원천 M7-2 하위 항목(①) · 모양 낱말(2방향 · 다방향 · 콘 · 오메가 …)은 장비 속성 `thread_design`(OQ-310)
  - K12 소수술 — 2단계 M15 deferred 「서브시전 · 면포압출 · 펀치 → 5단계 시술」. 큰 기법 K12 는 세부 셋의 근거로 선다(스크립트: 큰 기법은 세부 근거로도 선다)
- **2층까지** — 단위 시술 → 기법 하나(`uses_technique` 단일) · canonical technique 은 `parent_id` 계층. 세부 아래 세부 없음
- **노드 아님(안 세움)**: 층(진피 주입 · 피하 주사) · 펄스(피코초) · 전극(모노폴라) · 매질(IPL · 알렉산드라이트) · 실 디자인(오메가) · 상담 이름(스킨보톡스 · 네페르티티 리프트) · 장비 프로그램(BBL Forever Young · 포토나 4D)

## 4. 대안 구조(J1 — 고르지 않은 것)

| 안 | 노드 | 단위 시술 키(조사 추정) | 무엇 |
|---|---|---|---|
| 안 1 (추천 · 채택) | 24 | 199 | 큰 기법 12 + 세부 12 노드 · 층 · 대상 근육 · 도구 = 단위 시술 속성(키 밖) · 펄스 · 가능 방식 · 박피 · 전극 · 주입기 · 침투 방식 · 실 디자인 = 장비 속성 |
| 안 2 | 56 | 약 210(추정) | 층 13 · 펄스 3 · 대상 근육 16 까지 하위 노드 |
| 안 3 | 65 | 209 | 초안 그대로(평평한 65) |

키 수는 조사 추정(초안 236행 기준)이다. 5단계에서 실제로 단위 시술에 기법을 붙일 때 다시 센다.
