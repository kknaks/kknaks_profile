# [코디] BE-2 · BE-3 파일 조정 1 — 저장소 겹침 (BE-1 검수 W-6, 2026-10-06)

BE-1 의 `backend/src/ax_workspace/platform/external_channels.py`(저장소) 는 **이제 얼린다 — BE-2·BE-3 둘 다 이 파일을 고치지 마라.**
- 이미 있는 함수(메시지 upsert 등)는 **불러 쓰기만** 한다
- 새 저장 함수가 필요하면 **각자 새 파일**에:
  - BE-2 → `platform/external_channels_sync_store.py` (슬랙·Gmail 수집 쓰기 · 백필 진행률 · 동기화 상태)
  - BE-3 → `platform/external_channels_inbox_store.py` (메시지함 조회·읽음·보낸 답장 · 카톡 수신 쓰기 · 프로필 이미지)
- 이미 그 파일을 고쳤다면 **지금 되돌리고** 위 파일로 옮겨라. 보고에 「옮긴 것」을 적어라
- 참고(BE-3): 카톡 첨부 업로드는 `aid` 만으로 찾지 말고 연동 범위와 함께(검수 지적)
- 참고: local-stack 은 이제 `sync-demo-schema` 가 필요하다
