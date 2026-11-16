# 미결 — post-procedure-timeline.json

> build.py 생성. 원천은 manual/S*.txt 의 Q 줄과 manual/global-issues.txt.

분류: A=에이전트 추출/해석 오류 · B=원문 정보 부족 · C=현재 사용자 결정 필요 · K=알려진 분석 한계 · P=잠정 · F=후속 의미 조사 · I=원문 내 불일치. 원문 내 불일치는 C 가 아니다.

## 집계

| 분류 | 건수 |
|---|---|
| A 에이전트 추출/해석 오류 | 1 |
| B 원문 정보 부족 | 21 |
| C 현재 사용자 결정 필요 | 0 |
| K 알려진 분석 한계 | 3 |
| P 잠정 | 6 |
| F 후속 의미 조사 | 4 |
| I 원문 내 불일치 | 4 |

**C(사용자 결정 필요) 0건의 근거:** 아래 B 는 원문에 정보가 없는 것이라 사용자 추측으로 채울 대상이 아니고, P·F 는 21개 원장 비교 후 의미 설계 단계에서 묶어 다룰 과제이며, I 는 원본 보존 지시 아래 후속 확인 후보다. 도구 선택(형태소 설정)은 에이전트가 정해 기록했다. 따라서 현재 사용자에게 선택을 요청할 항목은 없다. 이것은 미결이 닫혔다는 뜻이 아니다.

## A — 에이전트 추출/해석 오류 (1)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| G-A1 | GLOBAL | `/timelines/8/phases/1/abnormal/0` | 단서 덮임 대조에서 EM DASH 1출현이 manual 구절 밖에 있었다(직접 읽기 기록 누락). manual/S09.txt 에 보완하고 재생성·재검증했다. | 해결됨(아래 validation 참조) |

## B — 원문 정보 부족 (21)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| S00-Q1 | S00 | `/consensus_method` | 항목별 근거·문헌·합의 불일치 기록이 원문에 없다. 개별 시간·빈도 표현의 출처 확인이 제한된다. | 열림 |
| S00-Q2 | S00 | `/reaction_levels/caution` | 「24-48시간 내」의 기준 시점(증상 발견 시·시술 시)이 원문에 없다. | 열림 |
| S01-Q1 | S01 | `/timelines/0/phases/0/normal/0` `/timelines/0/phases/1/normal/2` `/timelines/0/phases/1/abnormal/0` `/timelines/0/phases/1/abnormal/1` | 괄호 속 소실 시간의 기준 시점(시술 후·발현 후)이 원문에 없다. | 열림 |
| S01-Q2 | S01 | `/timelines/0/phases/*/period` | 기간 경계일의 포함·제외가 원문에 없다(Day 14 가 두 기간에 걸림). | 열림 |
| S02-Q1 | S02 | `/timelines/1/phases/0/emergency/0` `/timelines/1/phases/1/emergency/0` | 「골든타임」 이 어떤 처치의 시한인지 원문에 없다. phases/1 은 범위도 없다. | 열림 |
| S02-Q2 | S02 | `/timelines/1/phases/0/caution/0` | 「통증 스케일 7 이상」 의 척도 정의(0-10 등)가 원문에 없다. | 열림 |
| S03-Q1 | S03 | `/timelines/2/name` `/timelines/2/phases/*/*` | HIFU 와 RF 중 어느 쪽에 해당하는 반응인지 phases/3/emergency/0 외에는 원문에 없다. | 열림 |
| S04-Q2 | S04 | `/timelines/3/phases/3/caution/0` | 「10일 이상」 의 기준(시술 후 경과일인지 지연 기간인지)이 원문에 없다. | 열림 |
| S04-Q3 | S04 | `/timelines/3/phases/0/caution/1` | 통증 스케일 정의 없음(S02 와 같은 원인). | 열림 |
| S05-Q1 | S05 | `/timelines/4/phases/4/abnormal/0` `/timelines/4/phases/4/caution/1` | 「조기」「만성」 의 기간 기준이 원문에 없다. | 열림 |
| S06-Q1 | S06 | `/timelines/5/phases/1/normal/0` | 「거의 필발」 은 원문으로 뜻을 정할 수 없다. 오기 여부를 원본 정정 없이 후속 확인 후보로 둔다(현재 사용자 선택 아님). | 열림 |
| S07-Q1 | S07 | `/timelines/6/phases` | Day 7 이후 경과(효과 발현·재시술)가 원문에 없다. | 열림 |
| S08-Q1 | S08 | `/timelines/7/phases` | Day 7 이후 경과·재시술 시점이 원문에 없다. | 열림 |
| S09-Q1 | S09 | `/timelines/8/name` | 「바이오스티뮬레이터/콜라겐부스터」 의 「/」 가 동의어 병기인지 대안인지 원문에 없다. | 열림 |
| S09-Q2 | S09 | `/timelines/8/phases/1/abnormal/0` | 「주입 깊이·농도 문제」 의 기준 깊이·농도가 원문에 없다. | 열림 |
| S10-Q1 | S10 | `/timelines/9/phases/3/caution/0` | 「피부 타입 III-V」 의 분류 체계 이름이 원문에 없다. | 열림 |
| S10-Q2 | S10 | `/timelines/9/phases/1/normal/3` `/timelines/9/phases/3/normal/3` | 「주의 기간」「필수 기간」 의 시작·끝이 소속 period 외에 원문에 없다. | 열림 |
| G-B1 | GLOBAL | `/consensus_method` | 항목별 출처·근거가 없다. 빈도(극히 드묾·드묾·흔함)와 시간 수치의 근거 확인이 원장만으로 불가능하다. | 열림 |
| G-B2 | GLOBAL | `/timelines/0/phases/0/normal/0` `/timelines/7/phases/1/normal/0` `/timelines/2/phases/3/normal/0` | 괄호·값 속 시간(15-60분 내, 24-48시간 내, 2-4주 등)의 기준 시점(시술 시각·증상 발현 시각)이 대부분 원문에 없다. period 는 시술 기준(Day 0 = 시술 당일)이지만 값 속 시간이 같은 기준인지는 원문에 없다. | 열림 |
| G-B3 | GLOBAL | `/timelines/0/phases/0/emergency/0` `/timelines/1/phases/0/abnormal/0` `/timelines/7/phases/0/emergency/1` `/timelines/8/phases/0/emergency/1` | 빈도 표현은 언어 표현(극히 드묾·드묾·흔함·대개)뿐이고 수치·분모가 없다. 백분율로 바꾸지 않는다. | 열림 |
| G-B4 | GLOBAL | `/timelines/1/phases/0/caution/0` `/timelines/3/phases/0/caution/1` `/timelines/9/phases/3/caution/0` | 척도 정의 부재: 「통증 스케일 7/8 이상」, 「피부 타입 III-V」, 화상 「2도」 의 척도 이름·범위가 원문에 없다. | 열림 |

## C — 현재 사용자 결정 필요 (0)

없음.

## K — 알려진 분석 한계 (3)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| G-K1 | GLOBAL | `/timelines` | 형태소 출력은 교정하지 않았다. 문맥 대조로 확인한 오분절·오태깅 서명(build.py SEQ_RULES)에 맞는 모든 출현을 morphology.json known_errors_rule 에 기록했다(지속→지/NP+속, 내→나/NP+의, 스무딩→스무/MM+딩, 시사→시/NNB+사, 삼출→삼/NR, 수포→수+포, 안동맥→안+동맥, 멍/MAG 등). 서명 밖 토큰의 정확성은 보장하지 않는다. | 기록됨(교정 안 함) |
| G-K2 | GLOBAL | `/consensus_method` `/timelines/3/name` `/timelines/9/phases/3/caution/0` `/timelines/1/phases/0/caution/1` | 영문·약어·혼합 표기(Perplexity·Gemini·Claude·AI·CO2·HIFU/RF·DCA·HA·TCA·PIH·blanching·frost·papule·dimpling·III-V·Day)는 Kiwi 출력(SL/SN/W_SERIAL)만 보존했고 영어 형태소 분석은 하지 않았다. 원문은 전부 보존되며, 영문 단어의 수식·조건은 직접 읽기(manual)로만 수집했다. 이 원장의 영문은 단어·약어 수준이며 영어 문장은 없다. | 기록됨(교정 안 함) |
| G-K3 | GLOBAL | `/timelines` | 자동 후보(auto)는 expressions.json method.patterns 의 정규식 일치분뿐이다. 패턴 밖 접두 부정·반복(비대칭의 비, 재발의 재, 불규칙의 불 등)은 auto 에 없고 residual_tokens 에 남는다. 이 출현들은 전부 manual 구절에 덮여 있다(verify 의 잔여·단서 덮임 검사). | 기록됨(교정 안 함) |

## P — 잠정 (6)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| S00-Q3 | S00 | `/reaction_levels` | 등급 키와 phases 배열 키의 이름 일치를 정의 참조로 볼지는 후속 의미 조사(F-LEVEL)에서 정한다. | 열림(잠정) |
| S01-Q3 | S01 | `/timelines/0/phases/0/emergency/1` `/timelines/0/phases/0/emergency/0` `/timelines/0/phases/2/emergency/0` | 「/」 앞 수식어(심한·전신·악화)가 뒤 항목까지 걸리는지 잠정. README 의 「/」 규칙은 시술 이름 규칙이라 증상 나열에 그대로 적용하지 않는다. | 열림(잠정) |
| S02-Q4 | S02 | `/timelines/1/phases/0/abnormal/0` | 「흔함」 이 혈관 천자 시 조건부 빈도인지 멍 전체 빈도인지 잠정. | 열림(잠정) |
| S03-Q2 | S03 | `/timelines/2/phases/0/abnormal/0` | 「(24시간 이상)」 이 부종 지속 시간인지 원문 표현이 생략돼 있다. | 열림(잠정) |
| S05-Q2 | S05 | `/timelines/4/phases/2/caution/0` `/timelines/4/phases/4/emergency/1` | 「돌출」 이 caution·emergency 양쪽에 있어 등급을 가르는 기준(촉지 vs 노출)은 잠정. | 열림(잠정) |
| S06-Q2 | S06 | `/timelines/5/phases/3/emergency/0` | 「4주 이상」 의 기준이 손상 지속 기간인지 시술 후 경과인지 잠정. | 열림(잠정) |

## F — 후속 의미 조사 (4)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| S06-Q3 | S06 | `/timelines/5/phases/3/abnormal/0` | 복합 값의 절 단위 분해(증상·판정·금기·이유·조건부 대응)는 후속 의미 조사. | 열림(후속) |
| G-F1 | GLOBAL | `/reaction_levels` `/timelines` | 등급(normal~emergency)·기간(period)·사건(증상 문자열)·조치(연락·문의·고려)를 분리하는 의미 모델과, 같은 증상이 등급·기간에 따라 다르게 놓인 것(안검하수·실 돌출·돌기 지속시간 등)의 표현 방식은 21개 원장 비교 후 설계 단계 과제다. | 열림(후속) |
| G-F2 | GLOBAL | `/timelines/*/category` `/timelines/*/name` | category 코드(M1·M2·…·M16-DCA)와 name 이 다른 원장의 분류·시술과 어떻게 연결되는지는 이 원장만으로 정하지 않는다(다른 원장 미조사). HIFU/RF·바이오스티뮬레이터/콜라겐부스터 처럼 한 타임라인이 둘 이상을 묶는 경우 포함. | 열림(후속) |
| G-F3 | GLOBAL | `/timelines/*/phases/*/*` | 값 하나에 사건·정도·시간·원인·판정(정상)·조치가 괄호와 기호로 함께 들어 있다. 절·괄호 단위 분해 규칙은 후속 변환 과제다(수동 표현은 구간만 잡았고 분해는 확정하지 않았다). | 열림(후속) |

## I — 원문 내 불일치 (4)

| ID | 구획 | 위치 | 내용 | 상태 |
|---|---|---|---|---|
| S02-Q3 | S02 | `/timelines/1/phases/*/period` | 같은 원장 안에서 기간 경계 방식이 시술마다 다르다(겹침·공백). 원문 내 불일치로 기록(I-PERIOD). | 열림(원본 보존, 후속 확인 후보) |
| S04-Q1 | S04 | `/timelines/3/phases/3/normal/3` `/timelines/3/phases/4/normal/1` | 홍반 지속 기간 표현이 두 기간에서 다르다(수주 / 1-3개월). 원문 내 불일치 후보(I-DUR). | 열림(원본 보존, 후속 확인 후보) |
| G-I1 | GLOBAL | `/timelines/1/phases/1/period` `/timelines/1/phases/2/period` `/timelines/1/phases/4/period` `/timelines/8/phases/1/period` `/timelines/0/phases/2/period` | 기간 경계 방식이 시술마다 다르다: 대부분 경계일을 공유(1-3, 3-7), ha-filler 는 1-2 다음 3-5(공백)·5-7 다음 8-14(비공유), biostimulator 는 1-7 하나. 원문 내 불일치 후보로 기록하고 원본은 고치지 않는다. | 열림(원본 보존, 후속 확인 후보) |
| G-I2 | GLOBAL | `/timelines/3/phases/3/normal/1` `/timelines/9/phases/3/normal/0` | 값 안 세부 시점(「Day 7-10: …」)이 소속 period(Day 5-7)를 벗어난다(fractional-co2). 소속 기간과 값 시점 중 어느 것을 기준으로 할지 후속 변환 규칙 과제. | 열림(원본 보존, 후속 확인 후보) |

## K 상세 — 알려진 형태소 오분절 출현

규칙 서명 76출현 + 출현별 직접 판정 0건. 위치·원시 토큰은 morphology.json known_errors_rule / segmentation_manual, 구획별로는 review-part 7절.

| 규칙/판정 | 출현 수 |
|---|---|
| K-NAE | 1 |
| K-BALJEOK | 18 |
| K-ANGEOMHASU | 1 |
| K-LOANSPLIT | 3 |
| K-MAG-NOUN | 10 |
| K-ANDONGMAEK | 1 |
| K-APTONG | 2 |
| K-GYEOLJEOL | 4 |
| K-CHOKJI | 2 |
| K-YUKAJONG | 2 |
| K-JISOK | 1 |
| K-SEONBEON | 1 |
| K-YUSA | 1 |
| K-SUPO | 4 |
| K-GAPI | 5 |
| K-SAMCHUL | 1 |
| K-GWA-NNG | 3 |
| K-CHIMJA | 1 |
| K-HWANGSAEK | 1 |
| K-DAEBUBUN | 1 |
| K-NONGYANG | 2 |
| K-IJUNGTEOK | 1 |
| K-GYEONGGYEOL | 3 |
| K-ULTUNG | 1 |
| K-MISECHIM | 1 |
| K-DOLGI | 3 |
| K-SMOOTHING | 1 |
| K-SISA | 1 |

