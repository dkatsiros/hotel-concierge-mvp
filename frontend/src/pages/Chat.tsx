import { Link } from "react-router";
import ChatWindow from "../components/ChatWindow";
import VoiceAgent from "../components/VoiceAgent";

export default function Chat() {
  return (
    <div className="flex min-h-screen flex-col bg-stone-50">
      <header className="flex items-center justify-between border-b border-stone-200 px-4 py-3">
        <Link to="/" className="text-stone-500 hover:text-stone-800">
          &larr; Back
        </Link>
        <h1 className="text-lg font-semibold text-stone-800">Concierge Chat</h1>
        <div className="w-12" />
      </header>
      <div className="flex flex-1 flex-col">
        <ChatWindow />
        <VoiceAgent />
      </div>
    </div>
  );
}
