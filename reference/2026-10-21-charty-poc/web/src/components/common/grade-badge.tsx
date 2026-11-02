'use client';

import { Badge, cn } from '@medisolve-ai/medikit';
import { GRADE_META } from '@/domain/grade';
import type { Grade } from '@/domain/skin-report';

/** 등급 배지 — 색만으로 전하지 않고 항상 글자를 같이 쓴다(SPEC §2-1) */
export function GradeBadge({ grade, size = 'md', className }: { grade: Grade; size?: 'sm' | 'md' | 'lg' | 'screen'; className?: string }) {
  const meta = GRADE_META[grade];
  return (
    <Badge
      variant={meta.badge.variant}
      size={size === 'sm' ? 'sm' : 'md'}
      data-grade={grade}
      className={cn(meta.badge.className, size === 'lg' && 'h-8 px-3 text-typo-heading-md-600',
        size === 'screen' && 'h-8 px-3 text-typo-heading-md-500', className)}
    >
      {meta.label}
    </Badge>
  );
}
