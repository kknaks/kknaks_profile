# 지시서 — silver 통합 검사 걸린 것 고치기 + 정의 없는 칸 29 뜻 초안

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

silver 47표 통합 검사(`drafts/silver-check/silver-check.py`)가 FAIL 8 · WARN 401 을 냈다(`drafts/silver-check/silver-check-notes.md` §3). 참조 · 원문 · 숫자 대조는 모두 통과했고, 걸린 것은 형식 · 근거 표시 · 별칭 정리다. 이번 일: 사용자가 고른 대로 고치고, 검사를 PASS 로 만든다.

## 2. 읽을 것

- `drafts/silver-check/` 전부(notes §3 걸린 것 · §4 알려진 빈칸 · §5 정의 없음 · `check-stats.json` warn 행 목록 · `silver-schema.json` · `silver-check.py`)
- `notes/silver-erd.md` · `notes/silver-tables.md`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)
- 칸 뜻을 찾을 곳: `drafts/relation-pilot/relation-notes.md` §9-2 · `drafts/relation-*/` notes · build 스크립트 · `../relation-*-brief.md` · `notes/product-*-notes.md` · `notes/split-notes.md`

## 3. 사용자 결정 (11-15 「응」 — notes §3 추천 그대로)

**A. FAIL 8 — 전부 (a)**
1. modality M12 name_ko 「마이크로니들링」 · alias 「MTS」(kind 약어 — 기존 alias kind 값 중 맞는 것) 덧붙임 · 근거는 기존 M12 근거 포인터.
2. ADV-186 source_ref 덧붙임(adverse · ADV-186 · name_en · notes 에 적힌 포인터).
3~7. ADV-184~188 각 행 field 빈칸 근거 한 행씩(그 행 description 근거 포인터).
8. ADV-188 description 에서 「(ADV-119)」 를 빼고 「실 이동」 만. 「」 인용 원장 글자는 그대로.

**B. WARN — 추천대로**
- **고침**: A2 이름과 같은 별칭 13 지움 · A7 띄어쓰기만 다른 별칭 22~23 지움(notes 목록 전부 — 「method 별칭 띄어쓰기 8」 포함) · A3 ANA-049 의 「비근근」 별칭 지움 · Q1 설명 인용 8 — 원장 글자가 아닌 「」 를 떼어 서술로(글은 그대로, 인용 표시만) · S2 MET-100 같은 근거 행 하나 지움.
- **그대로 + 알려진 빈칸 기록**: D5 product_modality 근거 300(근거 = product 행 근거) · A6 조직 별칭 괄호 38 · A5 별칭 근거 글자 13 · C9 케이스 설명 4. `silver-check.py` 는 이것들을 WARN 에서 「알려진 예외」 셈으로 옮긴다(목록을 스크립트 · notes 에 고정 — 새로 생기면 다시 WARN).
- 지운 alias · source_ref 행은 목록을 notes 에(표 · 행 · 값 · 이유).

**C. 정의 없는 칸 29 — 뜻 초안**: 칸마다 silver 에 실제 들어 있는 값(서로 다른 값 · 빈도 · 예 3)과 그 칸을 만든 build 스크립트 · notes 의 쓰임을 보고 뜻 한 줄 초안을 쓴다. 근거(어디서 알았나)를 같이. 값이 섞여 뜻을 하나로 못 쓰면 「뜻 갈림」 으로 적고 값별 예. **silver 값은 고치지 않는다.** `notes/silver-tables.md` 에는 「(초안)」 표시로 넣고, 사용자 확인 목록을 notes 에.

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · `notes/silver-tables.md` · `drafts/silver-check/` 를 `archive/silver-before-fix/` 에 복사.
- silver 변경은 §3 A · B 의 고침만(행 덧붙임 · 칸 값 바꿈 · 행 지움 — 목록과 같아야 함). 그 밖 바이트 불변. alias · source_ref 는 지우는 행 말고 앞쪽 행 바이트 그대로.
- 스크립트 · notes: `drafts/silver-fix/`(`silver-fix-build.py` · `silver-fix-notes.md`) · `drafts/silver-check/silver-check.py` 갱신(기존 기준 유지 + 알려진 예외 셈). CSV UTF-8 BOM · `;` 금지. 원장 변경 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → **PASS**(FAIL 0 · 남은 WARN 은 0 이거나 notes 목록과 같음).
- `silver-fix-build.py` 의 변경 목록(바뀐 칸 · 덧붙인 행 · 지운 행) = 실제 silver diff(archive 대비).
- 음성 시험 다시(`--negative`).
- `notes/silver-erd.md` · `silver-tables.md` 의 FK · 행 수 = 고친 뒤 silver.
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`drafts/silver-fix/silver-fix-notes.md`, 짧게)

1. 고친 것 표(FAIL 8 · WARN 고침 — 표 · 행 · 전 → 후) 2. 지운 행 목록 3. 알려진 예외 셈 4. 칸 29 뜻 초안 표(칸 · 뜻 · 값 예 · 근거 · 갈림 여부) 5. 사용자 판단이 필요한 것(새로 나온 것만) 6. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(새 판정 · 사전 행 추가 · 빈칸 채우기 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/silver-fix/silver-fix-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "silver 고치기 완료: drafts/silver-fix/silver-fix-notes.md" --enter`
