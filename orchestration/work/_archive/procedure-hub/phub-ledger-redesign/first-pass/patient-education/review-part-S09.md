# S09 — /categories/8 M9 기기 리프팅

[← review.md 목차](./review.md)

- 읽기 상태: **직접 읽음** · 마지막 읽은 Pointer `/categories/8/common_concerns/2/a`
- 소유 노드 19 · 소유 말단 14 · 공동 참조 문맥(소유 아님): `/version`, `/updated`
- 수동 기록 `manual/S09.json` · 구조화 기록: source-map.json · morphology.json · expressions.json

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 디코딩 값을 JSON 리터럴로 그대로 싣는다. 관찰은 이 표에 섞지 않고 §2 에 둔다.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/8` | [8] | object | (object, 자식 9) | 5856–6618 |  |  |
| `/categories/8/id` | id | string | "M9" | 5863–5865 | 제외(category_code) |  |
| `/categories/8/name` | name | string | "기기 리프팅" | 5875–5881 | 2토큰 | E0405 |
| `/categories/8/patient_name` | patient_name | string | "비수술 리프팅 (울쎄라/써마지 등)" | 5899–5918 | 9토큰 | E0406, E0407, E0408 |
| `/categories/8/simple_explanation` | simple_explanation | string | "초음파나 고주파 에너지로 피부 깊은 층을 자극하여 처짐을 개선하는 비수술 시술입니다." | 5942–5989 | 27토큰 | E0409, E0410, E0411, E0412, E0413 |
| `/categories/8/how_it_works` | how_it_works | string | "기기에서 나오는 에너지(초음파 또는 고주파)가 피부 깊은 곳의 조직에 열을 가합니다. 이 열 자극으로 기존 콜라겐이 수축하면서 즉각적인 당김 효과가 나타나고, 이후 새로운 콜라겐이 만들어져 탄력이 개선됩니다." | 6007–6123 | 61토큰 | E0414, E0415, E0416, E0417, E0418, E0419 |
| `/categories/8/duration_simple` | duration_simple | string | "약 6-12개월 지속되며, 3개월에 걸쳐 점진적으로 효과가 나타납니다." | 6144–6183 | 20토큰 | E0420, E0421, E0422 |
| `/categories/8/pain_level` | pain_level | string | "시술 중 열감과 뻐근함이 있음, 부위에 따라 마취 크림 사용" | 6199–6232 | 19토큰 | E0423, E0424, E0425 |
| `/categories/8/downtime` | downtime | string | "거의 없음 - 약간의 붉은기와 붓기가 수시간~1일" | 6246–6273 | 17토큰 | E0426, E0427, E0428 |
| `/categories/8/common_concerns` | common_concerns | array | (array, 자식 3) | 6293–6617 |  |  |
| `/categories/8/common_concerns/0` | [0] | object | (object, 자식 2) | 6294–6411 |  |  |
| `/categories/8/common_concerns/0/q` | q | string | "울쎄라와 써마지은 뭐가 다른가요?" | 6300–6318 | 11토큰 | E0429 |
| `/categories/8/common_concerns/0/a` | a | string | "울쎄라는 초음파로 피부 깊은 층(SMAS)까지 도달하고, 써마지은 고주파로 넓은 면적의 피부 탄력을 개선합니다. 의사가 피부 상태에 맞게 추천해드려요." | 6325–6409 | 46토큰 | E0430, E0431, E0432, E0433, E0434, E0435 |
| `/categories/8/common_concerns/1` | [1] | object | (object, 자식 2) | 6412–6521 |  |  |
| `/categories/8/common_concerns/1/q` | q | string | "기기 리프팅이 수술만큼 효과 있나요?" | 6418–6438 | 9토큰 | E0436 |
| `/categories/8/common_concerns/1/a` | a | string | "수술적 리프팅만큼 극적이지는 않지만, 비수술적으로 피부 탄력을 개선하는 데 효과적이에요. 처짐 정도에 따라 의사와 상담하시면 됩니다." | 6445–6519 | 43토큰 | E0437, E0438, E0439, E0440, E0441, E0442 |
| `/categories/8/common_concerns/2` | [2] | object | (object, 자식 2) | 6522–6616 |  |  |
| `/categories/8/common_concerns/2/q` | q | string | "기기 리프팅이 지방을 녹이나요?" | 6528–6545 | 8토큰 | E0443 |
| `/categories/8/common_concerns/2/a` | a | string | "일부 고출력 시술에서 지방층에 영향을 줄 수 있습니다. 의사가 볼륨이 필요한 부위는 피하거나 강도를 조절합니다." | 6552–6614 | 33토큰 | E0444, E0445, E0446, E0447, E0448, E0449 |

## 2. 잠정 관찰·미결 (원문과 분리)

| ID | 상태 | Pointer | 관찰 |
|---|---|---|---|
| S09-O1 | I | `/categories/8/common_concerns/0/q` | 「써마지은」 — patient_name 「써마지」 뒤 조사 「는」 대신 「은」(받침 없음). 같은 표기가 a 에도 「써마지은」. 원문 표기 그대로 보존 |
| S09-O2 | K | `/categories/8/common_concerns/0/q` | 「써마지은」 형태소 분절 이상 확인됨 — q 는 써마지/NNG 이/VCP(길이0) 은/EC, a 는 써마지은/NNG 로 출현마다 다르게 깨진다. 출현별 기록은 issues.md K 표(교정 안 함) |
| S09-O3 | B | `/categories/8/pain_level` | 마취 크림 사용 부위 미기재 |
| S09-O4 | B | `/categories/8/common_concerns/2/a` | 「일부 고출력 시술」 어느 시술인지·출력 기준 미기재 |
| S09-O5 | F | `/categories/8/patient_name` | 울쎄라·써마지(제품명)와 카테고리 「기기 리프팅」의 관계는 후속(다른 원장 연결) |
| S09-O6 | P | `/categories/8/how_it_works` | 효과 시간 역할 두 단계: 즉각적 당김 → 이후 콜라겐(duration_simple 「3개월에 걸쳐 점진적」) |

## 3. 직접 읽기로 수집한 표현 (원문 부분문자열 · facets 는 탐색 관점)

| ID | Pointer | 원문 구간 | 값 내 [s,e) | facets | 메모 |
|---|---|---|---|---|---|
| E0405 | `/categories/8/name` | 기기 리프팅 | 0–6 | name |  |
| E0406 | `/categories/8/patient_name` | 비수술 리프팅 (울쎄라/써마지 등) | 0–19 | name,negation,paraphrase | 괄호 안 「/」 제품 나열 · 「등」 |
| E0407 | `/categories/8/patient_name` | 울쎄라 | 9–12 | name |  |
| E0408 | `/categories/8/patient_name` | 써마지 | 13–16 | name |  |
| E0409 | `/categories/8/simple_explanation` | 초음파나 고주파 에너지로 피부 깊은 층을 자극하여 처짐을 개선하는 비수술 시술입니다. | 0–47 | sentence |  |
| E0410 | `/categories/8/simple_explanation` | 초음파나 고주파 에너지 | 0–12 | device_param | 「나」 대안 |
| E0411 | `/categories/8/simple_explanation` | 피부 깊은 층 | 14–21 | site,depth | 「깊은」 — 수치 없음 |
| E0412 | `/categories/8/simple_explanation` | 처짐을 개선하는 | 28–36 | concern,effect |  |
| E0413 | `/categories/8/simple_explanation` | 비수술 시술 | 37–43 | negation,name |  |
| E0414 | `/categories/8/how_it_works` | 기기에서 나오는 에너지(초음파 또는 고주파)가 피부 깊은 곳의 조직에 열을 가합니다. | 0–47 | sentence,device_param,site,depth,mechanism |  |
| E0415 | `/categories/8/how_it_works` | 에너지(초음파 또는 고주파) | 9–24 | device_param,paraphrase | 「또는」 대안 |
| E0416 | `/categories/8/how_it_works` | 피부 깊은 곳의 조직 | 26–37 | site,depth |  |
| E0417 | `/categories/8/how_it_works` | 이 열 자극으로 기존 콜라겐이 수축하면서 즉각적인 당김 효과가 나타나고, 이후 새로운 콜라겐이 만들어져 탄력이 개선됩니다. | 48–116 | sentence,mechanism,time,effect,sequence |  |
| E0418 | `/categories/8/how_it_works` | 즉각적인 당김 효과 | 71–81 | time,effect | 시간 역할 두 단계(즉각·이후) |
| E0419 | `/categories/8/how_it_works` | 이후 새로운 콜라겐이 만들어져 | 89–105 | time,sequence,mechanism |  |
| E0420 | `/categories/8/duration_simple` | 약 6-12개월 지속되며, 3개월에 걸쳐 점진적으로 효과가 나타납니다. | 0–39 | sentence,time,approx,range,quantity,manner |  |
| E0421 | `/categories/8/duration_simple` | 약 6-12개월 지속 | 0–11 | time,approx,range,quantity |  |
| E0422 | `/categories/8/duration_simple` | 3개월에 걸쳐 점진적으로 효과가 나타납니다 | 15–38 | time,quantity,manner,effect | 발현 경과 |
| E0423 | `/categories/8/pain_level` | 시술 중 열감과 뻐근함이 있음, 부위에 따라 마취 크림 사용 | 0–33 | time,sensory,condition,site,substance |  |
| E0424 | `/categories/8/pain_level` | 시술 중 열감과 뻐근함 | 0–12 | time,sensory |  |
| E0425 | `/categories/8/pain_level` | 부위에 따라 마취 크림 사용 | 18–33 | condition,site,substance | 어느 부위인지 미기재 |
| E0426 | `/categories/8/downtime` | 거의 없음 - 약간의 붉은기와 붓기가 수시간~1일 | 0–27 | negation,degree,adverse,time,range,approx |  |
| E0427 | `/categories/8/downtime` | 거의 없음 | 0–5 | negation,degree |  |
| E0428 | `/categories/8/downtime` | 약간의 붉은기와 붓기가 수시간~1일 | 8–27 | degree,adverse,time,range,approx | 「~」 범위 |
| E0429 | `/categories/8/common_concerns/0/q` | 울쎄라와 써마지은 뭐가 다른가요? | 0–18 | sentence,name,comparison | 「써마지은」 조사 표기 원문 그대로 |
| E0430 | `/categories/8/common_concerns/0/a` | 울쎄라는 초음파로 피부 깊은 층(SMAS)까지 도달하고, 써마지은 고주파로 넓은 면적의 피부 탄력을 개선합니다. | 0–62 | sentence,name,comparison,device_param,depth,site |  |
| E0431 | `/categories/8/common_concerns/0/a` | 울쎄라는 초음파로 피부 깊은 층(SMAS)까지 도달하고 | 0–30 | name,device_param,depth,site,paraphrase |  |
| E0432 | `/categories/8/common_concerns/0/a` | 피부 깊은 층(SMAS) | 10–23 | site,depth,paraphrase | 전문어 괄호 |
| E0433 | `/categories/8/common_concerns/0/a` | 써마지은 고주파로 넓은 면적의 피부 탄력을 개선합니다 | 32–61 | name,device_param,degree,effect |  |
| E0434 | `/categories/8/common_concerns/0/a` | 넓은 면적 | 42–47 | degree,site |  |
| E0435 | `/categories/8/common_concerns/0/a` | 의사가 피부 상태에 맞게 추천해드려요. | 63–84 | sentence,actor,condition |  |
| E0436 | `/categories/8/common_concerns/1/q` | 기기 리프팅이 수술만큼 효과 있나요? | 0–20 | sentence,comparison |  |
| E0437 | `/categories/8/common_concerns/1/a` | 수술적 리프팅만큼 극적이지는 않지만, 비수술적으로 피부 탄력을 개선하는 데 효과적이에요. | 0–49 | sentence,comparison,negation,degree,effect |  |
| E0438 | `/categories/8/common_concerns/1/a` | 수술적 리프팅만큼 극적이지는 않지만 | 0–19 | comparison,negation,degree |  |
| E0439 | `/categories/8/common_concerns/1/a` | 처짐 정도에 따라 의사와 상담하시면 됩니다. | 50–74 | sentence,condition,degree,instruction,actor |  |
| E0440 | `/categories/8/common_concerns/1/a` | 처짐 정도에 따라 | 50–59 | condition,degree |  |
| E0441 | `/categories/8/common_concerns/1/a` | 비수술적으로 피부 탄력을 개선하는 데 효과적이에요 | 21–48 | negation,effect | regex 대조 후 보충(구절 누락 수정) |
| E0442 | `/categories/8/common_concerns/1/a` | 의사와 상담하시면 됩니다 | 60–73 | instruction,actor | regex 대조 후 보충(구절 누락 수정) |
| E0443 | `/categories/8/common_concerns/2/q` | 기기 리프팅이 지방을 녹이나요? | 0–17 | sentence,adverse |  |
| E0444 | `/categories/8/common_concerns/2/a` | 일부 고출력 시술에서 지방층에 영향을 줄 수 있습니다. | 0–30 | sentence,scope,condition,degree,site,possibility,adverse |  |
| E0445 | `/categories/8/common_concerns/2/a` | 일부 고출력 시술에서 | 0–11 | scope,condition,degree | 「고출력」 기준 미기재 |
| E0446 | `/categories/8/common_concerns/2/a` | 지방층에 영향을 줄 수 있습니다 | 12–29 | site,possibility,adverse |  |
| E0447 | `/categories/8/common_concerns/2/a` | 의사가 볼륨이 필요한 부위는 피하거나 강도를 조절합니다. | 31–62 | sentence,actor,site,avoid,degree,management |  |
| E0448 | `/categories/8/common_concerns/2/a` | 볼륨이 필요한 부위는 피하거나 | 35–51 | site,avoid,condition | 회피 부위 — 시술자 행동 |
| E0449 | `/categories/8/common_concerns/2/a` | 강도를 조절합니다 | 52–61 | degree,management |  |

## 4. 형태소 원시 출력 (Kiwi 0.24.1 cong · 교정 없음)

- `/categories/8/name`: 기기/NNG 리프팅/NNG
- `/categories/8/patient_name`: 비/XPN 수술/NNG 리프팅/NNG (/SSO 울쎄라/NNG //SP 써마지/NNG 등/NNB )/SSC
- `/categories/8/simple_explanation`: 초/XPN 음파/NNG 나/JC 고/XPN 주파/NNG 에너지/NNG 로/JKB 피부/NNG 깊/VA 은/ETM 층/NNG 을/JKO 자극/NNG 하/XSV 어/EC 처지/VV ᆷ/ETN 을/JKO 개선/NNG 하/XSV 는/ETM 비/XPN 수술/NNG 시술/NNG 이/VCP ᆸ니다/EF ./SF
- `/categories/8/how_it_works`: 기기/NNG 에서/JKB 나오/VV 는/ETM 에너지/NNG (/SSO 초/XPN 음파/NNG 또는/MAG 고/XPN 주파/NNG )/SSC 가/JKS 피부/NNG 깊/VA 은/ETM 곳/NNG 의/JKG 조직/NNG 에/JKB 열/NNG 을/JKO 가하/VV ᆸ니다/EF ./SF 이/MM 열/NNG 자극/NNG 으로/JKB 기존/NNG 콜라겐/NNP 이/JKS 수축/NNG 하/XSV 면서/EC 즉각/MAG 적/XSN 이/VCP ᆫ/ETM 당기/VV ᆷ/ETN 효과/NNG 가/JKS 나타나/VV 고/EC ,/SP 이후/NNG 새롭/VA-I 은/ETM 콜라겐/NNP 이/JKS 만들/VV 어/EC 지/VX 어/EC 탄력/NNG 이/JKS 개선/NNG 되/XSV ᆸ니다/EF ./SF
- `/categories/8/duration_simple`: 약/MM 6-12/W_SERIAL 개월/NNB 지속/NNG 되/XSV 며/EC ,/SP 3/SN 개월/NNB 에/JKB 걸치/VV 어/EC 점진/NNG 적/XSN 으로/JKB 효과/NNG 가/JKS 나타나/VV ᆸ니다/EF ./SF
- `/categories/8/pain_level`: 시술/NNG 중/NNB 열/NNG 감/XSN 과/JC 뻐근/XR 하/XSA ᆷ/ETN 이/JKS 있/VV 음/ETN ,/SP 부위/NNG 에/JKB 따르/VV 어/EC 마취/NNG 크림/NNG 사용/NNG
- `/categories/8/downtime`: 거의/MAG 없/VA 음/EF -/SO 약간/NNG 의/JKG 붉/VA 은/ETM 기와/NNG 붓/VV-I 기/ETN 가/JKS 수/MM 시간/NNB ~/SO 1/SN 일/NNB
- `/categories/8/common_concerns/0/q`: 울쎄라/NNG 와/JC 써마지/NNG 이/VCP 은/EC 뭐/NP 가/JKS 다르/VA ᆫ가/EF 요/JX ?/SF
- `/categories/8/common_concerns/0/a`: 울쎄/NNP 이/VCP 라는/ETM 초/XPN 음파/NNG 로/JKB 피부/NNG 깊/VA 은/ETM 층/NNG (/SSO SMAS/SL )/SSC 까지/JX 도달/NNG 하/XSV 고/EC ,/SP 써마지은/NNG 고/XPN 주파/NNG 로/JKB 넓/VA 은/ETM 면적/NNG 의/JKG 피부/NNG 탄력/NNG 을/JKO 개선/NNG 하/XSV ᆸ니다/EF ./SF 의사/NNG 가/JKS 피부/NNG 상태/NNG 에/JKB 맞/VV 게/EC 추천/NNG 하/XSV 어/EC 드리/VX 어요/EF ./SF
- `/categories/8/common_concerns/1/q`: 기기/NNG 리프팅/NNG 이/JKS 수술/NNG 만큼/JKB 효과/NNG 있/VV 나요/EF ?/SF
- `/categories/8/common_concerns/1/a`: 수술/NNG 적/XSN 리프팅/NNG 만큼/NNB 극/NNG 적/XSN 이/VCP 지/EC 는/JX 않/VX 지만/EC ,/SP 비/XPN 수술/NNG 적/XSN 으로/JKB 피부/NNG 탄력/NNG 을/JKO 개선/NNG 하/XSV 는/ETM 데/NNB 효과/NNG 적/XSN 이/VCP 에요/EF ./SF 처지/VV ᆷ/ETN 정도/NNG 에/JKB 따르/VV 어/EC 의사/NNG 와/JKB 상담/NNG 하/XSV 시/EP 면/EC 되/VV ᆸ니다/EF ./SF
- `/categories/8/common_concerns/2/q`: 기기/NNG 리프팅/NNG 이/JKS 지방/NNG 을/JKO 녹이/VV 나요/EF ?/SF
- `/categories/8/common_concerns/2/a`: 일부/NNG 고/XPN 출력/NNG 시술/NNG 에서/JKB 지방/NNG 층/XSN 에/JKB 영향/NNG 을/JKO 주/VV ᆯ/ETM 수/NNB 있/VA 습니다/EF ./SF 의사/NNG 가/JKS 볼륨/NNG 이/JKS 필요/NNG 하/XSA ᆫ/ETM 부위/NNG 는/JX 피하/VV 거나/EC 강도/NNG 를/JKO 조절/NNG 하/XSV ᆸ니다/EF ./SF

알려진 오분절(출현별, 교정 안 함):

- `/categories/8/common_concerns/0/q` 「써마지은」 [5,9) → 써마지/NNG 이/VCP 은/EC — 원문 조사 표기 이상(「써마지은」)으로 길이0 VCP와 연결어미 EC 생성 — 화제 조사 소실·가짜 서술격
- `/categories/8/common_concerns/0/a` 「써마지은」 [32,36) → 써마지은/NNG — 조사가 명사에 흡수된 미등록 명사 — 제품명 토큰 「써마지」 검색 누락
- `/categories/8/common_concerns/0/a` 「울쎄라는」 [0,4) → 울쎄/NNP 이/VCP 라는/ETM — 제품명이 「울쎄」로 잘리고 화제 조사 「는」이 인용형 「라는」으로 오인 — 제품명 손상·가짜 인용 구조
- `/categories/8/simple_explanation` 「초음파」 [0,3) → 초/XPN 음파/NNG — 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음
- `/categories/8/how_it_works` 「초음파」 [13,16) → 초/XPN 음파/NNG — 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음
- `/categories/8/common_concerns/0/a` 「초음파」 [5,8) → 초/XPN 음파/NNG — 「초음파」가 접두사+명사로 분해 — 에너지 종류 토큰 검색 시 「음파」로만 남음
- `/categories/8/simple_explanation` 「고주파」 [5,8) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/8/how_it_works` 「고주파」 [20,23) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/8/common_concerns/0/a` 「고주파」 [37,40) → 고/XPN 주파/NNG — 「고주파」가 접두사+명사로 분해 — 「고」가 정도(높음) 접두로 읽힐 위험·에너지 종류 토큰 누락
- `/categories/8/downtime` 「붉은기와」 [12,16) → 붉/VA 은/ETM 기와/NNG — 「붉은기와 붓기」의 「기」+조사 「와」가 명사 「기와」로 묶임 — 부작용 「붉은기」 소실·무관 명사 생성
