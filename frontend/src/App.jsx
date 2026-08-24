import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const SUGGESTIONS = [
  {
    label: "Track my order",
    desc: "Get live updates on your order status",
    prompt: "What is the status of order ORD-1001?",
    color: "orange",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M3.27 6.96 12 12.01l8.73-5.05M12 22.08V12"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    label: "Return policy",
    desc: "Learn about our 30-day return window",
    prompt: "What is the standard return period?",
    color: "blue",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M9 14 4 9l5-5"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M4 9h11a5 5 0 0 1 5 5v0a5 5 0 0 1-5 5H8"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
  {
    label: "Shipping information",
    desc: "Delivery times, zones, and costs",
    prompt: "Do you ship to Canada?",
    color: "teal",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M1 3h13v13H1z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M14 8h4l3 3v5h-7V8Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <circle cx="5.5" cy="18.5" r="1.8" stroke="currentColor" strokeWidth="2" />
        <circle cx="17.5" cy="18.5" r="1.8" stroke="currentColor" strokeWidth="2" />
      </svg>
    ),
  },
  {
    label: "Warranty information",
    desc: "Coverage details for your products",
    prompt: "What is the warranty period for bags?",
    color: "purple",
    icon: (
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M12 2 4 5v6c0 5 3.4 9 8 11 4.6-2 8-6 8-11V5l-8-3Z"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
  },
];

function Avatar({ size = "md" }) {
  return (
    <div className={`ar-avatar ar-avatar-${size}`}>
      <span>A</span>
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: userMessage,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, I couldn't connect to the support service. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setInput("");
  };

  const useSuggestion = (text) => {
    setInput(text);
  };

  return (
    <div className="ar-app">
      <div className="ar-chat-container">

        {/* HEADER */}
        <header className="ar-header">
          <div className="ar-brand">
            <Avatar size="md" />
            <div className="ar-brand-text">
              <h1>Aster &amp; Row</h1>
              <p>AI Customer Support</p>
            </div>
          </div>

          <div className="ar-header-actions">
            <div className="ar-status">
              <span className="ar-status-dot"></span>
              Online
            </div>

            {messages.length > 0 && (
              <button
                className="ar-clear-button"
                onClick={clearChat}
                disabled={loading}
              >
                Clear chat
              </button>
            )}
          </div>
        </header>

        {/* MESSAGES */}
        <main className="ar-messages">

          {messages.length === 0 && (
            <div className="ar-welcome">
              <div className="ar-welcome-icon">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z"
                    fill="white"
                  />
                </svg>
              </div>

              <h2 className="ar-welcome-title">How can we help you today?</h2>

              <p className="ar-welcome-subtitle">
                Get instant answers about orders, returns,
                shipping, warranties, and more.
              </p>

              <div className="ar-suggestions">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s.label}
                    className="ar-suggestion-card"
                    onClick={() => useSuggestion(s.prompt)}
                  >
                    <span className={`ar-suggestion-icon ar-icon-${s.color}`}>
                      {s.icon}
                    </span>
                    <span className="ar-suggestion-text">
                      <span className="ar-suggestion-title">{s.label}</span>
                      <span className="ar-suggestion-desc">{s.desc}</span>
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`ar-message ar-message-${message.role}`}
            >
              {message.role === "assistant" && <Avatar size="sm" />}
              <div className="ar-bubble">
                <ReactMarkdown>
                  {message.content}
                </ReactMarkdown>
              </div>
            </div>
          ))}

          {/* LOADING */}
          {loading && (
            <div className="ar-message ar-message-assistant">
              <Avatar size="sm" />
              <div className="ar-bubble ar-typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

        </main>

        {/* INPUT */}
        <div className="ar-input-area">

          <input
            type="text"
            placeholder={
              loading
                ? "AI is thinking..."
                : "Ask something..."
            }
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
          />

          <button
            className="ar-send-button"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M22 2 11 13"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M22 2 15 22l-4-9-9-4 20-7Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>

        </div>

      </div>
    </div>
  );
}

export default App;