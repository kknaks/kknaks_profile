export const SUPPORTED_LANGS = ["ko", "en"] as const;
export type Lang = (typeof SUPPORTED_LANGS)[number];

export function isLang(value: string): value is Lang {
  return (SUPPORTED_LANGS as readonly string[]).includes(value);
}

export const DEFAULT_LANG: Lang = "ko";
