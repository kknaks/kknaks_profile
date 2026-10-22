'use client';

import { Stage } from '@/components/stage/stage';
import { TabletView } from '@/components/tablet/tablet-view';
import { useSkinReport } from '@/data/sources/use-skin-report';
import { useTabletSync } from '@/sync/use-tablet-sync';

export default function TabletPage() {
  const report = useSkinReport();
  const screenLinked = useTabletSync();
  return (
    <Stage width={1180} height={820} background="#ffffff">
      <TabletView report={report} screenLinked={screenLinked} />
    </Stage>
  );
}
