# 미확정 자료 HTML 결정 카드 아티팩트

## 사용자 요청·범위

사용자는 현재구현완료보고후미확정자료를하나씩카드로보고결정하고그결과를반영할수있는HTML아티팩트를요청했다. 첫candidate P0~P4완료, 코디validator재실행PASS, P5독립검수는별도진행중이다. **이번은실제candidate근거를검토할결정UI/수출입포맷작성만**, 원장/실버/candidate에결정을적용하지않는다.

DATA-001/WORK-013, silver-batch1-implementation/report.md, candidate의records/source-row-index/mapping-ledger/identity-ledger/coverage/input-outputmanifest를읽는다. 기존미부착152 safety field(candidate49/out_of_batch83/owner_unresolved20)를실제로전수추출하여목록누락0·중복0으로만든다. 152는독립원장질문152개가아니라원문field수다. 같은source행/같은결정으로묶을수있으면카드상단은행별그룹으로하되모든원문field를하위카드에서개별확인·결정가능하게한다. 서로다른claimscope를임의합치지않는다.

## 카드내용·결정

- 사람읽는이름·자료유형·현재대상/후보label, 미부착이유(후보여럿/이번범위밖/대상미확정), 원장원문과그주변문맥, 실제출처file/JSONpointer·원문판hash, 현실버값·candidate상태·기존매핑근거를보여준다. 기술ID는접어서확인가능하되원문출처는확인쉬워야한다.
- 무엇을결정해야하는지평이한한국어로각카드에한문장, 권고처리안과근거·확신불가사유를쓴다. 자료에없는임상판단을권고로창작하지않는다. out_of_batch는정보없음이아니며단순후속이관이면'후속묶음으로유지'같은처리선택이다. 원천확인필요와데이터변환으로해결가능한경우를구분한다.
- 선택은미선택기본이며보류/원장확인/후속이관유지/근거있는대상연결제안과메모를지원한다. 연결대상은실제registry후보만허용하고자유입력은entity자동생성이아닌텍스트수정제안이다. 제품선택·clinical승인을자동생성하지않는다. P5미검수상태를명시한다.
- 원문이나관계근거없이자동대상확정을권하지않는다. 공통선택일괄적용은명시범위·미선택대상수와확인동작으로만가능하고각field의개별결정/재설정을지원한다. 카드판단이현재이관범위밖이거나clinical원천확인인경우상태를그대로보존한다.

## 아티팩트·동작

쓰기허용 silver-decision-cards/만: index.html 단일offline파일, cards.json, decision-schema.json, README.md, 검증script/results. 외부CDN/font/library/fetch/import/서버/설치없음. inline실제data는escape하여script종료주입방지. 검색·이유필터·미결/작성/검토완료필터·진행률·카드북마크·원문펼치기·모바일·키보드UI. 원문긴배열은정보를숨기지않고구조표시/접기지원.

결정은localStorage에best-effort저장(file환경차이대비)하고명시JSON내보내기/불러오기지원. 저장보장으로오인시키지말고JSON백업안내. 내보내기에는schema_version/artifact판/candidate input+output fingerprint/card stableID/claim+sourceID·rawhash/선택·이유·사용자입력·실제결정시각을포함한다. 작성전가짜결정/날짜금지. 다른candidate판·알수없는카드/중복ID·잘못된enum/대상/자료hash·형식오류import는거부하고사용자편집이덮이지않게한다. 클라이언트내UI는DB/원본에쓰기없음. '적용완료'표시금지, '결정내보내기'로후속검증·반영과구분.

## 검증

152필드정확집합·이유49/83/20·원문/source/provenance·각카드refs·candidate판hash·결정schema/UIexport-import정합을검증한다. 실제브라우저검색/필터/개별선택/저장복원/JSONexport-import/미지원판거부/모바일·한글원문표시를확인한다(기존로컬Chromium사용가능). 테스트파일은이폴더안에만. P5결과가아직없으면미검수로고정하고그상태를속이지않는다.

P5worker는읽기전용별도경로다. 이worker도candidate/migration/원장/실버/설계/스펙/WORK/manifest/앱·Hub/env/DB/서버수정금지. 네트워크/모델/업로드/임의설치/하위worker/commit/push/PR금지. 새clinical정보를검색하지않는다. report/README에그룹카드수와field152분모·검증·제약·인계결정JSON반영절차를기록한다. 시작/종료candidatehash불변을확인하고liveOrca preamble의inbox/heartbeat/worker_done한번후멈춘다.
