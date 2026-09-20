/* 회의 작업 화면(4칸) 데이터. 목록은 data.js 의 MEETING_UPCOMING / MEETING_PAST 를 그대로 쓴다.
   상세 내용은 상태별 표본 하나씩 — 화면이 상태로 갈리는 것을 보이려는 자료다. */

const WS_COPY = {
  info: '회의 정보',
  editInfo: '회의 정보 수정',
  noteHead: 'AI 회의록',
  purpose: '목적',
  edit: '수정',
  save: '저장',
  cancel: '취소',
  start: '회의 시작',
  end: '회의 종료',
  share: '공유',
  export: '내보내기',
  bookNext: '다음 회의 예약',
  tabMemo: '메모',
  tabAi: 'AI 요약',
  tabScript: '스크립트',
  tabMaterials: '첨부',
  attach: '자료 첨부',
  materialsEmpty: '올린 자료가 없습니다.',
  scriptEmpty: '아직 받아 적은 말이 없습니다.',
  summarizingNow: '정리하는 중',
  lastSaved: (t) => `마지막 저장 ${t}`,
  convertFailed: '회의록을 만들지 못했습니다.',
  retry: '다시 시도',
  focus: '회의에 집중',
  exitFocus: '목록 보기',
  startMeeting: '회의 시작',
  endMeeting: '회의 종료',
  agent: '유하람님 회의 시작 전\n안건을 정리해드릴까요?',
  endTitle: '회의를 종료할까요?',
  endBody: '종료하면 녹음이 멈추고 받아 적은 것을 회의록으로 정리합니다.',
  evidence: '근거',
  todos: '다음 할 일',
  promote: '업무 생성',
  dropTodo: '후보 빼기',
  requested: '요청됨',
  addAgenda: '안건 추가',
  agendaPlaceholder: '안건을 적으세요',
  memoPlaceholder: '회의 중 메모를 적으세요',
  panelEmpty: '왼쪽에서 회의를 고르면 회의록이 열립니다.',
  startedBy: (who) => `${who}님이 시작`,
};

/* 완료된 회의 — 최종 회의록. 줄마다 근거 구간의 시작 시각(회의 시작에서 흐른 mm:ss)이 붙는다 */
const WS_AGENDAS_DONE = [
  { id: 'a1', title: '토큰 수요 전망', source: 'carried', concluded: true,
    lines: [
      { id: 'l1', text: '에이전틱 AI 확산으로 토큰 수요가 구조적으로 는다는 전제에 합의했다.', at: ['02:14', '04:02'] },
      { id: 'l2', text: '대응은 인프라 확장과 단위 효율 개선 두 축으로 같이 간다.', at: [] },
      { id: 'l3', text: '수요 전망치는 분기별로 다시 뽑아 다음 회의에 올린다.', at: ['04:02'] },
    ],
    todos: [{ id: 't1', title: '토큰 수요 전망치 분기별로 다시 뽑기', who: '정우성', due: '09-12' }] },
  { id: 'a2', title: '토큰 비용 절감을 위한 AI 인프라 전략', source: 'manual', concluded: true,
    lines: [
      { id: 'l4', text: '절감 다섯 갈래 중 지능형 요청 분배와 KV 캐싱을 먼저 적용한다.', at: ['11:20'] },
      { id: 'l5', text: '캐시 히트는 68%에서 86%로 올랐다.', at: ['19:05'] },
      { id: 'l6', text: 'HBM 제약은 계층 저장으로 넘기되 지연 증가 여부는 아직 측정 전이다.', at: ['22:41'] },
    ],
    todos: [
      { id: 't2', title: '캐시 히트 레이쇼 측정 지표 정의', who: '정우성', due: '09-15' },
      { id: 't3', title: '계층 저장 지연 측정', who: '유하람', due: '09-18', linked: true },
    ] },
];

/* 예정 — 안건만 있고 줄이 없다 */
const WS_AGENDAS_PLANNED = [
  { id: 'p1', title: '9월 정산 범위 확정', source: 'manual' },
  { id: 'p2', title: '취합 담당과 기한', source: 'carried' },
];

/* 진행 중 — 메모 트랙과 AI 트랙이 갈린다.
   메모는 사람이 적은 줄이라 근거 구간이 없다 — 시간 칩이 붙지 않는다. */
const WS_AGENDAS_LIVE = {
  memo: [
    { id: 'a1', title: '토큰 수요 전망', source: 'carried', lines: [
      { id: 'm1', text: '수요 전망은 분기별로 다시 뽑기로.' },
      { id: 'm2', text: '캐시 히트 68 → 86. 측정 조건 확인 필요.' },
    ] },
  ],
  ai: [
    { id: 'a1', title: '토큰 수요 전망', source: 'carried', lines: [
      { id: 'x1', text: '수요 증가 전제에 합의. 대응은 인프라 확장과 단위 효율 개선 두 축.', at: ['02:14'] },
    ], todos: [{ id: 'x2', title: '분기별 수요 전망치 재산출', due: '09-12' }] },
  ],
};

/* 스크립트 — 받아 적은 발화만 선다. 회의 중 메모는 여기 들어오지 않는다 (회의록 「메모」 탭에 산다) */
const WS_SCRIPT = [
  { id: 's1', who: '화자 1', at: '02:14', text: '오늘은 토큰 수요가 어디까지 늘어날지, 그 전제부터 맞춰보고 싶습니다.' },
  { id: 's2', who: '화자 2', at: '04:02', text: '에이전틱 AI 가 사람 개입 없이 처리하는 구간이 늘면 수요는 계단식으로 올라갑니다.' },
  { id: 's4', who: '화자 1', at: '11:20', text: '비용 쪽으로 넘어가면, 저희가 쓰는 절감 전략은 다섯 가지입니다.' },
  { id: 's5', who: '정우성', at: '19:05', text: '라우팅과 KV 캐시 오프로드를 붙였을 때 캐시 히트가 68에서 86까지 올라갔습니다.' },
  { id: 's7', who: '화자 2', at: '22:41', text: 'HBM 이 부족한 구간은 계층 저장으로 넘기는데, 지연은 아직 측정 전입니다.' },
  { id: 's8', who: '화자 1', at: '26:30', text: '협력은 PoC 한 건으로 좁히죠. 성공 기준은 다음 회의에서 정합시다.' },
];

const WS_MATERIALS = [
  { id: 'f1', name: '토큰_수요_전망_2026Q3.xlsx', size: '1.2MB', who: '정우성' },
  { id: 'f2', name: 'AI_인프라_절감안.pdf', size: '340KB', who: '이건학' },
];

/* 회의별 목적 — 없으면 목적 줄이 서지 않는다 */
const WS_PURPOSE = {
  m1: '9월 정산의 취합 범위와 담당을 정한다.',
  m4: 'DB 영역의 AX 전환 범위를 정하고, 토큰 비용 구조에 합의한 뒤 PoC 한 건을 확정한다.',
};

Object.assign(window, { WS_COPY, WS_AGENDAS_DONE, WS_AGENDAS_PLANNED, WS_AGENDAS_LIVE, WS_SCRIPT, WS_MATERIALS, WS_PURPOSE });
