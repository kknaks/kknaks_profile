# [researcher] 허브 부위 3단 배치안 + 명동점 진료항목 부위 대조 (검수용 · 읽기만)

## 배경(사용자 11-19 확정)
- 허브 부위를 **3단**으로 정리한다: **1단 = 얼굴 / 몸(전신)** → **2단 = 큰 부위**(얼굴: 이마 · 미간 · 관자놀이 · 눈 주변 · 코 · 볼 · 입 · 턱 · 귀 … / 몸: 목 · 어깨 · 팔 · 손 · 가슴 · 등 · 복부 · 엉덩이 · 다리 · 발 …) → **3단 = 상세 부위**(눈밑 · 코끝 · 입꼬리 · 승모근 · 하완 · 발가락 …).
- 진료항목 부위는 가장 구체적인 단에 매달고, 조회는 위 단 → 아래 단으로 같이 찾는다.
- 지금 허브는 89 중 68 이 최상위(1단 68 · 2단 16 · 3단 5) — 얼굴 부위(코 · 입술 · 턱 · 눈 …)도 얼굴 밑이 아니라 최상위에 흩어져 있다.
- 「바디」 · 「페이스」 = 메뉴 분류 말(몸 · 얼굴 묶음) · 「바디보톡스 승모근」 의 부위 = 승모근.
- 이번 일은 **배치안(검수용)** 까지. 허브 데이터 · 진료항목 CSV 수정 0 · 결정은 사용자.

## 입력(읽기만)
- 허브 부위: 로컬 PG `s_site`(code · name_ko · name_en · parent_code · 출처 칸) · 다른 이름(silver `alias.csv` / `g_entry`) — `set -a; . ~/.config/phub/medallion-pg.env; set +a` · 값 출력 금지 · SELECT 만. silver 원본: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/data/medallion/silver/site.csv` 등.
- 허브 해부 구조: `s_anatomy` · `s_anatomy_site`(예: ANA-064 승모근 = 부위 연결 0 · ANA-051 측두근 → 관자놀이 · ANA-070 비복근 → 종아리).
- 명동점 진료항목: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/reference/2026-11-19-myeongdong-kos/myeongdong-kos-medical-services-20261119.csv`(324 · `부위` · `부위 출처` 칸 + 진료항목명 · 시술명 원문).
- 원장 근거: `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/research-site-evidence.md` · 원장 `…/PROCEDURE-HUB/phub-consult-demo/data/medallion/bronze/phub-ledger/*.json`.

## 할 일
1. **허브 부위 89 전부를 3단에 배치** — 부위마다 1단 · 2단 · 3단 자리. 지금 parent 와 달라지면 「이동」. 빠짐 0.
2. **3단에 안 맞는 부위**(두피 · 머리 · 정수리 · 이개 · 구강 · 잇몸 · 비강 · 부비동 · 관절 · 사지 · 상체 · 체간 · 중안면 · 하안면 · 마리오네트라인 · 팔자주름 같은 주름선 등)는 억지로 넣지 말고 「3단 밖」 으로 모아 선택지(1단 후보 「머리」 / 「기타」 · 얼굴 2단 · 묶음 부위로 두기 등)만.
3. **명동점 진료항목 부위 원문 전부 대조** — 진료항목명 · 시술명에서 부위 낱말을 다시 읽어(지금 `부위` 칸의 「바디 + 승모근」 · 「다리 + 얼굴」 같은 잘못 자름은 고쳐 읽고, 고친 것은 목록으로) 각 낱말을 판정: ① 있음(그 허브 부위) · ② 다른 이름만 추가(넥 → 목 · 콧볼 → 비익 · 힙 → 엉덩이 · 애교 → 애교살 · 겨 → 겨드랑이 · 페이스 → 얼굴 …) · ③ 상세 부위 추가(하완 · 뒷목 · 승모근 · 발등 · 발가락 · 손가락 · 유륜 · 상복부 · 하복부 …) · ④ 새 부위(쇄골 · 부유방 · 헤어라인 · 하관 · 나비존 · 침샘 …) · ⑤ 부위 아님(바디 · 페이스 등 메뉴 분류 말 · 규격 · 기기 낱말).
4. **추가 부위(②③④)마다 원장 근거** — 있음(원장 · 키 경로 · 문맥 한 줄) / 없음 · 해부 구조(anatomy)에 이미 있으면 그 코드.

## 산출
- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/reference/2026-11-19-myeongdong-kos/hub-site-tree-draft.csv`(utf-8-sig) — 한 줄 = 부위 하나(허브 89 + 추가 후보). 칸: `1단 · 2단 · 3단 · 부위 이름 · 허브 코드(새 부위는 빈칸) · 지금 위 부위 · 이동 여부 · 다른 이름 추가 · 구분(기존 / 추가-다른이름 / 추가-상세 / 추가-새 / 3단 밖) · 원장 근거 · anatomy 코드 · 명동점 진료항목 수 · 메모`
- `/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo/research-site-tree.md` — 트리 그림(얼굴 · 몸) · 이동 목록 · 추가 목록(종류별 · 원장 근거 유무) · 3단 밖 목록과 선택지 · 명동점 부위 낱말 판정 수(①~⑤) · 잘못 자른 부위 고친 목록 · 정할 것 · 확인 안 됨.

## 하지 말 것
허브 · 진료항목 CSV · KOS 수정 0 · 커밋 0 · 서브에이전트 0 · 결정 금지(정할 것으로) · 가격 · KOS id 0.

## 검증
허브 89 빠짐 0(코드 대조) · 명동점 부위 원문 판정 빠짐 0 · 추가 후보마다 원장 근거 칸 채움(있음/없음) · `git status --short` 로 변경이 산출 2 개뿐.

## 완료 보고
앞과 같은 2채널(worker_done 인박스 + 코디 터미널 주입) · subject 「researcher 완료: 부위 3단 배치안」.
