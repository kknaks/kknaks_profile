---
type: spec
id: SPEC-001
title: "통역 PWA — 로그인 · 용어집 context · 통역 WS · 화면 · PWA 계약"
version: 0.6.1
status: draft
product: interpret-pwa
created_at: 2026-10-26
updated_at: 2026-10-28
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
  - para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md (D-01 ~ D-41 · accepted — D-13 · D-32 는 뒤집힘 · D-41 이 Scope Out 「통역 기록 저장」을 In 으로)
  - 확정 시안 — Claude Design 캔버스 「Interpret PWA」(r3 · D-22 ~ D-24 · D-28 ~ D-30 반영 · r7 D-36 `Mode-Auto-Idle` · `PTT-Ready` · `PTT-Pressed` · r8 D-37 `Glossary` 삭제 · 화면 21개) 로컬 사본 interpret-pwa-poc 코드 워크트리 design/{README.md,project/*.dc.html,project/ceramique-theme.css} (D-20 · D-21 · 화면 19개)
  - 구현 kknaksss/interpret-pwa main d0a91a7(배포본 · D-22 ~ D-32 반영 — 0.4.0 은 이 코드에 맞춰 적고, 다르면 DEC 를 따른다) · main 9befd18(PR #4 · D-33 시드 — 0.4.1 대조) · main fe8475e(PR #5 ~ #8 · D-34 ~ D-37 · 운영 장애 수정 — 0.5.0 대조) · main 2a9d5a5(PR #9 · D-38 시드 `.5` — 0.6.0 대조) · **main 17c26b5(PR #10 · 시드 `.6` · 통역 기록 · 언어별 한도 — 0.6.1 대조 · 지금 back 배포본)**
  - orchestration/work/interpret-pwa-poc/{research-tw-names-report.md,d35-be-report.md,live-check-d35-2026-10-27.json,d36-fe-report.md,design-r7-report.md,d37-be-report.md,d37-fe-report.md,design-r8-report.md} (대만 현지명 조사 77/157 · D-35 시드 · 운영 장애 2026-10-27 02:07 원인 · D-36 · D-37 구현)
  - orchestration/work/interpret-pwa-v2/{research-r1-zh-report.md,research-r2-ja-en-tw-report.md,research-r3-th-vi-yue-report.md,research-dispositions.md} (D-39 · D-40 조사 3갈래 2026-10-27 · **코디 처분이 기준** — 0.6.0 §4.2.1 ~ §4.2.3)
  - orchestration/work/interpret-pwa-v2/{wp16-be-report.md,wp17-infra-report.md,live-check-wp16-{seed,seed-2,seed-3,ceiling,newterms,newterms-2,records}.json} (WP16 「처분 2」 · 「처분 3」 — 언어별 한도 · OQ-018 ⑤ 뒤집음 · 실물 ⑲ ~ ㉑ · WP17 PVC — 0.6.1)
  - k8s_infra_mac origin/main charts/interpret-pwa/{values.yaml,values-prod.yaml} (PR #35 PVC · 기록 · back 17c26b5 · PR #36 back cpu request 50m — 0.6.1 §9.6)
  - orchestration/work/interpret-pwa-seed-tw/{research-tresure-report.md,seed-tw-be-report.md} · para/projects/summer-star/interpret-pwa/log/2026-10-27-interpret-pwa-seed-tw.md (D-38 시드 `.5` — 0.6.0 에서 §4.2.1 에 뒤늦게 기록)
  - k8s_infra_mac origin/main charts/cc-prototype/{templates/back-pvc.yaml,templates/back.yaml,values.yaml,values-prod.yaml} · charts/interpret-pwa/* (PVC · local-path 노드 제약 선례 — 0.6.0 §9.6)
  - orchestration/work/interpret-pwa-poc/{wp9-be-report.md,wp9-fe-report.md,live-check-wp9-2026-10-27.json} (시드 실물 ⑫ ~ ⑯ · 한도 20251 처분)
  - orchestration/work/interpret-pwa-poc/{wp6-be-report.md,wp6-fe-report.md,fix-phone1-be-report.md,fix-phone1-fe-report.md,fix-phone2-be-report.md,fix-phone2-fe-report.md,fix-phone2-design-report.md,fix-phone3-be-report.md,fix-phone3-fe-report.md,live-check-wp6-2026-10-26.json} (D-22 ~ D-32 구현 · 실물 ⑧ ~ ⑪ · 한도 18832)
  - orchestration/work/interpret-pwa-poc/{design-report.md,live-check-2026-10-26.json,review-code-report.md,e2e-feedback-batch-1.md} (시안 제안 · Soniox 실물 ① ~ ⑦ · 코드 리뷰 FAIL-1 · WARN 1 ~ 6)
  - para/projects/summer-star/interpret-pwa/00-baseline/baseline-001-interpret-pwa.md (입력 1 ~ 4 · 확인한 사실)
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
> SSOT 순서(이기는 순): ① DEC-001 D-01 ~ D-41 ② 화면 = 확정 시안(D-20) ③ 통역 로직 = 원형 코드(`origin/main`) ④ Soniox 공식 문서 · 실물 결과(§9.3) ⑤ 이 문서의 기본값.
> **화면 정본은 확정 시안이다(0.3.0 · D-20 · D-21)** — Claude Design 캔버스 「Interpret PWA」(사용자가 직접 고친다). 로컬 사본은 코드 레포 `design/project/*.dc.html` — 참고 자료이고 빌드에 넣지 않는다. 시안이 바뀌면 사본을 다시 받고 §6 · §7 을 맞춘다. **시안과 DEC 가 다르면 DEC 가 이긴다**(D-22 ~ D-25 · D-29 · D-31 은 시안보다 뒤에 정했거나 시안을 고친 결정이다). 시안에 없는 자리(네트워크 실패 로그인 · 오프라인 화면)는 이 문서 문구를 따른다.
>
> 이 레포는 public — Soniox 키 · 로그인 아이디 · 비밀번호 · 세션 비밀값 · 실명을 쓰지 않는다. env 는 **이름만**(D-06 · D-11).

## 변경 이력

| 버전 | 날짜 | 무엇 |
|---|---|---|
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

## 1. 범위 — D-01 · D-02 · DEC Scope · D-41

| In | Out(DEC Scope Out) |
|---|---|
| 로그인(계정 하나) · 통역 화면(양방향 실시간 · 자막 · TTS) · 듣기 방식 전환(자동 듣기 · 누르고 말하기 — D-36) · 용어집 context · **통역 기록 — 서버에만(D-41 · §5.9)** · PWA · 로컬 실행 · Mac Studio 배포 | 통역 기록을 보는 화면 · API(D-41 「내부 검토용」) · 여러 계정 · 권한 · 자동 언어 맞추기(DEC Option B) · ccc(cc-prototype) 변경 |

- **0.6.0 — 통역 기록은 back 의 볼륨(PVC)에만 남긴다**(D-41 · §5.9): 세션 언어 · 시작/끝 시각 · 확정 발화의 원문 · 번역 · 말한 쪽 · 걸린 term id · 날짜별 JSONL · 7일 뒤 삭제 · 음성 없음. 화면 · API 로는 내지 않는다(§3.5 허용 경로 6개 그대로) — 꺼내는 건 코디가 클러스터에서(§9.6). front 는 지금처럼 화면을 떠나면 지운다. (0.5.0 까지의 「어디에도 저장하지 않는다」는 D-41 로 바뀌었다.)
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
│   │   ├── service/           # auth.py · glossary.py(시드 로더 · 검사 · context — 메뉴 행 없음) · interpret/{session,soniox,assembler,chinese,langs}.py · records.py(통역 기록 · 걸린 term · 7일 삭제 — 0.6.0 · §5.9)
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
| `GLOSSARY_CONTEXT_MAX_CHARS` | back — context 줄이기 기준(§4.6). **값이 있으면 7개 언어 모두를 그 값 하나로 덮는다**(언어별 표보다 작든 크든) | **언어별 표**(§4.6 — en 23,424 · ja 20,419 · zh 20,933 · zh-Hant 21,689 · th 21,343 · vi 22,891 · yue 21,123 · 시드 `.6` 실측 통과 최대치 × 0.9 내림). **운영 ConfigMap · Secret 에는 넣지 않는다**(넣으면 언어별 표가 꺼진다) | WP16 코디 처분 3 2026-10-27 (0.6.1 — 0.4.1 의 단일 기본값 20251 을 고침) |
| `NEXT_PUBLIC_API_BASE_URL` | front 빌드 — 브라우저가 부르는 back 주소(http · ws 둘 다 여기서) · 읽는 곳은 §2.3 한 줄 | `http://localhost:8800` | 원형 |

- **`GLOSSARY_MATRIX_URL` 은 지운다(0.4.0 · D-33)** — back 은 Procedure Hub 를 부르지 않는다. matrix 주소는 가져오기 스크립트 상수 · `--url` 인자로만(§4.8). 시드 경로는 env 가 아니다(`back/seed/glossary.json` 고정 · §4.2).
- `.env.example` 은 이름만 — `INTERPRET_DEMO_LOGIN=` · `GLOSSARY_CONTEXT_MAX_CHARS=` · `INTERPRET_RECORD_DIR=`(0.6.0) 도 값을 비우고 주석에 기본값만(WP6-BE · 폰 피드백 2 방식). `GLOSSARY_CONTEXT_MAX_CHARS` 주석 = 「비면 언어별 표 · 넣으면 모든 언어를 그 값 하나로」(0.6.1).
- `INTERPRET_RECORD_DIR` 은 비밀값이 아니다(경로) — 운영은 ConfigMap(§9.6). 로컬에서 켜 보려면 **레포 밖 경로**(기록 파일에 대화 문장이 들어간다 — 레포 · 커밋에 들어가지 않게).
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

## 4. 용어집 — 우리 시드 파일 — D-33(D-05 · D-13 · D-14 개정) · D-17 · D-18 · D-19 · D-28 · D-32 · D-35 · D-37 · D-38 · D-39 · D-40

> 0.4.0 — **용어집 정본은 레포의 시드 파일**이다(D-33). Procedure Hub matrix 는 **첫 가져오기 원천**일 뿐 back 이 런타임에 부르지 않는다.
> 0.5.0 — 시드에 **대만 현지명**을 넣었다(D-35 · §4.2.1) · **용어집 메뉴 API 를 지웠다**(D-37 · §4.7) — 시드는 Soniox `context` 로만 쓴다.
> 0.6.0 — 사전 밖 **새 시술 13개**를 7개 언어로 더하고(D-39 · §4.2.2) **대륙 중국어를 검증**했다(D-40 · §4.2.3). 내용 규칙을 언어 공통으로 다시 썼다(§4.2.1). 스키마 · 로더 · context 조립 · 줄이기 규칙은 그대로다(검사 7 하나만 더함).
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
| `version` | 필수 | 문자열 `YYYY-MM-DD.n` | 시드 판. **고칠 때마다 올린다**(PR 마다). back 기동 로그 · 통역 기록 세션 시작 줄(§5.9)에만 쓴다(0.5.0 — 응답에 내지 않음 · §3.5). 배포본 main 2a9d5a5 = `2026-10-27.5`(D-38) → **0.6.0 판 = `2026-10-27.6`**(§4.2.2 · §4.2.3 · 판 번호를 이어 간다) |
| `langs` | 필수 | 문자열 배열 | 이 파일이 다루는 앱 lang — **정확히 7개** `["en","ja","zh","zh-Hant","th","vi","yue"]`(back `langs.py` `APP_LANGS` 와 같은 집합 · 순서 무관) |
| `imported_from` | 선택 | 객체 `{source, url, version, count, at}` | 첫 가져오기 기록(§4.8). 런타임은 읽기만 하고 쓰지 않는다 |
| `terms` | 필수 | 배열(1개 이상) | 시술. **배열 순서 = context 순서** |

**term(시술)**

| 필드 | 필수 | 타입 | 뜻 |
|---|---|---|---|
| `id` | 필수 | 문자열 `[a-z0-9-]+` | 바뀌지 않는 이름. 파일 안 유일. **붙이는 규칙**: 첫 가져오기 = `ph-001` ~ (matrix 순서) · **조사로 더한 Procedure Hub 밖 시술 = `kr-001` ~ (더한 순서 · 3자리 · 번호를 다시 쓰지 않는다 — 0.6.0 · D-39)** · 손으로 더한 단발 = `m-<짧은 영문>`(지금 0개). 한 번 붙인 `id` 는 바꾸지 않는다 — 통역 기록의 걸린 term(§5.9)이 이 값을 남긴다 |
| `category` | 필수 | 문자열(비지 않음) | 카테고리 — 사람이 시드를 읽을 때 묶음(0.5.0 — 메뉴가 없어 런타임은 안 쓴다) |
| `ko` | 필수 | 문자열(비지 않음) | **ko 대표명** — 정방향 source · 역방향 target |
| `ko_aliases` | 선택 | 문자열 배열(기본 `[]`) | ko 별칭(예 상담사가 줄여 부르는 이름). 정방향 source 로만 쓴다 |
| `entries` | 필수 | 객체 `{<lang>: entry}` | 언어별 표기. 키 ⊆ `langs`. **없는 언어는 그 언어 context 에서 이 시술이 빠진다**(전부 채울 필요 없음) |
| `note` | 선택 | 문자열 · null | 사람 메모(예 손 편집의 출처 — 「사용자 지적 2026-10-26 …」) · 런타임은 안 쓴다 (0.4.1 — backend 가 더함) |

**entry(언어별 표기)**

| 필드 | 필수 | 타입 | 뜻 |
|---|---|---|---|
| `name` | 필수 | 문자열(비지 않음 · **괄호 `(` `)` `（` `）` 0**) | **현지명** — 그 언어 손님이 부르는 이름. 정방향 target · 역방향 source · TTS 가 읽는 말 |
| `aliases` | 선택 | 문자열 배열(기본 `[]` · 괄호 0) | 그 언어의 다른 이름(영문 상표명 · 현지 별명 등). **역방향 source 로만** 쓴다 |
| `source` | 필수 | `"procedure-hub"` · `"draft-s2twp"` · `"manual"` · **`"web-research YYYY-MM-DD"`**(0.5.0 · D-35 — 날짜 모양까지 검사 · `web-research` 만 · 날짜 모양이 틀리면 오류) 중 하나 | 출처 — 가져온 것 · zh-Hant 기계 초안(이름은 스키마 값 그대로 — 변환은 §4.8) · 사람이 쓴 것 · 웹 조사로 넣은 것(조사 날짜). **0.6.0**: 조사 리포트로 정한 값(찾은 현지명이든, 조사로 「현지에 없음」을 확인해 영문으로 둔 것이든) = `web-research 2026-10-27` · 조사 없이 규칙으로만 고친 데이터 결함(§4.2.3 C) = `manual` |
| `reviewed` | 필수 | bool | 검수 여부. `false` = 사람이 아직 안 본 초안 · 출처가 하나뿐인 조사값(§4.2.1). context 에는 **그대로 넣는다**(검수 여부로 빼지 않는다 — 기본값 · D-33 은 초안을 넣고 사용자가 고친다고 했다). 0.5.0 — 메뉴가 없어 화면에 보이지 않는다 · 검수 목록은 시드 파일에서 `reviewed:false` 로 찾는다 |
| `raw` | 선택 | 문자열 · null | 가져오기 때 원문(괄호 분해 전) — 분해가 원문과 다를 때만. 검수용 · 런타임은 안 쓴다 |
| `note` | 선택 | 문자열 · null | 사람 메모 · 런타임은 안 쓴다. `web-research` entry 는 대표 출처 URL 1개(D-35) — 0.6.0 · 「현지에 없음 = 영문」 entry 는 URL 대신 `현지 출처 없음 — <리포트 파일 이름>`(근거가 부재라 가리킬 URL 이 없다) |

예(값은 2026-10-27 matrix 를 §4.8 규칙으로 바꾼 모양 — 실제 파일은 스크립트가 만든다):

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
| zh · zh-Hant | `热玛吉`(브랜드 전체 — 4세대 CPT · 5세대 FLX) · `黄金微针`(射频微针 장르) · `童颜针`(PLLA · PDLLA 장르) · `素颜` · `素妍` · `凤凰` · `仙女` · `彩虹针` | **name · alias** | D-38 ④ · D-40 · 처분 r1-6 · 조사 r1 표 C · r2 표 C |
| zh · zh-Hant | `超声刀` · `韩版超声刀` · `韩版热玛吉` | **alias**(0.5.0 그대로) — 0.6.1: zh name 으로 남았던 ph-123 「韩版热玛吉」 · ph-126 「韩版超声刀」 도 영문으로 바꿔(§4.2.3 D · OQ-018 ①) **name · alias 모두 0** | D-35 · OQ-018 처분 ① |
| yue | `黃金微針`(홍콩은 Exion · 대만은 바늘 종류) · `童顏針` · `膠原槍` · `韓國仙女針` · `舒膚微`(출처 1 · 다른 음역) | **name · alias** | 조사 r3 표 C |
| yue | `水光針`(스킨부스터 공통 꼬리) | **alias** — ph-074 · ph-078 의 name 「水光針」 은 물광 시술 자체 이름이라 그대로 | 조사 r3 표 C-4 |
| ja | `サーマクール`(단독 — CPT · FLX · アイ) | **name · alias** | 조사 r2 표 C-1 |
| en · th · vi | `Thermage`(단독) · `Density` · `Revive` · `Tesla`(일반 단어 · 다른 회사) | **alias** — 덴서티의 `name` `DENSITY` 는 브랜드라 둔다(OQ-019) | 처분 r2-8 · 조사 r2 표 C-4 ~ C-7 |

- 시험(§9.1 「시드」 ⑥)은 위 표를 그대로 상수로 갖는다. 표에 없는 말을 시험이 스스로 늘리지 않는다 — 늘리려면 이 표를 고친다.
- 기존 시드의 `水光`(ph-089 물광) · `水光针`(ph-074 · ph-078)은 그 시술의 현지 이름(물광 = 水光)이라 R4 대상이 아니다.
- `.5` 기준 이 표에 걸리는 값 = zh ph-130 alias `热玛吉` · zh-Hant ph-130 alias `熱瑪吉` · zh ph-135 name `黄金微针` — 셋 다 `.6` 에서 지운다(§4.2.3 A). 그 밖은 0(확인 2026-10-27 · `.5` 대조).

**지금까지 반영한 판**

| 판 | 결정 | 무엇 | 수치 |
|---|---|---|---|
| `.4` | D-35 | zh-Hant 대만 현지명(조사 77/157) · 초안은 alias · 「鐳射」 → 「雷射」 · zh 「热玛吉」 alias(**0.6.0 에서 뺌**) · 볼뉴머 카테고리 기기 리프팅 | `web-research` 77 · `reviewed:true` 38 |
| `.5` | D-38 | zh-Hant 2차(대만 클리닉 3곳 전수 대조 · 40 term) — 톡신 대만 허가명(保提拉 · 優力柔 · 娜柏塔) · **대만에 없는 한국 전용 제품 19개 = 영문 name**(`manual` · `reviewed:false` — 이 판은 「현지에 없음」도 `manual` 로 적었다) · 대륙식 · `s2twp` 오변환 정리 · 모호어 제거 · 포텐자 zh-Hant 無限電波(검수 전) | 배포 main 2a9d5a5(PR #9) · infra #34 — 0.6.0 에서 뒤늦게 기록 |
| **`.6`** | **D-39 · D-40** | **새 시술 13 term × 7개 언어**(§4.2.2) · **기존 표기 변경**(§4.2.3) · 검사 7 | §4.2.2 · §4.2.3 표 그대로 |

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

### 4.5 언어별 `context` 조립 (D-05 · D-18 · D-33)

통역 연결(§5.3 `start`) 때 고른 언어 `L` 로 Soniox STT 설정에 `context` 를 넣는다. 칸(`general` 고정 3쌍 · `text` 안 넣음)은 0.3.0 그대로.

**재료** — 시드 순서대로 `entries[L]` 이 있는 term 만. 간체화 `norm`: **`L ∈ {yue, zh-Hant}` 면 OpenCC `t2s`**(Soniox 의 중국어 출력은 간체 — 번체 source/target 이 간체 출력 사이에 섞이고 TTS 로 가면 발음이 깨진다 · D-17 · 0.3.0 §4.3 의 yue 이유와 같음), 그 밖은 그대로. 괄호는 시드에 없다(§4.2) — 가공 없음.

| 칸 | 넣는 것(이 순서) | 근거 |
|---|---|---|
| `general` | 0.3.0 고정 3쌍 그대로 | 입력 1 |
| `terms` | ① ko 대표명 전부(시드 순서) ② 그 뒤 ko 별칭 전부(시드 순서 · term 안 순서) | D-05 「`terms` 는 ko 표기」 |
| `translation_terms` | **정방향 기본** `{source: ko, target: norm(name)}` → **정방향 별칭** `{source: ko 별칭, target: norm(name)}` → **역방향 기본** `{source: norm(name), target: ko}` → **역방향 별칭** `{source: norm(alias), target: ko}` | D-05 정방향 · D-18 역방향 · D-33 「정방향 = ko 대표명 · ko 별칭 → 현지명, 역방향 = 현지명 · 별칭 → ko 대표명」 |

- 역방향 source 중복(다른 시술의 같은 현지명 · `norm` 뒤 같아진 것 · 현지명과 다른 시술 별칭이 같음)은 **위 순서에서 처음 짝만** 둔다(0.3.0 규칙 그대로 — 기본 짝이 별칭 짝보다 앞).
- 정방향 source 중복은 §4.2 검사 3 이 막는다(조립에서 다시 거르지 않는다).
- **zh-Hant 는 zh-Hant entry 를 쓴다(0.4.0)** — 0.3.0 · D-28 의 「zh-Hant target 은 zh 열」은 시드에 zh-Hant 표기가 없을 때의 대안이었다. D-33 이 zh-Hant 표기를 시드에 두고 D-32 가 「대만 현지 별명은 그 언어 표기를 추가해서 해결」이라 했으므로, 대만 손님이 부르는 이름(예 美國音波)이 Soniox 에 닿으려면 zh-Hant entry 가 context 재료여야 한다. **0.5.0 — D-35 로 대만 현지명 77개가 들어가 zh-Hant context 는 zh 와 실제로 다르다**(정방향 target 美國音波 · 역방향 source 美國音波 · 極線音波 등 → `t2s` 뒤 美国音波 …). OQ-013 닫음.
- 크기 로그(§4.6 5번)는 칸 수를 넷으로 나눠 적는다: `terms` · 정방향(기본 · 별칭) · 역방향(기본 · 별칭) · 뺀 수 · 글자 수.

**구조로 들고 다닌다(0.4.0)** — 조립 결과를 Soniox dict 하나로 합쳐 두고 나중에 「앞 정방향의 거울인 첫 짝」으로 정방향/역방향 경계를 다시 찾지 않는다(별칭 짝이 생기면 거울 추측이 틀린다 · 0.3.0 `split_translation_terms`). `build_context` 는 네 묶음을 따로 가진 값(예 `ContextParts{general, terms, forward, forward_alias, reverse, reverse_alias}`)을 내고, Soniox 설정 dict 는 `to_soniox(parts)` 로 만든다. `forward_only(parts)` · `is_forward_only(parts)` 도 이 값으로.

### 4.6 한도 — 줄이기 (D-05 · D-18 · 0.3.0 §4.4 를 넷으로)

Soniox context 한도는 **8,000토큰** · 넘으면 `invalid_request`(공식 문서). back 은 글자 수로 미리 줄이고, 그래도 거절되면 한 번 더 줄인다.

1. `to_soniox(parts)` 를 `json.dumps(ensure_ascii=False)` 한 길이를 잰다.
2. **그 언어의 기준**(아래 언어별 표 · env `GLOSSARY_CONTEXT_MAX_CHARS` 가 있으면 그 값)을 넘으면 아래 순서로 **하나씩 뺀다** — 넘지 않을 때까지.
   1. **`terms`** — 뒤에서부터(ko 별칭이 먼저 빠지고 그다음 대표명 뒤쪽부터)
   2. **역방향 별칭** — 뒤에서부터
   3. **역방향 기본** — 뒤에서부터
   4. **정방향 별칭** — 뒤에서부터
   5. **정방향 기본 · `general` 은 줄이지 않는다**(D-05 우선). 다 빼도 넘으면 그대로 연결해 본다(4번이 받는다)
3. 2번을 거친 설정으로 STT 를 연다(§4.6.1 확인).
4. 연결 직후 `invalid_request` 로 거절되면 **`general` + 정방향 기본만**(`forward_only`)으로 STT 만 1회 다시 연결. 그것도 거절되면 `error soniox_unavailable`. 보낸 설정이 이미 정방향 기본만이면 재연결 없이 바로 `soniox_unavailable`. 용어집 없이 몰래 연결하지 않는다.
5. 실제로 보낸 칸 수(§4.5 끝)를 언어별 정보 로그 1줄 — 용어 문자열 0 · 끝에 `max=<그 언어 기준>`(0.6.1).

**줄이기 기준 = 언어별 표 (0.6.1 · 시드 `.6` 실측 · WP16 코디 처분 3)**

| lang | 기준(글자) | 통과 최대치(⑬′) | 거절 최소치 | 줄이기 없는 전체(`.6`) |
|---|---|---|---|---|
| en | **23,424** | 26,027 | 26,069 | 17,589 |
| ja | **20,419** | 22,688 | 22,771 | 19,408 |
| zh | **20,933** | 23,259 | 23,347 | 18,565 |
| zh-Hant | **21,689** | 24,099 | 24,142 | **24,750 — 그대로는 거절** |
| th | **21,343** | 23,715 | 23,833 | 20,804 |
| vi | **22,891** | 25,435 | 25,512 | 17,596 |
| yue | **21,123** | 23,471 | 23,557 | 17,636 |

- 기준 = 언어별 통과 최대치 × 0.9 **내림**. 표는 코드 **한 곳**(back `service/interpret/langs.py` `CONTEXT_MAX_CHARS` · `context_max_chars(lang, override)`)에만 둔다 — config · container · `live_check.py` 가 같은 함수를 쓴다.
- **env `GLOSSARY_CONTEXT_MAX_CHARS`** = 비면 언어별 표 · **값이 있으면 7개 언어 모두를 그 값 하나로**(언어별 값보다 작든 크든 — 실험 · 비상용 덮어쓰기). 언어별 env 는 두지 않는다. 운영 ConfigMap · Secret 에는 넣지 않는다(§2.4 · §9.6).
- 재는 법(⑬′): 전체가 통과하는 6개 언어는 ⑬ 과 같은 padding 이분 탐색. **zh-Hant 는 전체(24,750)가 거절돼 padding 이 안 된다** → `build_context(max_chars=m)` 로 실제 보낼 모양을 만들어 `m` 을 이분 탐색(`live-check-wp16-ceiling.json` `trim_search`).
- **왜 언어별로**(0.6.0 → 0.6.1): `.6` 에서 공통 기본값(가장 작은 ja 기준)으로는 zh-Hant 역방향 별칭 63 · th `terms` 38 이 빠졌다(20,419 · ⑲ 다시) — 다른 언어의 한도에 묶여 넉넉한 언어가 짝을 잃었다. 언어별 표로 th 뺀 수 0 · zh-Hant 역방향 별칭 63 → 33.
- **남는 손실**: zh-Hant — `terms` 170 전부 · 역방향 별칭 33(시드 뒤쪽 = 새 시술 · 대만 2차 별칭). 전체가 실제 한도를 넘어 줄이기 없이는 거절되므로 피할 수 없다 — 더 살리려면 별칭 정리(시드) 또는 줄이기 순서 변경(계약)이고 0.6.1 은 둘 다 하지 않는다. 다른 6개 언어 뺀 수 0.
- 시드가 다시 크게 바뀌면(별칭 · term 추가) ⑬′ 방법으로 다시 재서 이 표 · `langs.py` 를 같이 고친다(코디 · 사용자 판정 — 워커가 표를 바꾸지 않는다).

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

## 5. 통역 WS — D-03 · D-04 · D-17 · D-19 · D-28 · D-33 · D-35 · D-37 · D-41

### 5.1 원형과 무엇이 같고 무엇이 다른가

| 항목 | 원형(`procedure/back`) | 이 레포 | 근거 |
|---|---|---|---|
| 중계 구조 | 브라우저 WS 하나 ↔ back ↔ Soniox STT(two_way) + TTS 두 연결 · 세션이 끝나면 둘 다 닫음 | **그대로** | D-03 · 개념 websocket-relay |
| 메시지 종류 · 오디오 형식 | §5.3 표 | **그대로** | 원형 `interpret-ws-contract.md` · `session.py` |
| 발화 묶기 · 자막 갱신 | `assembler.py`(`<end>`/`<fin>` 까지 한 발화 · non-final 갈아 끼움 · 같은 caption 재전송 안 함 · zh · ja · th 빈칸 정리) | **그대로** | 원형 · 개념 nondeterministic-stt-output |
| Soniox 모델 · 음색 · 샘플레이트 · keepalive 주기 | `stt-rt-v5` · `tts-rt-v2` · 음색 `Jiwoo` · 16k 입력 · 24k 출력 · 10초/20초 keepalive · stop 뒤 3초 드레인 | **그대로** | 원형 `soniox.py` · `session.py` |
| TTS keepalive **메시지 모양** | `{}` | **`{"keep_alive": true}`**(공식 형식) · 다른 stream_id 의 오류는 발화를 끊지 않음(§5.8 · 0.5.0) | 운영 장애 2026-10-27 · Soniox 공식 문서 |
| `start` 의 `lang` | 8개 `{zh,en,ja,th,fr,es,tl,hi}` | **7개 `{en, ja, zh, zh-Hant, th, vi, yue}`** — 앱 언어 코드(§5.5 · 0.4.0 zh-Hant 추가) | D-04 · D-28 |
| `start` 의 `traditional` | front 가 보냄 | **없앤다** — 번체 여부는 `lang` 이 정한다(§5.6). 와도 무시 | D-17 |
| `start` 의 `scheduleId` | 받아서 버림 | 없앤다(와도 무시). 0.6.0 통역 기록(§5.9)은 back 이 세션 id 를 스스로 만든다 — front 가 보내는 값을 쓰지 않는다 | Scope · D-41 |
| STT 설정 | `context` 없음 | **`context` 를 넣는다**(§4.5 · §4.6 — 시드의 정방향 + 역방향 · 0.4.0) | D-05 · D-18 · D-33 |
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

### 5.9 통역 기록 — 서버 볼륨에만 · 화면 · API 없음 (0.6.0 — D-41)

> 「어떤 통역을 했는지 궁금해서」 · 「poc 라 시연 정도만」 · 「화면이 필요 없다 · 내부 검토용」(D-41). 기록은 back 이 볼륨에 쓰고, 코디가 클러스터에서 꺼내 본다(§9.6). **밖으로 내는 것은 그대로 6개 경로뿐**(§3.5 · D-37).

**저장 위치**

| 항목 | 계약 |
|---|---|
| 폴더 | env **`INTERPRET_RECORD_DIR`**(§2.4). 운영 = back PVC 마운트 `/data` 아래 **`/data/records`**(§9.6). **비면 기록 끔**(로컬 · 시험 기본) — 파일도 삭제 작업도 없다 |
| 기동 | lifespan 에서 ① 폴더가 비었으면 정보 로그 1줄 `interpret records: off` ② 있으면 `mkdir -p` · 쓰기 가능한지 확인 → 정보 로그 1줄 `interpret records: on dir=<경로> keep_days=7` ③ 만들기 · 쓰기 확인이 실패하면 **경고 로그 1줄(예외 종류만) 뒤 그 프로세스는 기록 끔으로 뜬다** — 기록 때문에 기동을 멈추지 않는다(시드와 다르다 · §4.4 — 기록은 통역의 부속이다) ④ 7일 삭제 1회(아래) |
| 파일 | **날짜별 하나** — `<폴더>/<YYYY-MM-DD>.jsonl`. 날짜 = 그 줄 `at` 의 **한국 시간(UTC+9 고정 · 서머타임 없음)** 날짜. 자정을 넘긴 세션은 두 파일에 나뉜다(세션 id 로 잇는다). 인코딩 UTF-8 · 한 줄 = JSON 객체 하나(`ensure_ascii=False` · 줄바꿈 없음) · 끝에 `\n` |
| 쓰기 | 줄마다 append 1회(`open(…, "a")` · 한 번의 `write` · flush · fsync 하지 않음). 한 프로세스 안 쓰기는 직렬(이벤트 루프에서 동기 append 또는 잠금). 줄 하나는 수 KB 이하라 같은 노드의 두 pod 가 겹쳐 써도(롤링 · §9.6) 줄이 섞이지 않는다 — 기본값 |

**줄 모양** — 세 종류. 키는 아래 순서 · 여기 없는 키 0.

```json
{"type":"session_start","session":"9f2c4e7a1b3d5f60","at":"2026-10-28T14:03:11.204+09:00","lang":"zh-Hant","seed":"2026-10-27.6"}
{"type":"utterance","session":"9f2c4e7a1b3d5f60","at":"2026-10-28T14:03:19.882+09:00","lang":"zh-Hant","id":"u1","side":"me","original":"써마지 CPT 하고 프로파일로 같이 하실 수 있어요","translation":"您可以同時做黃金電波和逆時針","terms":["kr-001","kr-007"]}
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
| `id` · `side` · `original` · `translation` | utterance | 그 발화의 **`final:true` caption 과 같은 값**(§5.3 — 화면에 나간 자막 그대로 · zh-Hant · yue 는 번체 변환 뒤 · 괄호도 그대로 · TTS 입력이 아니다) |
| `terms` | utterance | 걸린 term `id` 목록(아래 판정) — 시드 순서 · 중복 없음 · 없으면 `[]` |
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

**7일 뒤 삭제**

| 항목 | 계약 |
|---|---|
| 대상 | 폴더 안 이름이 정확히 `YYYY-MM-DD.jsonl` 이고 그 날짜가 **오늘(한국 시간) − 7일 이하**인 파일 — 예 10-28 에는 10-21 파일까지 지운다(그날 쓴 기록은 꽉 찬 7일을 산다). 이름이 그 모양이 아닌 파일 · 폴더는 건드리지 않는다 |
| 때 | **기동 때 1회 + 그 뒤 24시간마다**(lifespan 의 배경 작업 · 종료 때 취소). 기록 끔이면 돌지 않는다 |
| 실패 | 파일 하나 지우기 실패 → 경고 로그 1줄(예외 종류 · 파일 이름) 뒤 다음 파일 계속. 작업 전체가 죽지 않는다 |
| 로그 | 지운 파일 수 1줄(`interpret records sweep: deleted=N`) — 내용 0 |
| 보관 기간 | **7일 고정**(D-41 · 코디 기본값) — env 로 바꾸지 않는다. 바꾸려면 DEC → 이 절 |

**쓰기 실패는 통역을 끊지 않는다**

- 줄 쓰기에서 나는 예외(`OSError` 등 — 디스크 가득 · 권한 · 폴더 사라짐 · 직렬화)는 기록 쪽에서 삼킨다 → **경고 로그 1줄**(`interpret record write failed: <예외 종류>` — 문장 · 경로 밖 값 0) · 그 세션의 남은 줄은 계속 시도하되 **경고는 세션당 1번만**(로그 홍수 방지).
- 통역(caption · 오디오 · `ready` · 오류 코드)은 기록 성공 여부와 무관하게 지금과 같다. 기록 실패로 `error` 프레임을 보내거나 연결을 닫지 않는다.
- 판정(`terms`) 계산에서 나는 예외도 같은 처리 — 그 줄은 `terms: []` 로 쓴다.

**화면 · API 없음** — 기록을 읽는 코드 · 경로 · 화면 · 다운로드를 두지 않는다(§3.5 허용 경로 6개 그대로 · `tests/test_api_surface.py` 가 고정). front 는 바뀌지 않는다. 꺼내기는 §9.6.

- 일반 로그에는 지금처럼 발화 원문 · 번역문을 쓰지 않는다(§5.8) — 대화 문장은 기록 파일에만.

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

## 9. 검증 — 완료 조건 — D-03 · D-05 · D-12 · D-33 · D-35 ~ D-41

### 9.1 back 시험 (pytest · Soniox 가짜 · 시드는 가짜 + 실제 파일)

| 묶음 | 시험 |
|---|---|
| 로그인 | 맞는 아이디 · 비밀번호 → 200 `{token, expiresAt}` · 틀림(아이디만 · 비번만 · 둘 다) 같은 401 · 필드 빠짐 400 · 5회 실패 → 429 · 1분 뒤 풀림 · env 비면 401 · 만료 토큰 401 · env 아이디 바꾸면 기존 토큰 401 · `/api/auth/me` · 망가진 토큰(ASCII 아님 · 점 개수 · base64 · JSON) → HTTP 401 · WS 1008(500 0) · 로그인 env 빈 채 기동 → 경고 로그 1줄(이름만 · 값 0) · 응답은 같은 401 |
| 데모 로그인(0.4.0 · D-30) | 꺼짐: `config` `{demoLogin:false}`(토큰 없이 200) · `demo` 404 `not_found` / 켜짐: `config` true · `demo` 200 `{token, expiresAt}` · 그 토큰으로 `/api/auth/me` = env 아이디 · 응답에 비밀번호 0 / 잠긴 상태에서도 demo 200 · demo 뒤에도 잠금 그대로 / 켜짐 + 로그인 env 빈 것 → demo 401 / env 파싱 `true` · `1` 켬 · `false` · 빈 값 끔 |
| **시드(0.4.0 · D-33 · 0.5.0 D-35)** | **① 레포의 실제 `back/seed/glossary.json` 을 로더와 같은 검사 함수로 읽어 통과**(이 시험이 깨진 시드의 머지를 막는다 — §4.4) ② 가짜 시드로 §4.2 검사 하나씩 어김 → `SeedError`(파일 없음 · JSON 아님 · `schema` 다름 · `version` 모양 · `langs` 집합 다름 · 필수 필드 빠짐 · 타입 · `id` 모양 · `id` 중복 · `ko` · `ko_aliases` 겹침 · entry 키가 `langs` 밖 · `name` 빔 · `name` · `aliases` 괄호 · `source` 값 · `reviewed` bool 아님 · entry 안 겹침 · 앞뒤 공백 · 줄바꿈) · 오류 문구에 경로 · `id` ③ 시드가 깨지면 앱 lifespan 기동이 실패한다(빈 용어집으로 뜨지 않음) ④ 다른 시술의 같은 현지명은 통과 ⑤ `grep` 대신 시험: back 런타임 모듈에 matrix 주소 · `GLOSSARY_MATRIX_URL` 없음(§4.9) ⑥ **(0.6.0 · §4.2.1 ~ §4.2.3) 레포 시드 내용** — `version` `2026-10-27.6` · **§4.2.2 표 그대로**(`kr-001` ~ `kr-013` 이 배열 맨 뒤 이 순서 · `ko` · `category` · 언어 7개 × `name` · `aliases`(순서까지) · `reviewed` · `source` `web-research 2026-10-27` · `note` 가 URL 또는 `현지 출처 없음 — ` 로 시작) · **§4.2.3 표 그대로**(A · B · C 의 name · aliases · `reviewed` · `source` — C 는 `manual`) · **모호어 목록(§4.2.1) 금지 자리마다 0**(zh · zh-Hant · yue `t2s` 뒤 · 라틴 `casefold` 뒤) · 보이지 않는 글자 0(검사 7 — 가짜 시드로 U+200C 하나 → `invisible_char`) · 기존 157 term 의 `id` 순서 그대로 · 0.5.0 항목 중 유지: 울쎄라 zh-Hant 美國音波 · 써마지FLX zh-Hant 鳳凰電波 · 볼뉴머 기기 리프팅 · zh-Hant 「鐳射」 0 / **0.5.0 의 「zh 「热玛吉」 있음」 · 「`web-research` 77 · `reviewed:true` 38」 고정값은 지운다**(`.5` · `.6` 에서 바뀜 — 개수 대신 표 대조) / `source` 검사: `web-research`(날짜 없음) · 날짜 모양 틀림은 오류 · `web-research 2026-10-27` 통과 ⑦ **(0.6.1 · §4.2.3 D) OQ-018 처분 표 그대로**(ph-123 · ph-126 zh · ph-121 yue · ph-113 zh · th) · **ph-130 `ko_aliases == []` · 어느 term 에도 ko 별칭 「써마지」 0** |
| context | (0.4.0 · §4.5 · §4.6) 순서 = 정방향 기본 → 정방향 별칭 → 역방향 기본 → 역방향 별칭 · `terms` = 대표명 뒤 ko 별칭 · `entries[L]` 없는 시술은 빠짐 · `yue` · `zh-Hant` 는 `t2s`(정방향 target · 역방향 source 둘 다) · zh 는 그대로 · zh-Hant 는 zh-Hant entry 를 씀(zh entry 아님) · 역방향 source 중복은 처음 짝(기본이 별칭보다 앞) · 줄이기 순서 `terms`(별칭부터) → 역방향 별칭 → 역방향 기본 → 정방향 별칭 · **정방향 기본 · `general` 은 줄지 않음** · `forward_only` = `general` + 정방향 기본만 · `is_forward_only` · 그 언어 entry 0 이면 `context` 키 없음 · 경계를 거울 추측 없이 구조로 들고 다님(별칭 짝이 있어도 `forward_only` 가 정확) · **(0.6.1) 언어별 기준** — `CONTEXT_MAX_CHARS` 값이 §4.6 표와 같음 · 키가 7개 언어 · env 없으면 언어마다 표 값으로 조립 · env `15000` 이면 7개 언어 모두 15000(레포 시드로 `build_context` 결과와 같은지) · §4.6.1 가짜 Soniox 6건(0.3.0 그대로 — 설정 직후 `invalid_request` → 정방향 기본만 2번째 STT 연결 뒤 `ready` · 두 번 거절 → `soniox_unavailable` · TTS 안 열림 · 다른 `error_type` → 재연결 없음 · 2초 무응답 → `ready` · `ready` 뒤 `invalid_request` → 재연결 없음 · 처음부터 정방향 기본만이면 재연결 없음) · 로그 칸 수(용어 문자열 0) |
| ~~메뉴(0.4.0 · §4.7)~~ | 0.5.0 — 메뉴 API 삭제로 시험도 지움(D-37). 대신 아래 「밖으로 내는 것」 |
| **밖으로 내는 것(0.5.0 · §3.5 · D-37)** | `tests/test_api_surface.py` — **앱 경로가 정확히 6개**(그 밖 Route 가 있으면 실패) · `/docs` · `/redoc` · `/openapi.json` · `/docs/oauth2-redirect` · `/api/glossary` → 404 일반 문구 · 응답 최소 모양(health `{ok:true}` · me `{ok:true}` · config `{demoLogin}`) · **허용 경로 전부(성공 · 401 · 404)의 응답에 시드 판 · 시드 낱말 0** · `app/api` · `app/schemas` 소스에 `glossary` · `.terms` · `.entries` · `menu_rows` · `load_seed` · `build_context` 0 · 오류 일반 문구(검증 400 · 405 · 데모 꺼짐 404 · 처리기 밖 예외 500 — 예외 내용이 응답에 없고 로그에 종류) · WS 문구 4개에 `SONIOX` · `Soniox` · `.env` · `API_KEY` · `start` · `type` · `JSON` 0 · 받은 `lang` 을 되돌려 보내지 않음 |
| 가져오기 스크립트(0.4.0 · §4.8) | 저장한 matrix 가짜(`--from-file`)로: 괄호 분해 다섯 모양(없음 · 라틴(현지) · 현지(라틴) · 같음 · 그 밖 → `reviewed:false` · 괄호 뺀 이름 · `raw`) · 반각 · 전각 · 앞 공백 · 줄바꿈 정리 · 같은 `ko` 행 합치기(뒤 행 다른 표기 → 처음 term `aliases`) · zh-Hant = 분해 뒤 zh 의 `to_display("zh-Hant")`(0.5.0 — 「离子导入 → 離子導入」 · 「激光导入 → 雷射導入」 · 「特色项目 → 特色項目」) · `draft-s2twp` · `reviewed:false` · 빈 칸이면 entry 없음 · `id` = `ph-001` 순서 · 머리 `imported_from` · 출력이 §4.2 검사 통과 · **출력 파일이 이미 있으면 쓰지 않고 0 아닌 코드** · 같은 입력 두 번 → 같은 바이트(결정적) |
| 통역 | 원형 `test_interpret.py` 복사분(묶기 · 갱신 · 번체 자막 · TTS 간체 · flush · bad start · 전체 흐름 · 닫기 정리 · 오류 코드 · Origin · 토큰) + `lang` **7개** 매핑(§5.5) · `yue` · `zh-Hant` 는 Soniox 에 `zh` · **자막 변환 yue `s2tw`(「激光治療」) · zh-Hant `s2tw` + 표(「雷射治療」 · 「離子導入」 · 0.5.0 D-35) · `to_display` 「激光 软件 导入 项目 → 雷射 軟件 導入 項目」 · zh 간체 · 셋 다 TTS 입력은 간체**(§5.6) · `traditional` 이 와도 무시 · STT 설정에 `context` 가 들어감 · §5.7 괄호 제거 목록 — TTS 입력만 괄호 없음 · caption 은 괄호 그대로 · **(0.5.0 · §5.8) TTS keepalive 가 `{"keep_alive": true}` · 스트림 밖 검증 오류(`stream_id: ""`)가 와도 그 발화 오디오가 끝까지 나옴 + 경고 로그 · 자기 스트림 오류는 `SonioxError(channel="tts")` · 중계 중 오류 로그에 channel · message · lang · paused · stt_last · tts_last(len · lang) — 번역문 · 키 0** |
| **기록(0.6.0 · §5.9 · D-41)** | `tests/test_records.py` — 가짜 Soniox · `tmp_path` 폴더 · 시계 주입: ① 세션 1회(`start` → final caption 2 · non-final 1 → `stop`) → 오늘 파일 1개 · 줄 = `session_start` · `utterance` 2 · `session_end`(`reason=stop` · `utterances=2`) · 키 순서 · 여기 없는 키 0 · `at` `+09:00` · `seed` = 시드 판 ② 파일 날짜 = UTC+9 날짜(UTC 15:00 = 다음 날 파일) ③ `final:false` 안 씀 · 같은 `id` 두 번 → 1줄 · 둘 다 빈 caption 안 씀 ④ `bad_request`(lang 밖 · 첫 프레임 아님) → 줄 0 · `no_api_key` → start + end(`error` · `no_api_key`) · Soniox 거절 → end `soniox_unavailable` · 브라우저 닫힘 → `close` ⑤ **판정**: ko 대표명 · ko 별칭(0.6.1 — 레포 시드에 ko 별칭이 0개라 가짜 시드로) · L name · L alias 각각 걸림 · 「써마지 하실래요」 → `[]`(0.6.1 — 「써마지」 단독은 아무 term 도 아님) · zh-Hant 번체 자막 ↔ 시드(`t2s`) · 라틴 경계(「contact」 → `ACT` 아님 · 「ACT 시술」 → 걸림) · 공백 무시(「써마지 FLX」 → ph-130) · **더 긴 일치**(「써마지 CPT」 → `kr-001` 만 · 「벨로테로 리바이브」 → `kr-009` 만 · 짧은 이름이 ko 별칭인 경우는 가짜 시드) · `entries[L]` 없는 term 은 ko 로만 · 순서 = 시드 순서 · 없으면 `[]` ⑥ **넣지 않는 것**: 가짜 토큰 · 로그인 아이디 · 주입한 IP · Origin 문자열 · PCM 바이트가 파일에 0 ⑦ 폴더 비면 파일 0 · 삭제 작업 없음 · 로그 `off` / 쓸 수 없는 폴더 → 기동 성공 · 경고 1줄 · 기록 끔 ⑧ **쓰기 실패**(쓰기 함수가 `OSError`) → 그 세션 caption · 오디오 · `ready` 가 기록 없을 때와 같음 · `error` 프레임 0 · 경고 로그 세션당 1줄 ⑨ **7일 삭제**: 오늘 − 7 · − 8 일 파일 지움 · − 6 일 · 오늘 남김 · 이름이 다른 파일(`note.txt` · `2026-10-01.jsonl.bak`) 남김 · 기동 때 1회 · 24시간 뒤 다시(시계 · 잠 주입) · 지우기 실패 파일 하나 → 나머지 계속 ⑩ 표면: 허용 경로 6개 그대로(`test_api_surface.py` 변경 없이 통과) · 일반 로그 캡처에 발화 문장 0 |
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

- ⑲ ~ ㉑ 은 backend 가 로컬에서(WP16) · ⑳ 의 일부(3개 언어 1회) · ㉑ · 7일 삭제는 운영에서 다시(WP18 · §9.6).

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

- 반영 방식: Actions(main · arm64 · sha 태그) → infra `values-prod` 이미지 태그 PR → 머지 → ArgoCD **수동 sync**.
- 운영은 **데모 로그인 켬**(`INTERPRET_DEMO_LOGIN=true` — Secret · D-30). 데모가 끝나면 값만 지우고 back 재시작.
- **배포 주소 확인(코디 · 8차)**: `/api/health` · `/api/auth/me` → `{ok}` · `/api/glossary` 404 · `/docs` 404 · `wss /api/interpret` `start` → `ready`. (4차까지: 로그인 200 · manifest `name` 통키 · `short_name` Tongky · 데모 로그인 `demoLogin:true` · `/api/auth/demo` 200.) **사람 목소리 폰 E2E(D-35 대만명 · D-36 길게 누름)는 남음**(OQ-017).

### 9.6 배포 — 통역 기록 PVC (0.6.0 — D-41 · 선례 cc-prototype `procedure-db`)

**infra 차트 `charts/interpret-pwa`(k8s_infra_mac)** — 지금 back 은 볼륨 없는 무상태(차트 주석 「Stateless (no DB, no volume)」 · `podSecurityContext` 에 `fsGroup` 없음). 아래를 더한다.

| 항목 | 값 | 근거 |
|---|---|---|
| PVC | 이름 **`interpret-pwa-records`** · `ReadWriteOnce` · **`storageClassName: local-path`** · **1Gi** · 주석 `helm.sh/resource-policy: keep`(차트를 지워도 남는다) · 템플릿 `templates/back-pvc.yaml` · 이름 · 크기는 values(`back.recordsPvcName` · `back.recordsStorage` 류) | cc-prototype `back-pvc.yaml`(`procedure-db` · local-path · keep · 1Gi) |
| 크기 근거 | 한 줄 수백 B ~ 수 KB · 시연 규모(하루 발화 수백 ~ 수천) · 7일만 보관 → 수 MB. 1Gi 는 선례와 같은 최소 단위 · 남는 여유 | 기본값 |
| 마운트 | back 컨테이너 `/data` ← PVC · **ConfigMap `INTERPRET_RECORD_DIR=/data/records`**(비밀 아님 · `checksum/config` 로 pod 재시작) — 하위 폴더는 back 이 기동 때 만든다(§5.9) | §2.4 |
| 쓰기 권한 | `podSecurityContext.fsGroup: 10001` 을 더한다(이미지 uid/gid 10001 · `runAsUser` · `runAsGroup` 그대로) | cc-prototype values `fsGroup: 10001` |
| **노드 고정(prod)** | `values-prod.yaml` 에 **`back.nodeSelector: {kubernetes.io/hostname: lima-worker-1}`** · 템플릿에 `nodeSelector` 블록. **local-path 는 `lima-worker-1` 에서만 프로비저닝된다**(local-path-config `nodePathMap`) — WaitForFirstConsumer 라 다른 노드에 잡히면 PVC 가 Pending 으로 남고 back 이 뜨지 않는다 | cc-prototype `values-prod.yaml` 주석(fix1 2026-10-13 — Pending 사고) |
| replicas · 전략 | `replicas: 1` 그대로 · **롤링(기본 RollingUpdate) 그대로** — 새 pod 가 같은 노드(노드 고정)라 RWO 볼륨을 같이 붙일 수 있고, §4.4 「깨진 시드면 readiness 가 안 올라와 옛 pod 가 남는다」 를 지킨다. 겹치는 몇 초 동안 두 pod 가 같은 날짜 파일에 append 할 수 있다 — 줄 단위 append 라 섞이지 않는다(§5.9 「쓰기」). cc-prototype 의 `Recreate` 는 SQLite 단일 쓰기 때문이라 여기는 따르지 않는다 | 기본값 |
| **CPU 예약(0.6.1)** | back `resources.requests.cpu` **50m**(100m 에서 · memory 256Mi · limits cpu 1 · memory 1Gi 그대로). 노드 고정으로 back 은 `lima-worker-1` 에만 뜰 수 있는데 그 노드의 CPU 예약이 3,950m(98%)라 request 100m 새 pod 가 **Pending**(infra PR #36). back 은 Soniox 중계라 평소 사용량이 작다 — 실제 사용은 limit 1 까지 그대로 | 배포 10 실측 · 코디 |
| 차트 주석 · NOTES | 「Stateless (no DB, no volume)」 · 「No volumes → no fsGroup」 주석을 고친다 | — |
| 비밀값 | 바뀌지 않는다(Secret 키 목록 그대로). `INTERPRET_RECORD_DIR` 은 ConfigMap | §2.4 |

**꺼내기 — kubectl(코디 · 배포 문서 `docs/interpret-pwa-deploy.md` 에 절을 더한다)**

```text
kubectl -n interpret-pwa-prod get pod -l app=back                          # back pod 이름
kubectl -n interpret-pwa-prod exec <back pod> -- ls -l /data/records       # 날짜별 파일
kubectl -n interpret-pwa-prod cp <back pod>:/data/records/<YYYY-MM-DD>.jsonl ./<YYYY-MM-DD>.jsonl
#   cp 가 안 되면(이미지에 tar 없음): kubectl -n interpret-pwa-prod exec <back pod> -- cat /data/records/<YYYY-MM-DD>.jsonl > ./<YYYY-MM-DD>.jsonl
```

- 꺼낸 파일에는 **대화 문장**이 들어 있다 — **레포(특히 public 문서 레포) · PR · 보고서 본문에 붙이지 않는다**. 로컬 작업 폴더(git 밖)에서 보고 지운다. 보고에는 줄 수 · term 적중 수 같은 **수치만**.
- 기록을 지우고 싶으면(시연 전 초기화 등) 같은 방식으로 `exec … rm /data/records/<파일>` — back 은 파일이 없어도 다음 줄에서 새로 만든다.

**배포 뒤 확인(WP18 · 운영 주소)** — ① back 기동 로그 `glossary seed loaded: version=2026-10-27.6 …` · `interpret records: on dir=/data/records keep_days=7` ② PVC `Bound` · back pod 가 `lima-worker-1` ③ **새 시술 3개 언어 실발화 1회**(⑳ 과 같은 문장 · zh-Hant · ja · en — 폰 또는 합성 음성) ④ **오늘 파일이 생기고** 그 세션의 start · utterance · end 줄 · `terms` 에 `kr-…` ⑤ **7일 삭제**: `exec` 로 `<오늘−8일>.jsonl` · `<오늘−6일>.jsonl` · `keep.txt` 를 만들고 back 을 재시작(`rollout restart` — 기동 때 삭제) → −8일 파일만 사라짐 · 로그 `sweep: deleted=1` → 시험 파일 정리 ⑥ §3.5 표면 그대로(`/api/health` `{ok}` · `/api/glossary` · `/docs` 404) ⑦ 롤아웃이 PVC 를 다시 붙이며 끝남(Pending 0).

**배포 뒤 확인 결과 (0.6.1 — 코디 · 배포 10 · 11)**

| # | 결과 |
|---|---|
| ① | 기동 로그 시드 `.6` 로드 · `interpret records: on dir=/data/records keep_days=7` |
| ② · ⑦ | 첫 롤아웃에서 새 pod **Pending**(노드 CPU 예약 98% — PVC 문제 아님) → PR #36(request 50m) 뒤 기동 · 위 ① 로그로 확인 |
| ④ | 운영 세션의 `session_start` · `session_end` 줄이 기록됨(`utterance` 줄 수 · `terms` 적중 수는 이번 보고에 없음) |
| context | 운영 zh-Hant context **21,658 / 21,689**(`terms` 170 · 역방향 별칭 33 줄임 — ⑲ 최종과 같음) |
| ③ · ⑤ · ⑥ | 이번 코디 보고에 결과 없음(새 시술 3개 언어 실발화 · 7일 삭제 시험 · 표면) — 기록하지 않았다 |

- 운영 `GLOSSARY_CONTEXT_MAX_CHARS` 는 비어 있어야 언어별 표가 쓰인다(§2.4) — 위 zh-Hant 기준 21,689 가 로그에 나온 것이 그 확인이다.

## 10. 열린 것 — 근거(DEC · 공식 문서 · 원형)로 닫지 못한 것

> 0.5.0 마감 정리 — **남은 것은 셋**: 사람 목소리 E2E(OQ-017) · 못 찾은 대만명 80(OQ-016) · 데모 로그인 끄기(OQ-008). 나머지는 닫았거나 합쳤다(근거는 각 행).
> 0.6.0 — **둘을 더한다**: 처분 밖에 남은 모호 · 근거 없는 시드 값(OQ-018) · 대문자 영문 name 의 TTS · 일반 단어 역방향(OQ-019). OQ-016 에 0.6.0 의 `reviewed:false` 가 더해진다.
> 0.6.1 마감 — **OQ-018 닫음**(처분 ① ~ ⑤ · ⑤ 는 뒤집음 · §4.2.3 D). **남은 것**: 사람 목소리 E2E(OQ-017 · ④ 새 시술 미적중 더함) · 시드 검수 숙제(OQ-016) · 데모 로그인 끄기(OQ-008) · 대문자 영문 TTS · 일반 단어 역방향(OQ-019 — 사용자 청취 대기). 계약 안에서 안고 가는 손실: zh-Hant 역방향 별칭 33(§4.6 — 별칭 정리나 줄이기 순서 변경이 필요해지면 새 결정).

| ID | 무엇 | 지금 | 왜 못 닫나 · 권장 |
|---|---|---|---|
| **OQ-017** | **사람 목소리 E2E**(0.5.0 — OQ-001 · OQ-007 의 남은 확인을 합침) — ① 대만 현지명 양방향: 한국어 「울쎄라」 · 「써마지FLX」 → 대만명이 합성 음성에서 상표명 · 음역으로 나옴(⑰ 1/4 — 짝은 context 에 있음 · 줄이기와 무관) ② `yue` = 표준 문어(번체 자막) + 만다린 음성(OQ-001) ③ iPhone 길게 누름(D-36 — 선택 · 확대 · 콘텍스트 메뉴 · 원 밖으로 미끄러짐) · 누르는 중에 TTS 가 오면 송신 막힘(반이중 그대로 · DEC 에 따로 없음) ④ **(0.6.1) 새 시술 미적중**(⑳ 합성 음성 · 짝은 context 에 있음): 프로파일로 → STT 가 「프로파일」로 들음(3개 언어 모두 · 번역 전) · 뉴라미스 zh-Hant → 「優美思」 · ja 「サーマジCPT」(시드 name `サーマクールCPT` 와 다른 음역 — ja alias 로 넣을 근거 없음 · 조사 R4 · R5) · 덴서티 ja → 「デンソティ」 · zh-Hant 에서 Exion · density · 엠페이스가 영문 | 코드 · 시드로 더 할 것이 보이지 않음 · 배포 fe8475e(④ 는 17c26b5) | 합성 음성 표본 1문장씩이라 판정 못 함. 권장: 사용자가 폰(배포 주소)에서 사람 목소리로 1회 — 결과로 시드(대만명 별칭 · ④ 의 음역 alias 는 근거가 생기면) 또는 DEC 를 고친다. 운영 기록(§5.9)의 `terms` 로 적중을 셀 수 있다 |
| **OQ-016** | **시드 검수 숙제(사용자 PR)** — ① **대만 현지명을 못 찾은 80 term**(zh-Hant = 초안 · `draft-s2twp` · `reviewed:false` — `.5`(D-38)로 일부 정리) ② 출처 1개뿐인 대만명(`web-research` · `reviewed:false`) ③ 첫 가져오기 「그 밖」 괄호 60(OQ-012 를 합침 — 괄호를 뺀 이름 + `raw` 보존 · `reviewed:false`) ④ **(0.6.0) 새 시술 · 대륙 변경의 ✗ 칸**(§4.2.2 · §4.2.3 — 「현지에 없음 = 영문」 · 출처 1) · **C 결함 4칸의 현지 표기**(`manual` · 영문으로 둠) | 데이터 그대로 · context 에는 들어감(§4.2 — 검수 여부로 빼지 않음). 메뉴가 없어(D-37) 목록은 시드에서 `reviewed:false` 로 찾는다 | 현지명 · 별칭은 사람이 정한다(D-32 · D-33 · D-35 — 우리가 짓지 않는다). 권장: 사용자가 시드 PR(§4.2.1 규칙) → 재배포(§9.5) |
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
| D-41 통역 기록 — 서버에만 · 화면 · API 없음 · 날짜별 JSONL · 음성 없음 · 7일 삭제 · kubectl(Scope Out → In) | §1 · §2.1 · §2.4 · §3.5 · §5.1 · **§5.9** · §9.1 「기록」 · §9.3 ㉑ · **§9.6** |
| (DEC 밖) 운영 장애 2026-10-27 02:07 — TTS keepalive 형식 | §5.1 · §5.8 · §9.1 · §9.3 ⑱ |
