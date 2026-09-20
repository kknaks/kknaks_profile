/* 「캘린더」 목데이터 — 업무 화면과 공용인 ../../shared/js/work-data.js 를 그대로 쓴다.
   CAL_TASKS    업무   : 완료된 업무는 캘린더에서 다루지 않는다.
   CAL_SCHEDULE 스케쥴 : 회의 + 업무의 시간 배정. */

const CAL_MONTH = window.WORK_MONTH;
const CAL_TASKS = (window.WORK_TASKS || []).filter((t) => t.group !== 'done');
const CAL_SCHEDULE = (window.WORK_SCHEDULE || []).slice();

const CAL_TABS = [
  { value: 'all', label: '전체' },
  { value: 'meeting', label: '회의' },
  { value: 'task', label: '업무' },
];

Object.assign(window, { CAL_MONTH, CAL_TASKS, CAL_SCHEDULE, CAL_TABS });
