# TheSC AX 화면 패키지

## 실행
```
cd package
npx serve .        # 또는: python3 -m http.server 8000
```
브라우저에서 `index.html` 열기. (file:// 직접 열기는 JSX 로딩이 CORS 로 막힙니다.)

## 구성
- `index.html` — 화면 목록
- `MyWork.html` `Projects.html` `Calendar.html` `MeetingWorkspace.html` `Files.html` — 각 화면
- `handoff/<screen>/css|js` — 화면별 스타일·JSX·목데이터, `handoff/shell` 공용 내비·모달·UI, `handoff/shared` 공용 업무 데이터
- `_ds_bundle.css` / `_ds_bundle.js` — 디자인 시스템 토큰·컴포넌트
- `styles.css` — 전역 리셋
- `fonts/` — Pretendard / Pretendard JP (SIL OFL 1.1)

## 의존성
React 18.3.1 · ReactDOM · Babel standalone 을 unpkg CDN 에서 로드합니다(버전 고정 + integrity). 완전 오프라인이 필요하면 세 파일을 로컬로 내려 각 HTML 의 `<script src>` 를 바꿔 주세요.

## 데이터
모두 목데이터입니다. API 연결 지점은 `handoff/*/js/data.js` 와 `handoff/shared/js/work-data.js`.
