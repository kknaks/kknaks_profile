---
type: concept
id: pdf-text-layer
title: PDF 텍스트 층 vs 윤곽선 글자
aliases:
  - 텍스트 층
  - 텍스트 레이어
  - 윤곽선 글자
  - 글자 윤곽선
  - outlined text
  - 벡터 윤곽선
  - 스캔 PDF
  - PDF 텍스트 추출
up:
  - 2026-10-15-strong-hajin-attach-read
tags:
  - pdf
  - 텍스트 추출
  - 문서 처리
---

# PDF 텍스트 층 vs 윤곽선 글자

PDF 에서 화면에 보이는 글자는 세 가지 중 하나로 그려진다 — **폰트 + 텍스트 연산자(텍스트 층)**,
**이미지 안의 픽셀(래스터)**, **채움 경로로 그린 도형(윤곽선)**. 추출기가 꺼낼 수 있는 것은 첫째뿐이다.
눈에는 셋 다 같은 글자라서 「글자가 보이는데 추출이 0자」 는 셋 중 어느 것인지 파일 구조를 세어 가른다.

## 정의

1. **텍스트 층** — 쪽 `/Resources` 에 `/Font` 가 있고, 콘텐츠 스트림에 `BT … Tj/TJ … ET` 텍스트 연산자가 있다.
   글자 코드가 남아 있어 추출기가 문자열로 꺼낸다(`ToUnicode` 가 없으면 깨진 글자로 나올 수는 있다)
2. **래스터(스캔)** — 글자가 이미지 픽셀 안에 있다. 이미지는 세 자리에 산다
   - 쪽 리소스의 최상위 Image XObject(`/XObject` → `/Subtype /Image`)
   - Form XObject 안쪽 — 쪽을 재포장한 PDF 에 흔하다. 재귀로 들어가야 보인다
   - 인라인 이미지 — 콘텐츠 스트림의 `BI … ID … EI`. 리소스 사전에 없다
   읽으려면 OCR 이 필요하다
3. **윤곽선** — 폰트도 이미지도 없고 글리프 모양이 `m`(moveto) · `l` · `c`(곡선) + `f`(fill) 경로로 그려져 있다.
   글자 코드가 사라졌으므로 어떤 텍스트 추출기로도 안 나온다. 쪽을 래스터화한 뒤 OCR 해야 읽힌다

**가르는 순서** — 쪽마다 `/Font` 수 · `BT`/`Tj`/`TJ` 수 · 이미지 수(최상위 · Form 재귀 · 인라인)를 센다.

| 폰트 · 텍스트 연산자 | 이미지 | 경로 연산 | 판정 |
|---|---|---|---|
| 있음 | — | — | 텍스트 층. 0자면 추출기 · 인코딩을 의심 |
| 없음 | 있음 | — | 래스터(스캔) |
| 없음 | 없음 | 수백~수천 | 윤곽선 |
| 없음 | 없음 | 거의 없음 | 정말 빈 쪽 |

메타데이터 `/Producer` · `/Creator` 가 어떤 경로로 만들어졌는지 단서를 준다.

## 사용 예시

```python
from pypdf import PdfReader
import re

def probe(page):
    res = page.get("/Resources") or {}
    fonts = len(res.get("/Font") or {})
    data = page.get_contents().get_data() if page.get_contents() else b""
    text_ops = len(re.findall(rb"\b(?:Tj|TJ)\b", data))
    inline = len(re.findall(rb"\bBI\b", data))
    fills = len(re.findall(rb"\bf\*?\b", data))
    images = count_images(res)          # /XObject 를 돌며 /Image 를 세고 /Form 이면 그 /Resources 로 재귀
    return dict(fonts=fonts, text_ops=text_ops, images=images + inline, fills=fills)
```

인터뷰 PDF(3.1MB · 14쪽)를 이렇게 세었더니 13쪽은 폰트 0 · 텍스트 연산자 0 · 이미지 0(Form 재귀 · 인라인 포함) ·
채움 경로 284~839개 · `moveto` 859~2,250개였다. 나머지 1쪽의 텍스트도 공백 글리프 둘뿐. `/Producer` 는 macOS Quartz
PDFContext, `/Creator` 는 Claude — 앱 웹뷰에서 HTML 을 「PDF 로 저장」 한 것이 글자를 윤곽선으로 내보냈다
(Quartz 가 보통 폰트를 임베드하는데 왜 이 파일은 경로가 됐는지는 확인하지 못했다).

## 왜 중요한가

- **세 가설의 처방이 전부 다르다** — 래스터면 OCR, 윤곽선이면 래스터화 + OCR 이나 원본(HTML · 문서)을 받기,
  추출기 문제면 코드 수정. 구조를 세지 않고 「스캔이겠지」 로 정하면 엉뚱한 쪽을 고친다 — 이 실례에서 이미지 판정을
  강화하는 개선안은 효과가 0 이었다(이미지가 정말 0개)
- **코드만 읽어서는 단정할 수 없다** — 분기 조건은 코드에 있지만 파일이 어느 갈래를 탔는지는 파일에 있다.
  화면 증상 조사는 원본 파일을 먼저 받아 운영과 같은 추출기에 넣는 것이 가장 짧은 길이었다
  (첫 조사는 행이 로컬에 없어 형식별 가설로만 끝났다)
- **사용자가 「멀쩡한 문서」 라고 믿는 파일이 기계에는 그림이다** — 「HTML 을 PDF 로 뽑았는데 왜 못 읽나」 는
  자연스러운 질문이고, 안내 문구가 이 갈래를 말해 주지 않으면 사용자는 업로드가 깨졌다고 읽는다

## 경계와 오해

- **윤곽선 ≠ 스캔** — 둘 다 텍스트 층이 없지만 윤곽선은 이미지도 없다. 「텍스트 없음 + 이미지 있음 = 스캔」 판정은
  윤곽선을 「빈 파일」 로 보낸다 → [[failure-reason-classification]]
- **텍스트 층이 있다 ≠ 내용이 읽힌다** — 쪽번호 한 줄만 텍스트 층에 있는 스캔 PDF 는 「텍스트 있음」 이지만 검색엔 거의
  안 걸린다. 0자 임계값은 반대 방향 오판을 만든다
- **깨진 글자 ≠ 0자** — `ToUnicode` 없는 폰트 · Type3 폰트는 대개 엉뚱한 글자를 낸다. 완전히 빈 문자열은 텍스트 연산자가
  없다는 강한 신호다
- **추출기를 바꿔도 안 나온다** — 윤곽선은 꺼낼 글자 코드 자체가 없다. 「다른 라이브러리로 해 보자」 는 `BT` 가 0 이면 의미가 없다
- **최상위 리소스만 보면 이미지를 놓친다** — Form XObject · 인라인 이미지는 `/Resources/XObject` 한 단계 순회에 안 걸린다

## 함께 보는 개념

- [[failure-reason-classification]] — 이 구조 판정 결과를 사용자 사유로 옮길 때의 규칙
- [[character-encoding]] — 텍스트 층이 있어도 글자 코드 → 유니코드 대응(`ToUnicode`)이 없으면 깨진다
- [[multimodal-model]] — OCR 로 텍스트만 뽑는 전처리가 레이아웃을 잃는 대가
- [[dev-prod-parity]] — 합성 픽스처가 아니라 실제 파일로 확인해야 갈래가 보인다

## 출처

- [[2026-10-15-strong-hajin-attach-read]] §2 · §3 — Strong Hajin 결과 자료 PDF 가 「본문에 텍스트가 없습니다」 를 받은 원인 조사.
  쪽별 폰트 · 텍스트 연산자 · 이미지(최상위 · Form 재귀 · 인라인)를 세어 래스터 · 추출기 가설을 지우고 벡터 윤곽선으로 확정
  (`research-attach-read-report.md` §6.2 합성 PDF 다섯 종 · §7 실측)
