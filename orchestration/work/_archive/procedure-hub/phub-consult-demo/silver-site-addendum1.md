# [silver] 추가 지시 1 (코디 · 검수 r3 반영)

1. **별칭 「애교 → 애교살」 은 넣지 마라** — 이미 있다(`alias.csv:308`) → 넣으면 A1 중복 FAIL. 「팔 상완」 · 「하관」 은 배치안 글자 「상완」 · 「하관전체」 로.
2. **검사 · 빌드 스크립트는 작업 사본(`silver-model/gold/*.py`)에 한해 아래만 고쳐도 된다**(원본은 금지 · 고친 줄은 리포트에 diff 로):
   - `silver-check.py:30-37` 원장 · step1 경로가 낡음(`orchestration/work/phub-recommend/…` → 지금은 `orchestration/work/_archive/procedure-hub/phub-recommend/…`) — 이 워크트리에서 실제로 있는 경로로. `gold-check.py` G1 산출물 경로(`:426-430`)도 같은 이유면 같은 방식으로.
   - 근거 종류 식 세 곳(`gold-build.py:50-57` · `gold-check.py:173-178` · `silver-check.py:128-134`) + `resolve`: ref 머리 `drafts/clinic-supplement/` 를 **「사용자 제공」** 으로(원장으로 분류되면 안 됨 · 앱에 「원장」 표지로 실림). 순서 목록에 새 값을 만들지 말고 기존 「사용자 제공」 을 쓴다.
   - D3(`silver-check.py:543-550` · anatomy 와 같은 이름 금지): `anatomy_site` 로 이어진 같은 이름 짝(침샘 · 쇄골 · 승모근)은 허용하도록.
   그 밖의 검사 실패는 고치지 말고 멈춰서 질문.
3. 새 부위 넷의 자리(3단 조사 결과대로): 침샘 → 얼굴 > 턱 · 나비존 → 얼굴 > 볼 · 부유방 → 몸 > 가슴 · 쇄골 → 몸 > 목. 사지 · 상체 · 체간 · 코안면은 description 에 「묶음 부위(3단 조사 처리)」.
