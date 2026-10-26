'use client';

import { useEffect, useState } from 'react';
import { anchorEditEnabled } from './anchors';
import { setEditEnabled } from './anchor-store';

/** `/screen?anchors=edit`(개발 서버만) — 첫 렌더 뒤 주소를 읽는다 */
export function useAnchorEdit(): boolean {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const v = anchorEditEnabled(process.env.NODE_ENV, window.location.search);
    setEditEnabled(v);
    // eslint-disable-next-line react-hooks/set-state-in-effect -- 주소는 마운트 뒤에만 읽을 수 있다(SSR)
    setOn(v);
  }, []);
  return on;
}
