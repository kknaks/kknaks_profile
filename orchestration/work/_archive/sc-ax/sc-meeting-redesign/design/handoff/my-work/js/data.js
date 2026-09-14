/* Screen data for 「내 업무」 — copy is exactly the current screen's copy. */

const INBOX_FILTERS = [
  { value: 'all', label: '전체' },
  { value: 'task', label: '업무' },
  { value: 'cc', label: '참고' },
];

const INBOX_ITEMS = [
  {
    id: 'i1',
    kind: 'task',
    badge: '업무',
    title: '8월 매출 자료 오늘까지 보내주세요.',
    excerpt: '데모에서 업무·회의·자료가 채팅에서 안전하게 이어지는 경험을 검증한다. 여섯줄까지 말줄임 없이 노...',
    who: '홍길동',
    avatar: './assets/avatar-person.png',
    date: '2026.10.10',
    source: '메일',
    sourceIcon: 'mail',
    primary: '내 업무로',
    secondary: '답장',
  },
  {
    id: 'i2',
    kind: 'cc',
    badge: '참고',
    title: '[9월 정산 자료 취합]에 참조로 걸렸습니다',
    who: '홍길동',
    avatar: './assets/avatar-person.png',
    date: '2026.10.10',
    source: '메일',
    sourceIcon: 'mail',
    primary: '원문 확인하기',
    secondary: '확인완료',
  },
  {
    id: 'i3',
    kind: 'cc',
    badge: '참고',
    title: '[사내 공지] 추석 연휴 근무 안내',
    who: '총무팀',
    avatar: './assets/avatar-company.png',
    date: '2026.10.10',
    source: '메신저',
    sourceIcon: 'message',
    primary: '원문 확인하기',
    secondary: '확인완료',
  },
];

const WORK_TABS = [
  { value: 'my', label: '내 업무' },
  { value: 'sent', label: '보낸 업무' },
  { value: 'done', label: '완료 업무' },
];

const TASK_FILTERS = [
  { value: 'all', label: '전체 (00)' },
  { value: 'request', label: '받은 요청 (0)' },
  { value: 'blocked', label: '막힘 (0)' },
  { value: 'overdue', label: '기한 지남(0)' },
];

const STATUS_OPTIONS = [
  { value: 'progress', label: '진행 중', tone: 'accent' },
  { value: 'blocked', label: '막힘', tone: 'danger' },
  { value: 'done', label: '완료', tone: 'positive' },
];

const TASK_ROWS = [
  { id: 't1', title: '8월 정산 자료 정리', badge: '완료 확인', badgeTone: 'neutral', requester: '홍길동', due: '09-10', dueExtra: '+1', status: 'progress', starred: true, actions: 'confirm' },
  { id: 't2', title: '8월 정산 자료 정리', badge: '담당 변경', badgeTone: 'neutral', requester: '홍길동', due: '09-10', status: 'progress', unread: true, actions: 'accept' },
  { id: 't3', title: '예외 승인 건', badge: '결정 요청', badgeTone: 'danger', requester: '홍길동', due: '09-10', status: 'progress', actions: 'accept' },
  { id: 't4', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
  { id: 't5', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
  { id: 't6', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
  { id: 't7', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
  { id: 't8', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
  { id: 't9', title: 'Task name here', requester: '-', due: '09-10', status: 'progress' },
];

const CALENDAR_RANGES = [
  { value: 'today', label: '오늘' },
  { value: 'week', label: '주' },
  { value: 'month', label: '월' },
];

const AGENDA_ITEMS = [
  { id: 'a1', badge: '회의', tone: 'positive', time: '14:00 - 15:00', title: '거래처 미팅' },
  { id: 'a2', badge: '업무', tone: 'accent', time: '14:00 - 15:00', title: '8월 정산 마감', sub: '2026.10.10 까지' },
  { id: 'a3', badge: '업무', tone: 'accent', time: '14:00 - 15:00', title: '8월 정산 마감', sub: '2026.10.10 까지' },
];

const WORK_DAY = { date: '9월 7일 월요일', hours: '09:00 - 18:00' };

const INBOX_UNREAD_COUNT = 5;


/* ---- 보낸 업무 ---- */
const SENT_TASK_FILTERS = [
  { value: 'all', label: '전체 (00)' },
  { value: 'not-started', label: '시작 안함 (0)' },
  { value: 'overdue', label: '기한 지남 (0)' },
];

const SENT_ROWS = [
  { id: 's1', title: '8월 정산 자료 정리', assignee: '홍길동', due: '09-10', dueExtra: '+1', status: 'progress' },
  { id: 's2', title: '8월 정산 자료 정리', assignee: '박민수', due: '09-27', status: 'not-started' },
  { id: 's3', title: '8월 정산 자료 정리', assignee: '박민수', due: '09-27', status: 'not-started' },
];

const SENT_STATUS_LABEL = { progress: '진행 중', 'not-started': '시작 전' };

/* ---- 완료 업무 ---- */
const DONE_TASK_FILTERS = [
  { value: 'all', label: '전체 (00)' },
  { value: 'await', label: '확인 대기 (0)' },
];

const DONE_GROUPS = [
  { id: 'g1', label: '내 업무', rows: [
    { id: 'd1', title: '8월 정산 자료 정리', counterpart: '-', closedAt: '09-10', status: 'done' },
    { id: 'd2', title: '8월 정산 자료 정리', counterpart: '박민수', closedAt: '09-27', status: 'done' },
    { id: 'd3', title: '8월 정산 자료 정리', counterpart: '박민수', closedAt: '09-27', status: 'done' },
  ] },
  { id: 'g2', label: '보낸 업무', rows: [
    { id: 'd4', title: '8월 정산 자료 정리', counterpart: '박민수', closedAt: '09-27', status: 'cancelled' },
  ] },
];

const DONE_STATUS = { done: { label: '완료', tone: 'info' }, cancelled: { label: '취소', tone: 'danger' } };

/* ---- 주간 캘린더 ---- */
const WEEK_LABEL = '2026년 9월 2주 차';
const WEEKDAY_HEADS = ['월', '화', '수', '목', '금', '토', '일'];
const WEEK_DAYS = [
  { date: 7, dot: false }, { date: 8, dot: false }, { date: 9, dot: false },
  { date: 10, dot: true, selected: true }, { date: 11, dot: false }, { date: 12, dot: false }, { date: 13, dot: false },
];
const WEEK_SECTIONS = [
  { id: 'w1', label: '9월 7일 월요일', count: 1, items: [] },
  { id: 'w2', label: '9월 8일 화요일', count: 2, items: [] },
  { id: 'w3', label: '9월 8일 수요일', count: 0, items: [] },
  { id: 'w4', label: '9월 10일 목요일', count: 3, open: true, items: AGENDA_ITEMS },
  { id: 'w5', label: '9월 11일 금요일', count: 2, items: [] },
];

/* ---- 월간 캘린더 ---- */
const MONTH_LABEL = '2026년 9월';
const MONTH_WEEKS = [
  [{ date: 1, dot: true }, { date: 2, dot: true }, { date: 3, dot: true }, { date: 4 }, { date: 5 }, { date: 6 }, null],
  [{ date: 7 }, { date: 8 }, { date: 9 }, { date: 10, dot: true, selected: true }, { date: 11 }, { date: 12 }, { date: 13 }],
  [{ date: 14 }, { date: 15 }, { date: 16 }, { date: 17 }, { date: 18 }, { date: 19 }, { date: 20 }],
  [{ date: 21 }, { date: 22 }, { date: 23 }, { date: 24, muted: true }, { date: 25, muted: true }, { date: 26, muted: true }, { date: 27 }],
  [{ date: 28 }, { date: 29 }, { date: 30 }, null, null, null, null],
];


/* ---- 업무 만들기 모달 (MOD-101) ---- */
const MODAL_SOURCE = { icon: 'mail', label: '계약서 검토 부탁드립니다' };

const TASK_DRAFT = {
  name: '계약서 검토',
  due: '2026-09-08',
  body: '데모에서 업무·회의·자료가 채팅에서 안전하게 이어지는 경험을 검증한다.\n200자 입력할 수 있습니다. 최대 높이를 지정하고 그 이상 길어지면 스크롤이 적용되게 해주세요.',
  bodyLimit: 200,
};

const SUGGESTED_PEOPLE = [
  { id: 'p1', name: '박민철', role: '법무담당', avatar: './assets/avatar-person.png' },
  { id: 'p2', name: '김길동', role: '계약 검토 이력' },
  { id: 'p3', name: '박혜진', role: '팀장' },
];

const PEOPLE_OPTIONS = ['박민철', '박OO', '박OO', '송OO', '이OO', '이OO', '정OO'];

const SAMPLE_FILES = [
  { id: 'f1', icon: 'document', name: 'Document File.html', size: '1.2 MB' },
  { id: 'f2', icon: 'image', name: 'Image File.jpg', size: '1.2 MB' },
  { id: 'f3', icon: 'link', name: 'https://www.medisolveai.com/' },
];

const AGENT_MESSAGE = '홍길동님  업무 시작 전\n일정을 정리해드릴까요?';

Object.assign(window, {
  INBOX_FILTERS, INBOX_ITEMS, WORK_TABS, TASK_FILTERS,
  STATUS_OPTIONS, TASK_ROWS, INBOX_UNREAD_COUNT, CALENDAR_RANGES, AGENDA_ITEMS, WORK_DAY, AGENT_MESSAGE,
  SENT_TASK_FILTERS, SENT_ROWS, SENT_STATUS_LABEL, DONE_TASK_FILTERS, DONE_GROUPS, DONE_STATUS,
  WEEK_LABEL, WEEKDAY_HEADS, WEEK_DAYS, WEEK_SECTIONS, MONTH_LABEL, MONTH_WEEKS,
  MODAL_SOURCE, TASK_DRAFT, SUGGESTED_PEOPLE, PEOPLE_OPTIONS, SAMPLE_FILES,
});
