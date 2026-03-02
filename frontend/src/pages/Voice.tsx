import { Link } from "react-router";

const agentId = import.meta.env.VITE_ELEVENLABS_AGENT_ID;

export default function Voice() {
  return (
    <div className="flex min-h-screen flex-col bg-stone-50">
      <header className="flex items-center justify-between border-b border-stone-200 px-4 py-3">
        <Link to="/" className="text-stone-500 hover:text-stone-800">
          &larr; Back
        </Link>
        <h1 className="text-lg font-semibold text-stone-800">Voice Concierge</h1>
        <div className="w-12" />
      </header>
      <div className="flex flex-1 flex-col items-center justify-center">
        {agentId ? (
          <elevenlabs-convai agent-id={agentId}></elevenlabs-convai>
        ) : (
          <p className="text-stone-400">
            Voice not configured — set VITE_ELEVENLABS_AGENT_ID
          </p>
        )}
      </div>
    </div>
  );
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "elevenlabs-convai": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & { "agent-id": string },
        HTMLElement
      >;
    }
  }
}
