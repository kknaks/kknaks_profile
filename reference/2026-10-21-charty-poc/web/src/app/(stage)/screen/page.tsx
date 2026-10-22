'use client';

import { ScreenView } from '@/components/screen/screen-view';
import { Stage } from '@/components/stage/stage';
import { useSkinReport } from '@/data/sources/use-skin-report';
import { useScreenStore } from '@/stores/screen-store';
import { useScreenSync } from '@/sync/use-screen-sync';

export default function ScreenPage() {
  const report = useSkinReport();
  const session = useScreenStore((s) => s.session);
  const { linked, requestFilter } = useScreenSync();
  return (
    <Stage width={1920} height={1080}>
      <ScreenView session={session} report={report} linked={linked} onFilter={requestFilter} />
    </Stage>
  );
}
