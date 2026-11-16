# P5 BR-H1/BR-M1 독립 source validator 보완

WORK-013 P5 report silver-batch1-review/report.md의High scope의미검증/Medium line관계누락검증을고친다. 현재candidate값/원문보존/152미부착분류는독립검수에서정상이며검증기가잘못된변조를받는문제다. DATA-001/2·WORK-013·84fieldcontract·manifestv2를유지한다. 새임상판정/데이터설계확대금지.

BR-H1: builder/rules변환을oracle로import하지않고원문·고정fieldcontract로각scope의축전체(knowledge/value_kind/included/excluded/raw_refs)와statement_qualifiers 전체(raw/source/state/operator/value), expectedparent·conflicts·application을독립복원하여exact비교한다. 제품/계열/membership/safety의모든1002scope를대상으로하며excluded발명·qualifier삭제/치환/추가·원문ref변경을ID재계산/sidecar/outputhash정합후에도관련진단으로거부한다. 원문미해석context를임상정규화하지않고현재정상값과unknown은유지한다. generic집합/refs검사도유지.

BR-M1: product.line_memberships 기대전체집합을원문 row.line·lines.items의명시ledger_id/line_row만으로복원하고누락/추가/role/source근거/parent변경을검사한다. 이름추정/새approval금지. 원문에없거나needs_review인parent는기존미정mapping·fieldstate와함께대조한다. 나머지typed필드를raw만보존해서완료처리하지않는다.

쓰기허용 migration/validate.py·test_contract.py 및필요신규독립검사helper와 silver-batch1-validator-fix/**(report/변조복사본/tmp/검증결과/시작끝hash)뿐이다. builder/rules/transport/type-contract·원candidate/**·원장/실버/기존P5검수·계약/manifest/스펙·HTML/cards·환경/서버·DB무변경. validator수정으로candidate output-manifest·data·validation파일은**재작성하지않는다**. CLI결과는stdout/별도fix results로저장하고원본CLI가쓰기한다면직접함수또는검증용복사본에서실행한다. 다른파일이반드시필요하면근거와ask. 카드worker가원candidate읽는중이므로payload/manifest불변필수.

원P5 full_cli_probes.py/full_qualifier_probe.py 방식으로검증용copy만이폴더아래에서변조하고 normalizedID·sidecar·outputmanifest를모두정합시킨뒤수정validator전체CLI에서3반례거부를확인한다. 원본raw값변조대조와정상positive/기존35negative14positive·추가line삭제/role/partial소실·다른scope유형제외/qualifier변조를ID검사가아닌의미진단으로확인한다. 기존재현/이동결과는변경없는builder기준증거로보존하고새validator가원candidate와재현본을수용하는지만확인한다. 무관한대용량재생성반복금지.

report.md에각finding폐쇄·현재정상candidate불변·새코드hash/독립원문검사·CLI재현·남은P5재검수·152원문분류영향없음을쓴다. 원문/코드불변범위를시작끝검사. 네트워크/모델/설치/하위worker/commit/push/PR금지. liveOrca inbox/heartbeat·worker_done한번후멈춤.
