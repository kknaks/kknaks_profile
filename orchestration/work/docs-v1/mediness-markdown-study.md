# mediness 마크다운 렌더·편집 조사

> 2026-09-05 조사. 출처: `harness_works/mediness-app/front/`.
> 용도: 문서함(DEC-004) 편집기 선택(FE-OQ-4) 근거.

## 결론 — 에디터 라이브러리를 쓰지 않는다

mediness 는 **마크다운 편집기 라이브러리가 없다.** 편집은 **순수 `<textarea>` + 모노스페이스**,
렌더는 **`react-markdown`** 이다. WYSIWYG·CodeMirror·Monaco·TipTap·Toast UI 계열 **전부 미사용**.

## 의존성 (`front/package.json`)

| 패키지 | 역할 |
|---|---|
| `react-markdown` ^10.1 | 렌더 |
| `remark-gfm` ^4.0 | 표·체크박스·취소선 등 GFM |
| `rehype-raw` ^7.0 | 본문 내 HTML 허용 |
| `rehype-slug` ^6.0 | 헤딩 id(앵커) |
| `rehype-highlight` ^7.0 | 코드 하이라이트 |

플러그인 세트를 `components/library/markdown/sharedMarkdownProps.tsx` 한 곳에 모아
여러 화면(문서 상세·채팅·회의록·브리핑)이 **같은 렌더 규약**을 공유한다.

## 편집 구현 (`components/department-space/DocumentPane.tsx`)

```tsx
<textarea
  ref={textareaRef}
  value={draft}
  onChange={(e) => onDraftChange(e.target.value)}
  spellCheck={false}
  className="... font-mono text-[13px] leading-[1.65] ..."
  placeholder="markdown 본문을 입력하세요."
/>
```

- **모드 전환** — `preview` ↔ `editor` 를 상태로 토글(같은 창에서 갈아끼움)
- **dirty 판정** — `draft !== detail.body` 비교 한 줄
- **저장** — 명시적 [저장] + `Cmd/Ctrl+S`. **낙관적 갱신 안 함**
- **충돌 처리** — 저장 요청에 `base_version` 을 실어 보내고, **409 `DOCUMENT_CONFLICT`** 면
  draft 를 유지한 채 병합 UX 로 넘긴다. last-write-wins 아님
- 서식 툴바·문법 하이라이트 **없음**

## 우리 적용 (FE-OQ-4 결론)

**같은 방식으로 간다 — `react-markdown` 렌더 + `textarea` 편집.** 근거:

1. **사내에서 검증된 조합**이고 의존성이 가볍다. 에디터 라이브러리는 번들도 크고 커스터마이즈 비용이 크다
2. 디자인이 요구하는 것이 **「마크다운 소스에 문법 기호(`##`·`-`·`>`·`**`)를 `#B3B3B3` 로 흐리게 + 표는 모노스페이스」**(14-library §문서 화면)인데, 이건 **소스 편집 위 얇은 하이라이트**지 WYSIWYG 이 아니다. textarea 위에 하이라이트 레이어를 얹는 방식으로 충분하다
3. 렌더 플러그인 세트를 **한 파일에 모으는 패턴**을 그대로 가져온다 — 문서함·회의록·업무 메모가 같은 규약을 쓰게 된다

**차이 나는 점 (우리 정책)**

| 항목 | mediness | 우리 |
|---|---|---|
| 저장 | 명시적 [저장] + Cmd/S | **자동 저장**(포커스 해제) — 저장 버튼 없음(DEC-004 §4) |
| 버전·충돌 | `base_version` + 409 병합 | **v1 에 버전 관리 없음**(DEC-004). 단일 사용자라 동시 편집 충돌이 사실상 없다 |
| 서식 툴바 | 없음 | **디자인에 있다**(14-library §문서 화면) — 우리는 만든다 |

## 참고 파일

- `components/library/markdown/sharedMarkdownProps.tsx` — 플러그인·컴포넌트 매핑 SoT
- `components/library/MarkdownDocumentView.tsx` — 읽기 전용 렌더(383줄)
- `components/department-space/DocumentPane.tsx` — preview/editor 토글 + 저장·충돌
