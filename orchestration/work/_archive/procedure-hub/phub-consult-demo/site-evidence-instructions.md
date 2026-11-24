# [researcher] 남은 부위 낱말 26 줄 — 원장 근거 확인 (허브 보강 판단 전)

앞 판(`research-kos-map.md` · CSV 2판)에 이어서. 읽기만 · 결정 금지 · 서브에이전트 0 · 커밋 0.

## 배경
KOS 시술 이름을 나누고 남은 글자가 허브 사전에 없는 줄이 26 이다(CSV `note` 의 「남은 글자 …」). 코디 1차 분류(사용자에게 보고함 · 검증해라):
- ① 허브에 이미 있는 부위의 다른 이름: 힙 → 엉덩이 SITE-109 · 뒷목 → 목 SITE-079 · 풀페이스 · 페이스 → 얼굴 SITE-007 · 아이 → 눈 주변 SITE-019 · 상완 · 하완 → 팔 SITE-100(팔뚝 SITE-101) · 근(측두근) → 관자놀이 SITE-016
- ② 허브에 없는 부위: 쇄골 · 침샘 · 부유방 · 콧볼 · 손가락 · 발가락
- ③ 부위 아님: 120 · 365 · 티타늄 · hero · 더마 · 소노 · 재생 · 관리 · 레나룻(배레나룻) · 필녹주(필러 제거 = 히알루로니다제 → 다른 시술)

**원칙(사용자 10-30 · 11-10)**: 허브는 원장(의사 자료) 기반이고 병원(명동점) 데이터로 바뀌지 않는다. 그래서 ② 를 허브에 넣으려면 **원장 근거**가 있어야 한다.

## 원천
- 원장(브론즈): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/data/medallion/bronze/phub-ledger/*.json`(21 원장 · README · CHANGELOG)
- silver/gold: 같은 레포 `data/medallion/silver/` · `gold/`(특히 site.csv · g_entry.csv) · 로컬 PG(SELECT · 접속 값 출력 금지)
- KOS: `reference/2026-11-19-myeongdong-kos/myeongdong-kos-products-20261119-v2.json`(상품 · 옵션 · 시술 항목 이름 · 설명 — 그 낱말이 무엇을 뜻하는지 판단 근거)

## 할 일 — 26 줄의 남은 낱말마다
1. **원장에 나오나** — 낱말 + 흔한 다른 표기(예: 쇄골 · 쇄골라인 · clavicle / 침샘 · 이하선 · 악하선 · parotid · salivary / 부유방 · accessory breast / 콧볼 · 비익 · alar / 상완 · upper arm / 하완 · forearm / 손가락 · 발가락 · 힙 · 둔부 · 엉덩이 · 뒷목 · 후경부)로 21 원장 전수 grep. 나오면 원장 · 키 경로 · 문맥 한 줄(어떤 시술 · 적응 · 부위 맥락) · 수.
2. **silver/gold 에 있나** — site 표 이름 · 다른 이름 · g_entry 에 있는지. 있으면 코드. 원장에 있는데 silver 로 안 옮겨졌으면 그렇다고(어느 단계에서 빠졌는지 알면).
3. **KOS 쪽 뜻** — 그 낱말이 KOS 상품 · 옵션 · 시술 항목 이름 · 설명에서 무엇을 가리키는지(부위 / 기기 규격 · 팁 / 제품 용량 / 그 밖). ③ 분류가 맞는지 검증.
4. **줄마다 판정 근거 표** — KOS 줄 · 남은 낱말 · 원장 근거(있음 n · 없음) · silver/gold(있음 코드 · 없음) · KOS 뜻 · 코디 1차 분류(①②③)가 맞나(맞음 / 틀림 + 이유) · 선택지(허브 기존 부위로 · 허브 보강 후보(원장 근거 있음) · 허브 보강 불가(원장 근거 없음) · 부위 아님). **추천은 쓰지 마라 — 사실과 선택지만.**

## 산출
`orchestration/work/phub-consult-demo/research-site-evidence.md` — 머리에 한눈 표(①②③ 별 수 · 원장 근거 있는 ② 의 수) → 줄마다 표 → 확인 안 됨. 회사 원장 본문을 길게 옮기지 마라(문맥 한 줄 · 80 자 안).

## 검증
26 줄 전부 다룸 · 근거마다 파일 · 키 경로 · `git status --short` 로 변경이 리포트 1 개뿐.

## 완료 보고
앞과 같은 2채널(worker_done 인박스 + 코디 터미널 주입) · subject 「researcher 완료: 부위 낱말 원장 근거」.
