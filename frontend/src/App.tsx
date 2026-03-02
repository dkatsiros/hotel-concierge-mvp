import { Routes, Route } from "react-router";
import Home from "./pages/Home";
import Chat from "./pages/Chat";
import Voice from "./pages/Voice";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/voice" element={<Voice />} />
    </Routes>
  );
}
