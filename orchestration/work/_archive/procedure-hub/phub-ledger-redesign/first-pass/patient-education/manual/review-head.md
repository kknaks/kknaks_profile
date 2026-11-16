# review — patient-education.json 1차 조사

> **1차 수집 범위: 종료** (아래 상태표 기준) · **원장 전체 완료 아님** — 원문 정보 부족 B·잠정 P·후속 F·원문 표기 이상 I·알려진 분석 한계 K 가 열려 있다. 의미 관계·정규화는 하지 않았다.

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/patient-education.json` (읽기 전용)
- sha256 `6c96520c514b76ef7f93d7f685e53023afe91b05133a9b9ca5db0a95d42d91ac` · 26,551 bytes · 13,043 코드포인트 · 한 줄(minified) JSON · 줄바꿈 0 · 백슬래시 이스케이프 0 · 중복 키 0 · BMP 밖 문자 0
- 조사일 2026-11-09 · 이 원장 외 다른 원장은 열지 않았다

## 상태

| 단계 | 상태 |
|---|---|
| 전수 읽기 | 18/18 구획(S00 상위 메타 + S01~S17 카테고리 17개) 원문을 위에서 아래로 직접 읽음. 각 구획 기록은 `manual/S*.json`, 진행은 `progress.md` · `coverage.json` |
| 구조·값 수집 | 노드 327(객체 69·배열 18·문자열 240) · 말단 240 · 빈 컨테이너 0 · 빈 문자열 0 · 숫자/불리언/null 0 — `source-map.json` |
| 형태소 | Kiwi(kiwipiepy 0.24.1, cong, 스레드 1, 사용자 사전 없음) 적용 221값 4,989토큰 · 제외 19값(version·updated·id) · 필드명 14종 제외(영문 식별자) · 알려진 오분절/오태깅 25출현 기록(교정 안 함) — `morphology.json` |
| 표현 수집 | 직접 읽기 표현 806건(문장 231 포함, 겹침 의도) · 보조 정규식 후보 572건(패턴 일치분뿐) 중 수동 구절 밖 49건 전부 판정(문장 단위 보존 43 · 오탐 6) — `expressions.json` |
| 기계 검증 | `verify.py` 34,232검사 실패0(원본 해시 시작/끝 불변·양방향 대조·구간 재현·구획 소유·문서 대조·변이 시험) — `validation.md` |
| 읽기 검토 | 작성자 별도 읽기 검토 1회: 형태소 수식어(MAG·VA·XR·XPN·부정·조건 어미) 대조로 패턴 밖 구절 27건 보충·오태깅 1건 추가. 독립 검토자 검토는 아직 없음 |
| 열린 미결 | B 36 · P 42 · F 10 · I 1 · K 1관찰+25출현 · A 0(발견분 수정) · **C 0** — `issues.md` |
| 후속 의미 조사 | 시작 안 함 |

## 이 원장의 형태 (요약 — 상세 값은 구획 파일)

`{version, updated, categories[17]}`. 각 카테고리는 같은 9키(id·name·patient_name·simple_explanation·how_it_works·duration_simple·pain_level·downtime·common_concerns)를 갖고, `common_concerns` 는 언제나 `{q, a}` 3개다. 모든 말단이 문자열이다. 언어별 필드는 없고 한국어 문장에 라틴 약어(PRP·RF·SMAS·PIH·AHA 등)·제품명·수치가 섞여 있다.

같은 키 이름 아래 정보 종류가 다르다(잠정 관찰): `duration_simple` 은 지속 기간·발현 시점·반복 회차·생착률(%)·최대 효과 시점을 오가고, `downtime`·`pain_level` 은 종류별 세분(「토닝: … / 프락셔널: …」)이 들어간다. `common_concerns/*/a` 에는 행동 지시·금기 대상·근거 서술·규제 서술·위험 목록이 섞여 있다.
