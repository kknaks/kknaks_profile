import { TRANSCRIPT } from '@/data/mock/transcript';

/** 상담 텍스트 탭 — 읽기 전용 목 대화 */
export function TranscriptPanel() {
  return (
    <ul className="custom-scrollbar h-full space-y-2 overflow-y-auto px-3 py-3" data-testid="transcript-panel">
      {TRANSCRIPT.map((l, i) => (
        <li key={i} className="flex gap-2 text-[12px] leading-relaxed">
          <span className={`w-12 shrink-0 font-semibold ${l.speaker === 'counselor' ? 'text-primary' : 'text-ms-gray-700'}`}>
            {l.speaker === 'counselor' ? '상담사' : '고객'}
          </span>
          <span className="text-ms-gray-800">{l.text}</span>
        </li>
      ))}
      <li className="pt-2 text-[10px] text-ms-gray-500">목업용으로 새로 쓴 대화예요(실제 상담 기록 아님).</li>
    </ul>
  );
}
