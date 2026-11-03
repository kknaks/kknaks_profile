# WORK-013 P5 첫 candidate 독립 검수

계획 단계4의 독립 검수. DATA-001/2·WORK-013·84필드계약·contract-fix 승인manifest v2와 실제원문을 기준으로 silver-batch1-migration/** 및 candidate/**를읽기전용검수한다. 구현보고 silver-batch1-implementation/report.md의P0~P4 PASS를 독립확인하며정본전환권한없다.

필수: 제품395/계열27/membership354·active/inactive/null/pending/84필드엄격타입·명시원천/허가/업체역할/continuity/needs_design; 안전580행1394field4170leaf·원문16leaf/소실10복구·정상rename·override624연결; eligible1242/not_created152(49/83/20)의단일owner근거·152원문보존·미부착사유; source/raw·normalized·scope·refs·ID/판/감사분리·규칙고정·입력판·원천단독oracle/검사자기참조를검수한다. source label/id이름추정이나임상승격없음, typed미구현을raw보존으로대체완료처리하지않음을확인한다.

원문을직접읽고검증기·명시변조35·positive14·재현2회·실제이동은쓰기sink와tmp를아래검수폴더로바꿔원candidate불변으로검증한다. 코드실행후검수대상hash불변검사. ID재계산뒤부정값이관련진단에서거부되는지핵심추가반례를확인하되무제한pilot재설계로확대하지않는다. 42사례/146combo는기존회귀이지이번이관실적이아니다. 미승인임상/허가최신성/전체247필드완료승인금지.

카드아티팩트worker가별도경로에서미부착152를정리중이며코드/데이터는수정하지않는다. P5에서misclassification이발견되면정확한claim/sourceID·사유를보고하여카드판에도반영할수있게한다. 작성허용 silver-batch1-review/**만. 기존migration/candidate/원장/실버/설계/스펙/WORK/manifest/앱·Hub/env/DB/서버무변경. 네트워크/모델/설치/하위worker/commit/push/PR금지. 구현worker가runtime user_takeover retained이므로시작/종료기준hash를고정하고공유변경시판을혼합하지않는다.

report.md에PASS/FAIL·severity·구체적재현·정상대조·분모/coverage·입력/출력manifest확인·정본무변경·전환전제조건을쓴다. liveOrca preamble대로inbox/heartbeat/worker_done한번후멈춘다.
