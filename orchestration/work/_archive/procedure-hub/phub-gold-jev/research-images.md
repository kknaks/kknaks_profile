# 조사 — 원리 · 방법 그림을 silver → gold → DB → 허브 → 상담 화면으로 잇기

- 워커: procedure-hub researcher(그림) · read-only · 2026-11-17
- 브리프: `image-research-brief.md` · 결정하지 않는다 — 고를 것은 §0-2 「정할 것」
- 경로 약어: `I` = `reference/2026-11-17-procedure-images` · `SM` = `orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model` · `H` = PROCEDURE-HUB 워크트리 `phub-gold-jev`(HEAD daa54e3) · `A` = clinic_chat 워크트리 `phub-gold-jev`(HEAD 6303e18 + 미커밋 · 0.2 구현 중) · `W` = `orchestration/work/phub-gold-jev`
- 셈은 전부 이 워커가 파일을 읽어 다시 센 값이다(python `csv.DictReader` · `os.path.getsize` · `hashlib.sha256`). 서버 · DB · 외부 호출 0.

## 0. 요약

### 0-1. 질문당 요약

| Q | 답 |
|---|---|
| Q1 실태 | 103 코드(원리 54 · 방법 49) = silver 와 코드가 **정확히 같다**(빠짐 0 · 남음 0). 파일 117(SVG 116 + JPG 1) · 5.40MB. 그런데 **묶음이 둘로 갈린다** — 새로 그린 70 코드(73 SVG · 라벨 528 · 1200×800 · 평균 62KB)와 옛 초안을 그대로 둔 33 코드(43 SVG + JPG 1 · 글자 0 · viewBox 셋 · 평균 1.5KB). 여러 장 12 코드 가운데 3 은 **같은 파일의 복사본**(별칭)이고 9 는 서로 다른 옛 초안이다. 의료 검수는 전부 「검수 전」 이고 **코드별 검수 칸은 구조화돼 있지 않다**(글자 한 칸 `review` 70행 + JSON 한 줄). 권리 표기가 필요한 것은 MEC-070 한 장. |
| Q2 경로 | 원리 코드는 gold 에 `g_profile.mechanism_code` 한 칸(401행 · 51 코드)뿐이다. **방법 코드는 gold 어디에도 없다** — `g_profile.methods` 는 이름을 ` · ` 로 이은 글자(159행 · 39 이름)다. 원리는 코드로 바로 잇고, 방법은 이름 → 코드(`g_entry` 의 method 입구 · 이름 중복 0)로 잇는다. 원리 코드는 LLM 에 안 가고 기록(`verified_lines`)에만 남는다 — 그림은 LLM 을 거치지 않고 붙일 수 있다. |
| Q3 담는 꼴 | (a) 칸 더하기는 여러 장 · 장마다 다른 권리 · 검수 값을 한 칸에 넣어야 해 「담을 칸 없는 값」 이 생긴다. (b) 새 silver 표는 값이 전부 제 칸에 들어가지만 표 74 → 75(라벨까지면 76) · 마이그레이션 1 · 계약 상수 · silver-schema 가 함께 바뀐다. 어느 쪽이든 **지금 해시 식으로는 그림 판이 바뀌어도 `gold_hash` · `aux_hash` 가 안 바뀐다** — 보조 입력으로 넣어야 응답 머리에 드러난다. |
| Q4 허브 응답 | 길 셋 — ① `facets` profile 행에 칸 ② 새 도구(코드 → 그림 목록) ③ 허브는 표만 싣고 앱이 따로. ② 가 계약 변경이 가장 작다(도구 9 → 10 · 기존 응답 불변). 검수 거르기는 허브가 상태를 **값으로 내고** 앱이 거르는 꼴과 허브가 아예 안 내는 꼴이 있다. |
| Q5 서빙 | 허브는 지금 정적 파일을 **내지 않는다**(`StaticFiles` 0 · 스토리지 코드 0). 앱은 `/static` 을 이미 낸다. 사용자 제안(바인드 마운트 · `_RESUME` §2 11-17)은 반입 CLI 전례와 꼴이 같지만, **그 전례는 한 번 도는 컨테이너**이고 서빙 컨테이너는 배포 helper 가 「기존 mounts 없음」 을 확인한다. stg 가 띄우는 것은 `app.main` 이고 gold 진입점은 stg 에 없다(SPEC-003 N-1). 바인드 마운트로 갈 때의 라우트 · env · VM 디렉터리 · 해시 기록 사실은 §5-3. |
| Q6 화면 | 지금 화면은 세 칸 · 이벤트 여섯 · 「새 칸 · 새 이벤트 없음」(SPEC-005 SC1)이다. 그림 자리는 계약에 없다 — 어디에 두든 SPEC-004/005 를 고쳐야 한다. 새 SVG 는 글자가 `<text>` 라 `<img>` 로 넣으면 화면 폰트가 안 먹고, 인라인으로 넣으면 **파일 사이 id 40개가 겹친다**. |

### 0-2. 정할 것(사용자가 고를 것만)

| # | 정할 것 | 선택지 | 추천 | 근거 | 위험 |
|---|---|---|---|---|---|
| U-1 | 그림을 담는 꼴 | (a) `mechanism` · `method` 에 칸 (b) 새 silver 표 하나(그림 한 장 = 한 행) (c) 표 둘(그림 + 라벨) | **(b)** | 여러 장 9 코드 · 장마다 다른 형식 · 권리 · 검수 값이 한 칸에 안 들어간다(§3) · 다형 참조 전례가 silver 에 15칸 있다(SPEC-003 §2-7) | 표 74 → 75 · 마이그레이션 1 · 헤더 계약 · silver-schema · SPEC-003 수 전부 고침 |
| U-2 | 별칭 3장(같은 파일 복사본) | (a) 대표 하나만 싣는다(114장) (b) 그대로 둘 다(117장) | **(a)** | 세 쌍 모두 sha256 이 같다(§1-3) · README 가 「대표 경로 하나를 시드로」 라고 적었다(`I/README.md:13`) | 옛 경로를 참조하던 것이 있으면 끊긴다 — 참조하는 코드는 **확인 안 됨** |
| U-3 | 옛 초안 33 코드(43 SVG + JPG 1)를 같이 싣나 | (a) 싣되 검수 전으로 (b) 새 70 코드만 싣고 33 은 다시 그린 뒤 (c) 전부 싣고 꼴이 다른 것은 표에 값으로 | **원천 질문** — 추천 없음 | 33 코드는 글자 0 · viewBox 셋(1000×600 34 · 1200×700 7 · 1000×760 2) · 다국어 라벨 없음(§1-2). 새 70 과 한 화면에 섞이면 크기 · 꼴이 다르다 | (b) 는 「103 전부 그림 있음」 이 「70」 으로 준다 · (a) 는 화면이 들쭉날쭉 |
| U-4 | 의료 검수를 누가 · 어떤 값으로 | 값 목록(예: 검수 전 / 통과 / 반려)과 검수자 · 날짜 칸을 둘지 | **원천 질문** — 추천 없음 | 지금 원천에는 코드별 검수 값이 없다(§1-5). 「검수된 것만 노출」 은 정해졌지만 **검수할 사람 · 절차는 어디에도 없다** | 정하지 않고 실으면 노출 0장인 채로 판이 나간다(지금 값으로는 117장 전부 「검수 전」) |
| U-5 | 「검수된 것만」 을 어디서 거르나 | (a) 허브가 상태를 값으로 내고 앱이 거른다 (b) 허브가 검수된 것만 낸다 (c) 적재기가 검수된 것만 싣는다 | **(a)** | 허브 원칙이 「값을 바꾸지 않는다 · 있는 것을 그대로」(SPEC-001 §5-4) · 검수 화면(내부)은 검수 전 그림을 봐야 한다 | 앱이 거르기를 빠뜨리면 검수 전 그림이 손님에게 나간다 → 앱 시험 1줄이 필수 |
| U-6 | MEC-070 외부 사진 | (a) 출처 표기를 붙여 싣는다 (b) 싣지 않고 SVG 로 새로 그린다 (c) 이번 판에서 뺀다 | **(b)** — 그리기 전까지는 (c) | 117장 가운데 SVG 가 아니고 · 외부 권리가 걸리고 · 0.80MB(전체의 15%)인 한 장이다. CC BY-SA 4.0 은 고친 파생물에 같은 라이선스를 요구한다(`manifest.json` A02 `notes`) | (a) 는 표기 칸 넷(저작자 · 출처 · 라이선스 · 라이선스 주소)이 이 한 장 때문에 생긴다 · 화면에 표기 자리가 필요하다 |
| U-7 | 라벨 528 을 DB 에 두나 | (a) 안 둔다 — SVG 안 글자가 원천 (b) 표로 둔다(다국어 교체용) | **(a)** — 다국어가 범위에 들 때 (b) | 라벨은 70 코드에만 있고 ko · en 초안뿐이다(§1-4) · 상담 화면은 지금 한국어뿐 · README 는 「위치 변경의 원천은 SVG」 라고 적었다(`I/README.md:7`) | (a) 면 영어 등으로 바꾸려 할 때 표를 그때 더한다 |
| U-8 | 허브 응답의 꼴 | (a) `facets` profile 행에 칸 (b) 새 도구 하나(코드 목록 → 그림 행) (c) 허브는 표만 · 앱이 다른 길로 | **(b)** | profile 에 넣으면 `g_profile` 739행 응답 전부가 바뀌고 방법은 이름뿐이라 행 옆에 못 붙는다(§2-2) · 새 도구는 기존 9 도구 응답이 그대로다 | 도구 9 → 10 · 앱 조회 1회 추가 |
| U-9 | 그림 파일을 어디서 내나 | (a) 허브 컨테이너에 읽기 전용 바인드 마운트(사용자 제안) (b) 허브 이미지에 싣는다 (c) 앱 정적 폴더 (d) 스토리지 | **(a)** — 로컬. stg 는 N-1 과 함께 | `_RESUME` §2 11-17 「바인드 마운트 1순위」 · 반입 CLI 전례(`H/docs/guides/deployment.md:461-472`) | 서빙 컨테이너의 배포 helper 가 「기존 mounts 없음」 을 확인한다(`H/docs/guides/prod-migration.md:273`) — stg · prod 에서 그대로는 안 선다 · 허브에 정적 서빙 코드가 새로 든다 |
| U-10 | 그림 폴더를 어느 레포에 두나 | (a) 프로필(PUBLIC)에 커밋 (b) gitignore 로 로컬만(silver-model 과 같은 꼴) (c) 허브(PRIVATE) | **(b)** — 검수 · 권리 정리 전까지 | 지금 `I` 는 **미추적이고 gitignore 에 없다**(§1-6). 옛 그림 폴더는 「권리 검증 전 — public 레포에 올리지 않는다」 로 막혀 있다(`.gitignore:118-119`) | 마감 PR 이 미추적 파일을 함께 넣으면 검수 전 그림 117장과 CC BY-SA 사진이 공개 레포에 올라간다 |
| U-11 | 화면의 어디에 · 언제 | (a) 원리 · 방법을 물은 턴에만 답 아래 (b) 리스트 행을 눌렀을 때 (c) 리스트 행마다 늘 | **(a)** | 「묻지 않은 것 안 붙임」(SPEC-004 §7-1) · `mechanism` 은 기본 묶음이 아니라 물었을 때만 읽힌다(SPEC-002 §3-2a) · 리스트 행 누르기는 0.2 에서 정할 자리다(SPEC-004 PL9) | 새 이벤트 또는 `done` 조각 확장 — SPEC-005 SC1 「새 이벤트 없음」 을 고쳐야 한다 |

- 추천을 붙인 9 건 가운데 **사용자 판단이 꼭 필요한 것은 U-3 · U-4(원천 질문 — 조사로 답이 안 나옴)와 U-6 · U-10(권리 · 공개)** 넷이다. 나머지는 추천대로 가도 되돌릴 수 있다.

---

## 1. Q1 — 그림 묶음 실태

### 1-1. 수

| 무엇 | 수 | 근거 |
|---|---:|---|
| 코드 | 103(원리 54 · 방법 49) | `I/image-map.csv` 103행 · `구분` 셈 |
| silver 와 대조 | 빠진 코드 0 · 남는 코드 0 | `SM/silver/mechanism.csv` 54 · `method.csv` 49 의 `code` 와 집합 비교 |
| 그림 상태 | `있음(직접)` 103 · 맞춤 `A` 103 | `image-map.csv` `이미지 상태` · `맞춤` 칸 |
| 경로 | 117(서로 다른 경로 117 · 없는 파일 0 · 표에 없는 파일 0) | `이미지 경로` 칸을 ` ; ` 로 나눠 `images/` 와 대조 |
| 형식 | SVG 116 · JPG 1 | 확장자 셈 |
| 크기 | 그림 5,398,921 바이트(SVG 4,594,566 + JPG 804,355) · 미리보기 PNG 둘 3,138,128 · 폴더 전체 8.7MB | `os.path.getsize` · `du -sh` |
| 여러 장 코드 | 12(3장 2 · 2장 10) | 아래 §1-3 |

`image-validation.json` 의 수(`svg_paths` 73 · `label_entries` 528 · `inventory_codes` 103 · 빠진 경로 0)와 위 셈이 맞는다. 검사 11 항목은 전부 `true`, `render_audit.errors` · `bounds` 는 빈 목록이다(`I/image-validation.json:9-27`). **이 검사는 새로 그린 70 코드에만 돈 것이다**(`render_audit.codes: 70`).

### 1-2. 묶음이 둘이다

| | 새로 그린 것(`image-assets.csv`) | 옛 초안을 둔 것 |
|---|---|---|
| 코드 | 70(원리 35 · 방법 35) — 1단계 교체 37 · 2단계 신규 33 | 33(원리 19 · 방법 14) |
| 파일 | SVG 73(대표 70 + 별칭 3) | SVG 43 + JPG 1 |
| viewBox | `0 0 1200 800` 73 | `0 0 1000 600` 34 · `0 0 1200 700` 7 · `0 0 1000 760` 2 |
| 글자 | `<text>` 있음 73 · `data-i18n` 73 · `lang="ko"` 73 | `<text>` 0 · `data-i18n` 0 · `lang` 없음 43 |
| 크기 | 합 4,530,916 · 최소 4,156 · 중앙 88,677 · 최대 95,638 | 합 63,650 · 최소 661 · 중앙 1,444 · 최대 2,462 |
| 외부 참조 · 래스터 · 스크립트 · `<style>` | 0 | 0 |
| 폰트 지정 | `Pretendard, Noto Sans KR, Apple SD Gothic Neo, sans-serif` 73 | 없음 |
| sha256 기록 | 70행 전부 실제 파일과 일치 | 기록 없음 |

- README 는 「103개 코드는 모두 이미지 경로가 존재」 라고 적었고 그것은 맞다(`I/README.md:23`). 다만 **33 코드의 그림은 10-27 초안 그대로**다(`I/README.md:36` 「이번 작업 대상 이외의 직접 대응 그림 33개는 유지한다」) — 크기 · 꼴 · 라벨이 새 70 과 다르다.
- 옛 초안의 권리 값: 원천 `reference/2026-10-27-reference-image/시술원리/manifest.json` 에서 SVG 36건이 `rights_status: original_draft_unreviewed` · `license` = 「Original draft / no third-party artwork copied」 류다(직접 그린 초안 · 검수 전). 43 파일 ↔ manifest 36건의 1:1 대조는 **확인 안 됨**(파일 이름이 바뀌었다).

### 1-3. 여러 장 12 코드

| 코드 | 장 | 묶음 | 서로 다른가 | 크기(바이트) |
|---|---:|---|---|---|
| MEC-031 | 2 | 새 | **같은 파일**(별칭) | 4,848 · 4,848 |
| MET-061 | 2 | 새 | **같은 파일**(별칭) | 91,609 · 91,609 |
| MET-069 | 2 | 새 | **같은 파일**(별칭) | 89,277 · 89,277 |
| MEC-040 | 3 | 옛 | 다름 | 835 · 796 · 943 |
| MEC-050 | 3 | 옛 | 다름 | 1,558 · 1,905 · 1,025 |
| MEC-051 · MEC-060 · MEC-065 · MEC-075 · MEC-107 | 각 2 | 옛 | 다름 | 661 ~ 2,462 |
| MET-006 · MET-068 | 각 2 | 옛 | 다름 | 661 ~ 880 |

- 별칭 3 은 `image-assets.csv` 의 `alias_paths` 칸에 적혀 있고 검사 `aliases_identical_to_representative: true` 와 맞는다. **「여러 장」 으로 실제 내용이 다른 것은 9 코드 21 파일**이고 전부 옛 초안이다.
- 한 그림을 두 코드가 함께 쓰는 경우 0(경로 117 = 서로 다른 경로 117).
- 장 사이의 **순서 · 뜻**(어느 것이 대표인가 · 각 장이 무엇을 그렸나)은 표에 칸이 없다 — 파일 이름 뒤쪽(`__pigment-laser` 등)과 `image-map.csv` 의 나열 순서뿐이다.

### 1-4. 라벨 528

- `I/image-labels.csv` 528행 · 칸 10(`code` · `svg_path` · `element_id` · `i18n_key` · `x` · `y` · `font_size` · `text_anchor` · `ko` · `en`). 70 코드 · 70 경로(대표 경로에만 — 별칭 경로 행은 없다).
- 종류: `label-*` 388(그림 안 글자) + `diagram-title` 70 + `diagram-desc` 70(접근성 `<title>` · `<desc>` — 좌표 빈칸 140). `image-assets.csv` 의 `text_count` 합 = 528.
- `i18n_key` 528 전부 유일 · (`svg_path`, `element_id`) 528 전부 유일 · `en` 빈칸 0.
- 쓰임(README): 서버가 SVG 를 XML 로 읽어 `element_id` 또는 `data-i18n` 키의 글자만 바꾼다 · 좌표는 SVG 가 원천이고 CSV 의 좌표는 뽑아 둔 값이다(`I/README.md:7,15`). 「현재 라벨 데이터는 한국어와 영어 초안」 · 「지원 언어 7종의 번역 완료를 뜻하지 않는다」(`:17`).
- **옛 초안 33 코드에는 라벨이 없다**(글자 0).

### 1-5. 의료 검수 · 권리 칸

| 무엇 | 어디에 있나 | 값 |
|---|---|---|
| 의료 검수(묶음 전체) | `I/image-validation.json:28` `"medical_review": "not_performed"` | 한 줄 — 코드별이 아니다 |
| 의료 검수(코드별) | `I/image-assets.csv` 의 `review` 칸(글자) | 70행 전부 「구조·한영 렌더 확인 / 의료 검수 전」 — 값 하나 · 구조 검사와 의료 검수가 한 칸에 섞여 있다 |
| 의료 검수(옛 33 코드) | **없다** | `image-map.csv` 에 검수 칸이 없다(`메모` 에 새 70 만 「의료 검수 전」 글자) |
| 출처 · 라이선스 | **`image-assets.csv` 에 그런 칸이 없다**(칸 12 = `code` · `kind` · `name_ko` · `stage` · `svg_path` · `alias_paths` · `width` · `height` · `background` · `text_count` · `sha256` · `review`) | — |
| 권리(MEC-070) | `image-map.csv` `메모` 글자 + `I/README.md:39` + 옛 `manifest.json` A02 | 아래 |

브리프가 물은 「image-assets 의 출처 · 라이선스 칸」 은 **없다.** 권리 값은 글자 메모와 옛 manifest 에만 있다.

**외부 · 권리 표기 필요한 것 전수 = 1장**

| 코드 | 파일 | 원천 기록 |
|---|---|---|
| MEC-070 | `images/mechanism/MEC-070__cryolipolysis.jpg`(JPEG 1920×1080 · 804,355 바이트 · sha256 `6f1ec26f…` — manifest 값과 같다) | `reference/2026-10-27-reference-image/시술원리/manifest.json` A02: `title` 「Cryolipolysis procedure」 · `author` 「Scientific Animations」 · `source_url` commons.wikimedia.org 의 그 파일 쪽 · `license` 「CC BY-SA 4.0」 · `rights_status` `commercial_reuse_with_attribution_sharealike` · `modified` `no` · `customer_ready` `false` · `notes` 「변경/번역한 파생 도해는 동일 또는 호환 라이선스로 공유 … 실제 장비 흡입 구조와 시간 경과 검증 필요」 |

- 나머지 116 SVG 에 외부 참조 · 래스터는 0 이다(셈). 다만 **옛 manifest 는 173건 전부 `customer_ready: false`** 이고(재셈), 그 조사 문서는 「붙일 수 있다와 보여 줄 수 있다는 별개」 라고 적었다(`I/media-coverage-survey.md:30`).
- 원천 manifest 가 든 폴더(`reference/2026-10-27-reference-image/`)는 gitignore 다(`.gitignore:118-119`) — MEC-070 의 저작자 · 출처 주소는 **지금 커밋되는 어느 파일에도 없다.**

### 1-6. 폴더의 git 상태

- `I` 는 **미추적**(`?? reference/2026-11-17-procedure-images/`)이고 gitignore 에 걸리지 않는다(`git check-ignore` 불일치). 프로필 레포는 PUBLIC(브리프 §3 Q5 기재 · 이 워커가 원격을 확인하지는 않았다).
- 옛 그림 폴더에는 「병원 기기 사진 · 교육 자료 원본 — 권리 검증 전, public 레포에 올리지 않는다」 는 줄이 있다(`.gitignore:118`). 새 폴더에는 그런 줄이 없다.

---

## 2. Q2 — silver → gold 경로

### 2-1. silver 에서 원리 · 방법을 가리키는 표

| 표 | 칸 | 행 | 무엇 |
|---|---|---:|---|
| `mechanism` | `code` · `name_ko` · `name_en` · `name_en_source` · `parent_code` · `description` | 54 | 사전. `parent_code` 값 있음 11 |
| `method` | `code` · `name_ko` · `name_en` · `name_en_source` · `kind` · `parent_code` · `description` | 49 | 사전. `kind` 7 값(에너지 조사 방식 14 · 주입 방식 10 · 도구 10 · 투여 경로 7 · 흡수 촉진 5 · 실 형태 2 · 재료 처리 1) |
| `procedure` | `mechanism_code` | 138 가운데 값 136 · 서로 다른 코드 51 | 시술 → 원리(FK) |
| `case_method` | `method_code` | 107 · 서로 다른 코드 36 | 케이스 → 방법(FK) |
| `product_method` | `method_code` | 63 · 서로 다른 코드 17 | 제품 → 방법(FK) |
| `alias` | `target_table` + `target_code`(다형) | 원리 11 · 방법 82 | 다른 이름 |
| `source_ref` | `target_table` + `target_id`(다형) | 원리 123 · 방법 252 | 근거 |

- 어느 시술도 가리키지 않는 원리 3 · 케이스 · 제품 어느 쪽도 가리키지 않는 방법 10 — 그림은 있지만 **gold 의 행으로는 닿지 않는 코드가 13** 이다(상위 코드로만 존재).
- FK 는 `silver_contract.py` 에 그대로 있다(`H/backend/app/modules/gold/silver_contract.py:164,176,177,191,197`).

### 2-2. gold 에 들어가는 자리

gold 15표 전 칸을 `MEC-` · `MET-` 로 훑은 결과(재셈):

| 표 | 칸 | 행 | 꼴 |
|---|---|---:|---|
| `g_profile` | `mechanism_code` | 401(시술 136 + 케이스 265) · 코드 51 | **코드** |
| `g_profile` | `mechanism_name` | 401 | 이름 |
| `g_profile` | `mechanism_text` | (계열 · 시술의 원리 글 — silver `modality.mechanism` · `procedure.mechanism`) | 글 |
| `g_profile` | `methods` | 159(케이스 97 + 제품 62) · 이름 39 | **이름을 ` · ` 로 이은 글자 — 코드 없음** |
| `g_entry` | `entity_code`(`entity_table` = `method`) | 131 | 방법 이름 → 코드 입구. **원리 입구는 0행** |
| `g_evidence` | `silver_id` | 131 | 위 입구의 근거 |

- 짓는 자리: `SM/gold/gold-build.py:293`(시술 행 — `p['mechanism_code']`) · `:301-302`(케이스 행 — 시술의 원리 코드 + `jn('method', cmeth[...])`) · `:271-277`(`jn` — 코드를 이름으로 바꿔 잇는다).
- 제품 행(315)은 자기 행에 원리 칸이 없다(`mechanism_code` 0) — 시술 층에서 물려받는다(SPEC-001 변경 기록 0.5.1 「`inherited` 만 있는 대상의 규모(원리 314 / 315)」).
- 방법 이름 39 는 전부 `method.name_ko` 와 글자 그대로 맞고 이름 중복은 0 이다(재셈) — 허브가 속성 쪽 조회에서 이미 이 맞춤을 쓴다(SPEC-001 §4-4 「맞추는 법」 · §5-7 A2).

### 2-3. 상담에서 원리 · 방법이 재료로 실리는 자리

| 정보 종류 | 읽는 조회 | LLM 에 싣는 칸 | 기본 묶음 |
|---|---|---|:-:|
| `mechanism` | `facets` profile | `name_ko` · `modality_name` · `procedure_name` · `mechanism_name` · `mechanism_text` | — (물었을 때만) |
| `overview` | `facets` profile | … `methods` …(15칸) | ✓(시술 · 속성 시작) |
| `indication`(고민 쪽) | `concern_candidates` + 후보별 profile | `mechanism_name` 한 줄 | ✓(부위·고민) |

(SPEC-002 §3-2a 두 표 — `W/SPEC-002-chat-eval.md:394` 부터)

- `mechanism_code` 는 **기록에만 두는 칸**이다(같은 절 「고르는 식」 — `*_code` · `gid` 는 `verified_lines[]` 에) · 앱 상수도 같다(`A/clinic_chat/walk/kinds.py:131,172`).
- 고민 → 리스트 턴의 요약 줄에는 계열마다 `mechanism_name[]` 이 든다(SPEC-004 AP4 · `A/clinic_chat/consult/material.py:72-128`).

### 2-4. 그림이 「그 행 옆」 에 붙으려면

| 무엇 | 잇는 열쇠 | 지금 있나 |
|---|---|---|
| 원리 그림 ↔ profile 행 | `g_profile.mechanism_code` = 그림 표의 코드 | 있다 — 앱은 `verified_lines` 의 코드로 LLM 없이 붙일 수 있다 |
| 방법 그림 ↔ profile 행 | `g_profile.methods` 의 항목 이름 → `g_entry`(method) → 코드 | 이름 맞춤으로만. 코드 칸을 원하면 gold 에 칸(`method_codes`)을 더해야 하고 그러면 `gold_hash` · 헤더 계약 · gold-check 가 바뀐다 |
| 제품 행 | 물려받은 시술 층의 profile 행 | 지금 `layer.role` 로 내려온다 |
| 리스트 행(시술) | `procedure_code` → 그 시술의 profile 행 → `mechanism_code` | 리스트 자료에는 원리 코드가 없다(SPEC-004 §6-1 장부 `list` 꼴 — `procedure_code` · `reach` · `concern_match` · `gids`) |

---

## 3. Q3 — 담는 꼴 선택지

### 3-1. 담아야 할 값(실물 기준)

그림 한 장마다: 코드(원리 / 방법) · 순서 · 경로 · 형식(svg / jpg) · 크기(viewBox 4종 + JPG) · sha256 · 묶음(새 / 옛) · 구조 검사 결과 · 의료 검수 상태 · (MEC-070 만) 저작자 · 출처 주소 · 라이선스 · 라이선스 주소 · 고쳤는지. 코드 하나에 1 ~ 3장.

### 3-2. 비교

| | (a) `mechanism` · `method` 에 칸 | (b) 새 silver 표 하나 | (c) 표 둘(그림 + 라벨) |
|---|---|---|---|
| 꼴 | `image_paths`(` ; ` 목록) · `image_status` 등 칸을 두 표에 | `concept_image`(이름 제안) — 그림 한 장 = 한 행 | (b) + `concept_image_label` |
| 행 수 | 54 + 49 그대로 | 117(별칭 빼면 114 · 옛 33 코드 빼면 70) | + 528(라벨) |
| 담을 칸 없는 값 | **생긴다** — 여러 장 9 코드에서 장마다 다른 크기 · 검수 · sha256 을 한 칸에 못 담는다. MEC-070 의 권리 넷은 53행이 빈 칸 넷으로 남는다 | 0 — 값마다 칸 | 0 |
| 「CSV 그대로」 | 지킨다(칸만 늘어남) | 지킨다(CSV 1 = 테이블 1 — SPEC-003 R1) | 지킨다 |
| FK | 그대로(새 FK 0) | 코드가 두 표를 가리키므로 **다형 참조**(`target_table` + `target_code` — silver 에 15칸 전례 · FK 를 걸지 않는다 · SPEC-003 §2-7) 또는 칸 둘(`mechanism_code` · `method_code` 각각 FK · 한쪽은 빈칸) | 라벨 → 그림 FK 1 |
| silver-check | `silver-schema.json` 의 두 표 `columns[]` 에 칸 추가 | 스키마에 표 1 추가(`key` · `id_pattern` · `columns[].fk` 또는 `poly`) | 표 2 추가 |
| gold · gold-check | gold 가 이 칸을 읽지 않으면 불변. `g_profile` 에 실으려면 헤더 27 → 늘고 `gold_hash` 가 바뀐다 | gold 불변(gold 가 그림을 안 읽는 길) | 같음 |
| SPEC-003 테이블 | 74 그대로 · `s_mechanism` 6칸 → · `s_method` 7칸 → 늘어남 | **74 → 75** | **74 → 76** |
| 헤더 계약 | `SILVER_HEADERS["mechanism"]` · `["method"]` 고침(`silver_contract.py:44-45`) | `SILVER_HEADERS` · `SILVER_KEY` · (`SILVER_FK`) 에 표 추가 | 표 둘 추가 |
| 마이그레이션 | 새 revision 1(칸 추가) — `b202611170001` 은 「그 시점의 풀어 쓴 고정본」 이다(`H/backend/app/model/medallion.py:3-5`) | 새 revision 1(표 추가) | 같음 |
| 적재기 | V5(헤더 = 계약)가 계약과 함께 바뀜 | V2(57표 전부 있다) → 58 · **V3 이 먼저 걸린다** — 계약에 없는 CSV 가 silver 폴더에 있으면 exit 2(SPEC-003 §4-3) | 같음(59) |
| 빌드 기록 | 74행 그대로 | 75행 | 76행 |
| 해시 | `mechanism` · `method` 는 `kind = silver`(52표)라 **`gold_hash` · `aux_hash` 어디에도 안 든다** — 그림 판이 바뀌어도 응답 머리 · cursor 의 build 가 그대로다(SPEC-003 O-4) | 새 표도 기본은 `silver` — 같다. **허브가 읽는 보조 입력으로 올리면** `aux_hash` 가 6 → 7 파일이 되고 값이 바뀐다(`inputs.py:129-178`) | 같음 |

### 3-3. 해시에 대해 따로

- 지금 식: `gold_hash` = gold 폴더 16 파일 · `aux_hash` = `source_ref` + `concern` · `adverse` · `condition` · `concern_site` + 원장 확인 목록 6 파일(SPEC-003 §2-5 · `H/backend/app/modules/gold/inputs.py:64-67,129-178`).
- 허브가 그림 행을 **응답으로 내려면** 그 표는 허브가 읽는 입력이 된다 — 그때 `aux` 로 넣지 않으면 「응답은 바뀌는데 build 값은 같은」 판이 생긴다. cursor 가 build 값에 기댄다(SPEC-001 §2-3 4).
- **그림 파일 자체의 바이트는 어느 해시에도 안 든다.** 표의 `sha256` 칸이 그 일을 한다 — 새 70 코드에는 값이 있고(전부 실제와 일치) 옛 44 파일에는 없다(적재 전에 세어 넣어야 한다).

### 3-4. 라벨 528 을 DB 에 둘지

| | 안 둔다 | 둔다 |
|---|---|---|
| 원천 | SVG 안 글자 하나 | SVG 와 표 둘 — README 는 좌표의 원천을 SVG 로 정했다(`I/README.md:7`) |
| 다국어 | 한국어로만 낸다 | 서버가 글자를 갈아 끼울 수 있다(README 가 그린 길 — `:15`). 지금 값은 ko · en 초안 |
| 넓이 | — | 언어가 칸(`ko` · `en`)이다 — 언어를 더하면 칸이 는다(계약 · 마이그레이션이 그때마다). 행으로 풀면 1,056행 |
| 덮는 범위 | — | 70 코드뿐(옛 33 코드는 글자가 없다) |
| 누가 쓰나 | — | 지금 쓰는 코드 0(상담 화면은 한국어 · 번역 표 `statement_translation` 은 silver 에 따로 있다) |

---

## 4. Q4 — 허브 응답

### 4-1. 지금

- 도구 9(`resolve` · `scope` · `neighbors` · `facets` · `concern_candidates` · `pair` · `evidence` · `health` · `coverage` — SPEC-001 §4). 응답 행은 「그 gold 표 행 그대로」 + 표지(`layer` · `hier` · `attr`)다(§4-4).
- 허브가 읽는 것: gold 15 + silver 보조 5표 + 원장 확인(SPEC-003 D-1). **`mechanism` · `method` 표는 허브가 읽지 않는다**(올려 두기만).
- 원리 · 방법 칸의 자리: `MECHANISM_COLUMNS` = `mechanism_code` · `mechanism_name` · `mechanism_text`(`H/backend/app/modules/gold/headers.py:85`) · 속성 쪽 `method` → `g_profile.methods`(`:68`).

### 4-2. 길 셋

| | ① profile 행에 칸 | ② 새 도구 | ③ 허브는 표만 |
|---|---|---|---|
| 꼴 | `facets` profile 행마다 `images[]` 를 얹는다 | `images(nodes: ["mechanism:MEC-001", "method:MET-101", …])` → 그림 행 목록(그 표 행 그대로) | 허브 응답 불변 · 앱이 DB 또는 파일 목록을 따로 읽는다 |
| 계약 변경 | `facets` 출력 · 부록 A · `g_profile` 을 읽는 앱 코드 전부 | 도구 9 → 10 · §4 에 절 하나 · 부록 A 에 줄 하나. 기존 9 도구 응답 불변 | SPEC-001 불변 · 대신 「앱이 허브 DB 를 직접 읽는다」 는 새 계약(SPEC-003 N-7 「다른 소비자가 SQL 로 직접 읽는 계약 — 범위 밖」) |
| 방법 그림 | 행에 코드가 없어 이름 맞춤을 허브 안에서 | 앱이 `methods` 항목 이름을 `resolve` 또는 `g_entry` 로 코드로 바꿔 부른다(지금도 쓰는 길) | 앱 몫 |
| 「값을 바꾸지 않는다」 | gold 행에 gold 에 없는 것을 얹는다 — `layer` 같은 표지 전례는 있다 | 그 표 행 그대로 | — |
| 조회 수 | 0 추가 | 턴마다 +1(원리 · 방법을 읽은 턴만) | — |

- 응답에 실을 값(어느 길이든): 코드 · 순서 · 경로(또는 주소) · 형식 · 크기 · 검수 상태 · 권리 표기(있을 때). **주소를 허브가 지어 내느냐 · 경로만 내고 앱이 붙이느냐**는 서빙 자리(U-9)에 달렸다.

### 4-3. 「검수된 것만」 을 누가 거르나

| | 허브가 값으로 내고 앱이 거른다 | 허브가 검수된 것만 낸다 | 적재기가 검수된 것만 싣는다 |
|---|---|---|---|
| 허브 원칙 | 맞는다 — 있는 것을 그대로(SPEC-001 §5-4) | 허브가 값으로 행을 버린다 — 지금 그런 도구는 없다 | 「CSV 그대로 DB」 와 어긋난다(행이 준다) |
| 검수 화면(내부) | 같은 응답으로 검수 전 그림을 본다 | 따로 입력(`include_unreviewed`)이 필요 | DB 에 없다 |
| 빠뜨렸을 때 | 앱이 거르기를 잊으면 손님에게 나간다 | 허브 한 곳 | 적재 한 곳 |
| 지금 값으로 | 117장 전부 「검수 전」 → 화면에 0장 | 응답 0행 | 0행 적재 |

---

## 5. Q5 — 서빙

### 5-1. 지금 사실

| 무엇 | 사실 | 근거 |
|---|---|---|
| 허브 정적 서빙 | **없다** — `StaticFiles` · `FileResponse` 0건. `mount` 는 MCP 앱 하나 | `grep -rnE "StaticFiles\|\.mount\(\|FileResponse" H/backend/app` → `gold_main.py:89` 한 줄 |
| 허브 스토리지 | 없다 — S3 · blob · 이미지 주소 칸 0(`pyproject.toml` 에 boto · storage 0) | 같은 식 grep |
| 허브 이미지에 실리는 것 | `backend/app/` · `backend/alembic/` · `alembic.ini` · 스크립트 3 | `H/backend/Dockerfile:13-22` |
| build context | `backend/app/**` · `alembic/**` · `pyproject.toml` · `uv.lock` · 스크립트 1 만 통과 | `H/.dockerignore` |
| stg 가 띄우는 것 | `app.main:app` — gold 진입점(`gold_main`)은 별개이고 stg 에 없다 | `H/backend/Dockerfile:27` · SPEC-003 N-1 |
| 반입 전례 | corpus 는 VM 의 `/opt/procedure-hub/import/<날짜>/` 에 두고 **`docker run --rm -v …:/import:ro`** 로 한 번 도는 CLI 컨테이너에 연결 | `H/docs/guides/deployment.md:461-472` |
| 서빙 컨테이너의 마운트 | 배포 helper 가 「기존 mounts 없음」 을 확인한다 | `H/docs/guides/prod-migration.md:273` |
| 앱 정적 서빙 | 있다 — `/static`(폰트 · css · js · htmx) | `A/clinic_chat/consult/server.py:19,33,154` |
| 공개 여부 | 허브 PRIVATE · 앱 · 프로필 PUBLIC | 브리프 §3 Q5 기재 — 원격은 **확인 안 됨** |

### 5-2. 선택지

| | (a) 허브에 읽기 전용 바인드 마운트 | (b) 허브 이미지에 싣는다 | (c) 앱 정적 폴더 | (d) 스토리지 |
|---|---|---|---|---|
| 사용자 방향 | `_RESUME` §2 11-17 「바인드 마운트 1순위」 | — | — | — |
| 레포에 그림 | 안 든다(호스트 폴더) | 허브 레포(PRIVATE)에 5.4MB · `.dockerignore` · `Dockerfile` 각 한 줄 | 앱 레포(PUBLIC)에 5.4MB | 안 든다 |
| 허브 코드 | 정적 서빙 새로(`StaticFiles` + 폴더 env) — `gold_main` 에 | 같음 | 0 | 주소 짓기 · 올리기 도구 |
| 그림 판 = 표 판 | 폴더와 CSV 가 따로 움직인다 — 표의 `sha256` 으로 시작 때 대조할 수 있다 | 이미지 태그에 묶인다 | 앱 배포에 묶인다 — 허브 표와 따로 | 따로 |
| 검수 전 그림 | 경로를 알면 누구나 받는다(정적 폴더는 거르지 않는다) — 검수된 것만 폴더에 두거나 서빙이 표를 보고 걸러야 한다 | 같음 | 같음 + 공개 레포에 그대로 | 같음 |
| stg | 서빙 컨테이너에 마운트를 더하면 helper 의 「기존 mounts 없음」 확인과 부딪친다 · gold 진입점이 stg 에 없다(N-1) | N-1 만 | 앱의 배포 자리 — 앱은 지금 로컬 시험 앱이다 | 스토리지가 없다 |
| 로컬 | 폴더 env 하나 | 폴더 복사 | 폴더 복사 | — |

- 크기: 서빙 대상은 그림 5.40MB 다(미리보기 PNG 3.0MB 는 검토용 — `I/README.md:29`). MEC-070 을 빼면 4.59MB, 별칭 3 을 빼면 4.41MB.
- 반입 전례와 「같은 꼴」 인 것은 **호스트 폴더를 읽기 전용으로 잇는다**는 점까지다. 전례는 일회성 컨테이너이고, 이번 것은 떠 있는 서빙 컨테이너에 계속 붙는 마운트다 — 배포 helper · 롤백 절차가 그것을 아는지는 **확인 안 됨**(인프라 레포는 읽지 않았다).

### 5-3. 바인드 마운트로 갈 때의 사실(코디 보충 — 사용자 11-17 「바인드 마운팅으로 들어가면 되지 않나」)

결정이 아니다 — 이 길을 고르면 손대야 하는 자리와 지금 값을 적는다.

**① 허브가 정적 경로로 내는 법**

| 무엇 | 지금 | 이 길에서 생기는 것 |
|---|---|---|
| 앱 조립 | `create_gold_app` 이 `FastAPIBuilder` 로 라우터 둘(`health_router` · `gold_router`)을 `GOLD_API_PREFIX` 아래에 붙이고, MCP 앱을 `app.mount(settings.GOLD_MCP_MOUNT_PATH, mcp_app)` 로 얹는다(`H/backend/app/gold_main.py:62-89`) | 같은 자리에 정적 mount 한 줄(`StaticFiles(directory=…)`) 또는 파일 하나를 내는 라우트. **허브 코드에 `StaticFiles` · `FileResponse` 전례는 0** 이다 |
| 경로 접두어 | `GOLD_API_PREFIX` = `/procedure-hub/gold` · `GOLD_MCP_MOUNT_PATH` = `/procedure-hub/gold-mcp`(`H/backend/app/modules/gold/config.py:50-51`) | 그림 경로 접두어 하나(이름 미정 — 예: `/procedure-hub/gold-images`) |
| 폴더 env | 데이터 폴더는 전부 env 다 — `GOLD_CSV_DIR` · `GOLD_SOURCE_REF_PATH` · `GOLD_HIERARCHY_DIR` · `GOLD_LEDGER_CHECK_PATH`(필수 · 빈 값 = 시작 실패) · `GOLD_SILVER_DIR`(적재기) · 파일은 `backend/envs/.env.gold`(`config.py:24,32,38-41,56`) | 그림 폴더 env 하나(이름 미정). 필수로 두면 그림 없이는 허브가 안 뜬다 · 선택으로 두면 「없으면 그림 경로를 안 낸다」 는 규칙이 따로 필요하다 |
| mount 와 라우트의 차이 | — | mount 는 폴더를 통째로 낸다 — 표의 검수 상태를 보지 않는다. 라우트는 요청마다 표를 보고 거를 수 있지만 코드가 는다(§5-2 「검수 전 그림」 행) |
| 응답의 주소 | — | 허브가 경로(`images/mechanism/MEC-001__….svg`)만 내고 앱이 허브 주소를 붙이는 꼴과 허브가 완성된 주소를 내는 꼴이 있다. 손님 브라우저가 허브에 직접 닿는지는 배포 자리에 달렸다 — 지금 앱은 허브를 서버에서 부른다(MCP · HTTP) · 브라우저가 허브를 부르는 길은 **없다** |

**② 로컬 = 레포 밖 폴더**

- 지금 그림은 프로필 워크트리 안 `reference/2026-11-17-procedure-images/` 에 있다(미추적 · gitignore 아님 — §1-6). silver · gold CSV 는 `SM`(gitignore · 로컬)을 env 로 가리킨다(SPEC-003 §6-2 「경로는 로컬 `$SM` 의 gold · silver · notes」).
- 같은 꼴로 가면 그림 폴더도 **env 로 가리키는 로컬 폴더**다 — 허브 레포 안에 두지 않는다(SPEC-003 D-5 「레포에 CSV 커밋 금지」 와 같은 줄).
- 로컬 허브는 지금 컨테이너가 아니라 프로세스로 뜬다(SPEC-003 §6-3 「backend/ 에서」) — 로컬에서는 「바인드 마운트」 가 아니라 그냥 폴더 경로다. 마운트는 stg 컨테이너에서만 뜻이 있다.

**③ stg VM 디렉터리**

| 무엇 | 사실 | 근거 |
|---|---|---|
| VM 의 허브 자리 | `/opt/procedure-hub/` — `config/stg.env`(`azureuser:azureuser` · `600`) · `import/<날짜>/`(반입) · `cutover/`(백업) | `H/docs/guides/deployment.md:64,225-228,325,461` |
| 반입 전례의 마운트 | `-v "$PHUB_IMPORT_DIR":/import:ro`(날짜 폴더 · 읽기 전용) — **`docker run --rm` 일회성 CLI** | `deployment.md:468-472` |
| 서빙 컨테이너 | `docker run -d --name procedure-hub --restart unless-stopped --env-file …/stg.env -p 10000:8000 …:stg` — **`-v` 없음** | `deployment.md:254-260` |
| 배포 helper | 「정확한 `procedure-hub`/host10000/container8000/bridge/**기존 mounts 없음**」 을 확인한다 | `H/docs/guides/prod-migration.md:273` |
| stg 가 띄우는 앱 | `app.main:app` — `gold_main` 은 stg 에 없다 | `H/backend/Dockerfile:27` · SPEC-003 N-1 |

- 그림 폴더를 둔다면 같은 줄기(`/opt/procedure-hub/<이름>/`)가 전례와 맞는다. **날짜 폴더로 둘지 · 고정 폴더로 둘지 · 누가 올리나(scp · 배포 스크립트)는 어디에도 없다.**
- 서빙 컨테이너에 `-v` 를 더하려면 실행 명령 · 배포 스크립트 · helper 의 「mounts 없음」 확인 셋이 함께 바뀐다 — 그 스크립트 본문은 **확인 안 됨**(문서의 한 줄만 읽었다).
- gold 가 stg 에서 어느 진입점으로 뜨는지(N-1)가 먼저다 — 그림 서빙은 그 진입점에 붙는다.

**④ 이미지에 안 실음**

- 지금 `.dockerignore` 는 `**` 로 전부 막고 `backend/app/**` · `backend/alembic/**` · `pyproject.toml` · `uv.lock` · `alembic.ini` · 스크립트 1 만 연다(`H/.dockerignore`) — 그림 폴더를 허브 레포의 `backend/app/` 밖에 두는 한 **아무것도 안 바꿔도 이미지에 안 실린다.**
- 뒤집어 말하면 그림을 `backend/app/` 아래에 두면 한 줄도 안 고치고 이미지에 실린다(§5-2 (b)) — 두 길의 차이는 폴더 자리 하나다.
- 이미지에 안 실으면 **이미지 태그가 그림 판을 말해 주지 않는다** — 그림 판을 아는 길은 아래 ⑤ 뿐이다.

**⑤ 해시 기록 — 빌드 기록 표에 그림 묶음 해시?**

| 무엇 | 사실 |
|---|---|
| 빌드 기록의 한 행 | 「적재기가 읽은 **파일 하나**」 — `file_name`(PK) · `kind` · `sha256` · `file_rows` · `table_name` · `table_rows` · 판 값 넷(`gold_hash` · `aux_hash` · `built_at` · `loader_version`)(SPEC-003 §2-5 · `W/SPEC-003-hub-gold-db.md:219-232`) |
| `kind` 값 | `gold` · `hash_only` · `source_ref` · `aux` · `silver` 다섯 |
| 그림 파일 117 을 행으로 | `file_name` 이 PK 이고 지금은 이름만 든다 — 그림은 `images/mechanism/…` 처럼 폴더가 갈리지만 이름 117 은 서로 다르다(재셈 — 코드로 시작). 행 74 → 191 · `kind` 에 값 하나(`image`)가 는다 · `file_rows` · `table_name` · `table_rows` 는 NULL(`hash_only` 와 같은 꼴) |
| 그림 표(`concept_image`)의 `sha256` 칸 | 그림 한 장 = 한 행이면 이 칸이 장마다의 해시다 — 빌드 기록에 그림 행을 따로 두지 않아도 같은 값이 DB 에 있다. 새 70 코드는 값이 있고 실제와 일치(§1-2) · 옛 44 파일은 적재 전에 세어 넣어야 한다 |
| 묶음 해시 하나 | 지금 식(「파일 이름 + 공백 + sha256」 줄을 이름순으로 이어 다시 sha256 — `inputs.py:64-67`)을 그림 117 줄에 그대로 돌리면 `image_hash` 하나가 나온다. 빌드 기록에 칸으로 두려면 판 값이 넷 → 다섯(행마다 같은 값) · 허브 `health` 의 `build` 에 필드 하나 |
| 응답 머리 · cursor | 지금 build = (`gold_hash`, `aux_hash`) 둘이다(SPEC-001 §2-3 4). 그림 표를 `aux` 로 넣으면 그 CSV 의 바이트(= 장마다의 `sha256` 칸 포함)가 `aux_hash` 에 든다 — **그림 파일이 바뀌면 표의 sha256 이 바뀌고 `aux_hash` 가 따라 바뀐다**(표를 다시 지었을 때만) |
| 폴더 ↔ 표 대조 | 마운트된 폴더의 실제 파일과 표의 `sha256` 이 같은지는 누가 세지 않으면 모른다. 셀 자리는 둘 — 적재기(그림 폴더 env 를 받아 V 검사에 한 줄) · 허브 시작(지금 DB 판 시작 실패 조건 F1 ~ F7 에 한 줄 — SPEC-003 §5-3). 117 파일 5.4MB 의 sha256 은 시작 시간에 거의 안 얹힌다(어림 — 재지 않았다) |

- 요약: 「그림 묶음 해시」 를 두는 자리는 셋이다 — (가) 그림 표의 `sha256` 칸만(장마다) (나) 빌드 기록에 그림 행 117(파일마다) (다) 빌드 기록 · `health` 에 묶음 해시 칸 하나. (가) 는 U-1 을 (b) 로 고르면 저절로 생긴다 · (나)(다) 는 SPEC-003 §2-5 를 고친다.

---

## 6. Q6 — 상담 화면

### 6-1. 지금 화면의 자리

- 세 칸: 왼쪽 위 얼굴 · 왼쪽 아래 시술 리스트 · 오른쪽 채팅(SPEC-004 D-1 · `A/clinic_chat/consult/templates/page.html:3`).
- 이벤트 여섯: `step` · `list`(→ `#procedure-list`) · `sites`(→ `#face-marks`) · `delta` · `done` · `error`(SPEC-004 §4-3). 0.2 는 「새 칸 · 새 이벤트는 없다」(SPEC-005 SC1 — 결정 D5-12).
- 리스트 행에는 `data-procedure-code` 가 달려 있고 「누르는 동작은 없다」 — 0.2 의 「시술을 눌렀을 때」 가 걸릴 자리다(SPEC-004 PL9).
- 문구는 빈 자리(`data-slot`)만 두고 앱이 짓지 않는다(SPEC-004 §4-5 · SPEC-005 SC6).

**그림이 들어갈 자리는 지금 계약에 없다.** 어디에 두든 SPEC-004/005 의 이벤트 · 조각 · 장부(`shown`) 를 고쳐야 한다.

### 6-2. 둘 수 있는 자리

| | 답 아래(물은 턴에만) | 리스트 행을 눌렀을 때 | 리스트 행마다 늘 |
|---|---|---|---|
| 언제 | 그 턴이 `mechanism`(또는 방법을 실은 `overview`)을 읽었을 때 | 손님이 누른 시술 | 리스트가 뜰 때마다 |
| 「묻지 않은 것 안 붙임」(SPEC-004 §7-1 `common.md` 6) | 맞는다 — 읽은 종류의 그림만 | 맞는다 — 누른 것이 물은 것 | 어긋난다 — 고민만 말했는데 원리 그림이 붙는다 |
| 열쇠 | 그 턴 `verified_lines` 의 `mechanism_code` · `methods` | `procedure_code` → profile → 원리 코드(조회 1회 추가 — 리스트 자료에 원리 코드가 없다) | 같음 × 행 수 |
| 계약 | 새 이벤트 하나 또는 `done` 조각 확장 · `shown` 에 칸 | 0.2 의 누르기 설계(미정) 위에 | `list` 조각 확장 |
| 양 | 턴마다 1 ~ 몇 장 | 1 ~ 3장 | 리스트 시술 수십 × 장 |

- `mechanism` 은 기본 묶음이 아니다 — 고민만 말한 턴에는 원리 행이 안 읽힌다(SPEC-002 §3-2a 「시술 범위의 기본은 개요 하나」). 다만 고민 → 리스트 턴의 요약 줄에는 `mechanism_name[]` 이 든다(SPEC-004 AP4) — 이름이지 코드가 아니다.
- 물려받은 원리(제품 → 시술 층)는 층 밝힘 규칙이 있다(SPEC-002 RQ1). 그림에도 「어느 층의 원리인가」 가 따라붙어야 하는지는 스펙에 없다.

### 6-3. 그림을 화면에 넣는 법에서 걸리는 것(실물)

| 넣는 법 | 걸리는 것 |
|---|---|
| `<img src>` | SVG 안 글자가 Pretendard 를 가리키는데(73 파일) `<img>` 안의 SVG 는 화면의 `@font-face` 를 못 쓴다 — 기기에 그 폰트가 없으면 대체 글꼴로 그려진다. 앱은 Pretendard 를 정적 파일로 갖고 있다(`A/clinic_chat/consult/static/consult.css:4-6`). 글자 교체(다국어)도 못 한다 |
| 인라인 SVG | 폰트 · 글자 교체는 된다. **id 가 파일 사이에 겹친다** — 새 73 파일의 id 174 종 가운데 40 종이 둘 이상의 파일에 있다(`diagram-title` · `dermis` · `tissue-clip` … 73 파일 전부). 검사의 `unique_svg_ids` 는 파일 안에서의 유일함이다. 한 화면에 둘을 인라인으로 넣으면 그라디언트 · 클립 참조가 엇갈린다 → 넣을 때 id 에 접두어를 붙여야 한다 |
| 어느 쪽이든 | 옛 43 SVG 는 viewBox 가 셋이고 글자가 없다 — 새 그림과 한 자리에 놓으면 비율 · 설명이 다르다 · 캡션(이름)을 앱이 `name_ko` 로 따로 달아야 한다 |
| 인라인이면 | DB · 폴더에서 온 SVG 를 그대로 HTML 에 넣게 된다 — 지금 117 파일에 스크립트 · 외부 참조는 0 이지만(셈) 적재 때 다시 검사하지 않으면 보장이 없다 |

### 6-4. 검수 안 된 것의 처리

- 지금 값으로 거르면 화면에 뜨는 그림은 **0장**이다(117장 전부 「검수 전」).
- 그림이 없을 때 그 자리를 비우나 · 「준비 중」 을 띄우나는 문구다 — 빈 자리 규칙상 앱이 짓지 않는다(SPEC-004 D-17).
- 내부 검수용으로 검수 전 그림을 보는 화면(0.1 의 `/face-check` 같은 것)이 필요한지는 스펙에 없다.
- MEC-070 을 싣는다면 CC BY-SA 4.0 의 표기(저작자 · 출처 · 라이선스)를 그림 옆에 보여야 한다 — 표기 문구도 빈 자리다.

---

## 7. 확인 안 됨

| 무엇 | 왜 |
|---|---|
| 레포 공개 여부(허브 PRIVATE · 앱 · 프로필 PUBLIC) | 브리프 기재를 옮겼다 — 외부 CLI 금지라 원격을 확인하지 않았다 |
| stg · prod 서빙 컨테이너에 마운트를 더할 수 있나 | 인프라 레포 · helper 스크립트를 읽지 않았다. 허브 문서의 「기존 mounts 없음」 한 줄만 확인 |
| 옛 43 SVG ↔ 옛 manifest 36건의 1:1 대응 · 43 − 36 = 7 파일의 출처 | 파일 이름이 `<코드>__<개념>.svg` 로 바뀌었고 대응표가 없다 |
| 별칭 경로 3 을 참조하는 코드가 있나 | 허브 · 앱에 그림 경로를 쓰는 코드가 아직 없다(grep 0) — 그 밖의 소비자는 모른다 |
| 새 73 SVG 가 실제 브라우저에서 화면 폰트로 어떻게 보이나 | 서버를 띄우지 않았다. 검사 기록(`ko_en_render_review: true`)만 확인 |
| 그림의 의료 내용이 맞나 | 조사 범위 밖 — 원천이 「의료 검수 전 초안」 이라고 적었다(`I/README.md:31`) |
| 앱 `consult/` 의 그리기 코드 세부 | 0.2 구현 중이라 미커밋 변경이 있다(`git status` — `col_b.py` · `config.py` · `walk/*` 등) — 스펙(SPEC-004/005)을 기준으로 적었다 |
| `DEFERRABLE` FK 를 가진 표에 새 표를 더할 때 `alembic check` | DB 를 띄우지 않았다 |
