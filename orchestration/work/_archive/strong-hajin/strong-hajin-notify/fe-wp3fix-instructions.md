# [frontend] WP3 검수 손질 — FAIL 2 · WARN 2 · 코디 결정

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/review-wp2-wp3-report.md` §FAIL · §6 WARN. (WP4-SHELL 은 cargo 98/77 · vitest 30 코디 관문 통과 — 검수는 이 손질 뒤 함께)

- **F-2**: `lib/labels.ts` `meeting.changed` — `before`/`after` 를 서버 모양 `{starts_at, ends_at, place}` 객체로 읽는다(시간이 바뀌면 「회의 시간을 바꿨습니다」 + 「HH:MM → HH:MM」 · 장소만이면 「회의 장소를 바꿨습니다」 · 둘 다면 시간 문장 + 보조 줄에 장소) · `notificationLabels.test.ts` 대역을 서버 모양으로 · **OS 알림 문장도 같은 함수라 함께 바뀐다**
- **F-3**: `App.test.tsx:2628` — 처리 안 된 예외 없애기 · `npx vitest run src/App.test.tsx` **exit 0**
- **W-1(화면)**: 합친 슬랙 줄 「외 N명」 은 `sender_count` 가 있으면 그것으로(backend 가 지금 올리는 중)
- **W-5**: `App.tsx:386-432` `openFocus` 의존에 `changeSurface`(또는 ref)
- **코디 결정 W-6**: 사이드바 머리 `titleEnd` 슬롯 — **받아들인다**(SPEC-011 §2.1 이 머리에 「안 읽음 N」 을 정했다) · 그대로 둔다
- **코디 결정(앞서)**: 외부 발신자(메일·슬랙·카톡) 이름에는 「님」 을 붙이지 않는다 · 회원만 「이름님」 — 지금 구현 그대로인지 확인만
- 검증 관련만(고른 vitest · tsc · 셸 손댔으면 cargo 두 벌) · 금지는 앞 브리프 그대로 · ⚠ backend 워커가 `backend/` 손질 중
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-wp3fix-report.md` · 완료 보고 앞 브리프 §7 두 명령 — subject 「frontend 완료: WP3 손질」 · text 「[worker_done] frontend WP3 손질 완료 — <한 줄>. 리포트 fe-wp3fix-report.md」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
