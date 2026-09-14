/* 회의 목록 (SCR-105) 화면 데이터. 문구는 레거시 labels.ts `meetingScreen` 원문 그대로. */

/* 상태 여섯 (SPEC-004 §5.1) — 「완료」가 아니라 「종료」다 */
const MEETING_STATUS = {
  scheduled: { label: '예정', tone: 'neutral' },
  in_progress: { label: '진행 중', tone: 'accent' },
  summarizing: { label: '정리 중', tone: 'accent' },
  done: { label: '종료', tone: 'positive' },
  failed: { label: '실패', tone: 'danger' },
  cancelled: { label: '취소', tone: 'neutral' },
};

const MEETING_COPY = {
  title: '회의 목록',
  start: '회의 시작',
  book: '회의 예약',
  upcoming: '예정',
  past: '지난',
  more: '더 보기',
  remove: '삭제',
  listEmpty: '아직 회의가 없습니다. 회의를 예약하거나 바로 시작하면 여기에 쌓입니다.',
  listError: '불러오지 못했습니다. 다시 시도해 주세요.',
  noTitle: '제목 없는 회의',
  sharedTag: '열람',
  concluded: '결론 남',
  notConcluded: '결론 안 남',
  todos: '다음 할 일',
  requested: '요청됨',
  share: '공유',
  export: '내보내기',
  attendCount: (n) => `참석 ${n}명`,
  panelEmpty: '왼쪽에서 회의를 고르면 회의록이 열립니다.',
  openNote: '회의록 열기',
  /* 삭제 두 갈래 (T08) — 갈래를 두지 않는다. 회의를 취소하는 자리 하나다 */
  deleteTitle: '회의를 취소할까요?',
  deleteBody: '회의 삭제 시 회의 자료가 삭제되고 회의도 취소됩니다.',
  deleteMeeting: '회의 취소',
};

/* viewer_relation: 'attendee' | 'shared' — 'shared' 면 「열람」 꼬리표가 상태 옆에 선다 */
const MEETING_UPCOMING = [
  { id: 'm1', when: '09-12 14:00', title: '9월 정산 자료 취합 킥오프', place: '3F 회의실 A', attendees: 6, status: 'scheduled', relation: 'attendee' },
  { id: 'm2', when: '09-12 16:30', title: '계약서 검토 회의', place: '온라인', attendees: 4, status: 'scheduled', relation: 'attendee' },
  { id: 'm3', when: '09-15 10:00', title: null, place: null, attendees: 3, status: 'scheduled', relation: 'shared' },
  { id: 'm8', when: '09-12 13:00', title: '9월 정산 중간 점검', place: '3F 회의실 A', attendees: 5, status: 'in_progress', relation: 'attendee' },
];

const MEETING_PAST = [
  { id: 'm4', when: '09-11 11:00', title: '주간 업무 공유', place: '3F 회의실 B', attendees: 8, status: 'done', relation: 'attendee' },
  { id: 'm5', when: '09-10 15:00', title: '8월 매출 리뷰', place: '온라인', attendees: 5, status: 'summarizing', relation: 'attendee' },
  { id: 'm6', when: '09-09 09:30', title: '거래처 미팅', place: '고객사', attendees: 4, status: 'failed', relation: 'shared' },
  { id: 'm7', when: '09-08 13:00', title: '추석 연휴 근무 조율', place: '3F 회의실 A', attendees: 9, status: 'cancelled', relation: 'attendee' },
];

/* 회의 한 건의 회의록. 예정 회의는 안건만 있고 줄은 비어 있다 (E26).
   안건 출처(source)는 상태와 무관하게 늘 낸다 (E21). */
const MEETING_AGENDA_SOURCE = {
  manual: '직접 입력',
  set: '세트',
  carried: '지난 회의에서 넘어옴',
  derived: '다른 회의에서 파생',
  ai: 'AI 정리',
};

const MEETING_RECORDS = {
  m1: { range: '09-12 14:00~15:00', agendas: [
    { id: 'a1', title: '9월 정산 범위 확정', source: 'manual' },
    { id: 'a2', title: '취합 담당과 기한', source: 'carried' },
  ] },
  m2: { range: '09-12 16:30~17:30', agendas: [
    { id: 'a1', title: '계약 조항 검토', source: 'manual' },
  ] },
  m3: { range: '09-15 10:00~11:00', agendas: [] },
  m4: { range: '09-11 11:00~12:00', agendas: [
    { id: 'a1', title: '지난주 마감 결과', source: 'set', concluded: true,
      lines: ['8월 정산 마감은 09-10 에 끝났다.', '지연 건 한 건은 09-12 까지 이월한다.'],
      todos: [{ id: 't1', title: '이월 건 처리 계획 공유', due: '09-12' }] },
    { id: 'a2', title: '이번 주 우선순위', source: 'manual', concluded: false,
      lines: ['매출 자료 취합이 먼저다.', '나머지는 다음 회의에서 다시 본다.'],
      todos: [{ id: 't2', title: '8월 매출 자료 취합', due: '09-12', linked: true }] },
  ] },
  m5: { range: '09-10 15:00~16:00', agendas: [
    { id: 'a1', title: '8월 매출 리뷰', source: 'ai', concluded: true, lines: ['정리 중입니다.'], todos: [] },
  ] },
  m6: { range: '09-09 09:30~10:30', agendas: [
    { id: 'a1', title: '거래처 요청 사항', source: 'manual', concluded: false, lines: [], todos: [] },
  ] },
  m8: { range: '09-12 13:00~14:00', agendas: [
    { id: 'a1', title: '정산 진행 상황', source: 'carried', concluded: false, lines: ['취합은 절반 끝났다.'], todos: [] },
  ] },
  m7: { range: '09-08 13:00~14:00', agendas: [
    { id: 'a1', title: '연휴 근무 조율', source: 'manual', concluded: false, lines: [], todos: [] },
  ] },
};

/* 목록은 한 줄기다 — 탭이 상태로 가른다 (업무 탭의 내 업무/보낸 업무/완료 업무와 같은 구조) */
const MEETING_TABS = [
  { value: 'upcoming', label: '예정' },
  { value: 'live', label: '진행 중' },
  { value: 'done', label: '완료' },
];

/* 상태 여섯을 탭 셋으로 접는다. 정리 중은 아직 끝난 것이 아니라 진행 중에 선다 */
const MEETING_TAB_OF = {
  scheduled: 'upcoming',
  in_progress: 'live',
  summarizing: 'live',
  done: 'done',
  failed: 'done',
  cancelled: 'done',
};

const MEETING_ROWS = [].concat(MEETING_UPCOMING, MEETING_PAST);

Object.assign(window, { MEETING_STATUS, MEETING_COPY, MEETING_UPCOMING, MEETING_PAST, MEETING_ROWS, MEETING_TABS, MEETING_TAB_OF, MEETING_RECORDS, MEETING_AGENDA_SOURCE });
