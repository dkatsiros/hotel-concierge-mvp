const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000";

export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export function createChatSocket(): WebSocket {
  return new WebSocket(`${WS_URL}/ws/chat`);
}
