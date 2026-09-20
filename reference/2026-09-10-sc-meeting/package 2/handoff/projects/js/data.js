/* 「프로젝트」 화면 데이터 — 헤더 셀렉터 · 업무는 공용 목데이터(WORK_TASKS)를 프로젝트에 묶어 쓴다 · 자료 트리. */

const PROJECT_OPTIONS = [
  { value: 'p-ax', label: 'AX 워크스페이스 개편' },
  { value: 'p-data', label: '사내 데이터 허브 구축' },
  { value: 'p-brand', label: '브랜드 리뉴얼 2기' },
  { value: 'p-mobile', label: '모바일 앱 1.0' },
  { value: 'p-onboard', label: '온보딩 자동화' },
];

/* 업무 ↔ 프로젝트 배정. 실제 구현에서는 tasks.project_id 다. */
const PROJECT_TASK_MAP = {
  'p-ax': ['w1', 'w6', 'w10', 'w4', 'w15', 'x1', 'd3'],
  'p-data': ['w9', 'w17', 'w18', 'x3'],
  'p-brand': ['w5', 'w14', 'w16', 'x2'],
  'p-mobile': ['w3'],
  'p-onboard': ['w2', 'w8', 'x4', 'd1'],
};

const PROJECT_STATUS_BADGE = {
  progress: { label: '진행 중', tone: 'accent' },
  'not-started': { label: '대기', tone: 'neutral' },
  blocked: { label: '지연', tone: 'danger' },
  done: { label: '완료', tone: 'positive' },
  cancelled: { label: '취소', tone: 'neutral' },
};

/* 레일 카드에 필요한 꼴로 고른다 — 캘린더 ItemCard 와 같은 필드(when · meta). */
function projectTasks(projectId) {
  const ids = PROJECT_TASK_MAP[projectId] || [];
  return ids
    .map((id) => WORK_TASKS.find((t) => t.id === id))
    .filter(Boolean)
    .map((t) => {
      const st = PROJECT_STATUS_BADGE[t.status] || PROJECT_STATUS_BADGE.progress;
      const group = t.group === 'sent' ? '보낸 업무' : t.group === 'done' ? '완료' : '내 업무';
      return {
        id: t.id,
        title: t.title,
        badge: t.badge || st.label,
        badgeTone: t.badgeTone || st.tone,
        when: t.from ? `9월 ${t.from}일 ~ ${t.to}일` : t.due ? `9월 ${t.due}일 마감` : '기한 없음',
        meta: [t.owner, group].filter(Boolean),
      };
    });
}

/* 업무 간 의존(선행 → 후행). 실제 구현에서는 task_dependencies 표다. */
const PROJECT_DEPS = {
  w6: ['w1'], w10: ['w6'], x1: ['w10'], w4: ['w1'],
  w17: ['w9'], w18: ['w9'], x3: ['w17'],
  w14: ['w5'], w16: ['w14'], x2: ['w16'],
  w8: ['w2'], x4: ['w8'],
};

/* 진행률(%). 실제 구현에서는 tasks.progress 다. */
const PROJECT_PROGRESS = { w1: 100, w2: 70, w3: 10, w4: 40, w5: 100, w6: 85, w8: 30, w9: 55, w10: 20, w14: 60, w15: 0, w16: 0, w17: 45, w18: 15, x1: 25, x2: 0, x3: 0, x4: 50, d1: 100, d3: 100 };

/* 하위 업무 — 상위 업무 id 아래에 달린다. 실제 구현에서는 tasks.parent_id 다. */
const PROJECT_SUBTASKS = {
  w1: [
    { id: 'w1-1', title: '구성 잡기', owner: '유하람', status: 'done', from: 2, to: 2, progress: 100 },
    { id: 'w1-2', title: '내용 초안', owner: '박혀진', status: 'done', from: 3, to: 3, progress: 100 },
    { id: 'w1-3', title: '도표 정리', owner: '유하람', status: 'done', from: 4, to: 4, progress: 100, deps: ['w1-2'] },
  ],
  w4: [
    { id: 'w4-1', title: '통상 지표 수집', owner: '박및수', status: 'done', from: 16, to: 16, progress: 100 },
    { id: 'w4-2', title: '인상 시나리오 3안', owner: '유하람', status: 'blocked', from: 17, to: 18, progress: 20, deps: ['w4-1'] },
  ],
  w6: [
    { id: 'w6-1', title: '본문 쓰기', owner: '유하람', status: 'progress', from: 4, to: 4, progress: 90 },
  ],
};

/* 간트에 쓰는 꼴 — 시작·끝 일자(9월 기준), 진행률, 선행 업무, 하위 업무. */
function projectTimeline(projectId) {
  const ids = PROJECT_TASK_MAP[projectId] || [];
  return ids
    .map((id) => WORK_TASKS.find((t) => t.id === id))
    .filter((t) => t && (t.from || t.due))
    .map((t) => ({
      id: t.id,
      title: t.title,
      owner: t.owner,
      status: t.status,
      from: t.from || t.due,
      to: t.to || t.due,
      progress: PROJECT_PROGRESS[t.id] != null ? PROJECT_PROGRESS[t.id] : 0,
      deps: (PROJECT_DEPS[t.id] || []).filter((d) => ids.indexOf(d) >= 0),
      children: (PROJECT_SUBTASKS[t.id] || []).map((c) => Object.assign({ deps: [] }, c)),
    }))
    .sort((a, b) => a.from - b.from || a.to - b.to);
}

/* 요약 — 진행 중·지연·완료 개수와 전체 진행률. */
function projectSummary(projectId) {
  const ids = PROJECT_TASK_MAP[projectId] || [];
  const rows = ids.map((id) => WORK_TASKS.find((t) => t.id === id)).filter(Boolean);
  const count = (s) => rows.filter((t) => t.status === s).length;
  const sum = rows.reduce((n, t) => n + (PROJECT_PROGRESS[t.id] || 0), 0);
  return {
    total: rows.length,
    progress: count('progress') + count('not-started'),
    blocked: count('blocked'),
    done: count('done'),
    percent: rows.length ? Math.round(sum / rows.length) : 0,
  };
}

/* 업무 상자 — 우 레일에 쓰는 체크리스트. 실제 구현에서는 task_checklists 다. */
const PROJECT_CHECKLIST = {
  w1: [
    { id: 'c1', text: '발표 목적·대상 합의', done: true },
    { id: 'c2', text: '경쟁 사례 3건 수집', done: true },
    { id: 'c3', text: '도표 5장 제작', done: false },
    { id: 'c4', text: '감수 1차 반영', done: false },
  ],
  w4: [
    { id: 'c1', text: '현행 단가표 확인', done: true },
    { id: 'c2', text: '인상률 시나리오 3안', done: false },
    { id: 'c3', text: '재무 토의', done: false },
  ],
  w6: [
    { id: 'c1', text: '본문 톤 맞추기', done: true },
    { id: 'c2', text: '추가 자료 링키', done: false },
  ],
  w9: [
    { id: 'c1', text: '부서별 제출 현황 점검', done: true },
    { id: 'c2', text: '니칼 문의 회신', done: false },
  ],
};

/* 우 레일에 필요한 것을 한 번에 — 상위·하위 업무 모두 지원한다. */
function projectTaskDetail(projectId, taskId) {
  if (!taskId) return null;
  const rows = projectTimeline(projectId);
  let row = rows.find((r) => r.id === taskId);
  let parent = null;
  if (!row) {
    rows.some((r) => {
      const kid = r.children.find((c) => c.id === taskId);
      if (kid) { row = Object.assign({ children: [], deps: [] }, kid); parent = r; return true; }
      return false;
    });
  }
  if (!row) {
    /* 기한 없는 업무는 간트에 없다 — 공용 표에서 집는다 */
    const t = WORK_TASKS.find((x) => x.id === taskId);
    if (!t) return null;
    row = { id: t.id, title: t.title, owner: t.owner, status: t.status, from: t.from || t.due, to: t.to || t.due, progress: PROJECT_PROGRESS[t.id] || 0, deps: [], children: [] };
  }
  const src = WORK_TASKS.find((x) => x.id === taskId);
  const nodeOf = (id) => {
    const t = WORK_TASKS.find((x) => x.id === id);
    if (t) return { id, title: t.title, status: t.status };
    let hit = null;
    Object.keys(PROJECT_SUBTASKS).forEach((k) => { const c = PROJECT_SUBTASKS[k].find((s) => s.id === id); if (c) hit = { id, title: c.title, status: c.status }; });
    return hit || { id, title: id, status: 'progress' };
  };
  const ids = PROJECT_TASK_MAP[projectId] || [];
  const subIds = Object.keys(PROJECT_SUBTASKS).reduce((all, k) => all.concat(PROJECT_SUBTASKS[k].map((c) => ({ id: c.id, deps: c.deps || [] }))), []);
  const next = ids
    .filter((id) => (PROJECT_DEPS[id] || []).indexOf(taskId) >= 0)
    .concat(subIds.filter((s) => s.deps.indexOf(taskId) >= 0).map((s) => s.id))
    .map(nodeOf);
  return {
    row,
    parent,
    status: PROJECT_STATUS_BADGE[row.status] || PROJECT_STATUS_BADGE.progress,
    when: row.from ? (row.from === row.to ? `9월 ${row.from}일` : `9월 ${row.from}일 ~ ${row.to}일`) : '기한 없음',
    requester: src && src.requester && src.requester !== '-' ? src.requester : null,
    group: src ? (src.group === 'sent' ? '보놌 업무' : src.group === 'done' ? '완료' : '내 업무') : '하위 업무',
    prev: (row.deps || []).map(nodeOf),
    next,
    checklist: PROJECT_CHECKLIST[taskId] || [],
    children: row.children || [],
  };
}

/* 자료 트리 — 폴더/파일. children 있으면 폴더다. */
const PROJECT_FILE_TREE = [
  {
    id: 'f-plan', name: '기획', open: true, children: [
      { id: 'f-plan-ia', name: 'IA_v3.fig', meta: '09-12 · 유하람' },
      { id: 'f-plan-prd', name: 'PRD_프로젝트탭.docx', meta: '09-10 · 유하람' },
      {
        id: 'f-plan-old', name: '이전 안', children: [
          { id: 'f-plan-old-1', name: 'IA_v2.fig', meta: '08-21 · 유하람' },
          { id: 'f-plan-old-2', name: 'IA_v1.fig', meta: '07-30 · 유하람' },
        ],
      },
    ],
  },
  {
    id: 'f-design', name: '디자인', open: true, children: [
      { id: 'f-design-ds', name: 'DS_토큰표.xlsx', meta: '09-08 · 박혜진' },
      { id: 'f-design-sh', name: '화면_시안.pdf', meta: '09-14 · 박혜진' },
    ],
  },
  {
    id: 'f-dev', name: '개발', children: [
      { id: 'f-dev-api', name: 'API_명세.md', meta: '09-09 · 박민수' },
      { id: 'f-dev-arch', name: '아키텍처.drawio', meta: '08-28 · 박민수' },
    ],
  },
  {
    id: 'f-meet', name: '회의', children: [
      { id: 'f-meet-0904', name: '0904_킥오프.md', meta: '09-04 · 유하람' },
      { id: 'f-meet-0911', name: '0911_주간.md', meta: '09-11 · 박민철' },
    ],
  },
];

Object.assign(window, { PROJECT_OPTIONS, PROJECT_TASK_MAP, PROJECT_STATUS_BADGE, PROJECT_DEPS, PROJECT_PROGRESS, PROJECT_SUBTASKS, PROJECT_CHECKLIST, projectTasks, projectTimeline, projectSummary, projectTaskDetail, PROJECT_FILE_TREE });
