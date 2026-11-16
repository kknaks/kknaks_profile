# interpret-pwa-seed-tw 대만어 사전 2차(D-38) 결과 보고

## 상태: done (커밋 · push 안 함)

## 수행 — 파일
- `back/seed/glossary.json` — version `2026-10-27.4` → `2026-10-27.5` · zh-Hant entry 40개 바꿈(zh 대륙 · 다른 언어는 손대지 않음)
- `back/tests/test_seed.py` — D-35 시험 수치 조정(web-research 77→86 · reviewed 38→44 · source 에 `manual` 허용) + 새 시험 `test_repo_seed_taiwan_second_pass`
- 일회용 변환 스크립트는 레포 밖(scratchpad). s2tw 재생성은 `scripts/import_glossary.draft_zh_hant`(= `to_display("zh-Hant")`, s2tw + 激光→雷射)를 그대로 썼다

## 규칙
- 톡신 · 대륙식 고침 = `source: "web-research 2026-10-27"` · note = 근거 URL(` · ` 로 이음) · 출처 2곳 이상만 reviewed true
- 한국 전용 → 영문 = `source: "manual"`(조사로 찾은 이름이 아니라 D-38 규칙으로 정한 이름) · reviewed false · note 「대만 클리닉 3곳에 중문명 없음 — 영문 브랜드명(D-38)」 · 옛 초안은 s2tw 로 다시 만든 값을 alias 로
- 匯入 · 專案 · 裝置 · 鐳射 는 name · alias 어디에도 두지 않음(옛 표기로도)

## 바꾼 term (전 → 후 · zh-Hant `name / [aliases] · source · reviewed`)

| id | ko | 왜 | 전 | 후 |
|---|---|---|---|---|
| ph-031 | 레티보 | 톡신 대만 허가명 | `樂提保` / [Letibo] · draft-s2twp · false | `保提拉` / [Letybo, 白毒, 輕齡肉毒, 精品肉毒, 樂提保, Letibo] · web-research 2026-10-27 · true |
| ph-042 | 보툴렉스 | 톡신 대만 허가명 | `白毒‌` / [Botulax] · draft-s2twp · false | `保提拉` / [Letybo, 白毒, 輕齡肉毒, 精品肉毒, 樂提保, Botulax] · web-research 2026-10-27 · true |
| ph-041 | 메디톡신 | 톡신 대만 허가명 | `粉毒` / [Meditoxin] · draft-s2twp · false | `優力柔` / [Neuronox, 粉毒, 奇蹟肉毒, Meditoxin] · web-research 2026-10-27 · true |
| ph-027 | 나보타 | 톡신 대만 허가명 | `綠毒` / [Nabota] · draft-s2twp · false | `娜柏塔` / [NABOTA, 彩虹肉毒, 綠毒] · web-research 2026-10-27 · true |
| ph-001 | 신펄 | 한국 전용 → 영문 | `新珍珠` / [Synpurl] · draft-s2twp · false | `Synpurl` / [新珍珠] · manual · false |
| ph-004 | 더채움 | 한국 전용 → 영문 | `彩韻Plus` / [The Chaeum] · draft-s2twp · false | `The Chaeum` / [彩韻Plus] · manual · false |
| ph-008 | 엘라비에 | 한국 전용 → 영문 | `艾拉薇` / [Elravie] · draft-s2twp · false | `Elravie` / [艾拉薇] · manual · false |
| ph-040 | 리즈톡스 | 한국 전용 → 영문 | `麗姿妥適` / [Liztox] · draft-s2twp · false | `Liztox` / [麗姿妥適] · manual · false |
| ph-044 | 타임버스 | 한국 전용 → 영문 | `時光巴士` / [Timbus] · draft-s2twp · false | `Tyemvers` / [時光巴士, Timbus] · manual · false |
| ph-060 | 미라클 | 한국 전용 → 영문 | `奇蹟線` / [Miracle Thread] · draft-s2twp · false | `Miracle Thread` / [奇蹟線] · manual · false |
| ph-062 | 에버라인 | 한국 전용 → 영문 | `艾芙萊恩` / [Everline] · draft-s2twp · false | `Everline` / [艾芙萊恩] · manual · false |
| ph-070 | 벨피엔 | 한국 전용 → 영문 | `貝爾菲恩` / [Belpien] · draft-s2twp · false | `BelPN` / [貝爾菲恩, Belpien] · manual · false |
| ph-083 | 에스에프 | 한국 전용 → 영문 | `SF注射` / [SF Injection] · draft-s2twp · false | `SF Injection` / [SF注射] · manual · false |
| ph-084 | 큐어스킨 | 한국 전용 → 영문 | `CureSkin` / [] · draft-s2twp · false | `CureSkin` / [] · manual · false |
| ph-110 | 글로벨라 | 한국 전용 → 영문 | `格洛貝拉` / [Glovella] · draft-s2twp · false | `Glovella` / [格洛貝拉] · manual · false |
| ph-124 | 더블로골드 | 한국 전용 → 영문 | `多普勒金` / [Doublo Gold] · draft-s2twp · false | `Doublo Gold` / [多普勒金] · manual · false |
| ph-134 | 시크릿 | 한국 전용 → 영문 | `Secret黃金微針` / [] · draft-s2twp · false | `Secret RF` / [Secret黃金微針] · manual · false |
| ph-136 | 아그네스 | 한국 전용 → 영문 | `雅格尼斯` / [AGNES] · draft-s2twp · false | `AGNES` / [雅格尼斯] · manual · false |
| ph-137 | 인트라셀 | 한국 전용 → 영문 | `英特拉賽爾` / [INTRACELL] · draft-s2twp · false | `INTRAcel` / [英特拉賽爾, INTRACELL] · manual · false |
| ph-149 | 마이셀 | 한국 전용 → 영문 | `瑪伊賽爾` / [Mycell] · draft-s2twp · false | `Mycell` / [瑪伊賽爾] · manual · false |
| ph-150 | 셀피아 | 한국 전용 → 영문 | `賽爾皮亞` / [Cellpia] · draft-s2twp · false | `Cellpia` / [賽爾皮亞] · manual · false |
| ph-151 | 리젠ACR | 한국 전용 → 영문 | `瑞珍ACR` / [RegenACR] · draft-s2twp · false | `RegenACR` / [瑞珍ACR] · manual · false |
| ph-155 | MCT (메타셀) | 한국 전용 → 영문 | `MCT` / [] · draft-s2twp · false | `MCT` / [] · manual · false |
| ph-026 | 턱선 | 대륙식 | `下頜線` / [] · draft-s2twp · false | `下顎線` / [下頜線] · web-research 2026-10-27 · false |
| ph-047 | 턱선보톡스 | 대륙식(ph-026 따라) | `下頜線肉毒` / [] · draft-s2twp · false | `下顎線肉毒` / [下頜線肉毒] · manual · false |
| ph-093 | 초음파관리 | 대륙식 | `超聲波護理` / [] · draft-s2twp · false | `超音波導入` / [超音波護理, 超聲波護理] · web-research 2026-10-27 · false |
| ph-096 | 이온토포레시스 | s2twp 오변환(匯入) | `離子匯入` / [] · draft-s2twp · false | `離子導入` / [] · web-research 2026-10-27 · false |
| ph-116 | 무세포동종진피(hADM) | 대륙식 | `無細胞同種真皮` / [hADM] · draft-s2twp · false | `異體真皮` / [無細胞同種真皮, hADM, 異體真皮粉, 脫細胞真皮基質] · web-research 2026-10-27 · true |
| ph-059 | DCA (지방세포파괴) | 대륙식 | `脂肪細胞破壞` / [DCA] · draft-s2twp · false | `去氧膽酸` / [倍克脂, DCA, Belkyra, 脂肪細胞破壞] · web-research 2026-10-27 · true |
| ph-126 | 슈링크유니버스 | 슈링크유니버스 = 媚必提 | `海芙音波` / [Shurink Universe, Shurink, 韓版音波] · web-research 2026-10-27 · true | `海芙音波媚必提` / [海芙音波, 媚必提, Ultraformer MPT, 海芙媚必提, Shurink Universe, Shurink, 韓版音波] · web-research 2026-10-27 · true |
| ph-130 | 써마지FLX | alias 추가 | `鳳凰電波` / [美版熱瑪吉FLX, Thermage FLX, 熱瑪吉, 美版電波] · web-research 2026-10-27 · true | `鳳凰電波` / [美版熱瑪吉FLX, Thermage FLX, 熱瑪吉, 美版電波, 第四代電波拉皮] · web-research 2026-10-27 · true |
| ph-135 | 포텐자 | 無限電波 출처 추가 | `黃金微針` / [無限電波, Potenza] · web-research 2026-10-27 · false | `黃金微針` / [無限電波, Potenza] · web-research 2026-10-27 · false |
| ph-121 | 울쎄라 | 모호어 alias 삭제 | `美國音波` / [美版超聲刀, Ultherapy, Ulthera, 極線音波, 美版音波, 音波拉提] · web-research 2026-10-27 · true | `美國音波` / [美版超聲刀, Ultherapy, Ulthera, 極線音波, 美版音波] · web-research 2026-10-27 · true |
| ph-123 | 올리지오 | 모호어 alias 삭제 | `玩美電波` / [Oligio, 超玩美電波, 韓版電波, 小鳳凰] · web-research 2026-10-27 · true | `玩美電波` / [Oligio, 超玩美電波, 韓版電波] · web-research 2026-10-27 · true |
| ph-074 | 스킨부스터 | 모호어 alias 삭제 | `水光針` / [水光槍] · web-research 2026-10-27 · true | `水光針` / [] · web-research 2026-10-27 · true |
| ph-089 | 물광 | 모호어 alias 삭제 | `水光` / [水光針] · web-research 2026-10-27 · false | `水光` / [] · web-research 2026-10-27 · false |
| ph-092 | 주입장비 | s2tw 재생성 | `匯入裝置` / [] · draft-s2twp · false | `導入設備` / [] · draft-s2twp · false |
| ph-097 | 시그니처프로그램 | s2tw 재생성 | `特色專案` / [] · draft-s2twp · false | `特色項目` / [] · draft-s2twp · false |
| ph-127 | 시그니처 프로그램 | s2tw 재생성 | `特色專案` / [] · draft-s2twp · false | `特色項目` / [] · draft-s2twp · false |
| ph-142 | 니들RF 장비 | s2tw 재생성 | `微針式RF裝置` / [] · draft-s2twp · false | `微針式RF設備` / [] · draft-s2twp · false |

- 남은 초안(`draft-s2twp`, 뉴럭스 ph-028 제외 51개)은 전부 s2tw 로 다시 만들었다. 값이 실제로 달라진 것은 위 4개(ph-092 · 097 · 127 · 142)뿐 — 나머지 초안은 이미 s2tw 결과와 같았다
- ph-042 옛 name `白毒` 에 붙어 있던 보이지 않는 글자(U+200C)는 alias 로 옮길 때 지웠다

## 지운 alias (모호어 · 표 C — zh-Hant 만)

| id | ko | 지운 alias | 이유 |
|---|---|---|---|
| ph-121 | 울쎄라 | `音波拉提` | HIFU 일반명 — ph-131 name 으로만 |
| ph-123 | 올리지오 | `小鳳凰` | C-2 鳳凰 계열(鳳凰電波 · 鳳凰光 · 小鳳凰) |
| ph-074 | 스킨부스터 | `水光槍` | C-4 水光 계열 — ph-090 메조건 name 과 겹침 |
| ph-089 | 물광 | `水光針` | C-4 水光 계열 — ph-074 스킨부스터 name 과 겹침 |

- 그 밖에 `黃金微針` · `熊貓` · `光纖` · `素顏針` · `素妍針` · `鳳凰`(단독) 은 원래 zh-Hant alias 에 없었다(시험으로 0 확인)

## 검증
- `uv run ruff check .` — All checks passed
- `uv run pytest -q` — **247 passed**(새 시험 1 포함) · 시드 로더 검사 통과
- 새 시험이 보는 것: 톡신 3 이름(保提拉 ×2 · 優力柔 · 娜柏塔) + alias + reviewed · 妙盾 없음 · 한국 전용 5개 = en name · manual · 뉴럭스 그대로 · 대륙식 name 0(下頜線 · 超聲波護理 · 離子匯入 · 無細胞同種真皮 · 脂肪細胞破壞) · 匯入/專案/裝置/鐳射 zh-Hant name · alias 0 · 媚必提 · 第四代電波拉皮 · 無限電波 · 音波拉提 울쎄라 0 · 표 C 말 alias 0
- 실물(Soniox · 시드 2026-10-27.5 · lang zh-Hant · 레포 밖 `.env` 는 읽기만 · 값 출력 없음 · 입력 음성은 Soniox TTS zh)
  - 「我想打保提拉」 → `레티보를 맞고 싶어요.` ✅(보툴렉스 · 레티보가 같은 name 保提拉 이라 Soniox 가 레티보를 골랐다 — 같은 제품)
  - 「我想打彩虹肉毒」 → `나보타를 맞고 싶어.` ✅
  - errors 0

## 계약 대조 (DEC-001 D-38)
- ① 톡신 대만 허가명 — 같음 ② 한국 전용 = 영문 — 같음 ③ 대륙식 · 오변환 — 같음 ④ 모호어 — 같음(아래 예외 1) ⑤ 새 시술 안 넣음 — 같음 · zh 그대로 — 같음
- 스키마 SPEC-001 §4.2 — 바꾼 것 없음(source 는 기존 허용값 `manual` · `web-research <날짜>` · `draft-s2twp` 만 씀)

## 이슈 · 코디가 확인할 것
1. **ph-135 포텐자 name 이 아직 `黃金微針`** — 브리프는 alias `無限電波`(이미 있었음 · note 에 tresure URL 만 덧붙임)만 지시. 표 C-3 은 黃金微針 을 모호어로, 리포트 §6-4 는 name `無限電波` 후보로 적었다. name 을 바꿀지 결정 필요
2. ph-134 시크릿 alias `Secret黃金微針`(옛 초안) — 黃金微針 이 들어 있지만 상표가 붙은 합성어라 남겼다
3. ph-112 스컬트라 alias `素顏萃童顏針` — 素顏 이 들어 있지만 Sculptra 하나를 가리키는 말이라 남겼다(C-5 혼동은 素顏針 대 素妍針)
4. ph-126 alias `海芙音波` · `Shurink` 는 3세대(Ultraformer III)를 가리킬 수도 있음(C-1) — 브리프대로 alias 로 둠
5. ph-130 alias `熱瑪吉` · `美版熱瑪吉FLX` — tresure 가 「대만 표기 아님」이라고 했지만 브리프 범위 밖이라 그대로(D-35 시험도 이것을 요구)
6. **코어톡스는 사전에 없다** — 한국 전용 영문 처리 대상에서 빠짐(D-38 ⑤ 새 시술 안 넣음)
7. 리쥬란(ph-072 · 075 · 079)은 zh-Hant name 이 이미 `麗珠蘭` 이라 추가할 것이 없었다(reviewed 그대로). 黑盒/紅盒/白盒 alias 는 3 사이트에 없지만 지시 밖이라 둠
8. 메디톡신 alias 에 `奇肌肉毒`(tresure 1곳)은 브리프 목록에 없어 넣지 않았다
9. 한국 전용 목록에 포함한 19개: 1차 §4 묶음에서 톡신 4(나보타 · 레티보 · 메디톡신 · 보툴렉스) · 뉴럭스를 뺀 나머지(+ 리즈톡스 · 신펄 · 더채움 · 엘라비에 · 리젠ACR). ph-084 큐어스킨 · ph-155 MCT 는 이미 영문이라 source · note 만 바뀜. ph-044 타임버스 en name 은 `Tyemvers`(Procedure Hub 표기 그대로 — 철자 확인 필요)

## 추가 — 코디 처분(ph-135 포텐자)
- zh-Hant `黃金微針` / [無限電波, Potenza] → **`無限電波` / [Potenza]** · web-research 2026-10-27 · reviewed false · note `https://tresure-clinic.com/gold-microneedling/`(출처 1 — 黃金微針 근거였던 creatrip URL 은 뺌)
- `黃金微針` 은 name · alias 어디에도 없음(표 C-3). 시험 `test_repo_seed_taiwan_second_pass` 에 포텐자 name == 無限電波 · 黃金微針 0 추가
- ruff 깨끗 · pytest **247 passed** · 위 이슈 1 해소
