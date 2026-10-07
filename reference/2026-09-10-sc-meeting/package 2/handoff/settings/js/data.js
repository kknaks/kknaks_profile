/* 「설정」 초기 데이터 — 연동 대상·알림 항목. 실제로는 서버에서 읽어온다.
   메일·슬랙 연동은 사용자 한 번 연결로 실시간 수집한다(수집 주기 없음). 사람·워크스페이스·주소는 전부 가상이다.
   status: 'live' 실시간 · 'backfill' 과거 채우는 중 · 'broken' 연결 끊김(토큰 만료·권한 취소) */

/* 메일 — Gmail 계정 여러 개. 처음 연결 때 받은편지함 전체를 가져온다 */
const MAIL_ACCOUNTS = [
  { id: 'm1', addr: 'haram@company.example', count: '1,284', status: 'live', synced: '10-06 09:10' },
  { id: 'm2', addr: 'haram.lab@company.example', count: '312', status: 'live', synced: '10-06 09:08' },
];
const MAIL_BACKFILL = { id: 'm3', addr: 'pilot-team@company.example', count: '2,407', status: 'backfill', synced: '10-06 09:12' };

/* 슬랙 — 사용자 토큰으로 워크스페이스 하나를 연결하고, 볼 방을 고른다 */
const SLACK_WORKSPACE = { name: '노을웍스', domain: 'noeulworks.slack.com' };

/* 방 종류: channel(공개) · private(비공개 채널) · dm · group(그룹 DM — 참여자 실명을 「, 」로) */
const SLACK_ROOMS = [
  { id: 'C01', type: 'channel', name: '#pilot-launch', members: 14, count: '4,902', status: 'live' },
  { id: 'C02', type: 'private', name: '#pilot-ops', members: 6, count: '860', status: 'live' },
  { id: 'D01', type: 'dm', name: '오지훈', members: 2, count: '1,118', status: 'live' },
  { id: 'G01', type: 'group', name: '문다은, 배성민', members: 3, count: '377', status: 'live' },
];

/* 방 고르기 창 후보 — 내가 볼 수 있는 방 전부. 봇 DM 도 따로 묶지 않고 섞여 나온다 */
const SLACK_CANDIDATES = [
  { id: 'C01', type: 'channel', name: '#pilot-launch', members: 14 },
  { id: 'C03', type: 'channel', name: '#general', members: 52 },
  { id: 'C04', type: 'channel', name: '#design-review', members: 11 },
  { id: 'C05', type: 'channel', name: '#field-support', members: 9 },
  { id: 'C02', type: 'private', name: '#pilot-ops', members: 6 },
  { id: 'C06', type: 'private', name: '#leads', members: 4 },
  { id: 'D01', type: 'dm', name: '오지훈', members: 2 },
  { id: 'D02', type: 'dm', name: '한서윤', members: 2 },
  { id: 'D03', type: 'dm', name: '질문 도우미', members: 2, bot: true },
  { id: 'D04', type: 'dm', name: '문다은', members: 2 },
  { id: 'D05', type: 'dm', name: '배포 알리미', members: 2, bot: true },
  { id: 'G01', type: 'group', name: '문다은, 배성민', members: 3 },
  { id: 'G02', type: 'group', name: '한서윤, 오지훈, 서지안', members: 4 },
  { id: 'G03', type: 'group', name: '배성민, 오지훈', members: 3 },
];

/* 프로필 — 이름 · 소속 · 직책 · 직무는 조직 명부 값(읽기 전용). 가상 인물 */
const MY_PROFILE = { name: '유하람', unit: '노을웍스 · 기획팀', position: '매니저', duty: '서비스 기획', avatar: './assets/avatar-person.png' };

/* 카카오톡 — Mac 전용. Strong Hajin 데스크톱 앱(Rust)이 백그라운드로 이 Mac 카톡 로컬 DB 를 읽어 올린다.
   계정 = 지금 카카오톡에 로그인한 계정(고르는 목록 없음). 고른 1:1 · 단체방만 수집, 오픈채팅방은 목록에 나오지 않는다.
   type: 'direct'(1:1 — 상대 이름) · 'group'(단체방 — 이름 없으면 참여자 이름을 「, 」로) */
const KAKAO_STATUS = { device: 'MacBook Pro', appVersion: '1.2.0', account: '유하람', kakaoId: 'haram.k@kakao.example', lastSeen: '10-06 08:10', lastSync: '10-06 09:14' };

const KAKAO_ROOMS = [
  { id: 'k1', type: 'direct', name: '박지윤', members: 2, count: '2,318', status: 'live' },
  { id: 'k2', type: 'group', name: '김태오, 이수아, 정민재', members: 4, count: '1,077', status: 'live' },
  { id: 'k3', type: 'group', name: '현장팀 공지방', members: 12, count: '3,441', status: 'live' },
];

const KAKAO_CANDIDATES = [
  { id: 'k1', type: 'direct', name: '박지윤', members: 2 },
  { id: 'k4', type: 'direct', name: '오지훈', members: 2 },
  { id: 'k5', type: 'direct', name: '한서윤', members: 2 },
  { id: 'k6', type: 'direct', name: '문다은', members: 2 },
  { id: 'k3', type: 'group', name: '현장팀 공지방', members: 12 },
  { id: 'k2', type: 'group', name: '김태오, 이수아, 정민재', members: 4 },
  { id: 'k7', type: 'group', name: '파일럿 2차 TF', members: 7 },
  { id: 'k8', type: 'group', name: '배성민, 오지훈, 서지안, 유하람', members: 4 },
];

const NOTIFY_GROUPS = [
  {
    id: 'work', title: '업무',
    items: [
      { id: 'assign', label: '업무가 배정됐을 때', desc: '나에게 새 업무가 생기면 알립니다', on: true },
      { id: 'due', label: '기한 하루 전', desc: '마감 24시간 전에 한 번', on: true },
      { id: 'comment', label: '내 업무에 댓글', desc: '', on: false },
    ],
  },
  {
    id: 'meeting', title: '회의 · 연동',
    items: [
      { id: 'minutes', label: '회의록 정리 완료', desc: '에이전트가 정리를 마치면', on: true },
      { id: 'sync-fail', label: '연동 수집 실패', desc: '메일·슬랙·카카오 수집이 실패하면', on: true },
      { id: 'digest', label: '일일 요약', desc: '매일 오전 9시', on: false },
    ],
  },
];

const NOTIFY_CHANNELS = [
  { id: 'app', label: '앱 알림', desc: '수신함과 좌측 알림에 표시', on: true },
  { id: 'mail', label: '메일', desc: 'haram@thesc.co.kr', on: true },
  { id: 'slack', label: '슬랙 DM', desc: '@haram', on: false },
];

Object.assign(window, { MY_PROFILE, MAIL_ACCOUNTS, MAIL_BACKFILL, SLACK_WORKSPACE, SLACK_ROOMS, SLACK_CANDIDATES, KAKAO_STATUS, KAKAO_ROOMS, KAKAO_CANDIDATES, NOTIFY_GROUPS, NOTIFY_CHANNELS });
