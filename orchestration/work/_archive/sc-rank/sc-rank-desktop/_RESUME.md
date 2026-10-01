
# 재개 노트 — sc-rank-desktop (sc-rank)

**지금**: sc-rank#1 스쿼시 머지(main 4c6d570). profile#64 OPEN. 사용자 Windows 설치·실행(A-9) 대기
**다음**: A-9·링크(A-6) 결과 → sc-rank#1 · profile#64 머지 → (선택) v0.1.0 태그 Release → archive-work.sh sc-rank sc-rank-desktop

세팅: `scripts/new-work.sh sc-rank sc-rank-desktop` · 설정 SSOT `config/projects/sc-rank.json`
코디handle: `term_4d2a12b8-e3cf-45de-a097-daa193cfd908`

## 워크트리

- 코디(문서): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-prototype` (브랜치 `kknaksss/sc-prototype`)
- 코드(옛, P1~P5): `/Users/kknaks/orca/workspaces/kknaks_profile/sc-rank-desktop` — PR #65 닫음
- 코드(현): `/Users/kknaks/orca/workspaces/sc-rank/sc-rank-desktop` (레포 kknaksss/sc-rank, 브랜치 `kknaksss/sc-rank-desktop`)


## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] 코드 검수 WARN 6 → W-1·2·4 수정(test 39 · ring) · W-5·6 SPEC §7
- [x] P6 레포 분리 정리(fresh clone test 39) — desktop(새 워커) `term_7546f553-e9fa-47fb-b58b-1d35fecc8522` task `task_b7ff9e832534` ctx `ctx_ced08cc61a91` (디스패치 주입이 신뢰 창에 먹혀 포인터로 재주입. 고아 task `task_7ecdd98b6d5f`)
- [x] sc-rank#1 스쿼시 머지 4c6d570
- [ ] profile#64 머지
- [!] 사용자 pending: 링크 OS 브라우저 열림 여부(A-6) · Windows 빌드·설치(A-9) · CI 여부 질문 답 없음
- [!] 워커 보고: macOS 「Orca 가 다른 앱 데이터 접근」 권한 대화상자가 떠 있음 — 사용자 결정 → reviewer(code) → 코디 실측(A-4·A-8) → 코드 PR
- [!] ⚠ env `ORCA_TERMINAL_HANDLE`(term_f871…)은 stale. 코디 = `term_4d2a12b8-e3cf-45de-a097-daa193cfd908`(10-01 재연결 후). orca 명령 앞에 export 로 덮는다
- [!] 사용자 게이트: A-6 화면 E2E · A-9 Windows 설치·실행

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-30 | Tauri + Rust · 서버 없음 · 운영 Windows · 코드는 PoC 아래 `desktop/` · 범위 블로그+플레이스 | 사용자 대화 → DEC-001 |
| 2026-09-30 | 미결 다섯 기본값(NSIS·무서명·Windows PC 빌드·Edge→Chrome·화면 재사용) | 사용자 「쭈욱 진행해」 → DEC-001 D-09~14 |
| 2026-09-30 | P2 워커 이슈 1~6 수용: 플레이스 rows 의 id·reviews·addr null · WebP 목표 2번째 해시는 재인코딩 없이(손실 WebP 인코더 없음, 판정 기준 동일) · null 인자 기본값 · 엑셀 미세 차이 · map_concurrent limit≥1 · 창 1400×900·자리표시 아이콘·로그 파일 1개 | 실사용 영향 없음 · 판정 기준 불변 |
| 2026-09-30 | Mac 에 Edge 154 설치(brew). 플레이스 광고 0건은 같은 시각 PoC 대조로 네이버 편성 차이로 판정 — 앱=PoC 완전 일치 | 사용자 「엣지로 설치하고 테스트」 · 코디 실측 |
| 2026-10-01 | 코드 레포 분리 kknaksss/sc-rank(비공개, subtree split) · PR #65 닫음 · DEC D-07 개정 · SPEC v0.2.2 · WORK P6 | 사용자 「kknaksss 에 레포 만들어서 코드 옮기자」 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| reviewer_doc | `term_f5bb51be-d024-4dcb-8ba9-1946a0f5eae9` | `task_663c45c4545b` | `ctx_a8a1d77029f6` | `sc-rank-desktop-review-doc-brief.md` | 완료(2회차 WARN, 정정함) |
| desktop | `term_95308b9e-d8ad-46e1-ae6b-f40a81d9ae20` | `task_28095b32a2ff` | `ctx_15f19e05e681` | `sc-rank-desktop-desktop-brief.md` (P1+P2) · 핸들 재연결 후 `term_5065cf30-3784-4dae-bfa5-2e4934c0468e` → `…-desktop-p3-brief.md` task `task_71fbb631c14d` → `…-desktop-p4-brief.md` task `task_2a996254fba9` ctx `ctx_2eb1c2c25566` | 완료 |
| reviewer | `term_474e9b40-427f-4e01-98bd-fc77cef81d05` | `task_ad15cced6aa6` | `ctx_76021c204e9d` | `sc-rank-desktop-review-brief.md` | 진행 |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/kknaks/kknaks_profile/pull/64 (541f109)
- code PR: ~~kknaks_profile#65~~ 닫음 → https://github.com/kknaksss/sc-rank/pull/1 (f7dac29) · main 20ef3b7
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-09-30` 문서 검수 FAIL6/WARN11 → SPEC v0.2.0 → 재검수 WARN(N-1~3 정정) → desktop P1+P2 발주
- `2026-09-30` 제품 착수 · DEC/SPEC/WORK 작성 · config·roles 생성 · 문서 검수 발주

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
