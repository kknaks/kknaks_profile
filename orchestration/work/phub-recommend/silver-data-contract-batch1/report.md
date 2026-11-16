# DATA-001·WORK-013 작성과 첫 묶음 원천 검증 보고

2026-11-03 · Task `task_2fd07ab75479` · Dispatch `ctx_1588545777eb`.

**문서 작업 완료. 구현·candidate 생성·정본전환은 미실행이다.** [DATA-001](../DATA-001.md)을 먼저 완성하고 [WORK-013](../WORK-013.md)을 작성했다. 이 보고의 PASS는 문서·원천 locator·분모·보호입력 검증이며 독립 설계검수/전수 이관/임상승인 PASS가 아니다.

## 1. 채택한 계약과 기존 설계와의 차이

검수된 core의 domain/collection/logical key/물리 locator 분리, 정렬 full-hash manifest snapshot, source occurrence/native entity/normalized revision 수명 분리, typed refs, scope knowledge·포함/제외·원문 parent, 실제 source/version/구현 fingerprint 대조를 DATA-001에 부분 채택했다. HTML/design.json은 제안 증거 그대로 보존했다.

pilot 전체스키마를 복사하지 않았다. 본설계12축과 pilot10축, declared/explicit·unresolved/unknown의 조건부 alias, 직접 변환할 수 없는 축을 구분했다. mapping.rule nullable+reason, LOSS02 unit U5-016, first enum/options·same_day 구분, override/source/pair provenance를 반영했다. candidate용 새 source-preservation 규칙판과 entity-target decision DAG 경계를 명시하고, pilot duration/attachment의 검증 범위를 새 전체지원이라고 확장하지 않았다.

25논리타입 모두에 소유역할·Gold 독립노드13종/record/embedded 속성 대응·기존 coverage·이번 범위를 적었다. product/family prototype 네 칸을 실제 typed 속성으로 확장하는 실행계약과 source 원문/필드상태 sidecar를 정했다. 미정/설계 미확정/비적용/원천 미기재, identity/clinical 승인, source claim/resolution/검색 attachment를 분리했다.

## 2. 실제 읽은 분모와 원천 증거

| 대상 | 직접 재집계 | 증거 |
|---|---:|---|
| step1 제품 | 395, unique native ID395, active354/inactive41 | [recount](results/recount.json), [field 검증](results/field-validation.json) |
| step2 제품계열/계열 | 354/27, unique family ID27, active 제품 ID집합과 mapping source ID집합 일치 | 같은 결과 |
| 미정 계열 | family=null3/pending_director3 | 같은 결과; 임의 해소0 |
| 안전 원문 입력행 | extracted521 + taxonomy_products59 =580 | [행별 raw/current locator](results/safety-origin-locators.json) |
| safety/aftercare 원문field | 1,394, scalar잎4,170 | [독립 field oracle](results/safety-field-oracle.json) |
| 기존 override | 624(units248/product_links376) | [override inventory](results/override-inventory.json) |
| 알려진 common 충돌 | 3행/6원문field/16잎, 기존 소실10잎 | [collision oracle](results/collision-oracle.json) |
| 계열 기본기법 | 27행, 기존 registry ID 도달 오류0 | [field 검증](results/field-validation.json) |

580행 raw/current 순서와 native ID를 전부 대조했고 각 safety/aftercare field pointer도 실제 값과 대조했다. 독립 raw reader에서 기존 last-write 정규화를 적용하면 현행 source_text580행과 일치한다. 이는 현행 손실 분기의 재현이며 **손실 복구를 실행했다는 뜻이 아니다**. candidate는 충돌6field/16잎을 각각 보존하고 override 연결까지 before/after로 복구해야 한다. 비충돌 정상 rename도 유지하도록 WORK-013에 고정했다.

허가·규격·업체 원문은 step1 전체행/연구 artifact를 보존하는 계약이다. 새 허가/API/문헌 조회 또는 현재 허가 재인증0이다. raw21과 역사 조사/결정 artifact를 구분한 [69파일 input manifest](results/input-manifest.json)를 남겼다. `_RESUME.md`는 현재 코디 기록의 고정판이며 이후 변경은 구현 시 명시 reconciliation이 필요하다.

## 3. 필드 coverage와 미정

[필드 계약](field-contract.json)은 **product14 + family11 + 공통59 =84 제안필드**를 담는다. 공통은 snapshot5/source_record8/scope6/claim14/mapping9/decision8/attachment9다. 각 행에 제안 타입·필수·빈값·실제 current/source locator 또는 derived 생성근거·변환·출처 권한·기존 상태·독립 oracle을 적었고 제품/계열 직접 current locator4,576개를 추가 열거했다.

84필드의 기존 상태는 pilot검증55/원문raw보존만12/계약만14/미구현3이다. 이 값은 새 이관 실적이 아니다. 나머지163키도 별도 목록으로 보존했고 전체247의 기존 상태(78/33/71/62/3)는 수정하지 않았다. product/family typed field가 전수 이관됐다고 표시한 필드는0이다.

코디네이터 ask 답변에 따라 subfamily.key/axis·purpose.id는 새 stable key를 발명하지 않는다. 원문·legacy ID/관계를 보존하고 family.subfamilies의 typed stable-key 미발급을 needs_design으로 표시하며 전체 typed 완료에서 제외했다. 실제 후보 의미·사용위치·영향도 DATA-001 §9에 적었다. technique_defaults는 기존 ID 도달성 검증과 참조 보존만 하며 기법 의미·전수이관은 제외한다. 이 상태는 임상 미정/원천 미기재/not_applicable과 다르다.

## 4. 검증 결과와 재현

[document-validation.json](results/document-validation.json): **PASS**. 84필드 문서행·247키 연결·로컬 링크·표 열수·코드펜스를 확인했고 누락/깨진 링크/표 오류0이다. 기존 coverage의 origin/current locator1,186개 + typed evidence199개 =1,385개, 추가 current field4,576개를 실제 JSON에서 확인했다. raw safety field1,394개와 override624개도 실제 pointer에서 확인했다. 이 locator 수는 중복을 포함한 검사 수이며 고유 임상 사실 수가 아니다.

기존 작업폴더·raw21·승인 WORK 등 보호입력 **1,560파일 SHA256/bytes 변경0**이다. 시작값은 [protected-start.json](results/protected-start.json), 종료 대조는 document-validation에 있다. 원장/실버/decisions/apply/semantic/HTML/design/v1/v2/기존 review·SPEC·WORK·앱·Hub·환경 수정0, DB/서버/네트워크/모델/설치/하위worker/commit/push/PR 실행0이다.

검증은 표준라이브러리 Python의 읽기전용 inline 검사로 실행했다. 구현코드나 검사 runner 파일은 만들지 않았으며 아래는 저장 증거를 다시 대조하는 최소 명령이다. 전체 재집계·locator/field값은 위 결과 JSON에서 독립 재구성할 수 있다.

```sh
python3 - <<'PY'
import hashlib, json, pathlib
b = pathlib.Path('orchestration/work/phub-recommend/silver-data-contract-batch1')
for row in json.loads((b/'results/protected-start.json').read_text()):
    p = pathlib.Path(row['file'])
    assert p.stat().st_size == row['bytes']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256'], p
c = json.loads((b/'field-contract.json').read_text())
assert len(c['fields']) == 84 and len(c['excluded_fields']) == 163
cache = {}
for row in json.loads((b/'results/safety-field-oracle.json').read_text()):
    file = row['raw_file']
    if file not in cache: cache[file] = json.loads(pathlib.Path(file).read_text())
    value = cache[file]
    for key in row['raw_pointer'].split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    assert value == row['raw_value']
print('protected inputs / 84+163 fields / safety raw oracle: PASS')
PY
```

## 5. 다음 구현 전제조건

코디네이터의 독립 문서검수 후 WORK-013을 그대로 구현 브리프로 삼을 수 있다. 새 코드경로는 `silver-batch1-migration/`, 출력은 `silver-batch1-candidate/`로 같은 slug 안에 고정했다. 입력 hash 불일치는 중단하며 새 schema/ref/rule판, 전체분모 typed/raw candidate, 원천claim·mapping/identity ledger·247 coverage·오류 before/after·정/부 반례·이동/재현 검증을 요구한다.

종료점은 candidate 독립검수와 보고다. candidate검수→정본권한/전환승인→별도 전환→이전 manifest 기반 rollback을 분리했고, 이번 문서나 차기 candidate 구현이 서비스/DB/Gold 반영 권한을 주지 않게 했다. concern/combo/site/technique/unit/package/condition/literature 전수이관과 임상 의미 검수는 후속이다.
