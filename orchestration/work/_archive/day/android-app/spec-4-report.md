# planner 4회차 리포트 — review-doc-3 W-1~W-3 · R-1 반영 (2026-11-13)

워크트리 `android-app-spec` · 3회차 미커밋 위에 이어서 · `products/day/` 만 · 커밋 · Delivery 없음.

## 변경 파일:줄

| 항목 | 파일:줄 | 바뀐 것 |
|---|---|---|
| W-1 | `40-architecture/mobile-deployment.md:107` | §3 표 dev Android 칸 「로컬 실행용 · Google 쪽 등록 없음」 → 「로컬 실행 · Play 내부 테스트(2026-11-13 · §7-0) — Play 에 이 패키지로 올리면 바꿀 수 없음(위 문단 :103)」 |
| W-1 재grep | `mobile-deployment.md:110` | 같은 류 낡은 줄 1개 더 — 「정식 앱 Android id 와 Google 쪽 계정은 아직 [미결]」 → id 만 [미결] · 계정은 「조직 Play Console 권한 있음(2026-11-13 · M-3)」 |
| W-1 재grep | `mobile-deployment.md:20` · `:191` | 그대로 — :20 은 2026-11-12 ② 개정 노트(이력 · ③ 이 덮음) · :191 은 이미 취소선 |
| W-2 | `mobile-deployment.md:256` | §7-3-2 2 와 3 사이 「(코드 작업) 업로드 키로 서명한 release AAB 를 만들어 넘긴다 — §7-0 · Delivery」 |
| W-2 | `mobile-deployment.md:259` | 5 끝 「참여 링크는 게시 뒤 열리기까지 몇 시간 걸릴 수 있다(answer/9845334)」 |
| W-3 | `20-spec/spec-003-mobile-app.md:576` | 「로컬 빌드와 Play 빌드는 서명이 달라 한 기기에 함께 깔 수 없다 — 바꿀 때 지우고 깐다(세션도 지워져 다시 로그인)」 |
| W-3 | `spec-003-mobile-app.md:923` A-49 확인 칸 | 「에뮬레이터면 Google Play 시스템 이미지 + 테스터 목록의 Google 계정으로 Play 로그인 · 같은 기기의 로컬 빌드는 먼저 지움」 — 실기기 / 에뮬레이터 중 무엇으로 볼지는 정하지 않음(사용자 판단 대기) |
| R-1 | `mobile-deployment.md:245` · `:410` | 「기본으로 Play 앱 서명에 등록」 → 「Google 생성 키로 자동 등록(문서 현행 이름 「quantum-ready, hybrid signing with Google-generated keys」)」 — 뜻(앱 서명 키 = Google · 업로드 키 = 개발자) 그대로 |

새 화면 문구 0 · 값 0 · [미결] → [확정] 0. log.md 는 3회차 2026-11-13 행 범위 안이라 새 행 안 넣음.

## lint

`python3 scripts/lint-pipeline.py --strict` → exit 0 · `0 error, 263 warning` · products/day 줄 0.
