import * as React from 'react';
/**
 * Month-grid date picker, Monday-first. Controlled component.
 *
 * **Intentional addition.** The source Figma file defines no date-picker, so this
 * name has no kit counterpart by design. Do not rename.
 */
export interface DatePickerProps {
  /** Selected date as `YYYY-MM-DD`. */
  value?: string;
  /** Fires with the picked `YYYY-MM-DD`. */
  onChange: (value: string) => void;
  /** Dates (`YYYY-MM-DD`) that get an accent dot — days with events. */
  marks?: string[];
  /** Earliest selectable date, `YYYY-MM-DD`. */
  min?: string;
  /** Latest selectable date, `YYYY-MM-DD`. */
  max?: string;
  style?: React.CSSProperties;
}
export declare const DatePicker: React.FC<DatePickerProps>;
export default DatePicker;
