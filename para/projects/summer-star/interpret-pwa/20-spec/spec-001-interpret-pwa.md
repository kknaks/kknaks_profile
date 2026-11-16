---
type: spec
id: SPEC-001
title: "통역 PWA — 로그인 · 용어집 context · 통역 WS · 화면 · PWA 계약"
version: 0.9.3
status: draft
product: interpret-pwa
created_at: 2026-10-26
updated_at: 2026-11-15
tags:
  - product/interpret-pwa
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-001-interpret-pwa|BASE-001]]"
  decisions:
    - "[[decision-001-interpret-pwa|DEC-001]]"
  specs: []
  works:
    - "[[work-001-interpret-pwa|WORK-001]]"
  releases: []
  related: []
sources:
  - para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md (D-01 ~ D-66 · accepted — D-13 · D-32 는 뒤집힘 · D-41 이 Scope Out 「통역 기록 저장」을 In 으로 · D-42 가 D-41 의 「7일 뒤 자동 삭제」를 뒤집음 · D-43 ~ D-50 품질 개선(D-47 방향 바로잡음 · D-49 = SPEC OQ-025 · D-50 = SPEC OQ-029 · **D-51 「써마지」 일반 term · 사전 보정 처분 · D-52 토닝 zh · D-53 대만어 별칭 정리 · D-54 한도를 넘는 언어는 근거가 약한 별칭부터** · **D-55 끊김 비교 조합 C2 · D-56 언어별 한도 = v6 실측 × 0.96 · D-57 다국어 묶음 · D-58 번역 뒤 시술명 바로잡기 · D-59 나라별 시험 — 최종 버전만 · 0.9.0** · **D-60 써마지 zh-Hant 현지명 · D-61 그 나라 글자가 있는 언어는 `name` 을 그 나라 글자로 · D-62 ja · th 는 `terms` 줄이기로 받음 · D-63 바로잡기 ② 한자 언어 사이 한자 꼴 제외 · D-64 외 → 한 「가까운 한글 낱말」 — 0.9.2** · **D-65 · D-66 ④ 를 좁힘(첫 음절 · 남는 것 = 비었거나 조사 · 음절 빠짐 해석 안 함 · 멈춤 목록) — 0.9.3**) · 「열린 것 (2026-11-14 · 품질 개선)」 OQ-021 ~ 023 닫힘)
  - orchestration/work/interpreter-idea/{wp22-be-report.md,wp23-be-report.md,wp24-be-report.md,wp22-human.json,wp24-human.json,wp22-A.json,wp22-B.json,wp24-C.json,wp24-C2.json,wp24-C-guest.json,wp24-C2-guest.json} (품질 시험 6차 결과 — 조합 A · B · C · C2 · 손님 쪽 21문장 · v6 한도 재측정 ⑬′ · 사람 판정 · **번호 · 수치만** — 0.9.0 §4.6 · §9.3 「6차 결과」) · quality-research-dispositions.md §8 · §9 (WP22 · WP23 처분)
  - orchestration/work/interpreter-idea/{quality-spec-v090-brief.md,quality-spec-v090-add-1.md} (0.9.0 — 7차는 최종 버전 하나만)
  - orchestration/work/interpreter-idea/review-quality-doc-report-6.md (0.9.0 문서 6차 검수 F-1 · W-1 ~ W-5) · quality-research-dispositions.md §10(6차 결과 처분) · §11(검수 처분) — 0.9.1
  - orchestration/work/interpreter-idea/{review-wp26-code-report.md,seed-v9-be-report.md,seed-v9-diff.json,wp27-be-report.md,test7-result.json,test7b-result.json,test7c-result.json} (코드 검수 W-3 · 시드 `.9` · `.10` · 7차 결과 — **번호 · 수치만**) · quality-research-dispositions.md §12 ~ §16 · quality-spec-v092-brief.md — 0.9.2 · 7차 사람 판정은 로컬 전용 `reference/2026-11-12-interpreter-idea/quality-run/test7c-human.js`(git 제외 — 등급 수만 옮김)
  - orchestration/work/interpreter-idea/{review-predeploy-code-report.md,review-predeploy-code-report-2.md,wp27-be-report.md(수정 3 · 4),quality-spec-v093-instructions.md} (배포 전 코드 검수 F-1 · F-2 · W-1 · 재검수 W-1 · W-2 · D-65 · D-66 — 0.9.3)
  - 구현 워크트리 interpret-pwa `interpreter-idea`(미커밋 — WP21 · WP23 뒤 · `back/app/service/{records.py,glossary.py,interpret/session.py,interpret/assembler.py,interpret/langs.py}` · `back/seed/glossary.json` `2026-11-14.7` — 0.9.0 §4.2 · §5.9 · §5.12 대조)
  - orchestration/work/interpreter-idea/review-quality-doc-report.md (0.8.0 문서 검수 WARN W-1 ~ W-6 — 0.8.1)
  - orchestration/work/interpreter-idea/{quality-research-dispositions.md,quality-r1-zh-report.md,quality-r1-zh-cells.json,quality-r2-en-ja-th-vi-report.md,quality-r2-en-ja-th-vi-cells.json} (D-46 사전 보정 조사 2026-11-14 — 510 + 680칸 · **코디 처분(확정)이 값의 기준** — 0.8.2 §4.2.4 · **처분 §4(OQ-030) · §5(D-54) · §6(r3) — 0.8.3**)
  - orchestration/work/interpreter-idea/{quality-r3-tw-alias.json,quality-r3-tw-alias-report.md} (D-53 대만어 별칭 조사 — 245행 · 판정 넷 · 0.8.3 §4.2.4 ② F)
  - orchestration/work/interpreter-idea/review-quality-doc-report-3.md (0.8.2 문서 3차 검수 F-1 · W-1 ~ W-3 — 0.8.3)
  - orchestration/work/interpreter-idea/review-quality-doc-report-4.md (0.8.3 문서 4차 검수 F-1 · W-1 ~ W-3 · 코디 처분 §7 — 0.8.4)
  - orchestration/work/interpreter-idea/review-quality-doc-report-2.md (0.8.1 문서 재검수 WARN N-1 ~ N-3 — 0.8.2)
  - 확정 시안 — Claude Design 캔버스 「Interpret PWA」(r3 · D-22 ~ D-24 · D-28 ~ D-30 반영 · r7 D-36 `Mode-Auto-Idle` · `PTT-Ready` · `PTT-Pressed` · r8 D-37 `Glossary` 삭제 · 화면 21개) 로컬 사본 interpret-pwa-poc 코드 워크트리 design/{README.md,project/*.dc.html,project/ceramique-theme.css} (D-20 · D-21 · 화면 19개)
  - 구현 kknaksss/interpret-pwa main d0a91a7(배포본 · D-22 ~ D-32 반영 — 0.4.0 은 이 코드에 맞춰 적고, 다르면 DEC 를 따른다) · main 9befd18(PR #4 · D-33 시드 — 0.4.1 대조) · main fe8475e(PR #5 ~ #8 · D-34 ~ D-37 · 운영 장애 수정 — 0.5.0 대조) · main 2a9d5a5(PR #9 · D-38 시드 `.5` — 0.6.0 대조) · **main 17c26b5(PR #10 · 시드 `.6` · 통역 기록 · 언어별 한도 — 0.6.1 대조)** · **main e0fbda8(PR #11 · 보관 기간 env — 0.8.0 대조 · 지금 back 배포본 · `back/app/service/{glossary.py,interpret/soniox.py,interpret/langs.py,interpret/assembler.py,interpret/session.py}` · `front/lib/view.ts`)**
  - Soniox 공식 문서 2026-11-14 — stt/models(v6 2026-11-03 · v5 Deprecated · 2026-12-15 제거) · stt/concepts/context(`text` 칸 · 8,000토큰) · stt/rt/endpoint-detection(끊김 값 넷 · 범위 · 기본값) (0.8.0 §4.5 · §5.10)
  - 품질 시험 목록 T01 ~ T33 — 프로필 레포 워킹트리 `reference/2026-11-12-interpreter-idea/test-sentences.md`(**로컬 전용 · git 제외** — DEC OQ-021 · 이 문서에는 번호 · 분류 · 판정 방식만 · 0.8.0 §9.3)
  - orchestration/work/interpret-pwa-poc/{research-tw-names-report.md,d35-be-report.md,live-check-d35-2026-10-27.json,d36-fe-report.md,design-r7-report.md,d37-be-report.md,d37-fe-report.md,design-r8-report.md} (대만 현지명 조사 77/157 · D-35 시드 · 운영 장애 2026-10-27 02:07 원인 · D-36 · D-37 구현)
  - orchestration/work/interpret-pwa-v2/{research-r1-zh-report.md,research-r2-ja-en-tw-report.md,research-r3-th-vi-yue-report.md,research-dispositions.md} (D-39 · D-40 조사 3갈래 2026-10-27 · **코디 처분이 기준** — 0.6.0 §4.2.1 ~ §4.2.3)
  - orchestration/work/interpret-pwa-v2/{wp16-be-report.md,wp17-infra-report.md,live-check-wp16-{seed,seed-2,seed-3,ceiling,newterms,newterms-2,records}.json} (WP16 「처분 2」 · 「처분 3」 — 언어별 한도 · OQ-018 ⑤ 뒤집음 · 실물 ⑲ ~ ㉑ · WP17 PVC — 0.6.1)
  - k8s_infra_mac origin/main charts/interpret-pwa/{values.yaml,values-prod.yaml} (PR #35 PVC · 기록 · back 17c26b5 · PR #36 back cpu request 50m — 0.6.1 §9.6)
  - orchestration/work/interpret-pwa-seed-tw/{research-tresure-report.md,seed-tw-be-report.md} · para/projects/summer-star/interpret-pwa/log/2026-10-27-interpret-pwa-seed-tw.md (D-38 시드 `.5` — 0.6.0 에서 §4.2.1 에 뒤늦게 기록)
  - k8s_infra_mac origin/main charts/cc-prototype/{templates/back-pvc.yaml,templates/back.yaml,values.yaml,values-prod.yaml} · charts/interpret-pwa/* (PVC · local-path 노드 제약 선례 — 0.6.0 §9.6)
  - orchestration/work/interpret-pwa-poc/{wp9-be-report.md,wp9-fe-report.md,live-check-wp9-2026-10-27.json} (시드 실물 ⑫ ~ ⑯ · 한도 20251 처분)
  - orchestration/work/interpret-pwa-poc/{wp6-be-report.md,wp6-fe-report.md,fix-phone1-be-report.md,fix-phone1-fe-report.md,fix-phone2-be-report.md,fix-phone2-fe-report.md,fix-phone2-design-report.md,fix-phone3-be-report.md,fix-phone3-fe-report.md,live-check-wp6-2026-10-26.json} (D-22 ~ D-32 구현 · 실물 ⑧ ~ ⑪ · 한도 18832)
  - orchestration/work/interpret-pwa-poc/{design-report.md,live-check-2026-10-26.json,review-code-report.md,e2e-feedback-batch-1.md} (시안 제안 · Soniox 실물 ① ~ ⑦ · 코드 리뷰 FAIL-1 · WARN 1 ~ 6)
  - para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md (입력 1 ~ 5 · 확인한 사실 2026-10-26 · 2026-11-14)
  - cc-prototype origin/main procedure/back/app/{api/interpret.py,service/interpret/*.py,service/auth.py,config.py,main.py,domain/errors.py} · tests/test_interpret.py (통역 · 로그인 원형 — 로직 정본)
  - cc-prototype origin/main _archive/cc/front/lib/interpret.ts (브라우저 마이크 · 재생 · 반이중 원형)
  - cc-prototype origin/main procedure/front/{tailwind.config.ts,app/layout.tsx,app/styles/medikit-patches.css,package.json} · _archive/cc/design/_ds/medikit-*/README.md (medikit 붙이는 법)
  - orchestration/work/_archive/cc-prototype/sts-prototype/{interpret-ws-contract.md,wp2-be-report.md,research-soniox-chinese-report.md}
  - para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md §3 · §4 (원형 계약 문서)
  - Soniox 공식 문서 2026-10-26 — stt/concepts/context · stt/concepts/supported-languages · tts/concepts/supported-languages · translation/stt-translation/rt-translation
  - GET https://stg-procedure-hub.medisolveai.com/api/v1/glossary/matrix 실물 응답 2026-10-26 · 2026-10-27 (version 2026-07-01-reviewed-v5 · count 158 — 0.4.0 부터는 첫 가져오기 원천만 · §4.8)
---

# 통역 PWA — 계약

> 레포 `kknaksss/interpret-pwa` 의 `back/`(FastAPI · uv) 과 `front/`(Next.js PWA)가 지킬 계약.
> 통역 중계는 cc-prototype 원형(`procedure/back` 의 `service/interpret/` · `api/interpret.py`)을 **복사해서** 쓰고,
> 이 문서는 원형과 **달라지는 자리**와 새로 생기는 것(로그인 · 용어집 · 화면 · PWA)을 정한다.
>
> SSOT 순서(이기는 순): ① DEC-001 D-01 ~ D-66 ② 화면 = 확정 시안(D-20) ③ 통역 로직 = 원형 코드(`origin/main`) ④ Soniox 공식 문서 · 실물 결과(§9.3) ⑤ 이 문서의 기본값.
> **화면 정본은 확정 시안이다(0.3.0 · D-20 · D-21)** — Claude Design 캔버스 「Interpret PWA」(사용자가 직접 고친다). 로컬 사본은 코드 레포 `design/project/*.dc.html` — 참고 자료이고 빌드에 넣지 않는다. 시안이 바뀌면 사본을 다시 받고 §6 · §7 을 맞춘다. **시안과 DEC 가 다르면 DEC 가 이긴다**(D-22 ~ D-25 · D-29 · D-31 은 시안보다 뒤에 정했거나 시안을 고친 결정이다). 시안에 없는 자리(네트워크 실패 로그인 · 오프라인 화면)는 이 문서 문구를 따른다.
>
> 이 레포는 public — Soniox 키 · 로그인 아이디 · 비밀번호 · 세션 비밀값 · 실명을 쓰지 않는다. env 는 **이름만**(D-06 · D-11).

## 변경 이력

| 버전 | 날짜 | 무엇 |
|---|---|---|
| 0.9.3 | 2026-11-15 | 배포 전 마지막 — DEC **D-65 · D-66** · 배포 전 코드 검수 두 번(`review-predeploy-code-report.md` FAIL F-1 · F-2 · W-1 → `-2.md` WARN W-1 · W-2) · backend 수정 3 · 4(`wp27-be-report.md`): **§5.12 ④ 「가까운 한글 낱말」 을 좁힘** — 첫 음절이 대표명과 같을 때만(D-65 ⓐ) · 앞부분 길이는 대표명과 같거나 + 1 뿐(음절이 빠진 꼴은 해석하지 않음 — D-66 ⓑ) · 남는 것이 비었거나 조사일 때만(D-66 ⓐ — 거르기) · 끝 음절이 조사인 「빠진 꼴 + 조사」 제외 · 홀로 붙은 해요체 「요」 는 조사 아님 · 대표명에 한글 밖 글자가 들면 건너뜀 · 멈춤 목록 = 코드 상수 `KO_NEAR_STOP` 21개 · 낱말 전체 · 조사 뗀 낱말에도(D-65 ⓒ) / **OQ-033 닫힘 — 넓히지 않는다**(D-66) / **§9.3 「7차 결과」 152 / 196**(저장 결과로 다시 봄 — 손님 쪽 zh-G03 한 행이 pass → fail · 첫 음절이 다른 꼴) / §9.1 「바로잡기」 ⑰ 고침 · ⑱ / 부록 A D-65 · D-66. ① ② ③ · 한 → 외 · 시드 `.10` · WS 메시지 모양 · 기록 키 그대로 |
| 0.9.2 | 2026-11-15 | 배포 전 동기화 — DEC **D-60 ~ D-64** · 처분 §12 ~ §16 · 코드 검수 W-3(`review-wp26-code-report.md`) · 7차 결과(WP27 · 수정 1 · 2). 코드 · 시드는 이미 이 모양이다 — 문서를 맞춘다: **§4.2.5 「바뀌는 것」**(시드 `.8` 은 틀린 꼴 말고도 kr-014 zh-Hant(D-60) · ph-033 zh · yue 별칭(처분 §13 ①)을 바꿨다 · 실제 목록 40개 · 16칸 · T04 칸은 뺌 — 처분 §14 W-1) / **새 절 §4.2.6 시드 `.9`**(D-61 · 처분 §15 — 그 나라 글자가 있는 언어의 영문 `name` 을 그 나라 글자로 · `name` 73칸 · 근거 없는 별칭 36개 뺌 · 칸 목록은 `seed-v9-diff.json`) · **§4.2.7 시드 `.10`**(처분 §16 — 7차에서 나온 틀린 꼴 7개) / **§4.6 「시드 `.8` ~ `.10` 의 글자 수」**(D-62 — `.9` 부터 ja `terms` 2 · th `terms` 79 가 빠진다 · 짝 손실 0 · 거절 0 · 한도 표는 D-56 그대로) / **§5.12 ② 에서 한자 언어 사이의 한자 꼴을 후보에서 뺌**(D-63) · **새 단계 ④ 「가까운 한글 낱말」**(D-64 — 외 → 한만 · ko 대표명과 음절 하나만 다른 꼴) / §9.1 「밖으로 내는 것」 — `api/interpret.py` 의 세션에 넘기는 한 줄 예외 · 「바로잡기」 ⑮ ~ ⑰ / **§9.3 「7차 결과」 채움**(언어별 기계 판정 · 사람 판정 등급 수 · 남은 실패 갈래 — 문장 0) / §9.6 배포 뒤 확인 0.9.2(시드 `.10` · 사용자 확인 끝 2026-11-15) / 부록 A D-60 ~ D-64. 새 env 없음 · WS 메시지 모양 · 허용 경로 6개 · front 그대로 |
| 0.9.1 | 2026-11-15 | 6차 검수 처분(`quality-research-dispositions.md` §10 · §11 · `review-quality-doc-report-6.md` F-1 · W-1 ~ W-5): **§5.12 ③(가까운 라틴 낱말)은 번역 글자가 라틴이 아닌 쪽에서만**(F-1 — 한 → 외는 ja · zh · zh-Hant · th · yue · 외 → 한은 7개 언어 전부 · **en · vi 한 → 외는 ① ② 만**) · **글을 바꾸는 일치의 라틴 낱말 경계 = 앞뒤가 라틴 글자(부호 붙은 글자 포함) · 숫자가 아님**(ASCII 구간 아님 — 베트남어 낱말 가운데를 바꾸지 않게) / **조건 2 에 한 줄**(W-1 — 외 → 한: 원문의 그 이름을 같이 가진 다른 term 의 ko 가 번역에 있으면 대상 아님 · 로그 0) / **순서 = 걸린 term 전부에 ① ② 먼저 · 남은 term 만 ③**(W-2) / 자리 두 줄(W-3 — 빈 원문이면 부르지 않음 · `fixed` 는 caption dict 에 싣지 않고 따로 넘김 · 정규화가 글자 수를 안 바꾼다는 시험) / **§5.9 새 키 `translation_before`**(바로잡은 발화 줄에만 — 바로잡기 전 번역 · **OQ-031 닫음**) / **§4.2.5 첫 목록에서 T46(`ko_wrong`)을 뺌**(일상 한국어 낱말은 틀린 꼴로 넣지 않는다 — 실패로 남긴다) / §9.3 「6차 결과」 처분 칸을 처분 §10 으로 채움(W-5 · T24 포함) / §9.1 「바로잡기」 시험 더함 / WORK WP26 완료 조건 「시드 `.8` 은 코드와 같은 PR」(W-4). ③ 의 숫자(4 · 2) · 조사 안 맞춤 · 검사 8 의 2글자 하한 · ② 의 범위 · 7차 손님 쪽 기대 ko 는 그대로(처분 §11) |
| 0.9.0 | 2026-11-15 | 품질 개선 2루프 — DEC **D-55 ~ D-59** · 품질 시험 6차 결과(WP22 · WP23 · WP24): **§4.6 · §2.4 언어별 한도 = v6 실측 통과 최대치 × 0.96 내림**(D-56 — en 24,892 · ja 21,962 · zh 22,551 · zh-Hant 22,685 · th 23,215 · vi 24,349 · yue 22,825 · 시드 `.7`(D-54 로 27개 뺀 판)에서 7개 언어 줄이기 0 · th 여유 22자 · **OQ-028 닫음**) / **새 절 §5.12 「시술명 바로잡기」**(D-58 — 확정 발화의 원문에 term 이 걸렸는데 번역에 대상 쪽 사전 이름이 없으면, 번역 속 틀린 꼴을 사전 `name`(외 → 한은 ko 대표명)으로 갈아 끼운 뒤 자막 · TTS · 기록으로 · 찾는 순서 ① 시드 틀린 꼴 ② 다른 언어 이름 · 별칭 ③ 가까운 라틴 낱말(숫자는 기본값 · 시험으로 확인 — OQ-032) · 못 찾으면 그대로 + 로그 1줄) / **§4.2 시드 새 필드 둘** — entry `wrong` · term `ko_wrong`(틀린 꼴 · 바로잡기만 읽음 · context 재료 아님) · **검사 8** `wrong_form` / **§4.2.5 시드 `.8`**(`2026-11-15.8` — 틀린 꼴 첫 목록 · 번호 · term · 언어만 · 이름 · 별칭은 `.7` 그대로) / **§5.9 발화 줄 새 키 `fixed`**(바로잡은 term id · 「여기 없는 키 0」 을 함께 고침) / **§5.10 끊김 `max_endpoint_delay_ms` 1000 유지**(D-55 — C2(2000)는 조각 수 · 판정이 C 와 같고 지연만 늘어남 · **OQ-027 닫음**) / **§9.3 「6차 결과」 채움** · **「7차 — 나라별 시험」**(D-57 · D-59 — 7개 언어 × 직원 쪽 19 · 손님 쪽 9 = 196행 · **최종 버전 하나만**(이전 조합은 다시 돌리지 않는다) · 판정은 사전에서 자동 · 결과 페이지 = 언어별 탭 · 로컬 전용) · ㉖ · ㉗ / §9.1 「시드」 ⑧ · 「바로잡기」 · 「기록」 ⑪ / §9.6 배포 뒤 확인 0.9.0(WP25 는 WP27 뒤 · 사용자 확인 뒤) / §10 OQ-031 · OQ-032 / 부록 A D-55 ~ D-59. 새 env 없음 · WS 메시지 모양 · 허용 경로 6개 · front 그대로. 코드 · 시드는 WP26 에서 따라온다 |
| 0.8.4 | 2026-11-14 | 4차 검수 처분(`quality-research-dispositions.md` §7) — **D-54 의 「넘는다」 = 줄이기 없는 전체 글자 수 > 기준(실측 통과 최대치 × 0.9 내림)**(F-1 · §4.6 「D-54 절차」 2 · 4 · 5) / yue ph-034 는 `.6` 그대로 확인(W-1) / **① 별칭 순서 = 지금 별칭 → 옛 name → 제안 · 표 대조는 집합 비교**(W-2) / **옛 zh-Hant name `瘦臉針`(ph-034)도 뺀다**(W-3 — 남김 4 · 뺌 3 · zh-Hant 별칭 247 → **167** · F 뒤 22,356자 · **667자 초과 · `terms` 61** · D-54 뒤 여유 272) / 읽는 법 a 14 → 13칸 |
| 0.8.3 | 2026-11-14 | 시드 `.7` 보완 — DEC **D-54** · 코디 처분 **§4(OQ-030) · §5 · §6(조사 r3)** · 문서 3차 검수 F-1 · W-1 ~ W-3(`review-quality-doc-report-3.md`): **§4.2.4 「읽는 법」 e = 7개 언어 전부**(부위 term 에 시술 이름을 name · alias 로 새로 넣지 않는다 — 9칸을 ② C 에 칸마다 · F-1) · **OQ-030 닫음** · **③ 개수 다시 계산**(`name` 201 → **199** · alias 더한 칸 220 → **214**(낱개 319 → 306) · 바뀐 칸 349 → **343** · `reviewed` 66 / 56 그대로) / **② F 다시 씀**(W-1): r3 파일 필드(`id` · `alias` · `verdict` · `sources` · `note`) · **판정 넷과 처리**(유지 138 · 유지 — 10-27 근거 23 · 뺌 77 · 다른 term 과 겹침 7 은 건드리지 않음) · **별칭으로 내려오는 옛 zh-Hant `name` 7개에도 D-53**(근거 없는 2개 뺌) · F 뒤 zh-Hant 별칭 247 → **168** / **읽는 법 c — 버리는 28칸을 id 로**(W-3) · ja 별칭 1개 차이 원인(ph-071 `VOLNEWMER` — 대소문자만 다른 별칭 · ① 문구를 못 박음) / **§4.6 「시드 `.7` 추정」 다시 계산**(W-2 — 「zh-Hant 는 안 잘릴 것」 을 고침: D-53 뒤에도 **703자 초과 · `terms` 64** · 역방향 별칭 0 / ja `terms` 138 → **128** · th 역방향 별칭 15 → **9**) · **「D-54 절차」**(v6 재측정 → 넘는 언어만 약한 별칭 뺌 → 다시 잼 → 그래도 넘으면 멈춤) / §9.3 ㉒ · §10 OQ-028 · 부록 A D-54. 값은 문서만 — 시드 · 코드는 WP23 에서 따라온다 |
| 0.8.2 | 2026-11-14 | 시드 `.7` 값 채움 — DEC **D-51 · D-52 · D-53** · 사전 보정 조사 r1 · r2(1,190칸) · 코디 처분(`quality-research-dispositions.md`) · 문서 재검수 N-1 ~ N-3: **§4.2.4 를 채움** — 칸 판정 → 반영 규칙(처분 §1) · 손 처분 칸(새 term **`kr-014` 써마지 · `kr-015` 리투오** · 합치는 term 두 쌍 **ph-105 ← ph-106 · ph-097 ← ph-127**(없앤 `id` 는 다시 쓰지 않음 · 통역 기록은 고치지 않음) · 토닝 zh `调Q激光`(D-52) · yue 출처 없는 음역 17칸 → 영문 · zh 장비 셋 영문 · 빗금 정리 31칸 등) · **언어별 개수**(planner 계산 — `name` 바뀜 201 · alias 더한 칸 220 · `reviewed` ✗→✓ 66 · ✓→✗ 56 · vi S3 단독 0) · 「기계 적용 — 읽는 법」 a ~ k / 시드 `version` = **`2026-11-14.7`** · `id` 규칙(§4.2) / **§4.2.1 모호어 목록 — `kr-014` 의 name 예외**(D-51 이 10-27 처분 6 · OQ-018 ⑤ 를 뒤집음) / **§4.2.4 ② F — 대만어(zh-Hant) 별칭 정리(D-53)**: 조사 r3 `quality-r3-tw-alias.json` 에서 「뺌」 인 별칭을 지운다 · term 은 안 뺌 · 값은 그 파일이 나오면 WP23 에서 / **§4.6 「시드 `.7` 추정」**(순수 계산 · D-53 적용 전 — **ja `terms` 138 · th `terms` 전부 + 역방향 별칭 15 · zh-Hant 역방향 별칭 44 → 53** · 정방향 0 · zh-Hant 는 D-53 정리 뒤 안 잘릴 것으로 봄) / §9.3 N-1(「여섯 가지」) · N-2(규칙 ① 「걸리는 쪽」) · ㉒ 「써마지」 다시 보기 / §10 **OQ-030**(처분이 말하지 않은 자리) · OQ-028 에 ja · th / 부록 A D-51 · D-52 · D-53. 값은 문서만 — 시드 · 코드는 WP23 에서 따라온다 |
| 0.8.1 | 2026-11-14 | 품질 개선 보완 — DEC **D-49 · D-50** · 고친 **D-47** · 문서 검수 WARN 6(`review-quality-doc-report.md`): **§4.5 문안 = S1 ~ S4 네 문장**(D-49 — 「시술은 수술이 아닌 미용 시술」 · OQ-025 닫음 · 424자) · **§4.6 다시 계산**(문안 439자 — zh-Hant 역방향 별칭 33 → **44** · th 여유 **100**) / **§9.3 손님 쪽 문장 = 7개 언어 × 3 = 21**(D-50 · OQ-029 닫음) / **§9.3 「조합」 — 끄는 길**(W-1: 조립 · 세션 함수의 선택 인자로만 · 운영 기본값 = 켬 · env · WS 로 못 끔 · A · B 확인에 「막힌 빈 원문 수 0」) · **3절 = 기대한 수의 발화**(W-2: 규칙 파일에 문장마다 기대 확정 발화 수 · 조각 수 = 실제 − 기대) · **기계 판정 규칙 종류 넷**(W-3: 글자 그대로 · 정규식 · 발화 수 · 기계로 못 옮기면 사람 판정) · **합성 언어 = 말할 문장의 언어**(W-4) / §9.1 「기본값 = 켬」 시험 / **§5.10 · OQ-027 `endpoint_sensitivity` 방향 단정**(공식 「Higher values make endpoints more likely」 → 덜 끊으려면 낮춘다 · D-47) / 부록 A D-47 · D-49 · D-50 |
| 0.8.0 | 2026-11-14 | 품질 개선 — DEC D-43 ~ D-48 · DEC OQ-021 ~ 023 반영(배포본 main e0fbda8 대조 · 코드는 WP21 · 시드는 WP23 에서 따라온다): **§5.10 STT 모델 `stt-rt-v6`**(D-43 — 모델 이름만 · 다른 STT 설정 그대로) · **끊김 값**(D-47 — 1루프 `max_endpoint_delay_ms` 1000 그대로 · 올릴지는 시험 3절 뒤 사용자 · 공식 문서의 이름 · 범위만 인용) / **§5.11 빈 원문 막기**(D-48 — 원문에 글자 · 숫자가 하나도 없는 발화는 자막 · TTS 로 내보내지 않음) / **§4.5 context 서술 칸 `text`**(D-45 — 역할 · 방향 문안 초안 · `general` 은 그대로 · 일반 낱말 짝은 `translation_terms` 에 넣지 않음) · **§4.6 `text` 는 줄이지 않는 칸** · 언어별 여유 계산 방법 · 시드 `.6` 기준 추정(zh-Hant 역방향 별칭 33 → 42) / **§4.2.4 시드 `.7` 보정 절 — 자리만**(D-46 — 근거 · 규칙 · 처분 절차 · 이름 겹침 원칙 · 확인된 오류 목록 · **바꿀 값 표는 조사 뒤 채움**) / **§9.3 「6차 — 품질 시험」**(D-44 — 목록 위치 · 분류 5개 · 조합 A · B · C · 입력 = Soniox TTS 음성 파일 · 기계 / 사람 판정 · 손님 쪽 문장 조건 · 울쎄라 원인 가르기 · 결과는 번호 · 수치만) / §9.1 시험(STT 설정 · context `text` · 빈 원문) / §9.6 배포 뒤 확인 0.8.0(WP25) / §5.1 표 / §10 OQ-024 ~ OQ-029 / 부록 A D-43 ~ D-48. 새 env 없음 · WS 메시지 모양 · 허용 경로 6개 · 통역 기록 줄 모양은 그대로 |
| 0.7.0 | 2026-11-14 | 보관 기간 env — DEC D-42 반영(배포본 main 17c26b5 대조 · 코드는 WP19 에서 따라온다): **§5.9 「7일 뒤 삭제」 → 「보관 기간 — env」** — `INTERPRET_RECORD_KEEP_DAYS` · **비어 있으면 삭제 안 함**(기동 때 삭제 0 · 24시간 배경 작업을 만들지 않음 · 기동 로그 `keep_days=off`) · 양의 정수 N 이면 0.6.0 규칙 그대로 7 자리에 N(`keep_days=N`) · 그 밖의 값(0 · 음수 · 숫자 아님)은 경고 1줄 뒤 삭제 안 함(기동은 멈추지 않음) · 기록 끔이면 값과 무관 / §2.4 env 행 / §1 · §2.1 디렉토리 설명 / §9.1 「기록」 ⑦ · ⑨ 시험 / §9.3 주 / **§9.6** — 운영 ConfigMap 에 넣지 않음(infra 는 이미지 태그만) · 크기 근거(무기한 · 실측 4일 44KB) · 배포 뒤 확인 0.7.0(WP20) / §10 OQ-020(베타가 끝나는 때 · 넣을 값) / 부록 A D-42. D-41 의 나머지(넣는 것 · 안 넣는 것 · 화면 · API 없음 · 꺼내기 kubectl · 허용 경로 6개)는 그대로 |
| 0.6.1 | 2026-10-28 | v2 마감 동기 — 배포본 code main 17c26b5(PR #10) · infra PR #35 · #36 · WP16 「처분 2」 · 「처분 3」 대조: **§2.4 · §4.6 한도 = 언어별 표**(en 23,424 · ja 20,419 · zh 20,933 · zh-Hant 21,689 · th 21,343 · vi 22,891 · yue 21,123 — 시드 `.6` 실측 통과 최대치 × 0.9 내림 · `GLOSSARY_CONTEXT_MAX_CHARS` 는 값이 있으면 모든 언어를 덮는 하나의 값 · 운영은 넣지 않음) / **OQ-018 닫음 — ⑤ 뒤집음**(ph-130 ko 별칭 「써마지」 지움 — 「써마지 CPT」 가 FLX 로 오역 · 실물 ⑳) · ① ~ ④ 처분 반영을 **§4.2.3 D** 로 기록 / §4.2.1 모호어 표 · §4.2.2 · §5.9 「더 긴 일치」 예 · §9.1 시드 · context · 기록 시험 / **§9.3 ⑲ ~ ㉑ 결과**(5차) / **§9.5 배포 기록 10 · 11 · §9.6 back `requests.cpu` 50m**(lima-worker-1 CPU 예약 98% — PVC 고정 노드에 새 pod Pending · limit 1 그대로) · 배포 뒤 확인 결과 / §10 OQ-019(사용자 청취 대기) · OQ-017 ④ 새 시술 미적중 |
| 0.6.0 | 2026-10-27 | interpret-pwa-v2 — DEC D-38 ~ D-41 반영(배포본 main 2a9d5a5 대조): **§4.2.1 사전 내용 규칙을 언어 공통으로 다시 씀** — 현지 허가명 · 공식명 우선(대륙 = NMPA · 브랜드 대륙 공식명 · D-40) · **「현지에 없음 = 영문」을 7개 언어 공통 규칙**으로 · 옛 표기는 alias · 모호어 목록(언어별) · 묘사 꼬리 · 제조사 접두 · 대소문자 변형은 alias 로 안 넣음 · `reviewed` = 독립 현지 출처 2+ · **홍콩(yue)은 대만(zh-Hant)과 독립** · D-38(시드 `.5`) 기록 / **§4.2.2 새 시술 13개**(D-39 · term id `kr-001` ~ `kr-013` — Procedure Hub 밖 · N13 울트라셰이프 제외) × 7개 언어 표 / **§4.2.3 기존 표기 변경**(zh 대륙 공식명 · 미허가 톡신 · 한국 전용 제품 영문 · 포텐자 · 장르어 제거 · th 쥬베룩 · 스컬트라 · yue · vi 결함) / §4.2 검사 7 「보이지 않는 글자 0」(`白毒` 의 U+200C) · term `id` 규칙 · `version` `2026-10-27.6` / §4.6 `.6` 크기는 실측 ⑲ 로 · 기본값 20,251 그대로 / **§5.9 통역 기록 신설**(D-41 — back PVC · `INTERPRET_RECORD_DIR` · 날짜별 JSONL · 세션 시작/발화/끝 줄 · 걸린 term 판정 · 음성 · 토큰 · IP · 계정값 0 · 7일 삭제 · 쓰기 실패는 통역을 끊지 않음 · 화면 · API 없음 · 꺼내기 = kubectl) / §1 범위 · §2.4 env · §3.5 / §9.1 「시드」 · 「기록」 시험 · §9.3 ⑲ ~ ㉑ · **§9.6 배포 — back PVC(local-path · `lima-worker-1` 노드 고정 · 1Gi · keep)** / §10 OQ-018 · OQ-019 |
| 0.5.0 | 2026-10-27 | fix5 — 마감 동기. DEC D-35 ~ D-37 · 운영 장애를 최종 배포본 main fe8475e(PR #5 ~ #8)와 맞춤: **§4 시드** — 대만 현지명(조사 77/157 · zh-Hant `name` · 초안은 `aliases` · 출처 2+ 만 `reviewed:true`) · `source` 에 `web-research YYYY-MM-DD` · zh 구어 별칭(热玛吉) · 모호어 제외(zh · zh-Hant) · 볼뉴머 카테고리 · `version` `.4`(D-35) / **§4.7 용어집 메뉴 API 삭제 · §7.6 메뉴 = 로그아웃만**(D-37 · D-13 뒤집힘) / **§5.6 zh-Hant 자막 = `s2tw` + 「激光 → 雷射」**(D-35 · D-32 의 `s2twp` 폐기) · 가져오기 초안도 같은 변환 / §5.4 · §3.3 오류 문구 일반화 · `/api/auth/me` · `/api/health` = `{ok}` · `/docs` · `/openapi.json` 끔 · 허용 경로 6개(D-37 · §3.5) / **§5.8 TTS keepalive `{"keep_alive": true}` · 다른 stream_id 오류는 발화를 끊지 않음**(운영 장애 2026-10-27 02:07) / **§7.7 누르고 말하기 모드**(D-36 · 시안 r7) / §9 시험 · 실물 ⑰ ⑱ · 배포 기록 5 ~ 8 / §10 OQ 정리(남은 것: 사람 목소리 E2E · 못 찾은 대만명 80 · 데모 로그인 끄기) |
| 0.4.1 | 2026-10-27 | fix4 — 배포본 main 9befd18(PR #4) · WP9 보고 · DEC D-34 반영: §2.4 · §4.6 `GLOSSARY_CONTEXT_MAX_CHARS` **18832 → 20251**(시드 실측 ⑬ 가장 작은 통과 최대치 ja 22,502 × 0.9 · th 줄이기 0 · 코디 처분) · §4.2 backend 가 더한 것(알 수 없는 필드 = `unknown_field` 오류 · term 선택 필드 `note`) · §4.8 가져오기 `--date` · §7.3 #1 시작 오버레이 = **언어 단추 7개 — 누르는 것이 시작 · 상담사 방향(D-34)** · §9.3 ⑫ ~ ⑯ 결과 · §9.5 배포 확인 결과 · §10 OQ-005 · OQ-013 · OQ-014 갱신 |
| 0.4.0 | 2026-10-27 | fix3 — DEC D-22 ~ D-33 동기(배포본 main d0a91a7 대조): **§4 를 새로 씀 — 용어집 = 우리 시드 `back/seed/glossary.json`(D-33)** · 스키마(term · entry · 현지명 · 별칭 · 출처 · 검수) · 기동 때 읽기 · 깨지면 기동 실패(기본값 · 코디 권장) · context 정방향/역방향 × 기본/별칭 · 줄이기 순서 넷 · 메뉴 API 에 별칭 · 검수 · 첫 가져오기 스크립트(괄호 분해 · zh-Hant 초안 s2twp) · Procedure Hub 런타임 호출 제거 · `GLOSSARY_CONTEXT_MAX_CHARS` **18832**(실측 · OQ-002 닫음) / §2.4 · §3 데모 로그인(D-30) · `GLOSSARY_MATRIX_URL` 삭제 / §5.5 언어 7개 · zh-Hant · 목록 표시 이름 · 한국어 이름 중국어/대만어(D-28) / §5.6 번체 변환 언어별(yue s2tw · zh-Hant s2twp · D-32) / §7 원 위 외국어 안내(D-22) · 원 64/88 · 원 줄 140(D-23) · 말풍선(D-24) · 자동 스크롤 · ↓ 최신(D-25) · 로그인 입력 16px(D-27) · 초기화(D-29) · 데모 로그인 화면(D-30) · 언어 목록 180° 자체 목록(D-31) · 용어집 메뉴 별칭 · 검수 표시 / §9.3 ⑧ ~ ⑪ 결과 · 시드 재확인 ⑫ ~ ⑮ / §9.5 배포 주소(D-26) / §10 OQ-002 · 004 · 010 · 011 닫음 · OQ-012 ~ 014 |
| 0.3.0 | 2026-10-26 | fix2 — DEC D-18 ~ D-21 · 확정 시안 · Soniox 실물 결과 · 코드 리뷰 반영: §4.3 · §4.4 역방향 용어(D-18 · 줄이기 순서 terms → 역방향 · 정방향만 재연결 · 한도 기본값은 WP6 실측 — 코디 답 2026-10-26) · §5.7 TTS 입력 괄호 제거(D-19) · §6 · §7 시안 정본(ceramique 테마 · 앱 이름 통키 · 회전 아이콘 · 원 크기 · 글리프 · 색 점 · `final:false` gray-600 · 오버레이가 헤더까지 덮음 — 리뷰 WARN-3 닫음) · §7.4 멈춤 뒤 남은 TTS 조각 버림(FAIL-1) · 출력 언어 표시 시점(WARN-4) · §3 · §4.2 기동 · 토큰 오류 처리(WARN-1 · 2 · 5 · 6) · §8 manifest 이름 · §9.3 실물 ① ~ ⑦ 결과 · 재확인 ⑧ ~ ⑪ · `STT_CONFIG_CHECK_SEC` 2초 확정 · OQ-003 · OQ-009 닫음 · OQ-002 는 WP6 실측으로 닫음 · OQ-010 일부 닫음 |
| 0.2.0 | 2026-10-26 | fix1 — 문서 리뷰(`review-doc-report.md`) FAIL 2 · WARN 6 반영: §4.4 `invalid_request` 판별 · 시점 · PCM · TTS(FAIL-1) · §7.3 「출력 중」을 「멈춤」 위로(FAIL-2) · 「시작 전」 상태와 「탭해서 통역 시작」 오버레이(WARN-1 · WARN-6) · `INTERPRET_BACK_PORT` 삭제 · `NEXT_PUBLIC_API_BASE_URL` 읽는 곳(WARN-2) · medikit 실재 이름(WARN-3) · 오류 때 외국어 영역 문구(WARN-4) · OQ-003 · 006 · 009 닫는 자리(WARN-5 — WORK-001) |
| 0.1.0 | 2026-10-26 | 첫 판 |

## 0. 근거 표기

- `D-nn` = DEC-001 의 결정. `입력 n` = BASE-001 의 사용자 원문.
- `원형` = cc-prototype `origin/main` 의 `procedure/back`(통역 · 로그인) · `_archive/cc/front/lib/interpret.ts`(브라우저 오디오).
- `기본값` = DEC 가 SPEC 에 맡긴 자리, 또는 원형을 그대로 가져온 자리에 이 문서가 정한 값. 사용자 결정이 아니다 — 바꾸려면 이 문서를 고친다.
- `OQ-nnn` = 근거로 닫지 못해 §10 에 남긴 것.
- 0.4.0 — 0.3.0 의 §4.3(조립) · §4.4(한도) · §4.4.1(거절) · §4.6(메뉴)은 **§4.5 · §4.6 · §4.6.1 · §4.7** 로 옮겼다. 다른 절의 참조는 새 번호다.

## 1. 범위 — D-01 · D-02 · DEC Scope · D-41 · D-42

| In | Out(DEC Scope Out) |
|---|---|
| 로그인(계정 하나) · 통역 화면(양방향 실시간 · 자막 · TTS) · 듣기 방식 전환(자동 듣기 · 누르고 말하기 — D-36) · 용어집 context · **통역 기록 — 서버에만(D-41 · §5.9)** · PWA · 로컬 실행 · Mac Studio 배포 | 통역 기록을 보는 화면 · API(D-41 「내부 검토용」) · 여러 계정 · 권한 · 자동 언어 맞추기(DEC Option B) · ccc(cc-prototype) 변경 |

- **0.6.0 — 통역 기록은 back 의 볼륨(PVC)에만 남긴다**(D-41 · §5.9): 세션 언어 · 시작/끝 시각 · 확정 발화의 원문 · 번역 · 말한 쪽 · 걸린 term id · 날짜별 JSONL · 7일 뒤 삭제(0.7.0 에서 바뀜 — 아래) · 음성 없음. 화면 · API 로는 내지 않는다(§3.5 허용 경로 6개 그대로) — 꺼내는 건 코디가 클러스터에서(§9.6). front 는 지금처럼 화면을 떠나면 지운다. (0.5.0 까지의 「어디에도 저장하지 않는다」는 D-41 로 바뀌었다.)
- **0.7.0 — 베타 테스트 기간에는 기록을 지우지 않는다**(D-42 · §5.9 「보관 기간」): 보관 기간은 env `INTERPRET_RECORD_KEEP_DAYS` · **비어 있으면 삭제 안 함**(운영 기본 — ConfigMap 에 넣지 않는다 · §9.6). 베타가 끝나면 코드 수정 없이 값만 넣어 다시 켠다. D-41 의 나머지는 그대로다.
- **0.8.0 — 품질 개선(D-43 ~ D-48)**: STT 모델 v6(§5.10) · 역할 context(§4.5 `text`) · 빈 원문 막기(§5.11) · 사전 전체 보정(§4.2.4 — 값은 조사 뒤) · 완료 조건 = 품질 시험(§9.3 「6차」). 범위 표(In · Out)는 바뀌지 않는다 — front · 화면 · API · 기록 줄 모양 그대로. LLM 번역으로 바꾸기 · 다른 STT 회사 비교 같은 것은 DEC 에 없다(하지 않는다).
- **0.9.0 — 품질 개선 2루프(D-55 ~ D-59)**: 언어별 한도를 v6 실측으로 올리고(§4.6 · D-56) · **번역 뒤 시술명 바로잡기**(§5.12 · D-58 — 사전 이름이 반드시 나가게)를 더하고 · 품질 시험을 **나라별**(7개 언어 × 직원 쪽 · 손님 쪽 · 최종 버전만 — §9.3 「7차」 · D-57 · D-59)로 넓힌다. 끊김 값은 1000 그대로(D-55). 범위 표(In · Out)는 바뀌지 않는다 — front · 화면 · API · WS 메시지 모양 그대로 · 기록 발화 줄에 키 하나(`fixed` · §5.9)가 는다.
- **0.9.2 — 배포 전 동기화(D-60 ~ D-64)**: 사전 `name` 을 그 나라 글자로 한 번 더 고치고(§4.2.6 · D-61 · 시드 `.9`) · 7차에서 나온 틀린 꼴을 더하고(§4.2.7 · 시드 `.10`) · 바로잡기를 한 군데 좁히고(② — D-63) 한 군데 넓혔다(④ 가까운 한글 낱말 — D-64). 7차 결과는 §9.3. 범위 표(In · Out)는 바뀌지 않는다.
- **0.9.3 — 배포 전 마지막(D-65 · D-66)**: 외 → 한 「가까운 한글 낱말」(§5.12 ④)을 배포 전 코드 검수대로 좁혔다 — 멀쩡한 한국어 낱말 · 조사를 건드리지 않는 쪽으로. 7차 기계 pass 는 153 → 152(§9.3). 범위 표는 바뀌지 않는다.
- **용어집 메뉴(읽기 전용)는 0.5.0 에서 뺐다**(D-37 — D-13 뒤집음). 용어집(시드)은 back 안에서 Soniox `context` 로만 쓰고 화면 · 응답에 나가지 않는다(§3.5 · §4.7).

## 2. 구성 · 실행 — D-01 · D-02 · D-06 · D-11 · D-12

### 2.1 폴더

```text
interpret-pwa/                 # 레포 루트 (D-01)
├── docker-compose.yml         # back + front 한 줄 실행
├── .env.example               # 이름만 (D-11). 실제 값은 사용자가 .env 에 (gitignore)
├── back/                      # FastAPI · uv (D-02)
│   ├── pyproject.toml · uv.lock · Dockerfile   # Dockerfile 이 seed/ 를 이미지에 복사 (0.4.0)
│   ├── seed/glossary.json     # 용어집 정본 — 우리 시드(D-33 · §4.2). PR 로 고친다 · 0.6.0 판 `2026-10-27.6`(§4.2.2 · §4.2.3)
│   ├── scripts/               # import_glossary.py(첫 가져오기 · 한 번 · §4.8) · live_check.py(실물 확인 · §9.3)
│   ├── app/
│   │   ├── main.py · config.py · container.py
│   │   ├── api/               # router — auth.py(login · me · config · demo) · health.py · interpret.py (0.5.0 — glossary.py 삭제 · D-37)
│   │   ├── service/           # auth.py · glossary.py(시드 로더 · 검사 · context — 메뉴 행 없음) · interpret/{session,soniox,assembler,chinese,langs}.py · records.py(통역 기록 · 걸린 term · 보관 기간 삭제 — 0.6.0 · 0.7.0 env · §5.9)
│   │   ├── domain/            # errors.py (DomainError)
│   │   └── schemas/           # front 계약(pydantic) — auth.py · health.py
│   └── tests/                 # 0.6.0 — test_records.py(§9.1 「기록」)
└── front/                     # Next.js PWA (D-02)
    ├── package.json · tailwind.config.ts · Dockerfile
    ├── .env.example           # NEXT_PUBLIC_API_BASE_URL 이름만 — 개발은 .env.local(gitignore) (0.2.0)
    ├── app/                   # login/ · (main)/ 통역 화면 · manifest
    ├── components/ · lib/     # components/interpret/{InterpretScreen,StartOverlay,Circle,ModeToggle,CaptionArea,LangSelect,HeaderMenu}.tsx · lib/{interpret,halfDuplex,output,view,scroll,start,ptt,prefs,langs,phrases,session,api}.ts (0.5.0 — GlossaryModal · lib/glossary 삭제)
    └── public/                # 아이콘 · 서비스 워커
```

- back 은 원형과 같은 계층(router → service, 아래층은 HTTP 를 모르고 `DomainError` 만 던진다 · 원형 `domain/errors.py`). DB 는 없다 — 계정은 env, 용어집은 **시드 파일을 읽은 메모리**(§3 · §4 · D-33 「DB · 편집 화면은 두지 않는다」), 통역 기록은 **볼륨의 JSONL 파일**(§5.9 · D-41 — DB 아님 · 읽는 코드 없음).
- 통역 4파일(`session.py` · `soniox.py` · `assembler.py` · `chinese.py`)과 `tests/test_interpret.py` 는 원형 `origin/main:procedure/back` 에서 **복사**하고 §5 의 자리만 고친다. cc-prototype 을 import 하지 않는다.
- front 는 원형 `procedure/front` 처럼 `@medisolve-ai/medikit@1.4.0`(Tailwind preset · `@medisolve-ai/medikit/styles`) · `pretendard` · Next.js 16 · React 19 · Tailwind 3 (§7.8).

### 2.2 포트 — 기본값

| 무엇 | 포트 | 이유 |
|---|---|---|
| back | **8800** | cc-prototype 8600(1차) · 8700(procedure · 2026-10-26 사용자 맥에서 LISTEN 중)과 겹치지 않게 |
| front | **3800** | 같은 이유 — 3600 · 3700 다음 |

- 포트는 **env 로 바꾸지 않는다(고정)**. back 8800 을 쓰는 곳 = `back/Dockerfile` CMD(`uvicorn … --port 8800`) · compose `ports: "8800:8800"` · 개발 명령(§2.3). front 3800 을 쓰는 곳 = `package.json` 의 `next dev -p 3800` · `next start -p 3800` · compose `ports: "3800:3800"`. (0.2.0 — WARN-2)
- 워커는 사용자 포트(3600 · 8600 · 3700 · 8700)에 떠 있는 프로세스를 건드리지 않는다.

### 2.3 실행

- 로컬 한 줄: 레포 루트에서 `docker compose up --build` → back `http://localhost:8800` · front `http://localhost:3800`.
- 개발: `cd back && uv run uvicorn app.main:app --port 8800 --reload` · `cd front && npm run dev`.
- compose: back 은 `env_file: .env`(없어도 뜬다 — `required: false`), front 는 `NEXT_PUBLIC_API_BASE_URL` 을 **build.args** 로 받는다(번들에 박히는 값 — 원형 `procedure/docker-compose.yml` 과 같음).
- **`NEXT_PUBLIC_API_BASE_URL` 을 읽는 곳(0.2.0 — WARN-2)**: 개발 = `front/.env.local`(gitignore · 예시는 `front/.env.example` 에 이름만) · compose = `build.args: NEXT_PUBLIC_API_BASE_URL: ${NEXT_PUBLIC_API_BASE_URL:-http://localhost:8800}` — compose 가 레포 루트 `.env` 로 **치환**한다(`env_file` 이 아니다) · front `Dockerfile` 은 `ARG` → `ENV` 로 받아 `npm run build`. 그 밖에서는 읽지 않는다.

### 2.4 env — 이름만 (D-06 · D-11)

`.env.example`(레포 루트)에 아래 **이름만** 둔다(`NEXT_PUBLIC_API_BASE_URL` 은 루트 `.env.example`(compose 치환용) · `front/.env.example`(개발용) 두 곳 — §2.3). 값은 사용자가 `.env` 에 넣는다. back 은 레포 루트 `.env` → `back/.env` 순으로 읽고(뒤가 앞을 덮음 · 실제 환경변수가 우선 · 원형 `config.py` 방식), 빈 값은 기본값.

| 이름 | 쓰는 곳 | 비면 | 근거 |
|---|---|---|---|
| `SONIOX_API_KEY` | back — Soniox STT · TTS `Authorization` 헤더 | 통역 `error no_api_key` (§5.4) | D-03 · 원형 |
| `INTERPRET_LOGIN_ID` | back — 로그인 아이디 대조 | 로그인 불가(모든 시도 401) · 기동 경고 1줄(§3.1) | D-06 |
| `INTERPRET_LOGIN_PASSWORD` | back — 로그인 비밀번호 대조 | 로그인 불가(모든 시도 401) · 기동 경고 1줄(§3.1) | D-06 |
| `INTERPRET_SESSION_SECRET` | back — 토큰 HMAC 서명 키 | 로그인 불가(401) — 서명 없는 토큰을 내지 않는다 · 기동 경고 1줄(§3.1) | 원형 `PROC_SESSION_SECRET` |
| `INTERPRET_SESSION_HOURS` | back — 토큰 유효 시간 | 12 | 원형 `PROC_SESSION_HOURS` 기본 12 |
| `INTERPRET_FRONT_ORIGIN` | back — CORS 허용 출처 · 통역 WS Origin 검사 | `http://localhost:3800` | 원형 `PROC_FRONT_ORIGIN` |
| `INTERPRET_DEMO_LOGIN` | back — 데모 원탭 로그인 스위치(§3.4). `true` · `1` = 켬 | `false`(꺼짐 — `POST /api/auth/demo` 404) | D-30 (0.4.0) |
| `INTERPRET_RECORD_DIR` | back — 통역 기록 JSONL 을 쓰는 폴더(§5.9 · 0.6.0). 운영 = PVC 마운트 아래 `/data/records`(ConfigMap · §9.6) | **기록 끔** — 파일 · 삭제 작업 없음 · 기동 로그 1줄 `interpret records: off`(로컬 · 시험 기본) | D-41 · 기본값 |
| `INTERPRET_RECORD_KEEP_DAYS` | back — 통역 기록 보관 기간(일 · §5.9 「보관 기간」 · 0.7.0). 양의 정수 N = 날짜가 오늘(한국 시간) − N 이하인 날짜 파일을 지운다(기동 1회 + 24시간마다) | **삭제 안 함** — 비어 있음 · 없음 · 공백만 모두 · 기동 때 삭제 0 · 24시간 배경 작업 없음 · 기동 로그 `keep_days=off`. 0 · 음수 · 숫자 아님도 경고 로그 1줄 뒤 삭제 안 함(기동은 멈추지 않는다). `INTERPRET_RECORD_DIR` 이 비었으면 이 값과 무관하게 기록 끔. **운영 ConfigMap · Secret 에는 넣지 않는다**(= 삭제 안 함 · §9.6) | D-42 · 기본값(잘못된 값 · 공백만 처리) |
| `GLOSSARY_CONTEXT_MAX_CHARS` | back — context 줄이기 기준(§4.6). **값이 있으면 7개 언어 모두를 그 값 하나로 덮는다**(언어별 표보다 작든 크든) | **언어별 표**(§4.6 — **0.9.0 · D-56**: en 24,892 · ja 21,962 · zh 22,551 · zh-Hant 22,685 · th 23,215 · vi 24,349 · yue 22,825 · `stt-rt-v6` · 시드 `.7` · 문안 포함 실측 통과 최대치 × 0.96 내림 / 0.6.1 ~ 0.8.4 는 v5 · 시드 `.6` × 0.9 — en 23,424 · ja 20,419 · zh 20,933 · zh-Hant 21,689 · th 21,343 · vi 22,891 · yue 21,123). **운영 ConfigMap · Secret 에는 넣지 않는다**(넣으면 언어별 표가 꺼진다) | **D-56**(0.9.0 — WP23 ⑬′ v6 실측) · WP16 코디 처분 3 2026-10-27 (0.6.1 — 0.4.1 의 단일 기본값 20251 을 고침) |
| `NEXT_PUBLIC_API_BASE_URL` | front 빌드 — 브라우저가 부르는 back 주소(http · ws 둘 다 여기서) · 읽는 곳은 §2.3 한 줄 | `http://localhost:8800` | 원형 |

- **`GLOSSARY_MATRIX_URL` 은 지운다(0.4.0 · D-33)** — back 은 Procedure Hub 를 부르지 않는다. matrix 주소는 가져오기 스크립트 상수 · `--url` 인자로만(§4.8). 시드 경로는 env 가 아니다(`back/seed/glossary.json` 고정 · §4.2).
- `.env.example` 은 이름만 — `INTERPRET_DEMO_LOGIN=` · `GLOSSARY_CONTEXT_MAX_CHARS=` · `INTERPRET_RECORD_DIR=`(0.6.0) 도 값을 비우고 주석에 기본값만(WP6-BE · 폰 피드백 2 방식). `GLOSSARY_CONTEXT_MAX_CHARS` 주석 = 「비면 언어별 표 · 넣으면 모든 언어를 그 값 하나로」(0.6.1).
- `INTERPRET_RECORD_DIR` 은 비밀값이 아니다(경로) — 운영은 ConfigMap(§9.6). 로컬에서 켜 보려면 **레포 밖 경로**(기록 파일에 대화 문장이 들어간다 — 레포 · 커밋에 들어가지 않게).
- **0.8.0 — 새 env 없음.** STT 모델 이름(§5.10) · context `text` 문안(§4.5) · 끊김 값(§5.10)은 코드 상수다(env 로 빼라는 결정이 없다). 품질 시험(§9.3 「6차」)의 조합 바꾸기는 시험 스크립트 인자로만 한다 — 운영 설정이 아니다.
- **0.9.0 — 새 env 없음.** 시술명 바로잡기(§5.12)는 늘 켜져 있고 env 로 끄지 못한다(끄는 길은 세션의 선택 인자 — 품질 시험 스크립트만) · 가까운 라틴 낱말의 기준 숫자(§5.12)는 코드 상수다. 언어별 한도(§4.6)는 코드 표 값만 바뀐다.
- 로그인 아이디 값(DEC D-06 의 사용자 지정 계정)도 **문서 · 코드 · 시험 · `.env.example` 에 쓰지 않는다** — 시험은 가짜 값을 주입한다.
- 로그에 키 · 비밀번호 · 토큰 · 쿼리 문자열(`?token=`)을 남기지 않는다(원형 — 접근 로그 쿼리 지움).
- `INTERPRET_FRONT_ORIGIN` 은 **정확히 같은 문자열**만 통과한다 — `http://127.0.0.1:3800` 으로 열면 CORS · WS(1008)가 막힌다. 로컬은 `localhost` 로 연다.

## 3. 로그인 — D-06 · D-07 · D-30

### 3.1 계정

- 계정은 **하나**. back 이 `INTERPRET_LOGIN_ID` · `INTERPRET_LOGIN_PASSWORD` 와 대조한다(D-06). DB · 해시 저장 없음.
- 비교는 상수 시간(`hmac.compare_digest`) — 아이디 · 비밀번호 둘 다 비교한 뒤 판정한다(어느 쪽이 틀렸는지 시간으로 드러나지 않게 · 원형의 「같은 401 · 같은 시간」 원칙).
- 5회 연속 실패 → 1분 잠금(429) · 성공하면 실패 수를 지운다 · 실패 수는 back 메모리(원형 `service/auth.py` `MAX_FAILS=5` · `LOCK_SEC=60` — 기본값). 계정이 하나라 잠금 단위는 back 전체.
- **로그인 env 가 빈 채로 기동(0.3.0 — 리뷰 WARN-5)**: `INTERPRET_LOGIN_ID` · `INTERPRET_LOGIN_PASSWORD` · `INTERPRET_SESSION_SECRET` 중 빈 것이 있으면 back 이 **기동 때 경고 로그 1줄** — 빈 env 의 **이름만**(값 · 길이 0). 응답은 바꾸지 않는다 — 로그인 시도는 같은 401 `invalid_credentials`(잠금 규칙도 그대로 — 실패 수를 센다). 화면에서 「설정이 빠졌다」를 드러내지 않는다(같은 401 원칙).

### 3.2 토큰

- 원형 형식 그대로: `INTERPRET_SESSION_SECRET` 으로 HMAC-SHA256 서명한 `{sub: <로그인 아이디>, exp}` · base64url · 만료 `INTERPRET_SESSION_HOURS`.
- 검증 = 서명 · 만료 + `sub` 가 **지금 env 의 아이디**와 같은가(env 를 바꾸면 기존 토큰은 401). 실패면 401 `unauthorized`.
- **망가진 토큰도 401(0.3.0 — 리뷰 WARN-2)**: ASCII 아닌 글자 · 점(`.`) 개수 · base64url · JSON 모양이 틀린 토큰은 예외(500)가 아니라 **같은 검증 실패**다 — HTTP 는 401 `unauthorized`(CORS 헤더 포함 — 오류 처리기를 거친다), WS 는 accept 전 close 1008(§5.2). 서명 비교는 bytes 끼리(`hmac.compare_digest`).
- front 는 토큰을 `localStorage`(키 `interpret.session` · `{token, expiresAt}`)에 둔다 — 원형 `lib/session.ts` 방식 · 기본값. 만료가 지났으면 읽을 때 지운다.

### 3.3 API

| 메서드 · 경로 | 요청 | 응답 200 | 오류 |
|---|---|---|---|
| `POST /api/auth/login` | `{id, password}` — 둘 다 필수(빠지거나 그 밖 필드 = 400 `invalid_request`) | `{token, expiresAt}` (`expiresAt` = ISO 8601) | 401 `invalid_credentials` 「아이디 또는 비밀번호가 맞지 않아요」 · 429 `too_many_attempts` 「로그인 실패가 많아요. 1분 뒤 다시 시도해 주세요」 |
| `GET /api/auth/me` | 헤더 `Authorization: Bearer <token>` | **`{ok: true}`**(0.5.0 · D-37 — 아이디를 내지 않는다. 토큰이 살아 있는지 확인용) | 401 `unauthorized` 「로그인이 필요해요」 |
| `GET /api/auth/config` (0.4.0 · D-30) | — | `{demoLogin: bool}` — `INTERPRET_DEMO_LOGIN` 값 그대로(계정 · 비밀번호 값은 내지 않는다) | — (인증 없음) |
| `POST /api/auth/demo` (0.4.0 · D-30) | 본문 없음 | `{token, expiresAt}` — `/api/auth/login` 과 같은 모양 · 같은 토큰(§3.2 · `sub` = env 아이디) | 404 `not_found` 「찾을 수 없어요」(스위치 꺼짐 — 경로가 없는 것과 같은 응답 · 0.5.0 문구) · 401 `invalid_credentials`(켜졌는데 로그인 env 3개 중 빈 것이 있음) |
| `GET /api/health` | — | **`{ok: true}`** 만(0.5.0 · D-37). 시드 판 · term 수는 back 기동 로그 `glossary seed loaded: …` 에만(§4.3). 0.4.x 의 `glossary{loaded, version, count}` 는 지웠다 | — (인증 없음) |

- 오류 본문은 원형 모양 `{"error": {"code", "message"}}`(원형 `main.py` 처리기). **문구는 일반 문구**(0.5.0 · D-37 — §3.5).
- **보호 대상**: `/api/auth/me` · `WS /api/interpret`. `/api/auth/login` · `/api/auth/config` · `/api/auth/demo` · `/api/health` 만 인증 없음. (0.5.0 — `/api/glossary` 삭제 · D-37)
- **로그아웃**: 서버 API 없음(토큰은 상태가 없다). front 가 ① 통역 WS 에 `stop` 을 보내고 닫고 ② `localStorage` 토큰을 지우고 ③ 로그인 화면으로. 토큰은 만료까지 서버에서 거둘 수 없다 — PoC 한계(§10 OQ-008).
- front 는 어느 API 든 401 을 받으면 토큰을 지우고 로그인 화면으로 보낸다. 통역 WS 가 핸드셰이크에서 거절되면(§5.2) `GET /api/auth/me` 로 401 인지 확인해 같은 처리.

### 3.4 데모 원탭 로그인 (0.4.0 — D-30)

| 항목 | 계약 |
|---|---|
| 스위치 | back env `INTERPRET_DEMO_LOGIN`(§2.4). 켜져 있을 때만 `POST /api/auth/demo` 가 비밀번호 없이 env 계정 토큰을 낸다. 꺼지면 404 — front 는 404 를 「데모 꺼짐」으로만 본다 |
| 잠금 | 데모 로그인은 §3.1 잠금 · 실패 수와 **무관**(검사하지도 바꾸지도 않는다). 비밀번호 로그인이 잠겨 있어도 데모는 200, 데모 뒤에도 잠금은 그대로 |
| 비밀값 | 비밀번호를 front 번들 · 응답에 넣지 않는다(D-06 · D-30). `config` 응답은 bool 하나 |
| 운영 | 운영 Secret 에 켜고, 데모가 끝나면 **값만 지우고 back 재시작**(D-30). 켜져 있는 동안은 주소만 알면 누구나 로그인된다 — 결정대로(PoC 데모) |
| front | 로그인 화면이 진입 때 `GET /api/auth/config` → `demoLogin: true` 면 입력 칸 없이 「로그인」 단추 하나(§7.1) |

### 3.5 밖으로 내는 것 — 최소 정보만 (0.5.0 — D-37)

> 「통역만 왔다 갔다」 — 용어집(시드) · 설정 이름 · 내부 사정을 응답 · WS · front 번들로 내지 않는다.

**허용 경로 — 정확히 6개**(그 밖 경로는 404 · 시험이 목록을 고정한다 — 새 경로는 DEC 와 함께 목록에 더한다)

| 경로 | 인증 | 응답 200 |
|---|---|---|
| `POST /api/auth/login` | 없음 | `{token, expiresAt}` |
| `GET /api/auth/me` | Bearer | `{ok: true}` |
| `GET /api/auth/config` | 없음 | `{demoLogin: bool}` |
| `POST /api/auth/demo` | 없음 | `{token, expiresAt}` (꺼지면 404) |
| `GET /api/health` | 없음 | `{ok: true}` |
| `WS /api/interpret` | `?token=` · Bearer | `ready` · `caption` · `audio_start` · PCM · `audio_end` · `error`(§5.3) |

| 항목 | 계약 |
|---|---|
| API 문서 | FastAPI `/docs` · `/redoc` · `/openapi.json` **끔**(`docs_url=None` · `redoc_url=None` · `openapi_url=None` → 404) |
| `/api/glossary` | **삭제**(404) — 메뉴 API(0.4.x §4.7) · 그 스키마 · `menu_rows` 삭제 |
| 통역 기록(0.6.0 · D-41) | **경로 없음** — 기록을 읽거나 내려받는 API · 화면을 두지 않는다(허용 경로는 위 6개 그대로 · 시험이 고정). 기록 파일 · 걸린 term id · 세션 id 는 응답 · WS · front 번들에 나가지 않는다. 꺼내기는 클러스터 안에서만(§9.6 kubectl) |
| 시드 | back 이미지 안에서 `context_for` → 세션 → Soniox STT 설정으로만 간다. 응답 · WS · front 번들에 시드 판 · 시드 낱말(ko · 별칭 · 현지명) 0(시험 · 빌드 산출물 grep — §9.1 · §9.2) |
| HTTP 오류 문구 | 검증 오류 400 `invalid_request` 「요청 형식이 맞지 않아요」(필드 경로 · 검증기 문구 없음) · 404 `not_found` 「찾을 수 없어요」 · 그 밖 HTTP 오류(405 등) `http_error` 「요청을 처리하지 못했어요」 · 처리기 밖 예외 = JSON 500 `internal` 「요청을 처리하지 못했어요」(원인 종류는 back 로그에만) |
| 사용자 문구는 그대로 | 로그인 401 「아이디 또는 비밀번호가 맞지 않아요」 · 429 「로그인 실패가 많아요. 1분 뒤 다시 시도해 주세요」 · 토큰 401 「로그인이 필요해요」 — 화면에 그대로 쓰는 문구라 둔다(설정 이름 · 내부 원인 없음) |
| WS 오류 문구 | §5.4 — 코드 + 일반 문구 4종 · 받은 값을 되돌려 보내지 않는다 |
| front | 설정 · env 이름이 든 문구를 쓰지 않는다 — back 주소가 비었을 때도 「서버에 연결하지 못했어요」. 서버 `message` 는 그대로 보여 준다 |

## 4. 용어집 — 우리 시드 파일 — D-33(D-05 · D-13 · D-14 개정) · D-17 · D-18 · D-19 · D-28 · D-32 · D-35 · D-37 · D-38 · D-39 · D-40 · D-45 · D-46 · D-51 · D-52 · D-53 · D-54 · D-56 · D-58 · D-60 · D-61 · D-62

> 0.4.0 — **용어집 정본은 레포의 시드 파일**이다(D-33). Procedure Hub matrix 는 **첫 가져오기 원천**일 뿐 back 이 런타임에 부르지 않는다.
> 0.5.0 — 시드에 **대만 현지명**을 넣었다(D-35 · §4.2.1) · **용어집 메뉴 API 를 지웠다**(D-37 · §4.7) — 시드는 Soniox `context` 로만 쓴다.
> 0.6.0 — 사전 밖 **새 시술 13개**를 7개 언어로 더하고(D-39 · §4.2.2) **대륙 중국어를 검증**했다(D-40 · §4.2.3). 내용 규칙을 언어 공통으로 다시 썼다(§4.2.1). 스키마 · 로더 · context 조립 · 줄이기 규칙은 그대로다(검사 7 하나만 더함).
> 0.8.0 — context 에 **서술 칸 `text`**(역할 · 방향 · D-45 · §4.5)를 더하고, **사전 전체 보정**(시드 `.7` · D-46)의 절차 · 규칙 · 자리를 둔다(§4.2.4 — **값은 조사 · 코디 처분 뒤 채운다**). 스키마 · 검사 · 로더 · 줄이기 순서는 그대로다.
> 0.9.0 — 시드에 **틀린 꼴** 필드 둘(entry `wrong` · term `ko_wrong` · D-58)을 더한다 — **바로잡기(§5.12)만 읽고 context 에는 들어가지 않는다**(§4.2 · 검사 8 · 첫 목록 §4.2.5 · 시드 `.8`). **언어별 한도 표를 v6 실측으로 바꾼다**(§4.6 · D-56). 이름 · 별칭 · 로더 · 조립 · 줄이기 순서는 그대로다.
> 0.9.2 — 시드가 두 판 더 나갔다: **`.9`**(§4.2.6 · D-61 — 그 나라 글자가 있는 언어의 영문 `name` 을 그 나라 글자로) · **`.10`**(§4.2.7 — 7차 틀린 꼴). 스키마 · 로더 · 조립 · 줄이기 순서 · 한도 표는 그대로다 — `.9` 부터 ja · th 는 `terms` 일부가 줄이기로 빠진다(§4.6 · D-62).
> 0.3.0 의 「기동 때 matrix 를 읽음 · 실패면 빈 용어집」(0.3.0 §4.1 · §4.2)은 **폐기**. 정방향 · 역방향 · 줄이기 · 2초 확인 · 재연결(0.3.0 §4.4 · §4.4.1 → 이 판 §4.6 · §4.6.1)은 그대로 두고 **짝을 만드는 재료만 시드로** 바꾼다.

### 4.1 무엇이 바뀌나

| 항목 | 0.3.0 | 0.4.0 | 근거 |
|---|---|---|---|
| 정본 | Procedure Hub matrix(stg) | **`back/seed/glossary.json`**(git · PR 로 고친다) | D-33 |
| 읽는 때 | back 기동 때 HTTP 1회 | back 기동 때 **파일** 1회 · 메모리에 둔다(다시 읽지 않는다 — 고치면 PR → 재배포 · 재시작) | D-33 · D-14 「기동 때 한 번 캐시」 |
| 모양 | 행 = ko × 6개 언어 문자열(괄호 병기 섞임) | **정규화** — 시술(term) × 언어별 표기(entry: 현지명 · 별칭[] · 출처 · 검수) | D-33 |
| 언어 | matrix `langs` 6개 · zh-Hant 는 zh 열을 빌림 | 시드 `langs` **7개**(en · ja · zh · zh-Hant · th · vi · yue) — zh-Hant 가 **자기 표기**를 갖는다 | D-28 · D-32 · D-33 |
| 실패 | 빈 용어집으로 뜸 | **기동 실패**(§4.4) — 시드는 우리 파일이라 시험으로 막는다 | 기본값(아래) · D-33 |
| Procedure Hub | 런타임 호출 | **런타임 호출 0** · 가져오기 스크립트(§4.8)만 부른다(한 번) | D-33 |

### 4.2 시드 파일 — 위치 · 스키마

- 경로 **`back/seed/glossary.json`** 하나(D-33). env 로 바꾸지 않는다. back 은 `config.py` 의 `BACK_DIR / "seed" / "glossary.json"` 로 찾는다. `back/Dockerfile` 이 `seed/` 를 이미지에 복사한다.
- 인코딩 UTF-8 · `json.dumps(ensure_ascii=False, indent=2)` + 끝 줄바꿈(가져오기 스크립트 출력 = 사람이 고친 뒤 모양 · diff 를 읽을 수 있게). 키 순서는 아래 표 순서.

**파일 머리**

| 필드 | 필수 | 타입 | 뜻 |
|---|---|---|---|
| `schema` | 필수 | 정수 `1` | 스키마 판. 다르면 기동 실패 |
| `version` | 필수 | 문자열 `YYYY-MM-DD.n` | 시드 판. **고칠 때마다 올린다**(PR 마다). back 기동 로그 · 통역 기록 세션 시작 줄(§5.9)에만 쓴다(0.5.0 — 응답에 내지 않음 · §3.5). 배포본 main 2a9d5a5 = `2026-10-27.5`(D-38) → **0.6.0 판 = `2026-10-27.6`**(§4.2.2 · §4.2.3 · 판 번호를 이어 간다) → **0.8.2 판 = `2026-11-14.7`**(§4.2.4 · D-46 · D-51 · D-52 — 날짜 = 조사 · 처분 날짜 · 번호 7 · 이 문서는 「시드 `.7`」 로 부른다) → **0.9.0 판 = `2026-11-15.8`**(§4.2.5 · D-58 — 틀린 꼴 첫 목록 · 「시드 `.8`」) → **0.9.2 판 = `2026-11-15.9`**(§4.2.6 · D-61) → **`2026-11-15.10`**(§4.2.7 · D-63 — 지금 판 · 「시드 `.10`」) |
| `langs` | 필수 | 문자열 배열 | 이 파일이 다루는 앱 lang — **정확히 7개** `["en","ja","zh","zh-Hant","th","vi","yue"]`(back `langs.py` `APP_LANGS` 와 같은 집합 · 순서 무관) |
| `imported_from` | 선택 | 객체 `{source, url, version, count, at}` | 첫 가져오기 기록(§4.8). 런타임은 읽기만 하고 쓰지 않는다 |
| `terms` | 필수 | 배열(1개 이상) | 시술. **배열 순서 = context 순서** |

**term(시술)**

| 필드 | 필수 | 타입 | 뜻 |
|---|---|---|---|
| `id` | 필수 | 문자열 `[a-z0-9-]+` | 바뀌지 않는 이름. 파일 안 유일. **붙이는 규칙**: 첫 가져오기 = `ph-001` ~ (matrix 순서) · **조사로 더한 Procedure Hub 밖 시술 = `kr-001` ~ (더한 순서 · 3자리 · 번호를 다시 쓰지 않는다 — 0.6.0 · D-39 · **0.8.2: `kr-014` 써마지 · `kr-015` 리투오** · 합쳐서 없앤 `id`(`ph-106` · `ph-127`)도 다시 쓰지 않는다 — §4.2.4)** · 손으로 더한 단발 = `m-<짧은 영문>`(지금 0개). 한 번 붙인 `id` 는 바꾸지 않는다 — 통역 기록의 걸린 term(§5.9)이 이 값을 남긴다 |
| `category` | 필수 | 문자열(비지 않음) | 카테고리 — 사람이 시드를 읽을 때 묶음(0.5.0 — 메뉴가 없어 런타임은 안 쓴다) |
| `ko` | 필수 | 문자열(비지 않음) | **ko 대표명** — 정방향 source · 역방향 target |
| `ko_aliases` | 선택 | 문자열 배열(기본 `[]`) | ko 별칭(예 상담사가 줄여 부르는 이름). 정방향 source 로만 쓴다 |
| `ko_wrong` | 선택 | 문자열 배열(기본 `[]`) | **(0.9.0 · D-58) ko 틀린 꼴** — 외 → 한 번역에서 이 시술이 ko 대표명 대신 나온 꼴(다른 한글 표기 · 그대로 남은 외국어 표기 · 다른 낱말). **바로잡기(§5.12)만 읽는다** — context(§4.5) · 걸린 term 판정(§5.9)의 재료가 아니다. 검사 8 |
| `entries` | 필수 | 객체 `{<lang>: entry}` | 언어별 표기. 키 ⊆ `langs`. **없는 언어는 그 언어 context 에서 이 시술이 빠진다**(전부 채울 필요 없음) |
| `note` | 선택 | 문자열 · null | 사람 메모(예 손 편집의 출처 — 「사용자 지적 2026-10-26 …」) · 런타임은 안 쓴다 (0.4.1 — backend 가 더함) |

**entry(언어별 표기)**

| 필드 | 필수 | 타입 | 뜻 |
|---|---|---|---|
| `name` | 필수 | 문자열(비지 않음 · **괄호 `(` `)` `（` `）` 0**) | **현지명** — 그 언어 손님이 부르는 이름. 정방향 target · 역방향 source · TTS 가 읽는 말 |
| `aliases` | 선택 | 문자열 배열(기본 `[]` · 괄호 0) | 그 언어의 다른 이름(영문 상표명 · 현지 별명 등). **역방향 source 로만** 쓴다 |
| `wrong` | 선택 | 문자열 배열(기본 `[]`) | **(0.9.0 · D-58) 그 언어 틀린 꼴** — 한 → 외 번역에서 이 시술이 `name` 대신 나온 꼴(영문 음역 · 다른 낱말 등 — 시험 · 기록에서 실제로 나온 것만 · 짓지 않는다). **바로잡기(§5.12)만 읽는다** — context · 걸린 term 판정의 재료가 아니고 TTS 로도 가지 않는다. 검사 8 |
| `source` | 필수 | `"procedure-hub"` · `"draft-s2twp"` · `"manual"` · **`"web-research YYYY-MM-DD"`**(0.5.0 · D-35 — 날짜 모양까지 검사 · `web-research` 만 · 날짜 모양이 틀리면 오류) 중 하나 | 출처 — 가져온 것 · zh-Hant 기계 초안(이름은 스키마 값 그대로 — 변환은 §4.8) · 사람이 쓴 것 · 웹 조사로 넣은 것(조사 날짜). **0.6.0**: 조사 리포트로 정한 값(찾은 현지명이든, 조사로 「현지에 없음」을 확인해 영문으로 둔 것이든) = `web-research 2026-10-27` · 조사 없이 규칙으로만 고친 데이터 결함(§4.2.3 C) = `manual` |
| `reviewed` | 필수 | bool | 검수 여부. `false` = 사람이 아직 안 본 초안 · 출처가 하나뿐인 조사값(§4.2.1). context 에는 **그대로 넣는다**(검수 여부로 빼지 않는다 — 기본값 · D-33 은 초안을 넣고 사용자가 고친다고 했다). 0.5.0 — 메뉴가 없어 화면에 보이지 않는다 · 검수 목록은 시드 파일에서 `reviewed:false` 로 찾는다 |
| `raw` | 선택 | 문자열 · null | 가져오기 때 원문(괄호 분해 전) — 분해가 원문과 다를 때만. 검수용 · 런타임은 안 쓴다 |
| `note` | 선택 | 문자열 · null | 사람 메모 · 런타임은 안 쓴다. `web-research` entry 는 대표 출처 URL 1개(D-35) — 0.6.0 · 「현지에 없음 = 영문」 entry 는 URL 대신 `현지 출처 없음 — <리포트 파일 이름>`(근거가 부재라 가리킬 URL 이 없다) |

예(값은 2026-10-27 matrix 를 §4.8 규칙으로 바꾼 모양 — 실제 파일은 스크립트가 만든다 · 0.9.0 의 `ko_wrong` · `wrong` 은 이 예에 없다 — 키 자리는 위 표 순서: `ko_aliases` 다음 `ko_wrong` · `aliases` 다음 `wrong`):

```json
{
  "schema": 1,
  "version": "2026-10-27.1",
  "langs": ["en", "ja", "zh", "zh-Hant", "th", "vi", "yue"],
  "imported_from": {"source": "procedure-hub", "url": "https://stg-procedure-hub.medisolveai.com/api/v1/glossary/matrix",
                    "version": "2026-07-01-reviewed-v5", "count": 158, "at": "2026-10-27"},
  "terms": [
    {
      "id": "ph-0NN",
      "category": "기기 리프팅",
      "ko": "써마지FLX",
      "ko_aliases": [],
      "entries": {
        "zh": {"name": "美版热玛吉FLX", "aliases": ["Thermage FLX"], "source": "procedure-hub", "reviewed": true,
               "raw": "Thermage FLX（美版热玛吉FLX）"},
        "zh-Hant": {"name": "美版熱瑪吉FLX", "aliases": ["Thermage FLX"], "source": "draft-s2twp", "reviewed": false},
        "ja": {"name": "サーマクールFLX", "aliases": ["Thermage FLX"], "source": "procedure-hub", "reviewed": true,
               "raw": "サーマクールFLX（Thermage FLX）"}
      }
    }
  ]
}
```

**검사(로더 · 시험 둘 다 같은 함수)** — 하나라도 어기면 오류(§4.4):

1. JSON 파싱 · 머리 필드 · 타입 · `schema == 1` · `version` 모양 · `langs` 가 `APP_LANGS` 와 같은 집합
2. term: 필수 필드 · 타입 · `id` 모양 · **`id` 유일**
3. **ko 쪽 유일**: 모든 term 의 `ko` ∪ `ko_aliases` 를 모아 겹침 0(앞뒤 공백 뺀 값 기준) — 정방향 source 가 둘이면 Soniox 에서 어느 쪽이 이길지 모른다(0.3.0 §4.2 와 같은 이유 · 이제 「처음 것」으로 덮지 않고 파일에서 막는다)
4. entry: 키 ∈ `langs` · `name` 비지 않음 · `name` · `aliases` 에 괄호 0 · `source` 값 · `reviewed` bool · 한 entry 안에서 `name` · `aliases` 겹침 0
5. 문자열은 앞뒤 공백 없음 · 줄바꿈 없음
6. **알 수 없는 필드는 오류**(규칙 이름 `unknown_field` · 머리 · term · entry 모두) — `ko_alias` 같은 오타가 조용히 무시되지 않게 (0.4.1 — backend 가 더함)
7. **보이지 않는 글자 0**(0.6.0 · 규칙 이름 `invisible_char`) — 모든 문자열(`ko` · `ko_aliases` · `name` · `aliases`)에 유니코드 범주 `Cf`(U+200B ~ U+200D · U+2060 · U+FEFF 등) 0. 배포 시드 `.5` 의 ph-042 zh 「白毒」 뒤에 U+200C 가 붙어 있었다(가져오기 원문 그대로) — 화면에 안 보이는 글자가 짝을 다른 말로 만든다. `.6` 에서 지운다(§4.2.3)

8. **틀린 꼴(0.9.0 · D-58 · 규칙 이름 `wrong_form`)** — `ko_wrong` · `wrong` 의 문자열마다: ⓐ 5 · 7 을 그대로 건다(비지 않음 · 앞뒤 공백 · 줄바꿈 · 보이지 않는 글자 0). **괄호 금지는 걸지 않는다**(번역에 나온 꼴 그대로 적는다) ⓑ **공백을 뺀 글자 수 2 이상**(한 글자는 다른 낱말 안에 너무 쉽게 걸린다 — 기본값) ⓒ 한 목록 안 겹침 0 ⓓ **자기의 맞는 이름과 겹침 0** — `wrong` 은 그 entry 의 `name` · `aliases` 와, `ko_wrong` 은 그 term 의 `ko` · `ko_aliases` 와 같지 않다 ⓔ **다른 term 의 맞는 이름과 겹침 0** — `entries[L].wrong` 은 **어느 term 이든** `entries[L].name` · `aliases` 와, `ko_wrong` 은 어느 term 이든 `ko` · `ko_aliases` 와 같지 않다(한 발화에 시술이 둘일 때, 맞게 나온 옆 시술 이름을 덮어쓰지 않게). 「같다」 = §5.9 정규화(`L ∈ {zh-Hant, yue}` 면 `t2s` → `casefold` · ko 쪽은 `casefold` 만) 뒤 · ASCII 뿐인 꼴은 연속 공백을 하나로 · 그 밖은 공백을 모두 지우고 견준다. 다른 term 끼리 **같은 틀린 꼴**을 갖는 것은 허용한다(어느 term 으로 바꿀지는 원문에 걸린 term 이 정한다 — §5.12)

- **`schema` 는 1 그대로다(0.9.0)** — 새 필드 둘은 선택(없으면 `[]`)이라 `.7` 까지의 시드도 그대로 통과한다. 다만 **0.8.x 코드는 `.8` 시드를 `unknown_field`(검사 6)로 거절한다** — 코드와 시드를 같은 PR 로 낸다(WP26).
- 오류 = `SeedError(rule, where, term_id)` — 로그 1줄 예 `glossary seed invalid: id_duplicate at $.terms[1].id (id=ph-001) — 기동을 멈춘다`.
- term `ko` 에는 괄호 금지를 걸지 않는다(예 「피코초(Picosecond)」 — ko 는 정방향 source 일 뿐 TTS 로 가지 않는다).

- 다른 시술끼리 **같은 현지명**(역방향 source 가 겹침 — 2026-10-26 matrix 기준 en 2 · ja 1 · zh 2 · th 1 · yue 2)은 **허용**한다 — 실제로 같은 이름을 쓰는 시술이 있다. 역방향에서는 처음 짝만 둔다(§4.5 · 0.3.0 규칙 그대로).

### 4.2.1 시드 내용 규칙 — 7개 언어 공통 (0.6.0 — D-35 · D-38 · D-39 · D-40 을 하나로)

> 시드 값은 **우리가 짓지 않는다**(D-32 · D-33 · D-35) — 현지 클리닉 · 의료미용 플랫폼 · 허가 기관 · 현지 총판 표기를 조사 리포트(URL)로 가져온다.
> 아래 규칙은 언어마다 따로 있던 결정(D-35 대만 · D-38 대만 2차 · D-40 대륙)을 **7개 언어 공통**으로 묶은 것이다. 시드를 더 고칠 때도 같은 규칙이고, 규칙 밖 판단(어느 이름을 name 으로 할지 갈리는 것)은 코디 처분으로 정해 §4.2.2 · §4.2.3 표에 적는다.

| # | 규칙 | 근거 |
|---|---|---|
| R1 | **현지 허가명 · 공식명이 먼저.** 그 나라 허가 기관 · 브랜드 현지 공식명이 있으면 `name`. 업계 통칭 · 옛 표기 · 수출명 · 색 별명은 `aliases`. **대륙(zh) = NMPA 허가명 · 브랜드의 대륙 공식명**(예 리즈톡스 解索橙 · 써마지FLX 超玛吉FLX · 리쥬란 丽驻兰). 대만(zh-Hant) = 衛福部 허가명(예 레티보 · 보툴렉스 保提拉 · 뉴라미스 優美施). 허가명과 클리닉 메뉴 표기가 갈리면 처분을 따른다(예 프로파일로 zh-Hant = 클리닉 표기 逆時針 · 허가명 璞菲洛 는 alias) | D-38 ① · D-40 · 처분 r1-1 · r2-1 · r2-2 |
| R2 | **현지에 없음 = 영문(언어 공통).** 그 나라 클리닉 · 플랫폼 · 허가 목록에서 이 제품 이름을 찾지 못하면(미허가 · 미판매 · 한국 전용 제품) `name` = **영문 표기** — 새 시술은 §4.2.2 「영문」 칸, 기존 시술은 그 term 의 `en` `name`. `reviewed: false` · `note` = `현지 출처 없음 — <리포트>`. 지금 표기(음역 · 직역 · 색 별명)는 R3 대로 `aliases` | D-38 ② · D-40 · 처분 r1-2 · r1-3 · r1-5 · r2-3 · r3 |
| R2′ | **현지 메뉴가 영문인 나라는 영문이 곧 현지명.** 태국(th) · 베트남(vi) 클리닉 메뉴는 새 시술을 영문 브랜드명 그대로 쓴다 → `name` = 영문 표기이고, 현지 출처가 있으면 R7 로 `reviewed` 를 판단한다(R2 의 「없음」과 다르다). 현지 문자 음역(태국 문자 등)은 **현지 출처에서 본 것만** `aliases`(지금 4개 — §4.2.2) | 처분 r3 · 조사 r3 §0 |
| R3 | **옛 표기는 `aliases` 로 내린다** — name 을 바꿀 때 지금 name · aliases 는 alias 로 남긴다(손님이 그 이름으로 말할 수 있다). **예외**: R4 모호어 · 뜻이 없거나 잘린 결함 값(§4.2.3 C)은 남기지 않고 지운다 | D-35 「초안은 aliases」 · D-40 「지금 표기는 alias」 |
| R4 | **모호어는 넣지 않는다**(`name` · `aliases` 둘 다) — 한 시술로 확정되지 않는 말(장르 이름 · 브랜드 전체 · 일반 단어). 목록은 아래 「모호어 목록」 · 시험이 막는다(§9.1). 한 기기로 확정되는 구어는 alias 로 넣을 수 있다(D-35 — 예 精靈針 = AestheFill) | D-35 · D-38 ④ · D-40 · 처분 r1-6 · r2-8 |
| R5 | **alias 로 넣지 않는 꼴**(0.6.0 · 기본값 — 짝 수 · 글자 수만 늘고 새 이름이 아니다): ① 대소문자만 다른 표기(`EXION` 과 `Exion`) ② 묘사 꼬리를 붙인 표기(`…療程` · `…護理` · `…治療` · `…腋下多汗治療`) ③ 이름과 영문을 붙여 쓴 꼴(`miraDry清新微波` · `Thermage CPT電波拉皮`) ④ 제조사 · 회사 이름을 앞에 붙인 꼴(`BTL EMFACE` · `索塔素颜光`) ⑤ `t2s` 뒤 name 과 같아지는 표기(zh-Hant · yue — `無双電波` 와 `無雙電波`). 현지 문자 entry 의 영문 alias 는 **영문 표기 하나**(§4.2.2 「영문」 칸 그대로) | 기본값 · 조사 r2 · r3 표기 변형 |
| R6 | **홍콩(yue)은 대만(zh-Hant)과 독립.** yue 값을 zh-Hant 에서 복사하지 않는다 — 홍콩 클리닉 표기를 따로 조사한다(새 시술 13개 중 대만과 다른 것 9개 — §4.2.2). 둘 다 context 에서는 `t2s` 를 거친다(§4.5). 레이저는 홍콩 `激光` · 대만 `雷射`(§5.6) | 처분 r3 · 조사 r3 「yue 를 대만 값에서 복사하지 말 것」 |
| R7 | **`reviewed: true` = 독립 현지 출처 2개 이상**(서로 다른 도메인). 셈에서 빼는 것: 제조사 본사 · 한국 클리닉 · 플랫폼의 외국어 페이지 · **같은 클리닉 체인의 여러 도메인은 하나**(0.6.0 기본값). 현지 총판 · 현지 법인 · 허가 기관 · 현지 매체는 센다. 하나뿐이거나 R2 「없음」이면 `false` | D-35 · D-38 · 처분 「출처 2+ 만 reviewed」 |
| R8 | **`ko` 대표명 = 한국 클리닉 표기**(새 시술은 조사 r1 §0 목록 — 코디 확정) | D-39 |
| R9 | 괄호 · 보이지 않는 글자 0(§4.2 검사 4 · 7) — 조사 표기에 붙은 주석 괄호는 뺀다 | D-35 |

**모호어 목록**(R4 · 0.6.0 — 그 자리의 문자열과 **정확히 같으면** 시험 실패. 비교: zh · zh-Hant · yue 는 양쪽을 `t2s` 한 뒤 · 라틴은 `casefold` 뒤)

| 언어 | 모호어 | 금지 자리 | 왜 |
|---|---|---|---|
| zh · zh-Hant | `热玛吉`(브랜드 전체 — 4세대 CPT · 5세대 FLX · **0.8.2 — `kr-014` 「써마지」 의 zh `name` 만 예외**(D-51) · zh-Hant `熱瑪吉` 는 예외 없음) · `黄金微针`(射频微针 장르) · `童颜针`(PLLA · PDLLA 장르) · `素颜` · `素妍` · `凤凰` · `仙女` · `彩虹针` | **name · alias** | D-38 ④ · D-40 · 처분 r1-6 · 조사 r1 표 C · r2 표 C |
| zh · zh-Hant | `超声刀` · `韩版超声刀` · `韩版热玛吉` | **alias**(0.5.0 그대로) — 0.6.1: zh name 으로 남았던 ph-123 「韩版热玛吉」 · ph-126 「韩版超声刀」 도 영문으로 바꿔(§4.2.3 D · OQ-018 ①) **name · alias 모두 0** | D-35 · OQ-018 처분 ① |
| yue | `黃金微針`(홍콩은 Exion · 대만은 바늘 종류) · `童顏針` · `膠原槍` · `韓國仙女針` · `舒膚微`(출처 1 · 다른 음역) | **name · alias** | 조사 r3 표 C |
| yue | `水光針`(스킨부스터 공통 꼬리) | **alias** — ph-074 · ph-078 의 name 「水光針」 은 물광 시술 자체 이름이라 그대로 | 조사 r3 표 C-4 |
| ja | `サーマクール`(단독 — CPT · FLX · アイ · **0.8.2 — `kr-014` 의 ja `name` 만 예외**(D-51)) | **name · alias** | 조사 r2 표 C-1 |
| th · yue | **(0.8.2)** `เทอร์มาจ`(th) · `熱瑪吉`(yue) — `kr-014` 의 `name` | **`kr-014` 밖 term 의 name · alias** | D-51 — 세대 없는 이름은 일반 term 하나에만(역방향 짝이 FLX · CPT 로 가지 않게) |
| en · th · vi | `Thermage`(단독) · `Density` · `Revive` · `Tesla`(일반 단어 · 다른 회사) | **alias** — 덴서티의 `name` `DENSITY` 는 브랜드라 둔다(OQ-019) · **0.8.2 — `Thermage` 는 `kr-014` 의 en · zh-Hant · vi `name`**(D-51 — alias 금지는 그대로) | 처분 r2-8 · 조사 r2 표 C-4 ~ C-7 |

- 시험(§9.1 「시드」 ⑥)은 위 표를 그대로 상수로 갖는다. 표에 없는 말을 시험이 스스로 늘리지 않는다 — 늘리려면 이 표를 고친다.
- 기존 시드의 `水光`(ph-089 물광) · `水光针`(ph-074 · ph-078)은 그 시술의 현지 이름(물광 = 水光)이라 R4 대상이 아니다.
- `.5` 기준 이 표에 걸리는 값 = zh ph-130 alias `热玛吉` · zh-Hant ph-130 alias `熱瑪吉` · zh ph-135 name `黄金微针` — 셋 다 `.6` 에서 지운다(§4.2.3 A). 그 밖은 0(확인 2026-10-27 · `.5` 대조).

**지금까지 반영한 판**

| 판 | 결정 | 무엇 | 수치 |
|---|---|---|---|
| `.4` | D-35 | zh-Hant 대만 현지명(조사 77/157) · 초안은 alias · 「鐳射」 → 「雷射」 · zh 「热玛吉」 alias(**0.6.0 에서 뺌**) · 볼뉴머 카테고리 기기 리프팅 | `web-research` 77 · `reviewed:true` 38 |
| `.5` | D-38 | zh-Hant 2차(대만 클리닉 3곳 전수 대조 · 40 term) — 톡신 대만 허가명(保提拉 · 優力柔 · 娜柏塔) · **대만에 없는 한국 전용 제품 19개 = 영문 name**(`manual` · `reviewed:false` — 이 판은 「현지에 없음」도 `manual` 로 적었다) · 대륙식 · `s2twp` 오변환 정리 · 모호어 제거 · 포텐자 zh-Hant 無限電波(검수 전) | 배포 main 2a9d5a5(PR #9) · infra #34 — 0.6.0 에서 뒤늦게 기록 |
| **`.6`** | **D-39 · D-40** | **새 시술 13 term × 7개 언어**(§4.2.2) · **기존 표기 변경**(§4.2.3) · 검사 7 | §4.2.2 · §4.2.3 표 그대로 |
| `.7`(WP23 예정) | D-46 · D-51 · D-52 · D-53 · D-54 | 사전 전체 보정 — 7개 언어 × 그 나라 클리닉 공식 사이트 · 1,190칸 조사 + 처분(§4.2.4) · 새 term 2(`kr-014` · `kr-015`) · 합침 2쌍 · zh-Hant 별칭 정리(D-53 — r3 판정 파일) | 계산(§4.2.4 ③ · 0.8.3): 바뀌는 칸 343 / 1,176(D-53 적용 전 · 적용 뒤 393) · `name` 199 · 별칭 낱개 507 → 753(D-53 적용 전) → 673(적용 뒤) · term 170 그대로 |

### 4.2.2 새 시술 13개 — `kr-001` ~ `kr-013` (0.6.0 — D-39)

대상 = 조사 r1 §0 의 N01 ~ N14 에서 **N13 울트라셰이프를 뺀 13개**(처분 r2-7). 사전에 이미 있는 쥬베룩(ph-108) · 스컬트라(ph-112)는 새 term 이 아니다(§4.2.3). `id` 는 아래 순서로 `kr-001` ~ `kr-013`(N14 → `kr-013`). **시드 배열 맨 뒤에 이 순서로** 붙인다(배열 순서 = context 순서 · §4.5 — 기존 157 term 의 순서는 그대로).

| id | N | `ko` | `category` | 영문 표기(R2 · R5) |
|---|---|---|---|---|
| `kr-001` | N01 | 써마지 CPT | 기기 리프팅 | `Thermage CPT` |
| `kr-002` | N02 | 소프웨이브 | 기기 리프팅 | `Sofwave` |
| `kr-003` | N03 | 엑시온 | 기기 리프팅 | `EXION` |
| `kr-004` | N04 | 덴서티 | 기기 리프팅 | `DENSITY` |
| `kr-005` | N05 | 엠페이스 | HIFES/EMS | `EMFACE` |
| `kr-006` | N06 | 클리어앤브릴리언트 | 레이저 | `Clear + Brilliant` |
| `kr-007` | N07 | 프로파일로 | 스킨부스터 | `Profhilo` |
| `kr-008` | N08 | 뉴라미스 | 필러 | `Neuramis` |
| `kr-009` | N09 | 벨로테로 리바이브 | 스킨부스터 | `Belotero Revive` |
| `kr-010` | N10 | 에스테필 | 바이오스티뮬레이터/콜라겐부스터 | `AestheFill` |
| `kr-011` | N11 | 하이드라페이셜 | 메디컬스킨케어 | `HydraFacial`(처분 r2-5) |
| `kr-012` | N12 | 미라드라이 | 기기(다한증) | `miraDry` |
| `kr-013` | N14 | 텐서(테슬라포머) | HIFES/EMS | `TeslaFormer`(처분 r2-6) |

- `ko_aliases` 는 모두 `[]`(조사가 한국어 별칭을 다루지 않았다). 0.6.1 — 「써마지」 단독은 **어느 term 의 ko 별칭도 아니다**(ph-130 에서 지움 · §4.2.3 D · OQ-018 ⑤ 뒤집음) → 시드 전체 ko 별칭 0개.
- `category` 는 사람이 읽는 묶음(런타임 안 씀) — 가까운 기존 카테고리, 없으면 조사 r1 §0 표기(「기기(다한증)」).
- 영문 표기는 조사 r2 표 2-2 제조사 표기 + 처분(r2-5 · r2-6). 대문자 표기(EXION · DENSITY · EMFACE)를 TTS 가 어떻게 읽는지는 실물 ⑳ 에서 기록한다(OQ-019).

**언어별 entry** — 칸 = `name` · `aliases`(가운데점 뒤 · 순서대로) · `reviewed`(✓ = true · ✗ = false). 모든 entry `source: "web-research 2026-10-27"` · `note` = 대표 출처 URL 1개(리포트 그 칸의 첫 URL — 열람 표시 우선) 또는 R2 「현지 출처 없음 — <리포트>」. 근거 리포트: en · ja · zh-Hant = r2 · zh = r1 · th · vi · yue = r3.

| id | en | ja | zh | zh-Hant | th | vi | yue |
|---|---|---|---|---|---|---|---|
| `kr-001` | `Thermage CPT` ✓ | `サーマクールCPT` ✓ | `Thermage CPT` · `热玛吉CPT` ✓ | `黃金電波` · `CPT黃金電波` · `黃金電波拉皮` · `Thermage CPT` ✓ | `Thermage CPT` ✓ | `Thermage CPT` ✗ | `Thermage CPT` ✗ |
| `kr-002` | `Sofwave` ✓ | `ソフウェーブ` · `Sofwave` ✓ | `素芙波` · `素夫波` · `索夫波` · `Sofwave` ✓ | `索夫波` · `速飛威` · `Sofwave` ✓ | `Sofwave` ✓ | `Sofwave` ✗ | `索夫波` · `Sofwave` ✓ |
| `kr-003` | `EXION` ✓ | `エクシオン` · `EXION` ✗(처분 r2-4 · 출처 1) | `EXION` ✗ | `時空E電波` · `EXION` ✓ | `EXION` ✗ | `EXION` ✗ | `EXION` ✓ |
| `kr-004` | `DENSITY` · `Density RF` ✓ | `デンシティ` · `DENSITY` ✓ | `DENSITY` ✗ | `無雙電波` · `DENSITY` ✓ | `DENSITY` ✗ | `DENSITY` ✗ | `DENSITY` · `無雙電波` ✓ |
| `kr-005` | `EMFACE` ✓ | `エムフェイス` · `EMFACE` ✓ | `美菲斯` · `EMFACE` ✓ | `菲斯波` · `EMFACE` ✓ | `EMFACE` ✓ | `EMFACE` ✗ | `美菲斯` · `EMFACE` ✓ |
| `kr-006` | `Clear + Brilliant` · `Clear & Brilliant` · `Clear and Brilliant` ✓ | `クリア＆ブリリアント` · `クリア&ブリリアント` · `クリア＋ブリリアント` · `クリア アンド ブリリアント` · `C&B` · `Clear + Brilliant` ✓ | `素颜光` · `Clear + Brilliant` ✗ | `鳳凰光` · `Clear+Brilliant Touch` · `Clear + Brilliant` ✓ | `Clear + Brilliant` ✗ | `Clear + Brilliant` ✗ | `素顏光` · `C+B` · `Clear + Brilliant` ✓ |
| `kr-007` | `Profhilo` ✓ | `プロファイロ` · `プロフィーロ` · `Profhilo` ✓ | `Profhilo` ✗ | `逆時針` · `璞菲洛` · `Profhilo` ✓ | `Profhilo` · `โปรไฟโล` ✓ | `Profhilo` ✓ | `逆時針` · `Profhilo` ✓ |
| `kr-008` | `Neuramis` ✗(처분 r2-3) | `ニューラミス` · `Newramis` · `Neuramis` ✓ | `Neuramis` ✗ | `優美施` · `仙女玻尿酸` · `Neuramis` ✓ | `Neuramis` · `นิวรามิส` ✓ | `Neuramis` ✗ | `優美施` · `Neuramis` ✓ |
| `kr-009` | `Belotero Revive` ✓ | `ベロテロリバイブ` · `ベロテロ リバイブ` · `Belotero Revive` ✓ | `Belotero Revive` ✗ | `素妍針` · `Belotero Revive` ✓ | `Belotero Revive` ✓ | `Belotero Revive` ✗ | `Belotero Revive` ✓ |
| `kr-010` | `AestheFill` ✗(처분 r2-3) | `エステフィル` · `AestheFill` ✓ | `艾塑菲` · `AestheFill` ✓ | `艾麗斯` · `精靈針` · `艾麗斯精靈針` · `AestheFill` ✓ | `AestheFill` · `เอสเทอฟิล` ✓ | `AestheFill` ✗ | `精靈針` · `AestheFill` ✓ |
| `kr-011` | `HydraFacial` ✓ | `ハイドラフェイシャル` · `HydraFacial` ✓ | `海菲秀` · `HydraFacial` ✓ | `海菲秀` · `海飛秀` · `HydraFacial` ✓ | `HydraFacial` ✗ | `HydraFacial` ✗ | `HydraFacial` ✗ |
| `kr-012` | `miraDry` ✓ | `ミラドライ` · `miraDry` ✓ | `清新微波` · `miraDry` ✗ | `清新微波` · `miraDry` ✓ | `miraDry` · `มิราดราย` ✓ | `miraDry` ✗ | `miraDry` ✗ |
| `kr-013` | `TeslaFormer` · `TESLA Former` ✗(클리닉 체인 1 — R7) | `テスラフォーマー` · `TeslaFormer` ✓ | `TeslaFormer` ✗ | `易力肌塑` · `易力肌塑磁雕儀` · `TeslaFormer` ✓ | `TeslaFormer` ✗ | `TeslaFormer` ✗ | `TeslaFormer` ✗ |

- **이름이 영문인 칸 중 ✗** = R2 「현지에 없음」(note = `현지 출처 없음 — …`) 또는 현지 출처 1개(note = 그 URL). 리포트 확신 「하」 · 출처 0 은 앞, 「중」(출처 1)은 뒤.
- **대만과 홍콩이 다른 칸**(R6): `kr-001` · `kr-003` · `kr-005` · `kr-006` · `kr-008`(name 같음 · alias 다름) · `kr-009` · `kr-010` · `kr-011` · `kr-012` · `kr-013`. 같은 것: `kr-002` 索夫波 · `kr-004` 無雙電波 · `kr-007` 逆時針.
- **언어가 달라 같은 글자인 것은 겹침이 아니다**(검사 3 · 4 는 ko 쪽 · entry 안만 본다) — zh `素颜光` · yue `素顏光`, zh-Hant · yue `優美施` 등. 다른 시술끼리 같은 현지명도 허용(§4.2 — 역방향은 처음 짝).
- 조사에서 본 표기 중 **넣지 않은 것**(R4 · R5): ja `サーマクール` · en `Thermage` · `Density` · `Revive` · `Tesla` 단독 · zh `黄金微针` · `童颜针` · `彩虹针` · `热玛吉第四代`(원문은 「第四代(CPT)」) · zh-Hant `仙女` · `塑顏電波`(검색만) · `液態電波` · `丹士特`(키워드 메타만) · `水柔` · `Baby laser` · yue `黃金微針` · `膠原槍` · `水光針` · `韓國仙女針` · `舒膚微` · `…療程` 꼴 · 대소문자 변형 · 제조사 접두 · 이름+영문 꼴.

### 4.2.3 기존 표기 변경 (0.6.0 — D-40 · 처분 r1 · r3)

`source` · `note` 는 A · B = `web-research 2026-10-27` · 대표 URL(R2 칸은 `현지 출처 없음 — research-r1-zh-report.md`) · C = `manual` · `note` 에 「조사 r3 표 B-2 결함 — 현지 표기 미조사」. `raw` 는 그대로 둔다. 표에 없는 entry 는 바꾸지 않는다.

**A. zh(대륙) — 대륙 공식명 · 미허가 · 한국 전용 제품(R1 · R2 · R3 · R4)**

| term | ko | 지금(`.5`) name · aliases | `.6` name · aliases | `reviewed` | 근거 |
|---|---|---|---|---|---|
| ph-040 | 리즈톡스 | `丽姿妥适` · `Liztox` | **`解索橙`** · `丽姿妥适` · `Liztox` | ✓ | NMPA 2026-01 · 처분 r1-1 |
| ph-031 | 레티보 | `乐提保` · `Letibo` | **`乐提葆`** · `乐提保` · `Letibo` | ✓ | 처분 r1-1 |
| ph-042 | 보툴렉스 | `白毒`(+U+200C) · `Botulax` | **`乐提葆`** · `白毒`(U+200C 지움) · `Botulax` | ✗ — Botulax = Letybo 수출명(대만 조사)에서 이은 것 · 대륙 직접 근거 없음 | 처분 r1-2 · 검사 7 |
| ph-008 | 엘라비에 | `艾拉薇` · `Elravie` | **`艾莉薇`** · `艾拉薇` · `Elravie` | ✓ | CFDA 2015 · 처분 r1-1 |
| ph-112 | 스컬트라 | `素颜萃童颜针` | **`塑妍萃`** · `素颜萃童颜针` | ✓ | NMPA 2024 · 처분 r1-1 |
| ph-130 | 써마지FLX | `美版热玛吉FLX` · `Thermage FLX` · `热玛吉` | **`超玛吉FLX`** · `美版热玛吉FLX` · `Thermage FLX`(**`热玛吉` 지움** — R4) | ✓ | NMPA 2024 · 처분 r1-1 · r1-6 |
| ph-072 · 075 · 079 | 리쥬란아이 · 리쥬란 힐러 · 리쥬란 HB+ | `丽珠兰白盒` · `丽珠兰黑盒` · `丽珠兰红盒` | **`丽驻兰白盒`** · **`丽驻兰黑盒`** · **`丽驻兰红盒`**(브랜드 부분만 공식명 · 지금 name 은 alias) | ✗ — 白盒 · 黑盒 · 红盒 구분은 출처 미확인(기본값 · 0.6.1 OQ-018 ④ 처분 = 상자 표기 그대로 · ✗ 유지) | 처분 r1-1 |
| ph-108 | 쥬베룩 | `乔雅露` · `Juvelook` | **`Juvelook`** · `乔雅露` | ✗ — 대륙 중문명 없음(NMPA 2026-07 · 기사 1 도메인) | 처분 r1-4 |
| ph-027 | 나보타 | `绿毒` · `Nabota` | **`Nabota`** · `绿毒` | ✗(R2) | 대륙 허가 7종 밖 · 처분 r1-2 |
| ph-041 | 메디톡신 | `粉毒` · `Meditoxin` | **`Meditoxin`** · `粉毒` | ✗(R2) | 처분 r1-2 |
| ph-028 | 뉴럭스 | `纽乐适` · `Neurox` | **`NEWLUX`**(en name) · `纽乐适` · `Neurox` | ✗(R2) | 처분 r1-2 |
| ph-044 | 타임버스 | `时光巴士` · `Timbus` | **`Tyemvers`**(en name) · `时光巴士` · `Timbus` | ✗(R2) | 처분 r1-2 |
| ph-001 · 002 · 004 · 060 · 062 · 070 · 083 · 110 · 124 · 134 · 136 · 137 · 149 · 150 · 151 | 신펄 · 채움 · 더채움 · 미라클 · 에버라인 · 벨피엔 · 에스에프 · 글로벨라 · 더블로골드 · 시크릿 · 아그네스 · 인트라셀 · 마이셀 · 셀피아 · 리젠ACR | 음역 · 직역(新珍珠 · 彩韵 · 彩韵Plus · 奇迹线 · 艾芙莱恩 · 贝尔菲恩 · SF注射 · 格洛贝拉 · 多普勒金 · Secret黄金微针 · 雅格尼斯 · 英特拉赛尔 · 玛伊赛尔 · 赛尔皮亚 · 瑞珍ACR) | **그 term 의 en name**(Synpurl · Chaeum · The Chaeum · Miracle Thread · Everline · BelPN · SF Injection · Glovella · Doublo Gold · Secret RF · AGNES · INTRAcel · Mycell · Cellpia · RegenACR) · aliases = 지금 name + 지금 aliases(새 name 과 같은 것은 뺀다) | ✗(R2) | 조사 r1 표 B-3(대륙 원문 0건) · 처분 r1-3 |
| ph-135 | 포텐자 | `黄金微针` | **`Potenza`**(en name) · aliases `[]` — `黄金微针` 은 장르어라 alias 로도 남기지 않는다(R3 예외 · R4) | ✗(R2) | 처분 r1-6 · D-38 의 zh-Hant 처리와 같음 |

- ph-031 · ph-042 가 zh `name` 「乐提葆」 를 함께 쓴다 — 허용(다른 시술의 같은 현지명 · §4.2). 역방향은 시드 순서 첫 짝 ph-031 레티보로 간다(§4.5) — 같은 제품(Letybo)이라 의도와 맞다.
- ph-084 큐어스킨(zh 이미 `CureSkin`)은 바꾸지 않는다. 조사 r1 이 영문화 대상 목록에 넣은 ph-080 · 081 · 088 · 140 · 152 · 155 · 157 은 일반 약어 · 일반 명칭이라 이번에 보지 않았다(조사 r1 §3 B-3 끝) — 그대로.
- **zh-Hant ph-130 alias `熱瑪吉` 도 지운다** — `t2s` 뒤 `热玛吉` 로 같은 모호어(R4 · 0.5.0 「zh · zh-Hant 둘 다」 원칙). zh-Hant 의 그 밖 값은 바꾸지 않는다(조사 r2 표 B 「틀린 표기는 없다」).

**B. th — 현지 메뉴가 영문인 기존 term(R2′ · 처분 r3)**

| term | ko | 지금 | `.6` | `reviewed` |
|---|---|---|---|---|
| ph-108 | 쥬베룩 | `จูเบลุค` · `Juvelook` | **`Juvelook`** · `จูเบลุค` | ✗ — 현지 근거 1 도메인(hdmall) |
| ph-112 | 스컬트라 | `สกัลป์ตรา` | **`Sculptra`** · `สกัลป์ตรา` | ✓ — slcclinic · nitiponclinic · romrawin · apexprofoundbeauty · hdmall |

- 태국 문자 옛 name 은 R3 대로 alias(현지 출처에서 못 봤지만 손님 말 · STT 표기로 나올 수 있다 — 지우는 근거가 없다). ph-113 쥬베룩볼륨 th 는 아래 D(OQ-018 ③)로 바뀐다.

**C. 데이터 결함 — 뜻이 없거나 잘린 값(처분 r3 · R3 예외 — 옛 값은 지운다)**

| term | 언어 | 지금 | `.6` name | `reviewed` | 왜 |
|---|---|---|---|---|---|
| ph-090 메조건 | yue | `美條件` | **`Mesotherapy`**(en name) | ✗ | 「메조건」을 「미조건」으로 읽은 기계 오역 — 뜻 없는 말 |
| ph-077 엑소좀/성장인자 | vi | `Exosome/` | **`Exosome/Growth Factor`**(en name) | ✗ | 뒤 절반 잘림 |
| ph-148 전동 MTS | vi | `Tự động` | **`Electric MTS`**(en name) | ✗ | 「자동」만 남음 |
| ph-116 무세포동종진피(hADM) | vi | `Trẻ hóa da` | **`human Acellular Dermal Matrix`**(en name) | ✗ | 「피부 회춘」 — 뜻이 다름 |

- C 는 현지 표기를 조사하지 않았다 — R2 의 「현지에 없음」과 같은 꼴(영문)로 두고 `source: "manual"` 로 구분한다. 현지 표기는 OQ-016(시드 검수 숙제)으로.

**D. OQ-018 처분(0.6.1 — 코디 2026-10-27 · `research-dispositions.md` 「OQ-018 처분」 · 배포본 `.6` 대조)** — 판 번호는 `.6` 그대로(같은 PR #10).

| # | term | 언어 | `.5` name · aliases | `.6` name · aliases | `reviewed` · `source` | 왜 |
|---|---|---|---|---|---|---|
| ① | ph-123 올리지오 | zh | `韩版热玛吉` · `Oligio` | **`Oligio`** · `[]` | ✗ · `manual` | name 이 모호어(§4.2.1) — 영문으로 · 모호어는 alias 에도 두지 않음 |
| ① | ph-126 슈링크유니버스 | zh | `韩版超声刀` · `Shurink Universe` | **`Shurink Universe`** · `[]` | ✗ · `manual` | 같음 |
| ② | ph-121 울쎄라 | yue | `超聲刀` · `Ultherapy` | **`美版超聲刀`** · `Ultherapy`(**`超聲刀` 단독 지움** — 홍콩 HIFU 일반) | ✗ · `web-research 2026-10-27` | 조사 r3 표 B-2 · C-6 |
| ③ | ph-113 쥬베룩볼륨 | zh · th | `乔雅露黑瓶丰盈` · `Juvelook Volume` / `จูเบลุควอลุ่ม` · `Juvelook Volume` | **`Juvelook Volume`** · 옛 name 을 alias | ✗ · `manual` | ph-108 쥬베룩과 같은 처리 |
| ④ | ph-072 · 075 · 079 리쥬란 | zh | (위 A 그대로) | 바꾸지 않음 | ✗ | 상자 표기 그대로 |
| ⑤ | ph-130 써마지FLX | ko | `ko_aliases: ["써마지"]` | **`ko_aliases: []`** · term `note` 에 처분과 옛 근거 | — | **0.6.0 「그대로」를 뒤집음** — 「써마지」 는 CPT(`kr-001`)까지 덮는 브랜드명(zh `热玛吉` 를 뺀 것과 같은 이유). 실물 ⑳: 「써마지 CPT」 → zh-Hant `鳳凰電波`(FLX · 오역) — 지운 뒤 `黃金電波`(kr-001 · 맞음) |

- `manual` 칸의 `note` = 「OQ-018 처분 ① · ③ — …(코디 2026-10-27)」. 0.5.0 OQ-014 의 「써마지FLX ko 별칭」 은 이로써 뒤집혔다 — 상담사가 FLX 없이 「써마지」 라고만 하면 이제 정방향 짝이 없다(Soniox 번역에 맡김).

### 4.2.4 시드 `.7` — 사전 전체 보정 (0.8.0 자리 — D-46 · **0.8.2 값 채움** — D-51 · D-52 · D-53 · 조사 처분 · **0.8.3** — 처분 §4 ~ §6 · D-54)

> **값의 원천은 네 파일이다** — 조사 칸 판정 `orchestration/work/interpreter-idea/quality-r1-zh-cells.json`(zh · zh-Hant · yue 510칸) · `quality-r2-en-ja-th-vi-cells.json`(en · ja · th · vi 680칸) · 대만어 별칭 판정 `quality-r3-tw-alias.json`(245행 · D-53 — ② F) · 코디 처분 `quality-research-dispositions.md`(확정 2026-11-14 — §1 · §2 = D-51 · D-52 · **§4 = OQ-030 처분 · §5 = D-54 · §6 = 조사 r3 처분**(0.8.3)). **이 절은 1,190칸을 표로 옮기지 않는다** — ① 칸 판정을 시드에 옮기는 규칙 ② 규칙 밖에서 손으로 정한 칸 ③ 규칙을 기계로 적용했을 때 언어별 개수만 적는다. backend 는 이 파일들을 읽는 **변환 스크립트**로 시드를 바꾸고(WP23), 바뀐 칸 전부는 그 PR 의 대조표로 낸다. 값을 우리가 짓지 않는다(§4.2.1 머리말 · D-32 · D-33 · D-35) — 이 파일들에 없는 표기는 `.7` 에 없다.
> **선행(WP23 을 막는 것)**: 품질 시험 「울쎄라 원인 가르기」(㉔ — E7 · WP22) **하나**. (0.8.3) 대만어 별칭 조사 r3 은 끝났고(② F) · OQ-030 은 닫혔다(코디 처분 §4 — 아래 「기계 적용 — 읽는 법」).

**무엇을 · 어디서 (D-46)**

| 항목 | 계약 | 근거 |
|---|---|---|
| 대상 | 시드 `.6` 의 **170 term 전부** × 7개 언어 = 1,190칸 | D-46 |
| 나라 | en = **미국** · ja = 일본 · zh = 중국 대륙 · zh-Hant = 대만 · th = 태국 · vi = 베트남 · yue = 홍콩 | D-46 · 입력 5 「미국을 기본으로 할거야 영어는」 |
| 근거 사이트 | 언어마다 **그 나라 피부과 · 미용 클리닉 공식 홈페이지 6곳**(+ 같은 방법으로 더 읽은 곳 — 리포트 표 S). 시술 메뉴 · 가격표가 있는 곳 | D-46 · 조사 r1 · r2 표 S |
| 근거에서 빼는 것 | 블로그 · 중개 플랫폼 · **한국 병원의 외국어 페이지**(한국식 직역이 섞인다). r1 의 보조 사이트(B)는 출처 수에 세지 않는다 | D-46 · 조사 r1 방법 |
| 못 읽은 사이트 | 리포트 표 S 에 그대로(대륙은 가격표 있는 사이트를 못 채움 — zh 「못 찾음」 97) | D-46 · 조사 r1 한계 |
| 조사 날짜 | **2026-11-14** — `source` = `web-research 2026-11-14` | 조사 r1 · r2 |

**규칙** — §4.2.1 R1 ~ R9 를 그대로 쓴다. `.7` 에서 다시 못 박는 것:

| # | 규칙 | 근거 |
|---|---|---|
| Q1 | **현지어 우선 · 현지에 그 말이 없을 때만 영어**(R1 · R2 와 같은 방향 — 영어가 기본이 아니다). 현지 클리닉도 영문 브랜드명을 쓰면 그 영문이 곧 현지명이다(R2′) | D-46 · 입력 5 「최대한 현지어 … 없으면 영어 부득이 하게」 · D-38 ② · D-40 |
| Q2 | **`reviewed: true` = 독립 현지 출처 2개 이상**(R7 그대로) | D-35 |
| Q3 | 옛 `name` 은 `aliases` 로 내린다(R3) · 모호어 · 결함 값은 남기지 않는다(R3 예외 · R4) · alias 로 넣지 않는 꼴(R5) · yue 는 zh-Hant 에서 복사하지 않는다(R6) | §4.2.1 |
| Q4 | **이름 겹침**(같은 언어에서 다른 term 이 같은 `name`): 현지 클리닉이 장비 · 제품을 따로 부르면 그 이름으로 가른다. **현지도 가르지 않는 말은 우리도 가르지 않는다**(처분 r1-2). **앞 처분으로 일부러 같게 한 것은 그대로 — zh `乐提葆` = ph-031 레티보 · ph-042 보툴렉스**(§4.2.3 A) | D-46 · 처분 r1-2 |
| Q5 | 앞 처분(§4.2.2 · §4.2.3 · 10-27 `research-dispositions.md`)으로 정한 값은 **새 근거가 없으면 뒤집지 않는다.** `.7` 에서 뒤집은 것은 하나 — **「써마지」 맨 이름(D-51 · 10-27 처분 6 · OQ-018 ⑤)** | D-46 · D-51 |
| Q6 | **일반 낱말은 사전에 넣지 않는다**(§4.5 「넣지 않는 것」 · D-45). 조사 리포트의 현장 일반어 표(표 C)는 §4.5 `text` 문안의 참고일 뿐이다 | D-45 |

**① 칸 판정 → 시드 반영 규칙 (처분 §1 그대로 · 기계 적용)**

칸 = term × 언어 하나. `n` = 그 칸 `sources` 의 수(사이트 수). 「제안」 = 그 칸의 `proposed_name` · `proposed_aliases`.

| 판정(`verdict`) | 반영 |
|---|---|
| 유지 | 값 그대로. `n` ≥ 2 면 `reviewed: true`(지금 true 인 칸은 `n` < 2 여도 내리지 않는다 — 조사 r1 방법) |
| 변경 · `n` ≥ 2 | `name` = 제안 · 옛 `name` 은 alias(뜻이 틀린 값 · 결함 값은 alias 에도 안 둔다 — 아래 ② · 「읽는 법」 a) · `reviewed: true` |
| 변경 · `n` = 1 | `name` 은 그대로 · 제안 표기를 alias 로 · `reviewed: false` |
| 별칭 추가 | 제안 별칭을 alias 에 더한다 |
| 현지도 영문 | `name` = 영문 · 옛 현지 문자 값은 출처가 있으면 alias, 없으면 버린다(「읽는 법」 c) · `n` ≥ 2 면 `reviewed: true`, 이름이 바뀌고 `n` = 1 이면 `false` |
| 현지에 없음 → 영문 | **th = 영문 `name`**(옛 태국 문자 값은 alias · `reviewed: false` — R2 · R3) / **ja 는 가타카나 유지**(13칸 — 값 · `reviewed` 그대로. 일본은 외래 제품명도 가타카나 통례 · 처분 r2-4). r1(zh · zh-Hant · yue)은 이 판정을 내지 않았다 |
| 못 찾음 | 그대로(값 · `reviewed` 안 바꿈) |
| 처분과 다름 | 1칸(zh ph-130) — 아래 ② D-51 |
| vi 출처가 S3(Seoul Center)뿐인 칸 | 반영하지 않는다(운영 주체 국적 미확인 · 처분 r2-17) — **해당 0칸**(S3 은 늘 다른 사이트와 같이 나온다) |
| 빗금(`/` · `／`)이 든 `name` | 현지 근거 있는 한 낱말(그 칸의 「변경」 제안)이 있으면 그것 · 없으면 **빗금만 뺀다(빈칸 하나로)** — 표기 정리일 뿐 값을 짓지 않는다(처분 r2-14). 옛 빗금 꼴은 alias 로 남기지 않는다 |

- **두 파일의 `proposed_aliases` 는 뜻이 다르다** — r1(zh · zh-Hant · yue) = **제안하는 전체 목록**(지금 별칭 + 더한 것) · r2(en · ja · th · vi) = **새로 더할 별칭만**(지금 `name` 을 alias 로 내릴 때는 그 값이 여기 들어 있다). 스크립트는 r1 은 목록으로 **바꾸고** r2 는 지금 별칭에 **더한다**. r2 는 「유지」 · 「별칭 추가」 · 「못 찾음」 칸의 `proposed_name` 이 `null` 이다(= 지금 값).
- **별칭의 순서**(0.8.4 · 처분 §7 W-2): **지금 별칭 → 옛 `name` → 제안 순**으로 잇고, 겹치면 앞 것 하나만 남긴다(r1 처럼 목록을 바꾸는 칸은 「지금 별칭 가운데 남는 것 → 옛 `name` → 새로 드는 제안」). 순서는 줄이기가 뒤에서부터 빼는 역방향 별칭이 어느 것인지를 정한다. **이 절 ② 표의 별칭은 순서를 맞춰 적은 것이 아니다 — 표 대조(WP23 시험 · 대조표)는 순서를 보지 않고 집합으로 견준다.**
- **alias 로 더하지 않는 것**(기존 규칙 그대로): `name` 과 같은 말 · **`name` 이나 이미 있는 별칭과 대소문자만 다른 말**(R5 ① — 견줄 때 대소문자를 접는다. 0.8.3 · W-3: 걸리는 칸은 **ja ph-071 볼뉴머** — 제안 별칭 `VOLNEWMER` 는 이미 있는 별칭 `Volnewmer` 와 대소문자만 달라 더하지 않는다. 0.8.2 검수 재계산과 ja 별칭이 1개 갈린 자리가 여기다) · 이미 있는 별칭 · §4.2.1 모호어 목록(R4)에 걸리는 말 · 괄호 · 보이지 않는 글자(R9).
- **`source` · `note`**: 값(`name` · `aliases` · `reviewed`)이 하나라도 바뀐 entry 는 `source: "web-research 2026-11-14"` · `note` = 그 칸 `sources` 첫 번호의 사이트 URL(리포트 표 S) — 출처가 없는 칸(th 「현지에 없음」 · 아래 ② 의 영문 처분)은 `현지 출처 없음 — <리포트 파일 이름>`. **조사 근거 없이 규칙 · 처분만으로 고친 칸**(빗금 정리 · `reviewed` 만 내린 칸 · 합치기로 별칭만 는 칸)은 `source: "manual"` · `note` = 「D-51 처분 <번호> — …」(0.6.0 §4.2.3 C 방식). 바뀌지 않은 entry 는 `source` · `note` · `raw` 그대로.

**② 규칙 밖 — 처분 §2 가 손으로 정한 것** (칸 = `name` · `aliases` · `reviewed` ✓/✗. 표에 없는 칸은 ① 규칙대로)

A. **새 term 둘** — `id` 는 `kr-` 번호를 이어 **`kr-014` · `kr-015`**(§4.2 규칙 — 더한 순서 · 번호를 다시 쓰지 않는다) · 시드 배열 **맨 뒤에 이 순서로** · `ko_aliases: []` · 모든 entry `aliases: []` · `source: "web-research 2026-11-14"`.

| id | `ko` | `category` | en | ja | zh | zh-Hant | th | vi | yue | 근거 |
|---|---|---|---|---|---|---|---|---|---|---|
| `kr-014` | 써마지 | 기기 리프팅 | `Thermage` ✓ | `サーマクール` ✓ | `热玛吉` ✓ | `Thermage` ✗ | `เทอร์มาจ` ✓ | `Thermage` ✗ | `熱瑪吉` ✓ | **D-51**(처분 r1-1 · r2-1) — 세대 없는 이름: 미국 5 · 일본 8 · 대륙 4 · 태국 6 · 홍콩 4곳(✓ = R7). 대만은 세대별 이름뿐 · 베트남 근거 없음(✗ · `note` = 현지 출처 없음) |
| `kr-015` | 리투오 | 스킨부스터 | `Re2O` ✗ | `リトゥオ` ✗ | `Re2O` ✗ | `Re2O` ✗ | `Re2O` ✗ | `Re2O` ✗ | `Re2O` ✗ | 처분 r1-7 · r2-16 — 근거 ja 1곳 · 대만 1곳(`Re2O`). 현지어 없으면 영어 |

- `써마지FLX`(ph-130) · `써마지 CPT`(kr-001) term 은 **그대로** — zh ph-130 「처분과 다름」(별칭 `热玛吉` 되살리기)과 yue · th ph-130 의 맨 이름 별칭 제안(`熱瑪吉` · `เทอร์มาจ`)은 **반영하지 않는다**(맨 이름은 `kr-014` 하나에만 — 역방향 짝이 FLX 로 가지 않게). §4.2.1 모호어 목록에 「`kr-014` 의 `name` 은 다른 term 의 name · alias 로 못 쓴다」 를 더했다.
- **10-27 처분 6 · OQ-018 ⑤ 를 뒤집는다**(D-51): 그때는 ko 별칭 「써마지」 가 FLX 에 붙어 「써마지 CPT」 를 FLX 로 끌고 갔다(실물 ⑳). 이번에는 **따로 선 term** 이라 FLX · CPT 의 짝은 그대로 남는다 — 「써마지 CPT」 · 「써마지FLX」 가 일반 term 으로 뭉개지지 않는지는 WP23 실물에서 ⑳ 과 같은 방법으로 다시 본다(§9.3 ㉒).

B. **합치는 term 두 쌍** — 남는 term 의 `id` · `ko` · `category` · entry `name` 은 그대로 · 사라지는 term 의 `ko` 는 남는 term 의 **`ko_aliases`** 로 · 사라지는 term 의 그 언어 `name` · `aliases` 가운데 남는 term 에 없는 말은 **alias 로** 옮긴다(R3 — 손님이 그 이름으로 말할 수 있다). 두 term 모두 ① 규칙을 먼저 적용한 뒤 합친다.

| 남는 term | 사라지는 term | `ko_aliases` | 옮겨 오는 별칭 | 근거 |
|---|---|---|---|---|
| `ph-105` 냉각지방분해 | `ph-106` 크라이오리포라이시스 | `["크라이오리포라이시스"]` | th `Cryolipolysis` · `ไครโอลิโพไลซิส` · vi `Phân giải mỡ lạnh`(그 밖의 언어는 겹쳐서 0) | 처분 r2-9 — 같은 시술 |
| `ph-097` 시그니처프로그램 | `ph-127` 시그니처 프로그램 | `["시그니처 프로그램"]` | vi `Chương trình đặc biệt` | 처분 r2-10 · D-46 중복 항목 |

- **없앤 `id`(`ph-106` · `ph-127`)는 다시 쓰지 않는다.** 통역 기록(§5.9)의 `terms` 에는 옛 `id` 가 남아 있다 — **기록은 고치지 않는다**(지난 기록의 `ph-106` = 지금의 `ph-105` · `ph-127` = `ph-097` 로 읽는다. 세션 시작 줄의 시드 `version` 으로 어느 판의 `id` 인지 가린다). term 수 = 170 − 2 + 2 = **170**.

C. **손으로 정한 칸** — `지금(.6)` → `.7`. 칸 표기 = `name` · `aliases`(없으면 `[]`) · `reviewed`.

| term | ko | 언어 | 지금(`.6`) | `.7` | 처분 |
|---|---|---|---|---|---|
| ph-012 | 토닝 | zh | `提亮` · `[]` ✓ | **`调Q激光`** · `激光嫩肤` ✓ | **D-52**(E1) — `提亮`(효과 서술) · `激光美白` · `镭射净肤` 는 name · alias 모두 뺌 · `光子嫩肤`(IPL) 넣지 않음 |
| ph-012 | 토닝 | yue | `調色` · `[]` ✓ | **`淨膚激光`** · `激光嫩膚` ✓ | r1-6(E2) — `調色` 은 화장 글에만 → alias 로도 안 둠 |
| ph-010 | 색소 | ja | `レーザートーニング` · `[]` ✗ | **`シミ治療`** · `色素沈着` · `シミ取り` ✓ | r2-5(E3) — `レーザートーニング` 은 토닝으로 |
| ph-012 | 토닝 | ja | `肝斑治療` · `[]` ✓ | **`レーザートーニング`** · `トーニング` · `ピコトーニング` ✓ | r2-6(E3) — `肝斑治療`(목적어) 뺌 |
| ph-026 | 턱선 | ja | `顎ライ` · `[]` | **`フェイスライン`** · `顎ライン` · `あごのライン` ✓ | ① 규칙(변경 · 8곳) — 잘린 값 `顎ライ` 는 alias 로 안 둠(R3 예외 · E4) |
| ph-003 | 필러 | ja | `フィラー` · `[]` ✗ | **`ヒアルロン酸注入`** · `フィラー` · `ヒアルロン酸注射` ✓ | r2-7 — 출처 많은 쪽(8곳) |
| ph-074 | 스킨부스터 | ja | `スキンブースター` · `[]` ✓ | **`肌育注射`** · `スキンブースター` ✓ | r2-7 |
| ph-058 · ph-059 | 지방분해주사 · DCA | ja | `脂肪分解注射` / `脂肪溶解注射` · `DCA` | **`脂肪溶解注射`** · `脂肪分解注射` ✓ / **`デオキシコール酸`** · `DCA` ✓ | r2-8 — 같이 바꿔 겹침 방지(ph-059 의 옛 name 은 alias 로 안 둠) |
| ph-047 · ph-050 | 턱선보톡스 · 페이스앤넥큐레이션 | ja | ✓ | 값 그대로 · **✗** | r2-15 — 대체 근거 없음 |
| ph-019 · 020 · 023 | 레블라이트 · 클라리티2 · 엑셀V | zh | `激光` · (`RevLite` / `Clarity II` / `Excel V`) ✓ | **`RevLite`** / **`Clarity II`** / **`Excel V`** · `[]` ✗ | r1-2(E8) — 현지 문자 장비명 없음 → 영문 · `激光` 은 alias 로도 안 둠(ph-014 레이저 `激光` 은 그대로) |
| ph-074 · ph-078 | 스킨부스터 · HA (물광) | zh | `水光针` 둘 | 그대로(ph-078 「변경 → `水光注射`」 **반영 안 함**) | r1-2(E9) — 현지 사이트도 가르지 않는다 |
| ph-108 · ph-113 · ph-072 · 075 · 079 · ph-015 · 016 | 쥬베룩 · 쥬베룩볼륨 · 리쥬란 셋 · 프락셀 · 프락셔널 | zh-Hant | `喬雅露` ×2 · `麗珠蘭` ×3 · `飛梭雷射` ×2 | 그대로(ph-113 「현지도 영문 → `Lenisna`」 **반영 안 함**) | r1-2 · r1-5 |
| ph-125 | 마이크로웨이브 | zh | `微波治疗` ✓ | 값 그대로 · **✗** | r1-10 — 다한증 뜻으로 쓰임 |
| ph-034 · 035 · 038 | 사각턱 · 승모근 · 종아리 | zh | — | 별칭 `瘦脸针` · `注射瘦脸` · `瘦肩针` · `瘦腿针` **넣지 않음** | r1-11 — 역방향이 「瘦脸针 → 사각턱」 이 된다 |
| ph-034 | 사각턱 | ja | `エラ/咬筋` · `[]` ✓ | **`エラ`** · `咬筋` ✓ — 제안 별칭 `エラボトックス` **넣지 않음** | **처분 §4-e**(0.8.3 · r1-11 원칙을 7개 언어 전부에) — 부위 term 에 시술 이름을 name · alias 로 새로 넣지 않는다 |
| ph-035 | 승모근 | ja | `僧帽筋` · `[]` ✓ | 그대로 — 제안 별칭 `肩ボトックス` **넣지 않음**(칸 변화 없음) | 처분 §4-e |
| ph-029 · 035 · 038 | 다한증 · 승모근 · 종아리 | th | `ลดเหงื่อ` / `กล้ามเนื้อบ่า` / `น่อง` · `[]` ✓ | 그대로 — 제안 별칭 `โบท็อกรักแร้` / `โบท็อกบ่า` · `ลดบ่า` / `ลดน่อง` **넣지 않음**(세 칸 모두 변화 없음) | 처분 §4-e |
| ph-034 | 사각턱 | th | `กรามเหลี่ยม` · `[]` ✓ | **칸 전체 그대로** — 「변경 → `ลดกราม`」(6곳) **반영 안 함**. 제안 name 과 제안 별칭 `โบท็อกลดกราม` · `โบท็อกกราม` 이 모두 시술 이름이다(남는 제안 0) | 처분 §4-e |
| ph-034 | 사각턱 | yue | `方下巴` · `[]` ✓ | **칸 전체 그대로** — 「변경 → `瘦面針`」(5곳) **반영 안 함**. 제안의 나머지 별칭 `咀嚼肌` · `國字臉`(시술 이름 아님)도 이 판에서는 더하지 않는다 — **코디 확인(0.8.4 · 처분 §7 W-1): `.6` 그대로 · 홍콩 메뉴의 `瘦面針` 은 §4-e 라 더하지 않는다** | 처분 §4-e · §7 |
| ph-034 | 사각턱 | vi | `Cạnh hàm` · `[]` ✓ | **`Hàm vuông`** · `Cạnh hàm` · `Góc hàm` ✓ — 제안 별칭 `Gọn hàm` **넣지 않음** | 처분 §4-e |
| ph-034 | 사각턱 | zh-Hant | `瘦臉針` · `咬肌` · `國字臉` · `咀嚼肌肉毒` · `下顎角瘦臉針` · `瘦小臉` ✓ | **`國字臉`** · `瘦小臉` · `咀嚼肌` ✓ — 옛 name `瘦臉針` 은 **별칭으로 남기지 않는다**(0.8.4 · 처분 §7 W-3 — 대만 현지 클리닉 근거가 아니고 §4-e 와도 같은 꼴 · ② F 옛 name 표) | ① 「변경」(5곳) · 읽는 법 d · 처분 §7 |
| ph-121 | 울쎄라 | en | `Ulthera` · `[]` ✓ | **`Ultherapy`** · `Ulthera` · `Ultherapy PRIME` ✓ | r1-3 · r2-2 — 미국 7곳 |
| ph-121 | 울쎄라 | zh | `美版超声刀` · `Ultherapy` ✓ | **그대로** — 별칭 `Ultherapy` 를 뺄지는 품질 시험 「울쎄라 원인 가르기」(§9.3 ㉔ · WP22) 결과로 코디가 정한다(E7) | r1-3 — 대륙 6곳 0건이라 근거로는 못 정함 |
| ph-027 | 나보타 | en | `Nabota` · `[]` ✓ | `Nabota` · `Jeuveau` **✗** | r2-11 — 제품 대응(제조사 사실)은 alias 로만 |
| ph-065 | 실루엣소프트 | en | `Silhouette Soft` · `[]` ✓ | `Silhouette Soft` · `Silhouette InstaLift` · `InstaLift` **✗** | r2-11 |
| ph-126 | 슈링크유니버스 | ja | `シュリンク/ユニバース` · `[]` ✗ | `シュリンク ユニバース` · `ウルトラフォーマーMPT` · `シュリンクユニバース` ✗ | r2-11 · 빗금 |
| ph-126 | 슈링크유니버스 | th · vi | `ชูริงค์ยูนิเวิร์ส` · `Shurink Universe` ✓ / `Shurink Universe` · `[]` ✓ | name 그대로 · 별칭 + `Ultraformer MPT` **✗** | r2-11 |
| ph-046 | 스킨보톡스 | vi | `Skin Botox` · `[]` ✓ | `Skin Botox` · `Micro Botox` · `Meso Botox` **✗** | r2-11 |
| ph-032 · 034 · 052 · 128 · 131 · 141 · 146 | 목주름 · 사각턱 · 미백 · 기기 리프팅 · HIFU · 니들RF · MTS | en | `Neck Wrinkle` · `Square Jaw` · `Whitening / Antioxidant` · `Lifting Device` · `HIFU` · `Needle RF` · `MTS` | **name 그대로**(ph-052 는 빗금만 빼 `Whitening Antioxidant`) · 제안은 alias 로: `Neck Lines` · `Neck Bands` / `Masseter`(**`Jaw Slimming` 은 넣지 않는다 — 처분 §4-e**) / `Skin Brightening` · `Brightening` · `Whitening` / `Skin Tightening` / `Focused Ultrasound` · `Micro-Focused Ultrasound` / `RF Microneedling` · `Radiofrequency Microneedling` / `Microneedling` · `reviewed` 그대로 | r2-12 — 미국 일반어는 ko 뜻과 1:1 판단이 필요(실물 뒤) · ph-034 는 처분 §4-e |
| ph-012 · ph-089 | 토닝 · 물광 | en | `Toning` · `Water Glow` | 그대로 | r2-13 — 미국에 메뉴 없음 |
| kr-008 | 뉴라미스 | zh-Hant | `優美施` · `仙女玻尿酸` … | 그대로 | r1-12 |

D. **yue — 출처 없는 음역 17칸 → 영문**(처분 r1-4 — D-38 ② · D-40 을 yue 에도 · 본 6곳 + 보조 2곳 0건). 음역은 **버린다**(alias 로도 안 둠). `name` = 그 칸 판정이 현지 근거를 댔으면 그 제안, 아니면 그 term 의 en `name`.

| term(ko) | 지금 name(음역) | `.7` name · aliases | `reviewed` |
|---|---|---|---|
| ph-017 피코슈어 | `皮秒舒爾` | `PicoSure` · `[]` | ✓(현지도 영문 · 3곳) |
| ph-018 피코웨이 | `皮秒威` | **`超皮秒`** · `PicoWay` | ✓(변경 · 3곳 — 현지명 근거 있음) |
| ph-126 슈링크유니버스 | `秀靈宇宙` | `Ultraformer MPT` · `鋼筋索` · `Shurink Universe` | ✓(현지도 영문 · 3곳 · D-38 ③ 의 대응) |
| ph-023 엑셀V | `艾克賽爾V` | `Excel V` · `[]` | ✗(1곳) |
| ph-065 실루엣소프트 | `絲路軟線` | `Silhouette Soft` · `鈴鐺線`(출처 1 제안 → alias) | ✗ |
| ph-019 레블라이트 · ph-020 클라리티2 · ph-063 민트리프트 · ph-064 테스리프트 · ph-124 더블로골드 · ph-062 에버라인 · ph-060 미라클 · ph-149 마이셀 · ph-150 셀피아 · ph-151 리젠ACR · ph-153 ASCEplus | `瑞芙光` · `克萊瑞緹2` · `敏特提拉` · `特斯提拉` · `多普勒金` · `艾芙萊恩` · `奇蹟線` · `瑪伊賽爾` · `賽爾皮亞` · `麗珍ACR` · `艾思科+` | en name — `RevLite` · `Clarity II` · `MINT Lift` · `TESSLIFT` · `Doublo Gold` · `Everline` · `Miracle Thread` · `Mycell` · `Cellpia` · `RegenACR` · `ASCE+` · aliases `[]`(지금 별칭이 새 name 과 같거나 대소문자만 달라 빠진다) | ✗(R2 · `note` = 현지 출처 없음) |
| ph-154 EXOSOME SKIN | `艾克索姆肌膚` | `ExoSCRT` · `EXOSOME SKIN` | ✗ |

E. **빗금만 뺀 `name` 31칸**(처분 r2-14 · 한 낱말 제안이 없는 칸 — 값은 그대로 · `/` · `／` 자리만 빈칸 · `reviewed` 그대로 · `source: "manual"`). 한 낱말 제안이 있는 빗금 칸(ja ph-034 · 055 · 078 · 086 · 102 · 103 · th ph-085 · 103 · vi ph-103 · 114 · en ph-114)은 ① 「변경」 으로 바뀐다.

| 언어 | 칸 |
|---|---|
| en 4 | ph-052 `Whitening Antioxidant` · ph-076 `Collagen New` · ph-077 `Exosome Growth Factor` · ph-158 `PRP Autologous Blood` |
| ja 5 | ph-004 `ザ チェウム` · ph-030 `ザ トキシン` · ph-077 `エクソソーム 成長因子` · ph-126 `シュリンク ユニバース` · ph-140 `HIFES EMS` |
| zh 7 | ph-076 `胶原蛋白 新产品` · ph-077 `外泌体 生长因子` · ph-085 `干细胞 再生` · ph-103 `药物 外用` · ph-114 `胶原蛋白增生剂 再生针剂` · ph-118 `PDLLA 聚双旋乳酸` · ph-158 `PRP 自体血` |
| zh-Hant 5 | ph-057 `維他命B C D注射` · ph-076 `膠原蛋白 新產品` · ph-077 `外泌體 生長因子` · ph-103 `藥物 外用` · ph-158 `PRP 自體血` |
| th 3 | ph-076 `คอลลาเจน ใหม่` · ph-077 `เอ็กโซโซม โกรทแฟคเตอร์` · ph-158 `PRP เลือดตัวเอง` |
| vi 2 | ph-076 `Collagen Sản phẩm mới` · ph-077 `Exosome Growth Factor` |
| yue 5 | ph-076 `膠原蛋白 新產品` · ph-077 `外泌體 生長因子` · ph-085 `幹細胞 再生` · ph-103 `藥物 外用` · ph-158 `PRP 自體血` |

F. **대만어(zh-Hant) 별칭 정리 — D-53 · 처분 §6**(0.8.3 다시 씀 — 조사 r3 이 나왔다) — zh-Hant 별칭은 **대만 현지 클리닉에서 쓰임이 확인된 것만 남긴다**(이번 조사 대만 6곳 · 10-27 대만 조사). 근거 없는 별칭은 뺀다. **term 은 하나도 빼지 않는다** · `name` 은 건드리지 않는다.

| 항목 | 계약 |
|---|---|
| 값의 원천 | 조사 r3 — `orchestration/work/interpreter-idea/quality-r3-tw-alias.json` · `quality-r3-tw-alias-report.md`. **245행 = 시드 `.6` 의 zh-Hant 별칭 전부**(한 행 = term × 별칭 낱개 하나 · 빠진 별칭 0). 어느 별칭이 빠지는지는 이 파일이 정한다(planner · backend 가 고르지 않는다) |
| 필드 | `id`(term) · `alias`(별칭 — 시드와 글자 그대로 견준다) · `verdict`(아래 넷 중 하나 — 문자열 그대로) · `sources`(출처 URL 목록) · `note`(이유) |
| 규칙 | **`verdict` 가 `뺌` 인 행의 별칭을 그 term 의 zh-Hant `aliases` 에서 지운다.** 나머지 세 판정은 F 가 건드리지 않는다(아래 표). 다른 6개 언어 · zh-Hant `name` · `reviewed` 는 이 규칙으로 바뀌지 않는다. `id` 가 합쳐져 사라진 term(ph-106)이면 남는 term(ph-105)의 별칭에서 찾는다 |
| 적용 순서 | ① · ② A ~ E 를 먼저 적용한 뒤 F. **F 는 지우기만 한다** — ① 이 이미 뺀 별칭을 r3 「유지」 로 되살리지 않는다. 같은 별칭을 ① 은 남기고 r3 은 `뺌` 이라 하면(「읽는 법」 j 의 `提亮` 등) **r3 을 따른다**(별칭 낱개를 본 조사가 더 좁다) |
| `source` · `note` | 별칭만 빠진 entry = `source` 그대로 · `note` 그대로(값의 출처가 바뀐 것이 아니다). 대조표에 「D-53 뺌」 으로 낱개를 적는다 |
| 개수(계산 2026-11-14) | zh-Hant 별칭 낱개 247(F 앞) → **167**: `뺌` 77 + 옛 name 3 = **80개 · 64칸**(0.8.4). `뺌` 77행은 모두 ① · ② A ~ E 뒤에도 그 term 의 별칭으로 남아 있다(못 찾는 행 0). ③ 표의 「zh-Hant(F 뒤)」 행 |
| 한도 | **D-53 정리 뒤에도 zh-Hant 는 기준을 넘는다**(§4.6 「시드 `.7` 추정」 — 667자 · `terms` 61 · 역방향 별칭은 0). 넘는 만큼은 D-54 가 다룬다(§4.6 「D-54 절차」) |

**r3 판정 넷 → 처리**(처분 §6)

| `verdict` | 행 | 처리 |
|---|---|---|
| `유지 — 이번 6곳` | 138 | 그대로 |
| `유지 — 10-27 근거` | 23 | 그대로. **D-54 의 zh-Hant 첫 후보** — WP23 v6 재측정 뒤에도 zh-Hant 가 한도를 넘으면 이것부터 뺀다(§4.6 「D-54 절차」). 23 가운데 `.7` 에 남는 것은 **22**(ph-034 `下顎角瘦臉針` 은 ① · 읽는 법 d 로 이미 빠진다) |
| `뺌` | 77 | **지운다**(D-53) — r3 판정대로: 한국 플랫폼(강남언니 · creatrip)뿐인 13 · 글자는 있으나 뜻이 다른 3(`提亮` · `LED` · `InMode`) · 리쥬란 `麗珠蘭白盒` · `麗珠蘭紅盒` 포함(`麗珠蘭黑盒` 은 「유지 — 이번 6곳」 — 한 묶음으로 r3 판정 그대로). 되살리지 않는다 |
| `다른 term 과 겹침` | 7 | **건드리지 않는다**(빼도 context 글자 수 0) — ph-042 보툴렉스 4(`Letybo` · `白毒` · `輕齡肉毒` · `精品肉毒` = ph-031 레티보와 같은 별칭 · D-38 ① 의 의도된 겹침 → 남는다) · ph-106 2(`冷凍溶脂` · `酷塑` — ② B 로 ph-105 에 합쳐지는데 ph-105 에 이미 같은 별칭이 있어 옮길 것 0) · ph-019 `雷射` 1(① · 읽는 법 d 가 이미 뺐다 — F 가 되살리지 않는다) |

**별칭으로 내려오는 옛 zh-Hant `name` 에도 D-53 을 적용한다**(처분 §6) — r3 의 245행은 `.6` 의 별칭만 본다. ① 로 `name` 이 바뀌어 alias 로 내려오는 옛 `name` 은 **7개**다. 대만 근거(r1 칸 메모 · r3 · 10-27 대만 조사 `orchestration/work/_archive/interpret-pwa/interpret-pwa-poc/research-tw-names-report.md`)가 있을 때만 별칭으로 남긴다. **남김 4 · 뺌 3**(0.8.4 — 처분 §7 W-3 으로 `瘦臉針` 도 뺀다).

| term(ko) | 옛 `name` | 대만 근거 | `.7` |
|---|---|---|---|
| ph-013 혈관 | `血管雷射` | 10-27 — 대만 공식 2곳(지자체 수가표 · 대학병원 자료) · 이번 6곳은 0건 | 별칭으로 남김 |
| ph-019 레블라이트 | `淨膚雷射` | r1 — S1 1곳(장비명과 나란히 씀) | 남김(읽는 법 c) |
| ph-034 사각턱 | `瘦臉針` | 10-27 — 그 행 출처 3 가운데 대만 매체 1(나머지 2 는 한국 플랫폼 · 출처는 행 단위) · 이번 6곳은 0건. D-53 의 「대만 현지 클리닉」 근거가 아니고, 부위 term 의 시술 이름이라 §4-e 와도 같은 꼴(처분 §7 W-3) | **뺌** — `.7` = `國字臉` · `瘦小臉` · `咀嚼肌` |
| ph-058 지방분해주사 | `溶脂針` | r1 — S1 1곳 | 남김 |
| ph-102 탈모(비수술) | `脫髮` | r1 — S6 1쪽 | 남김 |
| ph-098 여드름 전용 | `痘痘專用` | **없음** — r1: 다른 낱말의 일부로만 걸림(직역) · 10-27 「찾지 못함」 | **뺌** — `.7` = `痘痘治療` · `青春痘治療` |
| ph-100 흉터 전용 | `疤痕專用` | **없음** — r1 6곳 0건(직역) · 10-27 「찾지 못함」 | **뺌** — `.7` = `除疤` · `疤痕治療` |

- ① 로 **새로 더하는** zh-Hant 별칭 4개(ph-034 `咀嚼肌` · ph-098 `青春痘治療` · ph-100 `疤痕治療` · ph-102 `掉髮`)는 이번 조사 r1 이 대만 사이트에서 본 것이라 그대로 둔다. 0.8.2 의 「새로 더한 zh-Hant 별칭 11개」 = 이 4개 + 위 옛 name 7개다.

- 그대로 두는 처분(값 변화 없음): r1-5 리쥬란 갈래 · r1-8 대륙 플랫폼 보조 조사(지금 안 함) · r1-9 한국 상품 · 분류 이름 직역(못 찾음 그대로) · r1-11 · r1-12 · r2-4(ja 가타카나) · r2-13.

**확인된 오류 E1 ~ E11 — 처분 결과** (BASE-001 「확인한 사실 (코디 2026-11-14)」)

| # | term · 언어 | `.7` |
|---|---|---|
| E1 | ph-012 토닝 · zh `提亮` | **`调Q激光`** · alias `激光嫩肤`(D-52 · ② C) |
| E2 | ph-012 토닝 · yue `調色` | `淨膚激光`(② C) |
| E3 | ph-010 색소 · ph-012 토닝 · ja 뒤바뀜 | `シミ治療` / `レーザートーニング`(② C) |
| E4 | ph-026 턱선 · ja `顎ライ` | `フェイスライン`(② C) |
| E5 | 「써마지」 맨 이름 | 새 term `kr-014`(D-51 · ② A) |
| E6 | 리투오 | 새 term `kr-015`(② A) |
| E7 | ph-121 울쎄라 · zh 별칭 `Ultherapy` | **그대로 — ㉔ 결과 뒤 코디 처분**(② C). en 은 `Ultherapy` name |
| E8 | zh `激光` ×4 | 장비 셋은 영문 name · ph-014 만 `激光`(② C) |
| E9 | zh `水光针` ×2 | 그대로(② C) |
| E10 | 시그니처프로그램 중복 | ph-097 로 합침(② B) |
| E11 | zh `乐提葆` ×2 | 유지(Q4) |

**③ 기계 적용 결과 — 언어별 개수** (planner 계산 2026-11-14 · **0.8.3 다시 계산 — 처분 §4-e · 조사 r3 반영**. 시드 `.6` + 두 `cells.json` + r3 JSON + 처분에 ① · ② 와 아래 「읽는 법」 을 적용. 셈 단위 = **칸**(entry) · 괄호 = 별칭 **낱개 수**. 바탕 = 합친 뒤 남는 기존 term 168개 × 7 = 1,176칸 — 사라지는 ph-106 · ph-127 의 14칸과 새 term 14칸은 따로. 위 일곱 줄과 「합(F 앞)」 은 ② F 를 적용하기 **전** 값이다 — F 는 zh-Hant 만 바꾼다)

| 언어 | `name` 바뀜 | alias 더함 | alias 뺌 | `reviewed` ✗ → ✓ | ✓ → ✗ | 바뀐 칸 | 안 바뀐 칸 | 반영 안 함(vi S3 단독) |
|---|---|---|---|---|---|---|---|---|
| en | 10 | 35 (50) | 0 | 1 | 2 | 38 | 130 | — |
| ja | 30 | 34 (48) | 0 | 8 | 4 | 46 | 122 | — |
| zh | 19 | 21 (32) | 0 | 2 | 8 | 33 | 135 | — |
| zh-Hant | 12 | 7 (11) | 2 (4) | 40 | 0 | 48 | 120 | — |
| th | 68 | 61 (85) | 1 (1) | 1 | 25 | 86 | 82 | — |
| vi | 20 | 28 (44) | 0 | 10 | 3 | 40 | 128 | **0** |
| yue | 40 | 28 (36) | 2 (2) | 4 | 14 | 52 | 116 | — |
| **합(F 앞)** | **199** | **214 (306)** | **5 (7)** | **66** | **56** | **343** | **833** | **0** |
| zh-Hant(**F 뒤** — D-53) | 12 | 7 (8) | **62 (81)** | 40 | 0 | **98** | 70 | — |
| **합(F 뒤)** | **199** | **214 (303)** | **65 (84)** | **66** | **56** | **393** | **783** | **0** |

- **0.8.2 와의 차이 = 처분 §4-e 뿐이다**(읽는 법 e 의 9칸): `name` 201 → 199(th ph-034 · yue ph-034) · alias 더한 칸 220 → 214(th 4 · ja 1 · yue 1 — 낱개 319 → 306) · 바뀐 칸 349 → 343 · `reviewed` 66 / 56 그대로. 0.8.2 3차 검수의 독립 재계산(199 · 214 · 343)과 같다.
- 읽는 법: 「alias 더함」 은 alias 로 내려간 옛 `name` 도 센다 · 「alias 뺌」 은 새 `name` 이 된 별칭을 세지 않는다 · **옛 `name` 이 alias 로도 남지 않은 칸** = en 4 · ja 17 · zh 11 · zh-Hant 5 · th 32 · vi 3 · yue 26 = 98(빗금 정리 31 포함 · F 뒤에는 zh-Hant 8 · 합 101). 한 칸이 여러 칸에 같이 든다(`name` 바뀜 + alias 더함). 「F 뒤」 행은 `.6` 대비다 — alias 뺌 낱개 81 = F 앞 4 + r3 `뺌` 77 · alias 더함 낱개 11 → 8 은 옛 name 3개(`痘痘專用` · `疤痕專用` · `瘦臉針`)를 별칭으로 내리지 않아서다.
- 별칭 낱개(168 term): en 4 → 54 · ja 75 → 121 · zh 76 → 105 · zh-Hant 243 → 247(F 앞) → **167**(F 뒤) · th 65 → 118 · vi 0 → 44 · yue 44 → 64. 7개 언어 합 507 → 753(F 앞) → 673(F 뒤). `reviewed: true` 칸(168 term · `.7`): en 147 · ja 160 · zh 123 · zh-Hant 96 · th 135 · vi 139 · yue 149.
- 판정별: 변경(`n` ≥ 2) 87 · 변경(`n` = 1) 6 — zh ph-043 · 090 · 114 · 122 · ja ph-042 · vi ph-035 · 별칭 추가 70 · 유지에서 `reviewed` 만 오른 칸 49(zh-Hant 32 · vi 10 · ja 3 · zh 2 · th 1 · yue 1) · 현지도 영문으로 name 이 바뀐 칸 41(th 36 · ja 2 · yue 2 · zh-Hant 1) · th 「현지에 없음 → 영문」 15.
- 같은 언어 안 이름 겹침(term 쌍이 아니라 겹치는 `name` 의 수): en 2 → 0 · ja 1 → 0 · zh 5 → 2 · zh-Hant 11 → 8 · th 1 → 0 · vi 0 → 0 · yue 3 → 1. 새로 생기는 겹침 0(F 는 `name` 을 안 건드려 그대로).
- **WP23 의 스크립트 결과가 이 표와 다르면 멈추고 코디에게 올린다** — 차이가 「읽는 법」 의 어느 항목에서 났는지 대조표로 가린다(시험에는 개수 고정값을 두지 않는다 — 표 ② 대조 · 0.6.0 방식). D-54 로 뺀 별칭(§4.6 「D-54 절차」)은 이 표에 넣지 않고 대조표에 따로 적는다.

**기계 적용 — 읽는 법 (처분이 말하지 않은 자리 · OQ-030 — **코디 처분 §4 로 닫힘**(0.8.3): a · b · c · d · f ~ k = planner 기본값 그대로 · **e 만 바꿈**. 위 개수는 이 읽는 법의 값이다)**

| # | 자리 | 지금 읽는 법(개수에 반영) | 걸린 칸 |
|---|---|---|---|
| a | 「변경」 · 「현지도 영문」 칸에서 리포트가 옛 `name` 을 aliases 목록에 **안 적은** 칸 — 처분 §1 은 「옛 name 은 alias(뜻이 틀린 값은 §2)」 | **리포트 목록대로 — alias 로 내리지 않는다**(직역 0건 · 긴 풀이말 · 빗금 꼴 — R3 예외 「결함 값」 · R5) | §2 · R3 로 닫히지 않는 것 **13칸**(0.8.4 — yue ph-034 는 §4-e 로 name 이 안 바뀌어 빠진다): yue ph-058 `脂肪分解注射` / ja 빗금 꼴 6(ph-034 · 055 · 078 · 086 · 102 · 103) / th ph-022 · ph-085(빗금) · ph-094 · 096 · 100(풀이말) / vi ph-114(빗금). 내리기로 하면 별칭 낱개 + 14 |
| b | 「별칭 추가」 칸의 `reviewed` — 처분 §1 은 「alias 에 더함」 뿐 | **그대로 둔다**(r2 의 출처 수는 별칭이 나온 사이트일 수 있다) | `n` ≥ 2 인데 지금 ✗ 인 15칸(en 8 · ja 1 · th 2 · vi 4) — 「유지」 처럼 올리면 ✗ → ✓ 합 81 |
| c | 「현지도 영문」 의 「옛 현지 문자 값은 출처가 있으면 alias, 없으면 버림」 — 칸에 그 값의 출처 수 칸이 없다 | **버리는 칸을 id 로 못 박는다**(0.8.3 · W-3 — 리포트 메모 문구에 기대지 않는다). 「현지도 영문」 으로 `name` 이 바뀌는 칸 가운데 **오른쪽 28칸은 옛 현지 문자 값을 버린다**(리포트 별칭 목록에 있어도 alias 로 두지 않는다 — 조사 메모가 그 값이 현지 사이트에 없다고 적은 칸). 그 밖의 칸은 리포트 목록(`proposed_aliases`)대로 | **버림 28** — th 24: ph-005 · 006 · 007 · 015 · 017 · 018 · 027 · 031 · 042 · 064 · 065 · 072 · 075 · 078 · 079 · 088 · 107 · 117 · 118 · 119 · 122 · 123 · 154 · 156 / yue 2: ph-015 · ph-157 / ja 2: ph-118 · ph-119. **alias 로 남김 12** — th 11: ph-009 · 012 · 037 · 039 · 071 · 120 · 135 · 141 · 146 · 153 · 157 / zh-Hant ph-019(+ 사라지는 ph-106 의 th · vi 두 칸도 남김 — ② B 로 ph-105 에 옮겨 온다). 나머지 1칸 th ph-022 는 a(리포트 목록에 옛 name 이 없다) — 28 + 12 + 1 = 41 |
| d | r1 「변경」 칸의 `proposed_aliases` 는 전체 목록 — 지금 별칭이 줄어드는 칸 | 리포트 목록대로 바꾼다 | zh-Hant ph-034(`咬肌` · `咀嚼肌肉毒` · `下顎角瘦臉針` 빠짐) · ph-019(`雷射` 빠짐). r3 은 `下顎角瘦臉針` 을 「유지 — 10-27 근거」 · `雷射` 를 「다른 term 과 겹침」 으로 보지만 ② F 는 지우기만 한다 — ① 이 뺀 것을 되살리지 않는다 |
| e | 처분 r1-11(부위 term 에 시술 이름 별칭 안 넣음)은 **zh 3칸**만 말한다 | **(0.8.3 · 처분 §4-e — planner 기본값을 바꿈) 7개 언어 전부에** — 부위 term 에 시술 이름을 `name` · alias 로 **새로 넣지 않는다**(역방향이 「시술 이름 → 부위」 가 된다). `.6` 에 이미 있는 그런 값은 그대로(이번 판은 더하지만 않는다). 제안 `name` 이 시술 이름인 칸은 칸 전체를 반영하지 않는다 | **9칸 — 칸마다의 `.7` 값은 ② C.** 제안 별칭만 뺌 7칸: ja ph-034 `エラボトックス` · ja ph-035 `肩ボトックス` · th ph-029 `โบท็อกรักแร้` · th ph-035 `โบท็อกบ่า` · `ลดบ่า` · th ph-038 `ลดน่อง` · en ph-034 `Jaw Slimming` · vi ph-034 `Gọn hàm` / 칸 전체 그대로 2칸: th ph-034(제안 name `ลดกราม`) · yue ph-034(제안 name `瘦面針`). 부위 term(보톡스 카테고리의 ph-024 · 025 · 026 · 029 · 032 · 034 · 035 · 036 · 038 · 043) × 7개 언어의 제안을 전부 훑었다 — 이 9칸과 zh 3칸(r1-11) 밖에는 시술 이름 제안이 없다 |
| f | 리포트가 더하자고 한 별칭이 §4.2.1 모호어 목록(R4)에 걸림 | **더하지 않는다**(목록은 그대로 — 시험이 막는다) | zh ph-141 `黄金微针` · yue ph-141 `黃金微針`(리포트: 「일반 term 인 니들RF 에는 맞는 뜻」) |
| g | yue ph-126 — 판정 「현지도 영문 → `Ultraformer MPT`」(3곳) 대 처분 r2-11 「제품 대응은 alias 로만」(en · ja · th · vi) | **① 규칙대로 name**(홍콩 3곳이 그 이름을 메뉴명으로 씀 · r2-11 은 r2 언어의 처분) | 1칸 |
| h | 처분 r1-2 「장비는 영문 name」 은 zh `激光` 을 말한다 | **zh 3칸만**. zh-Hant ph-019 는 ① 「현지도 영문」(1곳)으로 `RevLite` · ph-020 · ph-023 `雷射` 는 「못 찾음」 → 그대로(겹침 남음) | zh-Hant 2칸 |
| i | 처분 §2 가 name · alias 를 적은 칸의 **리포트 나머지 별칭** | 더한다(§2 가 빼라고 한 말만 뺀다) | ja ph-010 `シミ取り` · ph-003 `ヒアルロン酸注射` · en ph-121 `Ultherapy PRIME` |
| j | zh-Hant ph-012 의 별칭 `提亮` — D-52 는 zh 만 정했다 | ① 로는 그대로 — **② F 가 정한다: r3 판정 `뺌`(효과 서술뿐) → 빠진다** | 1칸 |
| k | 새 term `kr-014` 의 `reviewed` — D-51 은 값만 정했다 | R7(세대 없는 이름을 쓴 사이트 수 2+ 면 ✓) | zh-Hant · vi ✗ |

**처분 절차 — 기록** (0.8.0 에서 정한 순서 그대로 지나왔다)

1. **조사**(researcher · read-only · 2026-11-14) — r1(zh · zh-Hant · yue) · r2(en · ja · th · vi) 리포트 + `cells.json`. 판정 말 = 유지 · 변경 · 별칭 추가 · 현지도 영문 · 현지에 없음 → 영문 · 못 찾음 · 처분과 다름.
2. **코디 처분**(2026-11-14 확정 · 사용자 「추천으로 가고」 → D-51 · 토닝 zh = D-52) — `quality-research-dispositions.md` §1(칸 판정 → 반영 규칙) · §2(정할 것 29건).
3. **이 절**(planner · 0.8.2) — 규칙 · 손 처분 칸 · 개수.
4. **조사 r3**(researcher · 2026-11-14) — 대만어 별칭 245행 판정 · **코디 처분 §4 ~ §6 · D-54**(2026-11-14 — OQ-030 은 e 만 바꿈 · r3 판정 넷의 처리 · 한도) → **이 절 다시 계산**(planner · 0.8.3).
5. **시드**(backend · WP23) — 변환 스크립트(`back/scripts/` · 네 파일의 경로를 인자로) → `version` = **`2026-11-14.7`** → 대조표(바뀐 칸 전부) · 시드 검사 · §4.6 재측정.

- 기계 점검(`.6` · BASE): 그 언어 글자가 없는(영문만) `name` — zh 40 · zh-Hant 27 · yue 54 · th 23 · ja 7. `reviewed: false` — zh-Hant 113 · zh 39 · vi 36 · en 20 · ja 13 · th 9 · yue 9.
- 역방향은 같은 이름이면 처음 것 하나만 남는다(§4.5 — 역방향 기본이 별칭보다 앞).
- 따라 고친 자리(0.8.2): §4.2 `version` · `id` 규칙 · §4.2.1 모호어 목록 · 「지금까지 반영한 판」 · §4.6 「시드 `.7` 추정」. (0.8.3) ② C 의 §4-e 칸 · ② F · ③ · 읽는 법 c · d · e · j · §4.6 「시드 `.7` 추정」 · 「D-54 절차」 · §10 OQ-030 닫음. **따라 고칠 자리(WP23 뒤)**: §4.6 언어별 표(다시 재면) · §9.3 「6차」 손님 쪽 문장의 시술명.

### 4.2.5 시드 `.8` — 틀린 꼴 첫 목록 (0.9.0 — D-58)

> 품질 시험 6차(§9.3 「6차 결과」)에서 **사전 값이 context 에 들어갔는데도 사전대로 나오지 않은 칸**의 틀린 꼴을 시드에 적는다 — 바로잡기(§5.12)의 ① 단계 재료다. **이 문서에는 번호 · term · 언어만 적는다** — 꼴 자체는 시드에만(시험 결과의 원문 · 번역은 로컬 전용 · DEC OQ-021).

| 항목 | 계약 |
|---|---|
| `version` | **`2026-11-15.8`** |
| 바뀌는 것 | **`wrong` 을 더하는 것 + 아래 두 가지**(0.9.2 — D-60 · 처분 §13 ① · 코드 검수 W-3. 0.9.1 까지의 「틀린 꼴을 더하는 것뿐」 을 고친다) — term 수(170) · `id` · `ko` · `ko_aliases` · 배열 순서는 `.7`(D-54 로 27개 뺀 판 — WP23 결과) 그대로 · 그 밖의 칸의 `name` · `aliases` · `source` · `reviewed` · `note` 도 그대로. **ⓐ kr-014 써마지 zh-Hant(D-60)**: `name` = `熱瑪吉`(현지 글자) · 영문 옛 name 은 별칭으로 · `reviewed: true` · `note`(조사 r1 의 대만 클리닉 2곳 — D-51 의 영문 name 을 고침 · D-46 「현지어 우선 · 출처 2+ 면 reviewed」) **ⓑ ph-033 보톡스 zh · yue(처분 §13 ①)**: 별칭 1개씩 더함(현지 메뉴 낱말의 앞부분 — 번역에 그 낱말이 든 꼴이 맞는 이름으로 잡혀 바로잡기를 부르지 않는다) · `source` = `manual`(§4.2.4 「합치기로 별칭만 는 칸」 규칙) · `note` = 처분 문구 + 옛 출처 URL(처분 §14 W-3 — 지우지 않는다). **context 글자 수는 세 언어에서 는다**(zh +35 · zh-Hant +31 · yue +35 — §4.6 「시드 `.8` ~ `.10` 의 글자 수」) · 나머지 4개 언어는 `.7` 과 같다. 틀린 꼴 자체는 context 재료가 아니다 |
| 꼴의 원천 | 로컬 결과 `reference/2026-11-12-interpreter-idea/quality-run/*-local.json`(WP22 · WP24 — 조합 A · B · C · C2 · 손님 쪽 · 울쎄라 가르기) — backend 가 아래 표의 칸에서 **그 term 자리에 실제로 나온 꼴**을 뽑는다. 로컬 결과에 없는 꼴을 짓지 않는다(음역 · 추측 0) |
| 뽑는 범위 | 아래 표의 **term · 언어 칸**에 한해, 그 칸이 걸린 모든 실행(조합 · 다시 돌린 것 포함)에서 나온 꼴. 표 밖 칸은 이번 판에 넣지 않는다 |
| 넣지 않는 것 | ⓐ 그 언어의 맞는 이름 · 별칭과 같은 꼴(검사 8 ⓓ · ⓔ) ⓑ **STT 가 원문을 잘못 들어서 생긴 꼴**(원문에 term 이 걸리지 않은 발화 — 바로잡기의 대상이 아니다 · §5.12 「걸리는 조건」) ⓒ 문장 전체 · 여러 낱말에 걸친 풀이(그 term 자리의 낱말 · 이름 꼴만) ⓓ **(0.9.1 · 처분 §11) `ko_wrong` 에 일상 한국어 낱말** — 다른 시술 · 장비 이름처럼 한국어 문장에서 제 뜻으로 흔히 쓰이는 낱말은 넣지 않는다. 그런 칸은 바로잡기로 닫지 않고 **실패로 남긴다** |
| 확인 | backend 가 뽑은 목록(term · 언어 · 꼴 · 나온 번호)을 **로컬 대조표**(git 제외 폴더)로 내고 **코디가 확인한 뒤** 시드에 넣는다. 레포용 보고에는 term · 언어 · **개수**만 |
| 뒤에 더할 때 | 운영 로그 「바로잡지 못함」(§5.12) · 7차 결과(§9.3)에서 새 꼴이 나오면 같은 절차(로컬 대조표 → 코디 확인 → 시드 PR · `version` 올림)로 더한다 |

**첫 목록의 칸**(6차 조합 C · C2 기준 — 사람 판정 「사전대로 안 나옴」 · `wp24-human.json`)

| 시험 번호 | term | 언어 | 방향 | 필드 |
|---|---|---|---|---|
| T02 · T03 | ph-121 울쎄라 | zh | 한 → 외 | `entries.zh.wrong` |
| T03 | kr-014 써마지 | zh | 한 → 외 | `entries.zh.wrong` |
| T04 | ph-112 스컬트라 | zh | 한 → 외 | `entries.zh.wrong` |
| T30 | ph-042 보툴렉스 | zh | 한 → 외 | `entries.zh.wrong` |

- **실제로 들어간 목록(0.9.2 · 처분 §12 · §13 ② · §14 W-1 · WP26 수정 2)** — 위 표는 0.9.0 이 6차 조합 C · C2 에서 짚은 칸이고, 코디가 확인한 첫 목록은 **다국어 묶음(D-57 · 조합 C)에서 나온 칸까지** 넣었다: **틀린 꼴 40개 · 16칸**(term 6 — ph-121 · kr-014 · kr-015 · ph-112 · ph-012 · ph-042 · 언어 7개에 걸침 · 검사 8 로 뺀 꼴 4 · `ko_wrong` 0). 칸마다의 개수는 `wp26-be-report.md`(term · 언어 · 개수만) · 꼴은 시드에만. **T04 칸(ph-112 zh)은 뺐다**(처분 §14 W-1 — 그 꼴이 일상 낱말이라 같은 발화의 제 뜻 낱말까지 바뀐다 · 아래 「일반 낱말」 줄의 경우 · 그 칸은 「못 찾음」 으로 남는다). zh-Hant 써마지의 영문 꼴은 ⓐ 로 별칭이 되어 틀린 꼴이 아니다.
- **넣지 않는 칸(0.9.1 · 처분 §11)**: 손님 쪽 **T46(th · ph-121)** — 원문의 현지 이름은 걸렸지만 한국어 번역에 나온 것이 **다른 시술 · 장비를 가리키는 일상 한국어 낱말**이다(위 ⓓ). `ko_wrong` 에 넣지 않는다 → 바로잡기는 「못 찾음」 으로 남기고 로그 1줄이 난다. **첫 목록의 `ko_wrong` 은 0개다**(필드 · 검사 · ① 단계는 그대로 둔다 — 뒤에 한국어 틀린 표기가 나오면 넣는다).
- **넣지 않는 칸**: 손님 쪽 **T34(en) · T49(vi)** — 사람 판정 「인식」(손님 말의 영문 상표를 STT 가 다른 낱말로 들음). 원문에 term 이 걸리지 않아 바로잡기가 돌지 않는다 — 틀린 꼴로 풀 수 없는 갈래다(§9.3 「6차 결과」 · OQ-017).
- 위 칸의 꼴이 일반 낱말(다른 뜻의 낱말)일 수 있다(T04 — zh `wrong`). 바로잡기는 **원문에 그 term 이 걸리고 번역에 사전 이름이 없을 때만** 그 낱말을 갈아 끼우므로 일반 문장에서는 돌지 않는다 — 그래도 같은 발화 안에서 그 낱말이 제 뜻으로 쓰인 경우는 잘못 바꾼다. 코디 확인에서 그런 꼴을 빼도 된다(뺀 꼴은 대조표에 「뺌」 으로).
- 그 밖의 언어(ja · zh-Hant · th · vi · yue · en 직원 쪽)는 6차에 문장이 없어 틀린 꼴을 모른다 — **7차(§9.3)가 낸다**. 그 전에는 §5.12 의 ② · ③ 단계가 받는다. (0.9.2 — 다국어 묶음에서 나온 꼴은 위 「실제로 들어간 목록」 에 이미 들었고, 7차가 낸 꼴은 §4.2.7 시드 `.10` 이다.)

### 4.2.6 시드 `.9` — 영문 `name` 을 그 나라 글자로 (0.9.2 — D-61 · D-62 · 처분 §15)

> 「원칙이 해당 나라 언어 글자로 표기」(사용자 2026-11-15 · D-61). 시드 `.8` 에 **그 나라 글자가 있는 언어인데 `name` 이 영문인 칸**이 ja 9 · zh 42 · zh-Hant 29 · th 74 · yue 65 있었다(시드에서 센 값 — `seed-v9-be-report.md`. D-61 본문의 zh-Hant 30 · th 75 와 1씩 다르다 — 이 문서는 시드에서 센 값을 쓴다). 조사 r4a(zh · zh-Hant · yue) · r4b(th · ja)가 이 칸들을 다시 보았고 코디 처분 §15 가 값을 정했다. **이 문서에는 규칙과 개수만 적는다 — 칸 목록(id · 언어 · 옛 name → 새 name · reviewed · 별칭 수)은 `orchestration/work/interpreter-idea/seed-v9-diff.json` 이 정본이다.**

| 항목 | 계약 |
|---|---|
| `version` | **`2026-11-15.9`** |
| 대상 언어 | **ja · zh · zh-Hant · th · yue**(그 나라 글자가 있는 언어 — D-61). **en · vi 는 그대로**(D-46 규칙 그대로) |
| 원칙(D-61 — D-46 을 좁힘) | 그 나라 글자 표기가 **현지 클리닉 · 현지 의료미용 플랫폼**(손님이 보는 표기 — 플랫폼은 이 조사에서만 근거로 친다)에 있으면 그것이 `name` · **영문 옛 `name` 은 별칭으로 내린다**. 「현지 클리닉도 영문을 쓴다」 만으로는 영문 `name` 을 두지 않는다. **지어내지 않는다** — 근거 없는 음역 · 별명은 쓰지 않는다. 그래도 없으면 영문 `name` 그대로(7차 결과 페이지에 「현지 표기 없음」) |
| `reviewed` | 근거 **1곳 이상이면 `name`** · **2곳 이상이면 `reviewed: true`**(D-62 — 조사의 제안값이 아니라 출처 수로 · 조사가 false 로 둔 6칸이 true 가 됐다) · 1곳이면 `reviewed: false` |
| 그 밖의 필드 | `source` = `web-research 2026-11-15` · `note` = 그 칸의 첫 출처 URL · 별칭 순서 = 지금 별칭 → 옛 name → 제안(§4.2.4 ① 과 같다) · name 이 바뀐 entry 의 옛 `raw` 는 지운다(`.7` 과 같은 처리) |
| 쓰지 않는 것(처분 §15) | ⓐ **여러 기기 · 제품을 가리키는 말**(D-35 모호어 — name · 별칭 모두) ⓑ **다른 제품에도 쓰이는 시장 이름**(「~針」 류 — 그 이름이 다른 제품에 안 쓰일 때만 name) ⓒ 기술 설명뿐인 표기 ⓓ 영문 뒤에 붙인 설명이 1곳뿐인 꼴 ⓔ 더 넓은 뜻의 말 · 꾸밈말 |
| 현지 글자로 치는 것(처분 §15) | ⓐ 영문 + 현지 글자가 섞였어도 클리닉 · 플랫폼이 **통째로 쓰는 이름** ⓑ 상품명으로 쓰이는 상자 색 이름(zh 와 같은 처리) ⓒ **일반어(PN · PDRN · PRP 류)는 현지 글자 일반 명칭이 name** · 영문 약어는 별칭 |
| 갈릴 때 | 표기가 둘이면 출처 많은 쪽 · 같으면 지금 별칭과 같은 쪽 — 나머지는 별칭 |
| 근거 없는 별칭 | **뺀다**(D-53 원칙을 zh · th 에도 — 처분 §15 r4a-9 · r4b-9). term · name 은 건드리지 않는다 |
| 틀린 꼴(`wrong`) | 그대로 둔다 — 바꿀 대상은 늘 그 칸의 `name` 이라 새 name 으로 따라간다. 새 name · 별칭과 겹치는 꼴만 뺀다(검사 8) — **이 판에서 겹쳐 뺀 꼴 0** |
| 만드는 법 | 변환 스크립트 `back/scripts/seed_v9.py`(입력 = `.8` + 조사 파일 — 경로는 인자로만 · 재실행 같은 바이트 · 끝에 로더 검사) — 표를 손으로 옮기지 않는다 |

**개수**(`seed-v9-be-report.md` · `seed-v9-diff.json`)

| 언어 | `name` 바뀜 | 근거 없는 별칭 뺌 | 남은 영문 `name`(`.8` → `.9`) |
|---|---|---|---|
| ja | 6 | — | 9 → 3 |
| zh | 3 | 19 | 42 → 39 |
| zh-Hant | 9 | 0 | 29 → 20 |
| th | 35 | 17 | 74 → 39 |
| yue | 20 | 0 | 65 → 45 |
| en · vi | 0 | — | — |
| **합** | **73** | **36** | 219 → 146 |

- 바뀐 73칸의 `reviewed`: true 55 · false 18(D-62 반영 뒤 · 대조표에서 센 값).
- **반영하지 않은 칸 7**(처분 §15 의 「안 씀」 · 「그대로」): yue ph-108 · ph-017 · kr-003 · ph-123 · zh-Hant ph-136 · zh kr-001 · th ph-078 — 이유는 대조표 `skipped`.
- **7차 시술 9개 가운데 「현지 표기 없음」 으로 남은 칸**(그 언어 `name` 이 영문 — 손님 쪽 문장이 영문 이름으로 말한다): zh — 쥬베룩 · 리투오 / zh-Hant — 리투오 / th — 리투오 / yue — 쥬베룩 · 리투오 · 보툴렉스.
- **context 가 커진다** — 옛 영문 name 이 별칭으로 남아 th · ja · zh-Hant 가 는다. **ja · th 는 기준(「D-56 표」)을 넘어 `terms` 가 빠진다 — D-62 로 그대로 받는다**(§4.6 「시드 `.8` ~ `.10` 의 글자 수」).
- 조사 범위 밖(다음 판): th ph-154(처분 §15 r4b-10) · 대륙 추가 조사는 하지 않는다(r4a-11).

### 4.2.7 시드 `.10` — 7차 틀린 꼴 (0.9.2 — D-63 · 처분 §16)

| 항목 | 계약 |
|---|---|
| `version` | **`2026-11-15.10`** — 지금 판(배포할 판) |
| 바뀌는 것 | **`wrong` 에 7개를 더하는 것뿐** — `name` · 별칭 · term 수 · 순서 · context 글자 수는 `.9` 그대로(틀린 꼴은 context 재료가 아니다) |
| 더한 칸(term · 언어 · 개수만) | kr-015 리투오 — zh 1 · yue 1 · zh-Hant 1 / ph-121 울쎄라 — th 1 / kr-014 써마지 — th 1 · ja 1 / ph-042 보툴렉스 — zh-Hant 1. 검사 8 로 뺀 꼴 0 · 합 40 → **47개** |
| 원천 | 7차 첫 실행(시드 `.9`)의 로컬 결과 · 사람 판정에서 나온 꼴 → 로컬 대조표 → 코디 확인(§4.2.5 「뒤에 더할 때」 절차 그대로) |
| 넣지 않은 것(처분 §16) | ⓐ 일상 낱말(§4.2.5 의 T04 와 같은 원칙) ⓑ **그 나라 글자로 적힌 음역**인데 그 칸의 `name` 이 영문인 경우(th 리투오 — 그 꼴을 영문 name 으로 바꾸면 D-61 과 반대다 · 다음 판 사전 후보) ⓒ 손님 쪽 원문 인식 꼴(원문에 term 이 안 걸린 발화 — 바로잡기 대상 아님) |
| 긴 꼴 먼저 | 한 칸에 **앞부분이 같은 두 꼴**(짧은 꼴 · 긴 꼴)이 있으면 긴 꼴이 먼저 잡혀야 꼬리 글자가 남지 않는다(ja 써마지 칸) — §5.12 ① 「긴 꼴부터」 가 그대로 받는다 · 시험 1건(§9.1 「바로잡기」 ⑯) |
| 만드는 법 | `back/scripts/seed_v10.py`(`.9` → `.10` · 재실행 같은 바이트) |

- 이 판과 함께 바로잡기 ② 가 좁아졌다(§5.12 — D-63). 7차를 `.10` 으로 다시 돌린 결과가 §9.3 「7차 결과」 의 「7차 다시」 다.

### 4.3 기동 때 읽기 (D-33 · D-14 개정)

- back 기동(lifespan) 때 한 번 `load_seed(path) -> Glossary` — 파일 읽기 → §4.2 검사 → 메모리. 다시 읽지 않는다.
- 성공 로그 1줄: `glossary seed loaded: version=… terms=… entries={lang: n…}`(용어 문자열 0).
- `Glossary` 는 순수 데이터(term · entry 목록) — context 조립(§4.5)만 이것을 읽는다(0.5.0 — 메뉴 없음 · D-37). **HTTP 클라이언트 · `GLOSSARY_MATRIX_URL` · `load_glossary`(matrix) 는 back 런타임에서 지운다**(§4.9).

### 4.4 시드가 깨지면 — 기동 실패 (기본값)

| 경우 | 동작 |
|---|---|
| 파일 없음 · 읽기 오류 · JSON 아님 · §4.2 검사 실패 | **back 기동 실패** — lifespan 이 `SeedError` 를 올려 프로세스가 0 아닌 코드로 끝난다. 오류 로그 1줄 = 무엇이 틀렸나(필드 경로 · term `id` · 규칙 이름). 시드 값은 공개 데이터라 로그에 써도 되지만 줄 길이를 위해 경로 · id 만 |

- **왜 기동 실패인가(코디 권장 · 기본값)**: 0.3.0 의 「빈 용어집으로 뜬다」(D-14)는 **남의 서버**가 죽을 때를 위한 것이었다. 시드는 **우리 파일**이고 깨지는 길은 우리 PR 뿐 — 그건 **시험으로 막는다**(§9.1 「시드」: 레포의 실제 `back/seed/glossary.json` 을 같은 검사 함수로 읽는 시험). 그래도 깨진 채 배포되면 조용히 용어집 없이 통역하는 것보다 **readiness 가 안 올라와 옛 pod 가 남는 것**이 낫다(k8s 롤링 — 옛 판이 계속 서비스). 용어집이 들어간 줄 아는데 빠져 있는 상태(§4.6 4번 「몰래 빼지 않는다」와 같은 원칙)를 만들지 않는다.
- 그래서 `loaded=false` 경로는 **없어진다**. 0.5.0 — `loaded` 필드 자체를 응답에서 지웠다(`/api/health` = `{ok}` · 메뉴 없음 · §3.5).
- 시드에 term 이 있는데 **고른 언어 entry 가 하나도 없으면** 그 언어는 `context` 없이 연결한다(빈 용어집과 같은 경로 · 0.3.0 §4.5 「빈 용어집이면 `context` 키 없음」). 기동 실패가 아니다(언어별로 채워 가는 중일 수 있다).

### 4.5 언어별 `context` 조립 (D-05 · D-18 · D-33 · D-45 · D-49)

통역 연결(§5.3 `start`) 때 고른 언어 `L` 로 Soniox STT 설정에 `context` 를 넣는다. 칸은 넷 — `general`(고정 3쌍 · 0.3.0 그대로) · **`text`(0.8.0 — 역할 · 방향 서술 · D-45 · 0.8.1 넷째 문장 D-49 · 아래)** · `terms` · `translation_terms`. (0.7.0 까지는 `text` 를 넣지 않았다.)

**재료** — 시드 순서대로 `entries[L]` 이 있는 term 만. 간체화 `norm`: **`L ∈ {yue, zh-Hant}` 면 OpenCC `t2s`**(Soniox 의 중국어 출력은 간체 — 번체 source/target 이 간체 출력 사이에 섞이고 TTS 로 가면 발음이 깨진다 · D-17 · 0.3.0 §4.3 의 yue 이유와 같음), 그 밖은 그대로. 괄호는 시드에 없다(§4.2) — 가공 없음.

| 칸 | 넣는 것(이 순서) | 근거 |
|---|---|---|
| `general` | 0.3.0 고정 3쌍 그대로(0.8.0 에서도 안 바꾼다 — 아래 「`general` 은 그대로」) | 입력 1 |
| **`text`** | **고정 문안 하나**(아래 「서술 칸 `text`」 — 네 문장) — 언어와 무관하게 같은 문자열 | D-45 · D-49 |
| `terms` | ① ko 대표명 전부(시드 순서) ② 그 뒤 ko 별칭 전부(시드 순서 · term 안 순서) | D-05 「`terms` 는 ko 표기」 |
| `translation_terms` | **정방향 기본** `{source: ko, target: norm(name)}` → **정방향 별칭** `{source: ko 별칭, target: norm(name)}` → **역방향 기본** `{source: norm(name), target: ko}` → **역방향 별칭** `{source: norm(alias), target: ko}` | D-05 정방향 · D-18 역방향 · D-33 「정방향 = ko 대표명 · ko 별칭 → 현지명, 역방향 = 현지명 · 별칭 → ko 대표명」 |

- 역방향 source 중복(다른 시술의 같은 현지명 · `norm` 뒤 같아진 것 · 현지명과 다른 시술 별칭이 같음)은 **위 순서에서 처음 짝만** 둔다(0.3.0 규칙 그대로 — 기본 짝이 별칭 짝보다 앞).
- 정방향 source 중복은 §4.2 검사 3 이 막는다(조립에서 다시 거르지 않는다).
- **zh-Hant 는 zh-Hant entry 를 쓴다(0.4.0)** — 0.3.0 · D-28 의 「zh-Hant target 은 zh 열」은 시드에 zh-Hant 표기가 없을 때의 대안이었다. D-33 이 zh-Hant 표기를 시드에 두고 D-32 가 「대만 현지 별명은 그 언어 표기를 추가해서 해결」이라 했으므로, 대만 손님이 부르는 이름(예 美國音波)이 Soniox 에 닿으려면 zh-Hant entry 가 context 재료여야 한다. **0.5.0 — D-35 로 대만 현지명 77개가 들어가 zh-Hant context 는 zh 와 실제로 다르다**(정방향 target 美國音波 · 역방향 source 美國音波 · 極線音波 등 → `t2s` 뒤 美国音波 …). OQ-013 닫음.
- 크기 로그(§4.6 5번)는 칸 수를 넷으로 나눠 적는다: `terms` · 정방향(기본 · 별칭) · 역방향(기본 · 별칭) · 뺀 수 · 글자 수 · (0.8.0) `text` 글자 수.

**서술 칸 `text` — 역할 · 방향 · 시술의 뜻 (0.8.0 · D-45 · 0.8.1 · D-49)**

> 기록 분석(BASE-001 2026-11-14): 문제 44줄 가운데 약 10줄이 「상황 · 역할을 모르고 일반 뜻으로 옮김」, 약 4줄이 말투(높임)다 — 손님이 하는 접수를 직원이 응대하는 말로, 고민을 걱정으로, 이름 묻기를 반말로 옮겼다. context 는 `general` 세 줄뿐이었다. Soniox 공식 문서는 `text` 를 「Longer background, written however you like」 로, `general` 값은 「a name or short label, not a sentence」 로 적는다 — 역할 · 방향처럼 문장으로 써야 하는 것은 `text` 자리다.

| 항목 | 계약 | 근거 |
|---|---|---|
| 내용 | ① **역할** — 한국어로 말하는 쪽 = 클리닉 직원 · 다른 언어로 말하는 쪽 = 손님(환자) ② **한국어 → 외국어** = 손님이 **듣는** 말 · 높임 ③ **외국어 → 한국어** = 손님이 **한** 말 ④ **여기서 말하는 시술은 수술이 아니라 미용 시술**(0.8.1) | D-45 · D-49 |
| 문안 | 아래 **S1 ~ S4 네 문장**(영어 · 한 벌 · 글자 그대로). back 상수 **한 곳**(`service/glossary.py` — `GENERAL` 옆 `CONTEXT_TEXT` 류)에 둔다. 문장 사이는 `\n` | 문안 = 이 문서(S4 를 넣는 것은 D-49) · 언어 선택은 OQ-024 |
| 언어 | **영어 · 7개 언어 공통 한 벌**(고른 언어 이름을 넣지 않고 「the other language」 로 쓴다). 지금 `general` 이 영어이고, 한 벌이면 언어마다 크기가 같아 한도 계산(§4.6)이 단순하다. 공식 문서의 「Write the context in the language people speak」 는 한 세션에 두 언어가 오가는 이 앱에 그대로 맞지 않는다 — **한 벌 영어가 언어별 문안보다 나은지는 근거가 없다(OQ-024)** | 기본값 |
| 넣는 때 | `context` 를 넣는 모든 연결(= 그 언어 entry 가 하나라도 있을 때 · §4.4). 조립 결과가 `None`(entry 0)이면 지금처럼 `context` 키 자체가 없다. **운영에서는 늘 넣는다** — 빼는 길은 조립 함수의 선택 인자뿐이고 품질 시험 스크립트만 쓴다(env · WS 로는 못 뺀다 · §9.3 「조합」) | 0.4.0 그대로 · 0.8.1 W-1 |
| 줄이기 | **줄이지 않는 칸** — `general` 과 같은 취급(§4.6). `forward_only`(재연결 설정)에도 남는다 | D-45 「자리를 어떻게 낼지는 SPEC」 · 기본값 |
| 밖으로 | 응답 · front 번들 · WS 메시지에 나가지 않는다(§3.5 그대로). 로그에는 글자 수만(`text=<n>` · §4.6 5번) | D-37 |

**문안**(영어 · 네 문장 · **424자** — `json.dumps` 로는 429자 · 0.8.1 — 0.8.0 초안은 S1 ~ S3 347자)

```text
The Korean speaker is a staff member of a dermatology clinic. The speaker of the other language is a customer of the clinic.
Korean into the other language: these are words the customer hears. Translate them politely and respectfully, as staff speaking to a customer.
The other language into Korean: these are words the customer said to the staff.
Procedures discussed here are non-surgical cosmetic treatments, not surgery.
```

| 문장 | 무엇 | DEC |
|---|---|---|
| S1 | 역할 — 한국어 쪽 = 직원 · 상대 = 손님 | D-45 「한국어 쪽은 클리닉 직원, 상대는 손님(환자)」 |
| S2 | 한 → 외 = 손님이 듣는 말 · 높임 | D-45 「손님이 듣는 말 · 높임으로」 |
| S3 | 외 → 한 = 손님이 한 말 | D-45 「손님이 한 말로」 |
| **S4**(0.8.1) | 여기서 말하는 시술은 수술이 아니라 미용 시술 | **D-49** 「시술은 수술이 아니라 미용 시술 문장을 더한다」 — 입력 5 ③(시술 → 수술 뉘앙스)을 다룰 자리가 context 뿐(0.8.0 OQ-025 닫음) |

- 문안은 **품질 시험(§9.3 「6차」 — S1 ~ S3 은 2절 T11 ~ T22 · S4 는 1절의 T05 · T06)으로 판정한다** — 조합 B(문안 없음)와 C(문안 있음)의 차이가 이 문안의 효과다(C 는 시드도 같이 바뀐다 — 사전 대상이 아닌 문장에서만 문안 효과로 읽는다). 문안을 고치면 이 절 · 상수 · 시험(§9.1)을 같이 고친다(코디 → planner).
- **`general` 은 그대로**(0.8.0) — D-45 는 「`text` 와 `general` 에 역할 · 방향을 적는다」고 했고, `general` 의 `setting`(「Face-to-face interpretation between a Korean clinic staff member and a foreign patient」)이 이미 역할을 적고 있다. 방향 · 높임은 문장이라 `text` 로 갔다. 전후 비교(§9.3)에서 바뀌는 칸을 `text` 하나로 두려고 `general` 은 건드리지 않는다 — 시험 뒤 `general` 을 손볼 근거가 생기면 그때 고친다.

**`translation_terms` 에 넣지 않는 것 (0.8.0 · D-45)**

- **일반 낱말 짝을 넣지 않는다** — 「접수」 → 그 언어의 「등록」 같은 짝은 손님 쪽 문장을 고치려다 직원 쪽 문장(「접수 받았어요」)을 거꾸로 틀리게 만든다(D-45). `translation_terms` 의 재료는 **시드 term 뿐**이다 — 모든 짝의 ko 쪽은 시드의 `ko` · `ko_aliases`, 상대 쪽은 그 언어 entry 의 `name` · `aliases` 여야 한다(시험 · §9.1 「context」). 코드에 따로 박은 짝 0.
- 「시술」 · 「접수」 · 「상담」 · 「고민」 같은 말은 시드 term 으로도 넣지 않는다(§4.2.4 Q6). 이런 말의 옮김은 `text` 의 역할 · 방향에 맡긴다.
- **틀린 꼴(`ko_wrong` · `wrong` — 0.9.0 · D-58)은 context 에 넣지 않는다** — `terms` 에도 `translation_terms` 에도. 틀린 꼴을 역방향 source 로 주면 Soniox 에 「이 꼴도 그 시술 이름」 이라고 가르치는 셈이다. 조립(`build_context`)은 이 두 필드를 읽지 않는다(시험 · §9.1 「바로잡기」 — `.7` 과 `.8` 의 조립 결과가 바이트까지 같다).

**구조로 들고 다닌다(0.4.0)** — 조립 결과를 Soniox dict 하나로 합쳐 두고 나중에 「앞 정방향의 거울인 첫 짝」으로 정방향/역방향 경계를 다시 찾지 않는다(별칭 짝이 생기면 거울 추측이 틀린다 · 0.3.0 `split_translation_terms`). `build_context` 는 네 묶음을 따로 가진 값(예 `ContextParts{general, terms, forward, forward_alias, reverse, reverse_alias}`)을 내고, Soniox 설정 dict 는 `to_soniox(parts)` 로 만든다. `forward_only(parts)` · `is_forward_only(parts)` 도 이 값으로. **0.8.0 — `ContextParts` 에 `text`(문자열)를 더한다**: `to_soniox` 의 키 순서 = `general` → `text` → `terms` → `translation_terms` · `forward_only` 는 `general` + `text` + 정방향 기본 · `is_forward_only` 판정은 그대로(`text` 는 판정에 넣지 않는다 — 운영에서는 늘 있다). **0.8.1 — 조립 함수(`build_context`)는 선택 인자 둘을 받는다**: 문안 넣기(기본 = 넣음) · 뺄 역방향 짝의 source 목록(기본 = 없음). 둘 다 **품질 시험 스크립트만** 준다 — 통역 API 경로는 인자를 주지 않아 늘 기본값이다(§9.3 「조합」 · W-1).

### 4.6 한도 — 줄이기 (D-05 · D-18 · D-45 · 0.3.0 §4.4 를 넷으로)

Soniox context 한도는 **8,000토큰** · 넘으면 `invalid_request`(공식 문서). back 은 글자 수로 미리 줄이고, 그래도 거절되면 한 번 더 줄인다.

1. `to_soniox(parts)` 를 `json.dumps(ensure_ascii=False)` 한 길이를 잰다(0.8.0 — `text` 칸이 든 채로 잰다).
2. **그 언어의 기준**(아래 언어별 표 — **0.9.0 「D-56 표」** · env `GLOSSARY_CONTEXT_MAX_CHARS` 가 있으면 그 값)을 넘으면 아래 순서로 **하나씩 뺀다** — 넘지 않을 때까지.
   1. **`terms`** — 뒤에서부터(ko 별칭이 먼저 빠지고 그다음 대표명 뒤쪽부터)
   2. **역방향 별칭** — 뒤에서부터
   3. **역방향 기본** — 뒤에서부터
   4. **정방향 별칭** — 뒤에서부터
   5. **정방향 기본 · `general` · `text`(0.8.0 · D-45)는 줄이지 않는다**(D-05 우선). 다 빼도 넘으면 그대로 연결해 본다(4번이 받는다)
3. 2번을 거친 설정으로 STT 를 연다(§4.6.1 확인).
4. 연결 직후 `invalid_request` 로 거절되면 **`general` + `text`(0.8.0) + 정방향 기본만**(`forward_only`)으로 STT 만 1회 다시 연결. 그것도 거절되면 `error soniox_unavailable`. 보낸 설정이 이미 정방향 기본만이면 재연결 없이 바로 `soniox_unavailable`. 용어집 없이 몰래 연결하지 않는다.
5. 실제로 보낸 칸 수(§4.5 끝)를 언어별 정보 로그 1줄 — 용어 문자열 0 · 끝에 `max=<그 언어 기준>`(0.6.1).

**줄이기 기준 = 언어별 표 (0.9.0 · D-56 — `stt-rt-v6` · 시드 `.7` · 문안 포함 실측 · WP23 ⑬′)** — 지금 쓰는 표

| lang | **기준(글자)** | v6 통과 최대치 | 거절 최소치 | 줄이기 없는 전체(`.7` — D-54 뒤 · 문안 포함) | 여유 | 뺀 수 |
|---|---|---|---|---|---|---|
| en | **24,892** | 25,930 | 25,976 | 20,679 | 4,213 | 0 |
| ja | **21,962** | 22,878 | 22,952 | 21,647 | 315 | 0 |
| zh | **22,551** | 23,491 | 23,573 | 20,401 | 2,150 | 0 |
| zh-Hant | **22,685** | 23,631 | 23,702 | 21,417 | 1,268 | 0 |
| th | **23,215** | 24,183 | 24,280 | 23,193 | **22** | 0 |
| vi | **24,349** | 25,364 | 25,443 | 19,958 | 4,391 | 0 |
| yue | **22,825** | 23,777 | 23,865 | 19,034 | 3,791 | 0 |

- **기준 = v6 실측 통과 최대치 × 0.96 내림**(D-56). 재는 법은 ⑬′ 그대로 — 7개 언어 모두 전체가 통과해 짝을 덧붙여 가는 이분 탐색(언어당 9 ~ 10회 · 거절은 모두 `invalid_request`). 표는 코드 **한 곳**(back `service/interpret/langs.py` `CONTEXT_MAX_CHARS` · `context_max_chars(lang, override)`)에만 둔다 — config · container · 시험 스크립트가 같은 함수를 쓴다.
- **왜 × 0.96 인가(D-56)**: × 0.9(0.6.1 의 계산식)로는 시드 `.7` 에서 D-54 로 27개를 뺀 뒤에도 **ja `terms` 101 · zh-Hant `terms` 16 · th `terms` 145** 가 빠진다(WP23 — 빠지는 것은 `terms` 인식 힌트뿐 · 짝 0). 실제 거절선까지 4% 여유를 두고 7개 언어 **줄이기 0** 을 고른 것이다(사용자 2026-11-15). 넘어서 거절되면 위 4번(`general` + `text` + 정방향 기본만으로 1회 재연결)이 그대로 받는다.
- **실물 ㉒(D-56 값 · WP24)**: 7개 언어 거절 0 · 보낸 글자 = 위 「줄이기 없는 전체」 · 묶음별 뺀 수 0 · 순수 계산과 실물 수치가 같다.
- **th 여유 22자 · ja 315자** — 시드에 th 별칭 · ko 별칭 · term 을 **하나만 더해도** th 는 `terms` 부터 줄이기가 시작된다. 시드 `.8` 의 틀린 꼴(§4.2.5)은 context 재료가 아니라 이 수치를 바꾸지 않는다. **(0.9.2) 위 표의 끝 세 열(줄이기 없는 전체 · 여유 · 뺀 수)은 시드 `.7` 때의 값이다 — 지금 시드(`.10`)의 값은 바로 아래 표.** 기준 열(한도)은 그대로다.
- 시드의 이름 · 별칭 · term 이 바뀌면(틀린 꼴만 더하는 판은 아님) §4.6 「계산 방법」 으로 여유를 다시 내고, 넘는 언어가 생기면 ⑬′ 로 다시 재서 이 표 · `langs.py` 를 같이 고친다(코디 · 사용자 판정 — 워커가 표를 바꾸지 않는다).
- env `GLOSSARY_CONTEXT_MAX_CHARS` 의 뜻은 그대로다(아래 옛 표의 둘째 줄).

**시드 `.8` ~ `.10` 의 글자 수 (0.9.2 · D-62 — 실물 ㉒ 다시 · v6 · 문안 포함 · 기준 = 위 「D-56 표」)**

| lang | 기준 | 줄이기 없는 전체 `.7` | `.8` | **`.9` = `.10`** | 여유(`.10`) | **보낸 글자(`.10`)** | **뺀 수(`.10`)** |
|---|---|---|---|---|---|---|---|
| en | 24,892 | 20,679 | 20,679 | 20,679 | 4,213 | 20,679 | 0 |
| ja | 21,962 | 21,647 | 21,647 | **21,985** | **−23** | 21,958 | **`terms` 2** |
| zh | 22,551 | 20,401 | 20,436 | 19,917 | 2,634 | 19,917 | 0 |
| zh-Hant | 22,685 | 21,417 | 21,448 | 22,010 | 675 | 22,010 | 0 |
| th | 23,215 | 23,193 | 23,193 | **24,065** | **−850** | 23,214 | **`terms` 79** |
| vi | 24,349 | 19,958 | 19,958 | 19,958 | 4,391 | 19,958 | 0 |
| yue | 22,825 | 19,034 | 19,069 | 19,811 | 3,014 | 19,811 | 0 |

- **`.8`**: zh · zh-Hant · yue 가 `.7` 보다 31 ~ 35자 는다(§4.2.5 ⓐ · ⓑ — kr-014 zh-Hant · ph-033 zh · yue). 7개 언어 줄이기 0 그대로(코드 검수 W-3 · WP26 ㉒).
- **`.9`**: 옛 영문 name 이 별칭으로 내려와 ja · zh-Hant · th · yue 가 늘고, zh 는 근거 없는 별칭 19개를 빼 준다. **ja 는 23자 · th 는 850자 기준을 넘는다.**
- **D-62 — ja · th 가 넘는 만큼은 `terms`(한국어 받아쓰기 힌트) 줄이기로 받는다**: ja `terms` 2 · th `terms` 79 가 뒤에서부터 빠진다(위 줄이기 순서 1번). **번역 짝(정방향 · 역방향 — 기본 · 별칭) 손실 0 · 거절 0.** 한도 표(D-56)는 바꾸지 않는다.
- **왜 별칭을 빼지 않았나**(D-54 순서를 쓰지 않은 이유): D-54 후보(이번 판에 새로 든 별칭 가운데 출처 1곳뿐인 것)를 다 빼도 th 는 251자가 남고(ja 는 풀린다), 그 후보의 대부분이 **별칭으로 내린 영문 옛 name** 이다 — 손님이 영문 상표로 말할 때의 역방향 짝이라 빼지 않는다(D-62 · 처분 §15 가 「별칭」 으로 정한 값과도 어긋난다).
- **`.10`**: 글자 수 · 뺀 수가 `.9` 와 같다(틀린 꼴만 더한 판) — 실물 ㉒ 다시(WP27 수정 1 · 수정 2): 거절 0 · 정방향 뺀 수 0 · ja `terms` 2 · th `terms` 79 · 나머지 0.
- 빠지는 `terms` 는 시드 뒤쪽 것이다(직원이 한국어로 말하는 시술명의 인식 힌트). **7차 th 직원 쪽 결과로 다시 본다**(D-62) — 7차에서 th 직원 쪽의 「인식」 갈래는 1행(S17 · 다른 3개 언어에서도 같은 행)이고 나머지 실패는 「못 찾음」 이다(§9.3 「7차 결과」). 받아쓰기 손실로 볼 근거는 나오지 않았다.
- 앞으로 시드에 th · ja 이름 · 별칭 · term 을 더하면 그만큼 `terms` 가 더 빠진다. 다음에 볼 순서: 역방향 별칭이 빠지기 시작하면(줄이기 순서 2번) 코디 · 사용자에게 올린다 — 워커가 표 · 별칭을 스스로 바꾸지 않는다.

**옛 표 — 기록 (0.6.1 ~ 0.8.4 · `stt-rt-v5` · 시드 `.6` 실측 · WP16 코디 처분 3)** — 0.9.0 에서 위 표로 바뀜

| lang | 기준(글자) | 통과 최대치(⑬′) | 거절 최소치 | 줄이기 없는 전체(`.6`) |
|---|---|---|---|---|
| en | **23,424** | 26,027 | 26,069 | 17,589 |
| ja | **20,419** | 22,688 | 22,771 | 19,408 |
| zh | **20,933** | 23,259 | 23,347 | 18,565 |
| zh-Hant | **21,689** | 24,099 | 24,142 | **24,750 — 그대로는 거절** |
| th | **21,343** | 23,715 | 23,833 | 20,804 |
| vi | **22,891** | 25,435 | 25,512 | 17,596 |
| yue | **21,123** | 23,471 | 23,557 | 17,636 |

- (옛 계산식) 기준 = 언어별 통과 최대치 × 0.9 **내림** — 0.9.0 에서 × 0.96 으로(위 「D-56 표」).
- **env `GLOSSARY_CONTEXT_MAX_CHARS`** = 비면 언어별 표 · **값이 있으면 7개 언어 모두를 그 값 하나로**(언어별 값보다 작든 크든 — 실험 · 비상용 덮어쓰기). 언어별 env 는 두지 않는다. 운영 ConfigMap · Secret 에는 넣지 않는다(§2.4 · §9.6).
- 재는 법(⑬′): 전체가 통과하는 6개 언어는 ⑬ 과 같은 padding 이분 탐색. **zh-Hant 는 전체(24,750)가 거절돼 padding 이 안 된다** → `build_context(max_chars=m)` 로 실제 보낼 모양을 만들어 `m` 을 이분 탐색(`live-check-wp16-ceiling.json` `trim_search`).
- **왜 언어별로**(0.6.0 → 0.6.1): `.6` 에서 공통 기본값(가장 작은 ja 기준)으로는 zh-Hant 역방향 별칭 63 · th `terms` 38 이 빠졌다(20,419 · ⑲ 다시) — 다른 언어의 한도에 묶여 넉넉한 언어가 짝을 잃었다. 언어별 표로 th 뺀 수 0 · zh-Hant 역방향 별칭 63 → 33.
- **남는 손실**: zh-Hant — `terms` 170 전부 · 역방향 별칭 33(시드 뒤쪽 = 새 시술 · 대만 2차 별칭). 전체가 실제 한도를 넘어 줄이기 없이는 거절되므로 피할 수 없다 — 더 살리려면 별칭 정리(시드) 또는 줄이기 순서 변경(계약)이고 0.6.1 은 둘 다 하지 않는다. 다른 6개 언어 뺀 수 0.
- (옛 문구 — 지금 규칙은 「D-56 표」 의 다섯째 줄) 시드가 다시 크게 바뀌면(별칭 · term 추가) ⑬′ 방법으로 다시 재서 표 · `langs.py` 를 같이 고친다.

**`text` 칸의 자리 — 언어별 여유 · 계산 방법 (0.8.0 · D-45)**

`text` 는 줄이지 않으므로, 그만큼의 글자가 **줄이기 대상 칸에서 빠진다**. 언어별 기준(위 표)은 `text` 때문에 바꾸지 않는다(0.9.0 의 「D-56 표」 는 문안이 든 채로 잰 값이다) — 한도는 Soniox 의 것이고 `text` 도 같은 8,000토큰 안에 든다.

- **`text` 가 차지하는 글자** `c` = `len(json.dumps(text, ensure_ascii=False))` + 키 · 구분자 10자(`, "text": `). 문안 S1 ~ S4 = 429 + 10 = **439자**(0.8.0 초안 S1 ~ S3 은 361자).
- **계산 방법**(시드 판 · 문안이 바뀔 때마다 · 순수 함수 — 키 필요 없음): 언어 `L` 마다 ① 줄이기 없는 전체 `full(L)` = `build_context(max_chars=아주 큰 값)` 의 `context_size`(문안 포함) ② `full(L) ≤ 기준(L)` 이면 뺀 수 0 · 남는 여유 = `기준(L) − full(L)` ③ 넘으면 `build_context(max_chars=기준(L))` 을 돌려 **묶음별 뺀 수**(`report` 의 `dropped_terms` · `dropped_reverse_alias` · `dropped_reverse` · `dropped_forward_alias`)를 읽는다 ④ 같은 계산을 문안 없이 한 번 더 해 **문안 때문에 더 빠진 수** = ③ 의 차이. 결과는 언어 7개 × (전체 글자 · 기준 · 여유 또는 묶음별 뺀 수 · 문안 때문에 더 빠진 수) 표로 보고한다.
- **판정**: 정방향(기본 · 별칭)이 빠지는 언어가 생기면 코디 보고(0.6.0 판정 그대로 — 워커가 기준 · 문안 · 순서를 바꾸지 않는다). `terms` · 역방향만 빠지면 기록.

**시드 `.6` 기준 추정**(2026-11-14 · 배포본 코드의 `build_context` 로 계산 · 문안 S1 ~ S4 = 439자(0.8.1 · D-49) · 실물 연결 아님 — **`.7` 확정 뒤 WP23 에서 다시 잰다**)

| lang | 기준 | 줄이기 없는 전체(`.6` · 문안 없음) | 지금 여유 | 문안 넣은 뒤 여유 | 문안 때문에 더 빠지는 것 |
|---|---|---|---|---|---|
| en | 23,424 | 17,589 | 5,835 | 5,396 | 0 |
| ja | 20,419 | 19,408 | 1,011 | 572 | 0 |
| zh | 20,933 | 18,565 | 2,368 | 1,929 | 0 |
| zh-Hant | 21,689 | 24,750 | **없음**(이미 줄임 — 보낸 글자 21,658 · `terms` 170 · 역방향 별칭 33 빠짐) | 없음 | **역방향 별칭 33 → 44**(11 더 — 0.8.0 세 문장 추정은 42) |
| th | 21,343 | 20,804 | 539 | **100**(0.8.0 세 문장 추정은 178) | 0 |
| vi | 22,891 | 17,596 | 5,295 | 4,856 | 0 |
| yue | 21,123 | 17,636 | 3,487 | 3,048 | 0 |

- 읽는 법: **zh-Hant 만 문안 값을 치른다**(역방향 별칭 11개 — 시드 뒤쪽의 별칭부터 · 정방향 뺀 수 0). **th 는 여유가 100자 · ja 는 572자**라, 시드 `.7` 이 별칭 · term 을 조금만 늘려도 th 는 `terms` 부터 줄이기가 시작된다.
**시드 `.7` 추정**(0.8.2 · **0.8.3 다시 계산 — 처분 §4-e · 조사 r3 반영** · 2026-11-14 — §4.2.4 의 규칙 · 처분을 시드 `.6` 에 적용한 값을 위 계산 방법(순수 함수 · `build_context`)에 넣음 · 문안 포함 · 실물 연결 아님 · 기준은 `.6` · v5 로 잰 표 그대로)

| lang | 기준 | 줄이기 없는 전체(`.7` · 문안 포함) | 여유 | 빠지는 것 | `.6`(문안 포함) |
|---|---|---|---|---|---|
| en | 23,424 | 20,755 | 2,669 | 0 | 여유 5,396 |
| ja | 20,419 | **21,726** | **−1,307** | **`terms` 128**(172 중 · 짝은 0) | 여유 572 |
| zh | 20,933 | 20,443 | 490 | 0 | 여유 1,929 |
| zh-Hant(F 앞) | 21,689 | 25,565 | −3,876 | `terms` 172 전부 · 역방향 별칭 53 | `terms` 170 · 역방향 별칭 44 |
| **zh-Hant(F 뒤 — D-53)** | 21,689 | **22,356** | **−667** | **`terms` 61 · 역방향 별칭 0** | — |
| th | 21,343 | **23,372** | **−2,029** | **`terms` 172 전부 · 역방향 별칭 9** | 여유 100 |
| vi | 22,891 | 20,009 | 2,882 | 0 | 여유 4,856 |
| yue | 21,123 | 19,034 | 2,089 | 0 | 여유 3,048 |

- 읽는 법: **`.7` 은 줄이기가 도는 언어를 하나(zh-Hant)에서 셋(ja · th · zh-Hant)으로 늘린다.** 정방향(기본 · 별칭) 뺀 수는 7개 언어 모두 0. ja 는 `terms`(STT 인식 힌트 — ko 대표명 · ko 별칭)만 빠지고 짝은 다 남는다. th 는 `terms` 가 전부 빠진 뒤 역방향 별칭 9개(시드 뒤쪽)가 더 빠진다. 늘어나는 원인은 별칭 — th 65 → 118개(옛 태국 문자 값을 alias 로 내린 칸 · 별칭 추가) · ja 75 → 121개. 0.8.2 추정(ja 21,805 · `terms` 138 / th 23,658 · 역방향 별칭 15)보다 조금 준 것은 처분 §4-e 로 부위 term 의 시술 이름 별칭이 빠져서다.
- 이 수치는 §4.2.4 「읽는 법」 a ~ k(코디 처분 §4)의 값이다. **WP23 이 스크립트 결과로 다시 계산한다.**
- **zh-Hant 는 D-53 정리(§4.2.4 ② F) 뒤에도 기준을 넘는다**(0.8.3 · W-2 — 0.8.2 의 「잘리지 않을 것으로 본다」 를 고친다). r3 `뺌` 77개만 빼면 **22,471자 · 782자 초과 · `terms` 73개 빠짐 · 역방향 별칭 0** — 별칭으로 내려오는 옛 name 3개(② F · 0.8.4)까지 빼면 표의 값(**22,356자 · 667자 초과 · `terms` 61개 · 역방향 별칭 0**)이다. F 앞에 빠지던 역방향 별칭 53개의 손실은 없어지지만, `terms`(직원이 한국어로 말하는 시술명의 인식 힌트) 일부는 여전히 빠진다. 나머지는 D-54 가 다룬다.
- **ja · th 는 D-53 의 대상이 아니다** — 위 추정대로 줄이기가 돈다. 이것도 D-54 가 다룬다.

**D-54 절차 — 한도를 넘는 언어는 근거가 약한 별칭부터 · v6 로 실제로 다시 잰 뒤에만**(0.8.3 · D-54 · 처분 §5 — WP23 이 이 순서로. term · `name` · `reviewed` 는 건드리지 않는다)

| 순서 | 무엇 |
|---|---|
| 1 | 변환 스크립트로 시드 `.7` 을 만든다(§4.2.4 ① · ② A ~ F). **이 단계에서는 D-54 로 아무것도 빼지 않는다** |
| 2 | **v6 재측정**(§9.3 ㉒ ⑬′ — `stt-rt-v6` · 시드 `.7` · 문안 포함)으로 언어별 통과 최대치 · 거절 최소치를 잰다. **넘는지는 이 실측에서 낸 기준으로 가린다**(0.8.4 · 처분 §7 F-1) — **「넘는다」 = 그 언어의 줄이기 없는 전체 글자 수 > 기준**, 기준 = **v6 실측 통과 최대치 × 0.9(내림)**(이 절 언어별 표 · `CONTEXT_MAX_CHARS` 의 계산식 그대로). 운영 코드가 실제로 줄이기를 시작하는 선이 이것이다 — 통과 최대치 자체와 견주지 않는다. 위 추정 표의 기준 칸은 v5 · `.6` 으로 잰 값이라 판단에 쓰지 않는다(잣대는 같고 실측만 v6 로 바뀐다) |
| 3 | 안 넘는 언어는 그대로 둔다. **넘는 언어만** 뺀다 — **zh-Hant**: 조사 r3 `유지 — 10-27 근거` 별칭(23 가운데 `.7` 에 남은 22) / **ja · th**: 이번 판에 **새로 더한 별칭**(`.6` 의 그 칸 `aliases` 에 없던 것) 가운데 그 칸 `sources` 가 **1곳뿐**인 것. 스크립트의 인자 · 옵션으로 뺀다(시드를 손으로 고치지 않는다 · 다시 돌리면 같은 결과) · 대조표에 「D-54 뺌」 으로 낱개를 적는다 |
| 4 | 뺀 뒤의 전체 글자 수를 **2 에서 낸 기준과 다시 견준다**(같은 「넘는다」 — 별칭을 빼도 통과 최대치는 그대로라 한도를 다시 재는 것이 아니다) |
| 5 | **그래도 넘으면 멈춘다** — 더 빼지 않고 수치(언어 · 전체 글자 · 실측 통과 최대치 · 기준(× 0.9) · 묶음별 빠지는 수)를 코디에게 올린다(코디 → 사용자). 한도 표 · `langs.py` · 줄이기 순서는 워커가 바꾸지 않는다(OQ-028) |

- **3 의 후보(계산 2026-11-14)**: zh-Hant 22개 / ja 2개 — ph-037 `ボコーチュア` · ph-042 `ボツラックス` / th 3개 — ph-135 `โพเทนซ่า` · `โพเทนซา` · ph-153 `เอเอสซีพลัส`.
- **추정(순수 계산 · v5 기준 그대로일 때)**: zh-Hant 는 3 으로 기준 안에 든다 — 21,417자 · 여유 272 · 빠지는 것 0. **ja · th 는 3 으로 닫히지 않는다** — ja 21,647자(−1,228 · `terms` 119) · th 23,242자(−1,899 · `terms` 172 전부 + 역방향 별칭 7). v6 실측에서 낸 기준이 v5 와 비슷하면 ja · th 는 5(멈춤)로 간다.
- th 의 새 별칭 가운데 출처가 **0곳**인 15개(「현지에 없음 → 영문」 으로 alias 로 내려온 옛 태국 문자 값)는 D-54 의 문구(「출처 1곳뿐인 것」)에 들지 않아 후보에 넣지 않았다 — 넣으면 th 22,606자(−1,263 · `terms` 124 · 역방향 별칭 0)다. 넣을지는 5 에서 코디 · 사용자가 정한다(워커가 넓히지 않는다).

**D-54 절차의 결과 → D-56 (0.9.0 · WP23)**

| 순서 | 결과 |
|---|---|
| 1 | 시드 `2026-11-14.7` · 변환 스크립트(다시 돌리면 같은 바이트) |
| 2 | v6 ⑬′ 실측 — 통과 최대치는 위 「D-56 표」. 그때의 기준(× 0.9): en 23,337 · ja 20,590 · zh 21,141 · zh-Hant 21,267 · th 21,764 · vi 22,827 · yue 21,399 → **ja(+1,136) · zh-Hant(+1,089) · th(+1,559)가 넘음** |
| 3 | 넘는 세 언어에서 뺌 — zh-Hant 22 · ja 2 · th 3 = **27개**(후보는 위 「3 의 후보」 그대로) |
| 4 | 뺀 뒤에도 × 0.9 기준으로는 셋 다 넘음 — zh-Hant +150(`terms` 16) · ja +1,057(`terms` 101) · th +1,429(`terms` 145) · 짝은 0 |
| 5 | **멈춤 → 사용자 결정 D-56**: 더 빼지 않고 **기준을 × 0.96 으로** — 7개 언어 줄이기 0. 시드는 27개를 뺀 채로 둔다(D-54 로 뺀 것을 되돌리지 않는다 — 되돌리면 zh-Hant 22,356 · ja 21,726 · th 23,323 으로 th 가 다시 넘는다) |

- 이 절차의 「넘는다」(× 0.9)는 **WP23 의 그 한 번에 쓴 잣대**다. 0.9.0 부터 운영 기준은 「D-56 표」(× 0.96)이고, 앞으로 넘는 언어가 생기면 코디 · 사용자가 다시 정한다(같은 절차를 자동으로 되풀이하지 않는다). **OQ-028 닫음.**
- 위 「옛 표」 의 기준은 `stt-rt-v5` · 시드 `.6` 으로 잰 값이었다(0.6.1 ⑬′) — v6 통과 최대치는 en · zh-Hant · vi 가 조금 낮고(−97 · −468 · −71) ja · zh · th · yue 가 조금 높다(+190 · +232 · +468 · +306).

**옛 단일 기본값 — 기록 (0.4.1 ~ 0.6.0 · `GLOSSARY_CONTEXT_MAX_CHARS` 기본값 20251)**

- **0.4.1**: 시드(157 term)로 7개 언어 실제 한도를 다시 쟀다(§9.3 ⑬ — 같은 방법). 가장 작은 통과 최대치 **ja 22,502** × 0.9 = **20,251**(내림). 18,832 에서는 시드 th 전체 context(19,340자)가 넘어 `terms` 45개가 빠졌다 → 20,251 이면 7개 언어 모두 뺀 수 0(남는 여유 th 기준 911자). zh-Hant 통과 최대치 22,842 는 ja 보다 크다. 코디 처분(WP9 보고 이슈 1).
- **0.5.0 — 대만 현지명(D-35) 뒤 zh-Hant 는 줄이기가 돈다**(기본값은 그대로 20,251 · 코디 처분 「그대로」): 역방향 별칭이 55 → 190 으로 늘어 zh-Hant 전체 context 가 기본값을 넘는다 → 1단계로 `terms`(ko 대표명 뒤쪽부터)만 빠지고 **짝은 전부 남는다**(최종 시드 `.4` — 조립 뒤 20,250자 · `terms` 31개 남음). 다른 6개 언어는 뺀 수 0. 줄이기 없는 전체(21,605자 · 시드 `.3`)도 실물에서 거절되지 않았다(§9.3 ⑰) — 줄이기는 안전 여유다. 별칭이 더 늘면 2단계(역방향 별칭)가 시작된다.
- **0.6.0 — 시드 `.6`(새 시술 13 · §4.2.2)로 7개 언어 모두 짝이 13 ~ 40개쯤씩 늘어난다 → 기본값은 20,251 그대로 두고 줄이기 순서(위 2번)에 맡긴다**(→ 0.6.1 에서 위 언어별 표로 바뀜 — ⑲ 첫 실행에서 zh-Hant 역방향 별칭 68 · th `terms` 57 이 빠짐)(브리프 · 코디). 넘는 언어는 `terms` → 역방향 별칭 → 역방향 기본 → 정방향 별칭 순서로 빠진다 — 새 term 은 배열 맨 뒤라 `terms` 에서 먼저 빠지고, 짝은 별칭부터 빠진다. **실물 ⑲ 에서 7개 언어 글자 수 · 단계별 뺀 수 · 거절을 다시 잰다**(§9.3). 판정:
  - 거절 0 · 정방향(기본 · 별칭) 뺀 수 0 → 통과(기본값 그대로).
  - **정방향 별칭이 빠지는 언어가 생기거나 거절이 나면** 코디에게 보고 — 한도 재측정(⑬ 방법) 뒤 기본값을 고칠지(이 절 · §2.4 · `config.py`)는 코디 · 사용자가 정한다. 워커가 기본값을 바꾸지 않는다.
- 아래는 0.4.0 근거(matrix 시절 · 기록으로 남김).

- 근거 = WP6-BE 실측(§9.3 ⑧ · `live-check-wp6-2026-10-26.json`). 「통과 최대치」는 **같은 언어 짝을 덧붙여 크기를 늘리며 이분 탐색으로 찾은 실제 한도**다 — 역방향 포함 전체 context(최대 th 17,952자)가 6개 언어 모두 그대로 통과해 전체 크기로는 한도를 알 수 없었다. 언어별 통과 최대치 en 25,922 · **ja 20,925(가장 작음)** · zh 21,643 · th 22,566 · vi 24,778 · yue 22,643 → **20,925 × 0.9 = 18,832**(내림). 그 값으로 6개 언어 재연결 거절 0 · 뺀 `terms` 0 · 뺀 역방향 0.
- 0.3.0 문구(「통과한 최대 크기 중 가장 작은 값」)를 글자 그대로 읽으면 15,123 × 0.9 = 13,610 이지만, 그 값은 거절 없이 통과하는 언어에서 짝을 일부러 빼게 된다 → 실제 한도 기준(18,832)으로 정했다(코디 · WP6-BE 보고 이슈 1) — 0.4.1 에서 시드 실측 20,251 로 고침.
- 시드로 바뀌면 크기가 달라진다(괄호 병기가 빠져 짧아지고 · 별칭 짝이 늘어난다) — **실물 ⑫ 에서 7개 언어 크기 · 뺀 수를 다시 잰다.** zh-Hant 는 따로 한도를 잰 적이 없다 → ⑬ 에서 잰다. ⑬ 의 zh-Hant 통과 최대치가 20,925 보다 작으면 기본값을 그 값 × 0.9(내림)로 고친다(이 절 · §2.4 · `config.py`).
- 여유: 0.3.0 기준 가장 큰 전체 context(th 17,952)와 기본값 사이 880자. 시드에 별칭을 늘리면 th 부터 줄이기가 시작된다 — 줄이기는 별칭(2 ~ 4번)부터 빠지므로 정방향 기본은 끝까지 남는다.

### 4.6.1 거절을 알아채는 시점 · 판별

0.3.0 §4.4.1 **그대로**(STT 설정 뒤 `ready` 전 최대 `STT_CONFIG_CHECK_SEC` = 2초 · `SonioxError.error_type` · `invalid_request` 만 재연결 · STT 만 · TTS 는 확인 뒤 · 같은 브라우저 WS · `ready` 뒤 거절은 재연결 없음 · 로그는 `error_type` · `request_id` 만). 재연결 설정만 「정방향 기본만」(§4.6 4번)으로 읽는다. 가짜 Soniox 시험 6건도 그대로(§9.1 「context」).

### 4.7 ~~용어집 메뉴 API~~ — 삭제 (0.5.0 — D-37 · D-13 뒤집음)

- **`GET /api/glossary` 를 지운다**(404) · 응답 스키마 · `Glossary.menu_rows` 도 지운다. 화면의 용어집 메뉴 · 창도 지운다(§7.6).
- 이유(D-37): 밖으로는 통역에 필요한 최소 정보만 — 사전(시드)은 back 이미지 안에서 Soniox `context` 로만 쓰고 front 번들 · 응답에 나가지 않는다(§3.5).
- 0.4.x 의 메뉴 계약(`{loaded, version, count, lang, rows: [{id, category, ko, koAliases, term, aliases, reviewed}]}` · 「검수 전」 꼬리표)은 **폐기**. 검수는 시드 파일에서 `reviewed:false` 로 본다(§4.2).
- 시드 로더 · 검사 · context 조립은 그대로(§4.2 ~ §4.6).

### 4.8 첫 가져오기 스크립트 — Procedure Hub matrix → 시드 (D-33 · 한 번)

`back/scripts/import_glossary.py` — **한 번만 돈다.** 개발자가 손으로 실행하고 결과 파일을 PR 로 넣는다. back 런타임 · 시험 · 이미지 빌드는 이 스크립트를 부르지 않는다.

```text
cd back && uv run python scripts/import_glossary.py [--url <matrix 주소>] [--out seed/glossary.json] [--from-file <matrix.json>]
```

| 항목 | 규칙 |
|---|---|
| 원천 | `--url`(기본 = stg matrix 주소 — 인증 없는 공개 주소 · 스크립트 상수) 또는 `--from-file`(저장해 둔 matrix JSON — 시험 · 재현용) |
| 날짜 | `--date YYYY-MM-DD`(선택 · 기본 = 오늘) — `version` · `imported_from.at` 에 쓰는 날짜. 같은 입력 두 번 → 같은 바이트를 날짜와 무관하게 시험하려고(0.4.1 — backend 가 더함) |
| 한 번만 | `--out` 파일이 **이미 있으면 아무것도 쓰지 않고 0 아닌 코드로 끝난다**(사람이 고친 시드를 덮지 않는다). `--force` 는 두지 않는다 — 다시 가져와야 하면 사람이 파일을 지우고 돌린다 |
| term | matrix 행 하나 = term 하나. `id` = `ph-` + matrix 순서 3자리(`ph-001`). `category` · `ko` = 행 값(앞뒤 공백 · 줄바꿈 정리). `ko_aliases` = `[]`(matrix 에 없다) |
| 같은 `ko` 행 | **처음 행이 term**, 뒤 행은 term 을 만들지 않고 언어마다 표기가 다르면 그 표기(분해 뒤 현지명 · 별칭)를 처음 term 의 같은 언어 `aliases` 에 더한다 · 카테고리는 처음 행(2026-10-27 기준 `스킨보톡스` 2행 — yue 만 다름). 기본값 — 0.3.0 「같은 `ko` 는 처음 행」과 같은 쪽을 고르되 뒤 행의 표기를 버리지 않는다 |
| 언어 6개 | 행의 `en` · `ja` · `zh` · `th` · `vi` · `yue` 를 아래 **괄호 분해**로 entry 로. `source: "procedure-hub"` · `raw` = 분해가 원문과 다르면 원문 |
| zh-Hant | **zh entry(분해 뒤)를 자막과 같은 변환 `to_display("zh-Hant")`**(OpenCC `s2tw` + 「激光 → 雷射」 · §5.6 · 0.5.0 — D-35 처분. 0.4.x 의 `s2twp` 는 「鐳射」 · 「匯入」 오변환이라 폐기) 로 바꾼 것 — `name` · `aliases` 둘 다(영문은 그대로) · `source: "draft-s2twp"`(스키마 값 이름 그대로) · **`reviewed: false`**(D-33 — 현지 별명은 우리가 짓지 않는다 · 사용자가 고친다). 이미 시드가 있으므로 다시 도는 일은 사람이 파일을 지울 때뿐 |
| 빈 칸 | 표기가 빈 언어는 entry 를 만들지 않는다(zh 가 비면 zh-Hant 도 없음) |
| 머리 | `schema: 1` · `version` = 실행 날짜(`--date`) `.1` · `langs` 7개 · `imported_from{source:"procedure-hub", url, version: matrix version, count: matrix count, at: 날짜}` |
| 출력 | §4.2 모양 · 끝에 §4.2 검사를 스스로 돌려 통과해야 쓴다 · 요약 1화면(term 수 · 언어별 entry 수 · 합친 행 · 분해 종류별 수 · `reviewed:false` 수) |

**괄호 분해(D-33 「영문（현지명）→ 괄호 안 = 현지명 · 괄호 앞 = 별칭」을 일반화)**

글자 종류: **라틴** = ASCII + 라틴 확장(베트남어 성조 글자 포함 · U+00C0–024F · U+1E00–1EFF) · **현지 문자** = 그 밖(가나 · 한자 · 태국 문자 등). 원문을 `앞 (안)` 모양(반각 · 전각 괄호 · 괄호 하나 · 문자열 끝)으로 읽는다.

| 원문 모양 | 결과 | `reviewed` | 예(2026-10-27 matrix) |
|---|---|---|---|
| 괄호 없음 | `name` = 원문 | `true` | ja 「ジュビダーム」 · zh 「乔雅登」 |
| **라틴(현지)** | `name` = 안 · `aliases` = [앞] | `true` | zh 「Thermage FLX（美版热玛吉FLX）」 → 美版热玛吉FLX + Thermage FLX — **D-33 원문 규칙** |
| **현지(라틴)** | `name` = 앞 · `aliases` = [안] | `true` | ja 「シンパール (Synpurl)」 → シンパール + Synpurl · th 「อัลเธอราพี (Ultherapy)」 — 같은 원칙(현지명 = 현지 문자 쪽)의 거울 |
| 앞 = 안 | `name` = 앞 | `true` | vi 「Thermage FLX (Thermage FLX)」 |
| **그 밖** — 현지(현지) · 라틴(라틴) · 괄호 둘 이상 · 괄호 뒤에 글자 | `name` = 원문에서 괄호 부분(앞 공백 하나 포함)을 뺀 것 · `aliases` = [] | **`false`** | ja 「フィラー（ヒアルロン酸）」 → フィラー · en 「RF (Radiofrequency)」 → RF · ja 「瘢痕（傷跡）治療」 → 瘢痕治療 |

- 「그 밖」은 괄호 안이 **설명**(ヒアルロン酸 · 营销名称 · Marketing Name)인지 **다른 이름**(Radiofrequency)인지 글자만으로 가를 수 없다 → 이름을 짓지 않고 괄호를 빼서 넣고 **검수 전**으로 둔다(사람이 별칭으로 옮길지 정한다). 2026-10-27 matrix 로 센 수(시험 아님 · 참고): en 17 · ja 12 · zh 3 · th 2 · vi 23 · yue 3.
- 그 밖 기호(`/` · `／` 로 나열된 이름 — 예 ja 「シュリンク/ユニバース」)는 나누지 않는다(원문 그대로 · 괄호 규칙만).
- 원문의 줄바꿈 · 겹친 공백은 공백 하나로(예 en 「human Acellular Dermal ⏎ Matrix (hADM)」).

### 4.9 Procedure Hub 런타임 호출 제거 (D-33)

- back 에서 지운다: `load_glossary`(matrix HTTP) · `parse_matrix` · `_fetch` · `LOAD_TIMEOUT` · `GLOSSARY_MATRIX_URL`(config · `.env.example` · 운영 ConfigMap/Secret 이름 목록) · `context_rows`(matrix 행 기반) · `split_translation_terms`(거울 추측 · §4.5). matrix 주소는 **가져오기 스크립트 상수**로만 남는다.
- `httpx` 는 시험(TestClient) · 가져오기 스크립트가 쓰므로 의존성은 그대로 둔다.
- 확인: `grep -rn "stg-procedure-hub\|GLOSSARY_MATRIX_URL\|glossary/matrix" back/app` → 0(`"procedure-hub"` 는 entry `source` 값이라 걸러내지 않는다).

### 4.10 TTS 는 현지명 — 괄호 제거(§5.7)는 남긴다 (D-19 · D-33)

- 시드의 `name` 에는 괄호가 없다(§4.2 검사 4) → 용어집이 번역문에 괄호를 들여오는 길은 닫힌다. 정방향 target 이 현지명이라 TTS 는 **현지명을 읽는다**(예 zh 「美版热玛吉FLX」 — 영문 상표명이 아니라 · D-33 「써마지가 영어로 들어가는 게 아니라 중국어 · 대만어로」).
- 그래도 **§5.7 `strip_parens` 는 지우지 않는다** — 실물 ⑤(2026-10-26)에서 괄호는 Soniox 번역이 **스스로 만들기도** 했다(ja 「チャウム（補充）」 — 용어집 원문에 없던 괄호). D-19 「TTS 입력에서만 괄호를 뺀다」는 용어집과 무관하게 계속 맞다.

## 5. 통역 WS — D-03 · D-04 · D-17 · D-19 · D-28 · D-33 · D-35 · D-37 · D-41 · D-42 · D-43 · D-45 · D-47 · D-48 · D-55 · D-58 · D-63 · D-64 · D-65 · D-66

### 5.1 원형과 무엇이 같고 무엇이 다른가

| 항목 | 원형(`procedure/back`) | 이 레포 | 근거 |
|---|---|---|---|
| 중계 구조 | 브라우저 WS 하나 ↔ back ↔ Soniox STT(two_way) + TTS 두 연결 · 세션이 끝나면 둘 다 닫음 | **그대로** | D-03 · 개념 websocket-relay |
| 메시지 종류 · 오디오 형식 | §5.3 표 | **그대로** | 원형 `interpret-ws-contract.md` · `session.py` |
| 발화 묶기 · 자막 갱신 | `assembler.py`(`<end>`/`<fin>` 까지 한 발화 · non-final 갈아 끼움 · 같은 caption 재전송 안 함 · zh · ja · th 빈칸 정리) | **그대로** | 원형 · 개념 nondeterministic-stt-output |
| Soniox 모델 · 음색 · 샘플레이트 · keepalive 주기 | `stt-rt-v5` · `tts-rt-v2` · 음색 `Jiwoo` · 16k 입력 · 24k 출력 · 10초/20초 keepalive · stop 뒤 3초 드레인 | **STT 모델만 `stt-rt-v6`**(0.8.0 · D-43 · §5.10) · 나머지 그대로(0.7.0 까지는 전부 그대로 — STT `stt-rt-v5`) | 원형 `soniox.py` · `session.py` · D-43 |
| 끊김(발화 끝 감지) 설정 | `enable_endpoint_detection: true` · `max_endpoint_delay_ms: 1000` | **그대로**(0.8.0 1루프 · D-47 · §5.10 — **0.9.0: 1000 유지로 확정** · D-55 — 2000 으로 올려도 조각 수가 같았다) | 원형 `stt_config` · D-47 · D-55 |
| 빈 원문 발화 | 원문이 비어도 번역이 있으면 자막 · TTS 로 나감 | **내보내지 않는다**(0.8.0 · D-48 · §5.11) | D-48 |
| 확정 발화의 번역문 | Soniox 가 낸 그대로 자막 · TTS 로 | **시술명 바로잡기**(0.9.0 · D-58 · §5.12) — 원문에 사전 term 이 걸렸는데 번역에 사전 이름이 없으면 번역 속 틀린 꼴을 사전 이름으로 갈아 끼운 뒤 자막 · TTS · 기록으로. `final:false` 는 그대로 | D-58 |
| TTS keepalive **메시지 모양** | `{}` | **`{"keep_alive": true}`**(공식 형식) · 다른 stream_id 의 오류는 발화를 끊지 않음(§5.8 · 0.5.0) | 운영 장애 2026-10-27 · Soniox 공식 문서 |
| `start` 의 `lang` | 8개 `{zh,en,ja,th,fr,es,tl,hi}` | **7개 `{en, ja, zh, zh-Hant, th, vi, yue}`** — 앱 언어 코드(§5.5 · 0.4.0 zh-Hant 추가) | D-04 · D-28 |
| `start` 의 `traditional` | front 가 보냄 | **없앤다** — 번체 여부는 `lang` 이 정한다(§5.6). 와도 무시 | D-17 |
| `start` 의 `scheduleId` | 받아서 버림 | 없앤다(와도 무시). 0.6.0 통역 기록(§5.9)은 back 이 세션 id 를 스스로 만든다 — front 가 보내는 값을 쓰지 않는다 | Scope · D-41 |
| STT 설정 | `context` 없음 | **`context` 를 넣는다**(§4.5 · §4.6 — 시드의 정방향 + 역방향 · 0.4.0 · **0.8.0 서술 칸 `text`** — 역할 · 방향) | D-05 · D-18 · D-33 · D-45 |
| TTS 입력 | 번역문 그대로 | **괄호 부분을 뺀 문자열**(§5.7) — 자막은 그대로 | D-19 |
| `ready` 시점 | STT · TTS 를 열자마자 | STT 설정 확인(최대 2초 · 필요하면 정방향 기본만으로 1회 재연결) → TTS 열기 → `ready`(§4.6.1) · `SonioxError` 에 `error_type` (0.2.0) | D-05 · 공식 error-handling |
| 인증 | 헤더 Bearer 또는 `?token=` · accept 전 검증 · Origin 있으면 허용 출처만 | **그대로** — 토큰은 §3.2, 허용 출처는 `INTERPRET_FRONT_ORIGIN` | 원형 `api/interpret.py` · SPEC-004 §4.2 |
| 오류 문구 | 원인 · env 위치를 적은 문구(「`procedure/.env` 에 없어요」 · 「지원하지 않는 언어예요: 'xx'」 등) | **코드는 그대로 · 문구는 일반 문구 4종**(§5.4 · 0.5.0) — 원인은 back 로그에만 | D-37 |
| 자막 번체 변환 | `traditional` 이면 `s2tw` 하나 | **lang 별 설정**(yue `s2tw` · zh-Hant `s2tw` + 「激光 → 雷射」) — `CaptionAssembler(display=…)`(§5.6 · 0.5.0) | D-35(D-32 뒤집음) |

### 5.2 연결 · 인증

| 항목 | 계약 |
|---|---|
| 경로 | `WS /api/interpret` — 주소는 `NEXT_PUBLIC_API_BASE_URL` 의 `http`→`ws` · `https`→`wss` |
| 토큰 | 브라우저는 헤더를 못 싣는다 → `?token=<token>`. 헤더 `Authorization: Bearer` 도 받는다(시험 · 스크립트용) |
| 검증 순서 | ① `Origin` 이 있으면 `INTERPRET_FRONT_ORIGIN` 과 같아야 ② 토큰 §3.2 검증 — 둘 다 **`accept()` 전**. 실패면 accept 하지 않고 close 1008(브라우저에는 핸드셰이크 실패로 보인다) |
| 동시 연결 | 제한 없음(원형). 세션이 끝나면(닫기 · stop · 오류 · 브라우저가 그냥 닫음) Soniox 두 연결을 반드시 닫는다 — 시험으로 확인(원형 `test_client_close_cleans_up`) |
| 재연결 | **back 은 재연결하지 않는다**(끊김은 `error` 로 드러낸다 · 개념 websocket-relay §4). front 재연결은 §8 「끊김 · 재연결」 |

### 5.3 메시지 (원형 그대로 — `lang` · `traditional` 만 다름)

| 방향 | 프레임 | 모양 | 언제 |
|---|---|---|---|
| front → back | 첫 텍스트 | `{"type":"start","lang":"<L>"}` — `L ∈ {en, ja, zh, zh-Hant, th, vi, yue}`(대소문자 그대로 `zh-Hant`) | 연결 직후 한 번. 10초 안에 안 오면 `error bad_request` |
| front → back | 바이너리 | PCM s16le · 16,000 Hz · mono · 640샘플(40 ms) 조각 | 듣는 중 · **TTS 재생 중이 아닐 때만**(§7.4) |
| front → back | 텍스트 | `{"type":"pause"}` / `{"type":"resume"}` | 멈춤 / 다시 듣기 — 연결 유지. `pause` 때 back 이 말하던 발화를 확정(`finalize`) |
| front → back | 텍스트 | `{"type":"stop"}` 뒤 닫기 | 통역 끝 · 언어 바꿈 · 로그아웃 |
| back → front | 텍스트 | `{"type":"ready"}` | Soniox STT 설정 확인(§4.6.1) · TTS 연결 완료 |
| back → front | 텍스트 | `{"type":"caption","id":"u3","side":"me"\|"them","original":"…","translation":"…","final":false}` | 발화 단위. 같은 `id` 가 갱신되다가 `final:true` 로 확정 |
| back → front | 텍스트 | `{"type":"audio_start","id":"u3","sampleRate":24000}` | 그 발화(`final` 된 caption 의 `id`) 번역문 TTS 시작 |
| back → front | 바이너리 | PCM s16le · mono · `sampleRate` = 직전 `audio_start` 값 | 음성 조각 — 받는 대로 이어서 재생 |
| back → front | 텍스트 | `{"type":"audio_end","id":"u3"}` | 그 발화 음성 **보내기** 끝(재생 끝 아님) |
| back → front | 텍스트 | `{"type":"error","code":"…","message":"…"}` | 오류 — 보낸 뒤 back 이 닫는다 |

- `side` = 발화 원문 언어가 `ko` 면 `me`(한국어 쪽), 아니면 `them`(외국어 쪽) — 원형 `assembler._side`.
- `audio_start` 의 언어 = 그 `id` caption 의 반대편: `side=me` 발화의 TTS 는 외국어, `side=them` 발화의 TTS 는 한국어. front 는 `id` → `side` 로 안다(새 필드 안 둠 — 원형 모양 유지).
- TTS 는 한 번에 하나씩 차례로(원형 `_tts_worker` 큐).

### 5.4 오류 코드 — 코드는 원형 그대로 · 문구는 일반 문구 (0.5.0 — D-37)

| `code` | 언제 | `message`(0.5.0) |
|---|---|---|
| `bad_request` | 첫 프레임이 `start` 아님 · JSON 아님 · `lang` 이 7개 밖 · 10초 안에 `start` 없음 · 알 수 없는 텍스트 프레임 | 「요청을 처리할 수 없어요」 |
| `no_api_key` | `SONIOX_API_KEY` 비었음 | 「통역 서버를 쓸 수 없어요」 |
| `soniox_unavailable`(연결) | Soniox 연결 · 인증 실패 · §4.6 4번의 재시도도 거절 | 「통역 서버에 연결하지 못했어요」 |
| `soniox_unavailable`(중계 중) | 중계 중 Soniox 오류 · 중계가 끊김 | 「통역 연결이 끊겼어요」 |

- 문구에 설정 이름(`SONIOX` · `.env` · `API_KEY`) · 프로토콜 낱말(`start` · `type` · `JSON`) · **받은 값**(예 잘못 보낸 `lang`)을 넣지 않는다 — 0.4.x 의 「지원하지 않는 언어예요: 'xx' (가능: …)」 · 「알 수 없는 type: 'x'」 · 「SONIOX_API_KEY 가 .env 에 없어요」 · 「통역 서버(Soniox)…」는 **폐기**. 원인은 back 로그에만(`bad start: <예외 종류>` · 빈 키 경고 · §5.8 Soniox 오류 로그).
- front 는 `message` 를 그대로 보여 준다(§7.3 #2).
- 인증 실패는 `error` 프레임이 아니라 핸드셰이크 거절(close 1008 · §5.2).
- `bad_request` 중 「알 수 없는 텍스트 프레임」은 원형처럼 연결을 끊지 않고 오류만 보낸다.

### 5.5 언어 코드 매핑 (D-04 · D-28 · D-33)

| 앱 `lang` | 목록 표시 이름(자기 표기) | 한국어 이름(원 아래 안내) | Soniox STT `language_b` · `language_hints` | Soniox TTS `language` | 자막 표기 | 시드 entry(§4) · context `norm` |
|---|---|---|---|---|---|---|
| `en` | English | 영어 | `en` | `en` | 그대로 | `en` · 그대로 |
| `ja` | 日本語 | 일본어 | `ja` | `ja` | 그대로 | `ja` · 그대로 |
| `zh` | **中国 · 简体中文** | **중국어** | `zh` | `zh` | **간체**(Soniox 출력 그대로) | `zh`(간체) · 그대로 |
| `zh-Hant` | **臺灣 · 繁體中文** | **대만어** | **`zh`** | **`zh`**(간체 · 만다린 — 대만 음성 없음) | **번체 `s2tw` + 「激光 → 雷射」**(§5.6 · D-35) | **`zh-Hant`**(번체 · 대만 현지명 — D-35 · D-38 · D-39 · §4.2.1 ~ §4.2.2) · `t2s`(§4.5) |
| `th` | ไทย | 태국어 | `th` | `th` | 그대로 | `th` · 그대로 |
| `vi` | Tiếng Việt | 베트남어 | `vi` | `vi` | 그대로 | `vi` · 그대로 |
| `yue` | 廣東話 | 광둥어 | **`zh`** | **`zh`**(간체 · 만다린 발음) | **번체 `s2tw`**(§5.6) | `yue`(번체) · `t2s`(§4.5) |

- 목록 순서 = 위 표 순서(en · ja · zh · zh-Hant · th · vi · yue). 기본 선택 `en` · 마지막으로 고른 언어를 `localStorage` 에 기억(기본값 — 0.3.0 그대로).
- **중국과 대만은 별도 언어 항목**이다(D-28) — 대만을 중국어의 하위 갈래(「중국어(번체)」)로 쓰지 않는다. 한국어 이름은 「중국어」 · 「대만어」 → 원 아래 「대만어로 출력 중」 · 「대만어 듣는 중」.
- 한국어 쪽은 늘 `ko` — `translation: {type:"two_way", language_a:"ko", language_b:<위 표>}` · `language_hints: ["ko", <위 표>]`(원형 `stt_config`).
- **`yue` · `zh-Hant` 는 Soniox 에 별도 코드가 없다** — 공식 문서 STT · 번역 · TTS 지원 언어표(2026-10-26)에 중국어는 `zh` 하나다. 원형 실물(2026-10-13 `wp2-be-report.md` ②): 광둥어 발화가 `language: zh` 로 잡혔고 전사는 표준 문어 간체였다. 그래서 둘 다 `zh` 로 보낸다.
- ⚠ `yue` 를 고르면 한국어 → 광둥어 번역은 **표준 중국어 문어(번체 자막) + 만다린 음성**으로 나간다(§10 OQ-017 ②). `zh-Hant` 도 TTS 는 만다린(간체 입력)이다 — 외국어 안내의 출력 언어 이름은 「中文」(front 문구 · `lib/langs.ts`).
- 매핑 표는 back `service/interpret/langs.py` 한 곳(`APP_LANGS` · `SONIOX_LANG` · `TRADITIONAL_CONFIG`)에 둔다. front 는 `lib/langs.ts` 에 lang 7개 · 목록 표시 이름 · 한국어 이름 · 외국어 안내 문구만(같은 사실 한 곳 · lang 문자열은 back 과 정확히 같아야 한다 — `zh-Hant`).
- 0.4.0 — 0.3.0 의 `GLOSSARY_COLUMN = {zh-Hant: zh}`(대만이 zh 열을 빌림)은 **시드에 zh-Hant entry 가 생겨 지운다**(§4.5).

### 5.6 중국어 번체 — 언어별 변환 (D-17 · D-28 · D-35 — D-32 뒤집음)

| 앱 `lang` | 자막(`caption.original` · `caption.translation` 의 중국어 쪽) | TTS 입력 | Soniox context(§4.5) |
|---|---|---|---|
| `zh` | 간체 그대로 | 간체 | 시드 zh 그대로 |
| `zh-Hant` | **OpenCC `s2tw` 뒤 낱말 표 「激光 → 雷射」**(0.5.0 · D-35) | **간체**(변환 전 `Utterance.text`) | 시드 zh-Hant 를 `t2s` |
| `yue` | **OpenCC `s2tw`** | **간체** | 시드 yue 를 `t2s` |

- 변환 선택은 back `langs.py` 한 곳: `TRADITIONAL_CONFIG = {"yue": "s2tw", "zh-Hant": "s2tw"}` + **`DISPLAY_REPLACE = {"zh-Hant": {"激光": "雷射"}}`**(OpenCC 뒤에 적용). `to_display(lang)` 이 그 lang 의 변환 함수(없으면 간체 그대로)를 낸다 · 세션은 `CaptionAssembler(display=to_display(lang))`. 원형처럼 「`lang == "zh"` 인 쪽 문자열만」 바꾼다(Soniox 토큰 언어 기준). 가져오기 스크립트의 zh-Hant 초안도 같은 함수(§4.8).
- **`s2twp` 는 쓰지 않는다(0.5.0 · D-35 — D-32 뒤집음)**: `s2twp` 는 激光 → **鐳射**(홍콩 표기 — 대만은 雷射) · 导入 → **匯入**(離子導入이 맞음) · 项目 → **專案** 같은 오변환을 만들었다. 대만식 낱말은 표에 **필요한 것만** 더한다(지금 「激光 → 雷射」 하나).
  - 예(시험 · 실물): 激光治疗 → zh-Hant 「雷射治療」 · yue 「激光治療」 / 离子导入 → 「離子導入」 / 特色项目 → 「特色項目」 / 软件 → 「軟件」.
- TTS 로 보내는 번역문은 **간체 그대로**(번체를 넣으면 발음이 깨진다 · D-17).
- 변환은 화자가 한 원문 자막에도 적용된다 — 대만 화자가 「激光」이라 말해도 「雷射」로 보인다.
- **현지 별명은 라이브러리로 만들지 않는다**(D-32 의 이 부분은 D-35 에서도 유지) — 美國音波 · 鳳凰電波 같은 기기 현지 이름은 OpenCC 가 못 바꾼다. **시드 zh-Hant entry 의 `name` · `aliases`** 에 넣는다(§4.2.1). 우리 코드에 별칭 표를 짓지 않는다(`DISPLAY_REPLACE` 는 일반 낱말 표기 차이만).
- 의존성: `opencc-python-reimplemented`(원형 버전) — `s2tw`(자막 · 가져오기 초안) · `t2s`(context).

### 5.7 TTS 입력 괄호 제거 (0.3.0 — D-19)

> 0.4.0 — **그대로 둔다.** 시드 현지명에는 괄호가 없지만 Soniox 번역이 괄호를 스스로 만들기도 한다(⑤ 「チャウム（補充）」 · §4.10). `yue` · `zh-Hant` 는 간체 TTS 입력에 적용.

실물(§9.3 ⑤): ja 「フィラー（ヒアルロン酸）」가 번역문에 괄호째 나오고 TTS 가 괄호 안까지 읽었다. 그래서 **TTS 로 보내는 문자열에서만** 괄호 부분을 뺀다.

| 항목 | 규칙 |
|---|---|
| 어디서 | back 이 TTS 에 보내기 직전 한 곳(원형 `_tts_worker` 가 `Utterance.text` 를 보내는 자리) — 순수 함수 `strip_parens(text) -> str`. `yue` 는 간체로 된 TTS 입력(§5.6)에 적용 |
| 무엇을 | 반각 `( … )` · 전각 `（ … ）` — **여는 괄호부터 짝 닫는 괄호까지(안의 내용 포함)**. 반각 · 전각을 섞은 짝(`(…）` · `（…)`)도 짝으로 본다. 겹친 괄호는 바깥 짝 전체를 뺀다 |
| 공백 | 뺀 자리 **앞의 공백 하나**(반각 · 전각)를 같이 뺀다 — 「シンパール (Synpurl)」 → 「シンパール」 |
| 짝 없는 괄호 | 닫는 짝이 없는 여는 괄호 · 여는 짝이 없는 닫는 괄호는 **그대로 둔다**(글자만 남는다 — 문장을 자르지 않는다) |
| 그 밖 괄호 | `「」` · `【】` · `[]` · `<>` 등은 건드리지 않는다(D-19 는 괄호 병기만) |
| 비면 | 빼고 나서 공백만 남으면 **그 발화의 TTS 를 보내지 않는다**(`audio_start` 없음 · 자막은 그대로) — 기본값 |
| 자막 | `caption.original` · `caption.translation` 은 **그대로**(괄호 포함 · D-19 「자막에 그대로」) |
| 방향 | TTS 두 방향 모두(외국어 TTS · 한국어 TTS) — 용어집 역방향은 ko 가 target 이라 보통 괄호가 없지만, Soniox 번역문에 괄호가 생기면 같은 규칙 |
| 로그 | 바꾼 문자열을 로그에 쓰지 않는다 |

- 시험(§9.1 「통역」): 반각 · 전각 · 섞은 짝 · 겹친 괄호 · 짝 없는 괄호 · 앞 공백 · 다 빠져 빈 문자열 → TTS 안 보냄 · 같은 발화의 caption 은 괄호 그대로 · `yue` 는 간체 TTS 입력에서 뺌.

### 5.8 Soniox keepalive · TTS 오류 처리 (0.5.0 — 운영 장애 2026-10-27 02:07)

**장애**: 운영 통역(zh-Hant)이 연결 50초 뒤 `error soniox_unavailable` 로 끊겼다(로그 `error_type=invalid_request` · 설정 확인 2초 창 밖 · context 크기와 무관). 원인은 원형에서 복사한 **TTS keepalive 메시지 `{}`** — Soniox TTS 는 이것을 stream_id 없는 스트림 메시지로 보고 `{"stream_id": "", "error_type": "invalid_request", "error_message": "Missing stream_id"}` 를 돌려준다(실물 확인). Soniox 는 검증 오류 뒤에도 연결을 유지하지만(공식 `api-reference/tts/websocket-api` 「Error handling」), back `speak()` 는 TTS 소켓을 발화 때만 읽고 stream_id 를 보기 전에 오류를 올렸다 → keepalive 오류가 소켓에 쌓여 있다가 **다음 발화 TTS 에서 터져 세션 전체가 끝났다**(첫 TTS 뒤 20초 넘게 쉬었다 다시 말하는 모든 세션 · 언어 무관). 실물 재현(§9.3 ⑱)으로 확정.

| 항목 | 계약 |
|---|---|
| STT keepalive | `{"type": "keepalive"}`(공식 형식 · 원형 그대로) — 멈춤 · 말 없음 동안 |
| **TTS keepalive** | **`{"keep_alive": true}`**(공식 `tts/rt/connection-keepalive`) — `{}` 금지. 주기는 원형 그대로(20초 넘게 쉬면 10초마다) |
| TTS `speak(stream_id)` | 받은 메시지의 `stream_id` 가 **자기 것도 아니고 없음도 아니면**(다른 스트림 · 빈 문자열 `""`) **그 발화를 끊지 않는다** — 오류면 경고 로그 1줄(`soniox tts stray error: error_type · request_id · message`) 뒤 계속 읽는다. 자기 stream_id(또는 stream_id 없음)의 오류는 지금처럼 `SonioxError` 로 올린다 → `soniox_unavailable`(§5.4) |
| `SonioxError.channel` | `"stt"` · `"tts"` — 어느 연결의 오류인지 |
| 오류 로그 | `soniox error: channel · error_type · request_id · message · lang · paused · speaking · queue · stt_last=<audio·finalize·keepalive·end·config> N초 전 · tts_last=<text·keepalive·none> N초 전 [len · lang]` — **종류 · 길이 · 시각만**(키 · 발화 원문 · 번역문 0) |

- 원형(cc-prototype `procedure/back` `soniox.py`)에도 같은 `{}` 가 있을 수 있다 — 이 레포 범위 밖(DEC Scope Out 「ccc 변경」).

### 5.9 통역 기록 — 서버 볼륨에만 · 화면 · API 없음 (0.6.0 — D-41 · 0.7.0 보관 기간 — D-42)

> 「어떤 통역을 했는지 궁금해서」 · 「poc 라 시연 정도만」 · 「화면이 필요 없다 · 내부 검토용」(D-41). 기록은 back 이 볼륨에 쓰고, 코디가 클러스터에서 꺼내 본다(§9.6). **밖으로 내는 것은 그대로 6개 경로뿐**(§3.5 · D-37).

**저장 위치**

| 항목 | 계약 |
|---|---|
| 폴더 | env **`INTERPRET_RECORD_DIR`**(§2.4). 운영 = back PVC 마운트 `/data` 아래 **`/data/records`**(§9.6). **비면 기록 끔**(로컬 · 시험 기본) — 파일도 삭제 작업도 없다(`INTERPRET_RECORD_KEEP_DAYS` 값과 무관 · 0.7.0) |
| 기동 | lifespan 에서 ① 폴더가 비었으면 정보 로그 1줄 `interpret records: off` ② 있으면 `mkdir -p` · 쓰기 가능한지 확인 → 정보 로그 1줄 `interpret records: on dir=<경로> keep_days=<N 또는 off>`(0.7.0 — 보관 기간 env 가 양의 정수 N 이면 `keep_days=N` · 아니면 `keep_days=off` · 아래 「보관 기간」) ③ 만들기 · 쓰기 확인이 실패하면 **경고 로그 1줄(예외 종류만) 뒤 그 프로세스는 기록 끔으로 뜬다** — 기록 때문에 기동을 멈추지 않는다(시드와 다르다 · §4.4 — 기록은 통역의 부속이다) ④ **보관 기간이 N 일 때만** 삭제 1회(아래) — `off` 면 기동 때 지우지 않고 24시간 배경 작업도 만들지 않는다(0.7.0 · D-42) |
| 파일 | **날짜별 하나** — `<폴더>/<YYYY-MM-DD>.jsonl`. 날짜 = 그 줄 `at` 의 **한국 시간(UTC+9 고정 · 서머타임 없음)** 날짜. 자정을 넘긴 세션은 두 파일에 나뉜다(세션 id 로 잇는다). 인코딩 UTF-8 · 한 줄 = JSON 객체 하나(`ensure_ascii=False` · 줄바꿈 없음) · 끝에 `\n` |
| 쓰기 | 줄마다 append 1회(`open(…, "a")` · 한 번의 `write` · flush · fsync 하지 않음). 한 프로세스 안 쓰기는 직렬(이벤트 루프에서 동기 append 또는 잠금). 줄 하나는 수 KB 이하라 같은 노드의 두 pod 가 겹쳐 써도(롤링 · §9.6) 줄이 섞이지 않는다 — 기본값 |

**줄 모양** — 세 종류. 키는 아래 순서 · 여기 없는 키 0. (**0.9.0 — 발화 줄 끝에 `fixed` 하나를 더한다** · D-58 · §5.12. 0.8.x 가 쓴 줄에는 `fixed` 가 없다 — 지난 줄은 고쳐 쓰지 않는다. 읽는 쪽은 없으면 `[]` 로 본다. **0.9.1 — 바로잡은 발화 줄에만 그 뒤에 `translation_before` 하나가 더 붙는다**(처분 §11 · OQ-031 닫음 — `fixed` 가 `[]` 인 줄에는 이 키가 **없다**))

```json
{"type":"session_start","session":"9f2c4e7a1b3d5f60","at":"2026-10-28T14:03:11.204+09:00","lang":"zh-Hant","seed":"2026-10-27.6"}
{"type":"utterance","session":"9f2c4e7a1b3d5f60","at":"2026-10-28T14:03:19.882+09:00","lang":"zh-Hant","id":"u1","side":"me","original":"써마지 CPT 하고 프로파일로 같이 하실 수 있어요","translation":"您可以同時做黃金電波和逆時針","terms":["kr-001","kr-007"],"fixed":["kr-001"],"translation_before":"您可以同時做黃金波和逆時針"}
{"type":"session_end","session":"9f2c4e7a1b3d5f60","at":"2026-10-28T14:09:02.510+09:00","lang":"zh-Hant","reason":"stop","utterances":14}
```

(값은 모양 예시 — 실제 문장이 아니다)

| 키 | 줄 | 뜻 |
|---|---|---|
| `type` | 모두 | `session_start` · `utterance` · `session_end` |
| `session` | 모두 | back 이 세션마다 만드는 무작위 id — `secrets.token_hex(8)`(16자). 토큰 · 계정 · 연결 주소와 무관 |
| `at` | 모두 | 그 일이 back 에서 일어난 시각 — ISO 8601 · 밀리초 · `+09:00` |
| `lang` | 모두 | `start` 의 앱 lang(§5.5 — 7개 중 하나) |
| `seed` | start | 그 프로세스가 읽은 시드 `version`(§4.2) — 어느 사전으로 통역했는지 |
| `id` · `side` · `original` · `translation` | utterance | 그 발화의 **`final:true` caption 과 같은 값**(§5.3 — 화면에 나간 자막 그대로 · zh-Hant · yue 는 번체 변환 뒤 · 괄호도 그대로 · TTS 입력이 아니다). **0.9.0 — `translation` 은 바로잡은 뒤의 글이다**(§5.12 — 화면에 나간 것이 그 글이다). 바로잡기 전 번역은 `translation_before` 에(0.9.1) |
| `terms` | utterance | 걸린 term `id` 목록(아래 판정) — 시드 순서 · 중복 없음 · 없으면 `[]`. 0.9.0 — 바로잡은 뒤의 `translation` 으로 판정한다(바로잡은 term 은 번역 쪽에서도 걸린다) |
| **`fixed`**(0.9.0) | utterance | **바로잡은 term `id` 목록**(§5.12 — 그 발화에서 번역 속 틀린 꼴을 사전 이름으로 갈아 끼운 term) — 시드 순서 · 중복 없음 · **바로잡은 것이 없으면 `[]`(키는 늘 있다)**. 바로잡기가 꺼진 세션(품질 시험 인자)도 `[]`. 원문에 걸렸지만 바꿀 꼴을 못 찾은 term 은 여기 없다(로그에만 — §5.12). `fixed` ⊆ `terms` |
| **`translation_before`**(0.9.1) | utterance · **`fixed` 가 비지 않은 줄에만** | **바로잡기 전의 번역** — Soniox 가 낸 그 발화의 번역을, 바로잡지 않았다면 자막으로 나갔을 모양으로(§5.6 번체 변환 · 빈칸 정리 뒤 · 괄호 그대로 — `translation` 과 같은 가공). 화면 · TTS 로는 나가지 않은 글이다. `fixed` 가 `[]` 이면 키 자체를 쓰지 않는다(`translation` 과 같은 글을 두 번 쓰지 않는다). **왜 남기나**(처분 §11): 기록은 서버 내부 검토용(D-41)이고, 운영에서 **새 틀린 꼴**(§4.2.5 「뒤에 더할 때」)과 **잘못 바꾼 것**(§5.12 「한계」)을 찾는 유일한 재료다. 못 찾은 발화는 `translation` 이 곧 Soniox 가 낸 글이라 따로 남길 것이 없다 |
| `reason` | end | `stop`(front 가 `stop`) · `close`(브라우저가 닫음 · 끊김 · 그 밖) · `error`(back 이 `error` 프레임을 보냄) |
| `code` | end · `reason=error` 일 때만 | §5.4 의 `code`(`soniox_unavailable` · `no_api_key` 등) |
| `utterances` | end | 그 세션에서 쓴 utterance 줄 수 |

**언제 쓰나**

| 줄 | 때 |
|---|---|
| `session_start` | `start` 를 받아 lang 이 정해진 직후(Soniox 연결 전). **`bad_request`(첫 프레임이 `start` 아님 · lang 밖 · 10초)는 세션이 아니다 — 아무 줄도 쓰지 않는다** |
| `utterance` | 그 세션의 caption 이 **`final:true` 로 나갈 때마다 1줄**(back 이 브라우저로 보내는 자리 · `_emit`). `final:false` 는 쓰지 않는다. 같은 `id` 가 다시 `final:true` 로 오면 처음 것만(세션 안 id 집합). `original` · `translation` 이 둘 다 비면 쓰지 않는다. `pause` · `stop` 뒤 flush 로 확정된 발화도 같은 규칙 |
| `session_end` | 세션 정리(`_cleanup`) 때 1줄 — `session_start` 를 쓴 세션만. 서버가 내려가며 끊긴 세션은 `close` |

**걸린 term 판정**(`terms`)

> 발화 줄의 `terms` 는, 그 세션 언어 `L` 에서 시드의 각 term `t` 의 **이름 목록**(`t.ko` · `t.ko_aliases` · `t.entries[L].name` · `t.entries[L].aliases` — `entries[L]` 이 없으면 ko 쪽만) 가운데 하나라도 그 줄의 `original` 또는 `translation` 에 **나타나면** `t` 가 걸린 것으로 하는 목록이다. 「나타난다」는 아래 정규화를 한 문자열끼리 본다. 한 문장 안에서 어떤 term 의 일치 구간이 **다른 term 의 더 긴 일치 구간 안에 통째로 들어가면** 짧은 쪽은 그 일치로는 걸린 것으로 치지 않는다.

| 항목 | 규칙 |
|---|---|
| 정규화 | 문장 · 이름 둘 다: `L ∈ {zh-Hant, yue}` 면 OpenCC `t2s`(자막은 번체 · 시드는 번체 원문이지만 변환 글자꼴이 다를 수 있다 — §4.5 와 같은 기준) → `casefold` |
| 라틴 이름 | 이름이 **ASCII 글자로만** 되어 있으면(예 `Thermage CPT` · `ACT` · `PN`) 문장의 연속 공백을 하나로 줄인 뒤 찾고, **앞뒤 글자가 ASCII 영문 · 숫자가 아니어야** 일치(「contact」 안의 「act」 는 아님) |
| 그 밖 이름 | 한글 · 한자 · 가나 · 태국 문자가 섞인 이름(예 `써마지FLX` · `黃金電波`)은 **문장 · 이름 둘 다 공백을 모두 지운 뒤** 부분 문자열로 찾는다(STT 가 「써마지 FLX」 처럼 띄어 쓴 것도 잡는다) |
| 더 긴 일치 | 예 「벨로테로 리바이브」 → `kr-009` 만(ph-007 「벨로테로」 는 치지 않음). 같은 문장의 다른 자리에 「벨로테로」 가 따로 있으면 ph-007 도 걸린다. (0.6.1 — 0.6.0 의 예 「써마지 CPT」 안의 ko 별칭 「써마지」 는 시드에서 지워져(§4.2.3 D ⑤) 시험은 가짜 시드로 같은 규칙을 본다) |
| 무엇을 뜻하나 | 「문장에 그 시술 이름이 나왔다」 — Soniox 가 용어집 짝을 실제로 썼는지 · 줄이기로 그 짝이 빠졌는지와는 무관(그건 §4.6 로그 몫). 내부 검토용 근사 |
| 어디서 | back `service/records.py` 의 순수 함수(예 `hit_terms(glossary, lang, original, translation) -> list[str]`) — 시드는 메모리의 `Glossary`(§4.3) 그대로. 발화마다 시드 전체를 훑는다(157 + 13 term · PoC 규모라 색인을 두지 않는다 — 기본값) |

**넣지 않는 것** — 음성(PCM) · 토큰 · `?token=` · 로그인 아이디 · 비밀번호 · IP · `Origin` · User-Agent · TTS 입력 문자열 · Soniox `request_id` · 키. 기록은 **대화 문장만** 갖는다(D-41 「음성 없음」 · public 레포 원칙과 같은 선).

**보관 기간 — env (0.7.0 — D-42 · 0.6.0 의 「7일 뒤 삭제」를 고침)**

> 「지금 베타 테스트 기간이라 데이터 모아야하는데 7일 보관 없애자」(D-42). 0.6.0 은 7일로 고정하고 env 로 못 바꾸게 했다 — 0.7.0 은 보관 기간을 env 로 빼고 **비어 있으면 지우지 않는다**. 베타가 끝나면 코드 수정 없이 값만 넣어 다시 켠다(언제 · 몇 일인지는 OQ-020).

| `INTERPRET_RECORD_KEEP_DAYS`(§2.4) | 동작 | 기동 로그(위 「기동」 ②) |
|---|---|---|
| 비어 있음 · 없음 · 공백만(앞뒤 공백을 지우고 판정 — 코디 기본값) | **삭제 안 함** — 기동 때 삭제 0 · 24시간 배경 작업을 **만들지 않는다** | `interpret records: on dir=<경로> keep_days=off` |
| 양의 정수 N — 앞뒤 공백을 지운 뒤 **십진 숫자로만 된 1 ~ 36,500 의 값**(`7` · ` 7 ` · `07` = 7 · 상한 100년 = 날짜 계산이 넘치지 않게 · 코디 기본값) | 아래 삭제 규칙(0.6.0 규칙 그대로 · 7 자리에 N) — 기동 1회 + 24시간마다 | `interpret records: on dir=<경로> keep_days=N` |
| 그 밖의 값(0 · 음수 · 숫자 아님 · 36,500 초과 — `+7` · `7.0` · `7d` · `1000000` 포함) | **경고 로그 1줄 뒤 삭제 안 함** — 기동은 멈추지 않는다(기록은 통역의 부속 · 위 「기동」 ③과 같은 결 · 코디 기본값) | 경고 1줄 + `… keep_days=off` |
| (기록 끔 — `INTERPRET_RECORD_DIR` 비었음) | 0.6.0 그대로 파일 · 삭제 작업 없음 — 이 값과 무관 | `interpret records: off` |

- 운영은 이 값을 **ConfigMap 에 넣지 않는다**(= 삭제 안 함 · §9.6). 로컬 · 시험 기본도 비어 있다.
- 잘못된 값 때문에 기동이 멈추면 안 된다 — 설정을 읽는 단계의 정수 변환 실패로 프로세스가 죽지 않게 한다(값 판정은 위 표대로 · 방법은 backend).

**삭제 규칙 — 보관 기간이 N 일 때만**

| 항목 | 계약 |
|---|---|
| 대상 | 폴더 안 이름이 정확히 `YYYY-MM-DD.jsonl` 이고 그 날짜가 **오늘(한국 시간) − N 일 이하**인 파일 — 예 N=7 이면 10-28 에는 10-21 파일까지 지운다(그날 쓴 기록은 꽉 찬 N 일을 산다). 이름이 그 모양이 아닌 파일 · 폴더는 건드리지 않는다 |
| 때 | **기동 때 1회 + 그 뒤 24시간마다**(lifespan 의 배경 작업 · 종료 때 취소). 기록 끔 · 보관 기간 `off` 면 돌지 않는다(배경 작업 자체가 없다) |
| 실패 | 파일 하나 지우기 실패 → 경고 로그 1줄(예외 종류 · 파일 이름) 뒤 다음 파일 계속. 작업 전체가 죽지 않는다 |
| 로그 | 지운 파일 수 1줄(`interpret records sweep: deleted=N`) — 내용 0. 보관 기간 `off` 면 이 줄은 나오지 않는다 |
| 보관 기간 | env `INTERPRET_RECORD_KEEP_DAYS`(위 표 · D-42). 0.6.0 의 「7일 고정 — env 로 바꾸지 않는다」(D-41 · 코디 기본값)는 D-42 로 없어졌다 |

**쓰기 실패는 통역을 끊지 않는다**

- 줄 쓰기에서 나는 예외(`OSError` 등 — 디스크 가득 · 권한 · 폴더 사라짐 · 직렬화)는 기록 쪽에서 삼킨다 → **경고 로그 1줄**(`interpret record write failed: <예외 종류>` — 문장 · 경로 밖 값 0) · 그 세션의 남은 줄은 계속 시도하되 **경고는 세션당 1번만**(로그 홍수 방지).
- 통역(caption · 오디오 · `ready` · 오류 코드)은 기록 성공 여부와 무관하게 지금과 같다. 기록 실패로 `error` 프레임을 보내거나 연결을 닫지 않는다.
- 판정(`terms`) 계산에서 나는 예외도 같은 처리 — 그 줄은 `terms: []` 로 쓴다. (0.9.0) `fixed` 는 바로잡기가 낸 값을 그대로 받는다 — 바로잡기가 예외로 건너뛴 발화는 `fixed: []`(§5.12 「예외」).

**화면 · API 없음** — 기록을 읽는 코드 · 경로 · 화면 · 다운로드를 두지 않는다(§3.5 허용 경로 6개 그대로 · `tests/test_api_surface.py` 가 고정). front 는 바뀌지 않는다. 꺼내기는 §9.6.

- 일반 로그에는 지금처럼 발화 원문 · 번역문을 쓰지 않는다(§5.8) — 대화 문장은 기록 파일에만.

### 5.10 STT 모델 · 끊김 설정 (0.8.0 — D-43 · D-47)

**모델 — `stt-rt-v6` (D-43)**

| 항목 | 계약 | 근거 |
|---|---|---|
| `STT_MODEL` | **`stt-rt-v6`**(back `service/interpret/soniox.py` 상수 한 곳 · 0.7.0 까지 `stt-rt-v5`) | D-43 |
| 그 밖의 STT 설정 | **그대로** — `audio_format` · `sample_rate` 16,000 · `num_channels` · `language_hints` · `enable_endpoint_detection` · `max_endpoint_delay_ms` · `translation`(two_way) · `context`. 키를 더하거나 빼지 않는다(v6 의 새 값 `enable_agent_text_input` 도 쓰지 않는다 — 음성 에이전트용 · 결정 없음) | 공식 `stt/models`(2026-11-14): 「The v6 models are fully compatible with the existing v5 models and Soniox API. To upgrade, simply replace the model name in your API request」 |
| TTS | `tts-rt-v2` 그대로 | 결정 없음 |
| 왜 지금 | `stt-rt-v5` 는 Deprecated · **2026-12-15 제거**(그 뒤 v5 요청은 v6 로 자동 연결). v6(2026-11-03)의 관련 변경 — 「More accurate real-time translation that adjusts how much speech it gathers before translating」 · context 를 더 잘 씀 · 이름 · 전문 용어 인식 | 공식 `stt/models` · BASE-001 확인한 사실(2026-11-14) |
| 순서 | **v6 단독 효과를 먼저 본다** — 다른 손질(`text` · 시드 `.7`) 없이 모델만 바꾼 조합 B 를 시험 목록으로 돌린다(§9.3 「6차」) | D-43 「다른 손질보다 먼저 v6 단독 효과를」 |

- 한도(§4.6 언어별 표)는 0.8.4 까지 v5 로 잰 값이었다 — **0.9.0 에서 v6 로 다시 잰 값으로 바꿨다**(§4.6 「D-56 표」 · D-56 · OQ-028 닫음).

**끊김(발화 끝 감지) — 1루프는 그대로 (D-47) · 0.9.0 「1000 유지」 로 확정 (D-55)**

> 기록(BASE-001 2026-11-14): 한국어 발화 112줄 중 62줄이 6자 이하 · 29줄이 문장 중간에서 끊겼고, 끊긴 조각이 오역으로 이어졌다.

| 항목 | 계약 | 근거 |
|---|---|---|
| 1루프 값 | **`max_endpoint_delay_ms: 1000` 그대로** · `enable_endpoint_detection: true` 그대로 · 다른 끊김 값은 보내지 않는다(= Soniox 기본) | D-47 「v6 로 먼저 보고」 |
| 손보는 조건 | 품질 시험 **3절(T23 ~ T26 — 문장 중간 쉼)이 v6(조합 B · C)에서도 조각나면**(조각 수 = 실제 확정 발화 수 − 기대 수 > 0 · §9.3) **덜 끊는 쪽으로** 끊김 값을 손본다 | D-47 |
| 얼마로 | **이 문서는 정하지 않는다**(OQ-027) — 값을 올리면 말이 끝난 뒤 자막 · 음성이 그만큼 늦는다. 그 맞바꿈은 **사용자가 실물에서** 판단한다. 품질 시험이 3절의 조각 수와 지연(발화 끝 → 확정까지)을 수치로 올린다 | D-47 「지연이 느는 만큼은 실물에서 사용자가 판단」 |
| 바꾸는 방법 | 값이 정해지면 이 절 · `stt_config` · 시험(§9.1 「통역」)을 같이 고친다(코디 → planner → backend) | — |
| **결과(0.9.0 · D-55)** | **`max_endpoint_delay_ms` = 1000 그대로 둔다.** 조합 C2(C 와 같고 이 값만 2000)의 3절 조각 수(합 4) · 기계 판정(FAIL 6 — 같은 번호) · 사람 판정(등급별 수 같음)이 C 와 같았고, T23 · T25 의 지연만 900 ~ 1,000 ms 늘었다(§9.3 「6차 결과」) — 쉼 자리의 끊김을 막지 못하고 늦어지기만 한다. `endpoint_sensitivity` 는 돌려 보지 않았다(보내지 않음 = Soniox 기본 그대로). **OQ-027 닫음** — 사용자가 비교 페이지에서 다른 판단을 주면 이 행을 고친다 | D-55 · WP24 |

**공식 문서의 끊김 값**(`stt/rt/endpoint-detection` · 2026-11-14 — 이름 · 범위 · 기본값만 인용 · 어느 모델이 받는지는 그 문서에 없다)

| 이름 | 범위 | 기본 | 공식 설명 | 지금 |
|---|---|---|---|---|
| `enable_endpoint_detection` | bool | (문서에 기본값 없음) | 켜면 발화 끝에서 `<end>` 토큰 | `true` |
| `max_endpoint_delay_ms` | 500 ~ 3000 | 2000 | 「sets the maximum time Soniox can wait before returning an endpoint after speech has ended」 | **1000** |
| `endpoint_sensitivity` | −1.0 ~ 1.0 | 0.0 | 「controls how likely Soniox is to emit an endpoint」 | 안 보냄 |
| `endpoint_latency_adjustment_level` | 0 · 1 · 2 · 3 | 0 | 「reduces endpoint latency compared to the default endpointing behavior」 | 안 보냄 |

- D-47 의 「끊김 감도」 = 위 `endpoint_sensitivity` 다. 이 값들은 **v6 전용이 아니다** — 공식 v6 변경 목록에 끊김 값 이야기는 없다(v6 가 끊김에 주는 영향은 「번역 전에 모으는 말의 양을 조절」 한 줄뿐).
- **덜 끊는 쪽의 방향(0.8.1 · D-47)**: `max_endpoint_delay_ms` 는 **올린다** · `endpoint_sensitivity` 는 **낮춘다** — 공식 문서 「Higher values make endpoints more likely」(값이 클수록 더 잘 끊는다). `endpoint_latency_adjustment_level` 은 끊김을 앞당기는 값이라 덜 끊으려는 손질에는 쓰지 않는다(0 그대로). 얼마로 할지는 실물로 확인한 값만 쓴다(OQ-027).
- 「누르고 말하기」(D-36)는 뗄 때 `pause` → finalize 로 발화가 확정된다 — 끊김 값과 무관하다(그대로).

### 5.11 빈 원문 막기 (0.8.0 — D-48)

> 기록(BASE-001 2026-11-14): 원문이 마침표뿐인 발화에 원문에 없는 번역이 붙어 손님에게 나간 줄이 있다. Soniox 가 소리 없는 구간 · 잡음에서 번역만 지어낸 것이다.

**빈 원문 판정** — 발화의 원문(그 시점까지의 원문 토큰을 이은 문자열)에 **유니코드 범주 `L`(글자) · `N`(숫자)인 글자가 하나도 없으면** 빈 원문이다.

| 예 | 판정 |
|---|---|
| 빈 문자열 · 공백 · 줄바꿈뿐 | 빈 원문 |
| 문장부호뿐 — 마침표 · 쉼표 · 물음표 · 느낌표 · 말줄임표 · 따옴표 · 괄호 · 줄표(반각 · 전각 · CJK `。` `、` `？` `！` `…` 포함 — 범주 `P`) | 빈 원문 |
| 기호뿐 — `~` · `♪` 같은 것(범주 `S`) · 보이지 않는 글자(범주 `C`) · 결합 부호만(범주 `M`) | 빈 원문(기본값 — D-48 의 「문장부호뿐」 을 「글자 · 숫자 없음」 으로 넓게 읽는다) |
| 글자 · 숫자가 하나라도 있음 — 「네.」 · 「어,」 · 「30」 | **빈 원문 아님**(그대로 나간다 — 짧은 말을 막지 않는다) |

**동작**

| 항목 | 계약 |
|---|---|
| 확정 발화 | 빈 원문으로 확정된 발화는 **자막(`caption`)으로도 TTS 로도 내보내지 않는다** — 번역문이 있어도. `audio_start` · 오디오 · `audio_end` 없음 |
| 확정 전(`final:false`) | 그 시점 원문이 빈 원문이면 그 caption 을 보내지 않는다(번역만 든 말풍선이 뜨지 않게). 원문에 글자가 생기면 그때부터 지금처럼 보낸다 |
| 이미 보인 말풍선 | 같은 `id` 의 `final:false` caption 이 **이미 나간 뒤** 빈 원문으로 확정되면(확정 전 글자가 확정에서 사라진 경우) `original` · `translation` 이 **둘 다 빈 문자열인 `final:true` caption 을 1번** 보낸다 — front 는 글이 빈 말풍선을 그리지 않는다(`front/lib/view.ts` · 배포본) → 화면에서 사라진다. 나간 적이 없으면 아무것도 보내지 않는다 |
| WS 메시지 모양 | **그대로**(§5.3 — 새 종류 · 새 필드 없음). front 코드는 바꾸지 않는다 |
| 발화 `id` | 막힌 발화가 번호를 써도 된다(`u3` 다음이 `u5` 일 수 있다) — `id` 는 발화를 가르는 이름일 뿐이다(§5.3) |
| 통역 기록(§5.9) | §5.9 문구 그대로 — utterance 줄은 「`final:true` caption 이 **나갈 때**」 쓴다. 막힌 발화는 나가지 않으므로 **줄이 없다**(둘 다 빈 `final:true` 도 §5.9 「둘 다 비면 쓰지 않는다」). **막힌 발화를 기록에 남길지는 DEC 에 없다 → OQ-026** |
| 로그 | 막을 때 정보 로그 1줄 — `interpret blank original dropped: id · side · 원문 글자 수 · 번역 글자 수`(문장 0) |
| 자리 | 판정 함수는 한 곳(`assembler.py` — `strip_parens` 옆) · 내보내는 자리(`CaptionAssembler` 또는 `session._emit`)에서 한 번만 건다. TTS 큐에 넣기 전에 걸러 `_tts_worker` 는 건드리지 않는다 |
| 끄는 길(0.8.1 · W-1) | **운영에서는 늘 켠다.** 세션(`InterpretSession`)이 받는 선택 인자(기본 = 켬)로만 끌 수 있고 **품질 시험 스크립트만** 끈다(조합 A · B) — env · WS `start` 로는 못 끈다 · 통역 API 경로는 인자를 주지 않는다(§9.3 「조합」) |

- **막지 않는 것**: 원문에 글자가 있는데 번역이 틀리거나 지어낸 경우(원문과 번역을 견주는 판정은 없다) · 원문은 있고 번역이 빈 경우(지금 그대로 — 자막만 나가고 TTS 없음).
- `side` 판정 · 발화 묶기 · 괄호 제거(§5.7)는 그대로다.
- (0.9.0) **막힌 발화는 시술명 바로잡기(§5.12)를 거치지 않는다** — 나가지 않는 글이다. 순서 = 빈 원문 판정 → (막히지 않은 확정 발화만) 바로잡기 → 자막 · TTS · 기록.

### 5.12 시술명 바로잡기 (0.9.0 — D-58 · 0.9.2 — D-63 · D-64 · 0.9.3 — D-65 · D-66)

> 품질 시험 6차(§9.3 「6차 결과」): 사전 값이 context 에 들어갔는데도 울쎄라 · 써마지 · 스컬트라 · 보툴렉스 zh 가 영문 음역 · 다른 낱말로 나왔고, 손님 쪽 울쎄라 th 는 한국어 번역이 다른 시술로 나갔다. Soniox `translation_terms` 는 모델에 주는 **참고**다 — 보장이 아니다. 그래서 번역이 나온 **뒤에** back 이 한 번 더 본다: 「원문에 그 시술이 있는데 번역에 사전 이름이 없으면, 번역 속 틀린 꼴을 사전 이름으로 바꾼다」(D-58).
> **사전 이름 자체는 바꾸지 않는다** — 어느 이름이 맞는지는 D-46 규칙(현지어 우선 · 현지에 없으면 영어 · 0.9.2 — D-61: 그 나라 글자가 있는 언어는 그 나라 글자로)으로 시드가 정한다. 바로잡기는 「사전과 다른 꼴이 나가는 것」만 막는다.
> **0.9.2 — 7차 결과로 두 군데를 고쳤다**: ② 에서 **한자를 같이 쓰는 언어 사이의 한자 꼴**을 후보에서 뺀다(D-63 — 그 언어에서도 맞는 낱말일 수 있다) · 외 → 한에 **④ 「가까운 한글 낱말」** 단계를 더한다(D-64 — 원문은 맞게 받아썼는데 한국어 이름으로 안 옮긴 칸). 아래 「세 단계」 는 한 → 외에서는 그대로 셋이고 **외 → 한에서는 넷**이다.
> **0.9.3 — ④ 를 두 번 좁혔다**(D-65 · D-66 — 배포 전 코드 검수): 첫 음절이 같을 때만 · 남는 것이 비었거나 조사일 때만 · 음절이 빠진 꼴은 해석하지 않음 · 멈춤 목록을 낱말 전체에도. ① ② ③ 과 한 → 외는 그대로다.

**말 정리**

| 말 | 뜻 |
|---|---|
| `L` | 세션 언어(`start` 의 앱 lang · §5.5) |
| 방향 | 그 발화 caption 의 `side`(§5.3) — **`me` = 한 → 외**(원문 한국어 · 번역 `L`) · **`them` = 외 → 한**(원문 `L` · 번역 한국어) |
| 대상 쪽 맞는 이름 | 한 → 외 = `t.entries[L].name` · `aliases` / 외 → 한 = `t.ko` · `t.ko_aliases` |
| **대상 이름**(갈아 끼울 글) | 한 → 외 = **`norm(t.entries[L].name)`**(§4.5 의 `norm` — `L ∈ {zh-Hant, yue}` 면 `t2s` · Soniox 에 정방향 target 으로 준 것과 같은 문자열) / 외 → 한 = **`t.ko`**(ko 대표명) |
| 번역문 | Soniox 가 낸 그 발화의 번역 — **번체 변환(§5.6) 전 · 괄호 그대로**(자막 · TTS 로 갈라지기 전의 한 문자열) |
| 「나타난다」 | §5.9 「걸린 term 판정」 의 규칙 그대로 — 정규화(`L ∈ {zh-Hant, yue}` 면 `t2s` → `casefold`) · ASCII 뿐인 이름은 연속 공백을 하나로 줄이고 앞뒤가 ASCII 영문 · 숫자가 아니어야 · 그 밖 이름은 문장 · 이름 둘 다 공백을 모두 지우고 부분 문자열. **조건 1 · 2(걸렸나 · 있나)는 이 규칙 그대로 본다** |
| **「바꿀 자리」의 낱말 경계**(0.9.1 · F-1) | **글을 갈아 끼우는 일치(① ② ③)** 에서 ASCII 뿐인 꼴 · 라틴 낱말의 경계는 더 좁게 본다 — **앞뒤 글자가 라틴 글자 · 숫자가 아니어야** 한다. 「라틴 글자」 = ASCII 영문 **+ 부호 · 성조가 붙은 라틴 글자**(유니코드 문자 이름이 `LATIN` 으로 시작하는 글자 — 베트남어 `ệ` · `ơ` 류) · 숫자 = 유니코드 범주 `N`. 한글 · 한자 · 가나 · 태국 문자는 경계다(붙어 있어도 일치 — 예 한자 사이에 낀 영문 상표). §5.9 의 경계(ASCII 만)로는 베트남어 낱말이 성조 글자에서 조각나 **낱말 가운데**가 일치할 수 있다 — 판정만 할 때는 괜찮았지만 글을 바꿀 때는 안 된다. §5.9 기록 판정은 고치지 않는다(같은 찾기 함수에 경계 판정만 달리 준다) |

**걸리는 조건** — 막히지 않은(§5.11) **확정 발화**마다, 아래 둘을 모두 채우는 term `t` 가 바로잡을 term 이다.

| # | 조건 | 규칙 |
|---|---|---|
| 1 | **원문에 `t` 가 걸렸다** | §5.9 판정을 **원문 한쪽에만** 건 결과(코드로는 지금의 `_hits_in(glossary, L, original)` — 이름 목록 = `t.ko` · `t.ko_aliases` · `t.entries[L].name` · `aliases` · **「더 긴 일치」 포함**: 「써마지 CPT」 는 `kr-001` 만 걸린다). 기록의 `terms`(원문 ∪ 번역)와 같은 함수 · 같은 정규화를 쓴다 — 따로 짜지 않는다 |
| 2 | **번역에 대상 쪽 맞는 이름이 하나도 없다** | 번역문에 대상 쪽 맞는 이름(위 표) 가운데 어느 것도 「나타나지」 않는다. 여기에는 「더 긴 일치」 를 걸지 않는다(그 이름이 더 긴 다른 이름 안에 들어 있어도 「있다」 — 덜 바꾸는 쪽) |

- 별칭이라도 하나 나왔으면 **건드리지 않는다**(D-58 「`name` · 별칭이 하나도 없으면」) — 별칭을 `name` 으로 바꾸지 않는다.
- **같은 현지명을 나눠 가진 term(0.9.1 · W-1) — 외 → 한**: 원문에서 `t` 를 걸리게 한 그 이름(`entries[L].name` · 별칭)을 **다른 term `u` 도 갖고 있고**, 번역문에 `u` 의 `ko` · `ko_aliases` 가 나타났으면 **`t` 는 바로잡을 term 이 아니다**(로그 0 · 「못 찾음」 도 아님). context 의 역방향은 같은 현지명의 처음 짝만 보내므로(§4.5) 한국어 번역에는 그 묶음의 한 term 만 나오는 것이 계약대로다 — 시드 `.7` 에 이런 겹침이 17개 있다(zh-Hant 13 · zh 2 · ja 1 · yue 1 · 7차 시술 가운데 보툴렉스 · 토닝 · 쥬베룩이 든다). 한 → 외에는 이 줄이 필요 없다(대상 이름이 같아 조건 2 가 같이 풀린다).
- 한 → 외인데 `t.entries[L]` 이 없으면(그 언어에 표기가 없는 term) 대상 이름이 없다 — 바로잡지 않고 로그도 없다.
- 원문에 걸린 term 이 없으면(STT 가 시술명을 잘못 들은 발화 포함) 아무 일도 하지 않는다 — **인식 오류는 이 절의 대상이 아니다**.

**바꿀 꼴 찾기 — 세 단계(+ 외 → 한은 ④ · 0.9.2) · 앞 단계에서 바꿨으면 뒤 단계로 가지 않는다 · ③ 은 번역 글자가 라틴이 아닌 쪽에서만(0.9.1)**

| 단계 | 후보(번역문에서 찾을 꼴) | 찾는 법 · 바꾸는 법 |
|---|---|---|
| **① 시드의 틀린 꼴** | 한 → 외 = `t.entries[L].wrong` / 외 → 한 = `t.ko_wrong`(§4.2 · §4.2.5) | 「나타난다」 규칙으로 번역문에서 찾아, **일치하는 자리 전부**를 대상 이름으로 갈아 끼운다. 후보가 여럿이면 **긴 꼴부터**(정규화 뒤 글자 수 내림 · 같으면 목록 순서) |
| **② 그 term 의 다른 언어 이름 · 별칭** | 한 → 외 = `t.ko` · `t.ko_aliases`(번역에 한글이 그대로 남은 경우) + `L` 이 아닌 모든 언어 `M` 의 `t.entries[M].name` · `aliases` / 외 → 한 = **`L` 을 포함한** 모든 언어 `M` 의 `t.entries[M].name` · `aliases`(번역에 외국어 이름이 그대로 남은 경우) — 라틴 · 한자 · 가나 · 태국 문자 모두. **(0.9.2 · D-63) 한 → 외이고 `L ∈ {ja, zh, zh-Hant, yue}`(한자 언어)이면, 다른 한자 언어 `M ∈ {ja, zh, zh-Hant, yue}` 의 이름 · 별칭 가운데 한자가 든 꼴은 후보에서 뺀다** — 라틴 · 가나만인 꼴은 그대로 후보다 · ko 쪽 · th · en · vi 의 꼴도 그대로 · 외 → 한은 그대로(번역이 한국어라 한자 꼴은 남은 외국어다) | ① 과 같다(전부 · 긴 꼴부터 · 같은 길이는 시드 `langs` 순서 → `name` → `aliases` 순서) |
| **③ ① ② 와 아주 가까운 라틴 낱말** — **도는 범위(0.9.1 · F-1): 한 → 외는 `L ∈ {ja, zh, zh-Hant, th, yue}` 만 · 외 → 한은 7개 언어 전부.** `L ∈ {en, vi}` 의 한 → 외는 **① ② 만**(③ 없음) | 바탕 = ① ② 후보 가운데 **ASCII 뿐인 꼴** + 대상 쪽 맞는 이름 가운데 ASCII 뿐인 것(맞는 이름을 살짝 틀리게 적은 꼴도 틀린 꼴이다 — 기본값). 번역문의 **라틴 낱말**(라틴 글자 · 숫자가 이어진 구간 — 위 「바꿀 자리의 낱말 경계」 · ASCII 가 아닌 글자가 든 낱말은 견주지 않는다)과 견준다 | 아래 「가까운 라틴 낱말」 기준에 드는 것 가운데 **가장 가까운 하나만** 대상 이름으로 갈아 끼운다 |
| **④ 가까운 한글 낱말**(0.9.2 · D-64 · **0.9.3 — D-65 · D-66 으로 좁힘**) — **외 → 한만**(7개 언어 전부). 한 → 외에서는 돌지 않는다 | **① ② ③ 으로 못 바꾼 term 에만.** 바탕 = `t.ko`(ko 대표명 하나 — ko 별칭은 바탕이 아니다 · **한글로만 된 3음절 이상** 대표명만). 번역문(한국어)의 **낱말 앞부분**과 견준다 — **첫 음절이 대표명과 같고 · 뒤에 남는 것이 비었거나 조사일 때만** · 아래 「가까운 한글 낱말」 기준 | 기준에 드는 것 가운데 **하나만** · **그 앞부분만** ko 대표명으로 갈아 끼운다(뒤에 붙은 조사는 그대로) |

- **후보에서 빼는 것**(① ② ③ 공통): ⓐ `t` 의 대상 쪽 맞는 이름과 같은 꼴 ⓑ **다른 term 의 대상 쪽 맞는 이름과 같은 꼴**(한 → 외 = 어느 term 이든 `entries[L].name` · `aliases` / 외 → 한 = 어느 term 이든 `ko` · `ko_aliases`) — 맞게 나온 옆 시술 이름을 덮어쓰지 않는다(예 보툴렉스가 걸렸는데 번역에 「보톡스」 의 그 언어 이름이 있는 경우 그 이름은 후보가 아니다). 「같다」 = 검사 8(§4.2)의 비교.
- **보호 구간** — 번역문에서 **이미 맞게 나온 다른 term 이름의 일치 구간**(§5.9 판정을 번역 한쪽에 건 일치 구간)과 **앞 term 이 이미 갈아 끼운 구간**은 건드리지 않는다. 후보의 일치 구간이 보호 구간과 한 글자라도 겹치면 그 자리는 건너뛴다.
- **① ② 는 근거가 있는 꼴이다**(시드에 적힌 것 · 사전의 다른 언어 값). **③ · ④ 는 추측이다** — 그래서 맨 뒤이고, 하나만 바꾸고, 기준 숫자를 좁게 둔다.
- **왜 ② 에서 한자 언어 사이의 한자 꼴을 빼나(0.9.2 · D-63)**: 일본어 · 중국어(간체 · 번체) · 광둥어는 한자를 같이 쓴다 — 다른 한자 언어의 사전 이름이 **그 언어에서도 뜻이 맞는 보통 낱말**일 수 있다. 7차 첫 실행의 ja 직원 쪽 1행에서 맞는 번역 속 낱말이 다른 한자 언어의 이름과 같다는 이유로 바뀌었다(사람 판정 「잘못 바꿈」 1). 이 꼴을 빼면 그 칸은 「못 찾음」 으로 남는다(번역은 그대로 나간다 · 로그 1줄) — 맞는 번역을 망가뜨리는 것보다 낫다. 같은 꼴을 꼭 바꿔야 하는 칸은 **① 시드 틀린 꼴**로 그 칸에만 넣는다.
- **왜 ③ 을 라틴이 아닌 쪽에만(0.9.1 · F-1)**: 번역문이 영어 · 베트남어면 문장 전체가 라틴 낱말이다 — 시드 `.7` 의 ASCII 한 낱말 꼴 60개 가운데 15개 이상이 흔한 영어 낱말과 거리 1 ~ 2 라, 번역이 상표를 풀어 쓴 문장에서 **일반 낱말이 시술명으로 바뀐다**(거리를 1 로 줄여도 남는다 · 검수 6차). 일본어 · 중국어 · 태국어 번역과 한국어 번역에서는 라틴 낱말이 거의 상표다 — 6차에서 나온 틀린 꼴(zh 의 영문 음역)은 이 범위로 덮인다. en · vi 의 틀린 꼴은 **① 시드 목록으로만** 잡는다.
- **순서(0.9.1 · W-2) — 걸린 term 전부에 ① ② 를 먼저, 남은 term 만 ③**: 한 발화에 바로잡을 term 이 여럿이면 ⓐ 시드 순서로 term 마다 ① → ② 를 돌린다(바꿨으면 그 term 은 끝) ⓑ 그 뒤 **아직 못 바꾼 term 만** 시드 순서로 ③. 추측(③)이 다른 term 의 근거 있는 꼴(① ②)을 먼저 집어 가지 않는다(예 한 term 의 가까운 낱말이 옆 term 의 다른 언어 이름인 경우).

**가까운 라틴 낱말 — 기준(③)** — 아래 숫자는 **기본값이다 · 시험으로 확인한다**(DEC D-58 의 「아주 가까운」 을 숫자로 옮긴 planner 기본값 — 근거 실측 없음 · WP26 · 7차가 잘못 바꾼 수 · 못 바꾼 수를 내고 코디 · 사용자가 고친다 · OQ-032). 코드 상수 한 곳에 둔다.

| 항목 | 기본값 | 무엇 |
|---|---|---|
| 견주는 단위 | 낱말 수가 같은 것끼리 | 바탕 꼴이 낱말 `k` 개(공백으로 가름)면 번역문의 **이어진 라틴 낱말 `k` 개**(사이가 공백뿐인 것)를 한 칸으로 견준다. 견줄 때는 둘 다 `casefold` · 낱말 사이는 공백 하나 |
| 도는 범위(0.9.1) | 번역 글자가 라틴이 아닌 쪽 | 한 → 외 = `L ∈ {ja, zh, zh-Hant, th, yue}` · 외 → 한 = 전부. **en · vi 한 → 외에서는 ③ 을 돌리지 않는다**(처분 §11 F-1) |
| 길이 | **4글자 이상** | 바탕 꼴 · 번역문 쪽 둘 다 공백을 뺀 글자 수가 4 이상일 때만(짧은 약어 — 3글자 이하 — 는 ③ 으로 바꾸지 않는다) |
| 거리 | **편집 거리 ≤ 2** | 글자 넣기 · 빼기 · 바꾸기를 1 로 세는 편집 거리(Levenshtein). 0 은 ① ② 에서 이미 잡혔다 |
| 고르기 | 가장 가까운 하나 | 거리가 가장 작은 것 · 같으면 번역문에서 앞쪽 · 그것도 같으면 바탕 꼴의 후보 순서. **한 term 에 한 자리만** 바꾼다 |
| 빼는 것 | 위 「후보에서 빼는 것」 ⓑ · 보호 구간 | 번역문 쪽 낱말이 다른 term 의 맞는 이름이면 거리가 가까워도 바꾸지 않는다 |

- 라틴이 아닌 글자(한자 · 가나 · 태국 문자 · 한글)의 「비슷한 꼴」 은 ③ 이 다루지 않는다 — 그런 꼴은 **① 시드 목록으로만** 잡는다(음역 변형을 규칙으로 짓지 않는다). **(0.9.2) 한글만 예외다 — 외 → 한의 ④ 가 받는다.**

**가까운 한글 낱말 — 기준(④ · 0.9.2 · D-64 · 0.9.3 — D-65 · D-66)** — D-64 가 연 단계를 배포 전 코드 검수 두 번(`review-predeploy-code-report.md` F-1 · F-2 · W-1 · `-2.md` W-1 · W-2)이 좁혔다: 조사를 먹는 꼴 · 일상 낱말을 시술명으로 바꾸는 꼴 · 낱말 가운데를 자르는 꼴이 재현됐다. **남는 것은 「한 음절을 바꾼 꼴」 과 「한 음절이 더 붙은 꼴」 둘뿐이다.** 값은 코드 상수 한 곳(`KO_NEAR_MIN_SYL` · `KO_NEAR_MAX_DIST` · `KO_NEAR_STOP` · `KO_PARTICLES`)에 둔다 — 워커가 스스로 바꾸지 않는다.

| 항목 | 값 | 무엇 |
|---|---|---|
| 도는 범위 | **외 → 한만** | `side=them` · 7개 언어 전부. 한 → 외는 그대로(① ② ③) |
| 도는 때 | ① ② ③ 뒤 | 그 term 을 앞 단계에서 못 바꿨을 때만. 걸리는 조건(원문에 term · 번역에 ko 대표명 · ko 별칭 없음)은 같다 |
| 바탕 | `t.ko` | ko 대표명. **한글 음절로 세어 3음절 이상**일 때만 · **대표명에 한글 밖 글자(영문 · 숫자)가 들면 ④ 를 건너뛴다**(0.9.3 · 검수 W-1 — 음절 수를 한글 음절로 센다) |
| 견주는 단위 | 번역문 낱말의 **앞부분** | 낱말 = 공백 · 문장부호로 나눈 한글 구간. **앞부분 길이 = 대표명 음절 수(한 음절 바꿈) 또는 + 1(한 음절 더 붙음) 둘뿐**(0.9.3 · D-66 ⓑ). **대표명보다 짧은 앞부분(음절이 빠진 꼴)은 해석하지 않는다** — 「일상 낱말 + 조사」 가 「이름에서 한 음절 빠진 꼴」 과 같은 글자가 된다 |
| **첫 음절**(0.9.3 · D-65 ⓐ) | 대표명과 같아야 | 앞부분의 첫 음절 ≠ 대표명 첫 음절이면 후보가 아니다 — 이름 가운데 음절로 시작하는 일상 낱말을 막는다. **첫 음절을 틀리게 적은 꼴은 이제 안 바꾼다**(안전 우선 — 그 칸은 「못 찾음」 으로 남는다) |
| 거리 | **음절 편집 거리 = 1** | 음절(한글 한 글자) 하나를 바꾸기 · 더하기. 0 은 조건 2 에서 이미 「있다」 다. **2 이상은 바꾸지 않는다**(D-66 — 넓히지 않는다 · OQ-033 닫힘) |
| **남는 것**(0.9.3 · D-66 ⓐ) | 비었거나 조사 | 그 낱말에서 앞부분을 뗀 나머지가 **빈 글이거나 조사 목록(`KO_PARTICLES`)의 하나일 때만** 후보다 — 순서를 뒤로 미는 것이 아니라 **거른다**. 남는 것이 다른 글자면 그 낱말은 이름이 아니다(낱말 가운데를 자르지 않는다) |
| **해요체 「요」**(0.9.3) | 조사가 아니다 | 홀로 붙은 「요」 는 동사 어미라 조사 목록에 넣지 않는다(남는 것이 「요」 뿐인 낱말은 후보가 아니다). 「이에요 · 예요 · 에요」 는 조사 목록에 둔다(이름 + 이다) |
| **끝 음절이 조사인 꼴**(0.9.3) | 후보에서 뺀다 | 앞부분 길이가 대표명과 같고 · 남는 것이 없고 · **그 끝 음절이 조사이며 그 앞이 대표명의 앞부분과 같은 꼴**(= 이름의 끝 음절이 빠지고 조사가 바로 붙은 꼴)은 「한 음절 바꿈」 으로 읽지 않는다 — 읽으면 조사를 지운다(D-64 「조사는 그대로」 를 깬다 · 검수 F-1) |
| 고르기 | 하나만 | 한 term 에 한 자리. 후보가 여럿이면 번역문에서 앞쪽 · 같은 자리면 **짧은 앞부분**(D-65 ⓑ — 조사를 덮지 않는다). 바꾸는 범위는 **그 앞부분만** — 뒤의 조사는 건드리지 않는다(받침에 맞춰 조사를 고치지 않는다 — 「조사 · 문법 맞추기 없음」 그대로) |
| 바꾸지 않는 것 | ⓐ 다른 term 의 `ko` · `ko_aliases` 와 같은 꼴 ⓑ **멈춤 목록**의 낱말 ⓒ 보호 구간 | ⓑ 는 시술명과 닮은 일상 낱말 — **코드 상수 `KO_NEAR_STOP`(시드 · env 아님)**. **앞부분에도 · 낱말 전체에도 · 조사를 뗀 낱말에도 건다**(0.9.3 · D-65 ⓒ). 지금 21개: 울트라 · 테라피 · 마사지 · 레이저 · 주사 · 마지막 · 리프팅 · 페이스 · 풀페이스 · 레티놀 · 리투얼 · 레이스 · 지방 · 나보다 · 목주변 · 사각형 · 콜라 · 마이크로 · 사각지대 · 레티노이드 · 뉴스. 늘릴 때는 코디 확인(운영 기록의 `translation_before` 에서 나온 낱말) |
| 같은 현지명 묶음 | ④ 뒤에도 다시 본다 | 앞 term 이 ④ 로 갈아 끼운 ko 로 풀린 같은 묶음의 뒤 term 은 `fixed` 도 「못 찾음」 도 아니다(조건 2 의 W-1 줄 · 로그 0) |
| 로그 | `steps` 에 `4` | 「바꿨음」 로그의 `steps=<term 마다 1 · 2 · 3 · 4>` — 문장 · 꼴 0 |

- **왜 한글만 규칙으로 받나**: 외 → 한에서 번역이 한국어 이름을 **한 음절만 틀리게** 적는 경우가 7차 손님 쪽에 몰려 있었다(원문은 맞게 받아썼다 — 인식 문제가 아니다). 틀린 꼴이 실행마다 달라 ① 목록(`ko_wrong`)으로 쫓기 어렵고, 대상(ko 대표명)이 하나로 정해져 있어 잘못 바꿀 범위가 좁다.
- **왜 이만큼 좁혔나(0.9.3)**: ④ 가 도는 조건(원문에 그 term · 번역에 ko 이름 0)은 「번역이 이름을 틀린 발화」 다 — 틀린 꼴과 닮은 일상 낱말이 **같은 문장에 같이 있는 경우가 바로 대상**이라, 느슨한 규칙은 진짜 틀린 꼴을 두고 옆의 멀쩡한 낱말을 바꾼다. 잘못 바꾼 한국어 자막은 직원이 그대로 본다. **못 바꾸고 남기는 쪽(「못 찾음」 로그)이 잘못 바꾸는 쪽보다 낫다.**
- **거리 2 · 첫 음절이 다른 꼴 · 음절이 빠진 꼴은 받지 않는다**(D-64 「음절 하나만」 · D-65 · D-66) — 7차 손님 쪽에는 대표명과 두 군데가 다른 꼴 · 다른 문자가 섞인 꼴 · 첫 음절이 다른 꼴도 있었다. 그런 칸은 「못 찾음」 으로 남는다. **넓히지 않는다 — OQ-033 닫힘(0.9.3 · D-66).** 꼭 바꿔야 하는 꼴이 운영 기록에서 되풀이되면 그 꼴만 `ko_wrong`(① )에 넣는다(일상 낱말이 아닌 것만 — §4.2.5 ⓓ).

**여러 term · 끝 · 못 찾음**

| 항목 | 계약 |
|---|---|
| 한 발화에 바로잡을 term 이 여럿 | **term 마다 따로** — 위 「순서」(① ② 를 전부 먼저 · ③ 은 남은 term 만) 안에서 시드 순서로 하나씩, 앞 term 이 고친 번역문 위에서 이어 간다(보호 구간 유지). 같은 꼴이 두 term 의 후보이면 **같은 단계 안에서** 시드 순서가 앞인 term 이 갖는다 |
| 끝 | 한 단계에서 한 자리라도 갈아 끼웠으면 그 term 은 끝 — 번역문에 대상 이름이 생겼다(다음 단계로 가지 않는다) |
| **못 찾음** | 세 단계(외 → 한은 ④ 까지 네 단계) 모두 바꿀 자리가 없으면 **번역문을 그대로 둔다**(이름을 끼워 넣거나 문장을 고쳐 쓰지 않는다) + **정보 로그 1줄** `interpret term not corrected: term=<term id> lang=<L> side=<side>` — **문장 · 꼴 0**. 이 로그가 다음 판 틀린 꼴(§4.2.5 「뒤에 더할 때」)의 신호다 |
| 바꿨음 | 정보 로그 1줄(발화마다) `interpret term corrected: id=<발화 id> side=<side> lang=<L> terms=<term id 들> steps=<term 마다 1 · 2 · 3>` — 문장 · 꼴 0 |
| 결과 값 | 순수 함수가 **(고친 번역문 · 바로잡은 term id 목록 · 못 찾은 term id 목록)** 을 낸다 — 바로잡은 목록이 기록의 `fixed`(§5.9) · (0.9.1) 바로잡은 목록이 비지 않으면 **고치기 전 번역문**도 같이 들고 가 기록의 `translation_before` 로 쓴다 |
| 예외 | 바로잡기 안에서 나는 예외는 삼킨다 — 그 발화는 **고치지 않은 번역문 그대로** 내보내고 경고 로그 1줄(예외 종류만) · `fixed: []`. 통역(caption · 오디오)을 끊지 않는다(§5.9 「쓰기 실패」 와 같은 결) |

**자리 · 나가는 곳**

| 항목 | 계약 |
|---|---|
| 언제 | **발화가 확정될 때 한 번**(`final:true` caption 을 만들기 직전 — 자막 · TTS · 기록으로 갈라지기 전). `pause` · `stop` 뒤 flush 로 확정된 발화도 같다 |
| `final:false` | **그대로** — 확정 전 말풍선은 바로잡지 않는다(갱신마다 사전을 훑지 않는다 · 확정 전 글은 어차피 바뀐다). 그래서 확정 때 말풍선의 시술명이 바뀌어 보일 수 있다 |
| **한 번 고친 글에서 셋이 나온다** | 고친 번역문 → ⓐ **자막**: `final:true` caption 의 `translation`(§5.6 번체 변환 · 빈칸 정리는 고친 뒤에 지금처럼) ⓑ **TTS**: 그 글을 §5.7 괄호 제거 뒤 읽는다(zh-Hant · yue 는 간체 그대로 — 대상 이름이 `norm` 값이라 맞는다) ⓒ **기록**: utterance 줄 `translation`(= 자막) + `fixed` + (0.9.1) `translation_before`(§5.9 — 바로잡은 줄에만). 셋이 서로 다른 글을 갖지 않는다(자막만 고치고 TTS 는 옛 글을 읽는 경우 0) |
| WS 메시지 모양 | **그대로**(§5.3 — 새 종류 · 새 필드 없음 · 바로잡았다는 표시를 front 로 보내지 않는다). front 코드는 바꾸지 않는다 |
| 원문 | **건드리지 않는다** — 바로잡는 것은 번역뿐이다(STT 가 들은 원문은 그대로 자막 · 기록에) |
| 코드 자리 | 순수 함수 하나(예 `correct_terms(glossary, lang, side, original, translation) -> (translation, fixed, missed)`) — **§5.9 판정과 같은 찾기 함수를 쓴다**(`records.py` 의 정규화 · 일치 구간 함수를 같이 쓰고 복사하지 않는다 — 둘이 어긋나면 「걸렸다」 의 뜻이 둘이 된다). 부르는 자리는 발화를 확정하는 한 곳(`CaptionAssembler` 가 `final:true` caption 과 TTS 용 `Utterance` 를 만드는 자리 — 번체 변환 전의 번역문을 고친 뒤 둘을 만든다). 파일 나누기 · 이름은 backend. **(0.9.1 · W-3) ⓐ 빈 원문이면 부르지 않는다** — 빈 원문 막기(§5.11)는 지금 그 뒤(`session._emit` 의 `_blank_filter`)에서 걸린다. 발화를 확정하는 자리에서 `is_blank(원문)` 을 먼저 보고 참이면 바로잡기를 건너뛴다(빈 원문에는 걸린 term 이 없어 결과는 같지만, 부르지 않는 것이 계약이다 — §9.1 ⑥) **ⓑ `fixed` · `translation_before` 는 caption dict 에 싣지 않는다** — `_emit` 은 caption dict 를 그대로 브라우저로 보낸다. 실으면 WS 로 샌다(§5.3 「새 필드 없음」). 기록 쪽(`record.caption`)으로는 **caption 과 따로** 넘긴다(방법은 backend — 예 `Utterance` 나 별도 값) **ⓒ 자리 대응** — 일치 구간은 정규화한 글에서 찾고 원래 글의 자리로 되돌려 갈아 끼운다. `t2s` · `casefold` 가 글자 수를 바꾸면 자리가 어긋난다 — 이 앱이 다루는 글(한글 · 한자 · 가나 · 태국 문자 · 라틴)에서 **정규화 앞뒤 글자 수가 같다**는 것을 시험 1건으로 고정하고(§9.1), 길이가 달라지는 글자(예 `ß` → `ss`)가 든 발화는 그 발화만 바로잡지 않는다(「예외」 와 같은 처리) |
| 시드 | 메모리의 `Glossary`(§4.3) 그대로 — `Term` 에 `ko_wrong` · `Entry` 에 `wrong` 을 더해 읽는다. 발화마다 시드 전체를 훑는다(170 term · PoC 규모라 색인을 두지 않는다 — §5.9 와 같은 기본값) |
| **끄는 길** | **운영에서는 늘 켠다.** 세션(`InterpretSession`)이 받는 선택 인자(기본 = 켬)로만 끌 수 있고 **품질 시험 스크립트만** 끈다(6차 조합 C 를 같은 코드에서 다시 볼 때) — env · WS `start` 로는 못 끈다 · 통역 API 경로는 인자를 주지 않는다(§5.11 「끄는 길」 · §9.3 「조합」 과 같은 방식) |
| 밖으로 | 틀린 꼴 목록 · 바로잡은 표시는 응답 · front 번들 · WS 메시지에 나가지 않는다(§3.5 그대로). 일반 로그에 문장 · 꼴 0 |

**바꾸지 않는 것 · 한계**

- **뜻이 틀린 번역**(시술명 말고 문장이 틀린 것) · **말투** — 이 절은 시술명 낱말만 본다.
- **원문에 term 이 안 걸린 발화** — STT 가 시술명을 다른 낱말로 들은 경우(6차 손님 쪽 T34 · T49). 번역만 보고 시술명을 짐작해 넣지 않는다.
- **번역이 시술명을 풀어 쓰거나 빼 버린 경우**(대명사 · 설명으로 옮김) — 바꿀 꼴이 없어 「못 찾음」 으로 남는다.
- **조사 · 문법 맞추기 없음** — 갈아 끼우는 것은 낱말뿐이다. 외 → 한에서 ko 대표명 뒤 조사(「을/를」 · 「이/가」)가 받침과 안 맞을 수 있다(예 틀린 꼴과 대표명의 끝소리가 다를 때). 손보지 않는다 — 기본값.
- **en · vi 한 → 외의 틀린 꼴은 시드 목록(①)과 다른 언어 이름(②)으로만 잡힌다**(0.9.1) — 목록에 없는 새 음역은 「못 찾음」 으로 남고, 기록 · 로그로 모아 다음 판에 넣는다.
- **잘못 바꿀 수 있는 자리** — ① 의 꼴이 일반 낱말일 때 같은 발화 안에서 제 뜻으로 쓰인 그 낱말(§4.2.5) · ③ 의 가까운 낱말이 우연히 다른 영어 낱말일 때(0.9.1 — ja · zh · th · yue 번역 · 한국어 번역 속의 영어 낱말로 좁혀졌다) · **(0.9.2 · 0.9.3) ④ 의 가까운 한글 낱말이 멈춤 목록에 없는 일상 낱말일 때** — 지금 남은 틈은 「대표명과 첫 음절이 같고 · 길이가 같거나 한 음절 길고 · 한 음절만 다르고 · 뒤가 비었거나 조사인 일상 낱말」 뿐이다(D-65 · D-66 · 운영 기록의 `translation_before` 로 보고 멈춤 목록을 늘린다) · ② 의 th · en · vi 꼴은 D-63 뒤에도 그대로 후보다. 잘못 바꾼 발화는 기록의 `translation_before` 로 찾는다(§5.9). 조건 1 · 2(원문에 term · 번역에 이름 없음)가 범위를 좁히지만 0 은 아니다 — 7차(§9.3)가 「바로잡은 칸」 을 사람 판정으로 본다.

## 6. 화면 공통 — D-07 · D-10 · D-20 · D-21 · D-30

> 0.3.0 — **화면 정본 = 확정 시안**(D-20). 화면마다 근거 시안 파일을 단다(`design/project/<파일>`). 시안의 마크업은 medikit JS 없이 medikit 1.4.0 클래스 값을 옮긴 것이다(`design/README.md`) — **구현은 진짜 medikit 컴포넌트**를 쓰고 크기 · 색 · 글자 클래스를 시안 값에 맞춘다.

- 화면은 **둘**: `/login`(데모 모드면 단추 하나 · §7.1 · D-30) · `/`(통역). (D-07) 0.5.0 — 용어집 모달은 없다(D-37 · §7.6).
- 시안 화면은 **21개**(0.4.0 — r3 · `Login-Demo` · `Language-List` 추가 · `State-5-Paused` 에 초기화 / 0.5.0 — r7 `Mode-Auto-Idle` · `PTT-Ready` · `PTT-Pressed` 추가 · r8 `Glossary` 삭제 · `Menu` 로그아웃만). 시안보다 뒤에 정한 DEC(D-22 ~ D-25 · D-29 · D-31)가 시안과 다르면 DEC 를 따른다.
- 토큰이 없거나 만료면 `/` → `/login`. 로그인 성공이면 `/login` → `/`.
- 세로 화면 기준(기기 하나를 가운데 두고 양쪽이 본다 — 입력 3). 가로 고정은 하지 않는다. 시안 크기 390 × 844 — 다른 폭에서는 좌우 16px 여백을 두고 늘어난다.
- **테마(D-20)**: 루트 `<html lang="ko" data-product="ceramique">` + `app/styles/ceramique-theme.css`(cc-prototype `origin/main:procedure/front/app/styles/ceramique-theme.css` 를 **복사** — 시안 `project/ceramique-theme.css` 와 같은 내용) → `--ms-primary: #2498bd` · `--ms-primary-50/100: #e9f5f8` · `-300: #d3f4fe` · `-500: #b2e3f2`. import 순서는 원형 `procedure/front/app/layout.tsx` 그대로(medikit styles 뒤). 0.2.0 의 「`data-product` 두지 않음 · medikit 기본 파랑」은 **폐기**.
- **색 규칙(D-20 · 시안 README 「색 규칙」)**: 한국어 = `primary`(#2498bd) · 외국어 = `purple`(#ac47ff) · 대기 = `ms-gray-400` · 연결 중 · 멈춤 = `ms-gray-300` · 오류 = `red`. 원 둘레 링은 같은 토큰 값에 투명도만 준 `rgba`(primary `36,152,189` · purple `172,71,255` · red `255,78,81` · gray-400 `214,214,214`) — 토큰 클래스 밖 색은 이것과 카드 그림자 `rgba(0,0,0,.04)` · 오버레이 흰 선뿐.
- 바탕 `bg-ms-gray-100` · 카드 `bg-ms-white` · 둥글기 12px · 그림자 `0 2px 10px rgba(0,0,0,.04)`. 글꼴 Pretendard.
- **앱 이름(D-21)**: 「통키」(한글) · 「Tongky」(워드마크 · 영문). 문서 제목(`metadata.title`) = 「통키」 · 로그인 제목 = 「통키」 · 통역 화면 헤더 = 「Tongky」 · PWA 는 §8.
- 문구는 한국어. 단, 외국어 쪽 고정 문구(원 위 안내 · 오버레이 위 절반 · 「↓ 최신」)는 고른 언어로(§7.3 · §7.5) — 기본값.
- 아이콘: medikit 에 없는 것(햄버거 · 회전 · 원 안 글리프 · 말풍선 · 눈 · 시계 · 손가락)은 **시안의 인라인 SVG 를 그대로**(24 · stroke 1.8 등 시안 값). medikit 에 있는 것은 medikit(`CloseIcon` · `ErrorIcon`).

## 7. 화면 — D-07 · D-08 · D-09 · D-16 · D-20 ~ D-25 · D-27 · D-29 · D-30 · D-31 · D-34 · D-36 · D-37

### 7.1 로그인 (D-06 · D-07 · D-21 · D-27 · D-30) — 시안 `Main.dc.html` · `Login-Error.dc.html` · `Login-Locked.dc.html` · `Login-Demo.dc.html`

```text
┌──────────────────────────┐  bg-ms-gray-100 · 세로 가운데
│ ┌──────────────────────┐ │  카드 bg-ms-white · 둥글기 12 · 안쪽 32/20/28
│ │        (💬)          │ │  48px 원 bg-primary-100 text-primary · 말풍선 SVG
│ │        통키          │ │  text-typo-headline-md-600 text-ms-gray-800
│ │ 상담 통역을 시작하려면 로그인하세요 │  text-typo-body-400 text-ms-gray-600
│ │ 아이디                │ │  label text-typo-body-500
│ │ [아이디를 입력하세요 ] │ │  medikit Input · h50 · 둥글기 8 · border-ms-gray-300 · 입력 글자 16px(D-27)
│ │ 비밀번호              │ │
│ │ [비밀번호를 입력하세요 👁]│  type=password · 눈 아이콘 = 표시 ↔ 숨김
│ │ [       로그인       ] │ │  medikit Button solid · bg-primary · h50 · 가득 · text-typo-heading-md-500
│ │ (오류 자리)           │ │
│ └──────────────────────┘ │
└──────────────────────────┘
```

| 경우 | 모양 | 문구 | 시안 |
|---|---|---|---|
| 기본 | 위 | — | `Main.dc.html` |
| 401 `invalid_credentials` | 두 입력 테두리 `border-red`(`aria-invalid`) + 단추 아래 오류 한 줄 `text-typo-body-500 text-red`(앞에 오류 아이콘) | 서버 `message` 그대로 | `Login-Error.dc.html` |
| 429 `too_many_attempts` | 입력 테두리는 그대로 · 단추 아래 `bg-red-100` 박스(둥글기 8 · 시계 아이콘) 안에 `text-red` | 서버 `message` 그대로 | `Login-Locked.dc.html` |
| 네트워크 실패 | 401 줄과 같은 한 줄(시안 없음) | 「서버에 연결하지 못했어요」 | — (design-report 제안 8 · 이 문서 문구) |
| **데모 모드(0.4.0 · D-30)** | 진입 때 `GET /api/auth/config` → `demoLogin: true` 면 **아이디 · 비밀번호 칸 없이** 아이콘 · 「통키」 · 부제 + 「로그인」 solid 50px 단추 하나 → `POST /api/auth/demo` → 통역 화면. `false` 거나 config 실패면 기본 화면. config 를 받기 전에는 칸 · 단추를 그리지 않는다(깜빡임 방지 — 카드 머리만). 데모 오류(401 등)는 401 줄과 같은 한 줄 | 서버 `message` 그대로 | `Login-Demo.dc.html` |

- 로그인 부제 · 말풍선 아이콘 · 비밀번호 표시 단추는 시안에서 더한 요소 — **채택**(D-21).
- 아이디 칸에 값을 미리 채우지 않는다(placeholder 만).
- **입력 글자 16px 이상(0.4.0 · D-27)** — iOS Safari 는 16px 미만 입력에 포커스하면 화면을 확대한다. 두 칸 모두 medikit `Input` 에 `inputClassName="text-typo-heading-md-400"`(16px — medikit `cn` 이 기본 `text-typo-heading-sm-400`(14px)을 덮는다). **확대를 막는 viewport 설정(`maximum-scale` · `user-scalable=no`)은 쓰지 않는다**(접근성 · D-27). 앱의 텍스트 입력은 이 두 칸뿐이다(언어 목록은 단추 · §7.2).

### 7.2 통역 화면 배치 (D-07 · D-08 · D-21 · D-22 · D-23 · D-31) — 시안 `Interpret-Flipped.dc.html` · `Interpret-Upright.dc.html` · `Captions.dc.html` · `Language-List.dc.html`

```text
┌────────────────────────────────────┐
│ [☰] Tongky                         │ ← 헤더 56px · bg-ms-white · 아래 선 border-ms-gray-200 (뒤집히지 않음)
├────────────────────────────────────┤   햄버거 44×44 · 워드마크 text-typo-title-md-600 text-primary
│ ╔══ 외국어 영역 (기본 180°) ═══════╗ │ ← main 안쪽 12/16/16 · 카드 안쪽 14/16 · 사이 12
│ ║ [English  ⌄]            [⟳▯]  ║ │    언어 고르기 h44 · 최소 156 / 회전 단추 44×44
│ ║  말풍선(외국어)                  ║ │    안내 줄 없음(원 위로 옮김 — D-22)
│ ╚════════════════════════════════╝ │
│      ● 고른 언어 안내 (180°)        │ ← 가운데 줄 140px 고정(D-23) — 원 위 안내 20px(외국어 영역과 같은 방향)
│ [자동 듣기 ]( 원 · 92 상자 )[초기화] │    원 기본 64 · 듣는 중 최대 88 · 「초기화」는 멈춤 · 누르고 말하기 안 누름에서만(D-29 · D-36)
│ [누르고 말하기]                      │    원 왼쪽 = 듣기 방식 전환(D-36 · §7.7)
│          한국어 안내               │    원 아래 안내 20px · 13px
│ ╔══ 한국어 영역 ═══════════════════╗ │
│ ║  말풍선(한국어)                  ║ │    안내 줄 없음 · 자막만
│ ╚════════════════════════════════╝ │
└────────────────────────────────────┘
```

- 외국어 영역 · 한국어 영역은 남는 높이를 반씩 나눈다(`flex: 1 1 0`). **가운데 줄은 140px 고정 · 원은 92 × 92 상자 가운데**(0.4.0 — D-23 · 시안 r3. 0.3.0 의 196 · 144 상자는 폐기). 줄인 높이는 두 자막 영역이 반씩 갖는다.
- **뒤집힘**: 외국어 영역 카드에 `transform: rotate(180deg)` — 언어 고르기(펼친 목록 포함 · D-31) · 회전 단추 · 자막이 모두 함께 뒤집힌다. **원 위 외국어 안내 줄도 같은 방향**(뒤집힘이면 180° · 바로 보기면 바로 · D-22). **회전 단추**를 누르면 뒤집힘 ↔ 바로 보기(옆에서 볼 때). 바뀌는 것은 **렌더 방향뿐** — WS · 자막 · 상태는 그대로(D-08 · 입력 4). 마지막 방향을 `localStorage` 에 기억(기본값 — 처음은 뒤집힘).
- **회전 단추**: 기기 사각형 + 원형 화살표 두 개(시안 인라인 SVG · 24 · stroke 1.8). ⇅ 는 쓰지 않는다. 뒤집힘(기본) = `bg-ms-white border-ms-gray-300 text-ms-gray-700` · **바로 보기 = `bg-primary-100 border-primary-500 text-primary`**(「기본이 아님」 표시 — `Interpret-Upright.dc.html`). `aria-label` 「화면 방향 바꾸기」 · `aria-pressed` = 바로 보기.
- 햄버거 = 세 줄 인라인 SVG(stroke 2) · 메뉴가 열려 있으면 단추 바탕 `bg-ms-gray-200`(`Menu.dc.html`). `aria-label` 「메뉴 열기」/「메뉴 닫기」.
- **언어 고르기 = 카드 안에 그리는 자체 목록 `LangSelect`(0.4.0 — D-31)**. medikit 1.4.0 `ComboBox` 는 펼친 목록을 Popover portal 로 `body` 에 붙이고 끄는 prop 이 없어 180° 카드와 같이 돌지 않는다(iPhone 실기기) → D-31 의 「그 영역 안 자체 목록」을 택했다. 모양은 medikit 값 그대로:
  - 단추 = medikit `Button` outlined black · h44 · 최소 156 · 둥글기 8 · 이름 `text-typo-heading-sm-500` · medikit `ChevronIcon`(열리면 위) · 열리면 `border-primary`
  - 목록 = `bg-ms-white rounded-[8px] shadow-pop-over`(PopoverContent 값) · 항목 = `min-h-[50px] p-[15px] text-typo-heading-sm-400 hover:bg-ms-gray-100`(CommandItem 값) · 고른 것 `bg-primary-100 text-primary text-typo-heading-sm-500` + medikit `CheckIcon` · 7개(§5.5 순서 · 목록 표시 이름)
  - 카드(`relative`) 안 `absolute` — 카드째 돌아 **뒤집힘이면 맞은편 사용자 기준 아래로**, 바로 보기면 바로 펼쳐진다. 높이는 카드 안 남은 높이까지 · 넘으면 목록 안 스크롤(화면 밖으로 안 잘림)
  - 키보드 · 접근성: `role=combobox` · `listbox` · `option` · `aria-activedescendant` · 단추 ↓ · Enter · Space 열기 · ↑ ↓ · Home · End · Enter 고르기 · Esc(단추로 포커스) · Tab 닫기 · 바깥 누름 닫힘
- 언어를 바꾸면 지금 WS 에 `stop` → 닫고 → 새 `start` 로 다시 연다(원형 front 와 같음) → 「연결 중」 → 「대기」(멈춤이었어도 다시 듣기 — 고르는 동작이 사용자 동작이라 오디오도 깨어 있다). 자막은 지운다(기본값 — 대화 상대가 바뀐 것으로 본다).

### 7.3 가운데 원 — 상태표 (D-09 · D-20 · D-21 · D-22 · D-23 · D-29 · D-34 · D-36) — 시안 `State-1-Start` ~ `State-8-Idle.dc.html`(r3)

front 는 아래 상태 중 하나다. 판정은 **위에서부터**(먼저 맞는 것). (0.2.0 — FAIL-2 · WARN-1 · WARN-4 · WARN-6 / 0.3.0 — 색 · 글리프 · 링 · 색 점 / 0.4.0 — 크기 D-23 · 안내 위치 D-22 · 초기화 D-29 / **0.5.0 — #4′ 누르고 말하세요 D-36**)

| # | 상태 | 언제(판정) | WS | 원(클래스 · 크기 · 글리프 · 링) | **원 위** 안내(고른 언어 · 앞 색 점 · D-22) | **원 아래** 안내(한국어) | 누르면 | 시안 |
|---|---|---|---|---|---|---|---|---|
| 1 | 시작 전 | 통역 화면에 막 들어옴(로그인 뒤 · 새로고침 · 토큰이 살아 있어 바로 들어옴) · **백그라운드에서 돌아옴**(§8 — WS 를 닫았음) | 없음(닫힘) | 아래(가려짐): `bg-ms-gray-300` 64 · 글리프 없음 | — (오버레이가 덮음) | **오버레이가 헤더까지 화면 전체를 덮는다** — **언어 단추 7개**(0.4.1 · D-34 · 아래) | **언어 단추 하나 누름** = 그 언어로 `AudioContext.resume()` · 마이크 권한 · 새 WS · `start{lang}` → 3. 단추 밖을 누르면 아무것도 안 함 | `State-1-Start`(D-34 판) |
| 2 | 오류 | `error` 수신 · WS 끊김 · 마이크 거부 | 닫힘 | `bg-red text-ms-white` **56** · 「!」 · 링 5px `rgba(255,78,81,.15)` · 92 상자 없이 64 줄 | 점 대신 **`bg-red-100` 박스**(둥글기 8) 안에 `ErrorIcon` 14 + 짧은 오류 `text-red`(예 en 「Connection error」) | 오류 문구(서버 `message` · 끊김 문구) + **[다시 연결]**(medikit `Button` solid · ss · round · 다시 아이콘) | [다시 연결] = 새 WS · `start` → 3(원 누름은 아무것도 안 함) | `State-2-Error` |
| 3 | 연결 중 | 새 WS ~ `ready` 전 | 여는 중 | `bg-ms-gray-300 text-ms-gray-700` 64 · 점 셋 6px · 링 없음 | 점 `bg-ms-gray-600` · 그 언어로(예 en 「Connecting…」) | 「연결 중…」 | 아무것도 안 함 | `State-3-Connecting` |
| 4 | **〈언어〉로 출력 중** | 출력 구간(§7.4 — 표시 시점은 실제 재생 기준 · WARN-4) — **멈춤 중이어도 이 상태**(`pause` 의 `finalize` 로 확정된 발화의 TTS · D-09) | 열림 | 외국어로 출력 = `bg-purple` · 한국어로 출력 = `bg-primary` · `text-ms-white` **64 고정** · 스피커 글리프 · **링 두 겹**(7px 18% + 15px 8% — 맥박) | 점 = 출력 언어 색(외국어 `bg-purple` · 한국어 `bg-primary`) · 그 언어로(예 en 「Speaking in English」 · 「Speaking in Korean」) | 「〈한국어 이름〉로 출력 중」 — 예 「영어로 출력 중」 · 「대만어로 출력 중」 · 「한국어로 출력 중」 | 멈춤 중이 아니면 `pause` — **지금 재생을 멈추고 큐를 비우고 남은 조각을 버린 뒤**(§7.4 FAIL-1) `pause` 전송 → 5. 멈춤 중이면 `resume` → 8 | `State-4a-Speaking-Foreign` · `State-4b-Speaking-Korean` |
| **4′** | **누르고 말하세요**(0.5.0 · D-36) | 듣기 방식 = 누르고 말하기(§7.7) · 원을 **누르고 있지 않음** · 출력 중 아님 | **열림**(`pause` 상태) | 시안 `PTT-Ready`: **64 `bg-ms-white` + 2px `border-ms-gray-500`** · 마이크 22(`text-ms-gray-700`) · 링 없음 — 「눌러야 듣는다」를 대기(회색으로 채운 원)와 구분 · 원 오른쪽 「초기화」 | 점 `bg-ms-gray-600` · 그 언어로(예 en 「Hold to speak」 · §7.7) | 「누르고 말하세요」 | **누르고 있는 동안** 듣기(§7.7) — 누름 = `resume` → 듣는 중(6 · 7 · 8 모양) · 뗌 = `pause` → 4′ | `PTT-Ready` |
| 5 | 멈춤 | `pause` 를 보낸 뒤 · 출력 중 아님 · 자동 듣기 모드 | **열림** | `bg-ms-gray-300 text-ms-gray-700` 64 · 「‖」 · 링 없음 · **원 오른쪽에 「초기화」**(아래) | 점 `bg-ms-gray-600` · 그 언어로(예 en 「Paused」) | 「멈춤 · 원을 눌러 다시 듣기」 | `resume` → 8(또는 6 · 7) | `State-5-Paused` |
| 6 | **한국어 듣는 중** | 열린(`final:false`) caption 의 `side=me` | 열림 | `bg-primary text-ms-white` · **음량에 따라 64 ~ 88** · 마이크 글리프 · 링 7px 18% | 점 `bg-primary` · 그 언어로 「상대(한국어)를 듣는 중」(예 en 「Listening to Korean…」) — **0.4.0: 0.3.0 의 「안내 줄 없음」을 D-22 「상태 8개 전부」가 이긴다** | 「한국어 듣는 중」 | `pause` → 5 | `State-6-Listening-Korean` |
| 7 | **외국어 듣는 중** | 열린 caption 의 `side=them` | 열림 | `bg-purple text-ms-white` · 음량에 따라 64 ~ 88 · 마이크 · 링 7px 18% | 점 `bg-purple` · 그 언어로(예 en 「Listening」) | 「〈한국어 이름〉 듣는 중」 | `pause` → 5 | `State-7-Listening-Foreign` · `Captions` |
| 8 | **대기** | `ready` 뒤 · 위 어느 것도 아님 | 열림 | `bg-ms-gray-400 text-ms-gray-700` **64** · 마이크 · 링 7px `rgba(214,214,214,.35)` · 음량 반응 작게(최대 1.1배 ≈ 70) | 점 `bg-purple`(외국인이 말할 차례도 됨) · 그 언어로(예 en 「Please speak」) | 「말씀하세요」 | `pause` → 5 | `State-8-Idle` |

- **원 크기(0.4.0 — D-23 · 시안 r3)**: 기본 **64** · 오류 **56** · 듣는 중 **64 ~ 88**(음량 반응 최대 1.375배 · 92 상자를 넘지 않는다) · 대기 64 ~ 약 70. 링은 비례로 줄였다(7 · 15 · 5px). 글리프 = 시안 인라인 SVG(마이크 19 ~ 22 · 스피커 24 · ‖ 22 · 「!」 24 · 점 셋 6px). 0.3.0 의 96 · 88 · 100 · 96 ~ 144 는 폐기.
- **원 위아래 안내(0.4.0 — D-22 · D-23)**: 원을 사이에 두고 **두 언어 안내가 마주 본다** — 원 위 = 고른 언어(외국어 영역과 같은 방향 · 180°) · 원 아래 = 한국어(늘 바로). 높이 20px 씩 · 글자 13px — medikit 에 13px typo 토큰이 없어 `text-typo-caption-md-500/600` + `!text-[13px]`(`!` 없이는 토큰 12px 가 이긴다 — 계산값 확인 · wp6-fe 보고). 원 위 = `text-ms-gray-700`(오류는 `text-red`) · 원 아래 = `text-ms-gray-800`. 앞 색 점 6px. **외국어 카드 안의 안내 줄은 없앴다**(두 번 보이지 않게 · D-22). 시작 전(#1)은 오버레이가 두 안내를 대신한다.
- **초기화(0.4.0 — D-29)**: **멈춤(#5) · 누르고 말하세요(#4′ · 0.5.0)에서만** 원 상자 오른쪽 12px · 세로 가운데에 「초기화」 단추(0.5.0 — 시안 r7 모양: 흰 바탕 · `border-ms-gray-300` · h33 · 둥글기 6 · `text-typo-body-500` · 되돌리기 아이콘 · 한국어만 · 가운데 줄은 안 뒤집힘 — 상담사 쪽). 출력 중(#4 — 멈춤 중 출력 포함) · 오류(#2)에서는 안 보인다. 누르면 **확인 창 없이** ① 재생 중 · 대기 중 TTS 를 버린다(재생 큐를 비우고 다음 `audio_start` 까지 오는 조각은 버림 — §7.4 FAIL-1 과 같은 길) ② 두 영역 말풍선을 모두 지운다 ③ **멈춤 · 고른 언어 · WS 는 그대로** — 원을 다시 누르면(`resume`) 빈 화면에서 새 대화. back 에 보내는 메시지는 없다(WS 계약 그대로). 0.4.x 의 medikit ss round 모양은 0.5.0 에서 시안 r7 모양으로 바꿨다(#5 · #4′ 같은 모양 · d36-fe 보고).
- **원 안 글리프 · 원 위 안내 앞 색 점 · 링**은 시안에서 더한 요소 — **채택**(D-21).
- **시작 전 오버레이 = 언어 고르기(0.4.1 — D-34)**: 「탭해서 통역 시작」 대신 **언어 단추 7개** — **누르는 것이 시작**이다(언어를 고르지 않고 시작하는 길이 없다).
  - 자리: 화면 루트 `absolute inset-0` · `bg-ms-overlay` — **헤더(햄버거)까지 덮는다**(0.3.0 WARN-3 그대로 — 시작 전에는 메뉴를 열 수 없다).
  - 방향: **상담사 방향(바로) 하나** — 고르는 사람이 상담사다(D-34 · 방향은 코디 기본값). 0.3.0 의 「위아래 반으로 나눈 두 언어 오버레이 · 위 절반 뒤집힘」은 **폐기**. 회전 단추 상태(뒤집힘 · 바로 보기)와 무관.
  - 단추: §5.5 순서 7개 · 이름 = **목록 표시 이름**(English · 日本語 · 中国 · 简体中文 · 臺灣 · 繁體中文 · ไทย · Tiếng Việt · 廣東話) · **크게**(터치하기 쉽게 — 크기 · 배치 · 안내 문구는 시안 `State-1-Start`(D-34 판)를 따른다 · 시안이 없으면 frontend 기본값).
  - **마지막 언어는 표시만**(예 고른 표시 · 테두리) — **자동 선택 · 자동 시작하지 않는다**(D-34). 마지막 언어 기억(`localStorage` · §5.5)은 그대로.
  - 누르면 = 사용자 동작 안에서 `AudioContext` 깨우기 · 마이크 · WS · `start{lang}`(§7.4 「깨우는 곳」 — 0.4.1: 오버레이의 언어 단추 · [다시 연결] · 언어 고르기). 고른 언어는 드롭다운 값 · `localStorage` 와 같아진다.
  - **시작 뒤 언어 바꿈은 지금 드롭다운**(§7.2 `LangSelect`) — 그대로.
  - 백그라운드 복귀(§8)도 이 오버레이로 — 다시 언어를 누른다(마지막 언어 표시).
- **#4′ 와 #5 는 모드로 가른다**: 누르고 말하기 모드에서 손을 뗀 상태는 늘 #4′(WS 는 `pause` 지만 「멈춤」 문구가 아니라 「누르고 말하세요」) · #5 는 자동 듣기 모드에서 원을 눌러 멈춘 것. 출력 중(#4)은 둘보다 위.
- **멈춤(5)과 시작 전(1)은 다른 상태다**: 5 는 WS 가 열린 채 마이크만 멈춘 것(누르면 `resume`), 1 은 WS 가 없는 것(오버레이 언어 단추로 새로 연다 · D-34). 백그라운드 복귀는 1 이다.
- 멈춤 여부는 상태와 따로 들고 있다(판정 입력). 흔한 경로: 말하는 중(6 · 7)에 원을 누름 → `pause` → 5 → back 이 `finalize` 로 그 발화를 확정해 번역 TTS 를 보냄 → `audio_start` → **4(멈춤 중이어도 출력 중 안내 · D-09)** → 재생 끝 + 400 ms → 5. 원형 front 는 `pause` 때 그때까지의 재생만 멈추고(`stopPlayback`), 그 뒤에 온 `audio_start` 는 재생한다(`_archive/cc/front/lib/interpret.ts`).
- 원 단추 `aria-label` 「멈춤」(4 · 6 · 7 · 8) · 「다시 듣기」(5) · 누르고 말하기 모드는 「누르고 있는 동안 말하기」(§7.7).
- **음량 반응**: 마이크 입력을 Web Audio `AnalyserNode` 로 재서(RMS) 원 크기를 매끄럽게 바꾼다(D-09) — 듣는 중 64 ~ 88 · 대기는 64 에서 작게(최대 1.1배 · 기본값). 출력 중에는 마이크를 안 보내므로 음량 반응을 끈다(64 고정 · 링 두 겹 맥박만).
- 외국어 안내 문구는 7개 언어 × {시작 전 · 오류 · 연결 중 · 출력 중(외국어 · 한국어) · 멈춤 · 외국어 듣는 중 · **한국어 듣는 중** · 대기 · **「↓ 최신」 라벨**(§7.5) · **누르고 말하세요**(0.5.0 · §7.7)} 고정 표를 front 상수(`lib/langs.ts` `FOREIGN_PHRASES`)로 둔다. 값은 frontend 가 정했다 — 원어민 검수 없음(§10 OQ-006 · PoC 범위). en 값은 시안 문구와 같다. zh-Hant 는 번체(대만식 「韓語」) · yue 는 번체(「韓文」) · 둘 다 출력 언어 이름은 「中文」(TTS 가 만다린).
- **원을 누르면 멈춤 ↔ 다시 듣기**(`pause`/`resume` — 자동 듣기 모드 · WS 가 열린 4 ~ 8 에서만) · **시작은 오버레이의 언어 단추**(1 · D-34) — 원 누름과 나눴다. 누르고 말하기 모드의 원은 §7.7.

### 7.4 오디오 — 원형 `lib/interpret.ts` 그대로

- 시작: 통역 화면에 들어오면 「시작 전」 오버레이(§7.3 #1)를 띄운다. **오버레이의 언어 단추 누름 안에서(0.4.1 · D-34)** `AudioContext` 를 만들고 `resume()` → 마이크 권한 → WS → `start` → `ready` 뒤에만 PCM 송신(§4.6.1 — `ready` 전 송신 없음). 자동 시작하지 않는다(0.2.0 — WARN-6 · 기본값 · §10 OQ-005).
- 마이크: `getUserMedia({audio: {echoCancellation: true, noiseSuppression: true}})` → `AudioWorklet` 에서 16 kHz 로 리샘플 → Int16 640샘플 조각 송신(원형 `Pcm16kWriter`).
- 재생: `audio_start.sampleRate` 로 `AudioBuffer` 를 만들어 끊김 없이 이어 붙여 재생(원형).
- **반이중**(D-03 · 개념 half-duplex-echo-suppression): `audio_start` 를 받은 순간부터 마이크 PCM 을 보내지 않는다(트랙은 열어 둔다) · 마지막 재생 조각 `onended` + **400 ms** 뒤 재개 · 그 사이 새 `audio_start` 가 오면 재개 취소 · 멈춤 · 닫기 · 오류 · 언어 바꿈은 재생 큐를 비운다. 이 구간이 §7.3 「출력 중」이다.
- **멈춘 뒤 남은 조각은 버린다(0.3.0 — 리뷰 FAIL-1)**: back 은 `pause` 와 상관없이 그 발화의 남은 음성 조각과 `audio_end` 를 끝까지 보낸다(원형 `_tts_worker`). 그래서 front 는 재생 큐를 비울 때(멈춤 · 원 누름으로 `pause` · 닫기 · 오류 · 언어 바꿈 · **초기화**(0.4.0 · D-29 — `clearPlayback()`)) **「버림」 표시를 세우고, 다음 `audio_start` 를 받을 때까지 오는 바이너리 조각을 재생하지 않고 버린다**. `audio_end` 는 받아서 무시. 다음 `audio_start` 가 오면 표시를 풀고 평소대로(그 발화는 재생 · 반이중 막음 시작). 버리는 동안 반이중 게이트(`speaking`)는 **열지 않은 상태 그대로** — 버린 조각이 송신 재개 타이머를 건드리지 않는다. back 은 바꾸지 않는다(원형 유지).
- **출력 언어 표시 시점(0.3.0 — 리뷰 WARN-4)**: 「〈언어〉로 출력 중」의 언어 · 원 색 · 원 위 안내 점 색(0.4.0 — D-22)은 **그 발화의 첫 조각이 실제로 재생되기 시작하는 시각**(재생 스케줄 시각 — 이어 붙이는 재생의 `nextTime`)에 바꾼다. `audio_start` 를 받은 시각이 아니다 — 앞 발화가 아직 재생 중이면 앞 발화 재생이 끝나 다음 발화가 시작될 때 바뀐다. **마이크 막음(반이중)은 그대로 `audio_start` 를 받은 순간부터**(표시만 재생 기준으로 옮긴다).
- **누르고 말하기(0.5.0 · D-36)**: 반이중은 그대로 — 누르고 있는 중에 TTS 가 오면(`audio_start`) 송신이 막힌다. **TTS 재생 중에 원을 누르면 재생을 멈추고 큐를 비운 뒤**(`clearPlayback` · 버림 표시 — 위 FAIL-1 과 같은 길) `resume`. 반이중 게이트 기준 「출력 중」(`outputting`)은 표시보다 먼저 참이다(`audio_start` 받은 순간부터).
- iOS Safari: `AudioContext` 는 사용자 동작 안에서 `resume()` 해야 한다 — 깨우는 곳은 **오버레이 언어 단추(D-34) · [다시 연결] · 언어 고르기** 셋(모두 사용자 동작). 로그인 단추에 기대지 않는다(새로고침 · 토큰이 살아 있으면 로그인을 건너뛰므로). `AudioContext.state` 가 `suspended` 로 돌아가 있으면 다음 사용자 동작에서 다시 `resume()`(0.2.0 — WARN-6 · 실기기 확인 §9.5).

### 7.5 자막 — 말풍선 · 자동 스크롤 (D-16 · D-21 · D-24 · D-25) — 시안 `Captions.dc.html`(r3)

**어느 영역에 무엇을(D-16 — 그대로)**

| caption | 외국어 영역 | 한국어 영역 |
|---|---|---|
| `side=them`(외국인이 말함) | `original`(외국어 원문) | `translation`(한국어 번역) |
| `side=me`(한국어로 말함) | `translation`(외국어 번역) | `original`(한국어 원문) |

- 각 영역에는 **자기 언어 문장만**(D-16). 같은 `id` 는 같은 말풍선을 갈아 끼운다. 빈 문자열(번역이 아직 없음)은 그 영역에 말풍선을 만들지 않는다.

**말풍선(0.4.0 — D-24)** — 메신저처럼, **그 영역을 보는 사람 기준 내 말 = 오른쪽 · 상대 말 = 왼쪽**.

| 영역 | 오른쪽(내 말) | 왼쪽(상대 말) |
|---|---|---|
| 한국어 영역(상담사가 봄) | `side=me` 의 원문 · `bg-primary-100` | `side=them` 의 한국어 번역 · `bg-ms-gray-200` |
| 외국어 영역(뒤집힘 — 환자가 봄) | `side=them` 의 원문 · `bg-purple-100` | `side=me` 의 외국어 번역 · `bg-ms-gray-200` |

- 영역은 바로 선 기준으로 짜고 뒤집힘은 회전만 한다 — 외국어 영역의 「오른쪽」은 뒤집혀 있으므로 **환자 눈에 오른쪽**이다(D-24). 판정은 순수 함수 `isMine(side, area)`(`lib/view.ts`).
- 모양: 최대 폭 80% · 안쪽 8/12 · 사이 8 · 둥글기 16(말한 쪽 아래 모서리만 4) · 글자 **`text-typo-heading-md-500`(16px — 0.3.0 의 `text-typo-title-sm-500` 대신 · 코디 결정 · 시안 r3)** · `word-break: keep-all`.
- `final:false` = 말풍선 안 **`text-ms-gray-600`**(흐린 글자 · D-21 · D-24) · `final:true` = `text-ms-gray-800`.
- 색 = 내 말은 그 쪽 언어색 옅게 · 상대 말은 회색(D-24 · 값은 코디 기본값 — 시안 r3 와 같음).

**자동 스크롤(0.4.0 — D-25)**

| 항목 | 계약 |
|---|---|
| 따라가기 | 영역의 스크롤이 **맨 아래에서 40px 안**이면 「따라가는 중」 — 새 말풍선 · 같은 말풍선 갱신 때 맨 아래로 |
| 사용자가 위로 올림 | 40px 밖으로 올리면 따라가기를 멈춘다 — **끌어내리지 않는다**(지난 대화를 볼 수 있게) |
| 「↓ 최신」 | 따라가기를 멈춘 뒤 **새 말풍선이 생기면** 그 영역 아래 가운데에 작은 단추(medikit `Button` ss round · `text-typo-caption-md-600` · `shadow-pop-over`). 누르면 맨 아래로 · 따라가기 다시. 사용자가 손으로 맨 아래(40px 안)로 돌아와도 다시 따라가고 단추는 사라진다 |
| 영역별 | 두 영역이 **따로** 판단한다(한쪽을 올려 둬도 다른 쪽은 계속 따라감) |
| 뒤집힘 | 외국어 영역은 카드째 180° 라 「아래」 = **뒤집힌 자기 기준 아래**(화면상 위쪽 끝) · 단추도 자기 기준 아래 |
| 라벨 | 한국어 영역 「최신」 · 외국어 영역 = 고른 언어 문구(`FOREIGN_PHRASES[lang].latest` — en 「Latest」 등 · §7.3 끝) · 앞에 ↓ |
| 판정 함수 | `isNearBottom(40px)` · `hasNewBelow` — `lib/scroll.ts` 순수 함수(시험 §9.2) |

- 영역별 최대 말풍선 수는 두지 않는다 — 화면을 떠나면(로그아웃 · 새로고침) 지운다(Scope Out 기록 저장). 「초기화」(§7.3 · D-29)로도 지운다.

### 7.6 햄버거 메뉴 — 로그아웃만 (D-07 · D-21 · D-37) — 시안 `Menu.dc.html`(r8)

- 햄버거(헤더 왼쪽 · 인라인 SVG) → medikit **`Popover`**(`PopoverTrigger` · `PopoverContent`) — 헤더 아래 왼쪽(시안: 위 58 · 왼쪽 8) · 폭 196 · 둥글기 10 · 안쪽 6 · 그림자 `shadow-pop-over-more`. 안에 항목 **하나 — 로그아웃**(h44 · 둥글기 6 · 아이콘 + `text-typo-heading-sm-500` · **`text-red`** — 시안에서 더한 요소 · 채택). medikit `Menu` 는 경로 기반 옆 메뉴라 쓰지 않는다(0.2.0 — WARN-3).
- 로그아웃 = §3.3 순서.
- **용어집 항목 · 구분선 · 용어집 모달(`GlossaryModal` · `BaseModal` · `Table` · 별칭 줄 · 「검수 전」 꼬리표 · `medikit-patches.css` `[BaseModal-1]`)은 지웠다**(0.5.0 · D-37 — D-13 뒤집음 · 시안 r8 에서 `Glossary` 화면 삭제). front 는 `/api/glossary` 를 부르지 않고 용어집 타입 · 아이콘(`BookIcon`)도 없다.
- 메뉴는 뒤집히지 않는다(사용자 쪽 조작).

### 7.7 듣기 방식 — 자동 듣기 / 누르고 말하기 (0.5.0 — D-36) — 시안 `Mode-Auto-Idle` · `PTT-Ready` · `PTT-Pressed`(r7)

> 주변 소리(노래 등)가 계속 입력되는 자리에서 쓰려고 — 원을 누르고 있는 동안만 마이크를 보낸다. **back 무변경 · WS 메시지 그대로**(누름 = `resume` · 뗌 = `pause` → back `finalize`).

| 항목 | 계약 |
|---|---|
| 전환 | 원 **왼쪽** 세로 세그먼트 「자동 듣기 / 누르고 말하기」(`ModeToggle`) — 트랙 `bg-ms-gray-200` · 폭 104 · 둥글기 8 · 안쪽 2 · **칸 높이 44**(누르는 영역 · 코디 처분 — 시안 r7 처음 28 → 44) · 고른 칸 `bg-ms-white text-ms-gray-800 text-typo-caption-md-600` + 그림자 `0 1px 3px rgba(0,0,0,.08)` · 안 고른 칸 투명 `text-ms-gray-700 text-typo-caption-md-500` · `role=radiogroup` · `radio`. 한국어만 · 가운데 줄이라 회전 없음. 「초기화」(원 오른쪽)와 겹치지 않는다 |
| 기억 | `localStorage` 키 `interpret.mode` = `auto` · `ptt` · **처음은 `auto`**(지금과 같음) |
| 자동 듣기 | 지금 그대로(§7.3 · 원 누름 = 멈춤 ↔ 다시 듣기) — 시안 `Mode-Auto-Idle` |
| 누르고 말하기 — 시작 | `ready` 뒤 바로 `pause` → #4′(§7.3) |
| 모드 바꿈 | 자동 → 누르고 말하기 = `pause`(멈춤이 아니었으면) · 누르고 말하기 → 자동 = `resume`(멈춤이었으면). WS 는 그대로 |
| 누름 | 원을 **누르고 있는 동안** — `pointerdown`(+ pointer capture) = 시작 · `pointerup` · `pointercancel` · `lostpointercapture` · `pointerleave` = 끝 · 키보드 Space · Enter 누름/뗌 · `contextmenu` 막음 · iOS 길게 누름 대비 `touch-none select-none [-webkit-touch-callout:none] [-webkit-user-select:none]`. 원이 가운데라 **상담사 · 손님 누구나 누른다**(화자는 자동 감지 그대로 — `side`) |
| 누름 동작 | 재생 구간(`outputting`)이면 `clearPlayback()`(재생 멈춤 · 큐 비움 · 버림 표시 — §7.4) → `resume`. 누르는 동안은 듣는 중 그대로(음량 반응 64 → 88 · 화자 색 · 캡션 오기 전은 대기 모양) — 시안 `PTT-Pressed` |
| 뗌 동작 | `pause` → back 이 말하던 발화를 `finalize` → 번역 · TTS(출력 중 #4) → 끝나면 #4′ |
| 원 위 안내(고른 언어) | 안 누름 = 「Hold to speak」 류 7개 — en Hold to speak · ja 押しながら話してください · zh 按住说话 · zh-Hant 按住說話 · th กดค้างไว้แล้วพูด · vi Nhấn giữ để nói · yue 㩒住講嘢(design-r7 제안 · 원어민 검수 없음 — OQ-006). 누름 = 듣는 중 문구 그대로 |
| 원 아래 안내(한국어) | 안 누름 「누르고 말하세요」 · 누름 = 듣는 중 문구 |
| 그대로인 것 | 초기화(#4′ 에서도 보임) · 자동 스크롤 · 「↓ 최신」 · 반이중 · 언어 바꿈 · 백그라운드 → 시작 전 |
| 판정 함수 | `lib/view.ts` `CircleInput.ptt` · `holding` → `holdToTalk` · `canReset` · `lib/ptt.ts` `pressDown(session, outputting)` · `pressUp(session)` — 순수 함수(시험 §9.2) |

### 7.8 medikit (D-10 · D-20)

- medikit 은 원형 `procedure/front` 방식으로 붙인다: `tailwind.config.ts` 에 `medikitPreset` + `content` 에 `node_modules/@medisolve-ai/medikit/dist/**/*.js` · `app/layout.tsx` 에서 `pretendard` · `@medisolve-ai/medikit/styles` · `./styles/ceramique-theme.css`(§6) · `./styles/medikit-patches.css` import. 원형 `medikit-patches.css` 의 보정은 **필요한 것만**.
- 쓴 클래스(시안에서 옮긴 것 · 0.4.0 의 `bg-purple-100` · `text-typo-heading-md-400` · `text-typo-heading-md-500` · `shadow-pop-over` · 0.5.0 의 `border-ms-gray-500` · 세그먼트 클래스 포함)는 빌드 산출 CSS 와 전수 대조한다(§9.2). 0.5.0 — 용어집 창 클래스 · `[BaseModal-1]` 보정은 지웠다.

## 8. PWA — D-02 · D-12

| 항목 | 계약 |
|---|---|
| manifest | `app/manifest.ts`(Next.js 메타데이터 라우트) — **`name` 「통키」 · `short_name` 「Tongky」**(0.3.0 — D-21) · 문서 제목(`metadata.title` · `apple-mobile-web-app-title`) 「통키」 · `display: "standalone"` · `orientation: "portrait"` · `start_url: "/"` · `theme_color` · `background_color`(흰색) · 아이콘 192 · 512(+ maskable) · `apple-touch-icon` 180 |
| 홈 화면 추가 | Android Chrome = 설치 안내(브라우저 기본) · iOS Safari = 공유 → 홈 화면에 추가. 앱 안에 따로 설치 단추는 두지 않는다(기본값) |
| 서비스 워커 | 앱 껍데기(정적 파일)만 캐시 — `/api/*` · WS 는 캐시하지 않는다. 오프라인이면 「인터넷 연결이 필요해요」 화면(기본값). 라이브러리는 frontend 가 고른다(Next.js 16 호환) |
| HTTPS | 마이크(`getUserMedia`) · 서비스 워커는 **보안 출처**에서만 된다. 로컬은 `http://localhost:3800`(보안 출처로 취급) · 같은 맥의 브라우저로 확인한다. **휴대폰에서 맥 IP 로 `http://` 접속하면 마이크가 안 된다** → 기기 확인은 배포(HTTPS) 뒤(§9.5) |
| 화면 꺼짐 방지 | 통역 화면에서 `navigator.wakeLock.request("screen")`. 탭이 다시 보이면(`visibilitychange`) 다시 요청. 지원하지 않으면 조용히 넘어간다(기능 감지) — 기본값 |
| 끊김 · 재연결 | **자동 재연결 없음**. WS 가 끊기거나 `error` 면 「오류」 상태 + [다시 연결](§7.3) — 누르면 새 WS · 새 `start`. 앱이 백그라운드로 가면(`visibilitychange` hidden) `stop` 보내고 닫는다 → 돌아오면 **「시작 전」(§7.3 #1) 오버레이** — 언어 단추를 누르면 새 WS · 새 `start`(0.4.1 · D-34)(0.2.0 — WARN-1 · 기본값 — 원형 SPEC-004 §4.3 「백그라운드면 닫는다」 · 개념 websocket-relay 「끊김을 그대로 드러낸다」) |

## 9. 검증 — 완료 조건 — D-03 · D-05 · D-12 · D-33 · D-35 ~ D-66

### 9.1 back 시험 (pytest · Soniox 가짜 · 시드는 가짜 + 실제 파일)

| 묶음 | 시험 |
|---|---|
| 로그인 | 맞는 아이디 · 비밀번호 → 200 `{token, expiresAt}` · 틀림(아이디만 · 비번만 · 둘 다) 같은 401 · 필드 빠짐 400 · 5회 실패 → 429 · 1분 뒤 풀림 · env 비면 401 · 만료 토큰 401 · env 아이디 바꾸면 기존 토큰 401 · `/api/auth/me` · 망가진 토큰(ASCII 아님 · 점 개수 · base64 · JSON) → HTTP 401 · WS 1008(500 0) · 로그인 env 빈 채 기동 → 경고 로그 1줄(이름만 · 값 0) · 응답은 같은 401 |
| 데모 로그인(0.4.0 · D-30) | 꺼짐: `config` `{demoLogin:false}`(토큰 없이 200) · `demo` 404 `not_found` / 켜짐: `config` true · `demo` 200 `{token, expiresAt}` · 그 토큰으로 `/api/auth/me` = env 아이디 · 응답에 비밀번호 0 / 잠긴 상태에서도 demo 200 · demo 뒤에도 잠금 그대로 / 켜짐 + 로그인 env 빈 것 → demo 401 / env 파싱 `true` · `1` 켬 · `false` · 빈 값 끔 |
| **시드(0.4.0 · D-33 · 0.5.0 D-35)** | **① 레포의 실제 `back/seed/glossary.json` 을 로더와 같은 검사 함수로 읽어 통과**(이 시험이 깨진 시드의 머지를 막는다 — §4.4) ② 가짜 시드로 §4.2 검사 하나씩 어김 → `SeedError`(파일 없음 · JSON 아님 · `schema` 다름 · `version` 모양 · `langs` 집합 다름 · 필수 필드 빠짐 · 타입 · `id` 모양 · `id` 중복 · `ko` · `ko_aliases` 겹침 · entry 키가 `langs` 밖 · `name` 빔 · `name` · `aliases` 괄호 · `source` 값 · `reviewed` bool 아님 · entry 안 겹침 · 앞뒤 공백 · 줄바꿈) · 오류 문구에 경로 · `id` ③ 시드가 깨지면 앱 lifespan 기동이 실패한다(빈 용어집으로 뜨지 않음) ④ 다른 시술의 같은 현지명은 통과 ⑤ `grep` 대신 시험: back 런타임 모듈에 matrix 주소 · `GLOSSARY_MATRIX_URL` 없음(§4.9) ⑥ **(0.6.0 · §4.2.1 ~ §4.2.3) 레포 시드 내용** — `version` `2026-10-27.6` · **§4.2.2 표 그대로**(`kr-001` ~ `kr-013` 이 배열 맨 뒤 이 순서 · `ko` · `category` · 언어 7개 × `name` · `aliases`(순서까지) · `reviewed` · `source` `web-research 2026-10-27` · `note` 가 URL 또는 `현지 출처 없음 — ` 로 시작) · **§4.2.3 표 그대로**(A · B · C 의 name · aliases · `reviewed` · `source` — C 는 `manual`) · **모호어 목록(§4.2.1) 금지 자리마다 0**(zh · zh-Hant · yue `t2s` 뒤 · 라틴 `casefold` 뒤) · 보이지 않는 글자 0(검사 7 — 가짜 시드로 U+200C 하나 → `invisible_char`) · 기존 157 term 의 `id` 순서 그대로 · 0.5.0 항목 중 유지: 울쎄라 zh-Hant 美國音波 · 써마지FLX zh-Hant 鳳凰電波 · 볼뉴머 기기 리프팅 · zh-Hant 「鐳射」 0 / **0.5.0 의 「zh 「热玛吉」 있음」 · 「`web-research` 77 · `reviewed:true` 38」 고정값은 지운다**(`.5` · `.6` 에서 바뀜 — 개수 대신 표 대조) / `source` 검사: `web-research`(날짜 없음) · 날짜 모양 틀림은 오류 · `web-research 2026-10-27` 통과 ⑦ **(0.6.1 · §4.2.3 D) OQ-018 처분 표 그대로**(ph-123 · ph-126 zh · ph-121 yue · ph-113 zh · th) · **ph-130 `ko_aliases == []` · 어느 term 에도 ko 별칭 「써마지」 0** ⑧ **(0.9.0 · §4.2 검사 8 · §4.2.5 · D-58) 틀린 꼴** — 가짜 시드로 `wrong_form` 하나씩: 빈 문자열 · 앞뒤 공백 · 줄바꿈 · 보이지 않는 글자 · 한 글자 · 목록 안 겹침 · 자기 `name` / `aliases`(`ko_wrong` 은 `ko` / `ko_aliases`)와 같음 · **다른 term 의 그 언어 `name` / `aliases`(ko 쪽은 `ko` / `ko_aliases`)와 같음**(대소문자 · 공백 · zh-Hant 번체/간체만 다른 것도 같음으로) → `SeedError` / 통과: 괄호가 든 꼴 · 다른 term 끼리 같은 틀린 꼴 · 두 필드가 없는 시드(`.7` 모양) / 문자열 배열이 아니면 타입 오류 / **레포 시드 `.8`**: `version` `2026-11-15.8` · **`ko_wrong` · `wrong` 을 뺀 나머지가 `.7` 과 같다**(term 170 · `id` 순서 · `ko` · `ko_aliases` · 언어 7개 × `name` · `aliases` · `source` · `reviewed`) · 틀린 꼴이 든 칸 = §4.2.5 표의 term · 언어뿐(그 밖 칸 0) |
| context | (0.4.0 · §4.5 · §4.6) 순서 = 정방향 기본 → 정방향 별칭 → 역방향 기본 → 역방향 별칭 · `terms` = 대표명 뒤 ko 별칭 · `entries[L]` 없는 시술은 빠짐 · `yue` · `zh-Hant` 는 `t2s`(정방향 target · 역방향 source 둘 다) · zh 는 그대로 · zh-Hant 는 zh-Hant entry 를 씀(zh entry 아님) · 역방향 source 중복은 처음 짝(기본이 별칭보다 앞) · 줄이기 순서 `terms`(별칭부터) → 역방향 별칭 → 역방향 기본 → 정방향 별칭 · **정방향 기본 · `general` 은 줄지 않음** · `forward_only` = `general` + 정방향 기본만 · `is_forward_only` · 그 언어 entry 0 이면 `context` 키 없음 · 경계를 거울 추측 없이 구조로 들고 다님(별칭 짝이 있어도 `forward_only` 가 정확) · **(0.6.1) 언어별 기준** — `CONTEXT_MAX_CHARS` 값이 §4.6 표와 같음 · 키가 7개 언어 · env 없으면 언어마다 표 값으로 조립 · env `15000` 이면 7개 언어 모두 15000(레포 시드로 `build_context` 결과와 같은지) · §4.6.1 가짜 Soniox 6건(0.3.0 그대로 — 설정 직후 `invalid_request` → 정방향 기본만 2번째 STT 연결 뒤 `ready` · 두 번 거절 → `soniox_unavailable` · TTS 안 열림 · 다른 `error_type` → 재연결 없음 · 2초 무응답 → `ready` · `ready` 뒤 `invalid_request` → 재연결 없음 · 처음부터 정방향 기본만이면 재연결 없음) · 로그 칸 수(용어 문자열 0) · **(0.9.0 · D-56) `CONTEXT_MAX_CHARS` = §4.6 「D-56 표」 값**(en 24,892 · ja 21,962 · zh 22,551 · zh-Hant 22,685 · th 23,215 · vi 24,349 · yue 22,825) · 레포 시드로 7개 언어 조립 → **묶음별 뺀 수 0** · 전체 글자 수 = 그 표의 「줄이기 없는 전체」 · **틀린 꼴 필드는 조립에 안 들어감**(`ko_wrong` · `wrong` 을 채운 가짜 시드와 비운 시드의 `to_soniox` 결과가 같다) |
| ~~메뉴(0.4.0 · §4.7)~~ | 0.5.0 — 메뉴 API 삭제로 시험도 지움(D-37). 대신 아래 「밖으로 내는 것」 |
| **밖으로 내는 것(0.5.0 · §3.5 · D-37)** | `tests/test_api_surface.py` — **앱 경로가 정확히 6개**(그 밖 Route 가 있으면 실패) · `/docs` · `/redoc` · `/openapi.json` · `/docs/oauth2-redirect` · `/api/glossary` → 404 일반 문구 · 응답 최소 모양(health `{ok:true}` · me `{ok:true}` · config `{demoLogin}`) · **허용 경로 전부(성공 · 401 · 404)의 응답에 시드 판 · 시드 낱말 0** · `app/api` · `app/schemas` 소스에 `glossary` · `.terms` · `.entries` · `menu_rows` · `load_seed` · `build_context` 0 — **(0.9.2 · 처분 §12 · WP26) 예외 한 줄**: `app/api/interpret.py` 가 세션을 만들 때 넘기는 `glossary=c.glossary`(바로잡기가 메모리의 사전을 읽는다 — §5.12 「시드」). 시험은 그 문자열이 그 파일에 **정확히 1번** 나오는지 보고, 그 한 줄을 지운 나머지 소스에서 위 낱말이 0 인지 본다 · 다른 파일에는 예외가 없다 · 사전을 응답 · WS 메시지로 내는 것은 여전히 0(§3.5 그대로) · 오류 일반 문구(검증 400 · 405 · 데모 꺼짐 404 · 처리기 밖 예외 500 — 예외 내용이 응답에 없고 로그에 종류) · WS 문구 4개에 `SONIOX` · `Soniox` · `.env` · `API_KEY` · `start` · `type` · `JSON` 0 · 받은 `lang` 을 되돌려 보내지 않음 |
| 가져오기 스크립트(0.4.0 · §4.8) | 저장한 matrix 가짜(`--from-file`)로: 괄호 분해 다섯 모양(없음 · 라틴(현지) · 현지(라틴) · 같음 · 그 밖 → `reviewed:false` · 괄호 뺀 이름 · `raw`) · 반각 · 전각 · 앞 공백 · 줄바꿈 정리 · 같은 `ko` 행 합치기(뒤 행 다른 표기 → 처음 term `aliases`) · zh-Hant = 분해 뒤 zh 의 `to_display("zh-Hant")`(0.5.0 — 「离子导入 → 離子導入」 · 「激光导入 → 雷射導入」 · 「特色项目 → 特色項目」) · `draft-s2twp` · `reviewed:false` · 빈 칸이면 entry 없음 · `id` = `ph-001` 순서 · 머리 `imported_from` · 출력이 §4.2 검사 통과 · **출력 파일이 이미 있으면 쓰지 않고 0 아닌 코드** · 같은 입력 두 번 → 같은 바이트(결정적) |
| 통역 | 원형 `test_interpret.py` 복사분(묶기 · 갱신 · 번체 자막 · TTS 간체 · flush · bad start · 전체 흐름 · 닫기 정리 · 오류 코드 · Origin · 토큰) + `lang` **7개** 매핑(§5.5) · `yue` · `zh-Hant` 는 Soniox 에 `zh` · **자막 변환 yue `s2tw`(「激光治療」) · zh-Hant `s2tw` + 표(「雷射治療」 · 「離子導入」 · 0.5.0 D-35) · `to_display` 「激光 软件 导入 项目 → 雷射 軟件 導入 項目」 · zh 간체 · 셋 다 TTS 입력은 간체**(§5.6) · `traditional` 이 와도 무시 · STT 설정에 `context` 가 들어감 · §5.7 괄호 제거 목록 — TTS 입력만 괄호 없음 · caption 은 괄호 그대로 · **(0.5.0 · §5.8) TTS keepalive 가 `{"keep_alive": true}` · 스트림 밖 검증 오류(`stream_id: ""`)가 와도 그 발화 오디오가 끝까지 나옴 + 경고 로그 · 자기 스트림 오류는 `SonioxError(channel="tts")` · 중계 중 오류 로그에 channel · message · lang · paused · stt_last · tts_last(len · lang) — 번역문 · 키 0** |
| **기록(0.6.0 · §5.9 · D-41 · 0.7.0 ⑦ · ⑨ — D-42)** | `tests/test_records.py` — 가짜 Soniox · `tmp_path` 폴더 · 시계 주입: ① 세션 1회(`start` → final caption 2 · non-final 1 → `stop`) → 오늘 파일 1개 · 줄 = `session_start` · `utterance` 2 · `session_end`(`reason=stop` · `utterances=2`) · 키 순서 · 여기 없는 키 0 · `at` `+09:00` · `seed` = 시드 판 ② 파일 날짜 = UTC+9 날짜(UTC 15:00 = 다음 날 파일) ③ `final:false` 안 씀 · 같은 `id` 두 번 → 1줄 · 둘 다 빈 caption 안 씀 ④ `bad_request`(lang 밖 · 첫 프레임 아님) → 줄 0 · `no_api_key` → start + end(`error` · `no_api_key`) · Soniox 거절 → end `soniox_unavailable` · 브라우저 닫힘 → `close` ⑤ **판정**: ko 대표명 · ko 별칭(0.6.1 — 레포 시드에 ko 별칭이 0개라 가짜 시드로) · L name · L alias 각각 걸림 · 「써마지 하실래요」 → `[]`(0.6.1 — 「써마지」 단독은 아무 term 도 아님) · zh-Hant 번체 자막 ↔ 시드(`t2s`) · 라틴 경계(「contact」 → `ACT` 아님 · 「ACT 시술」 → 걸림) · 공백 무시(「써마지 FLX」 → ph-130) · **더 긴 일치**(「써마지 CPT」 → `kr-001` 만 · 「벨로테로 리바이브」 → `kr-009` 만 · 짧은 이름이 ko 별칭인 경우는 가짜 시드) · `entries[L]` 없는 term 은 ko 로만 · 순서 = 시드 순서 · 없으면 `[]` ⑥ **넣지 않는 것**: 가짜 토큰 · 로그인 아이디 · 주입한 IP · Origin 문자열 · PCM 바이트가 파일에 0 ⑦ 폴더 비면 파일 0 · 삭제 작업 없음 · 로그 `off`(0.7.0 — `INTERPRET_RECORD_KEEP_DAYS=7` 을 줘도 같다) / 쓸 수 없는 폴더 → 기동 성공 · 경고 1줄 · 기록 끔 ⑧ **쓰기 실패**(쓰기 함수가 `OSError`) → 그 세션 caption · 오디오 · `ready` 가 기록 없을 때와 같음 · `error` 프레임 0 · 경고 로그 세션당 1줄 ⑨ **보관 기간(0.7.0 · D-42)**: **(a) 비었음 · 없음 · 공백만(`"   "`)** → 경고 0 · 오래된 날짜 파일(오늘 − 8 일 등)이 기동 뒤에도 그대로(삭제 0) · 24시간 배경 작업이 만들어지지 않음 · 로그 `keep_days=off` · `sweep: deleted=` 줄 0 **(b) N=7**(` 7 ` · `07` 도 7) → 0.6.0 ⑨ 그대로: 오늘 − 7 · − 8 일 파일 지움 · − 6 일 · 오늘 남김 · 이름이 다른 파일(`note.txt` · `2026-10-01.jsonl.bak`) 남김 · 기동 때 1회 · 24시간 뒤 다시(시계 · 잠 주입) · 지우기 실패 파일 하나 → 나머지 계속 · 로그 `keep_days=7` **(c) 잘못된 값**(`0` · `-1` · `abc` · `+7` · `7.0` · `36501` · `1000000` · 4,300 자리 넘는 숫자 각각) → 경고 로그 1줄 · 삭제 0 · 배경 작업 없음 · 로그 `keep_days=off` · **기동 성공**(기록은 켜진 채 — 오늘 파일에 줄이 써진다) ⑩ 표면: 허용 경로 6개 그대로(`test_api_surface.py` 변경 없이 통과) · 일반 로그 캡처에 발화 문장 0 ⑪ **(0.9.0 · §5.9 `fixed` · D-58)** utterance 줄 키 순서 = `type` · `session` · `at` · `lang` · `id` · `side` · `original` · `translation` · `terms` · **`fixed`** · 여기 없는 키 0 · 바로잡은 발화 → `translation` = 고친 글 · `fixed` = 그 term id(시드 순서) · `fixed` ⊆ `terms` · 바로잡지 않은 발화 · 못 찾은 발화 · 바로잡기 끈 세션 → `fixed: []`(키는 있음) · `session_start` · `session_end` 줄에는 `fixed` 없음 · **(0.9.1) `translation_before`** — 바로잡은 줄: `fixed` 다음 키 · 값 = 고치기 전 번역(자막 모양 — zh-Hant 는 번체 변환 뒤) · `translation` 과 다름 / **`fixed: []` 인 줄에는 키가 없다**(바로잡지 않음 · 못 찾음 · 끈 세션) / 브라우저로 나간 caption 프레임에 `fixed` · `translation_before` 키 0 |
| **STT 설정(0.8.0 · §5.10 · D-43 · D-47)** | `stt_config` 결과의 `model == "stt-rt-v6"` · **그 밖의 키 · 값이 0.7.0 과 같다**(키 집합 = `model` · `audio_format` · `sample_rate` · `num_channels` · `language_hints` · `enable_endpoint_detection` · `max_endpoint_delay_ms` · `translation` (+ `context`) · `max_endpoint_delay_ms == 1000`) · `endpoint_sensitivity` · `endpoint_latency_adjustment_level` · `enable_agent_text_input` 키 없음 · 코드 · 시험에 `stt-rt-v5` 문자열은 품질 시험 스크립트의 조합 A 인자 말고는 0 |
| **context `text`(0.8.0 · §4.5 · §4.6 · D-45)** | `to_soniox` 결과에 `text` 키 · 값 = 문안 상수(**§4.5 S1 ~ S4 네 문장과 글자 그대로** · 424자 · 줄바꿈 3 — 0.8.1 · D-49) · 키 순서 `general` → `text` → `terms` → `translation_terms` · 7개 언어 모두 같은 문자열 · **줄이기에서 `text` 가 줄지 않음**(기준을 아주 작게 줘도 `text` · `general` · 정방향 기본 그대로) · 크기 계산에 `text` 가 들어감(문안 길이만큼 기준을 낮춘 것과 묶음별 뺀 수가 같음) · `forward_only` 에 `text` 남음 · `is_forward_only` 판정은 0.7.0 과 같음 · entry 0 인 언어는 `context` 키 없음 그대로 · 로그에 `text=<글자 수>`(문안 0) · **`translation_terms` 의 모든 짝이 시드에서 왔다** — 레포 시드로 7개 언어 조립 결과의 ko 쪽 ∈ 시드 `ko` ∪ `ko_aliases` · 상대 쪽 ∈ 그 언어 entry `name` ∪ `aliases`(`norm` 뒤) · 그 밖 0(일반 낱말 짝 금지) · `GENERAL` 3쌍은 0.7.0 과 같음 · §4.6.1 가짜 Soniox 6건 그대로 통과(재연결 설정에 `text` 가 든 것만 다름) |
| **빈 원문(0.8.0 · §5.11 · D-48)** | 판정 함수: 빈 문자열 · 공백뿐 · 문장부호뿐(반각 · 전각 · CJK) · 기호뿐 → 참 / 한 글자 · 숫자 하나 · 글자 + 문장부호 → 거짓. 가짜 Soniox 로: ① 원문 문장부호뿐 + 번역 있음으로 확정 → 브라우저로 `caption` 0 · `audio_start` 0 · TTS 연결에 보낸 글 0 · 로그 1줄(문장 0) ② 원문 빈 채 번역 토큰만 온 `final:false` → caption 0 ③ 원문에 글자가 생기면 그때부터 caption 이 나감 ④ `final:false` 가 나간 뒤 빈 원문으로 확정 → 같은 `id` 의 둘 다 빈 `final:true` caption 1번 · 오디오 0 ⑤ 짧은 정상 발화(글자 1 ~ 2개 + 마침표)는 0.7.0 과 같이 나감(caption · TTS) ⑥ 원문 있음 · 번역 빔 → 0.7.0 과 같음 ⑦ 막힌 발화 앞뒤의 정상 발화가 영향을 받지 않음(순서 · 오디오) ⑧ 기록 켠 채 ① → utterance 줄 0 · `session_end.utterances` 에 안 세어짐(OQ-026 닫히기 전 동작) ⑨ `pause` · `stop` flush 로 확정된 빈 원문도 같은 규칙 |
| **바로잡기(0.9.0 · §5.12 · D-58)** | **순수 함수**(가짜 시드 — term · 틀린 꼴을 시험이 정한다): **걸리는 조건** — 원문에 term · 번역에 이름 없음 → 돈다 / 번역에 `name` 있음 → 그대로 / 번역에 **별칭**만 있음 → 그대로(별칭을 name 으로 안 바꿈) / 원문에 term 없음 → 그대로(번역에 틀린 꼴이 있어도) / 한 → 외인데 `entries[L]` 없음 → 그대로 · 로그 0 / 원문 「더 긴 일치」(긴 이름의 term 만 대상) · **방향** — `side=me` → 대상 = `norm(entries[L].name)`(zh-Hant · yue 는 간체) · `side=them` → 대상 = `ko` 대표명 · **① 시드 틀린 꼴** — `wrong`(한 → 외) · `ko_wrong`(외 → 한) · 일치 자리 전부 · 긴 꼴부터 · 라틴 경계(낱말 안쪽은 안 바꿈) · 그 밖 글자는 공백 무시 · zh-Hant 번체 꼴 ↔ 간체 번역문 · **② 다른 언어 이름 · 별칭** — 한 → 외에 남은 한글 대표명 · 다른 언어의 `name` · `aliases`(라틴 · 다른 문자) / 외 → 한에 남은 `L` 의 `name` · 별칭 · **③ 가까운 라틴 낱말** — 거리 1 · 2 → 바꿈 · 거리 3 → 안 바꿈 · 4글자 미만 → 안 바꿈 · 대소문자 무시 · 낱말 수가 같은 것끼리(두 낱말 꼴) · 여러 개면 가장 가까운 하나 · 같으면 앞쪽 · 한 자리만 · 기준 숫자가 코드 상수 한 곳 · **단계 순서** — ① 에서 바꿨으면 ② · ③ 안 감 · **빼는 것 · 보호 구간** — 후보가 다른 term 의 맞는 이름이면 안 바꿈 · 번역에 맞게 나온 옆 term 이름 구간 · 앞 term 이 갈아 끼운 구간은 안 건드림 · **여러 term** — 각각 · 시드 순서 · 한쪽만 틀리면 그 term 만 · **못 찾음** — 번역문 그대로 · 로그 1줄(term id · 언어 · side — 문장 · 꼴 0) · 바꿨음 로그 1줄(문장 · 꼴 0) · 결과 = (고친 글 · 바로잡은 id · 못 찾은 id) / **가짜 Soniox 세션**: ① 틀린 꼴이 든 번역으로 확정 → `final:true` caption `translation` = 고친 글 · **TTS 연결에 보낸 글 = 고친 글**(괄호 제거 뒤 · zh-Hant 는 간체) · 기록 줄 = 고친 글 + `fixed` ② 같은 발화의 **`final:false` caption 은 고치지 않은 글 그대로** ③ zh-Hant — 자막은 번체 변환 뒤 사전 이름 · TTS 입력은 간체 ④ 원문 caption 은 그대로 ⑤ `pause` · `stop` flush 로 확정된 발화도 바로잡음 ⑥ 빈 원문으로 막힌 발화는 바로잡기를 부르지 않음 ⑦ 바로잡기 함수가 예외 → caption · 오디오는 고치지 않은 글로 그대로 나감 · 경고 1줄 · `fixed: []` ⑧ WS 메시지 키 집합이 0.8.x 와 같음(새 키 0) ⑨ 로그 캡처에 문장 · 틀린 꼴 문자열 0 / **(0.9.1 · 처분 §11)** ⑩ **③ 의 범위(F-1)** — `en` 세션 · 한 → 외 · 원문에 term · 번역에 이름 없음 · 번역에 이름과 거리 1 ~ 2 인 일반 낱말 → **안 바꿈**(못 찾음 로그 1줄) · `vi` 도 같음 · 같은 번역문을 `ja` · `zh` · `zh-Hant` · `th` · `yue` 세션에 주면 ③ 이 돈다 · 외 → 한은 `en` · `vi` 세션에서도 ③ 이 돈다 · `en` · `vi` 한 → 외에서 ① ② 는 그대로 돈다 ⑪ **낱말 경계** — 성조 글자가 든 베트남어 낱말 가운데의 ASCII 조각은 ① ② ③ 어느 단계에서도 안 바꿈 · 한자 · 가나 · 태국 문자 · 한글에 붙은 영문 꼴은 바꿈 ⑫ **같은 현지명 묶음(W-1)** — 외 → 한 · 두 term 이 같은 `name` · 번역에 첫 term 의 ko → 둘째 term 은 대상 아님 · 로그 0 · `fixed: []` / 번역에 어느 쪽 ko 도 없으면 지금처럼 대상 ⑬ **순서(W-2)** — 두 term 이 걸리고 앞 term 의 ③ 후보가 뒤 term 의 ② 꼴과 가까울 때 → 뒤 term 이 ② 로 먼저 바뀌고 앞 term 의 ③ 은 그 자리를 못 건드림 ⑭ **자리 대응(W-3)** — 이 앱이 다루는 글자(한글 · 한자 번체/간체 · 가나 · 태국 문자 · 라틴)에서 정규화(`t2s` · `casefold`) 앞뒤 글자 수가 같음 · 글자 수가 달라지는 글자가 든 발화는 고치지 않은 글 그대로 / **(0.9.2)** ⑮ **한자 언어 사이(D-63)** — 가짜 시드 · `ja` 세션 · 한 → 외 · 번역에 다른 한자 언어의 한자 이름이 들어 있음 → **안 바꿈**(못 찾음 로그 1줄) · 같은 term 의 **라틴 · 가나 꼴**은 ② 그대로 바꿈 · `th` · `en` 세션에서는 한자 꼴도 ② 후보 · 외 → 한은 그대로 ⑯ **긴 꼴 먼저(레포 시드 `.10`)** — 앞부분이 같은 두 틀린 꼴 가운데 긴 꼴이 먼저 잡혀 꼬리 글자가 남지 않음 ⑰ **가까운 한글 낱말(D-64 · 가짜 시드)** — 외 → 한: 음절 하나 더 붙은 꼴 + 조사 → 대표명 + **조사 그대로** · 음절 하나 바뀐 꼴 → 바꿈 / 안 바꿈: 멈춤 목록 낱말 · 대표명 2음절 · 다른 term 의 ko 이름과 같은 꼴 · 거리 2 이상 / 한 → 외에서는 ④ 가 돌지 않음 / 같은 현지명 묶음의 둘째 term 은 ④ 뒤에 「못 찾음」 이 아님 / 상수(`KO_NEAR_MIN_SYL` · `KO_NEAR_MAX_DIST` · `KO_NEAR_STOP`)가 코드 한 곳 · (처분 §14) W-2 — 앞 term 이 갈아 끼운 ko 로 풀린 같은 묶음의 뒤 term 은 `missed` 0 · W-4 — 성조 붙은 라틴 꼴이 더 긴 낱말 가운데면 안 바꿈. 관문 수치(WP27 수정 2 뒤): `uv run pytest -q` **460 passed** / **(0.9.3 · D-65 · D-66 — ⑰ 을 이렇게 고쳐 읽는다)** 바뀜 = **한 음절 바뀐 꼴 · 한 음절 더 붙은 꼴**(+ 조사 → 조사 그대로) 뿐 ⑱ **좁힌 자리**(레포 시드 `.10` + 가짜 시드 — 검수 재현 전부): **빠진 꼴 + 조사 → 안 바뀜**(조사를 먹지 않음 · F-1 4건) · **이름 가운데 음절로 시작하는 일상 낱말 → 안 바뀜**(F-2 9건) · **첫 음절이 다른 꼴 → 안 바뀜** · **남는 것이 조사가 아닌 낱말 → 안 바뀜**(낱말 가운데를 자르지 않음 · 재검수 W-1) · **「일상 낱말 + 조사」 가 이름에서 음절 빠진 꼴과 같을 때 → 안 바뀜**(W-2) · 남는 것이 홀로 「요」 → 안 바뀜 · 대표명에 한글 밖 글자 → ④ 건너뜀 · 멈춤 목록이 낱말 전체 · 조사 뗀 낱말에도 걸림 · 7차에서 ④ 로 바뀐 꼴 셋은 그대로 바뀜(조사 보존). 관문 수치(수정 4 뒤): `uv run pytest -q` **489 passed** |
| **기본값 = 켬(0.8.1 · W-1 · §9.3 「조합」)** | (0.9.0) **시술명 바로잡기도 기본 = 켬** — 세션 선택 인자로만 끔 · 끈 경우 번역문 · TTS 입력이 0.8.x 와 같고 `fixed: []` · env · WS `start` 로 못 끔(소스 · `config.py` · `.env.example` 에 이름 0). 선택 인자를 주지 않은 조립 · 세션은 **문안 넣음 · 빈 원문 막기 켬 · `stt-rt-v6` · 기동 때 읽은 시드 · 뺀 역방향 짝 0** · 통역 API 경로(`api/interpret.py` · `container.py`)가 이 인자들을 넘기지 않는다(소스에 인자 이름 0) · `config.py` · `.env.example` 에 조합용 이름 0 · WS `start` 에 그런 키(문안 · 막기 · 모델 등)를 넣어 보내도 무시(설정 · 동작이 기본값과 같음) · 인자로 끈 경우만: 문안 뺌 → `to_soniox` 에 `text` 키 없음 · 막기 끔 → 빈 원문 발화가 0.7.0 처럼 나감 · 역방향 짝 하나 뺌 → 그 source 짝만 없고 나머지 같음 |
| 비밀값 | 로그 캡처에 토큰 · 키 · 비밀번호 0 |

### 9.2 front 확인

- `npx tsc --noEmit` · `npm run lint` · `npm run build` · `npx vitest run` 통과.
- 쓴 medikit 클래스를 **빌드 산출 CSS 와 전수 대조** — 없는 클래스 0(개념 design-system · `scripts/check-classes.mjs`). 시안에서 옮긴 클래스 · 0.5.0 세그먼트 · `PTT-Ready` 클래스 포함(§7.8 끝). (fe8475e 기준 177 · 없는 것 0)
- **(0.5.0 · D-37) 빌드 산출물 grep**: `.next/static`(브라우저로 나감)에 시드 낱말(美國音波 · Thermage · 써마지 · `koAliases`) · `glossary` · `용어집` · `SONIOX` · `INTERPRET_` · `NEXT_PUBLIC` 0. 서버 소스맵에 주석이 실리므로 front 소스 주석에도 「용어집」을 남기지 않는다.
- **시안 대조(D-20)**: 화면 21개(0.5.0 — r7 3개 더함 · `Glossary` 뺌 · 시안 파일과 같은 상태)를 390 × 844 로 스크린샷해 시안 값과 대조 — `data-product="ceramique"`(primary `#2498bd` 계산값) · 헤더 「Tongky」 · 로그인 「통키」 · 데모 로그인 단추 하나 · 회전 아이콘 · 원 크기(64 · 56 · 88) · 원 줄 140 · 원 위아래 안내 13px · 말풍선 좌우 · 언어 목록 펼침(뒤집힘이면 카드와 같이 180°) · 초기화 · 오버레이가 헤더를 덮음(햄버거가 안 눌림) · **(0.5.0) 세그먼트 · `PTT-Ready` 흰 원 · `PTT-Pressed` · 메뉴 로그아웃 하나**.
- 단위 시험: caption → 영역 배치(§7.5) · **말풍선 좌우 `isMine`**(D-24) · **`isNearBottom` · `hasNewBelow`**(D-25) · 상태 판정 순서(§7.3 #1 ~ #8) — 멈춤 중 `audio_start` → 「〈언어〉로 출력 중」 · 재생 끝 + 400 ms → 「멈춤」(FAIL-2) · 백그라운드 복귀 → 「시작 전」 · 오류 때 원 위 오류 문구 · 반이중 재개 타이머 · `pause` 뒤 같은 발화 조각 → 재생 0 · 게이트 그대로 · 다음 `audio_start` 뒤 재생(FAIL-1) · 앞 발화 재생 중 다음 `audio_start` → 표시는 앞 발화 재생 끝에 바뀜 · 마이크 막음은 즉시(WARN-4) · **`canReset` 은 멈춤(#5)에서만 · 초기화 → TTS 버림**(D-29) · **lang 7개 · 목록 표시 이름 · 한국어 이름(중국어 · 대만어) · 외국어 문구 빠짐 없음 · `htmlLang`**(D-28) · **(0.5.0 · D-36 `tests/ptt.test.ts`) 누름/뗌 → `resume`/`pause` · TTS 중 누름 → `clearPlayback` 뒤 `resume` · 판정(안 누름 = #4′ · 누름 = 듣는 중 · 출력 중이 #4′ 위 · 자동 모드는 그대로) · `canReset` 이 #4′ 에서도 참 · 문구 · 모드 기억(`interpret.mode`)** · **(0.5.0 · D-37 `tests/minimal-exposure.test.ts`) `lib/api` 에 glossary 없음 · 설정 오류 문구에 env 이름 없음**. 0.4.0 WP10 메뉴 행 시험은 지움.
- 「시작 전」 오버레이: 새로고침으로 통역 화면에 바로 들어와도 오버레이가 뜨고, 탭 전에는 WS · 마이크 · `AudioContext` 가 없다 · 탭 한 번으로 `AudioContext.state === "running"` · 원 누름은 오버레이가 덮여 있는 동안 동작하지 않는다.

### 9.3 실물 확인 — **완료 조건** (back · 키는 사용자 `.env`)

브라우저 없이 시험 스크립트(`back/scripts/live_check.py` — 프로세스 안 실행 · 포트 안 씀)로 해도 된다. 결과는 보고서 · JSON 에 수치로 남긴다(키 · 토큰 값 0).

**1차 결과 — 2026-10-26 (`orchestration/work/interpret-pwa-poc/live-check-2026-10-26.json` · 용어집 `2026-07-01-reviewed-v5` · 158행 · 정방향만)** — ① ~ ⑦ 모두 통과.

| # | 무엇 | 통과 조건 | 2026-10-26 결과 | 판정 |
|---|---|---|---|---|
| ① | 6개 언어 각각 용어집 `context` STT 연결 1회 | 6개 모두 거절 없이 | `terms` 157 · `translation_terms` 157 · 뺀 것 0 — en 9,295 · ja 8,989 · zh 8,572 · **th 9,900(최대)** · vi 9,579 · yue 8,501자 · **거절 0** · 첫 메시지 `tokens` 0.21 ~ 0.24초 · 오디오 전 | 통과 |
| ② | 시술명 한국어 발화 → 번역이 용어집 target 대로(context 없는 연결과 비교) | 용어집 target 과 같음 | en 3/3(없으면 1/3) · zh 3/3(없으면 0/3) · ja 2/3(없으면 0/3 — 전각 괄호로 나와 글자 대조만 빗나감). **외국어 발화(역방향)**: en 1/3 · zh 2/3 · ja 1/3 | 통과(정방향) · 역방향 결과로 **D-18** |
| ③ | `yue` · 한국어 발화 → caption 번체 · TTS 입력 간체 | 둘 다 | caption 「填充劑 … 諮詢」 · TTS 입력 「填充剂 … 咨询」 · TTS 언어 `zh` | 통과 |
| ④ | 외국어 발화(en) → `side=them` · 한국어 번역 · 한국어 TTS 24 kHz | 수신 | `side=them` · 한국어 번역 1 · `audio_start` 24000 · 294,912 B | 통과 |
| ⑤ | 괄호 병기 target 이 번역 · TTS 에 어떻게 나오나 | 기록만 | ja 번역 · TTS 입력 둘 다 괄호째(「フィラー（ヒアルロン酸）」 · 「チャウム（補充）」 — 후자는 Soniox 가 만든 괄호) | 기록 → **D-19**(§5.7) |
| ⑥ | 용어집 주소를 틀리게 둔 back 기동 → 통역이 `context` 없이 됨 | 연결 | `loaded=false` · `context` 비움 · `ready` · 확정 발화 1 | 통과(0.4.0 에서 이 경로는 없어짐 — §4.4) |
| ⑦ | 일부러 한도를 넘긴 `context` → 거절 시간 · 오디오 전인가 · `error_type` | 오디오 없이 2초 안 `invalid_request` | 29,110자 → **0.458초** · 오디오 전 · `invalid_request` · `request_id` 있음 | 통과 → `STT_CONFIG_CHECK_SEC` 2초 확정 |

**2차 결과 — WP6-BE 2026-10-26 (`live-check-wp6-2026-10-26.json` · 역방향 포함 · D-18 · D-19 반영 뒤)** — ⑧ ~ ⑪ 통과.

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| ⑧ | 6개 언어 역방향 포함 context 의 **실제 한도** — 전체(15,123 ~ 17,952자)가 모두 통과해, 같은 언어 짝을 덧붙여 크기를 늘리며 이분 탐색 | 통과 최대치 / 거절 최소치: en 25,922 / 26,009 · **ja 20,925 / 21,014** · zh 21,643 / 21,729 · th 22,566 / 22,611 · vi 24,778 / 24,902 · yue 22,643 / 22,740 · 모두 `invalid_request` · 0.41 ~ 0.45초 · 오디오 전 → **기본값 18,832**(ja × 0.9) · 그 값으로 6개 언어 재연결 거절 0 · 뺀 `terms` 0 · 뺀 역방향 0 | 통과 → **OQ-002 닫음**(§4.6) |
| ⑨ | 역방향 적중(용어 3개씩 · 2회) | 외국어 → 한국어: en 2/3 · 2/3(D-18 전 1/3) · zh 3/3 · 2/3(2/3) · ja 3/3 · 3/3(1/3). 한국어 → 외국어: en 2/3 · 2/3 · zh 3/3 · 3/3 · ja 1/3 · 0/3 — 하락은 한국어 STT 의 「신펄」 반쪽 전사(「Syn펄」)와 괄호 표기 대조 한계(「フィラー（ヒアルロン酸）」 대조) 탓이 대부분 | 기록(사람 목소리 재확인은 E2E) |
| ⑩ | TTS 괄호 제거(ja) | caption 번역 괄호 그대로 · TTS 입력 「…チャウムと、フィラーも…」 괄호 0 · `audio_start` 1 · 417,792 B | 통과 |
| ⑪ | URL 모양부터 틀린 용어집 주소로 기동 | 기동 · `InvalidURL` 경고 1줄(주소 0) · `loaded=false` · `ready` | 통과(0.4.0 에서 이 경로는 없어짐) |
| (폰 1) | zh-Hant 한국어 발화(필러 · 쥬비덤 · 신펄) | caption 번체(「填充劑 … 喬雅登 … 新珍珠 (Synpurl)」) · 용어 3/3 · TTS 입력 간체 · 괄호 제거 · `zh` · `audio_start` 1 | 통과(fix-phone1) |

**3차 재확인 — 시드(0.4.0 · D-33 · WP9 backend)** — 시드 `back/seed/glossary.json`(첫 가져오기 판)으로.

| # | 무엇 | 통과 |
|---|---|---|
| ⑫ | **7개 언어**(en · ja · zh · zh-Hant · th · vi · yue) 각각 시드 context 로 STT 연결 1회 · 기본값 18,832 | 거절 0 · 언어별 글자 수 · 칸 수(`terms` · 정방향 기본/별칭 · 역방향 기본/별칭) · 줄이기로 뺀 수 기록 |
| ⑬ | **zh-Hant 한도**(실제로는 7개 언어 모두 잼) — ⑧ 과 같은 방법(짝을 덧붙여 이분 탐색)으로 통과 최대치 · 거절 최소치 · `error_type` | 기록. 통과 최대치가 20,925 보다 작으면 기본값 = 그 값 × 0.9(내림)로 고친다(§4.6 · §2.4 · `config.py`) → 7개 언어 다시 ⑫. zh-Hant context 가 zh 와 얼마나 다른지(`t2s` 뒤 다른 짝 수) 기록 — OQ-013 |
| ⑭ | **써마지 · 울쎄라 정방향** — 한국어 발화 「써마지FLX」 · 「울쎄라」를 넣은 문장 → zh · zh-Hant · ja 번역에 **시드 현지명**(영문 상표명 아님)이 나오는가 · TTS 입력에 현지명 · 괄호 0 | 언어별 적중 수 · 번역문 · TTS 입력 기록(시드의 그 시술 현지명 그대로 대조 — 괄호가 없어 ⑨ 의 대조 한계가 없다) |
| ⑮ | **써마지 · 울쎄라 역방향** — 같은 언어(zh · zh-Hant · ja)로 현지명 · 별칭(영문 상표명)을 말한 문장 → 한국어 번역에 ko 대표명(「써마지FLX」 · 「울쎄라」) | 언어별 적중 수 기록 · 줄이기로 빠진 짝이면 「빠짐」 |
| ⑯ | 시드 검사 실패로 기동 → 프로세스가 0 아닌 코드로 끝남 · 오류 로그 1줄 | 기동 실패(빈 용어집으로 뜨지 않음) |

- ⑭ ⑮ 의 음성: `say`(macOS) 합성 또는 PCM 파일 — 원형 WP2 방식. 표본이 적으니 판정은 코디 · 사용자.

**3차 결과 — WP9 backend 2026-10-27 (`live-check-wp9-2026-10-27.json` · 시드 `2026-10-27.2` · 157 term)** — 배포 main 9befd18(PR #4).

| # | 결과 | 판정 |
|---|---|---|
| ⑫ | 7개 언어 거절 0. 글자 수(그때 기본값 18,832) en 16,131 · ja 17,360 · zh 16,464 · zh-Hant 16,464 · **th 19,340 → `terms` 45 뺌**(짝은 다 남음) · vi 16,272 · yue 16,090. 정방향 기본 157 · 별칭 1(「써마지」) · 역방향 기본 151 ~ 157 · 역방향 별칭 0 ~ 60 | 통과 → 기본값 20,251 로 다시 조립하면 7개 언어 **뺀 수 0** |
| ⑬ | 통과 최대치 / 거절 최소치(모두 `invalid_request`): en 26,372 / 26,463 · **ja 22,502 / 22,600(가장 작음)** · zh 22,953 / 23,027 · zh-Hant 22,842 / 22,917 · th 23,661 / 23,735 · vi 25,843 / 25,950 · yue 23,763 / 23,835. zh-Hant context(`t2s` 뒤)와 zh 는 짝 359개 중 **22개 다름**(s2twp 낱말 바꿈이 남음 — 镭射 · 奈米 · 专案 등) | **기본값 20,251**(ja × 0.9 · §4.6) · OQ-013 기록 |
| ⑭ | 「써마지FLX」 · 별칭 「써마지」 → zh 「美版热玛吉FLX」 ✓ ✓ · zh-Hant 「美版熱瑪吉FLX」 ✓ ✓(TTS 입력 간체) · ja 「サーマジFLX」 ✗ ✗(음역 — 짝이 context 에 있는데 안 잡힘). 「울쎄라」 → zh · zh-Hant ✗(「不饱和疗法」 — 한국어 전사부터 빗나감으로 보임) · ja 「ウルセラ」 ✓. TTS 입력 괄호 0 | 써마지는 **현지명으로**(D-33 목표) · 나머지 기록 |
| ⑮ | 현지명 발화 → 써마지FLX 는 zh · zh-Hant · ja ✓ · 울쎄라는 ja ✓ · zh 「美版超声刀」 → ✗ 「슈링크유니버스」. 영문 상표명 발화는 엇갈림. 구어(热玛吉 · 超声刀)는 ✗ — **비슷한 현지명**(美版超声刀 ↔ 韩版超声刀 · 美版热玛吉FLX ↔ 韩版热玛吉)이라 역방향이 다른 시술로 간다 | 기록 → 시드 데이터 숙제(§10 OQ-015) |
| ⑯ | 깨진 시드(id 중복)로 uvicorn · docker 기동 → **종료 코드 3** · 0.32초 · 오류 1줄 · 포트 안 열림. 정상 시드 이미지 `/api/health` `{"ok":true,"glossary":{"loaded":true,"version":"2026-10-27.2","count":157}}`(그때 모양 — 0.5.0 부터 `{"ok":true}` · §3.5) | 통과 |

- 첫 시드 = 가져오기 1회(term 157 · 합친 행 1 · 괄호 분해 없음 667 · 라틴(현지) 76 · 현지(라틴) 130 · 같음 15 · 그 밖 60 · `reviewed:false` = 그 밖 60 + zh-Hant 157) + 코디 처분 손 편집 1건(`ph-130` 써마지FLX `ko_aliases: ["써마지"]` · term `note` · `version` `.2`) — §10 OQ-014.

**4차 결과 — D-35 backend 2026-10-27 (`live-check-d35-2026-10-27.json` · 시드 `2026-10-27.3` · 기본값 20,251)** — 배포 main 145c872(PR #6).

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| ⑰ | **zh-Hant 대만 현지명** — 대만 발화 → 한국어 · 한국어 → 대만(합성 음성 · 문장 1개씩) | 대만 → 한국어 **3/4**: 「美國音波」 → 울쎄라 ✓ · 「鳳凰電波」 → 써마지FLX ✓ · 둘을 한 문장에 → 울쎄라 ✓ · 써마지 ✗(슈링크유니버스). 한국어 → 대만 **1/4**: 「써마지」(ko 별칭) → 鳳凰電波 ✓(TTS 입력 간체 凤凰电波) · 「울쎄라」 → Ultherapy ✗ · 「울쎄라랑 써마지FLX」 → Ulthera · Somagic FLX ✗ ✗. **줄이기는 원인이 아니다** — 줄이기 없이(전체 21,605자 · 한도 22,000 으로) 다시 돌려도 같은 결과 · 21,605자는 거절 0. 자막 「激光治疗 → 雷射治療」 · 「离子导入 → 離子導入」 | 대만명 → 한국어는 D-35 전(짝 없음)보다 나아짐 · 한국어 → 대만명은 짝이 context 에 있는데 Soniox 가 상표명 · 음역으로 냄 → 사람 목소리 E2E(OQ-017) |
| ⑱ | **운영 장애 재현**(§5.8 · `live_check.py idle` — zh-Hant · 발화 → 멈춤 35초(TTS keepalive 나감) → 다시 듣기 → 발화) | 고치기 전 코드: **47.4초에 `error soniox_unavailable`**(`channel=tts` · `invalid_request` · `Missing stream_id` — 운영 50초와 같음) · keepalive 만 옛것 + 새 `speak`: 끝까지 통과(경고 로그만 — 방어 동작) · **고친 코드: 발화 2 · 오디오 2 · 오류 0**. TTS 프로브: `{}` → `{"stream_id":"","error_type":"invalid_request","error_message":"Missing stream_id"}` · `{"keep_alive": true}` → 응답 없음(정상) | 통과 → 배포(PR #6 · infra #30) |

**5차 재확인 — 시드 `.6` · 통역 기록(0.6.0 · D-39 ~ D-41 · WP16 backend → WP18 운영)** — 결과는 `live-check-v2-<날짜>.json`(키 · 토큰 0 · 발화 원문은 합성 문장이라 넣어도 된다).

| # | 무엇 | 통과 조건 |
|---|---|---|
| ⑲ | **7개 언어 시드 `.6` context** — STT 연결 1회씩 · 기준 = §4.6 언어별 표(0.6.1 — 0.6.0 은 기본값 20,251) | 거절 0 · 언어별 글자 수 · 칸 수(`terms` · 정방향 기본/별칭 · 역방향 기본/별칭) · **줄이기 단계별 뺀 수** 기록. 정방향(기본 · 별칭) 뺀 수 0 이면 통과 — 아니면 §4.6 「0.6.0」 판정대로 코디 보고 |
| ⑳ | **새 시술 정방향** — 한국어 문장 3개(①「써마지 CPT」 · 「소프웨이브」 ② 「프로파일로」 · 「뉴라미스」 ③ 「엑시온」 · 「덴서티」 · 「엠페이스」)를 **zh-Hant · ja · en** 3개 언어로(합성 음성 · `say` 또는 PCM) | 언어별 번역에 §4.2.2 name 이 나온 수(적중 / 시도) · TTS 입력 문자열 기록 · **en 의 대문자 name(EXION · DENSITY · EMFACE) TTS 를 사람이 들어 본 결과** 한 줄(글자 읽기인지 낱말 읽기인지 — OQ-019). 적중 수는 판정 기준이 아니다(기록 · 코디 · 사용자 판정) |
| ㉑ | **통역 기록** — ⑳ 세션을 `INTERPRET_RECORD_DIR` 켠 back 으로 | 오늘 파일 1개 · 세션마다 `session_start` · `utterance` · `session_end` · `utterance.terms` 에 ⑳ 의 `kr-…` id · 파일에 키 · 토큰 · IP 0(grep) · 일부러 폴더 권한을 뺀 실행 1회 → 통역은 끝까지 · 경고 로그 1줄 |

- ⑲ ~ ㉑ 은 backend 가 로컬에서(WP16) · ⑳ 의 일부(3개 언어 1회) · ㉑ · 7일 삭제는 운영에서 다시(WP18 · §9.6). (0.7.0 — 보관 기간이 env 로 바뀐 뒤의 운영 확인은 §9.6 「배포 뒤 확인 (0.7.0 · WP20)」.)

**5차 결과 — WP16 backend 2026-10-27 (`live-check-wp16-*.json` · 시드 `2026-10-27.6` · 결과 JSON 에 키 문자열 0)** — 배포 main 17c26b5(PR #10). 시험 `pytest` 295 passed · `ruff` 통과.

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| ⑲ (첫) | 기본값 20,251 · `seed.json` | 거절 0 · 정방향 기본 170 / 별칭 1(그때 ko 별칭 「써마지」) 뺀 수 0. **zh-Hant** 전체 → 20,241 · `terms` 171 전부 · 역방향 별칭 68 빠짐 · **th** `terms` 57 빠짐 · 나머지 5개 언어 0 | 0.6.0 판정으로는 통과 — 그러나 공통 기본값이 넉넉한 언어의 짝을 뺌 → ⑬′ 재측정 |
| ⑬′ | `.6` 언어별 한도(`ceiling.json`) | §4.6 표(통과 최대치 / 거절 최소치) · zh-Hant 는 줄이기 이분 탐색 · 가장 작은 ja 22,688 | 언어별 표로(코디 처분 3) |
| ⑲ (다시) | 공통 20,419(ja × 0.9 · `seed-2.json`) | 거절 0 · zh-Hant 역방향 별칭 63 · th `terms` 38 빠짐 | 중간 단계(기록) |
| **⑲ (최종)** | **언어별 표 · env 없음**(`seed-3.json`) | 거절 0 · 7개 언어 정방향 기본 170 · 정방향 뺀 수 0. 보낸 글자 en 17,589 · ja 19,408 · zh 18,565 · **zh-Hant 21,658**(기준 21,689 · `terms` 170 · 역방향 별칭 33 빠짐) · th 20,804(뺀 수 0) · vi 17,596 · yue 17,636(뺀 수 0) | **통과** — 남는 손실 zh-Hant 만(§4.6) |
| ⑳ (첫) | 새 시술 정방향(`newterms.json` · ko 별칭 「써마지」 있음) | zh-Hant **1/7** — 「써마지 CPT」 → **`鳳凰電波`(ph-130 FLX 이름 · 오역)** · 소프웨이브 ✓ · 프로파일로 → 「這個檔案」(STT 가 「프로파일」) · 뉴라미스 → 「優美思」(시드 優美施와 한 글자 다름) · `Exion` · `density` · `Mfase` 영문. ja **3/7** — サーマジCPT · プロファイル · デンソティ · エンペイス 빗나감. en **6/7** — 프로파일로만 「right profile」. 오류 0 · TTS 입력 괄호 0 | 기록 → **OQ-018 ⑤ 뒤집음**(§4.2.3 D) |
| ⑳ (다시) | ko 별칭 「써마지」 지운 뒤(`newterms-2.json`) | zh-Hant **2/7** — 「써마지 CPT」 → **`黃金電波`(kr-001 · 맞음)** · 기록 판정도 `kr-001`. ja **4/7** — サーマジCPT 그대로(시드 name `サーマクールCPT` 와 다른 음역 · ko 별칭과 무관) · エムフェイス 이번엔 적중(합성 음성 · 비결정). 오류 0 | 기록 — 남은 미적중은 STT · 번역 쪽(짝은 context 에 있음 · OQ-017 ④) |
| ⑳ TTS | 대문자 name 소리(`tts-samples/` — `EXION` · `DENSITY` · `EMFACE` × en · zh · th · vi 12개 + en 문장 1) | 길이 en 0.77 ~ 0.94초 · **`EMFACE-zh` 2.39초**(확연히 김 — 글자 읽기일 수 있음). 글자 / 낱말 읽기 판정은 **사람이 아직 안 들음** | **OQ-019 — 사용자 청취 대기** |
| ㉑ | 기록(⑳ 9세션 · 폴더 = 레포 밖) | 오늘 파일 1개 · 27줄 = 9 × start · utterance · end(`reason=stop`) · `terms` 에 kr-001 · 002 · 003 · 004 · 005 · 007 · 008(번역에 나온 것과 같음) · 키 · `Bearer` · token · IP 꼴 · `http` 0. **권한 뺀 폴더 1회** → 통역 끝까지(final 1 · error 0) · 경고 1줄 `interpret record write failed: PermissionError` · 파일 0 | 통과 |

**6차 — 품질 시험(0.8.0 · D-43 ~ D-48 · DEC OQ-021 ~ 023 · WORK WP21 ~ WP24)** — **품질 개선의 완료 조건**(D-44).

> 베타 기록에서 문제가 됐던 문장으로 만든 시험 목록을, 고치기 전과 고친 뒤에 **같은 소리로** 돌려 비교한다. **이 문서에는 문장을 쓰지 않는다**(실제 상담 문장을 다듬은 것 — DEC OQ-021) — 번호 · 분류 · 판정 방식 · 파일 위치만.

**시험 목록**

| 항목 | 계약 |
|---|---|
| 위치 | 프로필 레포 워킹트리 `reference/2026-11-12-interpreter-idea/test-sentences.md` — **로컬 전용 · git 제외**(DEC OQ-021). 레포 · PR · 보고에 그 문장을 붙이지 않는다 |
| 문장 수 | **T01 ~ T33**(33개) — zh 19 · en 8 · ja 6. 한 → 외(직원이 말함) 31 · 외 → 한(손님이 말함) 2(T10 · T22) |
| 문장마다 든 것 | 번호 · 언어 · 방향 · 말할 문장 · 기대(뜻) · **「나오면 FAIL」 문구** · 출처(기록 날짜 · 세션). 시술명의 정답 표기는 목록이 정하지 않는다 — 시드 `.7`(§4.2.4)을 따른다 |

| 절 | 분류 | 번호 | 수 | 언어 | 무엇을 보나 | 고치는 자리 |
|---|---|---|---|---|---|---|
| 1 | 시술명 | T01 ~ T10 | 10 | zh 6 · en 2 · ja 2 | 시술 · 제품 이름이 현지 표기로 나오는가(영문 · 직역 · 수술 뉘앙스가 아닌가) | 시드 `.7`(§4.2.4) · `text`(§4.5) |
| 2 | 손님에게 하는 말 | T11 ~ T22 | 12 | zh 6 · en 4 · ja 2 | 손님이 듣는 말로 · 높임으로 옮겨지는가(직원 쪽 낱말 · 반말이 아닌가) | `text`(§4.5) |
| 3 | 끊김 | T23 ~ T26 | 4 | zh 2 · en 2 | 쉼이 있어도 **기대한 수의 발화**로 나오는가(문장마다 기대 수가 다르다 — 한 발화로 묶여야 하는 문장 · 두 발화로 나뉘어야 하는 문장이 섞여 있다 · 기대 수는 규칙 파일에) | v6(§5.10) · 남으면 끊김 값(OQ-027) |
| 4 | 인식 | T27 ~ T29 | 3 | zh 3 | 한국어를 바르게 듣는가 · 말이 없을 때 번역을 지어내지 않는가(T29) | v6 · 빈 원문 막기(§5.11) |
| 5 | 사전 겹침 · 오류 값 | T30 ~ T33 | 4 | zh 2 · ja 2 | 의도된 겹침이 유지되는가(T30) · 겹침 · 뒤바뀜 · 잘림이 고쳐졌는가 | 시드 `.7`(§4.2.4 E3 · E4 · E8 · E11) |

**조합 — 전후 비교**

| 조합 | STT 모델 | 시드 | context `text` | 빈 원문 막기 | 끊김 | 무엇 |
|---|---|---|---|---|---|---|
| **A 「전」** | `stt-rt-v5` | `.6` | 없음 | 없음 | 1000 | **지금 운영 조합**(main `e0fbda8`) — 고치기 전 |
| **B 「v6 단독」** | `stt-rt-v6` | `.6` | 없음 | 없음 | 1000 | 모델만 바꿈 — v6 단독 효과(D-43) · 3절이 v6 에서도 조각나는지(D-47) |
| **C 「후」** | `stt-rt-v6` | `.7` | 있음 | 있음 | 1000 | 고친 뒤 전부(WP21 + WP23) |

- **A 는 2026-12-15 전에만 돌릴 수 있다** — 그날 `stt-rt-v5` 가 없어지고 v5 요청은 v6 로 간다(§5.10). A 를 먼저 끝낸다.
- A 가 운영과 같다는 확인: 조합 A 의 STT 설정(모델 · 끊김 · context 칸 · 글자 수)이 main `e0fbda8` 의 `stt_config` · `build_context` 결과와 같음을 결과 JSON 에 수치로 남긴다(언어별 context 글자 수 = §4.6 「줄이기 없는 전체」 · zh-Hant 21,658).
- **A 에서 막기가 꺼졌다는 확인(0.8.1 · W-1)**: 조합 A · B 의 결과에서 **막힌 빈 원문 수 = 0**(막기 꺼짐 — 33문장 합계) · `text` 글자 수 = 0. C 는 `text` 글자 수 = 424.
- **조합을 바꾸는 길(0.8.1 · W-1)** — A · B · C 는 **같은 코드(WP21 뒤)** 위에서 돈다(A 를 옛 커밋 체크아웃으로 돌리지 않는다). 여섯 가지를 **조립 · 세션 함수의 선택 인자로만** 바꾸고, 시험 스크립트가 그 인자를 준다:

| 바꾸는 것 | 받는 자리 | 기본값(= 운영) | A · B | 그 밖 |
|---|---|---|---|---|
| context 문안 넣기 | 조립 함수(`build_context`) | **넣음** | 뺌 | — |
| 빈 원문 막기 | 세션(`InterpretSession`) | **켬** | 끔 | — |
| STT 모델 이름 | 세션 → `stt_config` | `stt-rt-v6` | A = `stt-rt-v5` · B = 기본 | — |
| 시드(용어집) | 세션에 넘기는 용어집 — 스크립트가 시드 파일을 `load_seed` 로 읽어 준다 | 기동 때 읽은 `back/seed/glossary.json` | 시드 `.6` 파일 | C = `.7` |
| 역방향 짝 하나 빼기 | 조립 함수(뺄 source 목록) | 없음 | 울쎄라 원인 가르기에서만 | — |
| 끊김 값 | 세션 → `stt_config` | §5.10(1000 · 다른 값 안 보냄) | 기본 | OQ-027 추가 실행에서만 |

- **운영 기본값은 전부 「켬」(위 표의 기본값)이고 env · WS 메시지로는 못 바꾼다** — `config.py` 에 조합용 이름을 두지 않고(§2.4), `start` 메시지에 키를 더하지 않으며(§5.3 그대로), 통역 API 경로는 이 인자를 주지 않는다. 시험(§9.1 「기본값 = 켬」)이 막는다.
- 스크립트는 조립 결과를 손으로 고쳐 넣지 않는다 — 위 인자로만. 그래야 A · B · C 가 운영과 같은 길(조립 → 세션 → Soniox)을 탄다.
- 끊김 값을 바꿔 보는 실행(OQ-027)은 조합 C 에 값만 달리한 **추가 실행**으로 하고 값마다 따로 적는다. **0.9.0 — 조합 C2**(D-55): C 와 같고 `max_endpoint_delay_ms` 만 **2000** · T01 ~ T54 를 C 와 같은 음성으로(결과는 아래 「6차 결과」).
- **0.9.0 — 일곱째로 「시술명 바로잡기」**(§5.12 · 받는 자리 = 세션 · 기본값 = 켬)가 는다. 6차의 A · B · C · C2 는 바로잡기가 없던 코드에서 돌았다 — **6차 결과는 「바로잡기 없음」 의 수치다.** 7차(아래)는 기본값 그대로(전부 켬)만 돈다.

**입력 — Soniox TTS 로 만든 음성 파일(DEC OQ-022)**

| 항목 | 계약 |
|---|---|
| 만들기 | 목록의 「말할 문장」을 **Soniox TTS**(`tts-rt-v2` · **말할 문장의 언어** — 한 → 외 = `ko` · 외 → 한 = 목록 「언어」 칸의 언어(Soniox 코드 · §5.5) · 앱과 같은 음색)로 합성해 STT 입력 형식(PCM s16le · 16,000 Hz · mono)의 파일로 둔다. **문장마다 파일 하나 · 한 번 만들어 A · B · C 에 같은 파일**(파일 해시를 결과에 남겨 같은 소리임을 보인다) |
| 3절(쉼) | 목록의 쉼 표시 자리마다 **무음 1.0초**를 넣은 파일을 따로 만든다(조각을 따로 합성해 이어 붙임) |
| T29(말 없음) | 말 없는 5초 파일(무음 또는 낮은 잡음 — 무엇을 썼는지 결과에 적는다) |
| 재생 | back 을 거쳐(프로세스 안 · `live_check.py` 방식 — 브라우저 없음) **실시간 속도로** 40 ms 조각씩 보낸다(끊김 판정이 시간에 달렸다 — 한꺼번에 밀어 넣지 않는다). 파일 끝 뒤 무음 꼬리를 붙여 발화 끝을 기다린 다음 `stop`. **문장마다 새 세션** — `start` 의 `lang` = **목록 「언어」 칸의 언어**(한 → 외 문장도 그 언어 세션이다 — 말은 한국어 · 0.8.1 W-4) |
| 보관 | 음성 파일은 문장과 같은 것이다 — **레포에 넣지 않는다**(레포 밖 또는 git 제외 폴더) |
| 한계 | 합성 음성은 사람 목소리가 아니다 — 사람 목소리 확인은 OQ-017 그대로 남는다. 판정이 실행마다 갈리는 문장은 다시 돌린 횟수와 결과를 적는다(Soniox 출력은 결정적이지 않다 — ⑳) |

**판정**

| 누가 | 무엇을 | 어떻게 |
|---|---|---|
| **기계** | 「나오면 FAIL」 조건 | 목록의 FAIL 칸을 문장마다 **규칙**으로 옮겨 목록 옆 **규칙 파일**(로컬 전용)에 둔다. 규칙에 하나라도 걸리면 그 문장은 FAIL. **규칙 종류는 아래 넷뿐**(0.8.1 · W-3) |
| **기계** | 발화 수 | 한 파일에서 나온 **확정 발화 수** · 막힌 빈 원문 수 · 번역 줄 수를 센다. 규칙 파일에 **문장마다 기대 확정 발화 수**를 적고(33문장 전부 — 3절은 문장마다 다르다 · T29 는 번역 줄 0) **조각 수 = 실제 − 기대**(0.8.1 · W-2). 조각 수 > 0 이면 조각남 · < 0 이면 묶이면 안 될 것이 묶임 — 둘 다 그 수 그대로 적는다 |
| **기계** | 지연 | 파일의 말이 끝난 때 → 마지막 확정 caption 까지(ms) — 끊김 값 판단(OQ-027)의 재료 |
| **사람** | 기계로 못 옮긴 조건 | 규칙 ④ 로 남긴 문장 — 목록의 FAIL 칸을 사람이 읽고 걸렸는지 본다(걸리면 아래 등급에서 「오역」 · 「어색」 쪽으로) |
| **사람** | 뜻 · 자연스러움 | 목록의 「기대」와 견줘 발화마다 **좋음 · 어색 · 오역 · 인식 · 빈값**(BASE-001 2026-11-14 평가와 같은 분류). 코디가 먼저 보고 **중국어는 중국 코디 확인을 권장**(D-44). 사람 판정은 로컬 결과 파일(원문 · 번역이 든 것)을 보고 한다 |

**기계 판정 규칙 — 종류 넷(0.8.1 · W-3)** — 규칙 파일의 규칙은 이 가운데 하나다. 워커가 다른 종류를 만들지 않는다.

| # | 종류 | 무엇 | 적는 것 |
|---|---|---|---|
| ① | **글자 그대로** | 정한 문자열이 확정 발화에 **나오면** 걸림 — 또는(0.8.2 · N-2) **없으면** 걸림(손님 쪽 문장 — 있어야 할 ko 대표명) | 문자열 · 찾을 쪽(원문 · 번역) · **걸리는 쪽(나오면 · 없으면 — 적지 않으면 「나오면」)** · 대소문자를 가르는지 · 중국어는 양쪽을 간체로 맞춘 뒤(`t2s`) |
| ② | **정규식** | 글자 그대로로 못 적는 꼴 — 「영문으로 나오면」(라틴 글자열) · 소문자로 시작 같은 것 | 정규식 · 찾을 쪽 · 건너뛸 낱말(그 문장에서 영문이 정상인 것)이 있으면 그 목록 |
| ③ | **발화 수** | 기대 확정 발화 수와 다르면 걸림(위 「발화 수」) | 기대 수 · T29 는 번역 줄 0 |
| ④ | **기계 판정 없음 → 사람 판정** | 기계로 옮길 수 없는 조건 — 「뜻이 바뀌면」 · 「앞말이 붙으면」 · 「이름이 깨지면」 · 「다른 것으로 바뀌면」 처럼 위치 · 뜻을 봐야 하는 것 · FAIL 칸이 빈 문장 | 「없음」 과 왜 못 옮기는지 한 줄 |

- 한 문장에 규칙이 여럿일 수 있다(예 ① + ③). ④ 만 있는 문장의 기계 판정은 「없음」 — 전후 비교의 기계 FAIL 수에서 **분모에서도 뺀다**(기계 판정이 있는 문장 수를 같이 적는다).
- 애매하면 ④ 로 둔다 — 억지 정규식으로 옮기지 않는다(해석에 따라 전후 FAIL 수가 달라진다).
- **규칙 파일은 코디가 확인한 뒤에 조합 A 를 돌린다**(WORK WP22 ①). A 를 돌린 뒤에는 규칙을 바꾸지 않는다 — 바꾸면 A · B · C 를 그 규칙으로 다시 판정한다(음성 · 원본 결과는 그대로 · 판정만 다시).

**손님 쪽(외 → 한) 문장 — 7개 언어 × 3 = 21문장(DEC OQ-023 · D-50)**

- 기록에 손님 쪽 재료가 거의 없어(목록 2문장) **새로 짓는다** — 실제 기록 문장이 아니다.
- 조건: **앱 7개 언어(en · ja · zh · zh-Hant · th · vi · yue) 각각 3문장 = 21문장**(D-50 — 사전 보정이 7개 언어 전부라서) · 방향 외 → 한 · 문장마다 **시드 `.7` 의 그 언어 현지명**(§4.2.4 보정 결과)이 든 시술명 1개 이상 · 기대 = 한국어 번역에 그 term 의 ko 대표명 · 손님이 클리닉에서 할 법한 말(문의 · 경험 · 희망).
- 문장은 시드 `.7` 이 확정된 뒤 **WP24 에서** 짓고, 목록 파일에 번호를 이어(**T34 ~ T54** · 언어 순서는 §5.5 표 순서 · 언어마다 3개씩) 더한다. 이 문서에는 번호 범위 · 언어 · 판정만 적는다.
- 합성 언어 · 세션: 말할 문장이 외국어라 **합성 = 그 언어의 Soniox 코드**(zh-Hant · yue 는 `zh` — 문장은 간체로 바꿔 합성 · §5.5 · §5.6) · `start` 의 `lang` = 앱 lang(`zh-Hant` · `yue` 그대로). zh-Hant · yue 의 합성 음성은 만다린이다(광둥어 음성이 없다 — OQ-017 ②).
- 규칙 = ① 글자 그대로 · **걸리는 쪽 = 「없으면」**(한국어 번역에 그 term 의 ko 대표명이 없으면 걸림 — 규칙 종류 표 ① 의 「걸리는 쪽」 칸) + ③ 발화 수.
- 현지명이 `.7` 값이라 조합 C 에서 판정한다(A · B 는 참고로만 돌려도 된다).

**울쎄라 원인 가르기(D-44 · §4.2.4 E7)** — 짝이 context 에 들어갔는데 영문으로 나온 원인을 셋으로 가른다. 시드 `.6` 기준(조합 A · B)에서:

| 가르는 것 | 어떻게 | 읽는 법 |
|---|---|---|
| 단독 / 나란히 | **T02**(울쎄라만) 와 **T03**(울쎄라 · 써마지를 한 문장에) | 단독은 현지명 · 나란히만 영문이면 → 옆 낱말(써마지에 짝이 없음 — E5) 탓 |
| zh 별칭 `Ultherapy` 역방향 짝 유무 | 같은 두 문장을, context 에서 **역방향 별칭 짝 `Ultherapy → 울쎄라` 하나만 뺀** 변형으로 한 번 더(시험 스크립트 인자 — 시드 파일은 안 고친다) | 뺐을 때만 현지명이면 → 별칭 짝 탓 → `.7` 에서 별칭 처분(§4.2.4 E7) |
| 모델 | 위 넷을 A(v5) · B(v6) 둘 다 | v6 에서만 현지명이면 → 모델 탓(시드 손질과 별개) |

- 결과 = 2(문장) × 2(짝 유무) × 2(모델) = **8칸의 기계 판정**(영문이 나왔는가) — WP22 가 내고, 코디가 §4.2.4 처분에 쓴다. C 에서는 `.7` 처분 뒤 모양으로 T02 · T03 을 다시 본다.

**실물 번호 · 통과 조건**

| # | 무엇 | 통과 조건 · 기록 |
|---|---|---|
| ㉒ | **v6 context 연결** — 7개 언어 각각 `stt-rt-v6` · 문안 포함 context 로 STT 연결 1회. (WP21) 시드 `.6` · (WP23) 시드 `.7` + **⑬′ 한도 재측정**(v6 · 문안 포함) | 거절 0 · 언어별 글자 수 · `text` 글자 수 · 묶음별 뺀 수 · 문안 때문에 더 빠진 수(§4.6 계산 방법). WP23 은 통과 최대치 · 거절 최소치까지 — 정방향이 빠지거나 거절이 나면 코디 보고(OQ-028). **(0.8.3 · WP23) 이 재측정이 D-54 의 기준이다** — 넘는 언어만 근거가 약한 별칭을 빼고 다시 잰다 · 그래도 넘으면 멈춘다(§4.6 「D-54 절차」). **(0.8.2 · WP23) 「써마지」 다시 보기** — ⑳ 과 같은 방법(합성 음성 · 한 → 외)으로 「써마지」 · 「써마지FLX」 · 「써마지 CPT」 세 이름이 각각 제 term(`kr-014` · ph-130 · `kr-001`)의 현지명으로 나오는지(§4.2.4 ② A — 일반 term 이 세대 이름을 뭉개지 않는지 · 결과는 이름 · 판정만) |
| ㉓ | **품질 시험 조합 A · B** — T01 ~ T33 · 같은 음성 파일 | 33문장 × 2조합이 오류 없이 끝남 · 결과 JSON 2개 · A 의 설정이 운영과 같음(위) · **A · B 막힌 빈 원문 수 0 · `text` 글자 수 0**(0.8.1) · 규칙 파일 코디 확인 뒤 실행 |
| ㉔ | **울쎄라 원인 가르기** | 8칸 판정 |
| ㉕ | **품질 시험 조합 C** — T01 ~ T33 + 손님 쪽 **T34 ~ T54**(21문장 · D-50) · 같은 음성 파일(손님 쪽은 새 파일) | 오류 없이 끝남 · 결과 JSON · **전후 비교 표**(아래) · 3절 조각 수 · 지연 |

**결과 — 레포에는 번호 · 수치만**

- 결과 JSON(코디 작업 폴더 `orchestration/work/<slug>/` · 레포에 들어감): 조합 · STT 모델 · 시드 판 · `text` 글자 수 · 끊김 값 · 언어별 context 글자 수 · 묶음별 뺀 수 · 음성 파일 해시 + **문장마다** T 번호 · 언어 · 방향 · 절 · 기계 판정(pass · fail · 없음) · 걸린 규칙 번호(규칙 파일의 번호 — 문구 아님) · 규칙 종류(① ~ ④) · 확정 발화 수 · **기대 발화 수 · 조각 수** · 막힌 빈 원문 수 · 지연(ms) · 걸린 term id · 사람 판정(등급 — 비어 있을 수 있음). **원문 · 번역 · 문장 · FAIL 문구 0** · 키 · 토큰 0.
- 원문 · 번역이 든 원본 결과는 **로컬 전용**(목록과 같은 폴더 · git 제외) — 사람 판정용.
- **전후 비교 표**(보고 · 이 절 「6차 결과」): 절마다 A · B · C 의 기계 FAIL 수 / **기계 판정이 있는 문장 수**(규칙 ④ 만 있는 문장은 뺀다 — 그 수도 적는다) · 사람 판정 등급별 수 · 3절 조각 수 · 지연 중앙값, 그리고 **C 에서 기계 FAIL 이 남은 번호 목록**(번호만)과 번호마다 원인 갈래(시드 · `text` · 끊김 · 인식 · 모델).
- **완료 조건(D-44)**: A · C 가 같은 음성 파일로 끝까지 돌았고 · 비교 표가 나왔고 · C 에 남은 FAIL 번호마다 원인 갈래와 처분(더 고침 · 안고 감 · 다음 판)이 붙었다. **「몇 개 이상 통과」 같은 기준 수치는 DEC 에 없다** — 판정은 코디 · 사용자(⑳ 과 같은 방식).
- 3절이 B · C 에서도 조각나면(조각 수 > 0) 조각 수 · 지연을 코디 · 사용자에게 올린다(OQ-027 — 덜 끊는 쪽 · 값은 사용자가 실물에서).

**6차 결과 — WP22(2026-11-14) · WP24(2026-11-15)** — 조합 A · B(시드 `2026-10-27.6`) · C · C2(시드 `2026-11-14.7` · 문안 424 · 막기 켬 · 한도 = 「D-56 표」). 같은 음성 파일(T01 ~ T33 해시 33개 같음) · 같은 규칙 파일 · 오류 행 0 · 막힌 빈 원문 0(네 조합 모두). **바로잡기(§5.12)는 없던 코드다.** 결과 파일(번호 · 판정 · 수치만) `orchestration/work/interpreter-idea/{wp22-A,wp22-B,wp24-C,wp24-C2,wp24-C-guest,wp24-C2-guest}.json` · 사람 판정 `wp22-human.json` · `wp24-human.json`.

| # | 결과 | 판정 |
|---|---|---|
| ㉒ | (WP23) v6 ⑬′ 재측정 → §4.6 「D-56 표」 · 「D-54 절차의 결과」 / (WP24 · D-56 값) 7개 언어 거절 0 · 줄이기 0 · `text` 424 | 통과 → **D-56** |
| ㉓ | 조합 A · B — 33문장 × 2 · 오류 0 · 막힌 빈 원문 0 · `text` 0 | 통과 |
| ㉔ | 울쎄라 원인 가르기 8칸 — v5 는 별칭 짝이 있으면 영문 상표를 그대로 · 짝을 빼면 다른 영문 약어 / v6 는 짝과 무관하게 새 영문 음역. 어느 칸에서도 zh 사전 이름은 나오지 않았다 | 기록 → zh 별칭 `Ultherapy` 뺌(§4.2.4 E7 · 처분 §8) · 남은 것은 **D-58** |
| ㉕ | 조합 C · C2 — T01 ~ T33 + 손님 쪽 T34 ~ T54 · 오류 0 | 통과 — 아래 표 |

**기계 FAIL 수 — 절별**(기계 판정이 있는 문장 30 · 규칙 ④ 만 있는 문장 3 은 뺌)

| 절 | 판정 있는 문장 | A | B | C | C2 | C · C2 에 남은 번호 |
|---|---|---|---|---|---|---|
| 1 시술명 | 9 | 5 | 3 | 2 | 2 | T03 · T07 |
| 2 손님에게 하는 말 | 11 | 6 | 1 | 1 | 1 | T18 |
| 3 끊김 | 4 | 2 | 2 | 2 | 2 | T23 · T24 |
| 4 인식 | 3 | 0 | 0 | 0 | 0 | — |
| 5 사전 겹침 · 오류 값 | 3 | 2 | 1 | 1 | 1 | T30 |
| **합** | **30** | **15** | **7** | **6** | **6** | |

**사람 판정 — 등급별 수**(T01 ~ T33 · 코디)

| 조합 | 좋음 | 어색 | 오역 | 인식 | 빈값 |
|---|---|---|---|---|---|
| A | 13 | 5 | 12 | 3 | 0 |
| B | 20 | 2 | 7 | 4 | 0 |
| C | 21 | 2 | 6 | 4 | 0 |
| C2 | 21 | 2 | 6 | 4 | 0 |

**3절 — 확정 발화 수 · 조각 수(실제 − 기대) · 지연(ms)**

| # | 기대 | A | B | C | C2 |
|---|---|---|---|---|---|
| T23 | 1 | 2 · +1 · 1,739 | 2 · +1 · 2,063 | 2 · +1 · 2,226 | 2 · +1 · 3,144 |
| T24 | 1 | 3 · +2 · 442 | 3 · +2 · 420 | 3 · +2 · 449 | 3 · +2 · 420 |
| T25 | 1 | 2 · +1 · 1,499 | 2 · +1 · 1,819 | 2 · +1 · 1,845 | 2 · +1 · 2,880 |
| T26 | 2 | 2 · 0 · 1,615 | 2 · 0 · 499 | 2 · 0 · 477 | 2 · 0 · 500 |

- 조각 수 합 = **4**(네 조합 모두). 지연 중앙값(확정 발화가 있는 문장) A 1,579.5 · B 516 · C 544.5 · C2 510 ms.
- **D-55 결과 — C2(끊김 2000)는 C 와 조각 수 · 기계 판정(같은 번호 6) · 사람 판정(등급별 수)이 같고 T23 · T25 의 지연만 900 ~ 1,000 ms 늘었다** → `max_endpoint_delay_ms` **1000 유지**(§5.10 · OQ-027 닫음). 1회 실행 결과다.

**손님 쪽(외 → 한) T34 ~ T54 — 21문장**(C · C2 같음 · 지연 중앙값 C 704 · C2 733 ms)

| 언어 | 기계 통과 | 걸린 번호 | 걸린 term | 사람 판정 |
|---|---|---|---|---|
| en | 2 / 3 | T34 | ph-121 | 인식 |
| ja · zh · zh-Hant · yue | 3 / 3 씩 | — | — | 좋음 |
| th | 2 / 3 | T46 | ph-121 | 오역 |
| vi | 2 / 3 | T49 | ph-121 | 인식 |
| **합** | **18 / 21** | | | 좋음 18 · 오역 1 · 인식 2 |

**남은 것 — 번호 · 갈래 · 처분**(C 기준 · 기계 FAIL 과 사람 판정 「오역 · 인식 · 어색」 을 합친 것)

| 번호 | 무엇(사람 판정) | 갈래 | 처분 |
|---|---|---|---|
| T02 · T03 | 울쎄라 zh — 새 영문 음역(T02 는 기계 pass · 사람 오역) · T03 써마지 zh — 영문 | 모델(짝은 context 에 있음) | **더 고침 — 바로잡기**(D-58 · §5.12 · 틀린 꼴 §4.2.5) |
| T04 | 스컬트라 zh — 다른 뜻의 낱말(기계 pass · 사람 오역) | 모델 | **더 고침 — 바로잡기** |
| T30 | 보툴렉스 zh — 영문 음역(B 는 사전 이름 · C 에서 나빠짐) | 모델 | **더 고침 — 바로잡기** |
| T46 | 울쎄라 th(손님 쪽) — 현지 이름은 들었는데 한국어 번역이 다른 시술로 | 모델 | **안고 감 — 실패로 남긴다**(0.9.1 · 처분 §11): 나온 낱말이 일상 한국어 낱말(다른 시술 · 장비 이름)이라 `ko_wrong` 에 넣지 않는다 · 바로잡기 「못 찾음」 로그로 계속 본다 |
| T34 · T49 | 울쎄라 en · vi(손님 쪽) — 영문 상표를 STT 가 다른 낱말로 들음 | 인식 | 안고 감 — 바로잡기 대상 아님(원문에 term 이 안 걸림) · OQ-017 |
| T23 · T24 | 3절 조각(T23 어색 · T24 인식) | 끊김 · T24 는 원문 인식(한국어 STT)도 | 안고 감 — 끊김 값을 올려도 같음(D-55) · T24 인식은 아래 줄 |
| T07 | 기계 FAIL · 사람 좋음 | 규칙(규칙 13 헛걸림 — 처분 §8) | 규칙 파일은 고정 · 사람 판정으로 읽음 |
| T08 | 인식(사람) | 모델 — v6 가 문장 끝 문장부호를 글자로 받아씀 | 7차 결과를 보고 — 자주 나오면 바로잡기와 같은 자리에서 걸러 내는 작은 수정(다음 판 · 처분 §10) |
| T09 · T20 · T24 | 인식(사람) | 원문 인식(한국어 STT) | 이번 판 범위 밖 — 사전 · 바로잡기로 못 고친다. 기록으로 계속 본다(처분 §10) |
| T13 | 어색 | 일반 낱말 옮김(뜻은 통함) | 그대로(처분 §10) |
| T18 | 오역(기계 FAIL) | 일반 낱말 옮김(시술 부위 표시를 가리키는 말) | 7차에 그대로 두고 본다 · 일반 낱말 짝은 넣지 않는다(D-45 · 처분 §10) |
| T31 | 오역 | 사전 — 그 증상 낱말의 term 이 없다 | 다음 판 사전 후보(처분 §10) |

- B → C 에서 풀린 것 = T01 · T32(시드 `.7` — 토닝 zh · ja). A → C 로 기계 FAIL 15 → 6 · 사람 판정 오역 12 → 6 · 좋음 13 → 21.
- **남은 번호마다 갈래 · 처분이 붙었다**(0.9.1 — 처분 문서 `quality-research-dispositions.md` §8 · §10 · §11) — D-44 의 완료 조건(A · C 가 같은 음성으로 끝까지 · 비교 표 · 남은 FAIL 마다 원인 갈래와 처분)이 문서에서 닫힌다.
- 6차의 전후 비교(A 대 C)는 여기서 끝이다 — **이전 조합은 다시 돌리지 않는다**(D-59). 바로잡기와 나머지 언어는 7차가 본다.

**7차 — 나라별 시험(0.9.0 · D-57 · D-59 · WORK WP27)** — 7개 언어 × 직원 쪽 · 손님 쪽 · **최종 버전 하나만**.

> 6차의 33문장은 zh · en · ja 뿐이고 손님 쪽은 언어마다 3문장이라, 7개 언어 사전 보정(D-46)을 다 보지 못했다. 7차는 **언어(나라)마다 같은 시술 목록**을 직원 쪽 · 손님 쪽으로 돌린다. **이전 조합(A · B · C · C2)은 7차에서 돌리지 않는다** — 전후 개선은 6차(A 대 C)로 확인했다(D-59 · 사용자 2026-11-15). 6차의 T01 ~ T54 · 규칙 파일 · 결과는 **그대로 둔다**(고치지 않는다) — 7차는 그것을 넓히는 새 묶음이다. 이 문서에는 문장을 쓰지 않는다(번호 · 시술 · 판정 규칙만).

**최종 버전** = 운영 기본값 전부 — `stt-rt-v6` · 시드 `.8`(§4.2.5) · 문안 · 빈 원문 막기 · 끊김 1000 · 한도 「D-56 표」 · **시술명 바로잡기 켬**(§5.12). 시험 스크립트는 조합 인자를 하나도 주지 않는다(§9.3 「조합」 표의 기본값 칸 · 통역 API 와 같은 길). WP26 이 끝난 코드 위에서 돈다. **(0.9.2) 실제로는 시드 `.9`(D-61 — 첫 실행) · `.10`(7차 다시 · 손님 쪽 다시)에서 돌았다** — 아래 「시드 `.8`」 로 적힌 자리(손님 쪽 문장의 `name` · 규칙 파일을 만드는 시드)는 **그 실행의 시드 판**으로 읽는다(「7차 결과」 의 실행 표).

**시술 목록 — 9개**(D-59 · 언어마다 같다)

| 순번 | 시술(ko 대표명) | term |
|---|---|---|
| 1 | 토닝 | ph-012 |
| 2 | 울쎄라 | ph-121 |
| 3 | 써마지 | kr-014 |
| 4 | 스컬트라 | ph-112 |
| 5 | 쥬베룩 | ph-108 |
| 6 | 리투오 | kr-015 |
| 7 | 보툴렉스 | ph-042 |
| 8 | 보톡스 | ph-033 |
| 9 | 필러 | ph-003 |

**문장 — 언어마다 28행 · 7개 언어 = 196행**

| 쪽 | 번호 | 수 | 무엇 | 음성 |
|---|---|---|---|---|
| **직원 쪽**(한 → 외) | `S01` ~ `S10` | 10 | **D-57 다국어 묶음** — 6차의 T01 · T02 · T03 · T04 · T05 · T06 · T11 · T12 · T13 · T16(이 순서) | **6차에서 만든 한국어 음성 그대로**(해시 대조 · 다시 합성하지 않는다) — 7개 언어 세션에 같은 파일 |
| | `S11` ~ `S19` | 9 | **시술명 문장** — 위 시술 9개를 **하나씩** 든 한국어 문장(직원이 손님에게 할 법한 말 · 지어낸 문장 · ko 대표명 그대로) | 새로 합성(`ko`) — 문장마다 파일 하나 · 7개 언어 세션에 같은 파일 |
| **손님 쪽**(외 → 한) | `G01` ~ `G09` | 9 | 그 언어 문장 — 위 시술 9개를 **하나씩** · **시드 `.8` 의 그 언어 `name` 으로 말한다**(손님이 할 법한 말 · 지어낸 문장 · 실제 기록 문장 아님) | 언어마다 새로 합성 — 합성 언어 = 그 언어의 Soniox 코드(zh-Hant · yue 는 문장을 간체로 바꿔 `zh` · 6차 손님 쪽과 같음) |

- 행 이름 = `<lang>-<번호>`(예 `th-S12` · `yue-G03`). 세션 `start` 의 `lang` = 그 언어(앱 lang · zh-Hant · yue 그대로) · 행마다 새 세션 · 실시간 속도 재생 · 무음 꼬리(6차 「입력」 표 그대로).
- 목록 파일(문장) · 규칙 파일 · 음성 · 원본 결과는 **로컬 전용**(`reference/2026-11-12-interpreter-idea/` — git 제외 · DEC OQ-021). 6차 파일(`test-sentences.md` · `test-rules.json`)을 고치지 않고 **7차 파일을 따로** 둔다.
- 손님 쪽 문장은 backend 가 초안을 짓고(문장마다 그 언어 `name` 이 글자 그대로 들었는지 기계 확인) **코디 확인 뒤** 돌린다(6차 손님 쪽과 같은 순서).
- 직원 쪽 `S01` ~ `S10` 은 6차 문장이라 시술이 겹치거나(T03 = 울쎄라 + 써마지) 없는 문장(T06 · T11 ~ T16)이 섞여 있다 — `S11` ~ `S19` 가 9개 시술을 빠짐없이 하나씩 본다.

**판정 — 사전에서 자동**(규칙 파일은 **스크립트가 시드 `.8` 에서 만든다** — 손으로 짓지 않는다 · 규칙 종류는 6차의 넷 그대로)

| 쪽 | 기계 판정 | 규칙 |
|---|---|---|
| 직원 쪽 — 시술명이 든 행(`S01` ~ `S05` · `S11` ~ `S19`) | 문장 속 ko 대표명**마다**, 그 언어 번역에 그 term 의 `entries[L].name` 또는 `aliases` 가운데 **하나도 없으면 FAIL** | ① 글자 그대로 · 걸리는 쪽 「없으면」 · 찾을 쪽 = 번역 · 찾는 법 = §5.9 「나타난다」(zh-Hant · yue 는 양쪽 `t2s` · `casefold` · 라틴 경계). 문장 ↔ term 대응은 목록 파일에 적는다(`S01` 토닝 · `S02` 울쎄라 · `S03` 울쎄라 + 써마지 · `S04` 스컬트라 + 쥬베룩 + 리투오 · `S05` 보톡스 · `S11` ~ `S19` = 순번 1 ~ 9) |
| 직원 쪽 — `S06` ~ `S10`(T06 · T11 · T12 · T13 · T16) | **기계 판정 없음** | ④ — 사람이 본다(시술 뉘앙스 · 손님에게 하는 말) |
| 손님 쪽 `G01` ~ `G09` | 한국어 번역에 **기대 ko 대표명**(또는 그 term 의 ko 별칭)이 없으면 FAIL | ① 「없으면」 · 찾을 쪽 = 번역. **기대 ko 대표명 = 그 `name` 의 역방향 첫 짝의 ko**(§4.5 — 다른 시술과 현지명이 같으면 처음 짝만 남는다 · 그 경우 기대 term 이 표의 term 과 다를 수 있다 — 규칙 스크립트가 조립 결과에서 뽑고, 다른 칸은 결과에 「겹침」 으로 적는다) |
| 모두 | 확정 발화 수 | ③ — 기대 = 1(쉼 없는 한 문장) |

- **바로잡기 표시** — 행마다 기록 판정과 같은 값으로 `fixed`(바로잡은 term) · 못 찾은 term 을 같이 남긴다. 그래서 시술명 칸은 넷 중 하나다: **번역 그대로 사전 이름** · **바로잡아서 사전 이름** · **안 나옴(못 찾음)** · **원문에 term 이 안 걸림(인식)**.
- **사람 판정** — 코디가 로컬 결과 페이지에서 행마다 6차와 같은 다섯 등급(좋음 · 어색 · 오역 · 인식 · 빈값). 「바로잡아서 사전 이름」 인 행은 **잘못 바꾼 것이 아닌지**(§5.12 「한계」)를 같이 본다. 원어민 확인은 완료 조건이 아니다(오면 OQ-017 에).
- 판정이 실행마다 갈리는 행은 다시 돌린 횟수와 결과를 적는다(Soniox 출력은 결정적이지 않다).

**결과**

| 무엇 | 계약 |
|---|---|
| **결과 페이지 — 언어별 탭**(D-59) | **HTML 파일 하나 · 로컬 전용**(원문 · 번역이 든다 — git 제외 폴더 `reference/2026-11-12-interpreter-idea/quality-run/` · 레포 · PR · 보고에 붙이지 않는다) · 밖으로 요청 0(파일만으로 열린다). **탭 7개 = 언어**(§5.5 표 순서 en · ja · zh · zh-Hant · th · vi · yue) · 탭마다 **직원 쪽 표 · 손님 쪽 표** — 행 = 번호 · 시술 · 원문 · 번역 · 기계 판정 · 바로잡기 표시(위 넷) · 사람 판정 · 탭 머리에 그 언어 수치(아래 표의 한 줄). **조합 비교 칸은 없다** — 최종 버전 결과 하나만 |
| 레포용 JSON | `orchestration/work/<slug>/` — 행마다 번호 · 언어 · 쪽 · term id · 기계 판정 · 걸린 규칙 번호 · 확정 발화 수 · `fixed` · 못 찾은 term · 지연(ms) · 사람 판정(등급). **원문 · 번역 · 문장 · 틀린 꼴 0** · 음성 해시 · 시드 판 · 설정(모델 · `text` 글자 수 · 한도) |
| 언어별 표(보고 · 이 절 「7차 결과」) | 언어 7줄 × (직원 쪽 기계 FAIL / 판정 있는 수 · 손님 쪽 기계 FAIL / 9 · 바로잡은 칸 수 · 못 찾은 칸 수 · 원문에 안 걸린 칸 수 · 사람 판정 등급별 수) + 남은 FAIL 의 번호 · term · 갈래 |

**실물 번호 · 통과 조건**

| # | 무엇 | 통과 조건 · 기록 |
|---|---|---|
| ㉖ | **바로잡기 실물**(WP26) — §4.2.5 표의 칸(T02 · T03 · T04 · T30)과 **T46**(0.9.1 — 목록에 넣지 않은 칸 · 「못 찾음」 으로 남는지 본다)을 **6차와 같은 음성**으로 최종 버전에서 1회씩 | 오류 0 · 번호마다 기계 판정 · `fixed` · 못 찾은 term · TTS 입력에 사전 이름이 들었는지(참 · 거짓) — 번호 · 판정만. T46 은 `fixed` 없음 · 못 찾은 term = ph-121 이 기대다(바뀌면 무엇으로 바뀌었는지 단계만 보고). 못 찾은 칸이 있으면 그 꼴을 로컬 대조표에 더해 코디에게(§4.2.5 「뒤에 더할 때」) · 7개 언어 연결 1회씩 — 거절 0 · 글자 수 = 「D-56 표」(시드 `.8` 이 context 를 바꾸지 않았다는 확인) |
| ㉗ | **7차 나라별 시험**(WP27) — 196행 · 최종 버전 | 오류 없이 끝남 · 결과 페이지(언어별 탭) · 레포용 JSON · 언어별 표 · 남은 FAIL 마다 갈래와 처분(더 고침 = 틀린 꼴 추가 · 안고 감 · 다음 판). **「몇 개 이상 통과」 같은 기준 수치는 DEC 에 없다** — 판정은 코디 · 사용자(6차와 같은 방식) |

- **D-57 의 「조합 A · C」 실행은 D-59 로 바뀌었다** — 다국어 묶음 10문장은 7차 `S01` ~ `S10` 으로 최종 버전에서만 돈다. 그 전에 A · C 로 돌린 결과가 있으면 참고 기록으로만 둔다(7차 판정에 쓰지 않는다).
- 7차에서 새 틀린 꼴이 나오면 시드에 더하고(§4.2.5 절차 · `version` 올림) **그 칸만** 다시 돌린다 — 다시 돌린 횟수를 적는다.

**7차 결과 — WP27(2026-11-15)** — 196행 · 최종 버전(조합 인자 없음) · 세 번 돌았고, 그 뒤 ④ 를 좁힌 코드(D-65 · D-66)로 **저장 결과를 다시 보았다**(Soniox 를 다시 부르지 않음). 결과 파일(번호 · 판정 · 수치 · term id 만): `orchestration/work/interpreter-idea/test7-result.json` · `test7b-result.json` · `test7c-result.json` · 보고 `wp27-be-report.md`. 원문 · 번역 · 결과 페이지 · 사람 판정 파일은 로컬 전용(`reference/2026-11-12-interpreter-idea/quality-run/` — git 제외). **이 절에는 문장 · 틀린 꼴을 쓰지 않는다.**

| 실행 | 시드 | 코드 | 돌린 행 | 기계 pass / 196 | 바로잡은 행 | 못 찾음 행 | 오류 · 조각 | 지연 중앙값 |
|---|---|---|---|---|---|---|---|---|
| 7차(`test7`) | `.9` | WP26 | 196 | 146(직원 쪽 112 / 133 · 손님 쪽 34 / 63) | 30 | 29 | 0 · 0 | 547 ms |
| 7차 다시(`test7b`) | `.10` | + D-63 | 196 | 149(115 · 34) | 34 | 28 | 0 · 0 | 548.5 ms |
| 손님 쪽 다시(`test7c`) | `.10` | + D-64 | 손님 쪽 63(직원 쪽 133 은 `test7b` 그대로 합침) | 153(115 · 38) | 38 | 24 | 0 · 0 | 732 ms(손님 쪽 63) |
| **저장 결과 다시 봄(0.9.3 — 지금 결과)** | `.10` | + D-65 · D-66 | 실행 0 — `test7c` 손님 쪽 63행의 바꾸기 전 번역에 새 함수를 돌려 같은 규칙으로 다시 판정 | **152(115 · 37)** | **37** | **25** | — | — |

- 같은 목록 · 같은 음성(해시 대조 — 직원 쪽 `S01` ~ `S10` 은 6차 파일 10개 · 새로 합성 72개) · 규칙은 실행의 시드 판에서 스크립트가 만듦(196행 · 규칙 427). `S06` ~ `S10` 은 「발화 수 1」 규칙만 있어 기계 pass 로 잡힌다 — 뜻 · 말투는 사람 판정이다. **기계 FAIL 은 모두 시술명 규칙에서 났다**(발화 수 FAIL 0).
- 실행 사이에 달라진 행(번호만): **7차 → 7차 다시** — fail → pass 4(zh-S16 · zh-Hant-S04 · th-S13 · yue-S16 — 시드 `.10` 의 새 틀린 꼴 ① ) · pass → fail 1(zh-Hant-S01 — Soniox 가 다른 번역을 냄 · 코드와 무관한 실행마다 갈림) · 바로잡기만 달라진 행 2(ja-S01 — D-63 으로 안 바뀜 · 판정은 pass 그대로 / th-S03 — 한 term 은 바로잡히고 다른 term 은 못 찾음 그대로). **7차 다시 → 손님 쪽 다시** — fail → pass 4(ja-G04 · zh-G03 · zh-Hant-G07 · th-G05 — 모두 ④ 단계) · pass → fail 0. **손님 쪽 다시 → 저장 결과 다시 봄(D-65)** — pass → fail 1(**zh-G03** · kr-014 — 번역의 꼴이 대표명과 **첫 음절이 달라** 이제 안 바꾼다) · 나머지 62행은 같은 글 · D-66 으로는 바뀌는 행 0. 레포용 JSON 은 `test7c-result.json` 까지다(다시 본 결과는 `wp27-be-report.md` 수정 3 · 4 의 수치 · 비교 원본은 로컬).

**언어별 표(지금 결과 = `test7c` 에 「저장 결과 다시 봄」 을 반영 · 시드 `.10` · 0.9.3)**

| 언어 | 직원 쪽 기계 pass / fail(19) | 손님 쪽 기계 pass / fail(9) | 바로잡은 행 | 못 찾음 행 | 기계 FAIL 행의 갈래 — 못 찾음 · 인식 | 사람 판정(28) — 좋음 · 어색 · 오역 · 인식 |
|---|---|---|---|---|---|---|
| en | 18 / 1 | 5 / 4 | 4 | 4 | 1 · 4 | 21 · 1 · 1 · 5 |
| ja | 17 / 2 | 6 / 3 | 3 | 4 | 3 · 2 | 22 · 4 · 1 · 1 |
| zh | 17 / 2 | **4 / 5** | **6** | **3** | **3** · 4 | 18 · 4 · 2 · 4 |
| zh-Hant | 15 / 4 | 6 / 3 | 6 | 4 | 4 · 3 | 17 · 5 · 4 · 2 |
| th | 12 / 7 | 5 / 4 | 4 | 8 | 8 · 3 | 15 · 7 · 4 · 2 |
| vi | 18 / 1 | 4 / 5 | 6 | 1 | 1 · 5 | 18 · 2 · 2 · 6 |
| yue | 18 / 1 | 7 / 2 | 8 | 1 | 1 · 2 | 19 · 4 · 1 · 4 |
| **합** | **115 / 18** | **37 / 26** | **37** | **25** | **21 · 23** | **130 · 27 · 15 · 24** |

- **읽는 법**: 「바로잡은 행」 = `fixed` 가 비지 않은 행(37행 · term 39 — 그중 **35행이 기계 pass**) · 「못 찾음 행」 = 못 찾은 term 이 하나라도 있는 행(기계 pass 인 행도 든다 — 판정 대상이 아닌 term 이 못 찾음인 경우). 「갈래」 는 기계 FAIL 44행을 행 단위로 나눈 것 — **못 찾음** = 원문에 그 term 이 걸렸는데 번역에 사전 이름 · 바꿀 꼴이 없음 / **인식** = 원문에 그 term 이 안 걸림(STT 가 시술명을 다른 말로 들음 — 바로잡기 대상 아님 · §5.12 「한계」).
- **사람 판정**(코디 · 6차와 같은 등급 · 빈값 0) — 196행: **좋음 130 · 어색 27 · 오역 15 · 인식 24**. 쪽별: 직원 쪽 133 = 좋음 97 · 어색 21 · 오역 12 · 인식 3 / 손님 쪽 63 = 좋음 33 · 어색 6 · 오역 3 · 인식 21. **이 등급은 `test7c`(D-64) 때의 글에 매긴 것이다 — zh-G03 은 0.9.3 에서 바로잡기 전 글로 돌아가는데 다시 매기지 않았다**(그 글은 7차 다시와 같다 — 그때 zh 손님 쪽 등급 수는 오역 1 · 어색 0 이었고 지금 표는 오역 0 · 어색 1 이다 · 한 행 차이). 등급 수의 원천은 로컬 `test7c-human.js`(레포용 JSON 에는 사람 판정 칸이 아직 없다 — 「결과」 표의 계약과 다른 자리 · 미결로 보고).
- **바로잡기 단계**(OQ-032 재료): 7차 첫 실행 — 바로잡은 term 32 = **① 26 · ② 6 · ③ 0**. 사람 판정 「잘못 바꿈」 **1**(ja 직원 쪽 · ② — D-63 으로 닫음 · 7차 다시에서 그 칸은 안 바뀜). 손님 쪽 다시 — **④ 로 바뀐 행 4 · 모두 fail → pass** · 잘못 바꾼 것 0. **0.9.3(D-65 · D-66) — ④ 로 바뀌는 행은 3**(ja-G04 · zh-Hant-G07 · th-G05)이다. **③(가까운 라틴 낱말)으로 바뀐 칸은 7차에서 0 이다** — 기준 숫자(4 · 2)를 고칠 근거는 나오지 않았다.

**남은 기계 FAIL 44행 — 번호 · term · 갈래**(지금 결과 · 0.9.3)

| 언어 | 못 찾음(원문은 걸림 · 번역에 사전 이름 없음) | 인식(원문에 안 걸림) |
|---|---|---|
| en | G03 kr-014 | S17 ph-042 · G02 ph-121 · G04 ph-112 · G07 ph-042 |
| ja | S11 ph-012 · G02 ph-121 · G09 ph-003 | S17 ph-042 · G07 ph-042 |
| zh | S04 ph-112 · S14 ph-112 · **G03 kr-014**(0.9.3) | G01 ph-012 · G02 ph-121 · G04 ph-112 · G06 kr-015 |
| zh-Hant | S01 ph-012 · S11 ph-012 · S19 ph-003 · G05 ph-108 | S17 ph-042 · G04 ph-112 · G06 kr-015 |
| th | S01 ph-012 · S03 kr-014 · S04 ph-108 · kr-015 · S11 ph-012 · S15 ph-108 · S16 kr-015 · G02 ph-121 · G07 ph-042 | S17 ph-042 · G03 kr-014 · G06 kr-015 |
| vi | S19 ph-003 | G02 ph-121 · G03 kr-014 · G04 ph-112 · G06 kr-015 · G07 ph-042 |
| yue | S14 ph-112 | G06 kr-015 · G07 ph-042 |

**남은 실패 갈래 · 처분**(D-63 ~ D-66 · 처분 §16 — 사용자 2026-11-15 「이거 까지만 하자」 · 「진행하자」)

| 갈래 | 행 수 | 어디 | 처분 |
|---|---|---|---|
| **인식 — 손님 쪽**(외국어 음성의 시술명을 STT 가 다른 말로 들음) | 19 | 7개 언어 손님 쪽 — en · vi 에 9행 · 나머지 5개 언어에 10행(「현지 표기 없음」 칸 = 영문 이름으로 말하는 칸이 든다) · 리투오 5 · 보툴렉스 4 · 스컬트라 4 · 울쎄라 3 · 써마지 2 · 토닝 1 | **안고 감** — 바로잡기 대상이 아니다. 음성이 합성이다(영문 상표를 그 언어 음성으로) — **사람 목소리 확인은 OQ-017 그대로** |
| **인식 — 직원 쪽 `S17`**(한국어 음성의 보툴렉스) | 4 | en · ja · zh-Hant · th(같은 한국어 음성 — zh · vi · yue 세션에서는 걸렸다) | **안고 감 · 다음 판** — 세션 언어에 따라 한국어 받아쓰기가 갈린다. th · ja 는 `terms` 가 줄이기로 빠지는 언어지만(D-62) en · zh-Hant 는 줄이기 0 이라 그것만으로 설명되지 않는다 — 운영 기록으로 다시 본다 |
| **못 찾음 — th 직원 쪽 · 손님 쪽** | 8 | th — 토닝 · 써마지 · 쥬베룩 · 리투오 · 울쎄라 · 보툴렉스 | **안고 감 · 다음 판 사전 후보** — 시드에 바꿀 꼴이 없다(backend 보고: 번역이 태국 글자로 다른 표기를 냈을 가능성 — 로컬 결과로 확인할 일). 그 칸의 `name` 이 영문인 곳(리투오)은 태국 글자 음역을 틀린 꼴로 넣지 않는다(§4.2.7 ⓑ — D-61 과 반대) · 나머지는 운영 로그 「못 찾음」 · 기록으로 꼴을 모아 다음 시드 판에 |
| **못 찾음 — 그 밖 6개 언어** | 13 | ja 3 · zh-Hant 4 · zh 3 · en 1 · vi 1 · yue 1 — 토닝 · 필러 · 스컬트라 · 울쎄라 · 쥬베룩 · 써마지 | **안고 감** — 시드 · 규칙에 바꿀 꼴이 없는 칸이다(zh 스컬트라 2행은 §4.2.5 에서 뺀 T04 칸 — 처분 §14 W-1 · 일상 낱말은 틀린 꼴로 넣지 않는다 — 처분 §16). 로그 「못 찾음」 · 기록으로 계속 본다 |
| **외 → 한 — 대표명과 두 군데 이상 다른 꼴** | (위 못 찾음 · 사람 판정에 들어 있음) | 손님 쪽 | **안고 감** — D-64 는 「음절 하나만」 이고 D-65 는 첫 음절이 같을 때만이다(zh-G03 이 그 예). **넓히지 않는다(D-66 · OQ-033 닫힘)** |
| **사람 판정 오역 15 · 어색 27**(시술명 말고 뜻 · 말투) | — | zh-Hant · th 에 많다(오역 4 · 4 · 어색 5 · 7) | 바로잡기 범위 밖(§5.12 「한계」) — 문안 · 사전으로 풀 일인지는 운영 기록을 본 뒤 |

- 「겹침」 칸(zh-G07 · zh-Hant-G07 — 보툴렉스가 그 언어 `name` 을 ph-031 과 같이 가져 기대 ko 가 그 term 이다): zh pass · zh-Hant 는 손님 쪽 다시에서 ④ 로 pass.
- **㉗ 통과 조건**: 오류 없이 끝남 ○ · 결과 페이지(언어별 탭 7 · 로컬) ○ · 레포용 JSON ○ · 언어별 표 ○ · 남은 FAIL 마다 갈래와 처분 ○(위 · 0.9.3 — 152 / 196). 「몇 개 이상 통과」 기준은 없다 — **사용자 확인 끝(2026-11-15 「진행하자」)** → 배포(WP25 · §9.6 0.9.2).
- 실행은 조건마다 1회다(Soniox 출력은 결정적이지 않다 — zh-Hant-S01 이 그 예). 다시 돌린 것은 위 실행 표의 둘(전체 1회 · 손님 쪽 1회)뿐이다.

### 9.4 로컬 E2E (사용자 · D-12)

맥 브라우저 `http://localhost:3800` — 시안과 같은 모양(§9.2) · 로그인(데모 켬 · 끔 둘 다) · 언어 7개 고르기(뒤집힌 목록) · 한국어 ↔ 외국어 실발화 · 말풍선 좌우(D-24) · 자동 스크롤 · 「↓ 최신」(D-25) · 원 상태 8개 · 원 위아래 안내(D-22) · 멈춤 → 초기화(D-29) · 시작 오버레이 언어 단추 7개(D-34) · 백그라운드 복귀 · 뒤집힘 아이콘 · 출력 중 마이크 막힘 · 출력 중 멈춤 뒤 소리 안 남(FAIL-1) · 외국어 발화의 시술명이 한국어 대표명으로(D-18) · 대만어 자막 대만식(0.5.0 · D-35 — 「雷射」 · 「離子導入」) · **대만 현지명(美國音波 · 鳳凰電波) 양방향**(D-35 · OQ-017) · **누르고 말하기 — 모드 전환 · 누르는 동안만 듣기 · 뗌 → 번역 · TTS 중 누름 → 재생 멈춤 · 주변 소리 안 들어감**(D-36) · **메뉴 = 로그아웃 하나**(D-37) · **멈춤 35초 뒤 다시 말해도 안 끊김**(§5.8) · 로그아웃 · 401 처리. (0.5.0 — 「용어집 모달」 항목은 지움)

### 9.5 배포 뒤 (D-12 · D-26)

- 주소 **`https://tongky.medisolveai.xyz`** — 한 호스트 · `/api` → back(WS `/api/interpret` 포함) · 나머지 → front(D-26). k8s_infra_mac · 네임스페이스 `interpret-pwa-prod` · 이미지 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>`(Actions · arm64 · main 빌드만) · ArgoCD 수동 sync. front 빌드 `NEXT_PUBLIC_API_BASE_URL` = 배포 주소.
- 배포 주소(HTTPS)에서: 로그인(운영은 데모 켬 — D-30) · `wss` 통역 실발화 1회 · 유휴 2분 안 끊김(ingress WS 업그레이드 · 시간 초과 3600) · 휴대폰 홈 화면 추가 · standalone 실행 · 마이크 · 화면 꺼짐 방지 · **로그인 포커스 확대 없음(D-27) · 언어 목록 터치(D-31)** · **(0.5.0) iPhone 길게 누름 — 텍스트 선택 · 확대 · 콘텍스트 메뉴 없음 · 손가락이 원 밖으로 미끄러져도 뗄 때까지 유지(D-36)** · **최소 노출 — `/api/health` · `/api/auth/me` `{ok}` · `/api/glossary` · `/docs` · `/openapi.json` 404(D-37)**.
- 비밀값(`SONIOX_API_KEY` · 로그인 아이디 · 비밀번호 · 세션 비밀값 · `INTERPRET_DEMO_LOGIN`)은 클러스터 Secret 에만. **0.4.0 — 운영 ConfigMap · Secret 이름 목록에서 `GLOSSARY_MATRIX_URL` 을 지운다**(infra 차트 · `provisioning/secrets/*.env.example`).
- **시드를 고치면**: 시드 PR 머지 → main 이미지 → infra `values-prod` 태그 → sync(back 재시작) — 데이터만 고쳐도 재배포다(D-33 「git · PR 로 고친다」).

**배포 기록 (0.6.1 — 코디 확인 · 지금 back 17c26b5 · front fe8475e)**

| 판 | 코드(kknaksss/interpret-pwa) | infra(MediSolveAIDev/k8s_infra_mac) | 무엇 |
|---|---|---|---|
| 1 | PR #1 → main `046eabe` | PR #25 | 첫 배포 2026-10-26 — `tongky.medisolveai.xyz` · DNS CNAME `tongky` · ns `interpret-pwa-prod` · Secret `interpret-pwa-secret` · pull secret `ghcr-pull` |
| 2 | PR #2 → `4ccf905` | PR #26 | 폰 피드백 1 · 2(D-27 ~ D-30) |
| 3 | PR #3 → `d0a91a7` | PR #27 | 폰 피드백 3(D-31 · D-32) |
| 4 | PR #4 → `9befd18` | PR #28 | 용어집 시드(D-33) · 한도 20251 · `GLOSSARY_MATRIX_URL` 삭제 |
| 5 | PR #5 → `2b4976b` | PR #29(front) | 시작 오버레이 언어 단추 7개(D-34) |
| 6 | PR #6 → `145c872` | PR #30(back) | **운영 끊김 수정**(TTS keepalive · §5.8) · 대만 현지명 시드 `.4` · zh-Hant `s2tw` + 「激光 → 雷射」(D-35) |
| 7 | PR #7 → `10b4c38` | PR #32(front) | 누르고 말하기 모드(D-36 · back 무변경) |
| 8 | PR #8 → `fe8475e` | PR #33 | 최소 노출(D-37) — 용어집 API · 메뉴 삭제 · health/me `{ok}` · 오류 일반 문구 · docs 끔. back · front **같은 sha · 이미지 태그 하나**(5 ~ 7 의 back/front 개별 태그 오버라이드 정리) |
| 9 | PR #9 → **`2a9d5a5`** | PR #34(back) | 대만어 사전 2차(D-38 · 시드 `.5`) — back 만(`back.imageTag` 오버라이드 다시 생김 · front 는 `fe8475e`) |
| 10 | PR #10 → **`17c26b5`** | PR #35(back) | 시드 `.6`(D-39 · D-40 · OQ-018 처분) · 통역 기록(D-41) · 언어별 한도(§4.6) · back PVC `interpret-pwa-records` · `INTERPRET_RECORD_DIR=/data/records` · `lima-worker-1` 고정(§9.6) — back 만(`back.imageTag` · front 는 `fe8475e`) |
| 11 | — | PR #36 | back `resources.requests.cpu` **100m → 50m** — `lima-worker-1`(PVC 고정 노드) CPU 예약 3,950m(98%)라 새 back pod 가 Pending · limit 1 그대로(§9.6) |
| 12 | PR #11 → `e0fbda8` | PR #54 | 통역 기록 보관 기간 env `INTERPRET_RECORD_KEEP_DAYS`(D-42) — 운영 ConfigMap 에 넣지 않음 = 삭제 안 함 · back 만(`back.imageTag`) |

- 반영 방식: Actions(main · arm64 · sha 태그) → infra `values-prod` 이미지 태그 PR → 머지 → ArgoCD **수동 sync**.
- 운영은 **데모 로그인 켬**(`INTERPRET_DEMO_LOGIN=true` — Secret · D-30). 데모가 끝나면 값만 지우고 back 재시작.
- **배포 주소 확인(코디 · 8차)**: `/api/health` · `/api/auth/me` → `{ok}` · `/api/glossary` 404 · `/docs` 404 · `wss /api/interpret` `start` → `ready`. (4차까지: 로그인 200 · manifest `name` 통키 · `short_name` Tongky · 데모 로그인 `demoLogin:true` · `/api/auth/demo` 200.) **사람 목소리 폰 E2E(D-35 대만명 · D-36 길게 누름)는 남음**(OQ-017).

### 9.6 배포 — 통역 기록 PVC (0.6.0 — D-41 · 0.7.0 보관 기간 — D-42 · 선례 cc-prototype `procedure-db`)

**infra 차트 `charts/interpret-pwa`(k8s_infra_mac)** — 지금 back 은 볼륨 없는 무상태(차트 주석 「Stateless (no DB, no volume)」 · `podSecurityContext` 에 `fsGroup` 없음). 아래를 더한다.

| 항목 | 값 | 근거 |
|---|---|---|
| PVC | 이름 **`interpret-pwa-records`** · `ReadWriteOnce` · **`storageClassName: local-path`** · **1Gi** · 주석 `helm.sh/resource-policy: keep`(차트를 지워도 남는다) · 템플릿 `templates/back-pvc.yaml` · 이름 · 크기는 values(`back.recordsPvcName` · `back.recordsStorage` 류) | cc-prototype `back-pvc.yaml`(`procedure-db` · local-path · keep · 1Gi) |
| 크기 근거 | 한 줄 수백 B ~ 수 KB. **0.7.0 — 보관은 무기한**(D-42 · 운영은 삭제 안 함): 운영 실측 **11-11 ~ 11-14 4일에 44KB**(하루 약 11KB — 하루 수십 KB 안쪽) → 이 속도면 1년에 약 4MB · 1Gi 는 그대로 여유(크기 변경 없음). (0.6.0 근거: 시연 규모 · 7일만 보관 → 수 MB · 1Gi 는 선례와 같은 최소 단위) | 실측(코디 2026-11-14) · 기본값 |
| 마운트 | back 컨테이너 `/data` ← PVC · **ConfigMap `INTERPRET_RECORD_DIR=/data/records`**(비밀 아님 · `checksum/config` 로 pod 재시작) — 하위 폴더는 back 이 기동 때 만든다(§5.9) | §2.4 |
| 쓰기 권한 | `podSecurityContext.fsGroup: 10001` 을 더한다(이미지 uid/gid 10001 · `runAsUser` · `runAsGroup` 그대로) | cc-prototype values `fsGroup: 10001` |
| **노드 고정(prod)** | `values-prod.yaml` 에 **`back.nodeSelector: {kubernetes.io/hostname: lima-worker-1}`** · 템플릿에 `nodeSelector` 블록. **local-path 는 `lima-worker-1` 에서만 프로비저닝된다**(local-path-config `nodePathMap`) — WaitForFirstConsumer 라 다른 노드에 잡히면 PVC 가 Pending 으로 남고 back 이 뜨지 않는다 | cc-prototype `values-prod.yaml` 주석(fix1 2026-10-13 — Pending 사고) |
| replicas · 전략 | `replicas: 1` 그대로 · **롤링(기본 RollingUpdate) 그대로** — 새 pod 가 같은 노드(노드 고정)라 RWO 볼륨을 같이 붙일 수 있고, §4.4 「깨진 시드면 readiness 가 안 올라와 옛 pod 가 남는다」 를 지킨다. 겹치는 몇 초 동안 두 pod 가 같은 날짜 파일에 append 할 수 있다 — 줄 단위 append 라 섞이지 않는다(§5.9 「쓰기」). cc-prototype 의 `Recreate` 는 SQLite 단일 쓰기 때문이라 여기는 따르지 않는다 | 기본값 |
| **CPU 예약(0.6.1)** | back `resources.requests.cpu` **50m**(100m 에서 · memory 256Mi · limits cpu 1 · memory 1Gi 그대로). 노드 고정으로 back 은 `lima-worker-1` 에만 뜰 수 있는데 그 노드의 CPU 예약이 3,950m(98%)라 request 100m 새 pod 가 **Pending**(infra PR #36). back 은 Soniox 중계라 평소 사용량이 작다 — 실제 사용은 limit 1 까지 그대로 | 배포 10 실측 · 코디 |
| 차트 주석 · NOTES | 「Stateless (no DB, no volume)」 · 「No volumes → no fsGroup」 주석을 고친다 | — |
| 비밀값 | 바뀌지 않는다(Secret 키 목록 그대로). `INTERPRET_RECORD_DIR` 은 ConfigMap | §2.4 |
| **보관 기간(0.7.0)** | `INTERPRET_RECORD_KEEP_DAYS` 는 **ConfigMap · Secret 에 넣지 않는다**(= 삭제 안 함 · §5.9). 0.7.0 배포에서 infra 가 바꾸는 것은 **이미지 태그뿐**(차트 · PVC · ConfigMap 키 그대로). 베타가 끝나 다시 켤 때 ConfigMap 에 값만 넣는다(OQ-020) | D-42 |

**꺼내기 — kubectl(코디 · 배포 문서 `docs/interpret-pwa-deploy.md` 에 절을 더한다)**

```text
kubectl -n interpret-pwa-prod get pod -l app=back                          # back pod 이름
kubectl -n interpret-pwa-prod exec <back pod> -- ls -l /data/records       # 날짜별 파일
kubectl -n interpret-pwa-prod cp <back pod>:/data/records/<YYYY-MM-DD>.jsonl ./<YYYY-MM-DD>.jsonl
#   cp 가 안 되면(이미지에 tar 없음): kubectl -n interpret-pwa-prod exec <back pod> -- cat /data/records/<YYYY-MM-DD>.jsonl > ./<YYYY-MM-DD>.jsonl
```

- 꺼낸 파일에는 **대화 문장**이 들어 있다 — **레포(특히 public 문서 레포) · PR · 보고서 본문에 붙이지 않는다**. 로컬 작업 폴더(git 밖)에서 보고 지운다. 보고에는 줄 수 · term 적중 수 같은 **수치만**.
- 기록을 지우고 싶으면(시연 전 초기화 등) 같은 방식으로 `exec … rm /data/records/<파일>` — back 은 파일이 없어도 다음 줄에서 새로 만든다.

**배포 뒤 확인(0.6.0 · WP18 · 운영 주소 — 0.7.0 확인은 아래 「배포 뒤 확인 (0.7.0 · WP20)」)** — ① back 기동 로그 `glossary seed loaded: version=2026-10-27.6 …` · `interpret records: on dir=/data/records keep_days=7` ② PVC `Bound` · back pod 가 `lima-worker-1` ③ **새 시술 3개 언어 실발화 1회**(⑳ 과 같은 문장 · zh-Hant · ja · en — 폰 또는 합성 음성) ④ **오늘 파일이 생기고** 그 세션의 start · utterance · end 줄 · `terms` 에 `kr-…` ⑤ **7일 삭제**: `exec` 로 `<오늘−8일>.jsonl` · `<오늘−6일>.jsonl` · `keep.txt` 를 만들고 back 을 재시작(`rollout restart` — 기동 때 삭제) → −8일 파일만 사라짐 · 로그 `sweep: deleted=1` → 시험 파일 정리 ⑥ §3.5 표면 그대로(`/api/health` `{ok}` · `/api/glossary` · `/docs` 404) ⑦ 롤아웃이 PVC 를 다시 붙이며 끝남(Pending 0).

**배포 뒤 확인 결과 (0.6.1 — 코디 · 배포 10 · 11)**

| # | 결과 |
|---|---|
| ① | 기동 로그 시드 `.6` 로드 · `interpret records: on dir=/data/records keep_days=7` |
| ② · ⑦ | 첫 롤아웃에서 새 pod **Pending**(노드 CPU 예약 98% — PVC 문제 아님) → PR #36(request 50m) 뒤 기동 · 위 ① 로그로 확인 |
| ④ | 운영 세션의 `session_start` · `session_end` 줄이 기록됨(`utterance` 줄 수 · `terms` 적중 수는 이번 보고에 없음) |
| context | 운영 zh-Hant context **21,658 / 21,689**(`terms` 170 · 역방향 별칭 33 줄임 — ⑲ 최종과 같음) |
| ③ · ⑤ · ⑥ | 이번 코디 보고에 결과 없음(새 시술 3개 언어 실발화 · 7일 삭제 시험 · 표면) — 기록하지 않았다 |

- 운영 `GLOSSARY_CONTEXT_MAX_CHARS` 는 비어 있어야 언어별 표가 쓰인다(§2.4) — 위 zh-Hant 기준 21,689 가 로그에 나온 것이 그 확인이다.

**배포 뒤 확인 (0.7.0 · WP20 · 운영 주소 — D-42)** — 운영에는 지금 11-11 ~ 11-14 날짜 파일이 있고, 0.6.x 배포본이 떠 있으면 **11-11 파일이 11-18 에 지워진다** — 그 전에 0.7.0 back 이 떠 있어야 한다.

| # | 확인 |
|---|---|
| ① | back 기동 로그 `interpret records: on dir=/data/records keep_days=off`(시드 로드 줄은 0.6.1 과 같다 — 시드는 안 바뀐다) · `interpret records sweep: deleted=` 줄 0 |
| ② | 배포 전 `exec … ls -l /data/records` 로 **가장 오래된 날짜 파일 이름 · 파일 수**를 적어 둔다 → 배포(롤아웃 = 재시작) 뒤 다시 `ls` → **가장 오래된 날짜 파일이 그대로 남고 파일 수가 줄지 않았다** |
| ③ | 렌더된 ConfigMap 에 `INTERPRET_RECORD_KEEP_DAYS` 키가 **없다** · infra 변경은 이미지 태그뿐 |
| ④ | §3.5 표면 그대로(`/api/health` `{ok}` · `/api/glossary` · `/docs` 404) · 오늘 파일에 줄이 계속 써진다(세션 1회 뒤 줄 수 증가 — 수치만) |
| ⑤ | 롤아웃이 PVC 를 다시 붙이며 끝남(Pending 0) · back pod `lima-worker-1` |

- 운영 파일을 지우거나 고쳐서 시험하지 않는다(0.6.0 ⑤ 의 시험 파일 만들기는 0.7.0 에서 하지 않는다 — 삭제가 꺼져 있다). 확인 결과에는 파일 이름(날짜) · 줄 수 같은 **수치만** 적는다(문장 0).
**배포 뒤 확인 결과 (0.7.0 · WP20 · 2026-11-14 · 코디)** — 배포 12(code PR #11 → `e0fbda8` · infra PR #54 · ArgoCD sync `70490ee`)

| # | 결과 |
|---|---|
| ① | `interpret records: on dir=/data/records keep_days=off` · 시드 `2026-10-27.6` 170 term 로드 · `sweep` 줄 0 — 통과 |
| ② | 배포 전 4개(11-11 · 11-12 · 11-13 · 11-14 — 가장 오래된 11-11 · 11,361 B) → 롤아웃 뒤 4개 · 크기 같음 — 통과 |
| ③ | ConfigMap 키 = `INTERPRET_FRONT_ORIGIN` · `INTERPRET_RECORD_DIR` 뿐 · infra diff = `back.imageTag` 한 줄 — 통과 |
| ④ | `/api/health` `{ok:true}` · `/api/glossary` 404 · `/docs` 404 — 통과. 「오늘 파일에 줄이 계속 써진다」는 배포 뒤 세션이 아직 없어 **미확인**(다음 사용 뒤 줄 수로 확인) |
| ⑤ | back pod Running · `lima-worker-1` · PVC Bound · Pending 0 — 통과 |

**배포 뒤 확인 (0.8.0 · WP25 · 운영 주소 — D-43 ~ D-48)** — back 만 바뀐다(front · 차트 · PVC · ConfigMap 키 그대로 · infra 는 이미지 태그만).

| # | 확인 |
|---|---|
| ① | back 기동 로그 `glossary seed loaded: version=<…>.7 terms=<수>` · `interpret records: on dir=/data/records keep_days=off`(0.7.0 그대로) |
| ② | 통역 연결 1회씩(7개 언어) — context 로그의 글자 수 · `text` 글자 수 · 묶음별 뺀 수 · `max=` 가 ㉒(WP23) 수치와 같음 · 거절 0 |
| ③ | **대표 문장 확인** — 현장 지적 세 가지에 해당하는 시험 번호(토닝 **T01** · 울쎄라 · 써마지 **T03** · 시술 뉘앙스 **T05 · T06**)와 말 없음 **T29** 를 운영 주소에서(품질 시험 음성 파일 또는 사람 목소리) → 기계 판정 · 사람 판정을 **번호 · 판정만** 보고. 운영 기록에서 꺼낸 문장은 붙이지 않는다 |
| ④ | §3.5 표면 그대로(`/api/health` `{ok}` · `/api/glossary` · `/docs` 404) · 오늘 기록 파일에 줄이 계속 써진다(수치만) · 가장 오래된 날짜 파일이 그대로(0.7.0 ②) |
| ⑤ | 롤아웃이 PVC 를 다시 붙이며 끝남(Pending 0) · back pod `lima-worker-1` |

- 배포 기록(§9.5 표)에 13(또는 그때 번호) 행을 더한다 — 코드 PR · infra PR · 시드 `.7`(0.9.0 — `.8`).
- **0.9.0 — 이 배포는 WP27(7차) 뒤 · 사용자 확인 뒤에 한다**(D-59 결과 페이지를 사용자가 본 다음). 실리는 것 = WP21 · WP23 · WP26(v6 · 문안 · 빈 원문 막기 · 시드 `.8` · 한도 「D-56 표」 · 시술명 바로잡기). 위 ① ~ ⑤ 를 이렇게 읽는다: ① 시드 로그 `version=2026-11-15.8` ② context 수치 = ㉖(= 「D-56 표」 · `max=` 가 D-56 값 · 7개 언어 뺀 수 0) ③ 대표 문장에 **T30** 을 더하고, 바로잡기가 돈 발화는 로그 `interpret term corrected` 줄 수 · 기록 줄의 `fixed`(term id)로 확인(번호 · 판정만) ④ · ⑤ 그대로. infra 는 여전히 이미지 태그만(새 env · ConfigMap 키 없음).
- **0.9.2 — 배포 전 조건이 찼다**: 7차(WP27 · 수정 1 · 2) 끝 · **사용자 확인 끝(2026-11-15 「진행하자」)**. 실리는 것 = 위 0.9.0 줄 + **시드 `.9` · `.10`**(§4.2.6 · §4.2.7) + **바로잡기 D-63 · D-64**(§5.12) + **(0.9.3) D-65 · D-66**(④ 좁힘 — 배포 전 코드 검수 두 번의 처분). 위 ① ~ ⑤ 를 이렇게 고쳐 읽는다: ① 시드 로그 **`version=2026-11-15.10`** ② context 수치 = §4.6 「시드 `.8` ~ `.10` 의 글자 수」 의 `.10` 열 — `max=` 는 D-56 값 그대로 · **뺀 수는 ja `terms` 2 · th `terms` 79 · 나머지 5개 언어 0**(「7개 언어 뺀 수 0」 이 아니다 — D-62) · 거절 0 ③ 대표 문장 그대로(T01 · T03 · T05 · T06 · T29 · T30) · 바로잡기 로그의 `steps` 에 `4` 가 나올 수 있다(외 → 한) ④ · ⑤ 그대로. infra 는 이미지 태그만(새 env · ConfigMap 키 없음).
- **사람 목소리 확인**(실장 · 중국 코디가 같은 말을 다시 해 보는 것)은 이 확인의 완료 조건이 아니다 — 결과가 오면 OQ-017 에 적는다.

## 10. 열린 것 — 근거(DEC · 공식 문서 · 원형)로 닫지 못한 것

> 0.5.0 마감 정리 — **남은 것은 셋**: 사람 목소리 E2E(OQ-017) · 못 찾은 대만명 80(OQ-016) · 데모 로그인 끄기(OQ-008). 나머지는 닫았거나 합쳤다(근거는 각 행).
> 0.6.0 — **둘을 더한다**: 처분 밖에 남은 모호 · 근거 없는 시드 값(OQ-018) · 대문자 영문 name 의 TTS · 일반 단어 역방향(OQ-019). OQ-016 에 0.6.0 의 `reviewed:false` 가 더해진다.
> 0.7.0 — **하나를 더한다**: 베타가 끝나는 때 · 그때 넣을 보관 기간(OQ-020 · D-42).
> 0.9.3 — **하나를 닫는다**: OQ-033(D-66 — ④ 를 넓히지 않는다 · 오히려 좁혔다).
> 0.9.2 — **하나를 더한다**: OQ-033(외 → 한 「가까운 한글 낱말」 을 거리 2 까지 넓힐지 — D-64 는 「음절 하나만」). OQ-032 에 7차 수치를 적었다(③ 으로 바뀐 칸 0 — 숫자는 기본값 그대로 열려 있다).
> 0.9.1 — **하나를 닫는다**: OQ-031(처분 §11 — 바로잡기 전 번역을 기록에 남긴다 · `translation_before`). OQ-032 는 숫자만 열려 있다(③ 의 범위는 처분 §11 로 정해졌다).
> 0.9.0 — **둘을 닫고 둘을 더한다**: 닫음 = **OQ-027**(D-55 — 끊김 1000 유지) · **OQ-028**(D-56 — 언어별 한도 = v6 실측 × 0.96 · 7개 언어 줄이기 0). 더함 = **OQ-031**(바로잡기 전 번역을 기록에 남길지) · **OQ-032**(가까운 라틴 낱말의 기준 숫자 — 기본값). OQ-024 · OQ-026 은 그대로 열려 있다.
> 0.8.3 — **하나를 닫는다**: OQ-030(코디 처분 §4 — a · b · c · d · f ~ k 는 planner 기본값 그대로 · e 만 바꿈 · §4.2.4 「읽는 법」). OQ-028 의 추정을 다시 계산하고(zh-Hant 는 D-53 뒤에도 넘는다) **D-54 절차**(§4.6)를 달았다 — 한도 표 자체는 여전히 열려 있다.
> 0.8.2 — **하나를 더한다**: 사전 보정 처분이 말하지 않은 자리(OQ-030 — **WP23 의 선행 조건**). 대만어(zh-Hant) 별칭 정리는 열린 것이 아니라 **결정(D-53)** 이다 — §4.2.4 ② F. OQ-028 에 시드 `.7` 추정(ja · th 도 줄이기)을 더했다.
> 0.8.1 — **둘을 닫는다**: OQ-025(D-49 — 넷째 문장을 넣는다) · OQ-029(D-50 — 7개 언어 × 3 = 21문장). OQ-027 의 방향은 D-47 로 정해졌다(값만 열려 있다). 남은 0.8.0 OQ = 024 · 026 · 027 · 028.
> 0.8.0 — **여섯을 더한다**(품질 개선 · 근거로 닫지 못한 것만): `text` 문안의 언어(OQ-024) · 「시술 = 수술 아님」 문장(OQ-025) · 막힌 빈 원문 발화의 기록(OQ-026) · 끊김 값(OQ-027) · v6 · 문안 · 시드 `.7` 뒤 한도와 손실(OQ-028) · 손님 쪽 문장의 언어 범위(OQ-029). DEC 「열린 것 (2026-11-14 · 품질 개선)」 OQ-021 ~ 023 은 **DEC 에서 닫혔다** — 이 문서 §9.3 「6차」 가 그 기본값을 따른다.
> 0.6.1 마감 — **OQ-018 닫음**(처분 ① ~ ⑤ · ⑤ 는 뒤집음 · §4.2.3 D). **남은 것**: 사람 목소리 E2E(OQ-017 · ④ 새 시술 미적중 더함) · 시드 검수 숙제(OQ-016) · 데모 로그인 끄기(OQ-008) · 대문자 영문 TTS · 일반 단어 역방향(OQ-019 — 사용자 청취 대기). 계약 안에서 안고 가는 손실: zh-Hant 역방향 별칭 33(§4.6 — 별칭 정리나 줄이기 순서 변경이 필요해지면 새 결정).

| ID | 무엇 | 지금 | 왜 못 닫나 · 권장 |
|---|---|---|---|
| ~~OQ-030~~ | ~~(0.8.2) 사전 보정 처분이 말하지 않은 자리 — §4.2.4 「기계 적용 — 읽는 법」 a ~ k 11곳~~ | **닫힘(0.8.3) — 코디 처분 §4**(`quality-research-dispositions.md`): a · b · c · d · f · g · h · i · j · k = planner 기본값 그대로 · **e = 바꿈**(r1-11 원칙을 7개 언어 전부에 — 부위 term 에 시술 이름을 name · alias 로 새로 넣지 않는다). §4.2.4 ② C · ③ 개수 · §4.6 추정을 이 처분으로 다시 계산했다 | — |
| ~~OQ-031~~ | ~~(0.9.0) 바로잡기 전의 번역을 통역 기록에 남길지~~ | **닫힘(0.9.1) — 코디 처분 §11**: **남긴다** — 바로잡은 발화 줄에만 새 키 `translation_before`(§5.9). 기록은 서버 내부 검토용(D-41)이고 운영에서 새 틀린 꼴 · 잘못 바꾼 것을 찾는 유일한 재료다 | — |
| **OQ-032** | **(0.9.0) 「아주 가까운 라틴 낱말」 의 기준 숫자**(§5.12 ③) — D-58 은 「그 꼴과 아주 가까운 라틴 낱말」 이라고만 했다. **(0.9.1) 도는 범위는 정해졌다**(처분 §11 — 번역 글자가 라틴이 아닌 쪽만 · en · vi 한 → 외는 ③ 없음) · 바탕에 맞는 이름(ASCII)을 넣는 것도 그대로 — **열린 것은 숫자(4 · 2)뿐** | **기본값**: 4글자 이상 · 편집 거리 ≤ 2 · 대소문자 무시 · 낱말 수가 같은 것끼리 · 가장 가까운 하나만(planner 기본값 — 실측 근거 없음) | WP26(㉖) · 7차(㉗)가 ③ 으로 바꾼 칸 수 · 잘못 바꾼 칸 수 · 못 바꾼 칸 수를 낸다 → 코디 · 사용자가 숫자를 고치거나 그대로 둔다(코드 상수 · 이 절 표를 같이). 짧은 이름(4글자)에서 거리 2 가 넓으면 길이에 따라 거리를 줄이는 쪽이 후보다 — 시험 수치 없이 미리 바꾸지 않는다. **(0.9.2 · 7차 수치)** 7차 첫 실행의 바로잡은 term 32 가운데 ③ 은 **0**(① 26 · ② 6) · 잘못 바꾼 1 은 ② 였다(D-63 으로 닫음) — ③ 의 숫자를 고칠 근거가 아직 없다 · **기본값 그대로 배포하고 운영 기록(`translation_before`)으로 본다** |
| ~~OQ-033~~ | ~~(0.9.2) 외 → 한 「가까운 한글 낱말」(§5.12 ④)을 거리 2 까지 넓힐지~~ | **닫힘(0.9.3) — D-65 · D-66**: **넓히지 않는다.** 배포 전 코드 검수에서 거리 1 로도 조사를 먹고 일상 낱말을 바꾸는 꼴이 재현돼 ④ 를 오히려 좁혔다(첫 음절 같음 · 남는 것 = 비었거나 조사 · 음절 빠짐 해석 안 함 · 멈춤 목록 21개). 못 바꾸는 꼴은 「못 찾음」 으로 남기고, 운영 기록에서 되풀이되는 꼴만 `ko_wrong` 에 넣는다 | — |
| **OQ-024** | **(0.8.0) context `text` 문안의 언어** — 영어 한 벌(7개 언어 공통)인가, 언어별 문안(고른 언어 · 한국어)인가 | **영어 한 벌**(§4.5 네 문장 — `general` 과 같은 언어 · 한도 계산이 단순) | 공식 문서는 「Write the context in the language people speak」 라 하지만 한 세션에 두 언어가 오간다 — 어느 쪽이 번역을 더 바꾸는지 근거가 없다. 권장: 영어 한 벌로 조합 C 를 돌려 2절 결과를 본 뒤, 효과가 약하면 언어별 문안을 **추가 실행**으로 견준다(코디 · 사용자) |
| ~~OQ-025~~ | ~~(0.8.0) `text` 에 「시술은 수술이 아닌 미용 시술」 한 문장(S4)을 넣을지~~ | **닫힘(0.8.1) — D-49**: 넣는다 · 문안 = S1 ~ S4 네 문장(§4.5 · 439자 · zh-Hant 역방향 별칭 33 → 44 · th 여유 100 — §4.6) | — |
| **OQ-026** | (0.9.0 — 발화 줄에 `fixed` 키가 생겼지만 이 항목은 그대로다 · 막힌 발화는 여전히 줄이 없다) **(0.8.0) 막힌 빈 원문 발화를 통역 기록에 남길지** — D-48 은 「번역 · 음성으로 내보내지 않는다」까지만 정했고, D-41 의 기록은 「화면에 나간 확정 자막」 기준이다 | **남기지 않음**(§5.9 문구 그대로 — 나가지 않은 발화는 줄이 없다 · §5.11). 건수는 back 로그(`blank original dropped`)로만 | 남기면 얼마나 자주 생기는지 · 무엇이 지어졌는지 내부 검토에 쓸 수 있지만, 줄 모양(막힘 표시 키)이 바뀐다(§5.9 「여기 없는 키 0」). 권장: 지금은 남기지 않고, 로그 건수가 많으면 새 결정 |
| ~~OQ-027~~ | ~~(0.8.0) 끊김 값을 손볼지 · 얼마로~~ — **닫힘(0.9.0) — D-55**: `max_endpoint_delay_ms` **1000 유지**. 조합 C2(2000)는 3절 조각 수 · 기계 · 사람 판정이 C 와 같고 지연만 늘었다(§9.3 「6차 결과」 · §5.10). `endpoint_sensitivity` 는 돌려 보지 않았다 — 손볼 근거가 생기면 새 결정. 사용자가 비교 페이지에서 다른 판단을 주면 §5.10 을 고친다 | 1000 그대로(§5.10) | (아래는 0.8.1 기록) **방향은 정해졌다(0.8.1 · D-47)** — 덜 끊는 쪽 = `max_endpoint_delay_ms` 는 올리고 `endpoint_sensitivity` 는 낮춘다(공식 「Higher values make endpoints more likely」). **열린 것은 손볼지와 값**이다 — 지연과의 맞바꿈은 사용자가 실물에서. 품질 시험 3절의 조각 수(실제 − 기대) · 지연(B · C)을 올린 뒤 정한다. `endpoint_latency_adjustment_level` 은 끊김을 앞당기는 값이라 대상이 아니다 · 「누르고 말하기」(D-36)는 이 값과 무관 |
| ~~OQ-028~~ | **닫힘(0.9.0) — D-56**: 언어별 한도 = v6 실측 통과 최대치 × 0.96 내림(§4.6 「D-56 표」) · 시드 `.7`(D-54 로 27개 뺀 판)에서 7개 언어 줄이기 0 · 거절 0 · th 여유 22자(안고 감 — 시드에 이름 · 별칭을 더하면 th 부터 `terms` 가 빠진다). 아래는 0.8.x 기록 — ~~(0.8.0) v6 · 문안 · 시드 `.7` 뒤 언어별 한도와 손실~~ — ① §4.6 언어별 표는 v5 · 시드 `.6` 실측이다(v6 에서 같은 글자 수가 통과하는지 모름) ② `text` 는 줄이지 않아 zh-Hant 역방향 별칭이 더 빠진다(`.6` 추정 33 → 44 — 네 문장 · 0.8.1) · th 여유 100자 ③ 시드 `.7` 이 짝을 늘리면 더 빠진다 — **0.8.3 추정(§4.6 「시드 `.7` 추정」 · 순수 계산 · 처분 §4-e · r3 반영)**: **ja 가 기준을 1,307자 넘어 `terms` 128개 · th 가 2,029자 넘어 `terms` 전부 + 역방향 별칭 9개 · zh-Hant 는 D-53 정리 뒤에도 667자 넘어 `terms` 61개**(역방향 별칭 0) · zh 여유 490자. 정방향 뺀 수는 0 | 표 그대로 · 줄이기 순서 그대로. **넘는 언어는 D-54 절차로**(§4.6 — v6 재측정 뒤에만 · 근거가 약한 별칭부터 · 그래도 넘으면 멈춤) | WP21(㉒ 연결) · WP23(㉒ ⑬′ 재측정)이 수치를 낸다. 표 · `langs.py` 를 고칠지 · 줄이기 순서를 바꿀지는 코디 · 사용자(0.6.1 「안고 가는 손실」 의 연장 — 워커가 바꾸지 않는다). **(0.8.3) D-54 추정**: zh-Hant 는 「10-27 근거」 22개를 빼면 한도 안 · **ja · th 는 출처 1곳뿐인 새 별칭(ja 2 · th 3)으로는 닫히지 않는다** — v6 한도가 v5 와 비슷하면 D-54 의 「멈추고 사용자에게」 로 간다 |
| ~~OQ-029~~ | ~~(0.8.0) 손님 쪽 시험 문장 「언어마다 3문장」 의 언어 범위~~ | **닫힘(0.8.1) — D-50**: 앱 7개 언어 × 3 = 21문장(T34 ~ T54 · §9.3 「6차」) | — |
| ~~OQ-021~~ · ~~OQ-022~~ · ~~OQ-023~~ | ~~(DEC · 2026-11-14) 시험 목록 위치 · 시험 방식 · 손님 쪽 문장~~ | **DEC 에서 닫힘**(사용자 2026-11-14) — 로컬 전용 · Soniox TTS 음성 파일 · 언어마다 3문장 → §9.3 「6차」 | — |
| **OQ-020** | **(0.7.0) 베타가 끝나는 때 · 그때 넣을 보관 기간** — D-42 는 「베타가 끝나면 값만 넣어 다시 켠다」까지만 정했다. 언제 끝나는지 · `INTERPRET_RECORD_KEEP_DAYS` 에 몇 일을 넣는지 · 그동안 쌓인 파일을 그때 한꺼번에 지워도 되는지(값을 넣으면 첫 기동에 N 일보다 오래된 파일이 모두 지워진다 · §5.9)는 정해지지 않았다 | 운영 = 삭제 안 함(값 없음) · 기록이 계속 쌓인다(§9.6 크기 근거 — 4일 44KB) | 사용자가 베타 종료를 정할 때 같이 정한다. 할 일: 필요한 기록을 먼저 꺼낸 뒤(§9.6 kubectl) infra ConfigMap 에 값만 넣고 back 재시작 — 코드 수정 없음(D-42). 용량 경보 · 압축 같은 정책은 계약에 없다(짓지 않는다) |
| **OQ-017** | (0.9.0 — ⑤ **손님 쪽 울쎄라 en · vi 인식**: 6차 T34 · T49 에서 합성 음성의 영문 상표를 STT 가 다른 낱말로 들음 — 바로잡기 대상이 아니다 · 사람 목소리에서 같은지 모름) **사람 목소리 E2E**(0.5.0 — OQ-001 · OQ-007 의 남은 확인을 합침) — ① 대만 현지명 양방향: 한국어 「울쎄라」 · 「써마지FLX」 → 대만명이 합성 음성에서 상표명 · 음역으로 나옴(⑰ 1/4 — 짝은 context 에 있음 · 줄이기와 무관) ② `yue` = 표준 문어(번체 자막) + 만다린 음성(OQ-001) ③ iPhone 길게 누름(D-36 — 선택 · 확대 · 콘텍스트 메뉴 · 원 밖으로 미끄러짐) · 누르는 중에 TTS 가 오면 송신 막힘(반이중 그대로 · DEC 에 따로 없음) ④ **(0.6.1) 새 시술 미적중**(⑳ 합성 음성 · 짝은 context 에 있음): 프로파일로 → STT 가 「프로파일」로 들음(3개 언어 모두 · 번역 전) · 뉴라미스 zh-Hant → 「優美思」 · ja 「サーマジCPT」(시드 name `サーマクールCPT` 와 다른 음역 — ja alias 로 넣을 근거 없음 · 조사 R4 · R5) · 덴서티 ja → 「デンソティ」 · zh-Hant 에서 Exion · density · 엠페이스가 영문 | 코드 · 시드로 더 할 것이 보이지 않음 · 배포 fe8475e(④ 는 17c26b5) | 합성 음성 표본 1문장씩이라 판정 못 함. 권장: 사용자가 폰(배포 주소)에서 사람 목소리로 1회 — 결과로 시드(대만명 별칭 · ④ 의 음역 alias 는 근거가 생기면) 또는 DEC 를 고친다. 운영 기록(§5.9)의 `terms` 로 적중을 셀 수 있다 |
| **OQ-016** | **시드 검수 숙제(사용자 PR)**(0.8.0 — D-46 사전 전체 보정(§4.2.4)이 이 숙제의 상당 부분을 다시 본다 · 보정 뒤 남는 `reviewed:false` 가 이 항목으로 온다) — ① **대만 현지명을 못 찾은 80 term**(zh-Hant = 초안 · `draft-s2twp` · `reviewed:false` — `.5`(D-38)로 일부 정리) ② 출처 1개뿐인 대만명(`web-research` · `reviewed:false`) ③ 첫 가져오기 「그 밖」 괄호 60(OQ-012 를 합침 — 괄호를 뺀 이름 + `raw` 보존 · `reviewed:false`) ④ **(0.6.0) 새 시술 · 대륙 변경의 ✗ 칸**(§4.2.2 · §4.2.3 — 「현지에 없음 = 영문」 · 출처 1) · **C 결함 4칸의 현지 표기**(`manual` · 영문으로 둠) | 데이터 그대로 · context 에는 들어감(§4.2 — 검수 여부로 빼지 않음). 메뉴가 없어(D-37) 목록은 시드에서 `reviewed:false` 로 찾는다 | 현지명 · 별칭은 사람이 정한다(D-32 · D-33 · D-35 — 우리가 짓지 않는다). 권장: 사용자가 시드 PR(§4.2.1 규칙) → 재배포(§9.5) |
| **OQ-008** | **데모 로그인 끄기** · 로그아웃해도 토큰은 만료(기본 12시간)까지 유효 | 운영 **데모 켬**(`INTERPRET_DEMO_LOGIN=true`) — 주소만 알면 로그인된다 · 서버 토큰 무효화 없음 | 데모가 끝나는 때는 사용자가 정한다. 할 일: Secret 에서 `INTERPRET_DEMO_LOGIN` 값만 지우고 back 재시작(D-30 · §3.4). 토큰 무효화는 PoC 범위 밖 |
| ~~OQ-018~~ | ~~(0.6.0) 처분 밖에 남은 시드 값~~ | **닫음(0.6.1)** — 코디 처분 2026-10-27(`research-dispositions.md` 「OQ-018 처분」 · §4.2.3 D): ① ph-123 · ph-126 zh name → 영문(모호어는 alias 에도 없음) ② yue ph-121 = `美版超聲刀`(`超聲刀` 단독 지움) ③ ph-113 zh · th = `Juvelook Volume`(옛 값 alias) ④ 리쥬란 상자 표기 그대로 · ✗ ⑤ **ko 별칭 「써마지」 — 0.6.0 처분 「그대로」를 뒤집어 지움**(실물 ⑳: 「써마지 CPT」 → zh-Hant `鳳凰電波`(FLX) 오역 → 지운 뒤 `黃金電波`(kr-001) ✓) | — |
| **OQ-019** | **(0.6.0) 대문자 영문 name 과 일반 단어** — ① `EXION` · `DENSITY` · `EMFACE` 를 Soniox TTS 가 글자 하나씩 읽는지(en · zh · th · vi · yue 칸에서 TTS 가 읽는 말) ② en `DENSITY` 는 일반 단어(골밀도 · 피부 밀도)라 역방향 짝 `DENSITY → 덴서티` 가 일반 문장에 걸릴 수 있다(alias `Density` 는 막았지만 name 은 브랜드라 둠 — Soniox 가 대소문자를 가르는지 근거 없음) | **사용자 청취 대기**(0.6.1) — ⑳ 에서 소리 파일만 만들었다(`orchestration/work/interpret-pwa-v2/tts-samples/` 13개 · `EMFACE-zh` 2.39초로 확연히 김). en 번역문은 `Exion`(섞임) · `DENSITY` · `EMFACE` 로 나왔다. 그 전까지 name 은 제조사 표기(처분) | 권장: 사용자가 들은 결과 한 줄로 — 글자 읽기면 name 을 `Exion` · `Density` · `Emface` 꼴로 바꾸는 시드 PR(코디 · 사용자 결정 · 「영문 표기」 칸만 바꾸면 R2 칸이 따라 바뀐다) · 일반 문장 오역이 보이면 en 짝 처분 |
| ~~OQ-001~~ | ~~`yue` 음성 · 번역 품질~~ | **OQ-017 ② 로 합침**(0.5.0) | — |
| ~~OQ-002~~ | ~~한도 기본값~~ | 닫음 — 20,251(0.4.1 · §4.6 · ⑬). 0.5.0 zh-Hant 는 `terms` 만 줄어듦(짝 전부 남음). **0.6.1 — 언어별 표로 바꿈**(§4.6 · ⑬′) | — |
| ~~OQ-003~~ | ~~역방향 `translation_terms`~~ | 닫음(0.3.0) — D-18 | — |
| ~~OQ-004~~ | ~~대만 · 홍콩 만다린 화자용 선택지~~ | 닫음(0.4.0) — D-28 · 변환은 0.5.0 D-35(`s2tw` + 표) | — |
| ~~OQ-005~~ | ~~통역 시작 · 멈춤 조작~~ | **닫음(0.5.0)** — 시작 = 오버레이 언어 단추(D-34) · 원 = 멈춤 ↔ 다시 듣기 또는 누르고 말하기(D-36 · 사용자가 모드로 고른다) · 멈춤에 초기화(D-29) | — |
| ~~OQ-006~~ | ~~외국어 안내 문구 번역 값~~ | **닫음(0.5.0) — PoC 범위로 둔다**(frontend 상수 · 원어민 검수 없음 · 「Hold to speak」 류 포함) | 고칠 말이 생기면 front 상수(`lib/langs.ts`)만 고친다 |
| ~~OQ-007~~ | ~~휴대폰 실기기 확인 시점~~ | **닫음(0.5.0)** — 배포(HTTPS) 뒤 폰으로 확인해 왔다(폰 피드백 1 ~ 3 · D-27 ~ D-37). 남은 사람 목소리 확인은 OQ-017 | — |
| ~~OQ-009~~ | ~~괄호 병기 target 이 번역 · TTS 에 나옴~~ | 닫음(0.3.0) — D-19 · §5.7 유지 | — |
| ~~OQ-010~~ | ~~뒤집힌 영역 언어 목록~~ | 닫음(0.4.0) — D-31 · D-28 | — |
| ~~OQ-011~~ | ~~배포 도메인~~ | 닫음(0.4.0) — D-26 | — |
| ~~OQ-012~~ | ~~첫 가져오기 「그 밖」 괄호 표기~~ | **OQ-016 ③ 으로 합침**(0.5.0) | — |
| ~~OQ-013~~ | ~~zh-Hant context 재료~~ | **닫음(0.5.0)** — zh-Hant entry(`t2s`) · D-35 로 대만 현지명이 들어가 zh 와 실제로 다르다(§4.5 · ⑰) | — |
| ~~OQ-014~~ | ~~ko 별칭 · 써마지 단독~~ | **닫음(0.5.0)** — 써마지FLX `ko_aliases` 「써마지」(⑭ · ⑰ ✓). 더 필요한 호칭은 사용자 시드 PR(OQ-016 과 같은 길). **0.6.1 — 별칭은 OQ-018 ⑤ 로 지워졌다**(써마지 CPT 와 겹침 · §4.2.3 D) | — |
| ~~OQ-015~~ | ~~시드 숙제 ① zh-Hant 현지명 ② 美版/韩版 구어 ③ 그 밖 괄호~~ | **닫음(0.5.0)** — ① D-35 조사로 77 반영(못 찾은 80 → OQ-016 ①) ② D-35 — 한 기기로 확정되는 것만 alias(热玛吉 → 써마지FLX) · 모호어(超声刀 · 韩版超声刀 · 韩版热玛吉) zh · zh-Hant 에서 뺌(§4.2.1) ③ → OQ-016 ③ | — |

## 부록 A. 결정 대응표

| DEC | 이 문서 |
|---|---|
| D-01 새 레포 · `front/` · `back/` | §2.1 |
| D-02 Next.js PWA · FastAPI(uv) | §2.1 · §8 PWA |
| D-03 back WS 중계 · STT two_way + TTS · 반이중 · 키는 back env | §5 · §7.4 · §2.4 |
| D-04 언어 드롭다운(용어집 언어) | §5.5 · §7.2 |
| D-05 용어집 context · `terms` ko · `translation_terms` ko → L · 넘으면 줄임 | §4.5 · §4.6 |
| D-06 로그인 계정 하나 · 값은 env | §3 · §2.4 |
| D-07 화면 둘 · 배치 | §6 · §7.1 · §7.2 · §7.6 |
| D-08 외국어 영역 180° · 전환 아이콘 · 렌더만 | §7.2 |
| D-09 원 · 음량 · 색 · 출력 중 안내 | §7.3 |
| D-10 medikit · 단순 | §6 · §7.8 |
| D-11 키는 사용자 `.env` · `.env.example` 만 | §2.4 |
| D-12 로컬 확인 → 마지막 배포 | §9.3 · §9.4 · §9.5 · WORK-001 순서 |
| ~~D-13 용어집 메뉴 읽기 전용~~(D-37 로 뒤집힘) | §4.7 · §7.6 — 삭제 기록 |
| D-14 기동 때 한 번 캐시 · ~~실패면 용어집 없이~~(D-33 개정 — 시드 실패는 기동 실패 · 기본값) | §4.3 · §4.4 |
| D-15 배포 도메인은 배포 WP | D-26 으로 닫힘 · §9.5 |
| D-16 각 영역에 자기 언어 문장만 | §7.5 |
| D-17 번체는 back 변환 · 자막만 · TTS 간체 | §5.6 · §4.5 |
| D-18 역방향 용어(L 표기 → ko) | §4.5 · §4.6 · §9.3 ⑧ ⑨ ⑮ |
| D-19 괄호 병기는 자막 그대로 · TTS 입력에서만 뺌 | §5.7 · §4.10 · §9.3 ⑩ |
| D-20 화면 정본 = Claude Design 시안 · ceramique 테마 | 머리말 · §6 · §7 · §9.2 |
| D-21 앱 이름 통키(Tongky) · 시안에서 더한 요소 채택 · `final:false` gray-600 | §6 · §7.1 · §7.2 · §7.3 · §7.5 · §7.6 · §8 |
| D-22 원 위 고른 언어 안내(180°) · 상태 8개 · 카드 안 안내 줄 이동 | §7.2 · §7.3 |
| D-23 원 64(최대 88) · 원 줄 140 · 안내 13px · 자막 영역 확대 | §7.2 · §7.3 |
| D-24 말풍선 — 보는 사람 기준 내 말 오른쪽 | §7.5 |
| D-25 자동 스크롤 · 「↓ 최신」 | §7.5 |
| D-26 배포 도메인 tongky.medisolveai.xyz | §9.5 · OQ-011 닫음 |
| D-27 로그인 입력 16px · 확대 막는 viewport 안 씀 | §7.1 |
| D-28 중국 · 대만 별도 언어 항목 · 목록 표시 이름 · 한국어 이름 | §5.5 · §5.6 · OQ-004 닫음 |
| D-29 멈춤 때 「초기화」 | §7.3 · §7.4 |
| D-30 데모 원탭 로그인 | §2.4 · §3.3 · §3.4 · §7.1 |
| D-31 언어 목록 180° — 자체 목록 | §7.2 · OQ-010 닫음 |
| ~~D-32 zh-Hant 출력 s2twp~~(D-35 로 뒤집힘) · yue s2tw · 별칭은 데이터로(유지) | §5.6 · §4.5 |
| D-33 용어집 = 우리 시드 · 정규화 · 첫 가져오기 · 런타임 호출 0 | §4 전부 · §9.1 「시드」 「가져오기 스크립트」 · §9.3 ⑫ ~ ⑯ · OQ-016 |
| D-34 시작 오버레이에서 언어 단추 7개 — 누르는 것이 시작 · 상담사 방향 · 마지막 언어는 표시만 | §7.3 #1 · §7.4 · §8 · OQ-005 |
| D-35 대만 현지명 시드 · zh-Hant `s2tw` + 「激光 → 雷射」 · 구어 alias · 모호어 제외 · 볼뉴머 카테고리 | §4.2 `source` · §4.2.1 · §4.5 · §4.6 · §4.8 · §5.5 · §5.6 · §9.1 · §9.3 ⑰ · OQ-016 · OQ-017 |
| D-36 누르고 말하기 모드(원 옆 전환 · 기억 · 누름 = resume · 뗌 = pause · TTS 중 누름 = 재생 멈춤) | §7.2 · §7.3 #4′ · §7.4 · §7.7 · §9.2 · OQ-017 ③ |
| D-37 최소 노출(D-13 뒤집음) — 용어집 API · 메뉴 삭제 · health/me `{ok}` · WS 오류 일반 문구 · docs 끔 | §1 · §2.1 · §3.3 · §3.5 · §4.7 · §5.4 · §7.6 · §9.1 · §9.2 |
| D-38 대만어 사전 2차(시드 `.5` — 톡신 대만 허가명 · 한국 전용 제품 영문 · 모호어 제거) | §4.2.1 「지금까지 반영한 판」 · §9.5 배포 9 (0.6.0 에서 뒤늦게 기록) |
| D-39 사전 밖 시술 7개 언어 추가 — 현지 피부과 표기 · 출처 2+ 만 reviewed | §4.2 `id` 규칙(`kr-`) · §4.2.1 R1 ~ R9 · **§4.2.2** · §4.6 0.6.0 · §9.1 「시드」 ⑥ · §9.3 ⑲ ⑳ · OQ-016 ④ · OQ-019 |
| D-40 대륙 중국어 검증 — 대륙 공식명 · 한국 전용 제품 영문 · 모호어 제거 | §4.2.1 R1 · R2 · 모호어 목록 · **§4.2.3 A** · **§4.2.3 D**(0.6.1 OQ-018 처분) |
| D-41 통역 기록 — 서버에만 · 화면 · API 없음 · 날짜별 JSONL · 음성 없음 · 7일 삭제(D-42 가 뒤집음) · kubectl(Scope Out → In) | §1 · §2.1 · §2.4 · §3.5 · §5.1 · **§5.9** · §9.1 「기록」 · §9.3 ㉑ · **§9.6** |
| D-42 베타 기간에는 기록을 지우지 않는다 — 보관 기간 env `INTERPRET_RECORD_KEEP_DAYS` · 비면 삭제 안 함(운영 기본) · 값만 넣어 다시 켬(D-41 의 7일 삭제를 뒤집음) | §1 · §2.1 · **§2.4** · **§5.9 「보관 기간」** · §9.1 「기록」 ⑦ · ⑨ · **§9.6**(크기 근거 · 보관 기간 행 · 배포 뒤 확인 0.7.0) · OQ-020 |
| D-43 STT 모델 `stt-rt-v6` — 모델 이름만 · v6 단독 효과를 먼저 | §5.1 · **§5.10** · §9.1 「STT 설정」 · §9.3 「6차」 조합 B · ㉒ · OQ-028 |
| D-44 품질 개선의 완료 조건 = 시험 목록 T01 ~ T33 실물 시험 · 전후 비교 · 기계 / 사람 판정 · 울쎄라 원인 가르기 (DEC OQ-021 ~ 023 — 로컬 전용 목록 · TTS 음성 파일 · 손님 쪽 3문장) | **§9.3 「6차 — 품질 시험」**(㉒ ~ ㉕ · 0.8.1 조합을 바꾸는 길 · 규칙 종류 넷 · 기대 발화 수) · §9.1 「기본값 = 켬」 · §9.6 배포 뒤 확인 0.8.0 ③ |
| D-45 역할 context — 한국어 쪽 = 직원 · 상대 = 손님 · `text` · `general` · 일반 낱말 짝은 `translation_terms` 에 넣지 않음 | **§4.5 「서술 칸 `text`」 · 「넣지 않는 것」** · §4.6(`text` 는 줄이지 않는 칸 · 여유 계산) · §5.1 · §9.1 「context `text`」 · OQ-024 · OQ-028 |
| D-46 사전 전체 보정 — 7개 언어 × 그 나라 클리닉 공식 사이트 6곳 · 170 term · 현지어 우선 · 겹침 · 중복 · 확인된 오류 | **§4.2.4**(0.8.2 값 채움 — D-51 · D-52 · 처분 · 0.8.3 처분 §4 ~ §6) · §4.2 `version` `.7` · §4.2.1 「지금까지 반영한 판」 · §9.3 「6차」 5절 · 울쎄라 원인 가르기 · OQ-016 |
| D-47 끊김 기준 — v6 로 먼저 보고 남으면 **덜 끊는 쪽으로**(`max_endpoint_delay_ms` 올림 · `endpoint_sensitivity` 낮춤 — 0.8.1 방향 바로잡음) · 지연은 사용자가 실물에서 | §5.1 · **§5.10 「끊김」** · §9.1 「STT 설정」 · §9.3 「6차」 3절 · 지연 · OQ-027 |
| D-48 원문이 비었거나 문장부호뿐인 발화는 번역 · 음성으로 내보내지 않음 | §5.1 · **§5.11** · §9.1 「빈 원문」 · §9.3 「6차」 T29 · OQ-026 |
| D-49 (SPEC OQ-025) context `text` 에 「시술은 수술이 아니라 미용 시술」 문장 — 네 문장 | **§4.5 문안 S4** · §4.6(439자 · 다시 계산) · §9.1 「context `text`」 · §9.3 1절 T05 · T06 · OQ-025 닫음 |
| D-50 (SPEC OQ-029) 손님 쪽 시험 문장 = 7개 언어 × 3 = 21 | **§9.3 「6차」 손님 쪽 문장**(T34 ~ T54) · ㉕ · OQ-029 닫음 |
| D-51 세대 없는 「써마지」 term 을 새로(10-27 처분 6 · OQ-018 ⑤ 뒤집음) · 사전 보정 조사의 나머지는 처분 문서 규칙대로 | **§4.2.4**(① 반영 규칙 · ② A `kr-014` · B 합침 · C · D · E 손 처분 칸 · ③ 개수 · 읽는 법) · §4.2 `id` 규칙 · `version` `2026-11-14.7` · §4.2.1 모호어 목록(`kr-014` name 예외) · §4.6 「시드 `.7` 추정」 · §9.3 ㉒ 「써마지」 다시 보기 · OQ-030 |
| D-52 토닝(ph-012) zh = `调Q激光` · alias `激光嫩肤` — `提亮` · `激光美白` · `镭射净肤` 뺌 | **§4.2.4 ② C**(E1) |
| D-53 대만어(zh-Hant) 별칭은 쓰임이 확인된 것만 남긴다 · term 은 안 뺀다 · 별칭마다 짧은 조사 한 번 더 | **§4.2.4 ② F**(0.8.3 — 조사 r3 `quality-r3-tw-alias.json` 245행 · 판정 넷의 처리(처분 §6): `뺌` 77 을 지움 · 「다른 term 과 겹침」 7 은 건드리지 않음 · 별칭으로 내려오는 옛 name 에도 적용(3개 뺌 — 0.8.4) · 별칭 247 → 167) · ③ 「F 뒤」 행 · §4.6 「시드 `.7` 추정」(정리 뒤에도 667자 초과 · `terms` 61 — 실측은 WP23) |
| D-54 한도를 넘는 언어는 근거가 약한 별칭부터 뺀다 — 시드 `.7` · v6 로 실제로 다시 잰 뒤에만 · zh-Hant 는 r3 「유지 — 10-27 근거」 부터 · ja · th 는 새 별칭 중 출처 1곳뿐인 것부터 · term · name 은 안 건드림 · 그래도 넘으면 멈추고 사용자에게 | **§4.6 「D-54 절차」**(순서 1 ~ 5 · **「넘는다」 = 전체 > 실측 통과 최대치 × 0.9**(0.8.4) · 후보 zh-Hant 22 · ja 2 · th 3 · 추정) · §4.2.4 ② F(「유지 — 10-27 근거」 행) · §9.3 ㉒ · OQ-028 |
| D-55 (D-47 시험) 끊김 비교 조합 C2 — C 와 같고 `max_endpoint_delay_ms` 만 2000 · 운영 값은 결과를 보고 사용자가 | §9.3 「조합」(C2) · **「6차 결과」**(3절 표 · C 와 같음) · **§5.10 「결과」 — 1000 유지** · §5.1 · OQ-027 닫음 |
| D-56 (OQ-028 · D-54 절차 5) 언어별 context 한도 = v6 실측 통과 최대치 × 0.96 내림 · 7개 언어 줄이기 0 | **§4.6 「D-56 표」 · 「D-54 절차의 결과」** · §2.4 · §5.10 · §9.1 「context」 · §9.3 ㉒ 결과 · ㉖ · OQ-028 닫음 |
| D-57 (D-44 넓힘) 품질 시험을 7개 언어 전부로 — 다국어 묶음 10문장을 같은 한국어 음성으로 7개 언어 세션에서 · 판정은 사전에서 자동 | **§9.3 「7차」** 직원 쪽 `S01` ~ `S10` · 판정 표(조합은 D-59 로 최종 버전만) |
| D-58 번역 뒤 시술명 바로잡기 — 원문에 term 이 걸렸는데 번역에 사전 이름이 없으면 틀린 꼴을 사전 `name` 으로 · 방향 둘 다 · 틀린 꼴 목록은 시드에 term · 언어별 · 못 찾으면 그대로 + 로그 1줄 · 사전 이름 자체는 D-46 그대로 | **§5.12**(걸리는 조건 · 찾기 ① ② ③ · 자리 · 끄는 길 · 한계) · **§4.2**(`ko_wrong` · `wrong` · 검사 8) · **§4.2.5** 시드 `.8` 첫 목록 · §4.5(context 에 넣지 않음) · §5.1 · **§5.9 `fixed`** · §5.11(순서) · §9.1 「시드」 ⑧ · 「바로잡기」 · 「기록」 ⑪ · §9.3 ㉖ · 「7차」 바로잡기 표시 · §9.6 0.9.0 · OQ-031(0.9.1 닫음 — `translation_before`) · OQ-032 · **0.9.1(처분 §11)**: ③ 은 번역 글자가 라틴이 아닌 쪽만 · 라틴 낱말 경계 · 같은 현지명 묶음(조건 2) · ① ② 먼저 · 자리 두 줄 · 일상 한국어 낱말은 `ko_wrong` 에 안 넣음 |
| D-59 (D-44 · D-57 넓힘) 품질 시험은 나라(언어)별로 — 7개 언어 × 직원 쪽 · 손님 쪽 · 시술 9개 · 결과 페이지 = 언어별 탭 · **최종 버전(바로잡기 포함) 하나만** — 이전 조합은 다시 돌리지 않는다 | **§9.3 「7차 — 나라별 시험」**(시술 목록 9 · 196행 · 판정 · 결과 페이지 · ㉗) · §9.6 0.9.0(배포는 7차 뒤 · 사용자 확인 뒤) |
| D-60 (D-51 고침) 세대 없는 「써마지」(kr-014) zh-Hant = `name` `熱瑪吉` · 영문은 별칭 · `reviewed: true` | **§4.2.5 「바뀌는 것」 ⓐ**(시드 `.8`) · §4.6 「시드 `.8` ~ `.10` 의 글자 수」(zh-Hant +31) |
| D-61 (D-46 규칙 좁힘) 그 나라 글자가 있는 언어(ja · zh · zh-Hant · th · yue)는 `name` 을 그 나라 글자로 · 영문은 별칭으로 · 근거 없는 음역 · 별명은 안 씀 · 없으면 영문 그대로 + 「현지 표기 없음」 | **§4.2.6 시드 `.9`**(원칙 · 처분 §15 규칙 · 개수 — `name` 73 · 별칭 뺌 36 · 칸 목록은 `seed-v9-diff.json`) · §4.2 `version` · §5.12 머리 · §9.3 「7차」(시드 판 읽기 · 「현지 표기 없음」 칸) |
| D-62 (D-54 절차 5) 시드 `.9` 에서 ja · th 가 기준을 넘는 만큼은 `terms` 줄이기로 받는다 · 영문 옛 name 별칭은 빼지 않는다 · 출처 2곳 이상이면 `reviewed: true` | **§4.6 「시드 `.8` ~ `.10` 의 글자 수」**(ja `terms` 2 · th `terms` 79 · 짝 손실 0 · 거절 0) · §4.2.6 `reviewed` 행 · §9.6 0.9.2 ② · §9.3 「7차 결과」(th 직원 쪽 인식) |
| D-63 (D-58 좁힘 · 7차 결과) 바로잡기 ② 에서 한자를 같이 쓰는 언어(ja · zh · zh-Hant · yue) 사이의 한자 꼴은 후보로 쓰지 않는다 · 시드 `.10` 에 7차 틀린 꼴 · 7차를 다시 돌려 확인 | **§5.12 ②**(후보에서 뺌 · 왜) · **§4.2.7 시드 `.10`** · §9.1 「바로잡기」 ⑮ · ⑯ · §9.3 「7차 결과」(7차 다시 — `test7b`) |
| D-64 (D-58 넓힘 · 7차 손님 쪽) 외 → 한 바로잡기에 「가까운 한글 낱말」 — ko 대표명과 음절 하나만 다른 꼴(대표명 3음절 이상 · 길이 ±1) · 다른 term 이름 · 일상 낱말(멈춤 목록)은 안 바꿈 · 한 → 외는 그대로 | **§5.12 ④ · 「가까운 한글 낱말 — 기준」** · §9.1 「바로잡기」 ⑰ · §9.3 「7차 결과」(손님 쪽 다시 — `test7c` · ④ 로 4행) · §9.6 0.9.2 ③ · OQ-033 |
| D-65 (D-64 좁힘 · 배포 전 검수 F-1 · F-2) ④ 는 첫 음절이 대표명과 같을 때만 · 거리가 같으면 짧은 앞부분(조사를 덮지 않음) · 멈춤 목록을 낱말 전체에도 | **§5.12 「가까운 한글 낱말 — 기준」**(첫 음절 · 고르기 · 바꾸지 않는 것 ⓑ) · §9.1 「바로잡기」 ⑱ · §9.3 「7차 결과」(저장 결과 다시 봄 — zh-G03 pass → fail · 152 / 196) |
| D-66 (D-65 좁힘 · 배포 전 재검수 W-1 · W-2) ④ 를 더 좁힘 — 남는 것이 비었거나 조사일 때만 · 음절이 빠진 꼴은 해석하지 않음 · 멈춤 목록 더함 | **§5.12 「가까운 한글 낱말 — 기준」**(견주는 단위 · 남는 것 · 해요체 「요」 · 끝 음절이 조사인 꼴 · 멈춤 목록 21개) · §9.1 ⑱ · §9.3(바뀌는 행 0) · **OQ-033 닫힘** |
| (DEC 밖) 운영 장애 2026-10-27 02:07 — TTS keepalive 형식 | §5.1 · §5.8 · §9.1 · §9.3 ⑱ |
