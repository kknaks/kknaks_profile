# synergy.json — 1차 조사 (읽기용)

> 이 문서는 **원문 대응**과 **잠정 관찰**을 나눠 적는다. §3~§5 는 원문 값만, §6 이후의 「잠정」은 원문을 근거로 한 해석 후보다. 확정 의미·관계가 아니다. 공통 개념 ID·동의어·부위 체계·관계 방향은 정하지 않았다(1차 범위 밖).
> 원문의 임상·법적 주장은 **원장에 적혀 있다는 사실**로만 기록한다. 사실 여부는 검증하지 않았다. 다른 원장(taxonomy 등)은 열지 않았다.
> 이 파일은 `build.py` 가 `review-template.md` 에 전체 값 표와 집계를 채워 만든다. 손으로 고치지 말고 템플릿을 고친 뒤 다시 빌드한다.

## 0. 상태

**1차 범위 종료: 예(작성자 판단, 코디 확인 전) · 원장 전체 완료 아님.**

| 구분 | 상태 |
|---|---|
| 전수 읽기 | 115 link × 8필드 + 상위 3키 전부. 1회차 link 0–59 / 60–114 를 사람이 읽는 형태로 출력해 위에서 아래로 읽음. 2회차 고유값별 Kiwi 토큰을 원문과 나란히 대조. 3회차 후보 표현에 덮이지 않은 어절 목록을 읽고 규칙 보강 |
| 구조·값 수집 | [source-map.json](./source-map.json) — 노드 1,039/1,039 · 키 출현 923 · 중복 키 0 · 이스케이프 0 |
| 형태소·표현 수집 | [morphology.json](./morphology.json) · [expressions.json](./expressions.json) — 아래 §7·§8 |
| 기계 검증 | [validation.md](./validation.md) — `verify.py` 실패 0 |
| 읽기 검토 | 같은 작성자가 관점을 바꿔 다시 읽은 것. 독립 검토 아님 |
| 알려진 분석 오류 | 구절 규칙 26개·품사 서명 31개로 출현별 표시(교정 아님). 규칙 밖 토큰 정확성은 보장 안 함. 독립 검토가 찾은 `/links/55/reason` [35,37) 「전층」(전/MM+층/NNG, 미교정)은 issues A' 에 알려진 한계로 기록 |
| 열린 미결 | [issues.md](./issues.md) — 원문 정보 부족 B 10묶음 · 잠정 P 5 · 후속 F 10묶음 · 원본 수정 관련 후속 검토 후보 U 2(U1 → F1 관계 방향 · U2 → 실버 변환 규칙, batch-01 검토 반영 재분류) · **현재 사용자 선택 대기 0** — 원본은 사용자 지시대로 보존, 1차 종료를 막지 않음 |
| 후속 의미 조사 | 시작 안 함 |

### 집계

{{STATS}}

## 1. 원본과 기록 위치

| 항목 | 값 |
|---|---|
| 원본 | `orchestration/work/phub-recommend/bronze/phub-ledger/synergy.json` |
| 크기 | 33,102 bytes · 21,057 code points · UTF-8 · BOM 없음 · 개행 없는 한 줄 · 이스케이프 0 · BMP 밖 문자 0 · 공백 문자는 U+0020 만 · 한글·ASCII 밖 문자는 `·` `→` 두 종 |
| sha256 | `2c0fb244f6dc7f8521be355e83586bc7b6446979c041a51c77046bae1c3c653f` (작업 시작·끝 동일) |
| 구조·값 | [source-map.json](./source-map.json) — 모든 노드(pointer·부모·키·배열 위치·자료형·span·byte_span·literal_span·값·문맥) |
| 형태소 | [morphology.json](./morphology.json) — 적용 690 값·제외 232 값(사유별)·필드명 11 · 구절 규칙 출현 판정 · 품사 출현 판정 |
| 복합 표현 | [expressions.json](./expressions.json) — 후보 전체(오탐 표시 포함) |
| link 관찰 | [link-observations.json](./link-observations.json) — 여러 필드에 걸친 관찰(계산 + 직접) |
| 미결 | [issues.md](./issues.md) |
| 검증 | [validation.md](./validation.md) |
| 재현 | [build.py](./build.py) · [verify.py](./verify.py) + 수동 검토 기록 [segmentation-review-rules.json](./segmentation-review-rules.json) · [pos-review-rules.json](./pos-review-rules.json) · [name-keywords.json](./name-keywords.json) · [manual-expressions.json](./manual-expressions.json) · [expression-review.json](./expression-review.json) · [manual-link-observations.json](./manual-link-observations.json) · [build-output.txt](./build-output.txt) |

구간 기준: 디코딩된 원문 문자열의 Unicode 코드 포인트 `[start,end)`. source-map 의 `span` 은 파일 전체 텍스트 기준(문자열은 따옴표 포함 JSON 리터럴), `literal_span` 은 따옴표를 뺀 구간이다. 이 원장은 이스케이프가 없어 `literal_span` slice 가 디코딩 값과 같다(검증함). morphology·expressions 의 `span` 은 해당 값 문자열 기준이며 파일 기준은 `file_span_of_text[0] + start`. 바이트 구간은 `byte_span` 으로 따로 둔다.

## 2. 읽기 범위

| 구획 | 범위 | 읽기 |
|---|---|---|
| B0 | 루트 객체 · `/version` · `/updated` · `/links`(배열 115) | 직접 |
| B1 | `/links/0` ~ `/links/29` | 8필드 전부 직접 |
| B2 | `/links/30` ~ `/links/59` | 8필드 전부 직접 |
| B3 | `/links/60` ~ `/links/89` | 8필드 전부 직접 |
| B4 | `/links/90` ~ `/links/114` | 8필드 전부 직접 |

- 자동 처리: 구조 열거·포인터·구간·해시, Kiwi 형태소 분석, regex/keyword 후보 추출, 구절 규칙·품사 서명의 출현별 적용, 끝점 쌍 계산.
- 직접: 115개 link 의 모든 값(코드값 포함) 읽기, 고유값 240개의 Kiwi 토큰 전체 열람, 수식·부정·수량 품사 135출현 판정, 구절 규칙 391출현 판정 기준 작성, regex 후보 범주별 문맥 열람·오탐 지정, 절 단위 표현 82건 지정, link 관찰 25건 작성.
- 한계: 「별도 읽기 검토」는 같은 에이전트가 다른 관점으로 다시 읽은 것이다.

## 3. 컬럼 구성 표 — 원문 대응

자료형은 JSON 기준. 빈 문자열·null·빈 배열·빈 객체·숫자·불리언은 **0개**다(source-map `counts.by_type` 으로 확인). 선택적 필드 없음 — 115개 link 가 모두 같은 8키를 같은 순서로 가진다.

| 원본 컬럼명 / JSON 경로 패턴 | 자료형 · 중첩 | 출현 · 고유값 | 원문 예시 (위치) |
|---|---|---|---|
| (루트) `` | object, 키 3개 순서 `version` → `updated` → `links` | 1 | — |
| `version` · `/version` | string | 1 | `1.3` (`/version`) |
| `updated` · `/updated` | string (날짜 표기) | 1 | `2026-07-26` (`/updated`) |
| `links` · `/links` | array of object, 길이 115 | 1 | — |
| `/links/*` | object, 키 8개 순서 `from, from_category, to, to_category, type, reason, timing, target` | 115 | `/links/0` |
| `from` · `/links/*/from` | string (명칭) | 115 · 고유 41 | `M1-보톡스` (`/links/0/from`) |
| ↳ 변형: 코드 접두 `Mxx-` | string | from/to 합계 171/230 출현 | `M11-포텐자` (`/links/7/from`) |
| ↳ 변형: 접두 없는 이름 | string | | `필링` (`/links/22/from`), `CO2프락셔널` (`/links/87/from`) |
| ↳ 변형: 띄어 쓴 부위 접미 | string | | `보툴리눔 톡신 사각턱` (`/links/4/from`), `필러 코` (`/links/34/from`) |
| ↳ 변형: `/` 포함 | string | | `HIFES/EMS` (`/links/5/from`) |
| ↳ 변형: 한 단어 | string | | `혈관` (`/links/84/from`) |
| `from_category` · `/links/*/from_category` | string (코드 `M`+숫자) | 115 · 고유 17 (M1–M17) | `M1` (`/links/0/from_category`) |
| `to` · `/links/*/to` | string (명칭) | 115 · 고유 38 | `M2-필러` (`/links/0/to`) |
| ↳ 변형: 괄호 부위 | string | | `M1-보톡스(코끝)` (`/links/34/to`), `M9-인모드(바디)` (`/links/21/to`) |
| ↳ 변형: 괄호 약칭 | string | | `마이크로니들링(MTS)` (`/links/10/to`) |
| ↳ 변형: 괄호 약칭 + 부위 접미 | string | | `마이크로니들링(MTS) 두피` (`/links/58/to`), `저출력레이저(LLLT) 두피` (`/links/29/to`) |
| ↳ 변형: `/` + 부위 접미 | string | | `HIFES/EMS 바디` (`/links/20/to`) |
| ↳ 변형: 총칭으로 보이는 이름 | string | | `기기 리프팅` (`/links/2/to`) |
| `to_category` · `/links/*/to_category` | string (코드) | 115 · 고유 13 | `M2` (`/links/0/to_category`) |
| `type` · `/links/*/type` | string (라벨) | 115 · 고유 3 | `함께` (`/links/0/type`), `다음에` (`/links/3/type`), `대신` (`/links/7/type`) |
| `reason` · `/links/*/reason` | string (서술) | 115 · 고유 115 · 길이 26–174자 | 짧은 예 `실로 처진 살을 올리고 필러로 꺼진 볼륨을 채움` (`/links/67/reason`) |
| ↳ 변형: `+`·`=` 기호 구성 | string | | `/links/0/reason` |
| ↳ 변형: 여러 문장(`.`) + 근거 제한·부정 | string | 8 값 | `/links/14/reason`(174자) |
| ↳ 변형: `→` 순서 | string | 1 | `/links/114/reason` |
| ↳ 변형: 괄호 주석 | string | | `엘란쎄(PCL)와 래디어스(CaHA)는…` (`/links/36/reason`) |
| `timing` · `/links/*/timing` | string (시점·간격) | 115 · 고유 53 | `같은 날 시술 가능` (`/links/0/timing`) |
| ↳ 변형: 택일 | string | 16 | `택 1 시술` (`/links/7/timing`) |
| ↳ 변형: `X N주/N개월 후 Y` | string | | `보톡스 2주 후 리프팅` (`/links/3/timing`) |
| ↳ 변형: 대안 `또는` | string | 5 | `같은 날 또는 2주 간격` (`/links/21/timing`), `CO2 직후 또는 1주 후 줄기세포` (`/links/87/timing`) |
| ↳ 변형: 범위 `~` | string | 2 | `피코토닝 1~2주 후 스킨부스터` (`/links/82/timing`), `실리프팅 후 2~3개월 뒤 울쎄라` (`/links/71/timing`) |
| ↳ 변형: 조건 | string | 1 | `자가 지방유래 줄기세포(SVF)에 한해 같은 날 가능` (`/links/64/timing`) |
| ↳ 변형: 시간값 없음 | string | 1 | `의료진이 기기 원리·열부하를 평가해 간격 결정` (`/links/96/timing`) |
| ↳ 변형: 기준 시점 없음 | string | 1 | `2주 간격 순차 시술` (`/links/114/timing`) |
| `target` · `/links/*/target` | string (라벨) | 115 · 고유 17 | `안티에이징` (`/links/0/target`) |
| ↳ 변형: `/` 포함 | string | 4종 | `여드름/모공` (`/links/7/target`) |
| 빈 값 | — | 0 | 빈 문자열·null·빈 배열·빈 객체 없음 |

### 3.1 고유값 전체 (원문 그대로 · 출현 수)

- `type`: `함께` 50 · `다음에` 49 · `대신` 16
- `target`: `리프팅` 31 · `안티에이징` 30 · `여드름/모공` 8 · `피부결` 8 · `피부재생` 7 · `흉터/재생` 7 · `색소` 5 · `바디` 4 · `흉터` 4 · `안티에이징 패키지` 2 · `탈모` 2 · `색소/미백` 2 · `얼굴윤곽` 1 · `여드름` 1 · `코성형` 1 · `홍조/혈관` 1 · `제모` 1
- `from_category`: M1 5 · M2 5 · M3 11 · M4 12 · M5 5 · M6 3 · M7 6 · M8 21 · M9 22 · M10 2 · M11 7 · M12 3 · M13 2 · M14 3 · M15 3 · M16 2 · M17 3
- `to_category`: M1 15 · M2 6 · M3 5 · M4 26 · M5 7 · M7 2 · M8 9 · M9 22 · M10 2 · M11 6 · M12 6 · M15 4 · M17 5
- `timing`: `같은 날 시술 가능` 45 · `택 1 시술` 16 · `같은 날 또는 2주 간격` 3 · `필링 1주 후 스킨부스터` 2 · 나머지 49종 각 1회(§5 표에 전부 있음)
- `from`·`to` 명칭 52종(합계 230 출현): `M4-스킨부스터` 28 · `M1-보톡스` 18 · `M5-PRP` 12 · `M9-울쎄라` 11 · `M2-필러` 9 · `M7-실리프팅` 8 · `마이크로니들링(MTS)` 8 · `M11-니들RF` 7 · `기기 리프팅` 7 · `써마지FLX` 7 · `줄기세포치료` 7 · `M3-스컬트라` 6 · `M9-슈링크` 6 · `필링` 6 · `M3-래디어스` 4 · `M3-엘란쎄` 4 · `M4-쥬베룩` 5 · `M8-레이저토닝` 5 · `M8-프락셔널` 5 · `리쥬란힐러` 5 · `M8-IPL` 4 · `M9-더블로` 4 · `M9-인모드` 4 · `CO2프락셔널` 3 · `HIFES/EMS` 3 · `M6-지방이식` 3 · `M8-서브시전` 3 · `M8-피코토닝` 3 · `크라이오리포라이시스` 3 · `M11-시크릿` 2 · `M11-인트라셀` 2 · `M11-포텐자` 2 · `M13-플라즈마` 2 · `M16-수액치료` 2 · `M8-알렉산드라이트` 2 · `M9-볼뉴머` 2 · `M9-올리지오` 2 · `바이오스티뮬레이터` 2 · 1회: `HIFES/EMS 바디` `M1-보톡스(코끝)` `M15-메디컬스킨케어` `M17-엑소좀` `M8-피코슈어` `M8-피코웨이` `M9-인모드(바디)` `다이오드 레이저` `마이크로니들링(MTS) 두피` `보툴리눔 톡신 사각턱` `저출력레이저(LLLT) 두피` `필러 코` `필러 턱` `혈관`

## 4. 상위 값

- `/version` = `1.3`
- `/updated` = `2026-07-26`
- `/links` = 객체 115개 배열(아래 §5 가 전부)

## 5. 항목별 값 — 전체 (원본 컬럼명 그대로, 배열 순서)

각 행의 위치는 `/links/<i>/<컬럼명>` 이다. `reason` 은 길어서 같은 구획 아래 별도 표로 둔다. 표 안의 `|` 는 Markdown 이스케이프(`\|`)일 뿐 원문에는 없다.
{{LINK_VALUES}}

## 6. 잠정 관찰 (원문과 분리)

아래는 모두 **잠정**이다. 근거 위치를 붙였다. 상세·전체 목록은 [link-observations.json](./link-observations.json)(계산 12 + 직접 25).

### 6.1 구조에서 바로 보이는 것 (구조적 사실 + 잠정 해석)

- 모든 `대신` 16건은 from_category == to_category(같은 코드 안의 택일). `함께` 50건 중 같은 코드 4건, `다음에` 49건 중 1건.
- `type=다음에` 49건 중 47건의 timing 은 「from 이름 N주/개월 후 to 이름」 꼴. 예외: `/links/96`(시간값 없음)·`/links/114`(기준 시점 없음). 방향이 from→to 와 반대로 적힌 것: `/links/54`(from 스킨부스터, timing 「필링 1주 후 스킨부스터」) — 같은 쌍 `/links/24` 와 대비(LO01).
- 같은 두 끝점이 여러 번 나오는 쌍 11개(계산). 양방향 `다음에`: 니들RF↔필링(`/11`·`/22`), 스킨부스터↔울쎄라(`/57`·`/104`), 실리프팅↔울쎄라(`/71`·`/105`). 다른 type: 슈링크·써마지FLX 가 `함께`(`/100`)와 `대신`(`/101`), 바이오스티뮬레이터·스킨부스터가 `다음에`(`/45`)와 `함께`(`/55`), 보톡스·기기 리프팅이 `함께`(`/2`)와 `다음에`(`/3`). 역방향 `함께`: 보톡스↔필러(`/0`·`/30`), MTS↔스킨부스터(`/15`·`/53`), 필러↔실리프팅(`/32`·`/67`), PRP↔프락셔널(`/61`·`/78`).
- 총칭 「기기 리프팅」과는 보톡스→리프팅(`/3`), 개별 기기(더블로·슈링크·울쎄라·인모드)와는 기기→보톡스(`/93` `/97` `/103` `/110`) — 순서가 엇갈린다(LO05). 상하 관계는 정하지 않았다.
- 원장 README 는 from/to 에 `Mxx-` 접두를 금지하지만, 실제로는 230 출현 중 171 이 접두를 갖는다. 접두 코드는 모두 같은 link 의 `*_category` 와 일치(불일치 0, 계산).

### 6.2 문장에서 보이는 것 (잠정)

- **link 라벨과 reason 의 긴장**: `/14` `/27` `/76`(함께·「같은 날 시술 가능」)와 `/59`(함께), `/87`(다음에)의 reason 은 개방(미세)채널을 통한 화장품 성분 전달·주입을 「하지 않음」이라 한다. 부정의 범위는 「허가된 멸균 시술용 제제가 아닌」 성분(`/14` `/27`), 「화장품 전달·주입」(`/76` `/87`)으로 한정된다. 라벨을 지우거나 뒤집지 않았다(LO09–LO11).
- **조건이 timing 칸에**: `/64/timing` 「자가 지방유래 줄기세포(SVF)에 한해 같은 날 가능」. reason 도 「…에 한정하며 배양 줄기세포 제제 투여는 불가」.
- **끝점 밖의 시술**: `/2/reason` 「보톡스+필러+리프팅 3종」, `/114/reason` 「리프팅 → 스킨부스터 → 보톡스 순서로」, `/84/reason` 「반복 레이저/IPL이 표준」. 두 끝점 link 로는 담기지 않는 정보다(LO16).
- **대신의 의미 한정**: `/101/reason` 「단순 예산 택1이 아니라 목표(표면 탄력 vs 깊은 처짐)에 따라 선택」, `/113/reason` 방식(RF·HIFU)이 달라도 「대체 가능」(LO24). 선택 기준 표현: 팁 종류·가격(`/8`), 병원 보유 장비(`/9`), 파장·특성(`/79`), 피부 톤·부위(`/85`), 상황(`/86`), 예산·선호(`/99` `/112`), 가격·통증 정도(`/107`).
- **깊이·층 대비**: 「깊은 층」/「얕은 층」/「표피」/「진피 표면」/「SMAS 심부」/「전층·전체 층」(`/100` `/101` `/108` `/109` 등). 수치는 원문에 없다. mm 로 바꾸지 않는다.
- **정도·지속·속도 수식**: 「효과 극대화」「재생 효과 배가」「효과 오래 유지」「회복이 빠름」「흉터를 점차 채움」「과도한 근육만 선택적으로」. 시간 기준·수치 없음.
- **근거 수준 표현**: 「임상 검증은 제한적」(`/14` `/27` `/59` `/64` `/76` `/87`), 「확립된 임상근거가 제한적」(`/25`), 「입증되지 않았으며」(`/84`), 「고려할 수 있으나」(`/76` `/87`). 같은 from 의 `/64`(줄기세포 혼합: 생착률 근거 제한)와 `/65`(PRP 혼합: 생착률 「올라감」, 한정 없음)는 대상이 다르다(LO12).
- **부위**: 이름 안(`필러 턱`, `M1-보톡스(코끝)`, `… 두피`, `HIFES/EMS 바디`)과 reason 안(사각턱·턱끝·V라인·콧대·코끝·두피·모낭·얼굴·몸매·바디라인)에 있다. `/4` 는 to 「필러 턱」, reason 「턱끝 필러」로 표기가 다르다. 괄호는 부위(`(코끝)`)와 약칭(`(MTS)`)에 함께 쓰여 형식만으로 구분되지 않는다(LO19).
- **동형어 「동안」**: `/0` `/38` `/46` `/47` `/50` `/63` 의 「동안」은 문맥상 童顔으로 읽힌다(잠정). 시간 표현 「~동안」과 표기가 같다(SR22).
- **명칭 표기 차이**: timing 안의 이름이 from/to 와 다르다 — 「리프팅」(from M9-울쎄라, `/103` `/104`), 「써마지」(to 써마지FLX), 「리쥬란」(리쥬란힐러), 「혈관레이저」(from 혈관), 「크라이오」, 「CO2」, 「줄기세포」(LO17).

## 7. 형태소 분석

| 항목 | 값 |
|---|---|
| 분석기 | Kiwi (kiwipiepy 0.24.1), model_type `cong`, num_workers 1, `OMP_NUM_THREADS=1` |
| 실행 환경 | `uv run --python 3.12 --with kiwipiepy==0.24.1` |
| 옵션 | tokenize 기본값(normalize_coda=False, z_coda=True, split_complex=False, saisiot=None, compatible_jamo=False, split_sents=False, typos=None, blocklist=None) |
| 사전 | 기본 내장 사전만. 사용자 사전 없음 |
| 기본형 | Kiwi `Token.lemma` 값 그대로. 만들어 채우지 않음 |
| 길이 0 토큰 | Kiwi 가 표면에 없는 서술격 조사 `이/VCP` 를 복원한 7출현(`울쎄라`·`리쥬란`·`치료라`·`리프팅이라`·`기기라`·`울쎄라는`). 구간 `[k,k]`, `zero_length=true`, surface 빈 문자열로 그대로 보존 |
| 적용 | `/links/*/from` `/to` `/type` `/reason` `/timing` `/target` — 690 값 |
| 제외 | `/version`(버전 표기) 1 · `/updated`(날짜) 1 · `/links/*/from_category` 115 · `/links/*/to_category` 115(코드값 `^M\d+$` 확인) — 232 값, 출현별 사유는 morphology `excluded_values` |
| 필드명 | 11종 전부 분석(영문 식별자, SL). `_` 분해는 규칙 기반이며 분석기 산출 아님 |

### 7.1 알려진 오분절·의미위험 (출현별 표시, 교정 아님)

구절 규칙은 [segmentation-review-rules.json](./segmentation-review-rules.json). 각 구절의 **모든 출현**에서 겹치는 원시 토큰을 변형(variant)과 대조해 판정했다. 어느 변형과도 안 맞는 출현이 있으면 빌드가 실패한다.

| 규칙 | 구절 | 원시 결과 | 영향 | issue/ok 출현 |
|---|---|---|---|---|
| SR01 | 필러 | `M2-필러` → 필/NNP 러/EC; `코필러` 한 토큰 | 명칭 소실, 부위 미분리 | 10 / 15 |
| SR02 | 더블로 | 더블/NNG 로/JKB; 더블로로/NNG | 명칭이 '더블'+조사 | 8 / 2 |
| SR03 | 볼뉴머 | 보/VV ᆯ 뉴 머/EC 또는 볼/뉴/머 | 허위 동사 '보다', '볼' 부위 오인 위험 | 4 / 0 |
| SR04 | 인모드 | 인/NNG 모드/NNG | 명칭 소실 | 10 / 0 |
| SR05 | 써마지 | (timing) 쓰/VV 어 마/VX 지/EF | 허위 '말다'(부정 오탐) | 2 / 12 |
| SR06 | 울쎄라 | 울쎄/NNG 이/VCP 라 | 명칭 잘림 | 3 / 16 |
| SR07 | 리쥬란 | 리쥬 + 란/JX 등 | 명칭 잘림 | 3 / 9 |
| SR08 | 쥬베룩 | 쥬베/룩 | 명칭 소실 | 1 / 10 |
| SR09 | 슈링크 | 슈/NNP 링크/NNG | 명칭 소실 | 1 / 11 |
| SR10 | 올리지오 | 올리/VV 지 오가/VV | 허위 동사 둘 | 1 / 3 |
| SR11 | 피코초 | 피/코/초 | '코' 부위 오탐 위험 | 1 / 0 |
| SR12 | 열부하 | 열/NR | 수량 오탐 위험 | 1 / 0 |
| SR13 | CO2 | CO/SL 2/SN | 숫자 독립, 「CO2 2주」에서 2 두 번 | 8 / 0 |
| SR14 | `M\d+-` 접두 | M/SL 숫자/SN -/SO | 코드 숫자가 수량처럼 독립 | 171 / 0 |
| SR15 | 실로 | 실로/MAG | 수단 '실' 소실, 허위 부사 | 6 / 1 |
| SR16 | 자가 | 자/NNB 가/JKS | 출처 수식 '자가' 소실 | 2 / 4 |
| SR17 | 풀고 | 풀고/NNG | 행위 소실 | 1 / 2 |
| SR18–20 | 크라이오로·래디어스로·스컬트라로 | 명칭+조사 한 토큰 | 조사 미분리 | 7 / 2 |
| SR21 | 통한 전달 | 전/MM 달/NNG | 금지 대상 핵심어 소실 | 1 / 0 |
| SR22 | 동안 | 동안/NNG | 童顔/시간 구분 불가 | 6 / 0 |
| SR23 | 둘 다 | 두/VV ᆯ/ETM 다 | 범위 표현 소실 | 1 / 9 |
| SR24 | 리프팅이라 | 리프팅이/NNG 이/VCP 라 | 표면 겹침 | 1 / 1 |
| SR25 | 에 한해 | 한/NNG 하/XSV 어 | 기본형 '한하다' 미제공 | 1 / 0 |
| SR26 | `\d+주` | 주/NNG(대부분 NNB) | 품사 불일치 | 3 / 41 |

품사 서명 판정([pos-review-rules.json](./pos-review-rules.json)): MAG·MAJ·MM·NR·NP·VCN·XPN·VX 의 **모든 출현** 135건을 (form, tag) 서명 31개로 판정, issue 10(실로/MAG 6 · 열/NR 1 · 마/VX 2 · 전/MM 1 — 모두 위 규칙과 같은 출현). 부정 신호 `않/VX` 6 · `아니/VCN` 3 · `미/XPN` 4 는 보존됨.

한계: NNP/NNG 구분, VA/VV 구분, 규칙 밖 명사 분절은 출현별로 판정하지 않았다. 형태소 기본형은 도메인 표준명이 아니다.

## 8. 복합 표현

[expressions.json](./expressions.json). 범주는 탐색 관점이며 확정 분류가 아니다. 같은 구간이 여러 범주에 걸치는 것은 의도된 겹침이고, 같은 pointer·span·범주·방법의 중복은 0이다(verify).

| 방법 | 범주 |
|---|---|
| 값 전체 / 문장('.') / 기호 분할(`,` `+` `=` `→`) | `segment.value` `segment.sentence` `segment.operator_part` |
| regex | quantity_time · time_reference · sequence_marker · negation · possibility_hedge · condition_scope · condition_connective · alternative_connective · degree_intensity · depth_layer · region_candidate · material_annotation · symbol_operator · selection_criterion · evidence_regulatory · risk_event · state_appearance_modifier · origin_modifier · comparison · name_candidate(실+로) |
| keyword | name_candidate — [name-keywords.json](./name-keywords.json) 139개(from/to 52종 + 접두 제거형 + 원문에서 본 명칭) |
| manual | 절 단위 82건 — negation_scope · condition_scope · hedge_evidence · regulatory_statement · risk_statement · selection_criterion_clause · depth_contrast · multi_entity_reference · definitional_annotation 등 |

오탐 표시 12건([expression-review.json](./expression-review.json)): 명칭 「더블로」 안의 「더블」을 degree 로 잡은 10건, 혈관(대상·라벨)을 명칭으로 잡은 2건. 지우지 않고 `review.verdict=false_positive` 로 표시했다. timing 「같은 날 시술 가능」의 「가능」은 가능성 추정이 아니라 허용 진술로 읽히지만(잠정) possibility_hedge 후보로 남겼다.

regex·keyword 결과는 전수 의미 해석이 아니다. 효과·결과 어휘(「피부결 개선」「볼륨 채움」 등)는 범주 후보를 따로 만들지 않고 문장·기호 분할 구간과 manual 절로 보존했다.

## 9. 미결

[issues.md](./issues.md) 에 원문 정보 부족 · 잠정 해석 · 후속 의미 조사 · 원본 수정 관련 후속 검토 후보(U — 처음엔 사용자 결정 필요로 적었다가 재분류, 현재 사용자 선택 대기 0)를 구분해 적었다.
