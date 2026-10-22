import type { Metadata } from 'next';
import localFont from 'next/font/local';
import './globals.css';

const pretendard = localFont({
  src: './fonts/PretendardVariable.woff2',
  weight: '45 920',
  variable: '--font-pretendard',
  display: 'swap',
});

export const metadata: Metadata = {
  title: '차티 피부 상담 목업',
  description: 'M3D 피부 분석 리포트를 재구성한 피부과 상담 화면 목업',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={pretendard.variable}>
      <body>{children}</body>
    </html>
  );
}
