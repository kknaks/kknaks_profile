/* 자료 본문 — 마크다운만 그린다.
   ① renderMarkdown(src) : 블록 단위로 갈라 React 요소로 만든다. 폼(form)·스크립트·HTML 은 지원하지 않는다.
   ② FILE_DOCS / FILE_META : 미리보기용 목데이터. 실제 구현에서는 파일 본문·메타 조회 결과가 들어온다. */

/* ---- 인라인: **굵게** · *기울임* · `코드` · [글](주소) ---- */
function mdInline(text, keyBase) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[[^\]]+\]\([^)]+\))/g;
  let last = 0;
  let m;
  let i = 0;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(text.slice(last, m.index));
    const tok = m[0];
    const key = `${keyBase}-i${i++}`;
    if (tok.startsWith('**')) out.push(React.createElement('strong', { key }, tok.slice(2, -2)));
    else if (tok.startsWith('`')) out.push(React.createElement('code', { key, className: 'scax-md__code' }, tok.slice(1, -1)));
    else if (tok.startsWith('[')) {
      const cut = tok.indexOf('](');
      out.push(React.createElement('a', { key, className: 'scax-md__link', href: tok.slice(cut + 2, -1) }, tok.slice(1, cut)));
    } else out.push(React.createElement('em', { key }, tok.slice(1, -1)));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

const mdSlug = (text) => 'h-' + String(text).trim().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '').toLowerCase();

/* 목자 — 문서에서 제목(h1~h3)만 뽑는다. */
function mdOutline(src) {
  return (src || '').replace(/\r/g, '').split('\n')
    .map((l) => l.match(/^(#{1,3})\s+(.*)$/))
    .filter(Boolean)
    .map((m) => ({ level: m[1].length, text: m[2].replace(/[*`]/g, ''), id: mdSlug(m[2].replace(/[*`]/g, '')) }));
}

function renderMarkdown(src) {
  const lines = (src || '').replace(/\r/g, '').split('\n');
  const blocks = [];
  let i = 0;
  let k = 0;
  const key = () => `b${k++}`;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i += 1; continue; }
    /* 코드 블록 */
    if (line.startsWith('```')) {
      const lang = line.slice(3).trim();
      const body = [];
      i += 1;
      while (i < lines.length && !lines[i].startsWith('```')) { body.push(lines[i]); i += 1; }
      i += 1;
      blocks.push(React.createElement('pre', { key: key(), className: 'scax-md__pre', 'data-lang': lang || undefined }, React.createElement('code', null, body.join('\n'))));
      continue;
    }
    /* 구분선 */
    if (/^(-{3,}|\*{3,})$/.test(line.trim())) { blocks.push(React.createElement('hr', { key: key(), className: 'scax-md__hr' })); i += 1; continue; }
    /* 제목 */
    const h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      const lv = h[1].length;
      blocks.push(React.createElement(`h${lv}`, { key: key(), id: mdSlug(h[2].replace(/[*`]/g, '')), className: `scax-md__h${lv}` }, mdInline(h[2], `h${k}`)));
      i += 1;
      continue;
    }
    /* 인용 */
    if (line.startsWith('> ')) {
      const body = [];
      while (i < lines.length && lines[i].startsWith('> ')) { body.push(lines[i].slice(2)); i += 1; }
      blocks.push(React.createElement('blockquote', { key: key(), className: 'scax-md__quote' }, mdInline(body.join(' '), `q${k}`)));
      continue;
    }
    /* 표 */
    if (line.startsWith('|') && lines[i + 1] && /^\|[\s:|-]+\|$/.test(lines[i + 1].trim())) {
      const cells = (row) => row.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
      const head = cells(line);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) { rows.push(cells(lines[i])); i += 1; }
      blocks.push(React.createElement('table', { key: key(), className: 'scax-md__table' }, [
        React.createElement('thead', { key: 'h' }, React.createElement('tr', null, head.map((c, ci) => React.createElement('th', { key: ci }, mdInline(c, `th${ci}`))))),
        React.createElement('tbody', { key: 'b' }, rows.map((r, ri) => React.createElement('tr', { key: ri }, r.map((c, ci) => React.createElement('td', { key: ci }, mdInline(c, `td${ri}-${ci}`)))))),
      ]));
      continue;
    }
    /* 목록 — 할 일(- [ ]) 도 같은 목록으로 */
    if (/^\s*([-*]|\d+\.)\s+/.test(line)) {
      const ordered = /^\s*\d+\./.test(line);
      const items = [];
      while (i < lines.length && /^\s*([-*]|\d+\.)\s+/.test(lines[i])) {
        const raw = lines[i].replace(/^\s*([-*]|\d+\.)\s+/, '');
        const todo = raw.match(/^\[( |x|X)\]\s+(.*)$/);
        items.push(todo
          ? React.createElement('li', { key: items.length, className: `scax-md__todo${todo[1] !== ' ' ? ' scax-md__todo--done' : ''}` }, mdInline(todo[2], `li${items.length}`))
          : React.createElement('li', { key: items.length }, mdInline(raw, `li${items.length}`)));
        i += 1;
      }
      blocks.push(React.createElement(ordered ? 'ol' : 'ul', { key: key(), className: 'scax-md__list' }, items));
      continue;
    }
    /* 문단 */
    const para = [];
    while (i < lines.length && lines[i].trim() && !/^(#{1,4}\s|>\s|```|\||\s*([-*]|\d+\.)\s)/.test(lines[i])) { para.push(lines[i]); i += 1; }
    blocks.push(React.createElement('p', { key: key(), className: 'scax-md__p' }, mdInline(para.join(' '), `p${k}`)));
  }
  return blocks;
}

/* ---- 목데이터: 문서 본문 ---- */
const FILE_DOCS = {
  'f-meet-0904': `# 킥오프 회의록

**일시** 2026-09-04 11:00 · **장소** 회의실 B · **작성** 유하람

프로젝트 탭 개편의 범위와 일정을 맞췄다. 자료함은 트리 구조로 가고, 진행 라인은 간트에 의존선을 얹는다.

## 결정
1. 프로젝트 화면은 3열 — 업무 목록 / 진행 라인 / 업무 상자
2. 자료는 별도 탭으로 분리
3. 문서 형식은 \`.md\` 만 지원한다 (폼·첨부 편집은 범위 밖)

## 할 일
- [x] IA 3안 정리
- [x] 의존선 표기 규칙 합의
- [ ] 업무-자료 연결 규칙 정의
- [ ] 권한 정책 초안 검토

> 다음 주 회의에서 권한 정책 최종안을 다시 본다.

| 구분 | 담당 | 기한 |
| --- | --- | --- |
| IA 확정 | 유하람 | 09-22 |
| 자료함 API | 박민수 | 09-25 |
| 디자인 QA | 박혜진 | 10-02 |`,
  'f-meet-0911': `# 주간 회의 09/11

**참석** 유하람, 박민철, 박민수

## 진행 상황
- 진행 라인 간트 1차 붙였다 — 하위 업무 펼침까지 됨
- 자료함 트리 스타일 업무 탭과 맞춤

## 막힌 것
- 권한 정책 최종안 검토가 **지연** — 재무 토의 대기
- 정산 자료 취합은 부서 회신 2건 남음

---

다음 회의: 09-18 11:00`,
  'f-dev-api': `# 자료함 API 명세

## 목록
\`GET /projects/:id/files\`

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | string | 노드 id |
| kind | \`folder\` \\| \`md\` | 종류 |
| parentId | string | 상위 폴더 |

## 만들기
\`POST /projects/:id/files\`

\`\`\`json
{ "kind": "md", "parentId": "f-plan", "name": "회의록.md" }
\`\`\`

> 지금은 \`md\` 만 만든다. 업로드 파일은 저장만 하고 미리보기는 지원하지 않는다.`,
  'f-plan-prd': `# PRD · 프로젝트 탭

## 배경
업무·회의·자료가 화면마다 흩어져 있어, 프로젝트 단위로 진행 상황을 확인할 자리가 없다.

## 범위
- 프로젝트 단위 업무 목록과 진행 라인(의존선 포함)
- 업무 상자 — 메타 정보 · 체크리스트 · 하위 업무
- 자료는 \`.md\` 문서 보기만

## 범위 밖
- 문서 편집기, 폼 입력, 외부 포맷 미리보기`,
};

/* ---- 목데이터: 파일 메타 ---- */
const FILE_META = {
  'f-meet-0904': { author: '유하람', created: '2026-09-04', updated: '2026-09-04 12:40', size: '4.2 KB', words: 312, version: 'v3', path: '회의', tags: ['회의록', '킥오프'], task: '프로젝트 탭 IA 확정' },
  'f-meet-0911': { author: '박민철', created: '2026-09-11', updated: '2026-09-11 12:05', size: '2.1 KB', words: 148, version: 'v1', path: '회의', tags: ['회의록', '주간'], task: '권한 정책 최종안 검토' },
  'f-dev-api': { author: '박민수', created: '2026-09-09', updated: '2026-09-15 18:22', size: '3.4 KB', words: 205, version: 'v5', path: '개발', tags: ['API', '명세'], task: '자료함 업로드 API 연동' },
  'f-plan-prd': { author: '유하람', created: '2026-09-10', updated: '2026-09-16 09:10', size: '5.8 KB', words: 402, version: 'v7', path: '기획', tags: ['PRD'], task: '프로젝트 탭 IA 확정' },
};

Object.assign(window, { renderMarkdown, mdOutline, FILE_DOCS, FILE_META });
