import * as React from 'react';
export interface SocialProps {
  className?: string;
  style?: React.CSSProperties;
  social?: "android" | "apple" | "apple music" | "apple podcasts" | "artstation" | "baidu" | "behance" | "boosty" | "devianart" | "discord" | "dribbble" | "dzen" | "facebook" | "figma" | "github" | "gmail" | "google" | "google meets" | "google play" | "google podcast" | "imo" | "instagram" | "kickstarter" | "line" | "medium" | "messenger" | "microsoft teams" | "notion" | "ok" | "ok (only sign)" | "onlyfans" | "patreon" | "pinterest" | "product hunt" | "quora" | "reddit" | "signal" | "sina weibo" | "slack" | "snapchat" | "social icons" | "soundcloud" | "spotify" | "stack overflow" | "telegram" | "telegram (only sign)" | "threads" | "tiktok" | "tumblr" | "twitch" | "vk" | "vk (only sign)" | "vk music" | "vimeo" | "viber" | "wechat" | "whatsapp" | "x ex twitter" | "xing" | "yandex music" | "yelp" | "youtube" | "youtube shorts" | "youtube music" | "zoom" | "dprofile" | "max" | "bluesky";
  style2?: "black" | "original";
}
export declare const Social: React.FC<SocialProps>;
export default Social;
