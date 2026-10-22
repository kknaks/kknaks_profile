// 목 상담 텍스트 12줄 — 목업용으로 새로 쓴 대화(실제 상담 기록 아님).
// 체크리스트 초기 체크는 이 텍스트에 차티와 같은 키워드 매칭을 돌려 채운다(SPEC §3-3).

export interface TranscriptLine {
  speaker: 'counselor' | 'customer';
  text: string;
}

export const TRANSCRIPT: TranscriptLine[] = [
  { speaker: 'counselor', text: '안녕하세요, 오늘 피부 분석 결과 같이 보면서 말씀 나눠 볼게요. 요즘 제일 신경 쓰이는 데가 어디세요?' },
  { speaker: 'customer', text: '눈가 주름이 웃을 때마다 보여서 그게 제일 고민이에요. 눈밑도 좀 자글자글하고요.' },
  { speaker: 'counselor', text: '분석에서도 눈밑 잔주름이 조금 보였어요. 이전에 받아 보신 시술이 있으세요?' },
  { speaker: 'customer', text: '예전에 다른 데서 보톡스 한 번 맞아 봤는데, 그때는 괜찮았어요.' },
  { speaker: 'counselor', text: '좋아요. 모공도 넓어진 편으로 나왔는데, 코 옆이랑 볼 쪽 모공은 어떠세요?' },
  { speaker: 'customer', text: '모공도 거슬리긴 해요. 화장하면 더 티가 나서 개선하고 싶어요.' },
  { speaker: 'counselor', text: '혹시 드시는 약이나 알레르기 있으신 건 없으세요?' },
  { speaker: 'customer', text: '따로 복용하는 약은 없고 알레르기도 없어요.' },
  { speaker: 'counselor', text: '생각하시는 예산은 어느 정도 범위세요?' },
  { speaker: 'customer', text: '한 번에 너무 부담되지 않게 이백만 원 안쪽이면 좋겠어요. 그리고 통증이 많이 있나요? 아픈 걸 잘 못 참아서요.' },
  { speaker: 'counselor', text: '마취 크림 바르고 진행해서 통증은 많이 줄일 수 있어요. 리프팅은 따끔한 정도고 다운타임도 거의 없어요.' },
  { speaker: 'customer', text: '그럼 눈가 보톡스랑 리프팅 같이 받고 싶어요. 가격 한번 볼 수 있을까요?' },
];

export const TRANSCRIPT_TEXT = TRANSCRIPT.map((l) => l.text).join('\n');
