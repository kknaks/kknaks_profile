# 실버 엔터티 필드·골드 노드/엣지 최종 설계안 조사와 HTML

## 사용자 요청·결과

사용자는 실버 엔터티별 필드가 정확한지 추가 조사하여 최종 엔터티 구조, 각 노드의 구조, 엣지 관계를 HTML로 정리하라고 요청했다. 현재 데이터 수정이 아니라 **근거에 기반한 전체 데이터 설계 문서**가 목표다. 기존 조사 보고의63필드 제안만 꾸미지 말고 실제 엔터티별 필드와 관계를 조사·설계한다. 조사 근거가 부족한 임상 의미는 확정하지 않는다.

## 입력과 조사 기준

이 폴더 silver-origin-structure-audit/report.md, issues.json, inventory.json, field-census.json, schema-proposal.json, id-design.json을 읽는다. 사용자 지정 reference/2026-10-27-skills-procedure-hub의 README 및 관련 전체 SKILL/record-schema/규칙, 현재 step1~9 실버·결정·semantic·생성기, 원문21 snapshot을 대조한다. 원문 위치와 실제 소비 경로는 위 inventory를 사용한다. Hub graph builder/facts/memory/schema는 읽기 전용으로 참조하되 Gold export나 앱 요구를 원장 정답으로 삼지 않는다. AGENTS/문서 규약을 따른다.

## 조사·설계 내용

1. **현행 엔터티·필드 전수 목록**: 실제 step1~9/semantic에서 엔터티·주장·관계·판정·조회용 파생물을 구분한다. 제품/계열·하위/부위/기법/단위시술/패키지/고민·목적/조합/조건/위험·합병증/설명·근거 등 실제 타입을 누락하지 않는다. 이름만 다른 같은 개념, 한 필드에 여러 의미가 섞인 경우, 엔터티 속성과 주장 속성의 혼재를 표시한다. 현재 필드와 값의 의미를 원문/규약에 대조하고 검토 coverage를 명시한다. 전수 임상 재인증을 주장하지 않는다.
2. **제안 실버 엔터티 계약**: 각 타입마다 목적·고유ID·버전/수명·필드명/타입/필수/기본값/빈값·unknown 의미/참조대상/원장 locator/정규화 규칙/검수 불변식을 구체적으로 적는다. 기존ID 유지·legacy 대응·이름변경/재정렬/분할합병 규약을 포함한다. scope/claim/mapping/decision/resolution/attachment의 논리 분리와 실제 저장 위치를 제안한다. 모든 것을 별도 그래프 노드/DB 테이블로 만드는 과설계는 피하고 저장 레코드와 serving graph를 구분한다.
3. **골드 노드 계약**: 실버 타입 중 무엇이 노드가 되고 무엇이 속성/별도 근거 레코드인지 명확히 결정안을 제시한다. 각 노드 id/type/label/자체 속성/source refs/scope/status 및 상속 허용 범위를 정의한다. products·unit·family 등에서 상속/후보/실제선택을 구분한다. 현재와 제안의 변경점 및 근거를 붙인다.
4. **엣지 계약**: 모든 현행 edge kind를 builder/semantic에서 목록화하고 유지/변경/폐기/추가 대응표를 만든다. 제안 관계마다 from/to 타입·방향·cardinality·역방향 의미·중복/병렬엣지 허용·고유성키·필수속성·source_claim_refs·scope/조건·확정/후보·상속/파생·조회용 attachment 여부·금지 연결·실제 예를 정리한다. 삼항/n-ary/조건부 순서·같은날·간격을 단일 무조건 binary edge로 납작하게 만들지 않는다. 직접근거와 파생을 구분한다.
5. **실물 사례 검증**: 안전 alias 충돌3행, 튼살 동명이행2개, singleton21, note7의 기존 R8 refs, 팔자/목 원장상충, 비교 필러 ambiguous 후보, same_site 순서조건, 다계열 product override, K8 준비/상담, patient 언어한정, 보수 resolution을 새 구조에 표현한다. 원문→실버레코드→골드노드·엣지 사례를 포함하며 새로운 임상값은 만들지 않는다. 문헌/허가 최신성 검증은 범위 밖이고 source/version을 표시한다.
6. **이관·수용**: 기존필드→제안필드/분리/보존/폐기 사유 mapping, 데이터 fidelity/ID참조/매핑상태/조건/역추적·충돌 검사, 단계별 수정순서·원천확인 질문을 정리한다. 최종 '권고 설계안'은 구체적으로 제공하되 미확정 사항과 사용자 검토 전 상태를 분명히 한다. 향후 앱 수정 계획보다 데이터 구조를 우선한다.

## HTML 산출물

작성 허용은 이 폴더 silver-entity-graph-design/ 하나다. index.html을 **외부 CDN/라이브러리·네트워크 없이 브라우저에서 바로 열리는 단일 HTML**로 만든다. 함께 design.json(기계가 읽는 타입/필드/edge계약), evidence.md(정확한 파일:줄 또는 JSONpath), validation.json과 필요 오프라인 검사 script만 둔다. 링크·검색·엔터티/노드/엣지 필터, 현재/제안 구분, 타입별 상세 필드 표와 노드관계 SVG 도식, 사례별 추적을 제공한다. 제안/확인/미정은 색과 텍스트로 함께 표시한다. 중요 상세는 접을 수 있지만 초기 화면에서 전체 구조와 핵심 문제를 읽을 수 있어야 한다. 한글 가독성·키보드 탐색·모바일 가로스크롤을 고려한다. 색은 절제하고 장식보다 구조 이해를 우선한다.

HTML은 파일로 열었을 때 동작하도록 데이터를 inline하고 fetch/import/원격폰트/CDN을 쓰지 않는다. 표 HTML escaping과 source 문자/JSON script 종료 이스케이프를 지킨다. 엔터티/필드/edge 목록이 design.json과 일치하는지, 모든 참조 타입 존재/고유ID/앵커/구문/필수 계약 칸·근거 링크가 유효한지 검증한다. 로컬 Playwright/브라우저가 이미 있으면 렌더·검색/필터·표시를 확인하고 그렇지 않으면 검증 한계를 보고한다. 임의 패키지 설치/외부 서비스 업로드 금지.

## 경계·보고

원장·실버·decisions/apply·스킬·semantic·Gold·SSOT·WP·앱/Hub 코드·환경·DB·서버/포트 수정 금지. 원본 대량 재출력·생성기 실행·모델/의료외부검색·네트워크·commit/push/PR/하위 워커 금지. 필요하면 ask한다. 기존 알려진 오류를 수정했다고 보고하지 않는다.

초기 엔터티/edge 목록과 조사 분모를 Orca status로 알리고 체크포인트마다 inbox를 처리한다. HTML 작성 전 조사표를 완성하고, 생성 후 검증한다. 완료 시 실제 검토 범위·설계 결론·미정/누락·검증 결과·index.html 경로를 포함하여 live preamble worker_done을 한 번 보고하고 멈춘다.
