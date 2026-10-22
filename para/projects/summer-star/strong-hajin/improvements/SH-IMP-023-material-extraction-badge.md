# SH-IMP-023 — 결과 자료 「내용을 읽지 못함」 배지 문구가 너무 길다

상태: 미착수  
생성일: 2026-10-13  
갱신일: 2026-10-13  
출처: 사용자 2026-10-13 (HTML 을 PDF 로 뽑아 결과 자료에 올림 — 「내용을 읽지 못함 · 본문에 텍스트가 없습니다 (스캔 이미지 PDF 또는 빈 파일)」 배지가 잘려서 뜸)

## 문제

결과 자료 행의 추출 실패 배지가 `내용을 읽지 못함 · <사유 문장>` 으로 길게 붙어서 행 폭을 넘어 잘린다.
빨간색에 긴 문장이라 **파일 업로드 자체가 실패한 것처럼** 보이지만, 파일은 정상으로 올라가 있다(열기 ·
다운로드 · 완료 보고 첨부 정상). 안 되는 것은 AX 자료 검색 대상에서 빠지는 것뿐이다.

## 원하는 동작

배지에는 **「내용을 읽지 못함」만** 보인다. 사유 문장은 배지 `title`(마우스 올림)에 이미 들어 있으므로 거기에만 둔다.

## 고칠 자리

- `frontend/src/features/work/WorkModals.tsx` `ExtractionStatus` 의 마지막 분기 — 배지 본문 뒤에 붙는
  `` ` · ${extraction.failure_text}` `` 를 뺀다(`title` 은 그대로)
- 같은 분기를 쓰는 「검색 미지원 형식」도 같이 짧아진다 — 같이 줄일지는 착수 때 확인(기본: 둘 다 짧게)
- 합쳐진 문구를 단언하는 FE 테스트가 있으면 같이 고친다

## 조사로 드러난 것 (이번 항목 범위 밖 — 참고)

조사: `orchestration/work/strong-hajin-attach-read/research-attach-read-report.md` (backend 워커 read-only, 2026-10-13)

- **이번 파일의 원인**: Claude 가 만든 HTML 을 macOS Quartz PDFContext 로 PDF 화 → 글자가 전부 **벡터 윤곽선**
  (14쪽 · 폰트/텍스트 연산자 0 · 이미지 0 · 추출 0자). 텍스트도 이미지도 없으니 `empty_content` 판정은 현 계약대로다.
  사용자 우회: Chrome 「인쇄 → PDF로 저장」으로 다시 뽑거나 원본 HTML 을 올린다.
- 사유 문장 「스캔 이미지 PDF 또는 빈 파일」은 PDF 를 전제하고, 윤곽선 PDF · 그림만 있는 PPTX 도 같은 문장을 받는다
- PDF 이미지 판정이 최상위 Image XObject 만 본다 — Form 으로 감싼 이미지 · 인라인 이미지는 `needs_ocr` 가 아니라
  `empty_content` 로 오판(합성 PDF 로 확인). Office 형식은 이미지 판정 자체가 없다
- `needs_ocr` 로 판정돼도 저장 때 `status=failed` 로 바뀐다(`modules/work/material_extraction.py` `finish()`) —
  FE 의 「스캔 문서 · 내용 검색 불가」 배지는 실데이터로 뜨지 않는다. 설계 문서(§6 `status=needs_ocr`)와 어긋남
- 추출 실패 자료를 다시 추출할 수단이 UI · API 에 없다. OCR 은 미도입(설계상 별도 결정)

## 진행 관리

- [ ] 「검색 미지원 형식」도 같이 줄일지 확인
- [ ] FE 고침 → 앱에서 확인
