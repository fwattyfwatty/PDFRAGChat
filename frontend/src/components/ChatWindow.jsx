import React, { useState, useEffect, useRef } from 'react';
import useChat from '../hooks/useChat';

function ChatWindow({ sessionId }) {
  const [input, setInput] = useState('');
  const { messages, sendMessage, isConnected } = useChat(sessionId);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim() && isConnected) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ flexGrow: 1, overflowY: 'auto', border: '1px solid #eee', padding: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '10px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
            <span style={{ background: msg.role === 'user' ? '#dcf8c6' : '#f1f0f0', padding: '8px', borderRadius: '7px' }}>
              {msg.content}
            </span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSend} style={{ display: 'flex', padding: '10px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ flexGrow: 1, padding: '8px' }}
          placeholder={isConnected ? "メッセージを入力..." : "接続中..."}
          disabled={!isConnected}
        />
        <button type="submit" disabled={!isConnected}>送信</button>
      </form>
    </div>
  );
}

export default ChatWindow;