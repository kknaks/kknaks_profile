# SPEC-006 0.1 — 상담 채팅 0.3: 턴 종류 · 상담 말투 · 리스트 · 얼굴 점

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · 제약 · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-006-consult-v03.md` 새 파일 1개만.** SPEC-004 · 005 는 고치지 않는다(그 위에 얹는 것 표로). Procedure Hub 데이터 · medikit 은 공개. 외부 API · CLI 호출 금지.

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 앱 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(읽기만 · 0.1 + 수정 1 + 0.2 구현) · 장부 `$A/runs/consult/turns.jsonl`(사용자 실물 대화: conv `e3f90bfd3278476e` · `5c0d670e7bf44ac1` · 코디 `805816632b934c78`)

## 읽을 것

1. `$W/_RESUME.md` §1 「수정 2 목록」 전부 · §2 11-17 맨 위 행들(얼굴 점 · 메뉴는 시술 아님 · 시술로 내려가기 · 0.2 B 답 · U5) ← 정본
2. `$W/SPEC-004-consult-chat.md` · `$W/SPEC-005-consult-state.md` · `$W/review-code-chat-v02.md`(WARN 2) · 앱 `prompts/consult.json` · `consult/` 코드
3. 허브 쪽 변경은 **같은 시각 다른 워커가 SPEC-001 0.7 로 쓴다**(H1 시술로 내려가기 · H2 `concern_candidates` 에 고민 부위 코드 · H3 이름 맞춤) — 이 문서는 그 응답을 받는다고 두고, 칸 이름은 「SPEC-001 0.7 을 따름」 으로.

## 정해진 것(다시 묻지 마라)

- **A1 턴 종류 먼저 가르기**: 새 정보 → 검색 · 앞 답 이어 묻기 → 앞 대상으로 검색 · **되물음 · 불만(「왜 못 채워」 · 「아니 그게 아니라」) → 검색 없이 앞 대화로 답**(CLI `--resume` 기억 사용). 가르는 주체 · 꼴(Jev Noul 등) · 실패 때.
- **A2 상담 프롬프트 다시**: 해요체 상담사 · 「원장 진술」 · 「윗층」 · 「경유」 · 「행」 · 「○○로 읽었어요」 같은 출처 · 층 · 내부 말은 화면 답에서 빼고 기록에만 · 지어내지 않음 · 우열 판정 안 함 · 안전은 물을 때만(U5-4 (a1) 표지 예외 그대로) — prompts/consult.json 절 꼴(문구는 초안 · 사용자 확인).
- **A3** 객체가 고른 다음 질문(ask)을 답 끝에 반드시.
- **A4** 데이터 없음은 없다고(「같이 받는 조합 정보는 없어요」) + 같은 고민의 다른 계열로 이어 감 · 「확인 못 했어요 · n 행 더 볼까요」 꼴 금지.
- **A5 리스트**: 내부 층 이름 빼고 계열 → 시술 · **메뉴(V라인주사 등)는 시술로 띄우지 않음** · H1 로 내려온 시술은 묶음 머리에 계열 표시.
- **A6 얼굴 점**: 대화에서 나온 고민들의 부위에 점이 쌓임 · **점(고민 부위)을 누르면 그 고민의 시술 리스트** — SPEC-005 SC5(focus 고민만) · RV5(리스트 · 점 = focus) 를 이렇게 바꿈.
- **A7** 0.2 코드 검수 WARN 2(guess 반복 → confirmed 구멍 · 옛 대화 탭 off) 처리.
- LLM = CLI(Sonnet · resume) · 화면 htmx 그대로 · 얼굴 SVG · face_coords 는 고치지 않음.

## 할 것

A1~A7 각각 규칙 · 이벤트/조각 · 장부 칸 · 시험 · 실물 확인(사용자 실물 대화 세 개를 다시 돌려 무엇이 달라져야 하는지 턴별 기대표) · SPEC-004/005 위에 얹는 것 표 · 열린 것 · **WORK 전 사용자 결정**(최소 · 추천).

## 검증

결정 행 → 문서:줄 · 장부 인용(conv · 턴) · 공개 grep.
