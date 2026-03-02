const agentId = import.meta.env.VITE_ELEVENLABS_AGENT_ID;

export default function VoiceAgent() {
  if (!agentId) return null;

  return (
    <div className="border-t border-stone-200 p-4 text-center text-sm text-stone-500">
      <p>Voice agent powered by ElevenLabs</p>
      <elevenlabs-convai agent-id={agentId}></elevenlabs-convai>
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
