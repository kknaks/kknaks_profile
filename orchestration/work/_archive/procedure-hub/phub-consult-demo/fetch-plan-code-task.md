# [code] SPEC-011 0.1.2 구현 — WP-1 ~ WP-4 + 호출마다 토큰 기록 (사용자 승인 11-23 「응」)

너는 앱 코드 워커다. 앞 맥락 없음 — 이 문서와 가리킨 파일만으로. 앱 워크트리 `A=/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` 에서만 코드 수정 · **커밋 0** · 서브에이전트 0 · **18222 · 18105 손대지 마라**(실물은 빈 포트에 따로 띄우고 끝나면 끈다 · 허브 18105 GET 만) · 키 · 토큰 값 출력 0 · 시험은 WP 관련만(전체 pytest 는 마지막 한 번).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/상담봇/orchestration/work/phub-consult-demo` · 정본 **`$W/SPEC-011-fetch-plan.md` 0.1.2**(PASS · `$W/review-spec-011-r3.md` 의 P2-14 · P2-15 는 재생 셈에 반영) · 측정 스크립트 `$W/fetch-plan/` · 원인 조사 `$W/token-cause-report.md` · 18222 기동 env(같은 값으로 빈 포트): `CHAT_STATE=on CHAT_KOS_MAP=data/kos/myeongdong-mapping-20261120-v3.json CHAT_KOS_MAP_SHA=d21903f5 CHAT_IMAGE_DIR=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images uv run python -m clinic_chat.consult --port <빈 포트>`

## 사용자 결정(다시 묻지 마라)
- 스펙 UD1 ~ UD5 그대로(1차 JSON → 2차 결정론 → 3차 · Jev 거르기 없음 · `--resume` 둠 · 출력 안 줄임 · 상한 고정 없음 · 안전 · 명시 늘).
- **DQ1 = 예**: 범위 기본 = 명동점 진료항목에 닿는 것은 상세까지 · 밖은 이름만 · 손님이 명동점 밖을 말하거나 물을 때만 `all`.
- **(새) 호출마다 토큰 기록**: 상담 경로의 **모든 LLM 호출**(1차 이해 · 3차 답 · 그 밖에 상담 턴 중 부르는 것 전부 — grep 으로 세어 목록을 리포트에) 마다 `input_tokens` · `output_tokens` · `cache_creation_input_tokens` · `cache_read_input_tokens`(+ 있으면 thinking 토큰) · `model` · `ms` 를 받아 장부 `turns.jsonl` 에 남긴다.
  - 꼴: 턴 줄에 `tokens.calls[]`(호출마다 `{role: understand | answer | …, model, ms, input, output, cache_creation, cache_read}`) + `tokens.sum`(턴 합 · 네 칸). 기존 `tokens` 칸을 쓰는 곳(`speed.py` · `report.py` · `token-cause` · `fetch-plan` 스크립트)이 안 깨지게 — 옛 칸은 두거나 읽는 쪽을 같이 고친다(grep 전수).
  - CLI 가 왕복을 여러 번 하면 왕복마다(`llm/cli.py:131` usage) 합쳐서 · 값이 없으면 null(지어 넣지 않음).
  - 지금 버리는 이해 호출 `cache_creation`(스펙 LG4 · `understand.py:257-262`)도 여기로.

## 할 일
1. 스펙 §8 **WP-1 → WP-2 → WP-3 → WP-4** 순서. 자리 · 완료 조건 · 관련 시험은 스펙 표 그대로. 호출마다 토큰 기록은 WP-4 에 넣는다(LG4 는 WP-1).
2. WP-2 완료 ①②: 표본 43 · 지금 시대 밖 11(시대 판정 = `kinds_by` + `consult.understand` 기록 유무 · 검수 P2-15) · **실물 3 대화 재생으로 만든 11-23 이후 새 장부 턴** — 빠짐 0 · 감소 · 상세 잃음 ≤ 7.
3. **실물 재생**: 빈 포트에서 3 대화를 실제 이해 · 답 호출로 다시 돌린다 — 03b8(「팔자주름에 대해서 고민이돼」 → 「미간에 주름도 고민이야」 → 「얼굴에 탄력이 좀 떨어지는거 같은데」 → 「그중에서 소프웨이브, 써마지, 울쎄라만 관심이 잇어」 → 「고주파 원리가 머야 ?」 → 「응 고주파에 대해서 전반적으로 설명해줘」) · ecc6(「요즘 피부 탄력이 저하 되서 고민이야」 → 「얼굴에」 → 「얼굴에」) · 73bd(「얼굴에 피부 탄력이 없어져서 걱정이야」 → 「아 주름이 눈가 입꼬리에 잇어」 → 「아 눈가는 볼뉴머 이ㅃ고리는 필러를 맞고 싶어」 → 「입꼬리에는 필러를 맞고 싶다니까」). 턴마다 **전 → 후 토큰(calls 별 네 칸)** · 「## 자료」 크기 · 답 앞 2 줄 · 빠짐 · 「정보 없어요」 문장 0 · 이름만 줄에 지어낸 상세 0.
4. 화면(주제 · 점 · 목록 · 모달 · 스피너)이 깨지지 않았나 — 재생 마지막 화면 스크린숏(새 브라우저 프로필) `$W/e2e-shots/fetchplan-*.png`.

## 산출
`$W/fetch-plan-code-report.md`: WP 별 바뀐 파일:줄 · 완료 조건 표(수치) · 실물 3 대화 전 → 후 토큰 표(호출별) · LLM 호출 목록 · 시험 결과(관련 · 마지막 전체 한 번) · 남은 것.

## 완료 보고 — 2채널(둘 다)
```bash
orca orchestration send --to term_b48041d1-a8c0-4931-af01-55bd6b304541 --from term_40a05ce4-b775-47d6-96eb-5661d257d0ee --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "app 완료: SPEC-011 WP-1~4" --body "감소 % · 빠짐 / 실물 3 대화 입력 전 → 후 / 시험 수"
orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[worker_done] SPEC-011 구현 완료 — <한 줄>. 상세는 인박스." --enter
```
질문: `orca terminal send --terminal term_b48041d1-a8c0-4931-af01-55bd6b304541 --text "[질문] fetch-code: <질문>" --enter`
