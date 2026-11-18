# [app] 0.5.2 앱 수정 1 — 덮인 조각(볼주름 꼴) · 원천 미확정 (다) 끝 상태

**너는 앞 판의 맥락이 없다.** /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev/phub-gold-jev-app-brief.md 의 역할 · allowed_paths · 공개 레포 제약 · §9 완료 보고 그대로(핸들은 preamble 값). 문서는 전부 /Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev 에 있다. 워크트리 /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev(미커밋 위에 이어서). **디스크 여유 2~3GB — 큰 파일 만들지 마라.**

읽을 것: `_RESUME.md` §2 맨 위 행(「덮인 조각 규칙」 — 정본) · `SPEC-002-chat-eval.md` §3-1 TG2 · TG3 · CD2 · §5 종료 상태 (다) · `app-v052-report.md`(F2 · F3) · runs.jsonl 의 run `ba0678ffec2a`(F2) · `a804a471de82`(F3) trace. 코드 검수(`review-code-v052-app.md`)가 같은 때 돌고 있다 — 있으면 F2 · F3 에 대한 지적을 같이 반영.

## 고칠 것

**F-1 덮인 조각(사용자 결정)** — 「볼 주름에 뭐 해?」: resolve 후보 = 볼주름 CON-012(덮이지 않음) + 주름 CON-001 · 부위 볼(둘 다 `covered_by`=볼주름). Jev 사이 값(0.56 · 0.37)이라 TG2 로 남았고, 부위 「볼」 이 **볼주름 조회의 부위 거르개**가 되어 허브가 주는 윗고민 65 묶음 → 2 로 좁혀졌다(C 는 65 로 맞게 답함). 규칙(일반 — 볼주름만 아님):
- **덮인 조각(`covered_by` ≠ null)은 Jev yes(≥ 문턱)일 때만 대상**이다. 사이 값 · no 는 읽지 않고 `front.dropped[]` 에 noul 과 함께 남긴다. TG2(「사이 값은 넘김 쪽」)는 **덮이지 않은 조각에만**.
- **덮은 대상의 조회에는 그 안에 든 조각을 거르개로 쓰지 않는다** — 부위 조각이 yes 로 대상이 되더라도 `concern_candidates(덮은 고민, site=그 부위)` 로 좁히지 않는다(덮은 이름이 이미 그 부위를 품는다). 떨어진 이름(「이마에 주름」 — 주름 · 이마 둘 다 덮이지 않음)은 지금처럼 부위 거르개를 쓴다(HG3 꼴 그대로).
- 시험: 볼주름 꼴(덮인 부위 · 덮인 고민 사이 값 → dropped · 거르개 0) · 이마 꼴 회귀(16 묶음 그대로) · 덮인 조각 yes 꼴.

**F-2 (다) 끝 상태** — Q12 「필러 혈관 폐색은 언제 나타나고 얼마나 가나?」: B 답은 정답 꼴(시간 빈칸을 밝힘 · 효과 기간과 안 섞음)인데 종료 상태가 「후보 소진」(기대 「원천 미확정 (다)」 — 물은 칸이 silver 빈칸). 원인(보고서: adverse:ADV-051 대상 required 0 · end_state 1회차 (다) 미판정 O-5 ②)을 짚어 SPEC §5 (다) 대로 판정되게 고친다. SPEC 과 다르게 고쳐야 하면 고치지 말고 `[질문]`.

## 확인

- ruff · pytest(전체 1회).
- 실물: 18221 속도 탭 API(effort low · 동시 · 허브 **18105** — 코디가 0.5.2 로 재시작함)로 「볼 주름에 뭐 해?」 · Q12 · 「이마에 주름이 많아서 걱정이에요」 각 1회 → B 묶음 수 · 종료 상태 · C 대비. 18220 · 18105 는 코디 것(띄우거나 내리지 마라).
- 커밋 후보 grep. 보고서 `app-v052-fix1-report.md`(같은 폴더).
