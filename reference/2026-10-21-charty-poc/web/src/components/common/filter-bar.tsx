'use client';

import { CircleDot, Flame, Palette, Sparkles, Spline, Sun, Waves, type LucideIcon } from 'lucide-react';
import { FILTERS, FILTER_ORDER, type FilterKey } from '@/domain/filters';

const ICONS: Record<FilterKey, LucideIcon> = {
  natural: Sun,
  fineWrinkle: Waves,
  deepWrinkle: Spline,
  pore: CircleDot,
  redness: Flame,
  pigment: Palette,
  porphyrin: Sparkles,
};

interface FilterBarProps {
  value: FilterKey;
  onChange: (f: FilterKey) => void;
  /** screen = 화면 ① 큰 칩 56px · tablet = 차티 칩 문법 */
  size: 'screen' | 'tablet';
}

export function FilterBar({ value, onChange, size }: FilterBarProps) {
  return (
    <div className={size === 'screen' ? 'flex gap-3' : 'flex flex-wrap gap-1.5'} role="radiogroup" aria-label="3D 필터">
      {FILTER_ORDER.map((key) => {
        const Icon = ICONS[key];
        const active = value === key;
        return (
          <button
            key={key}
            type="button"
            role="radio"
            aria-checked={active}
            data-testid={`filter-${key}`}
            data-active={active}
            onClick={() => onChange(key)}
            className={
              size === 'screen'
                ? `flex h-14 items-center gap-2 rounded-full px-5 text-typo-heading-md-600 transition-colors ${
                    active ? 'bg-primary text-ms-white' : 'bg-white/90 text-ms-gray-800 hover:bg-white'
                  }`
                : `flex h-8 items-center gap-1 rounded-full px-3 text-[11px] transition-colors ${
                    active ? 'bg-primary text-white' : 'bg-ms-gray-200 text-ms-gray-700 hover:bg-ms-gray-300'
                  }`
            }
          >
            <Icon className={size === 'screen' ? 'h-5 w-5' : 'h-3.5 w-3.5'} />
            {FILTERS[key].label}
          </button>
        );
      })}
    </div>
  );
}
