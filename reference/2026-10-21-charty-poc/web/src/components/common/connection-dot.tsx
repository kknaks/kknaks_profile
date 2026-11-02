export function ConnectionDot({ on, label, size = 'md', testId }: { on: boolean; label: string; size?: 'md' | 'sm'; testId?: string }) {
  return (
    <span className="inline-flex items-center gap-2" data-testid={testId} data-on={on}>
      <span className={`rounded-full ${size === 'md' ? 'h-3 w-3' : 'h-2 w-2'} ${on ? 'bg-primary' : 'bg-ms-gray-500'}`} />
      <span className={on ? 'text-ms-gray-800' : 'text-ms-gray-600'}>{label}</span>
    </span>
  );
}
