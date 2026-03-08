/** Banner shown across all dashboard pages when AEGIS_OPENAI_API_KEY is unset. */
export default function LlmWarningBanner() {
  return (
    <div className="flex items-center gap-3 px-6 py-2.5 bg-amber-50 border-b border-amber-200 text-amber-800 text-sm">
      <svg
        className="w-4 h-4 flex-shrink-0 text-amber-500"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={2}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
        />
      </svg>
      <span>
        <span className="font-semibold">Limited mode</span> — AI-powered root cause analysis and
        table classification are unavailable.{" "}
        <span className="opacity-75">Set AEGIS_OPENAI_API_KEY to enable them.</span>
      </span>
    </div>
  );
}
