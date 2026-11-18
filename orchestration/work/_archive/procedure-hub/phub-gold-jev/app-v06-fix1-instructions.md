# [app] 0.6 수정 1 — 코드 검수 WARN 3 → 바로 37 batch

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev)의 역할 · 공개 레포 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 워크트리 /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev. **디스크 여유 2~3GB.**

읽을 것: `review-code-v06-app.md` W-1 ~ W-3 · `_RESUME.md` §2 맨 위 행(**0.6 코드 검수 뒤 코디 결정 — 정본**).

## 1. 고칠 것(동결 3 파일 `evalset/answer_key.py` · `walk/calls.py` · `walk/keycodes.py` 는 건드리지 마라 — 건드리면 멈추고 `[질문]`)

- **W-1**: `walk/value_pick.py` — 미룬 상세 조회마다 **같은 node · 같은 부위 필터로 읽은 adverse 응답 행 가운데 yes 사건 행**의 위험 id 만 건다. T32 에 「대상 둘 · id 다름 → 대상마다 자기 id 만」.
- **W-2**: `prompts/col_b.md` 「value 의 이름은 전부」 → 「value 가운데 물은 것에 해당하는 이름은 전부」(공통 12 번과 같은 말 쪽으로).
- **W-3**: `prompts/common.md` 5 번 「두 대상의 비교」 → 「우열 판정 · 칸 없는 기준의 견줌」 으로 좁히고, 「차이를 물으면 두 대상을 각각 빠짐없이 말한다(우열은 말하지 않는다 — 8 번)」 한 줄.
- 프롬프트는 여전히 미확정(확인 표시 그대로). ruff · pytest.

## 2. 그다음 바로 37 batch(코디 승인됨)

- `batch --check`(답 키 confirmed 37/37 이어야 — 동결 파일 그대로면 이어진다. 아니면 멈추고 `[질문]`)
- `batch --label v06-37 --columns a,b,c --no-b-on` → `quality.grade --batch` → `report --batch`(허브 18105 · 18220 은 코디 것).
- 요약 `batch-v06-summary.md`(같은 폴더) — `batch-v052-summary.md` 와 **같은 꼴 + 0.5.2 대비 열(B 의 전 → 후)**: 열별 표 · B 가 C 보다 못한 문항 · 0.5.2 에서 B 가 진 13 문항이 이번에 어떻게 됐나 · 원인 넷 각각 닫혔나 · `answer_check`(값 / 층) · KD9/KD10/BR6/VP 로 넓힌 문항의 asked_only. **회사 데이터 본문 0(id · 수 · 판정만).**
