'use client';

import { Button, Card } from '@medisolve-ai/medikit';
import { useState } from 'react';
import { FACE_ANCHORS } from '@/data/face-anchors';
import { AREAS, AREA_ORDER, type AreaKey } from '@/domain/areas';
import { anchorStore, setEditSelected, useAnchorPoints } from './anchor-store';
import { anchorFileSource } from './anchors';
import { useAnchorEdit } from './use-anchor-edit';

/** 개발용 앵커 찍기 도구(SPEC §3-2) — `/screen?anchors=edit`, 프로덕션 빌드에는 들어가지 않는다 */
export default function AnchorEditor() {
  const on = useAnchorEdit();
  const points = useAnchorPoints();
  const [sel, setSel] = useState<AreaKey | null>(null);
  const [copied, setCopied] = useState(false);
  if (!on) return null;
  const pick = (k: AreaKey) => {
    setEditSelected(k);
    setSel(k);
  };
  const copy = async () => {
    await navigator.clipboard?.writeText(anchorFileSource(FACE_ANCHORS.meshBytes, points)).catch(() => undefined);
    setCopied(true);
  };
  return (
    <Card padding="md" className="absolute right-6 top-20 z-40 w-[400px] gap-3 shadow-lg" data-testid="anchor-editor">
      <h2 className="text-typo-title-sm-600 text-ms-black">앵커 찍기 도구</h2>
      <p className="text-typo-heading-md-400 text-ms-gray-700">카드를 고르고 얼굴을 클릭하세요(드래그는 회전)</p>
      <div className="grid grid-cols-2 gap-1.5" role="radiogroup">
        {AREA_ORDER.map((k) => {
          const a = points.find((x) => x.key === k);
          return (
            <label key={k} className={`flex cursor-pointer items-center gap-2 rounded-lg border px-2 py-1.5 ${sel === k ? 'border-primary bg-primary-100' : 'border-ms-gray-300'}`}>
              <input type="radio" name="anchor" checked={sel === k} onChange={() => pick(k)} data-testid={`anchor-pick-${k}`} />
              <span className="text-typo-heading-md-500 text-ms-black">{AREAS[k].label}</span>
              <span className="ml-auto font-mono text-[11px] text-ms-gray-600">{a ? a.p.map((v) => v.toFixed(3)).join(' ') : '—'}</span>
            </label>
          );
        })}
      </div>
      <div className="flex gap-2">
        <Button size="m" onClick={copy} data-testid="anchor-copy">
          {copied ? '복사됨' : '복사'}
        </Button>
        <Button size="m" variant="outlined" color="gray" onClick={() => anchorStore.reset()} data-testid="anchor-reset">
          초기화
        </Button>
      </div>
    </Card>
  );
}
