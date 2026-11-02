import * as React from 'react';
/**
 * Date entry field: typed `YYYY-MM-DD` plus a DatePicker popover.
 *
 * **Intentional addition.** The source Figma file defines no date-picker and no
 * time input, so this name has no kit counterpart by design. Do not rename.
 */
export interface DateFieldProps {
  /** `YYYY-MM-DD`. */
  value?: string;
  onChange: (value: string) => void;
  /** Control height: sm 32 / md 39 / lg 47 — the kit's three button heights. */
  size?: 'sm' | 'md' | 'lg';
  placeholder?: string;
  /** Paints the danger border. */
  invalid?: boolean;
  /** Dates (`YYYY-MM-DD`) that get an accent dot in the popover. */
  marks?: string[];
  min?: string;
  max?: string;
  ariaLabel?: string;
  style?: React.CSSProperties;
}
export declare const DateField: React.FC<DateFieldProps>;
export default DateField;
