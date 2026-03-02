import { Link } from "react-router";

export default function Home() {
  const hasVoice = !!import.meta.env.VITE_ELEVENLABS_AGENT_ID;

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-stone-50 px-4">
      <h1 className="mb-2 text-4xl font-bold text-stone-800">
        Hotel Concierge
      </h1>
      <p className="mb-8 text-stone-500">How can we help you today?</p>
      <div className="flex gap-4">
        <Link
          to="/chat"
          className="rounded-lg bg-stone-800 px-6 py-3 text-white transition hover:bg-stone-700"
        >
          Start Chat
        </Link>
        {hasVoice ? (
          <Link
            to="/voice"
            className="rounded-lg border border-stone-300 px-6 py-3 text-stone-700 transition hover:bg-stone-100"
          >
            Voice
          </Link>
        ) : (
          <span
            title="Set VITE_ELEVENLABS_AGENT_ID to enable voice"
            className="cursor-not-allowed rounded-lg border border-stone-200 px-6 py-3 text-stone-400"
          >
            Voice (not configured)
          </span>
        )}
      </div>
    </div>
  );
}
