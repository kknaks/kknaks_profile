import * as React from 'react';
/**
 * Time entry field: typed `HH:MM` plus a slot list.
 *
 * **Intentional addition.** The source Figma file defines no time input, so this
 * name has no kit counterpart by design. Do not rename.
 */
export interface TimeFieldProps {
  /** `HH:MM`, 24-hour. */
  value?: string;
  onChange: (value: string) => void;
  /** Control height: sm 32 / md 39 / lg 47. */
  size?: 'sm' | 'md' | 'lg';
  /** Slot interval in minutes. Default 30. */
  step?: number;
  /** First slot, minutes from midnight. Default 0. */
  from?: number;
  /** Last slot, minutes from midnight. Default 1410 (23:30). */
  to?: number;
  placeholder?: string;
  invalid?: boolean;
  ariaLabel?: string;
  style?: React.CSSProperties;
}
export declare const TimeField: React.FC<TimeFieldProps>;
export default TimeField;
