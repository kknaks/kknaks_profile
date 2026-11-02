'use client';

import { Button } from '@medisolve-ai/medikit';
import Link from 'next/link';

export function StartActions() {
  return (
    <div className="mt-6 flex gap-3">
      <Button
        variant="solid"
        color="blue"
        size="l"
        data-testid="open-screen"
        onClick={() => window.open('/screen', 'charty-screen')}
      >
        큰 화면 열기
      </Button>
      <Button variant="outlined" color="blue" size="l" asChild>
        <Link href="/tablet" data-testid="open-tablet">
          상담사 화면 열기
        </Link>
      </Button>
    </div>
  );
}
