/* 「알림」 목데이터 — 실제로는 서버의 알림 목록을 읽는다. 사람·회사·주소·방은 전부 가상이다.
   theme: 'work' 업무 · 'message' 메시지 · 'meeting' 회의 (설정 > 알림 설정의 테마와 같은 셋)
   rel: 받는 사람(나)과 이 사건의 관계 — 같은 사건이라도 관계가 다르면 다른 알림이다
        업무 assignee 담당 · requester 요청자 · assigner 배정자(내가 배정한 담당이 수락·거절) · cc 참조(CC — 댓글만 받는다)
        메일 to 받는 사람 · mail-cc 참조 · mail-other 메일(To/CC 어디에도 내가 없음 — 숨은 참조·메일링) / 슬랙 dm DM · mention 멘션 · channel 채널 / 카톡 kakao-direct 1:1 · kakao-group 단체방
        회의 owner 소유자 · attendee 참석자 · shared 공유받음 / 연동 integration 내 연동
   관계·항목은 DEC-010 사건 × 관계 표를 따른다(2026-10-08)
   day: 'today' 오늘 · 'yesterday' 어제 · 'week' 이번 주 · 'earlier' 이전 — 오늘 = 2026-10-07(수)
   text: 문장 조각. { b } = 누가(굵게) · { q } = 무엇을(‘ ’ 로 감싼 이름) · 문자열 = 나머지
   to: 누르면 가는 자리(시안은 링크 모양만) — 업무 / 메시지함 / 회의
   fail: 실패·끊김 사건(아이콘 칸이 붉다) */

const ALERT_ITEMS = [
  /* 오늘 */
  { id: 'a01', theme: 'work', rel: 'assignee', day: 'today', at: '3분 전', unread: true,
    text: [{ b: '오지훈님' }, '이 ', { q: '견적서 정리' }, ' 업무를 요청했습니다'],
    sub: '기한 10월 9일(금) · 프로젝트 파일럿 2차', to: { href: './MyWork.html', label: '업무' } },
  { id: 'a02', theme: 'message', rel: 'mention', day: 'today', at: '12분 전', unread: true,
    text: [{ b: '한서윤님' }, '이 ', { q: '#pilot-launch' }, ' 에서 나를 멘션했습니다'],
    sub: '「@유하람 배포 체크리스트 마지막 항목 확인 부탁드려요」', to: { href: './Inbox.html', label: '메시지함 · 슬랙' } },
  { id: 'a03', theme: 'meeting', rel: 'attendee', day: 'today', at: '35분 전', unread: true,
    text: [{ b: '문다은님' }, '이 ', { q: '파일럿 2차 킥오프' }, ' 회의에 초대했습니다'],
    sub: '10월 9일(금) 14:00 – 15:00 · 3층 회의실', to: { href: './MeetingWorkspace.html', label: '회의' } },
  { id: 'a04', theme: 'message', rel: 'to', day: 'today', at: '1시간 전', unread: true,
    text: [{ b: '서지안님' }, '이 메일 ', { q: '현장 설치 일정표 공유' }, ' 을 보냈습니다'],
    sub: '첨부 2개 · haram@company.example 로 받음', to: { href: './Inbox.html', label: '메시지함 · 메일' } },
  { id: 'a05', theme: 'work', rel: 'requester', day: 'today', at: '2시간 전', unread: true,
    text: [{ b: '배성민님' }, '이 내가 요청한 ', { q: '고객 응대 매뉴얼 개정' }, ' 업무를 수락했습니다'],
    to: { href: './MyWork.html', label: '업무' } },
  { id: 'a06', theme: 'meeting', rel: 'owner', day: 'today', at: '3시간 전', unread: false,
    text: [{ q: '주간 기획 회의' }, ' 회의록 정리가 끝났습니다'],
    sub: '안건 4 · 할 일 6 · 결정 2', to: { href: './MeetingWorkspace.html', label: '회의' } },
  { id: 'a07', theme: 'work', rel: 'requester', day: 'today', at: '4시간 전', unread: false,
    text: [{ b: '김태오님' }, '이 내가 요청한 ', { q: '3분기 정산 보고' }, ' 업무 완료를 보고했습니다'],
    sub: '확인해 주세요 — 승인하거나 보완을 요청한다', to: { href: './MyWork.html', label: '업무' } },
  { id: 'a21', theme: 'message', rel: 'mail-other', day: 'today', at: '5시간 전', unread: true,
    text: [{ b: '노을웍스 인사팀' }, '이 메일 ', { q: '10월 사내 교육 일정 안내' }, ' 을 보냈습니다'],
    sub: '받는 사람 all@company.example · 나는 받는 사람·참조에 없음', to: { href: './Inbox.html', label: '메시지함 · 메일' } },

  /* 어제 */
  { id: 'a08', theme: 'message', rel: 'dm', day: 'yesterday', at: '어제 18:20', unread: true,
    text: [{ b: '오지훈님' }, '이 슬랙 DM 을 보냈습니다'],
    sub: '「내일 오전에 잠깐 통화 가능할까요? 견적 범위 같이 보고 싶어요」', to: { href: './Inbox.html', label: '메시지함 · 슬랙' } },
  { id: 'a09', theme: 'work', rel: 'assignee', day: 'yesterday', at: '어제 16:05', unread: false,
    text: [{ b: '한서윤님' }, '이 ', { q: '현장 점검표 작성' }, ' 업무의 기한을 바꿨습니다'],
    sub: '10월 8일(목) → 10월 9일(금)', to: { href: './MyWork.html', label: '업무' } },
  { id: 'a10', theme: 'message', rel: 'mail-cc', day: 'yesterday', at: '어제 11:42', unread: false,
    text: [{ b: '박지윤님' }, '이 메일 ', { q: '협력사 계약 갱신 안내' }, ' 을 보냈습니다'],
    sub: '받는 사람 서지안 외 1명 · 나는 참조', to: { href: './Inbox.html', label: '메시지함 · 메일' } },
  { id: 'a11', theme: 'meeting', rel: 'attendee', day: 'yesterday', at: '어제 10:15', unread: false,
    text: [{ b: '문다은님' }, '이 ', { q: '디자인 리뷰' }, ' 회의 시간을 바꿨습니다'],
    sub: '10월 8일(목) 11:00 → 15:00', to: { href: './MeetingWorkspace.html', label: '회의' } },
  { id: 'a12', theme: 'work', rel: 'assignee', day: 'yesterday', at: '어제 09:30', unread: false,
    text: [{ q: '부스 도면 확정' }, ' 업무가 끝나 ', { q: '부스 시공 발주' }, ' 업무를 시작할 수 있습니다'],
    sub: '선행 업무 완료 · 김태오님', to: { href: './MyWork.html', label: '업무' } },
  { id: 'a22', theme: 'work', rel: 'assigner', day: 'yesterday', at: '어제 08:50', unread: true,
    text: [{ b: '문다은님' }, '이 내가 배정한 ', { q: '현장 사진 정리' }, ' 업무의 담당을 수락했습니다'],
    to: { href: './MyWork.html', label: '업무' } },

  /* 이번 주 */
  { id: 'a13', theme: 'work', rel: 'requester', day: 'week', at: '10월 5일(월) 17:30', unread: false,
    text: [{ b: '배성민님' }, '이 ', { q: '행사 부스 견적 비교' }, ' 업무 완료를 보고했습니다'],
    sub: '확인해 주세요 — 승인하거나 보완을 요청한다', to: { href: './MyWork.html', label: '업무' } },
  { id: 'a14', theme: 'message', rel: 'kakao-direct', day: 'week', at: '10월 5일(월) 15:02', unread: false,
    text: [{ b: '박지윤님' }, '이 카카오톡 메시지를 보냈습니다'],
    sub: '「사진 5장」', to: { href: './Inbox.html', label: '메시지함 · 카톡' } },
  { id: 'a15', theme: 'message', rel: 'integration', day: 'week', at: '10월 5일(월) 08:44', unread: false, fail: true,
    text: ['메일 연동 ', { q: 'haram.lab@company.example' }, ' 의 연결이 끊겼습니다'],
    sub: '새 메일을 받지 못한다 — 설정에서 다시 연결', to: { href: './Settings.html', label: '설정 · 메일 연동' } },
  { id: 'a16', theme: 'meeting', rel: 'owner', day: 'week', at: '10월 5일(월) 08:10', unread: false, fail: true,
    text: [{ q: '파일럿 회고' }, ' 회의록을 만들지 못했습니다'],
    sub: '녹음 파일을 읽지 못했다 — 회의에서 다시 정리', to: { href: './MeetingWorkspace.html', label: '회의' } },

  /* 이전 */
  { id: 'a17', theme: 'work', rel: 'assignee', day: 'earlier', at: '9월 30일(수)', unread: false,
    text: [{ b: '서지안님' }, '이 ', { q: '설치 매뉴얼 초안' }, ' 업무를 나에게 넘겼습니다'],
    to: { href: './MyWork.html', label: '업무' } },
  { id: 'a18', theme: 'message', rel: 'channel', day: 'earlier', at: '9월 29일(화)', unread: false,
    text: [{ q: '#design-review' }, ' 에 새 메시지가 4건 왔습니다'],
    sub: '문다은 · 배성민 외 1명', to: { href: './Inbox.html', label: '메시지함 · 슬랙' } },
  { id: 'a19', theme: 'meeting', rel: 'shared', day: 'earlier', at: '9월 28일(월)', unread: false,
    text: [{ b: '김태오님' }, '이 ', { q: '협력사 미팅' }, ' 회의를 공유했습니다'],
    to: { href: './MeetingWorkspace.html', label: '회의' } },
  { id: 'a20', theme: 'work', rel: 'assignee', day: 'earlier', at: '9월 26일(토)', unread: false,
    text: [{ b: '오지훈님' }, '이 ', { q: '견적서 v1' }, ' 에 보완을 요청했습니다'],
    sub: '「단가 근거 표를 붙여 주세요」', to: { href: './MyWork.html', label: '업무' } },
];

Object.assign(window, { ALERT_ITEMS });
