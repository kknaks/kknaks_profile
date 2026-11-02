# [planner] SPEC-001 0.6.1 · WORK-001 · README — v2 마감 동기

너는 interpret-pwa planner 다. 역할(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/planner/role.md` (+ rules …). allowed_paths: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/README.md`. DEC · log.md 는 코디 몫. 커밋 금지.

## 입력
- 지금 SPEC 0.6.0 · WORK-001 · DEC D-39 ~ D-41
- 백엔드 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/wp16-be-report.md` — 「처분 2」 · 「처분 3」 절 · infra `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/wp17-infra-report.md` · 처분 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-v2/research-dispositions.md`
- 배포본(read-only): `git -C /Users/kknaks/git/toy_pr2/interpret-pwa show origin/main:back/app/service/interpret/langs.py` (CONTEXT_MAX_CHARS 표) · `…:back/seed/glossary.json`(.6 · 170 term)
- 배포(코디 확인): 코드 #10(main 17c26b5) · infra #35(PVC · 기록) · **#36(back cpu request 100m → 50m — lima-worker-1 CPU 예약 3,950m/98% 로 PVC 고정 노드에 새 pod Pending · limit 1 그대로)** · 확인: seed .6 로드 · records on dir=/data/records keep_days=7 · 세션 시작/끝 줄 기록됨 · zh-Hant context 21,658/21,689 (terms 170 · 역방향 별칭 33 줄임)

## 고칠 것 (0.6.0 → 0.6.1)
1. §2.4 · §4.6: 한도 = **언어별 표**(en 23,424 · ja 20,419 · zh 20,933 · zh-Hant 21,689 · th 21,343 · vi 22,891 · yue 21,123 — .6 실측 통과치 × 0.9) · `GLOSSARY_CONTEXT_MAX_CHARS` = 값이 있으면 모든 언어를 덮는 하나의 값
2. OQ-018 ⑤ **뒤집음** — ko 별칭 「써마지」 삭제(「써마지 CPT」 가 FLX 로 오역 · 실물 ⑳) · §9.3 ⑲ ~ ㉑ 결과
3. §9.6 배포: back request cpu 50m · 이유(PVC 노드 예약) · 배포 기록
4. §10: OQ-019(대문자 영문 TTS — 사용자 청취 대기) · 남은 OQ
5. WORK WP16 · WP17 · WP18 done(PR 번호) · README 현재 상태
6. 비밀값 0

## 완료 보고 (두 명령 · 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA')
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "planner 완료: SPEC 0.6.1" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] planner SPEC 0.6.1 완료 — <한 줄>" --enter`
