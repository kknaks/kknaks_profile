import { StartActions } from '@/components/common/start-actions';

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-ms-gray-100 p-8">
      <div className="w-[520px] rounded-xl border border-ms-gray-300 bg-ms-white p-8">
        <div className="flex items-center gap-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/charty-logo.svg" alt="Charty" width={55} height={22} />
          <h1 className="text-typo-title-md-600">피부 상담 목업</h1>
        </div>
        <ol className="mt-4 list-decimal space-y-1 pl-5 text-typo-body-400 text-ms-gray-800">
          <li>
            처음 한 번 <code className="rounded bg-ms-gray-200 px-1">npm run prepare:assets</code> 로 3D 에셋을 만든다.
          </li>
          <li>[큰 화면 열기] 로 새 창을 띄워 큰 스크린(1920×1080)에 둔다.</li>
          <li>[상담사 화면 열기] 로 태블릿 화면을 띄우고, 거기서 고른 시술·필터가 큰 화면에 따라 바뀐다.</li>
        </ol>
        <StartActions />
      </div>
    </main>
  );
}
