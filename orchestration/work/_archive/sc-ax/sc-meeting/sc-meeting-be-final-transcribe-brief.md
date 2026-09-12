# [backend] 종료 시 2-pass — 저장된 음원 전체를 Soniox 비동기(stt-async-v5)로 재전사(화자 분리) → 원문 교체 → 합성 새로

너는 **sc-ax backend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. `backend/` 만. 커밋 금지. 서버 재기동 금지. **지금 하는 합성 재작성(task_bbed6fc04fba)·memo.line 큐 뒤에 이어서.**

## 사용자 결정(2026-09-11, D44) — task-management 원형 그대로
실시간 전사는 화자 분리가 부정확하다. **회의를 끝내면 저장된 음원 전체를 Soniox 비동기 API 로 다시 전사해 화자 분리·시각을 새로 받고, `meeting_transcripts` 를 그 결과로 갈아 끼운 뒤, 그 원문 + 메모 + AI 요약을 재료로 합성을 새로 만든다.** 코디가 앞서 §11.1 에 「2-pass 폐기」로 적은 것은 오독 — 되돌린다.

## 원형(읽기만)
- `/Users/kknaks/git/toy_pr2/task_management/app/back/integrations/soniox.py` — `FinalTranscriber` · `stt-async-v5` · 파일 업로드→transcription 생성→상태 폴링→결과(토큰·speaker·ms) 
- `/Users/kknaks/git/toy_pr2/task_management/app/back/service/meeting_finalize_service.py` — 종료 파이프라인에서 재전사가 서는 자리·실패 시 처리.

## 할 것
1. `platform/soniox.py` 에 비동기 파일 전사 어댑터(`SonioxFileTranscriber`: 업로드 → transcription(diarization on, ko hints) → 폴링(간격·상한 상수) → 토큰 → 확정 블록(화자 변경·300자·2초 같은 경계 규칙 재사용)). 원본이 webm/opus 면 그대로 업로드(Soniox 가 컨테이너 인식), pcm 이면 wav 헤더를 붙여 업로드. 키는 같은 env.
2. `finalize_service` 파이프라인: `/end` → 잡 → **①재전사** → 성공 시 `meeting_transcripts` 전량 교체(seq·speaker_label·at_ms·end_ms·text, evidence 기준점 유지) → **②합성**(재작성 규칙) → done. 재전사 실패(업로드·타임아웃·오류)면 **실시간 원문 그대로 두고 합성**하되 `meeting.transcript_source = "realtime"|"final"` 로 남기고 화면 안내 한 줄(사람 말). 진행 상태는 summarizing 하나 그대로(화면은 로딩).
3. 회의 원본이 없으면(녹음 파일 없음) 재전사 생략 → 실시간 원문으로.
4. 테스트: 대역 transcriber — 재전사 성공 시 원문 교체·합성 입력이 새 원문 · 실패 시 실시간 유지 + transcript_source · 파일 없음 생략. 실제 Soniox 호출은 코디.

## 검증
```
cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/contract/test_meeting_stream.py tests/architecture -m 'not integration'
```

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 종료 2-pass 재전사" \
  --body "변경 파일 / 어댑터·파이프라인 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 2-pass 재전사. 상세는 인박스." --enter
```
