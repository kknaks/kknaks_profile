# [app] C 측정 보정 — 「첫 답 글자」 · 도구 사이 메모 섞임 막기

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-app-brief.md`(같은 폴더)의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev`(미커밋 위에 이어서).

사실(코디 실측 · run f0060a0fff0d): C 「팔자주름에 뭐 해?」 의 첫 글자 3.3s 는 도구 사이에 Sonnet 이 쓴 영어 메모 「Two readings: concern and site. Query concern.」 였고 **답 본문에도 그대로 섞였다**. 진짜 답은 마지막 도구 호출 뒤에 시작.

할 것:
- CLI stream-json 에서 **도구 호출 앞뒤 텍스트를 가른다** — 마지막 `tool_use` 뒤의 텍스트만 답(`answer`) · 그 앞 텍스트는 `trace.interim_text[]` 로 따로(답 · 채점 입력에 안 들어감). A 열(원장 도구)도 같은 꼴이면 같이.
- 시간: 열마다 `first_answer_text_ms`(열 시작 기준) · `click_to_first_answer_ms`(화면 요청 기준) 추가. 기존 `ttft_ms` · `click_to_first_text_ms` 는 「첫 글자(메모 포함)」 로 남겨 둔다. **화면 카드 맨 앞 큰 값 = `click_to_first_answer_ms`** 로 바꾸고, 속도 표 첫 칸도 그 값. B 계열은 도구가 없으니 두 값이 같다.
- 스트리밍: 화면에는 메모를 답 칸에 흘리지 말 것 — 도구 호출이 끝나기 전 텍스트는 카드의 작은 「메모」 줄(옛 화면 · WORK 의 말이 없으면 표지만)로, 답 칸은 마지막 도구 뒤부터. 마지막 도구인지 미리 모르면: 도구 호출이 오면 그때까지 답 칸에 흐른 글을 메모로 옮긴다(끝난 뒤 기록 답으로 갈아 끼우는 M-2 와 일치).
- 시험(모의 stream-json: 메모 → tool_use → 답 / 메모 없음 / 도구 여러 번) · ruff · pytest · grep.
- 실물: 화면 API(18221 띄웠다 내림 · effort low · 동시) 로 「팔자주름에 뭐 해?」 B 선별 · C 1회 → 두 시간 값 · 답 앞머리 보고. 18220 · 18105 는 코디 것.
