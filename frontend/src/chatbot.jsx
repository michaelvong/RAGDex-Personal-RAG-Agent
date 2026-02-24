import { useState, useRef, useEffect } from "react";

const SAMPLE_HISTORY = [
  { id: 1, title: "Project brainstorming session", date: "Today" },
  { id: 2, title: "Help with quarterly report", date: "Today" },
  { id: 3, title: "Python script for data parsing", date: "Yesterday" },
  { id: 4, title: "Email draft to stakeholders", date: "Yesterday" },
  { id: 5, title: "Marketing copy ideas", date: "Feb 20" },
  { id: 6, title: "API integration questions", date: "Feb 19" },
];



function TypingIndicator() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 5, padding: "4px 0 2px" }}>
      {[0, 1, 2].map((i) => (
        <span key={i} style={{
          width: 6, height: 6, borderRadius: "50%", background: "#b0a898", display: "inline-block",
          animation: "bounce 1.2s infinite ease-in-out", animationDelay: `${i * 0.18}s`,
        }} />
      ))}
    </div>
  );
}

function CollapseIcon({ flipped }) {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
      style={{ transform: flipped ? "scaleX(-1)" : "none", transition: "transform 0.3s" }}>
      <polyline points="15 18 9 12 15 6"/>
    </svg>
  );
}

function SendIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M22 2L11 13" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/><path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/></svg>;
}

function ChatBubbleIcon() {
  return <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>;
}

function PlusIcon() {
  return <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><path d="M12 5v14M5 12h14"/></svg>;
}

function SettingsIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>;
}

function HelpIcon() {
  return <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17" strokeWidth="2.5"/></svg>;
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeChat, setActiveChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [activeSection, setActiveSection] = useState("chat");
  const [toggles, setToggles] = useState({ notifications: true, sounds: false, compact: false, suggestions: true });
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, typing]);

  const startNewChat = () => {
    setActiveChat(null);
    setMessages([]);
    setInput("");
    setActiveSection("chat");
  };

  const loadChat = (chat) => {
    setActiveChat(chat);
    setMessages([
      { id: 1, role: "user", text: chat.title, time: chat.date },
      { id: 2, role: "assistant", text: "Sure! Here's what I found regarding that topic. This is a placeholder — connect your backend to load real conversation history.", time: chat.date },
    ]);
    setActiveSection("chat");
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg = { id: Date.now(), role: "user", text: input.trim(), time: now };
    if (!activeChat) setActiveChat({ id: Date.now(), title: input.trim().slice(0, 40), date: "Today" });
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    if (textareaRef.current) { textareaRef.current.style.height = "24px"; }
    setTyping(true);
    await new Promise((r) => setTimeout(r, 1200 + Math.random() * 600));
    setTyping(false);
    setMessages((prev) => [...prev, {
      id: Date.now() + 1, role: "assistant",
      text: "Thanks for your message! This is a placeholder response. Connect me to your backend to get real AI responses.",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }]);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const autoResize = (e) => {
    e.target.style.height = "24px";
    e.target.style.height = Math.min(e.target.scrollHeight, 160) + "px";
  };

  const flipToggle = (k) => setToggles((p) => ({ ...p, [k]: !p[k] }));

  const grouped = SAMPLE_HISTORY.reduce((acc, c) => {
    (acc[c.date] = acc[c.date] || []).push(c); return acc;
  }, {});

  const isEmptyChat = messages.length === 0;

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Outfit:wght@300;400;500;600&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html, body, #root { height: 100%; width: 100%; overflow: hidden; background: #ebe5dc; font-family: 'Outfit', sans-serif; color: #2e2820; }

        @keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-5px)} }
        @keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
        @keyframes fadeIn { from{opacity:0} to{opacity:1} }

        .app { display:flex; height:100vh; width:100vw; overflow:hidden; }

        /* SIDEBAR */
        .sidebar {
          width: 258px;
          min-width: 258px;
          transform: translateX(0);
          transition: transform 0.28s cubic-bezier(0.4,0,0.2,1), width 0.28s cubic-bezier(0.4,0,0.2,1), min-width 0.28s cubic-bezier(0.4,0,0.2,1);
          background: #ebe5dc;
          border-right: 1px solid #d8d2c8;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-shrink: 0;
        }
        .sidebar.closed { width:0; min-width:0; }

        .sidebar-inner { width:258px; display:flex; flex-direction:column; height:100%; }

        .sidebar-top { padding:14px 12px 12px; display:flex; align-items:center; justify-content:space-between; gap:8px; }

        .brand { font-family:'Instrument Serif',serif; font-size:17px; color:#2e2820; letter-spacing:-0.01em; white-space:nowrap; }

        .icon-btn { background:none; border:none; cursor:pointer; color:#8a8278; width:28px; height:28px; border-radius:7px; display:flex; align-items:center; justify-content:center; transition:background 0.15s,color 0.15s; flex-shrink:0; }
        .icon-btn:hover { background:#d8d2c8; color:#2e2820; }

        .new-chat-btn { margin:4px 10px 8px; background:#2e2820; color:#f2ede6; border:none; border-radius:10px; padding:9px 14px; font-family:'Outfit',sans-serif; font-size:13px; font-weight:500; cursor:pointer; display:flex; align-items:center; gap:8px; transition:background 0.15s; width:calc(100% - 20px); }
        .new-chat-btn:hover { background:#1e1a14; }

        .section-label { font-size:10px; font-weight:600; letter-spacing:0.09em; text-transform:uppercase; color:#a09890; padding:10px 14px 4px; }

        .history-scroll { flex:1; overflow-y:auto; padding:0 6px 6px; scrollbar-width:thin; scrollbar-color:#d0cac0 transparent; }
        .history-scroll::-webkit-scrollbar { width:3px; }
        .history-scroll::-webkit-scrollbar-thumb { background:#d0cac0; border-radius:3px; }

        .date-group-label { font-size:10px; font-weight:600; letter-spacing:0.07em; text-transform:uppercase; color:#b0a898; padding:8px 8px 3px; }

        .history-item { padding:7px 9px; border-radius:8px; font-size:13px; color:#5a5248; cursor:pointer; display:flex; align-items:center; gap:7px; transition:background 0.13s; }
        .history-item span { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
        .history-item:hover { background:#ddd6cc; }
        .history-item.active { background:#d4cdc3; color:#2e2820; font-weight:500; }
        .history-item svg { flex-shrink:0; opacity:0.45; }

        .sidebar-bottom { border-top:1px solid #d8d2c8; padding:8px 6px; display:flex; flex-direction:column; gap:1px; }
        .sidebar-nav { padding:8px 10px; border-radius:8px; font-size:13px; color:#5a5248; cursor:pointer; display:flex; align-items:center; gap:9px; transition:background 0.13s; border:none; background:none; font-family:'Outfit',sans-serif; width:100%; text-align:left; }
        .sidebar-nav:hover { background:#ddd6cc; color:#2e2820; }
        .sidebar-nav.active { background:#d4cdc3; color:#2e2820; font-weight:500; }

        /* MAIN */
        .main { flex:1; display:flex; flex-direction:column; min-width:0; background:#f7f3ee; }

        .topbar { display:flex; align-items:center; gap:10px; padding:0 18px; border-bottom:1px solid #e8e2d8; background:#f7f3ee; height:52px; flex-shrink:0; }
        .topbar-title { font-size:14px; color:#6a6258; font-weight:400; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1; }

        /* CHAT */
        .chat-area { flex:1; overflow-y:auto; display:flex; flex-direction:column; scrollbar-width:thin; scrollbar-color:#ccc7bf transparent; }
        .chat-area::-webkit-scrollbar { width:4px; }
        .chat-area::-webkit-scrollbar-thumb { background:#ccc7bf; border-radius:4px; }

        .messages-wrap { max-width:720px; width:100%; margin:0 auto; padding:28px 28px 0; display:flex; flex-direction:column; gap:0; flex:1; }

        .welcome { display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; padding:40px 28px; animation:fadeIn 0.4s ease; }
        .welcome h1 { font-family:'Instrument Serif',serif; font-size:34px; color:#2e2820; margin-bottom:8px; font-weight:400; }
        .welcome p { font-size:14.5px; color:#a09890; margin-bottom:32px; font-weight:300; }


        .message-group { animation:fadeUp 0.28s ease forwards; margin-bottom:18px; }
        .message-row { display:flex; gap:13px; }
        .message-row.user { flex-direction:row-reverse; }

        .msg-avatar { width:30px; height:30px; border-radius:50%; flex-shrink:0; display:flex; align-items:center; justify-content:center; font-size:13px; margin-top:2px; }
        .msg-avatar.assistant { background:linear-gradient(135deg,#c8bfb0,#b5a898); box-shadow:0 1px 4px rgba(60,50,40,0.12); color:#fff; }
        .msg-avatar.user { background:#2e2820; color:#f2ede6; font-size:11px; font-weight:600; font-family:'Outfit',sans-serif; }

        .bubble-col { display:flex; flex-direction:column; max-width:calc(100% - 44px); }
        .bubble { padding:11px 15px; border-radius:16px; font-size:14.5px; line-height:1.62; word-break:break-word; }
        .bubble.assistant { background:#fff; color:#2e2820; border:1px solid #e4ddd3; border-bottom-left-radius:4px; box-shadow:0 1px 4px rgba(60,50,40,0.06); }
        .bubble.user { background:#2e2820; color:#f5f0e8; border-bottom-right-radius:4px; align-self:flex-end; }
        .msg-time { font-size:10px; color:#b8b0a5; margin-top:4px; padding:0 4px; }
        .message-row.user .msg-time { text-align:right; }

        /* INPUT */
        .input-section { flex-shrink:0; padding:14px 24px 18px; background:#f7f3ee; border-top:1px solid #e8e2d8; }
        .input-container { max-width:720px; margin:0 auto; }
        .input-box { background:#fff; border:1.5px solid #ddd7cd; border-radius:16px; padding:11px 14px; display:flex; align-items:flex-end; gap:10px; box-shadow:0 2px 10px rgba(60,50,40,0.07); transition:border-color 0.2s,box-shadow 0.2s; }
        .input-box:focus-within { border-color:#b0a898; box-shadow:0 2px 16px rgba(60,50,40,0.10); }
        textarea { flex:1; border:none; outline:none; background:transparent; font-family:'Outfit',sans-serif; font-size:14.5px; color:#2e2820; resize:none; line-height:1.55; height:24px; max-height:160px; font-weight:300; }
        textarea::placeholder { color:#c0b8ae; }
        .send-btn { width:34px; height:34px; border-radius:9px; background:#2e2820; border:none; cursor:pointer; display:flex; align-items:center; justify-content:center; color:#f5f0e8; transition:background 0.15s,transform 0.1s; flex-shrink:0; }
        .send-btn:hover { background:#1e1a14; }
        .send-btn:active { transform:scale(0.93); }
        .send-btn:disabled { background:#ccc7bf; cursor:not-allowed; }
        .input-hint { text-align:center; font-size:11px; color:#c0b8ae; margin-top:7px; font-weight:300; }

        /* SETTINGS / HELP */
        .content-panel { flex:1; overflow-y:auto; padding:36px 40px; animation:fadeIn 0.25s ease; }
        .panel-title { font-family:'Instrument Serif',serif; font-size:26px; font-weight:400; color:#2e2820; margin-bottom:6px; }
        .panel-sub { font-size:13.5px; color:#a09890; margin-bottom:28px; font-weight:300; }
        .card-group { background:#fff; border:1px solid #e4ddd3; border-radius:14px; overflow:hidden; margin-bottom:16px; box-shadow:0 1px 4px rgba(60,50,40,0.05); }
        .card-group-label { font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#a09890; padding:13px 18px 7px; border-bottom:1px solid #f0ebe2; }
        .card-row { display:flex; align-items:center; justify-content:space-between; padding:13px 18px; border-bottom:1px solid #f2ede6; gap:16px; }
        .card-row:last-child { border-bottom:none; }
        .card-row-label { font-size:13.5px; color:#2e2820; }
        .card-row-sub { font-size:12px; color:#a09890; margin-top:2px; font-weight:300; }
        .toggle { width:38px; height:21px; border-radius:11px; background:#c8bfb0; border:none; cursor:pointer; position:relative; transition:background 0.2s; flex-shrink:0; }
        .toggle.on { background:#2e2820; }
        .toggle::after { content:''; position:absolute; top:3px; left:3px; width:15px; height:15px; border-radius:50%; background:#fff; transition:transform 0.2s; box-shadow:0 1px 3px rgba(0,0,0,0.15); }
        .toggle.on::after { transform:translateX(17px); }
        .ghost-btn { font-size:12px; padding:6px 13px; border-radius:8px; border:1.5px solid #e4ddd3; background:none; cursor:pointer; color:#7a7168; font-family:'Outfit',sans-serif; transition:background 0.15s; }
        .ghost-btn:hover { background:#f2ede6; }

        .help-card { background:#fff; border:1px solid #e4ddd3; border-radius:12px; padding:16px 18px; margin-bottom:10px; box-shadow:0 1px 4px rgba(60,50,40,0.05); }
        .help-card h3 { font-size:14px; font-weight:600; color:#2e2820; margin-bottom:5px; display:flex; align-items:center; gap:8px; }
        .help-card p { font-size:13px; color:#7a7168; line-height:1.55; font-weight:300; }
      `}</style>

      <div className="app">
        {/* ── SIDEBAR ── */}
        <div className={`sidebar${sidebarOpen ? "" : " closed"}`}>
          <div className="sidebar-inner">
            <div className="sidebar-top">
              <span className="brand">Assistant</span>
              <button className="icon-btn" onClick={() => setSidebarOpen(false)} title="Collapse">
                <CollapseIcon />
              </button>
            </div>

            <button className="new-chat-btn" onClick={startNewChat}>
              <PlusIcon /> New conversation
            </button>

            <div className="section-label">Recents</div>

            <div className="history-scroll">
              {Object.entries(grouped).map(([date, chats]) => (
                <div key={date}>
                  <div className="date-group-label">{date}</div>
                  {chats.map((c) => (
                    <div
                      key={c.id}
                      className={`history-item${activeChat?.id === c.id ? " active" : ""}`}
                      onClick={() => loadChat(c)}
                    >
                      <ChatBubbleIcon />
                      <span>{c.title}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            <div className="sidebar-bottom">
              <button
                className={`sidebar-nav${activeSection === "settings" ? " active" : ""}`}
                onClick={() => setActiveSection(s => s === "settings" ? "chat" : "settings")}
              >
                <SettingsIcon /> Settings
              </button>
              <button
                className={`sidebar-nav${activeSection === "help" ? " active" : ""}`}
                onClick={() => setActiveSection(s => s === "help" ? "chat" : "help")}
              >
                <HelpIcon /> Help & Docs
              </button>
            </div>
          </div>
        </div>

        {/* ── MAIN ── */}
        <div className="main">
          <div className="topbar">
            {!sidebarOpen && (
              <button className="icon-btn" onClick={() => setSidebarOpen(true)} title="Open sidebar">
                <CollapseIcon flipped />
              </button>
            )}
            <span className="topbar-title">
              {activeSection === "settings" ? "Settings" :
               activeSection === "help" ? "Help & Documentation" :
               activeChat ? activeChat.title : "New conversation"}
            </span>
          </div>

          {activeSection === "settings" ? (
            <div className="content-panel">
              <div className="panel-title">Settings</div>
              <div className="panel-sub">Manage your preferences and customize your experience.</div>

              <div className="card-group">
                <div className="card-group-label">Interface</div>
                {[
                  { key: "compact", label: "Compact mode", sub: "Reduce spacing between messages" },
                  { key: "suggestions", label: "Show suggestions", sub: "Show prompt suggestions on new chats" },
                ].map(({ key, label, sub }) => (
                  <div className="card-row" key={key}>
                    <div><div className="card-row-label">{label}</div><div className="card-row-sub">{sub}</div></div>
                    <button className={`toggle${toggles[key] ? " on" : ""}`} onClick={() => flipToggle(key)} />
                  </div>
                ))}
              </div>

              <div className="card-group">
                <div className="card-group-label">Notifications</div>
                {[
                  { key: "notifications", label: "Enable notifications", sub: "Get notified when responses arrive" },
                  { key: "sounds", label: "Sound effects", sub: "Play a sound on message send/receive" },
                ].map(({ key, label, sub }) => (
                  <div className="card-row" key={key}>
                    <div><div className="card-row-label">{label}</div><div className="card-row-sub">{sub}</div></div>
                    <button className={`toggle${toggles[key] ? " on" : ""}`} onClick={() => flipToggle(key)} />
                  </div>
                ))}
              </div>

              <div className="card-group">
                <div className="card-group-label">Data</div>
                <div className="card-row">
                  <div><div className="card-row-label">Clear conversation history</div><div className="card-row-sub">Permanently delete all past chats</div></div>
                  <button className="ghost-btn">Clear all</button>
                </div>
              </div>
            </div>
          ) : activeSection === "help" ? (
            <div className="content-panel">
              <div className="panel-title">Help & Docs</div>
              <div className="panel-sub">Everything you need to get the most out of your assistant.</div>
              {[
                { icon: "⌨️", title: "Keyboard shortcuts", body: "Press Enter to send. Use Shift+Enter to add a new line without sending." },
                { icon: "🗂️", title: "Chat history", body: "Conversations are saved automatically in the sidebar. Click any past chat to resume." },
                { icon: "🔌", title: "Connecting your backend", body: "Replace the mock response in the sendMessage function with a real API call to your LLM or backend service." },
                { icon: "🎨", title: "Customizing the UI", body: "All colors are controlled via CSS. Update the palette variables to match your brand." },
                { icon: "💬", title: "Better responses", body: "Be specific and detailed in your prompts. Provide context, examples, and desired output format." },
              ].map((item) => (
                <div className="help-card" key={item.title}>
                  <h3><span>{item.icon}</span>{item.title}</h3>
                  <p>{item.body}</p>
                </div>
              ))}
            </div>
          ) : (
            <>
              <div className="chat-area">
                {isEmptyChat ? (
                  <div className="welcome">
                    <h1>How can I help?</h1>
                    <p>Ask me anything to get started.</p>
                  </div>
                ) : (
                  <div className="messages-wrap">
                    {messages.map((msg) => (
                      <div key={msg.id} className="message-group">
                        <div className={`message-row ${msg.role}`}>
                          <div className={`msg-avatar ${msg.role}`}>
                            {msg.role === "assistant" ? "✦" : "U"}
                          </div>
                          <div className="bubble-col">
                            <div className={`bubble ${msg.role}`}>{msg.text}</div>
                            <div className="msg-time">{msg.time}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                    {typing && (
                      <div className="message-group">
                        <div className="message-row assistant">
                          <div className="msg-avatar assistant">✦</div>
                          <div className="bubble-col">
                            <div className="bubble assistant"><TypingIndicator /></div>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={bottomRef} style={{ height: 28 }} />
                  </div>
                )}
              </div>

              <div className="input-section">
                <div className="input-container">
                  <div className="input-box">
                    <textarea
                      ref={textareaRef}
                      value={input}
                      onChange={(e) => { setInput(e.target.value); autoResize(e); }}
                      onKeyDown={handleKey}
                      placeholder="Message your assistant…"
                      rows={1}
                    />
                    <button className="send-btn" onClick={sendMessage} disabled={!input.trim() || typing} aria-label="Send">
                      <SendIcon />
                    </button>
                  </div>
                  <div className="input-hint">Enter to send · Shift+Enter for new line</div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
}
