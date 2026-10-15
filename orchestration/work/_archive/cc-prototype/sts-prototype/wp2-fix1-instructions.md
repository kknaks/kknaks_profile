# [backend] WP2 fix1 — 중국어 · 일본어 · 태국어 문장 속 빈칸 제거

`wp2-be-report.md` 이슈 1. Soniox 토큰을 이어 붙일 때 「治療前 我會先塗」처럼 빈칸이 생긴다.

- 자막(`caption.original` · `caption.translation`)과 **TTS 로 보내는 텍스트** 모두: 원문/번역 언어가 `zh` · `ja` · `th` 이면, **양옆이 CJK 문자 · 가나 · 태국 문자 · 전각 구두점인 빈칸만** 지운다(영문 · 숫자 사이 빈칸은 둔다. 예: 「打 20 分钟」의 숫자 앞뒤 빈칸은 유지해도 됨)
- 번체 변환 전후 어디서 하든 결과가 같게
- 단위 시험 몇 개 추가 · `uv run pytest` · `uv run ruff check .` 1회
- 리포트: `wp2-be-report.md` 끝에 「fix1」 절 추가
- 완료 보고는 WP2 브리프 §5 두 명령 그대로(subject 「backend 완료: WP2 fix1 …」, taskId/dispatchId 는 WP2 것)
